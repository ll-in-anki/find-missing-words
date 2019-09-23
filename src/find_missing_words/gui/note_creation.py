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
        self.parent = parent
        self.word_model = word_model
        self.note_ids = []
        self.word_label = None
        self.mw = mw

        self.form = creation_form.Ui_Form()
        self.form.setupUi(self)
        self.form.note_list_widget.itemClicked.connect(self.display_note_editor)
        self.setup_note_widgets()

        self.reset_hooks()
        self.render_word_select()

    def setup_note_widgets(self):
        """
        Don't show list and stacked widgets at first since word may not have any notes to display
        Keep size policy of widgets even if hidden so as to not alter positioning of nearby widgets
        """
        self.form.note_list_widget.hide()
        self.form.note_stacked_widget.hide()
        list_policy = self.form.note_list_widget.sizePolicy()
        list_policy.setRetainSizeWhenHidden(True)
        self.form.note_list_widget.setSizePolicy(list_policy)
        stack_policy = self.form.note_stacked_widget.sizePolicy()
        stack_policy.setRetainSizeWhenHidden(True)
        self.form.note_stacked_widget.setSizePolicy(stack_policy)

    def reset_hooks(self):
        remHook("clear_notes", self.reset_list)
        remHook("populate_notes", self.populate_notes)
        remHook("display_word", self.display_word)
        addHook("clear_notes", self.reset_list)
        addHook("populate_notes", self.populate_notes)
        addHook("display_word", self.display_word)

    def render_word_select(self):
        self.word_select = word_select_widget = word_select.WordSelect(self.word_model, self)
        self.form.word_select_pane_vbox.addWidget(word_select_widget)

    def populate_notes(self, note_ids):
        """
        Display list of notes and their first fields
        :param note_ids: ids found in the original search
        """
        if not note_ids:
            self.form.note_list_widget.hide()
            self.form.note_stacked_widget.hide()
            return
        self.form.note_list_widget.show()
        self.form.note_stacked_widget.show()
        for note_id in note_ids:
            self.note_ids.append(note_id)
            note = self.mw.col.getNote(note_id)
            sort_field = self.reformat_sort_field(note.fields[0])
            self.form.note_list_widget.addItem(sort_field)

    def display_word(self, word):
        if not self.word_label:
            self.word_label = QLabel()
            self.word_label.setStyleSheet("font-size: 32px; font-weight: bold")
            self.form.note_pane_vbox.insertWidget(0, self.word_label)
        self.word_label.setText(word)

    @staticmethod
    def reformat_sort_field(text):
        """
        Convert literal HTML markup to plaintext with proper spacing
        :param text: HTML string
        :return: text with no HTML
        """
        text_with_spaced_divs = text.replace("<div>", " <div>")
        return Soup(text_with_spaced_divs, features="lxml").text

    def display_note_editor(self):
        """
        When note clicked in note_list_widget, reveal editor for the note
        """
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
        """
        Reset list widget (and close editor) on new word select
        """
        self.note_ids = []
        self.form.note_list_widget.clear()
        self.clear_note_editors()

    def clear_note_editors(self):
        """
        Close any aqt.Editor instances (usually just one)
        :return:
        """
        for i in range(self.form.note_stacked_widget.count()):
            widget = self.form.note_stacked_widget.widget(i)
            self.form.note_stacked_widget.removeWidget(widget)
            widget.deleteLater()

    def close(self):
        remHook("clear_notes", self.reset_list)
        remHook("populate_notes", self.populate_notes)
