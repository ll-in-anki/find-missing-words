from functools import partial

from aqt import mw
from aqt.qt import *
import aqt.deckchooser

from . import model_field_tree


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.deck_selection_enabled = True
        self.model_field_selection_enabled = True
        self.model_field_items = []
        self.selected_decks = []
        self.render()

    def render(self):
        self.render_deck_chooser()
        self.render_model_field_chooser()
        self.render_text_area()
        self.render_search_button()

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
        checkbox = QCheckBox("Filter Note Type & Field?")
        checkbox.setChecked(self.model_field_selection_enabled)
        checkbox.stateChanged.connect(self.toggle_model_field_selection)
        self.model_field_chooser_btn = QPushButton("Note Type & Field")
        self.model_field_chooser_btn.clicked.connect(self.render_model_field_tree)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(checkbox)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.model_field_chooser_btn)
        self.addLayout(btn_layout)

    def render_model_field_tree(self):
        if not self.model_field_items:
            self.generate_model_field_data()

        model_field_chooser_widget = model_field_tree.ModelFieldTree(mw, self.model_field_items, "Models/Fields")
        if model_field_chooser_widget.selected_items:
            print(model_field_chooser_widget.selected_items)

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

    def toggle_deck_selection(self):
        self.deck_selection_enabled = not self.deck_selection_enabled
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)

    def toggle_model_field_selection(self):
        self.model_field_selection_enabled = not self.model_field_selection_enabled
        self.model_field_chooser_btn.setEnabled(self.model_field_selection_enabled)

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

