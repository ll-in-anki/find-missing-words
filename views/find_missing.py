from aqt.qt import *


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.render()

    def render(self):
        self.text = QTextEdit()
        self.addWidget(self.text)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)
        btnLayout.addWidget(self.search_button)
        self.addLayout(btnLayout)

    def search(self):
        # Search through fetched cards here
        pass
