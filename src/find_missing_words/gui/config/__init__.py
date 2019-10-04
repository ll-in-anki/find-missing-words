"""
Config dialog entry point.
This module will load the config initially for the tabs.
Each tab of the config will write to the config itself.
"""
from aqt import mw
from aqt.qt import *

from ..forms import config as config_form
from .search_tab import SearchTab
from .note_creation_tab import NoteCreationTab


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.mw = mw
        self.config = mw.addonManager.getConfig(__name__)
        self.form = config_form.Ui_Dialog()
        self.form.setupUi(self)
        self.render_tabs()

    def render_tabs(self):
        self.search_tab = search_tab.SearchTab(self.config)
        self.note_creation_tab = NoteCreationTab(self.config)
        self.form.tab_widget.addTab(self.search_tab, "Search")
        self.form.tab_widget.addTab(self.note_creation_tab, "Note Creation")

    def accept(self):
        self.search_tab.set_default_deck()
        self.search_tab.set_default_note_fields()
        self.search_tab.set_default_deck_toggle()
        self.search_tab.set_default_note_fields_toggle()
        self.note_creation_tab.save_presets()
        super().accept()
