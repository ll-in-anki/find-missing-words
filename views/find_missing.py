from functools import partial

from aqt import mw
from aqt.qt import *
import aqt.deckchooser
import aqt.modelchooser
# import os
from anki.hooks import addHook, remHook

from . import field_chooser


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.deck_selection_enabled = True
        self.model_selection_enabled = False
        self.field_selection_enabled = False

        addHook('currentModelChanged', self.update_init_search)

        self.render()
        self.update_init_search()

    def cleanup(self):
        remHook('currentModelChanged', self.update_init_search)

####### UI


    def render(self):
        print("Render")
        self.deck_chooser = self.render_filter("Filter deck?", self.deck_selection_enabled, self.toggle_deck_selection, aqt.deckchooser.DeckChooser)
        self.model_chooser = self.render_filter("Filter model/note type?", self.model_selection_enabled, self.toggle_model_selection, aqt.modelchooser.ModelChooser)
        self.field_chooser = self.render_filter("Filter field?", self.field_selection_enabled, self.toggle_field_selection, field_chooser.FieldChooser)
        
        self.render_search_preview()
        self.render_text_area()
        self.render_search_button()
        self.render_results_area()
        

    def render_filter(self, checkbox_label, state, on_state_change, chooser_class):
        checkbox = QCheckBox(checkbox_label)
        checkbox.setChecked(state)

        chooser_widget = QWidget()
        chooser = chooser_class(mw, chooser_widget)
        chooser_widget.setEnabled(state)
        checkbox.stateChanged.connect(partial(on_state_change, chooser_widget))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(checkbox)
        btn_layout.addStretch(1)
        btn_layout.addWidget(chooser_widget)
        self.addLayout(btn_layout)
        return chooser

    def toggle_deck_selection(self, parent_widget):
        self.deck_selection_enabled = not self.deck_selection_enabled
        parent_widget.setEnabled(self.deck_selection_enabled)
        self.update_init_search()

    def toggle_model_selection(self, parent_widget):
        self.model_selection_enabled = not self.model_selection_enabled
        parent_widget.setEnabled(self.model_selection_enabled)
        self.update_init_search()

    def toggle_field_selection(self, parent_widget):
        self.field_selection_enabled = not self.field_selection_enabled
        parent_widget.setEnabled(self.field_selection_enabled)
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



####### Non-UI



    # def copy_preview(self):
    #     data = self.get_final_search("[Word]")
    #     command = 'echo ' + data.strip() + '| clip'
    #     os.system(command)
    
    def update_init_search(self):
        # print("Update Init Search")
        # deck_id = self.deck_selection_enabled and self.deck_chooser.selectedId()
        deck_name = self.deck_selection_enabled and self.deck_chooser.deckName()
        model_name = self.model_selection_enabled and mw.col.models.current()['name']
        self.field_name = self.field_selection_enabled and self.field_chooser.current_field_name

        self.initQuery = ""
        self.initQuery += self.search_formatter(True, "deck", deck_name) if deck_name else ""
        self.initQuery += self.search_formatter(True, "note", model_name) if model_name else ""

        self.search_preview.setText(self.get_final_search("[Word]"))



    def search(self):
        # Search through fetched cards here
        
        self.results_area.clear()
        
        self.update_init_search()

        # Convert to set to get unique entries, after splitting text box by white space
        words = set(self.text_area_text.toPlainText().split())

        for word in words:
            query = self.get_final_search(word)
        
            results = mw.col.findCards(query)
            hasResults = len(results) > 0
            print(query + ": " + str(hasResults))

            if not hasResults:
                self.results_area.addItem(self.create_result_item(word))
                



    def search_formatter(self, encapsulated, field, term):
        search = ""

        if encapsulated:
            search += "\""        

        if field is False:
            search += str(term)
        else:
            search += str(field) + ":" + str(term)

        if encapsulated:
            search += "\" "
        else:
            search += " "
        
        return search


    def get_final_search(self, word):
        return self.initQuery + self.search_formatter(True, self.field_name if self.field_name else False, word)


    def create_result_item(self, word):
        # print("Create Result Item: " + str(word))
        item = QListWidgetItem()

        item.setText(str(word))
        

        return item