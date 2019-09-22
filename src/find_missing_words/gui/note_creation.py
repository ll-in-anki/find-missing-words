from aqt import mw
import aqt.editor
from aqt.qt import *
from anki.hooks import addHook, remHook

from .forms import note_creation as creation_form
from . import word_select


class NoteCreation(QWidget):
    def __init__(self, word_model, parent=None):
        super().__init__()
        self.mw = mw
        self.parent = parent
        self.word_model = word_model
        self.form = creation_form.Ui_Form()
        self.form.setupUi(self)
        self.form.notes_scroll_area.setWidgetResizable(True)

        addHook("clear_notes", self.clear_note_editors)
        addHook("show_note", self.render_note_editor)

        self.render_word_select()

    def render_word_select(self):
        self.word_select = word_select_widget = word_select.WordSelect(self.word_model, self)
        self.form.word_select_pane_vbox.addWidget(word_select_widget)

    def render_note_editor(self, note_id):
        widget = QWidget()
        editor = aqt.editor.Editor(self.mw, widget, self)
        note = self.mw.col.getNote(note_id)
        editor.setNote(note, focusTo=0)
        self.form.notes_scroll_area_widget.layout().addWidget(widget)

    def clear_note_editors(self):
        layout = self.form.notes_scroll_area_widget.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def close(self):
        remHook("clear_cards", self.render_note_editor)
        remHook("show_card", self.clear_note_editors)
