"""
Holds the Anki menu integration and configuration options for the addon
"""

from aqt import mw
from aqt.qt import *

from .search import Search


def invoke_addon_window():
    """
    Load and open the addon

    In order to display the widget, we must assign it to the top-level mw.
    This prevents garbage collection once this function has exited.
    https://apps.ankiweb.net/docs/addons.html#qt
    """
    mw.find_missing_words_widget = window = Search(mw)
    window.show()


def initialize_menu_item():
    """
    Create menu item for addon in Anki "Tools" menu
    """
    action = QAction("Find Missing Words", mw)
    action.triggered.connect(invoke_addon_window)
    mw.form.menuTools.addAction(action)
