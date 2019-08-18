from aqt import mw
from aqt.qt import *
import aqt.deckchooser
import aqt.modelchooser


class FindMissingWords(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.deck_selection_enabled = True
        self.model_selection_enabled = False
        self.render()

    def render(self):
        self.render_deck_chooser()
        self.render_model_chooser()
        self.render_text_area()
        self.render_search_button()

    def render_text_area(self):
        self.text_area_label = QLabel()
        self.text_area_label.setText("Text:")
        self.addWidget(self.text_area_label)
        self.text = QTextEdit()
        self.addWidget(self.text)

    def render_deck_chooser(self):
        self.deck_selection_checkbox = QCheckBox("Filter Deck?")
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

    def render_model_chooser(self):
        self.model_selection_checkbox = QCheckBox("Filter Model/Note Type?")
        self.model_selection_checkbox.setChecked(self.model_selection_enabled)
        self.model_selection_checkbox.stateChanged.connect(self.toggle_model_selection)

        self.model_chooser_parent_widget = QWidget()
        self.model_chooser = aqt.modelchooser.ModelChooser(mw, self.model_chooser_parent_widget)
        self.model_chooser_parent_widget.setEnabled(self.model_selection_enabled)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.model_selection_checkbox)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.model_chooser_parent_widget)
        self.addLayout(btn_layout)

    def toggle_deck_selection(self):
        self.deck_selection_enabled = not self.deck_selection_enabled
        self.deck_chooser_parent_widget.setEnabled(self.deck_selection_enabled)

    def toggle_model_selection(self):
        self.model_selection_enabled = not self.model_selection_enabled
        self.model_chooser_parent_widget.setEnabled(self.model_selection_enabled)

    def render_search_button(self):
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.search_button)
        self.addLayout(btn_layout)

    def search(self):
        # Search through fetched cards here
        deck_id = self.deck_chooser.selectedId()
        self.deck_label = QLabel()
        self.deck_label.setText(str(deck_id))
        self.addWidget(self.deck_label)

        # model_id = self.model_chooser.selectedId()
        # self.model_label = QLabel()
        # self.model_label.setText(str(model_id))
        # self.addWidget(self.model_label)
