from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import cv2
import pytesseract
import re

class MyWebBrowser:
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Web Browser")

        # Create a vertical layout
        self.layout = QVBoxLayout()
        self.browser = QWebEngineView()

        # Create a label prompting the user to enter their search term
        self.search_prompt_label = QLabel("Enter your query below")
        self.search_prompt_label.setMaximumHeight(20)  # Reduced height
        self.search_prompt_label.setFont(QFont('Sans Serif', 14))  # Smaller font size
        self.layout.addWidget(self.search_prompt_label)

        # Create a horizontal layout for the URL bar and buttons
        self.horizontal = QHBoxLayout()

        # Create the URL bar (search bar) using QLineEdit
        self.url_bar = QLineEdit()
        self.url_bar.setMaximumHeight(20)  # Reduced height
        self.url_bar.setFont(QFont('Arial', 10))  # Smaller font size

        # Create the buttons with color
        self.go_btn = QPushButton("Go")
        self.go_btn.setStyleSheet("background-color: #ed82a7; color: white;")
        self.go_btn.setMinimumHeight(30)

        self.back_btn = QPushButton("back")
        self.back_btn.setStyleSheet("background-color: #92c9ef; color: white;")
        self.back_btn.setMinimumHeight(30)

        self.forward_btn = QPushButton("next")
        self.forward_btn.setStyleSheet("background-color: #f8eaa8; color: white;")
        self.forward_btn.setMinimumHeight(30)

        # Create the QWebEngineView for the browser
        self.browser = QWebEngineView()

        # Connect button signals to methods
        self.go_btn.clicked.connect(self.navigate)
        self.back_btn.clicked.connect(self.browser.back)
        self.forward_btn.clicked.connect(self.browser.forward)

        # Add widgets to the horizontal layout
        self.horizontal.addWidget(self.url_bar)
        self.horizontal.addWidget(self.go_btn)
        self.horizontal.addWidget(self.back_btn)
        self.horizontal.addWidget(self.forward_btn)

        # Add the horizontal layout to the main layout
        self.layout.addLayout(self.horizontal)

        self.browser.urlChanged.connect(self.apply_custom_css)  # Apply custom CSS when URL changes

        # Add the browser to the layout
        self.layout.addWidget(self.browser)

        # Set the layout for the main window
        self.window.setLayout(self.layout)
        self.window.show()

        # Initialize Selenium WebDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()

    def navigate(self):
        term = self.url_bar.text()
        if not term.startswith("http"):
            self.web_search(term)
            self.extract_text_and_find_urls()
        else:
            self.browser.setUrl(QUrl(term))

    def apply_custom_css(self):
        # Custom CSS style to set the page background color to light yellow
        custom_css = """
        body { background-color: #FFFFE0; }
        """
        # Inject the custom CSS into the web page
        self.browser.page().runJavaScript(f"""
        var style = document.createElement('style');
        style.type = 'text/css';
        style.innerHTML = `{custom_css}`;
        document.head.appendChild(style);
        """)

    def web_search(self, query):
        SAVE_FOLDER = 'Web_Photos'
        os.makedirs(SAVE_FOLDER, exist_ok=True)
        search_engines = {"http://www.google.com/search?q=": "google",
                          "https://www.bing.com/search?q=": "bing",
                          "https://search.yahoo.com/search?p=": "yahoo",
                          "https://duckduckgo.com/?q=": "duckduckgo"}

        dfs = []  # List to store DataFrames for each iteration

        for url, engine in search_engines.items():
            # getting the webpage
            self.driver.get(url + query)

            # wait for a few seconds for the page to load
            time.sleep(10)

            self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

            # wait a few seconds for the page to load
            time.sleep(10)

            # set the width and height of screenshot
            width = 1920
            height = self.driver.execute_script("return Math.max(document.body.scrollHeight,document.body.offsetHeight,document.documentElement.clientHeight,document.documentElement.scrollHeight,document.documentElement.offsetHeight);")
            self.driver.set_window_size(width, height)

            # take a screenshot
            screenshot_name = query.replace(' ', '_') + "_" + engine + ".png"
            save_path = os.path.join(SAVE_FOLDER, screenshot_name)
            self.driver.save_screenshot(save_path)

            # Create a DataFrame for the current query and engine
            new_df = pd.DataFrame({'query': [query], 'search_engine': [engine], 'img_paths': save_path})
            dfs.append(new_df)

        # Concatenate all DataFrames in the list
        self.df = pd.concat(dfs, ignore_index=True)
        print(self.df.head())
        
    def extract_text_and_find_urls(self):
        
        Text_Folder = "Extracted_Text"
        os.makedirs(Text_Folder, exist_ok=True)

        dfs = []  # List to temporarily store DataFrames for URLs
        for idx, row in self.df.iterrows():
            img_path = row['img_paths']
            pic_name = row['query'].replace(' ', '_')  # Construct unique file name
            search_engine = row['search_engine']  # Retrieve search engine from DataFrame

            # extract text from image
            image = cv2.imread(img_path)
            text = pytesseract.image_to_string(image)

            # Create a unique text file name
            txt_path = os.path.join(Text_Folder, f"{pic_name}_{search_engine}.txt")

            # write contents to file
            with open(txt_path, 'w') as text_file:
                text_file.write(text)

            # Store text file path in DataFrame
            row['txt_paths'] = txt_path

            with open(txt_path, 'r') as text_file:
                file_contents = text_file.read()
                urls = re.findall(r'(www\.[^\s]+|https?://[^\s]+)', file_contents)
                row['urls'] = urls

            # clean URLs
            for i, url in enumerate(row['urls']):
                row['urls'][i] = re.sub(r'^h[a-z]*:', 'https:', url)
                row['urls'][i] = re.sub(r':/A\w\w\w\.', 'https://www.', url)

            dfs.append(row)

        # Update the main DataFrame
        self.df = pd.DataFrame(dfs)
        print("Successfully cleaned URLs and appended to df.")
        print(self.df.head())


# Initialize the application and the main window
app = QApplication([])
window = MyWebBrowser()
app.exec_()
