import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QPushButton, QAction
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt  # Import Qt
from PyQt5.QtGui import QIcon

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the browser view
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Set up the navigation bar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        self.home_button = QPushButton("Home")
        self.home_button.clicked.connect(self.navigate_home)
        self.toolbar.addWidget(self.home_button)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.browser.back)
        self.toolbar.addWidget(self.back_button)

        self.reload_button = QPushButton("Reload")
        self.reload_button.clicked.connect(self.browser.reload)
        self.toolbar.addWidget(self.reload_button)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.bookmark_button = QPushButton("Bookmark")
        self.bookmark_button.clicked.connect(self.add_bookmark)
        self.toolbar.addWidget(self.bookmark_button)

        # Bookmarks toolbar
        self.bookmarks_toolbar = QToolBar("Bookmarks")
        self.addToolBar(Qt.BottomToolBarArea, self.bookmarks_toolbar)

        # Quick links toolbar
        self.quick_links_toolbar = QToolBar("Quick Links")
        self.addToolBar(Qt.TopToolBarArea, self.quick_links_toolbar)

        # Add quick links
        quick_link_google = QAction(QIcon("https://www.google.com/favicon.ico"), "Google", self)
        quick_link_google.triggered.connect(lambda: self.browser.setUrl(QUrl("https://www.google.com")))
        self.quick_links_toolbar.addAction(quick_link_google)

        quick_link_youtube = QAction(QIcon("https://www.youtube.com/favicon.ico"), "YouTube", self)
        quick_link_youtube.triggered.connect(lambda: self.browser.setUrl(QUrl("https://www.youtube.com")))
        self.quick_links_toolbar.addAction(quick_link_youtube)

        self.navigate_home()

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

    def add_bookmark(self):
        url = self.browser.url().toString()
        title = self.browser.page().title()
        favicon_url = self.get_favicon_url(url)
        action = QAction(QIcon(favicon_url), title, self)
        action.triggered.connect(lambda: self.browser.setUrl(QUrl(url)))
        self.bookmarks_toolbar.addAction(action)

    def get_favicon_url(self, url):
        domain = QUrl(url).host()
        return f"https://www.google.com/s2/favicons?domain={domain}"

app = QApplication(sys.argv)
QApplication.setApplicationName("PyBrowser")
window = Browser()
app.exec_()
