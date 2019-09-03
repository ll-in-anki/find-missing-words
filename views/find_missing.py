from functools import partial

from aqt import mw
from aqt.qt import *
import aqt.deckchooser
import aqt.modelchooser

from . import field_chooser, multi_chooser


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.deck_selection_enabled = True
        self.model_selection_enabled = False
        self.field_selection_enabled = False
        self.model_field_items = []
        self.selected_decks = []
        self.render()

    def render(self):
        # self.deck_chooser = self.render_filter("Filter deck?", self.deck_selection_enabled, self.toggle_deck_selection, aqt.deckchooser.DeckChooser)
        # self.model_chooser = self.render_filter("Filter model/note type?", self.model_selection_enabled, self.toggle_model_selection, aqt.modelchooser.ModelChooser)
        # self.field_chooser = self.render_filter("Filter field?", self.field_selection_enabled, self.toggle_field_selection, field_chooser.FieldChooser)
        # current_model = mw.col.models.current()
        # self.render_deck_chooser()
        self.render_model_field_tree()
        self.render_text_area()
        self.render_search_button()

    def render_deck_chooser(self):
        open_chooser_btn = QPushButton("Deck")
        open_chooser_btn.clicked.connect(self.open_deck_chooser)
        self.addWidget(open_chooser_btn)

    def open_deck_chooser(self):
        decks = mw.col.decks.all()
        deck_chooser_data = [[deck["name"]] for deck in decks]
        deck_chooser_widget = multi_chooser.ModelFieldTree(mw, deck_chooser_data, ["Deck"], "Decks")
        # from aqt.qt import debug; debug()
        if deck_chooser_widget.selected_items:
            self.selected_decks = deck_chooser_widget.selected_items
            print([deck.data(1,0) for deck in self.selected_decks])

    def render_model_chooser(self):
        open_chooser_btn = QPushButton("Model")
        open_chooser_btn.clicked.connect(self.open_model_chooser)
        self.addWidget(open_chooser_btn)

    def open_model_chooser(self):
        models = mw.col.models.all()
        model_chooser_data = [[model["name"]] for model in models]
        model_chooser_widget = multi_chooser.ModelFieldTree(mw, model_chooser_data, "Note Types")
        if model_chooser_widget.selected_items:
            self.selected_models = [model.data(1,0) for model in model_chooser_widget.selected_items]
            print(self.selected_models)

    def render_field_chooser(self):
        open_chooser_btn = QPushButton("Field")
        open_chooser_btn.clicked.connect(self.open_field_chooser)
        self.addWidget(open_chooser_btn)

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

    def render_model_field_tree(self):
        if not self.model_field_items:
            self.generate_model_field_data()

        field_chooser_widget = multi_chooser.ModelFieldTree(mw, self.model_field_items, "Models/Fields")

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

    def toggle_model_selection(self, parent_widget):
        self.model_selection_enabled = not self.model_selection_enabled
        parent_widget.setEnabled(self.model_selection_enabled)

    def toggle_field_selection(self, parent_widget):
        self.field_selection_enabled = not self.field_selection_enabled
        parent_widget.setEnabled(self.field_selection_enabled)

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

    def search(self):
        # Search through fetched cards here
        deck_id = self.deck_selection_enabled and self.deck_chooser.selectedId()
        deck_name = self.deck_selection_enabled and self.deck_chooser.deckName()
        model_name = self.model_selection_enabled and mw.col.models.current()['name']
        field_name = self.field_selection_enabled and self.field_chooser.current_field_name

