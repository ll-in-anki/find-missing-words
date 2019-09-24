from aqt import mw, deckchooser
from aqt.qt import *

from .forms import config as config_form
from . import note_field_chooser


class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.mw = mw

        self.form = config_form.Ui_Dialog()
        self.form.setupUi(self)
        self.render_default_deck_chooser()
        self.render_default_note_field_chooser()
        self.load_config()

    def render_default_deck_chooser(self):
        self.default_deck_chooser_parent_widget = QWidget()
        self.default_deck_chooser = deckchooser.DeckChooser(mw, self.default_deck_chooser_parent_widget)
        self.default_deck_chooser.deck.clicked.connect(self.update_default_deck)
        self.form.default_deck_hbox.addWidget(self.default_deck_chooser_parent_widget)

    def update_default_deck(self):
        new_deck_name = self.default_deck_chooser.deckName()
        config = mw.addonManager.getConfig(__name__)
        mw.addonManager.writeConfig(__name__, config.update({"default_deck": new_deck_name}))

    def render_default_note_field_chooser(self):
        self.default_note_field_chooser_parent_widget = QWidget()
        self.default_note_field_chooser = note_field_chooser.NoteFieldChooser(mw, self.default_note_field_chooser_parent_widget)
        self.default_note_field_chooser.deck.clicked.connect(self.update_default_note_fields)
        self.form.default_note_field_hbox.addWidget(self.default_note_field_chooser_parent_widget)

    def update_default_note_fields(self):
        new_selected_items = self.default_note_field_chooser.selected_items
        config = mw.addonManager.getConfig(__name__)
        mw.addonManager.writeConfig(__name__, config.update({"default_note_fields": new_selected_items}))

    def load_config(self):
        configured_default_deck = mw.addonManager.getConfig(__name__)["default_deck"]
        if configured_default_deck:
            self.default_deck_chooser.setDeckName(configured_default_deck)

        # TODO pass new selected_items arg to note_field_tree through note_field_chooser
