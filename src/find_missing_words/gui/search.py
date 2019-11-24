"""
First view of the addon: search

Enter search queries and filter by decks, note types, and fields
"""

from aqt import mw, deckchooser
from aqt.qt import *
from anki.hooks import addHook, remHook

from .forms import search as search_form
from .utils import note_field_chooser
from .search_results import note_creation
from .config.properties import ConfigProperties
from . import utils


class Search(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set up UI from pre-generated UI form:
        self.form = search_form.Ui_Dialog()
        self.form.setupUi(self)

        self.REPLACEMENT_STRING = "[[[WORD]]]"

        self.deck_selection_enabled = True
        self.note_field_selection_enabled = False
        self.note_field_items = self.note_field_selected_items = []
        self.selected_decks = []
        self.deck_name = ""
        self.note_creation_window = None

        self.render_deck_chooser()
        self.render_note_field_chooser()
        self.form.search_button.clicked.connect(self.search)
        addHook("search_missing_words", self.search)

    def render_deck_chooser(self):
        self.deck_chooser_parent_widget = QWidget()
        self.deck_chooser = deckchooser.DeckChooser(mw, self.deck_chooser_parent_widget, label=False)
        filter_on_decks = mw.addonManager.getConfig(__name__)[ConfigProperties.FILTER_DECK.value]
        if filter_on_decks:
            default_deck_name = mw.addonManager.getConfig(__name__)[ConfigProperties.DECK.value]
            self.deck_chooser.setDeckName(default_deck_name)
            self.deck_selection_enabled = True
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)
        self.form.filter_decks_checkbox.setChecked(self.deck_selection_enabled)

        self.form.filter_decks_checkbox.stateChanged.connect(self.toggle_deck_selection)
        self.deck_chooser.deck.clicked.connect(self.update_deck_name)

        self.update_init_search()

        self.form.filter_decks_hbox.addWidget(self.deck_chooser_parent_widget)

    def update_deck_name(self):
        self.deck_name = self.deck_chooser.deckName()
        self.update_init_search()

    def render_note_field_chooser(self):
        self.note_field_chooser = note_field_chooser.NoteFieldChooser(on_update_callback=self.update_note_fields, parent=self)
        filter_on_note_fields = mw.addonManager.getConfig(__name__)[ConfigProperties.FILTER_NOTE_FIELDS.value]
        if filter_on_note_fields:
            default_note_fields = mw.addonManager.getConfig(__name__)[ConfigProperties.NOTE_FIELDS.value]
            self.note_field_chooser.set_selected_items(default_note_fields)
            self.note_field_selected_items = default_note_fields
            self.note_field_selection_enabled = True
        self.note_field_chooser.setEnabled(self.note_field_selection_enabled)
        self.form.filter_note_fields_checkbox.setChecked(self.note_field_selection_enabled)

        self.form.filter_note_fields_checkbox.stateChanged.connect(self.toggle_note_field_selection)

        self.update_init_search()

        self.form.filter_note_fields_hbox.addWidget(self.note_field_chooser)

    def update_note_fields(self):
        if hasattr(self, "note_field_chooser"):
            self.note_field_selected_items = self.note_field_chooser.selected_items
            self.update_init_search()

    def toggle_deck_selection(self):
        self.deck_selection_enabled = not self.deck_selection_enabled
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)
        self.update_init_search()

    def toggle_note_field_selection(self):
        self.note_field_selection_enabled = not self.note_field_selection_enabled
        self.note_field_chooser.setEnabled(self.note_field_selection_enabled)
        self.update_init_search()

    def update_init_search(self):
        deck_name = self.deck_selection_enabled and (self.deck_name or self.deck_chooser.deckName())
        note_fields = self.note_field_selection_enabled and self.note_field_selected_items

        self.init_query = ""
        self.init_query += self.search_formatter(True, "deck", deck_name) if deck_name else ""
        if self.note_field_selection_enabled:
            note_type_selected = [mod['name'] for mod in note_fields] if note_fields else ""
            fields_selected = list(
                {fields['name'] for mod in note_fields for fields in mod['fields']} if note_fields else "")
            self.init_query += self.search_multiple_terms_formatter("note", note_type_selected)
            self.init_query += self.search_multiple_fields_formatter(fields_selected, self.REPLACEMENT_STRING)
        else:
            self.init_query += self.REPLACEMENT_STRING

        self.form.query_preview.setText(self.get_final_search("[Word]"))

    def search(self):
        """
        Search through fetched cards here
        Display search results in a new window (note creation and word select)
        """
        self.update_init_search()

        text = self.form.text_area.toPlainText()
        word_model = self.build_word_model(text)

        deck_name = self.deck_selection_enabled and (self.deck_name or self.deck_chooser.deckName())
        note_fields = self.note_field_selection_enabled and self.note_field_selected_items

        if not self.note_creation_window or not self.note_creation_window.isVisible():
            self.reset_note_creation_window()
            self.note_creation_window = note_creation_window = note_creation.NoteCreation(word_model, text, deck_name, note_fields, parent=self)
            note_creation_window.show()
        else:
            self.note_creation_window.word_select.set_word_model(word_model)
            self.note_creation_window.word_select.build()

    def build_word_model(self, text):
        word_model = {}
        tokens = utils.split_words(text)
        for token in tokens:
            if not utils.is_word(token):
                continue
            query = self.get_final_search(token)
            found_note_ids = mw.col.findNotes(query)
            config = mw.addonManager.getConfig(__name__)
            ignored_words = config[ConfigProperties.IGNORED_WORDS.value]
            is_word = utils.is_word(token)
            known = len(found_note_ids) > 0 or token.lower() in [ignored_word.lower() for ignored_word in ignored_words] or not is_word
            word_model[token] = {
                "note_ids": found_note_ids,
                "known": known
            }
        return word_model

    @staticmethod
    def search_formatter(encapsulated, field, term, with_space=True):
        search = ""

        if encapsulated:
            search += "\""

        if field is False:
            search += str(term)
        else:
            search += str(field) + ":" + str(term)

        if encapsulated:
            search += "\""

        if with_space:
            search += " "

        return search

    def search_multiple_terms_formatter(self, field, terms):
        if not terms:
            return ""
        if len(terms) == 1:
            return self.search_formatter(True, field, terms[0])

        search = "("
        search += " or ".join(self.search_formatter(True, field, x, False) for x in terms)
        search += ") "

        return search

    def search_multiple_fields_formatter(self, fields, term):
        if not fields:
            return ""
        if len(fields) == 1:
            return self.search_formatter(True, fields[0], term)

        search = "("
        search += " or ".join(self.search_formatter(True, x, term, False) for x in fields)
        search += ") "

        return search

    def get_final_search(self, word):
        return self.init_query.replace(self.REPLACEMENT_STRING, word)

    def closeEvent(self, event):
        remHook("search_missing_words", self.search)
        event.accept()

    def reset_note_creation_window(self):
        del self.note_creation_window
        self.note_creation_window = None
