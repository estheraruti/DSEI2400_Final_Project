from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont


class MyWebBrowser:
    def __init__(self):
        self.window = QWidget()
        self.window.setWindowTitle("Web Browser")

        # Create a vertical layout
        self.layout = QVBoxLayout()

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

    def navigate(self):
        term = self.url_bar.text()
        if not term.startswith("http"):
            term = f"http://www.google.com/search?q={term}"
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


# Initialize the application and the main window
app = QApplication([])
window = MyWebBrowser()
app.exec_()
