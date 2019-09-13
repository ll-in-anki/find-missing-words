from aqt import mw, deckchooser
from aqt.qt import *
from anki.hooks import runHook

from .forms import search as search_form
from . import note_field_tree


class Search(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent or mw
        # Set up UI from pre-generated UI form:
        self.form = search_form.Ui_Form()
        self.form.setupUi(self)

        self.REPLACEMENT_STRING = "[[[WORD]]]"

        self.results = []
        self.deck_selection_enabled = True
        self.note_field_selection_enabled = False
        self.note_field_items = self.note_field_selected_items = []
        self.selected_decks = []

        self.render_deck_chooser()
        self.render_note_field_chooser()
        self.form.search_button.clicked.connect(self.search)

    def render_deck_chooser(self):
        self.form.filter_decks_checkbox.setChecked(self.deck_selection_enabled)
        self.form.filter_decks_checkbox.stateChanged.connect(self.toggle_deck_selection)

        self.deck_chooser_parent_widget = QWidget()
        self.deck_chooser = deckchooser.DeckChooser(mw, self.deck_chooser_parent_widget)
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)

        self.form.filter_decks_hbox.addWidget(self.deck_chooser_parent_widget)

    def render_note_field_chooser(self):
        self.form.filter_note_fields_checkbox.setChecked(self.note_field_selection_enabled)
        self.form.filter_note_fields_checkbox.stateChanged.connect(self.toggle_note_field_selection)

        self.note_field_chooser_btn = QPushButton("Notes and Fields")
        self.note_field_chooser_btn.clicked.connect(self.render_note_field_tree)
        self.note_field_chooser_btn.setEnabled(self.note_field_selection_enabled)

        self.form.filter_note_fields_hbox.addWidget(self.note_field_chooser_btn)

    def toggle_deck_selection(self):
        self.deck_selection_enabled = not self.deck_selection_enabled
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)
        self.update_init_search()

    def toggle_note_field_selection(self):
        self.note_field_selection_enabled = not self.note_field_selection_enabled
        self.note_field_chooser_btn.setEnabled(self.note_field_selection_enabled)
        self.update_init_search()

    def render_note_field_tree(self):
        if not self.note_field_items:
            self.generate_note_field_data()

        self.note_field_chooser = note_field_tree.NoteFieldTree(self.note_field_items, parent=self)
        self.note_field_items = self.note_field_chooser.all_items
        self.note_field_selected_items = self.note_field_chooser.get_all_items(True)
        self.update_init_search()

    def generate_note_field_data(self):
        all_models = mw.col.models.all()
        self.note_field_items = []
        for model in all_models:
            model_dict = {"name": model["name"], "state": 2}
            note_fields = []
            for field in model["flds"]:
                field_dict = {"name": field["name"], "state": 2}
                note_fields.append(field_dict)
            model_dict["fields"] = note_fields
            self.note_field_items.append(model_dict)

    ########################
    #######  Non-UI  #######
    ########################

    # def copy_preview(self):
    #     data = self.get_final_search("[Word]")
    #     command = 'echo ' + data.strip() + '| clip'
    #     os.system(command)

    def update_init_search(self):
        # print("Update Init Search")
        deck_name = self.deck_selection_enabled and self.deck_chooser.deckName()
        note_fields = self.note_field_selection_enabled and self.note_field_selected_items

        if self.note_field_selection_enabled:
            noteTypesSelected = [mod['name'] for mod in note_fields] if note_fields else ""
            fieldsSelected = list(
                {fields['name'] for mod in note_fields for fields in mod['fields']} if note_fields else "")

            print(noteTypesSelected, fieldsSelected)

        self.initQuery = ""
        self.initQuery += self.search_formatter(True, "deck", deck_name) if deck_name else ""
        if self.note_field_selection_enabled:
            self.initQuery += self.search_multiple_terms_formatter("note", noteTypesSelected)
            self.initQuery += self.search_multiple_fields_formatter(fieldsSelected, self.REPLACEMENT_STRING)
        else:
            self.initQuery += self.REPLACEMENT_STRING

        self.form.query_preview.setText(self.get_final_search("[Word]"))

    def search(self):
        # Search through fetched cards here

        # self.results_area.clear()
        self.results.clear()

        self.update_init_search()

        words = set(self.form.text_area.toPlainText().split())

        for word in words:
            query = self.get_final_search(word)

            results = mw.col.findCards(query)
            hasResults = len(results) > 0
            print(query + ": " + str(hasResults))

            # if not hasResults:
            #     self.results.append(word)
            #     self.results_area.addItem(self.create_result_item(word))

        print(self.results)
        runHook('newMissingCardsResults', self.results)

    def search_formatter(self, encapsulated, field, term, withSpace=True):
        search = ""

        if encapsulated:
            search += "\""

        if field is False:
            search += str(term)
        else:
            search += str(field) + ":" + str(term)

        if encapsulated:
            search += "\""

        if withSpace:
            search += " "

        return search

    def search_multiple_terms_formatter(self, field, terms):
        if not terms:
            return ""
        elif len(terms) == 1:
            return self.search_formatter(True, field, terms[0])

        search = "("
        search += " or ".join(self.search_formatter(True, field, x, False) for x in terms)
        search += ") "

        return search

    def search_multiple_fields_formatter(self, fields, term):
        if not fields:
            return ""
        elif len(fields) == 1:
            return self.search_formatter(True, fields[0], term)

        search = "("
        search += " or ".join(self.search_formatter(True, x, term, False) for x in fields)
        search += ") "

        return search

    def get_final_search(self, word):
        return self.initQuery.replace(self.REPLACEMENT_STRING, word)
