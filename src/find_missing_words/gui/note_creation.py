from bs4 import BeautifulSoup as Soup
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
        self.note_ids = []
        self.form = creation_form.Ui_Form()
        self.form.setupUi(self)
        self.form.note_list_widget.itemClicked.connect(self.display_note_editor)
        self.reset_hooks()
        self.render_word_select()

    def reset_hooks(self):
        remHook("clear_notes", self.reset_list)
        remHook("populate_note", self.populate_note)
        addHook("clear_notes", self.reset_list)
        addHook("populate_note", self.populate_note)

    def render_word_select(self):
        self.word_select = word_select_widget = word_select.WordSelect(self.word_model, self)
        self.form.word_select_pane_vbox.addWidget(word_select_widget)

    def populate_note(self, note_id):
        self.note_ids.append(note_id)
        note = self.mw.col.getNote(note_id)
        sort_field = self.reformat_sort_field(note.fields[0])
        self.form.note_list_widget.addItem(sort_field)

    @staticmethod
    def reformat_sort_field(text):
        text_with_spaced_divs = text.replace("<div>", " <div>")
        return Soup(text_with_spaced_divs, features="lxml").text

    def display_note_editor(self):
        self.clear_note_editors()

        index = self.form.note_list_widget.currentRow()
        note_id = self.note_ids[index]
        note = self.mw.col.getNote(note_id)

        widget = QWidget()
        editor = aqt.editor.Editor(self.mw, widget, self)
        editor.setNote(note, focusTo=0)

        self.form.note_stacked_widget.addWidget(widget)
        self.form.note_stacked_widget.setCurrentIndex(index)

    def reset_list(self):
        self.note_ids = []
        self.form.note_list_widget.clear()
        self.clear_note_editors()

    def clear_note_editors(self):
        for i in range(self.form.note_stacked_widget.count()):
            widget = self.form.note_stacked_widget.widget(i)
            self.form.note_stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def close(self):
        remHook("clear_notes", self.reset_list)
        remHook("populate_note", self.populate_note)
