from aqt.qt import *

from . import find_missing


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.render()

    def render(self):
        self.tab_1 = QWidget()
        self.addTab(self.tab_1, "Find Missing Words")
        self.setTabText(0, "Find Missing Words")
        find_missing_layout = find_missing.FindMissingWords()
        self.tab_1.setLayout(find_missing_layout)
