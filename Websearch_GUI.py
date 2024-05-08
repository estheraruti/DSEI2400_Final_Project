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
        self.search_prompt_label.setFont(QFont('Arial', 14))  # Smaller font size
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
        self.web_search(term)
        self.extract_text_and_find_urls()

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
                          "https://duckduckgo.com/?q=": "duckduckgo",
                          "https://search.aol.com/aol/search?q=": "aol",
                         "https://www.ask.com/web?q=": "ask"}

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

        # Function to count occurrences of terms in a URL
        def count_term_occurrences(query, url):
            # Count occurrences of each term in the URL
            return sum(1 for word in query.split() if word in url)

        # List to temporarily store DataFrames for each URL
        dfs = []

        for idx, row in self.df.iterrows():
            img_path = row['img_paths']
            pic_name = row['query'].replace(' ', '_')
            search_engine = row['search_engine']

            # Extract text from image
            image = cv2.imread(img_path)
            text = pytesseract.image_to_string(image)

            # Create a unique text file name
            txt_path = os.path.join(Text_Folder, f"{pic_name}_{search_engine}.txt")

            # Write contents to file
            with open(txt_path, 'w') as text_file:
                text_file.write(text)

            # Store text file path in DataFrame
            row['txt_paths'] = txt_path

            # Extract URLs using regex
            with open(txt_path, 'r') as text_file:
                file_contents = text_file.read()
                urls = re.findall(r'(www\.[^\s]+|https?://[^\s]+)', file_contents)

            # Clean and normalize URLs
            for i, url in enumerate(urls):
                urls[i] = re.sub(r'^h[a-z]*:', 'https:', url)
                urls[i] = re.sub(r':/A\w\w\w\.', 'https://www.', url)

            # Process each URL individually
            for url in urls:
                term_count = count_term_occurrences(row['query'], url)

                # Create a new DataFrame for each URL
                url_df = pd.DataFrame({
                    'query': [row['query']],
                    'search_engine': [row['search_engine']],
                    'url': [url],
                    'term_count': [term_count],
                    'txt_paths': [row['txt_paths']]
                })

                # Append the DataFrame to the list of DataFrames
                dfs.append(url_df)

        # Concatenate all DataFrames
        self.df = pd.concat(dfs, ignore_index=True)
        print("Successfully counted search terms in each URL.")

        # Save the DataFrame to the database (code remains unchanged)
        import mysql.connector
        from sqlalchemy import create_engine

        user = input("Enter your MYSQL username")
        password = input("Enter your MYSQL password")
        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password
        )

        # Define the connection string
        connection_string = 'mysql+mysqlconnector://' + user + ':' + password + '@localhost/MY_CUSTOM_BOT'

        # Create a SQLAlchemy engine
        engine = create_engine(connection_string)

        # Save the DataFrame to the database
        self.df.to_sql(name='search', con=engine, if_exists='replace', index=False)

        # Dispose the engine
        engine.dispose()

        sql_query = "SELECT * FROM MY_CUSTOM_BOT.search ORDER BY term_count DESC"
        self.sql_df = pd.read_sql(sql_query, conn)
        self.sql_df.sort_values(by='term_count', ascending=False, inplace=True)
        print("Successfully appended the DataFrame to MYSQL database")
        print(self.sql_df.head())
        
        # converting the dataframe to html
        final_table_html = self.sql_df.to_html(index=False)
        self.browser.setHtml(final_table_html)
# Initialize the application and the main window
app = QApplication([])
window = MyWebBrowser()
app.exec_()
