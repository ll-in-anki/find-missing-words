import re
import functools

from bs4 import BeautifulSoup as Soup
from aqt import mw
import aqt.editor
from aqt.qt import *
from anki.hooks import addHook, remHook

from .forms import note_creation as creation_form
from . import word_select, add_note_widget
from .config.properties import ConfigProperties


class NoteCreation(QWidget):
    def __init__(self, word_model, text, deck_name, parent=None):
        super().__init__()
        self.parent = parent
        self.word_model = word_model
        self.text = text
        self.deck_name = deck_name
        self.note_ids = []
        self.word_label = None
        self.current_word = ""
        self.sentences = None
        self.mw = mw
        self.editor = None

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
        remHook("load_word", self.load_word)
        addHook("load_word", self.load_word)

    def render_word_select(self):
        self.word_select = word_select_widget = word_select.WordSelect(self.text, self.word_model, self)
        self.form.word_select_pane_vbox.addWidget(word_select_widget)

    def load_word(self, word, note_ids):
        self.reset_list()
        self.display_word(word)
        self.populate_notes(note_ids)
        self.render_note_creation_preset_buttons()

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
            self.form.note_list_widget.addItem(self.get_note_representation(note))

    def display_word(self, word):
        self.current_word = word
        if not self.word_label:
            self.word_label = QLabel()
            self.word_label.setStyleSheet("font-size: 32px; font-weight: bold")
            self.form.note_pane_vbox.insertWidget(0, self.word_label)
        self.word_label.setText(word)

    def find_sentences(self, word):
        """
        Find sentences surrounding a word in the original text
        :param word: word in the text
        :return: list of sentences including the word
        """
        pattern = rf"[^.]*\s?{word}\s?[^.]*\."
        return "\n".join([match.strip() for match in re.findall(pattern, self.text, re.IGNORECASE | re.MULTILINE)])

    @staticmethod
    def get_note_representation(note):
        """
        Convert literal HTML markup to plaintext with proper spacing
        :param note: note which holds field values
        :return: text with no HTML
        """
        sort_field = note.fields[0]
        text_with_spaced_divs = sort_field.replace("<div>", " <div>")
        return Soup(text_with_spaced_divs, features="lxml").text

    def display_note_editor(self, _, note=False):
        """
        When note clicked in note_list_widget, reveal editor for the note
        """
        self.clear_note_editors()

        index = self.form.note_list_widget.currentRow()
        if not note:
            note_id = self.note_ids[index]
            note = self.mw.col.getNote(note_id)

        widget = QWidget()
        self.editor = aqt.editor.Editor(self.mw, widget, self)
        self.editor.setNote(note, focusTo=0)

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
        """
        for i in range(self.form.note_stacked_widget.count()):
            widget = self.form.note_stacked_widget.widget(i)
            self.form.note_stacked_widget.removeWidget(widget)
            widget.deleteLater()
        self.delete_editor()

    def render_note_creation_preset_buttons(self):
        self.remove_note_creation_preset_buttons()
        config = mw.addonManager.getConfig(__name__)
        presets = config[ConfigProperties.NOTE_CREATION_PRESETS.value]
        for preset in presets.values():
            text = preset["preset_name"]
            btn = QPushButton(text)
            self.form.create_btns_hbox.addWidget(btn)
            btn.clicked.connect(functools.partial(self.create_note_from_preset, preset))

    def remove_note_creation_preset_buttons(self):
        for i in range(self.form.create_btns_hbox.count()):
            btn = self.form.create_btns_hbox.takeAt(i)
            if btn.widget():
                btn.widget().deleteLater()

    def update_deck(self):
        deck = mw.col.decks.byName(self.deck_name)
        self.mw.col.conf["curDeck"] = deck["id"]
        self.mw.col.decks.save(deck)

    def update_model(self, model):
        self.mw.col.conf['curModel'] = model['id']
        current_deck = self.mw.col.decks.current()
        current_deck['mid'] = model['id']
        self.mw.col.decks.save(current_deck)

    def create_note_from_preset(self, preset):
        self.clear_note_editors()
        word_dest = preset["preset_data"]["word_destination"]
        sentences_allowed = False
        if "sentences_allowed" in preset["preset_data"]:
            sentences_allowed = preset["preset_data"]["sentences_allowed"]
        model_name = word_dest["name"]
        model = self.mw.col.models.byName(model_name)
        if self.deck_name:
            self.update_deck()
        self.update_model(model)
        note = self.mw.col.newNote()
        word_dest_field_name = word_dest["fields"][0]["name"]
        note[word_dest_field_name] = self.current_word
        if sentences_allowed and "sentence_destination" in preset["preset_data"]:
            sentence_dest = preset["preset_data"]["sentence_destination"]
            if word_dest["name"] == sentence_dest["name"]:
                sentence_dest_field_name = sentence_dest["fields"][0]["name"]
                note[sentence_dest_field_name] = self.find_sentences(self.current_word)
        self.create_list_item_for_preset(preset["preset_name"], note)
        self.editor = add_note_widget.AddNoteWidget(mw, note, self.on_note_add, self.on_note_cancel)
        self.form.note_stacked_widget.addWidget(self.editor)

    def on_note_add(self, note):
        self.clear_note_editors()
        self.form.note_list_widget.takeItem(self.form.note_list_widget.currentRow())
        self.note_ids.pop()
        self.note_ids.append(note.id)
        self.form.note_list_widget.addItem(self.get_note_representation(note))
        row_to_select = self.form.note_list_widget.count() - 1
        self.form.note_list_widget.setCurrentRow(row_to_select)

    def on_note_cancel(self):
        self.clear_note_editors()
        self.form.note_list_widget.takeItem(self.form.note_list_widget.currentRow())
        self.note_ids.pop()

    def create_list_item_for_preset(self, preset_name, note):
        if not self.note_ids:
            self.form.note_list_widget.show()
            self.form.note_stacked_widget.show()
        self.note_ids.append(note.id)
        self.form.note_list_widget.addItem(f"New \"{preset_name}\"")
        row_to_select = self.form.note_list_widget.count() - 1
        self.form.note_list_widget.setCurrentRow(row_to_select)

    def delete_editor(self):
        if hasattr(self, "editor"):
            del self.editor

    def close(self):
        remHook("load_word", self.load_word)
        self.delete_editor()
        super().close()
