from aqt import mw
from aqt.qt import *

from .search import Search


def invoke_addon_window():
    window = Search()


def initialize_menu_item():
    action = QAction("Find Missing Words", mw)
    action.triggered.connect(invoke_addon_window)
    mw.form.menuTools.addAction(action)
