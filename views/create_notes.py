from aqt import mw
from aqt.qt import *

from anki.hooks import addHook, remHook, runHook

class CreateNotes(QVBoxLayout):
    def __init__(self):
        super().__init__()

        addHook('newMissingCardsResults', self.update_missing_card_results)

        self.render()

    def cleanup(self):
        remHook('newMissingCardsResults', self.update_missing_card_results)


####### UI


    def render(self):
        self.render_temp_results_view()
        self.render_create_note_button()

    def render_create_note_button(self):
        self.create_note_button = QPushButton("Create Notes")
        self.create_note_button.clicked.connect(self.create_notes)
        self.addWidget(self.create_note_button)

    def render_temp_results_view(self):
        self.search_preview = QTextEdit()
        self.search_preview.setReadOnly(True)
        self.addWidget(self.search_preview)



####### Non-UI



    def create_notes(self):
        print("create notes")
        

    def update_missing_card_results(self, newResults):
        print("Update Results in Create Notes Tab")
        self.results = newResults
        self.search_preview.setText(" ".join(self.results))