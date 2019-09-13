from aqt import mw
from aqt.qt import *

from .search import Search


def invoke_addon_window():
    # Prevent garbage collection my assigning widget to top-level mw
    mw.find_missing_words_widget = window = Search(mw)
    window.show()


def initialize_menu_item():
    action = QAction("Find Missing Words", mw)
    action.triggered.connect(invoke_addon_window)
    mw.form.menuTools.addAction(action)
