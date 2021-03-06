"""
Holds the Anki menu integration and configuration options for the addon
"""

from aqt import mw
from aqt.qt import *

from .search import Search
from .config import ConfigDialog

ADDON_NAME = "Find Missing Words"


def invoke_config_window():
    """
    Launch custom GUI on config change instead of default Anki JSON editor
    """
    mw.find_missing_words_config = config = ConfigDialog(mw)
    config.exec_()


def initialize_config_menu_item():
    """
    Add option for addon's config in Anki
    :return:
    """
    mw.addonManager.setConfigAction(__name__, invoke_config_window)


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
    action = QAction(ADDON_NAME, mw)
    action.triggered.connect(invoke_addon_window)
    mw.form.menuTools.addAction(action)


def cleanup_menu_items():
    """
    Remove any duplicate menu items for the addon in Anki "Tools" menu
    Used in development when the addon (at therefore its menu item) is reloaded multiple times within an Anki session.
    """
    old_actions = [action for action in mw.form.menuTools.actions() if action.text() == ADDON_NAME]
    for action in old_actions:
        mw.form.menuTools.removeAction(action)
