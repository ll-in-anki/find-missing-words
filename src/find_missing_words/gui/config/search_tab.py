from aqt import mw, deckchooser
from aqt.qt import *

from ..utils import note_field_chooser
from ..forms import config_search_tab as search_form
from .properties import ConfigProperties


class SearchTab(QWidget):
    """
    Config tab to handle user preferences for search filters.
    Holds config for default deck, default notes and fields, and ignored words.
    """
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.default_deck = ""
        self.default_note_fields = []

        self.form = search_form.Ui_Form()
        self.form.setupUi(self)
        self.load_config()
        self.render_default_deck_chooser()
        self.render_default_note_field_chooser()
        self.populate_ignored_words()

    def load_config(self):
        self.filter_deck = self.config[ConfigProperties.FILTER_DECK.value]
        self.filter_note_fields = self.config[ConfigProperties.FILTER_NOTE_FIELDS.value]
        self.default_deck = self.config[ConfigProperties.DECK.value]
        self.default_note_fields = self.config[ConfigProperties.NOTE_FIELDS.value]
        self.ignored_words = self.config[ConfigProperties.IGNORED_WORDS.value]

    def render_default_deck_chooser(self):
        self.default_deck_chooser_parent_widget = QWidget()
        self.default_deck_chooser = deckchooser.DeckChooser(mw, self.default_deck_chooser_parent_widget, label=False)
        self.form.default_deck_checkbox.setChecked(self.filter_deck)
        self.default_deck_chooser_parent_widget.setEnabled(self.filter_deck)
        if self.default_deck:
            self.default_deck_chooser.setDeckName(self.default_deck)
        self.form.default_deck_checkbox.stateChanged.connect(self.toggle_default_deck)
        self.form.default_deck_hbox.addWidget(self.default_deck_chooser_parent_widget)

    def toggle_default_deck(self):
        self.filter_deck = not self.filter_deck
        self.default_deck_chooser_parent_widget.setEnabled(self.filter_deck)

    def set_default_deck_toggle(self):
        self.config.update({ConfigProperties.FILTER_DECK.value: self.filter_deck})
        mw.addonManager.writeConfig(__name__, self.config)

    def set_default_deck(self):
        new_deck_name = self.default_deck_chooser.deckName()
        self.config.update({"default_deck": new_deck_name})
        mw.addonManager.writeConfig(__name__, self.config)

    def render_default_note_field_chooser(self):
        self.default_note_field_chooser = note_field_chooser.NoteFieldChooser(parent=self)
        self.form.default_note_field_checkbox.setChecked(self.filter_note_fields)
        self.default_note_field_chooser.setEnabled(self.filter_note_fields)
        if self.default_note_fields:
            self.default_note_field_chooser.set_selected_items(self.default_note_fields)
        self.form.default_note_field_checkbox.stateChanged.connect(self.toggle_default_note_fields)
        self.form.default_note_field_hbox.addWidget(self.default_note_field_chooser)

    def toggle_default_note_fields(self):
        self.filter_note_fields = not self.filter_note_fields
        self.default_note_field_chooser.setEnabled(self.filter_note_fields)

    def set_default_note_fields_toggle(self):
        self.config.update({ConfigProperties.FILTER_NOTE_FIELDS.value: self.filter_note_fields})
        mw.addonManager.writeConfig(__name__, self.config)

    def set_default_note_fields(self):
        new_selected_items = self.default_note_field_chooser.selected_items
        self.config.update({"default_notes_and_fields": new_selected_items})
        mw.addonManager.writeConfig(__name__, self.config)

    def populate_ignored_words(self):
        ignored_words_text = ", ".join(self.ignored_words)
        self.form.ignored_words_text_area.setText(ignored_words_text)

    def save_ignored_words(self):
        text_area_words = set([word.strip().lower() for word in self.form.ignored_words_text_area.toPlainText().split(",")])
        ignored_words = sorted(list(text_area_words))
        self.config.update({ConfigProperties.IGNORED_WORDS.value: ignored_words})
        mw.addonManager.writeConfig(__name__, self.config)
