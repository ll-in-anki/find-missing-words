from functools import partial

from aqt import mw
from aqt.qt import *
import aqt.deckchooser
# import os
from anki.hooks import addHook, remHook, runHook

from . import model_field_tree


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.REPLACEMENT_STRING = "[[[WORD]]]"

        self.results = []
        self.deck_selection_enabled = True
        self.model_field_selection_enabled = False
        self.model_field_items = self.model_field_selected_items = []
        self.selected_decks = []
        
        addHook('currentModelChanged', self.update_init_search)
        self.render()
        self.update_init_search()

    def cleanup(self):
        remHook('currentModelChanged', self.update_init_search)

########################
#######    UI    #######
########################

    def render(self):
        self.render_deck_chooser()
        self.render_model_field_chooser()
        self.render_search_preview()
        self.render_text_area()
        self.render_search_button()
        self.render_results_area()
        

    def render_deck_chooser(self):
        self.deck_selection_checkbox = QCheckBox("Filter Decks?")
        self.deck_selection_checkbox.setChecked(self.deck_selection_enabled)
        self.deck_selection_checkbox.stateChanged.connect(self.toggle_deck_selection)

        self.deck_chooser_parent_widget = QWidget()
        self.deck_chooser = aqt.deckchooser.DeckChooser(mw, self.deck_chooser_parent_widget)
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.deck_selection_checkbox)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.deck_chooser_parent_widget)
        self.addLayout(btn_layout)

    def render_model_field_chooser(self):
        checkbox = QCheckBox("Filter Notes and Fields?")
        checkbox.setChecked(self.model_field_selection_enabled)
        checkbox.stateChanged.connect(self.toggle_model_field_selection)
        self.model_field_chooser_btn = QPushButton("Notes and Fields")
        self.model_field_chooser_btn.clicked.connect(self.render_model_field_tree)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(checkbox)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.model_field_chooser_btn)
        self.addLayout(btn_layout)

    def render_model_field_tree(self):
        if not self.model_field_items:
            self.generate_model_field_data()

        self.model_field_chooser = model_field_tree.ModelFieldTree(mw, self.model_field_items)
        self.model_field_items = self.model_field_chooser.all_items
        self.model_field_selected_items = self.model_field_chooser.get_all_items(True)
        self.update_init_search()

    def generate_model_field_data(self):
        all_models = mw.col.models.all()
        self.model_field_items = []
        for model in all_models:
            model_dict = {"name": model["name"], "state": 2}
            model_fields = []
            for field in model["flds"]:
                field_dict = {"name": field["name"], "state": 2}
                model_fields.append(field_dict)
            model_dict["fields"] = model_fields
            self.model_field_items.append(model_dict)

    def toggle_deck_selection(self):
        self.deck_selection_enabled = not self.deck_selection_enabled
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)
        self.update_init_search()

    def toggle_model_field_selection(self):
        self.model_field_selection_enabled = not self.model_field_selection_enabled
        self.model_field_chooser_btn.setEnabled(self.model_field_selection_enabled)
        self.update_init_search()

    def render_text_area(self):
        self.text_area_label = QLabel()
        self.text_area_label.setText("Text:")
        self.addWidget(self.text_area_label)
        self.text_area_text = QTextEdit()
        self.addWidget(self.text_area_text)

    def render_search_button(self):
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.search_button)
        self.addLayout(btn_layout)

    def render_search_preview(self):
        search_preview_layout = QHBoxLayout()
        search_text = QLabel()
        search_text.setText("Search:")
        search_preview_layout.addWidget(search_text)
        
        self.search_preview = QTextEdit()
        self.search_preview.setReadOnly(True)
        self.search_preview.setFixedHeight(40)
        search_preview_layout.addWidget(self.search_preview)

        # self.copy_preview_button = QPushButton("Copy")
        # self.copy_preview_button.clicked.connect(self.copy_preview)
        # search_preview_layout.addWidget(self.copy_preview_button)

        self.addLayout(search_preview_layout)

    def render_results_area(self):
        self.results_area = QListWidget()
        self.addWidget(self.results_area)



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
        model_fields = self.model_field_selection_enabled and self.model_field_selected_items

        if self.model_field_selection_enabled:
            noteTypesSelected = [mod['name'] for mod in model_fields] if model_fields else ""
            fieldsSelected = list({fields['name'] for mod in model_fields for fields in mod['fields']} if model_fields else "")
            
            print(noteTypesSelected, fieldsSelected)

        self.initQuery = ""
        
        self.initQuery += self.search_formatter(True, "deck", deck_name) if deck_name else ""

        self.initQuery += self.search_multiple_terms_formatter("note", noteTypesSelected) if self.model_field_selection_enabled else ""
        
        if self.model_field_selection_enabled:
            self.initQuery += self.search_multiple_fields_formatter(fieldsSelected, self.REPLACEMENT_STRING) 
        else:
            self.initQuery += self.REPLACEMENT_STRING
        
        self.search_preview.setText(self.get_final_search("[Word]"))



    def search(self):
        # Search through fetched cards here
        
        self.results_area.clear()
        self.results.clear()
        
        self.update_init_search()

        words = set(self.text_area_text.toPlainText().split())

        for word in words:
            query = self.get_final_search(word)
        
            results = mw.col.findCards(query)
            hasResults = len(results) > 0
            print(query + ": " + str(hasResults))

            if not hasResults:
                self.results.append(word)
                self.results_area.addItem(self.create_result_item(word))
                
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


    def create_result_item(self, word):
        # print("Create Result Item: " + str(word))
        item = QListWidgetItem()

        item.setText(str(word))
        
        return item