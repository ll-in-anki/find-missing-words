"""
Second view of the addon: search results and note creation

Displays the word and buttons to create notes based on presets.
On word select, if notes currently exist for the word, show the basic editor.
If no notes currently exist and a note is created from a preset, show the add notes form/editor.
"""

import re
import functools

from bs4 import BeautifulSoup as Soup
from aqt import mw
import aqt.editor
from aqt.qt import *
from anki.hooks import addHook, remHook, runHook

from ..config.properties import ConfigProperties
from ..forms import note_creation as creation_form
from ..utils.note_field_chooser import NoteFieldChooser
from .. import config, utils
from . import add_note_widget, word_select


class NoteCreation(QWidget):
    def __init__(self, word_model, text, deck_name, note_fields, parent=None):
        super().__init__()
        self.parent = parent
        self.word_model = word_model
        self.text = text
        self.deck_name = deck_name
        self.note_fields = note_fields
        self.note_ids = []
        self.current_word = ""
        self.sentences = None
        self.mw = mw
        self.editor = None
        self.last_list_item = None

        self.form = creation_form.Ui_Form()
        self.form.setupUi(self)
        self.form.note_list_widget.itemClicked.connect(self.display_note_editor)
        self.form.ignore_button.clicked.connect(self.ignore_word)
        self.setup_note_widgets()

        addHook("load_word", self.load_word)
        self.render_word_select()

    def setup_note_widgets(self):
        """
        Don't show list and stacked widgets at first since word may not have any notes to display
        Keep size policy of widgets even if hidden so as to not alter positioning of nearby widgets
        """
        self.form.create_hbox_2.hide()
        self.form.no_word_selected_tip.show()
        self.toggle_note_creation_widgets_visibility(False)
        list_policy = self.form.note_list_widget.sizePolicy()
        list_policy.setRetainSizeWhenHidden(True)
        self.form.note_list_widget.setSizePolicy(list_policy)
        stack_policy = self.form.note_stacked_widget.sizePolicy()
        stack_policy.setRetainSizeWhenHidden(True)
        self.form.note_stacked_widget.setSizePolicy(stack_policy)
        self.form.word_details.hide()

    def toggle_note_creation_widgets_visibility(self, visible):
        self.form.note_list_widget.setVisible(visible)
        self.form.note_stacked_widget.setVisible(visible)
        self.form.notes_created_label.setVisible(visible)
        self.form.note_editor_label.setVisible(visible)

    def render_word_select(self):
        """
        Load the left pane (word select) to display the search text and highlight missing words.
        :return:
        """
        self.word_select = word_select_widget = word_select.WordSelect(self.text, self.word_model, self)
        self.form.word_select_pane_vbox.addWidget(word_select_widget)

    def load_word(self, word, note_ids, known):
        self.reset_list()
        self.display_word(word, known)
        self.populate_notes(note_ids)
        self.render_note_creation_preset_buttons()

    def ignore_word(self):
        config = mw.addonManager.getConfig(__name__)
        ignored_word_set = set(config[ConfigProperties.IGNORED_WORDS.value])
        ignored_word_set.add(self.current_word.lower())
        config[ConfigProperties.IGNORED_WORDS.value] = list(ignored_word_set)
        mw.addonManager.writeConfig(__name__, config)
        self.word_select.ignore_word(self.current_word)
        self.toggle_note_creation_widgets_visibility(False)
        self.form.word_details.hide()
        self.form.create_hbox_2.hide()
        self.form.no_word_selected_tip.show()

    def populate_notes(self, note_ids):
        """
        Display list of notes and their first fields
        :param note_ids: ids found in the original search
        """
        self.form.create_hbox_2.show()
        self.form.no_word_selected_tip.hide()
        if not note_ids:
            self.toggle_note_creation_widgets_visibility(False)
            return
        self.toggle_note_creation_widgets_visibility(True)
        for note_id in note_ids:
            self.note_ids.append(note_id)
            note = self.mw.col.getNote(note_id)
            self.form.note_list_widget.addItem(self.get_note_representation(note))

    def display_word(self, word, known):
        self.form.ignore_button.setEnabled(not known)
        self.form.word_details.show()
        self.current_word = word
        deck_name = self.deck_name or "All"
        if self.note_fields:
            note_fields = NoteFieldChooser.format_btn_text(self.note_fields)
        else:
            note_fields = "All"
        self.form.word_label.setText(word)
        self.form.deck_label.setText("Deck filter: " + deck_name)
        self.form.note_field_label.setText("Model/Field filter: " + note_fields)

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

    def display_note_editor(self, item_clicked, note=False):
        """
        When note clicked in note_list_widget, reveal editor for the note
        """
        if hasattr(self, "editor"):
            if self.last_list_item == item_clicked:
                return
            if isinstance(self.editor, add_note_widget.AddNoteWidget):
                can_close = self.editor.cancel()
                if not can_close:
                    self.form.note_list_widget.setCurrentItem(self.last_list_item)
                    return
            self.clear_note_editors()

        self.last_list_item = item_clicked
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
        utils.clear_stacked_widget(self.form.note_stacked_widget)
        self.delete_editor()

    def render_note_creation_preset_buttons(self):
        """
        If note creation presets were made in the config, show their buttons.
        If no presets exist, show button to create them.
        :return:
        """
        self.remove_note_creation_preset_buttons()
        config = mw.addonManager.getConfig(__name__)
        presets = config[ConfigProperties.NOTE_CREATION_PRESETS.value]
        for preset in presets.values():
            text = preset["preset_name"]
            btn = QPushButton(text)
            self.form.create_btns_hbox.addWidget(btn)
            btn.clicked.connect(functools.partial(self.create_note_from_preset, preset))
        self.prompt_preset_config_dialog()

    def remove_note_creation_preset_buttons(self):
        utils.clear_layout(self.form.create_btns_hbox)

    def prompt_preset_config_dialog(self):
        btn = QPushButton("+")
        btn.setToolTip("Define a new note preset")
        btn.clicked.connect(self.display_note_creation_config)
        self.form.create_btns_hbox.addWidget(btn)

    def display_note_creation_config(self):
        self.mw.find_missing_words_config = config_dialog = config.ConfigDialog(mw)
        config_dialog.form.tab_widget.setCurrentIndex(1)
        config_dialog.finished.connect(self.render_note_creation_preset_buttons)
        config_dialog.open()

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
        """
        Load note creation preset information into an AddNote widget.
        Must update the current deck (if defined in search filter) and model so that the editor will display
        the correct editor fields.
        :param preset: preset passed in from button click
        """
        if hasattr(self, "editor") and isinstance(self.editor, add_note_widget.AddNoteWidget):
            can_close = self.editor.cancel()
            if not can_close:
                return
        else:
            self.clear_note_editors()
        note_type = preset["preset_data"]["note_type"]
        word_dest_field = preset["preset_data"]["word_destination"]
        sentences_allowed = preset["preset_data"].get("sentences_allowed", False)
        model = self.mw.col.models.byName(note_type)
        if self.deck_name:
            self.update_deck()
        self.update_model(model)
        note = self.mw.col.newNote()
        note[word_dest_field] = self.current_word
        if sentences_allowed and "sentence_destination" in preset["preset_data"]:
            sentence_dest_field = preset["preset_data"]["sentence_destination"]
            note[sentence_dest_field] = self.find_sentences(self.current_word)
        self.create_list_item_for_preset(preset["preset_name"], note)
        self.editor = add_note_widget.AddNoteWidget(mw, note, self.on_note_add, self.on_note_cancel)
        self.form.note_stacked_widget.addWidget(self.editor)

    def on_note_add(self, note):
        """
        Note created in AddNote widget
        Overwrite temp list item with new saved note; refresh word select pane.
        :param note: new note saved into Anki
        """
        self.clear_note_editors()
        self.form.note_list_widget.takeItem(self.form.note_list_widget.count() - 1)
        self.note_ids.pop()
        self.note_ids.append(note.id)
        self.form.note_list_widget.addItem(self.get_note_representation(note))
        row_to_select = self.form.note_list_widget.count() - 1
        self.form.note_list_widget.setCurrentRow(row_to_select)
        self.last_list_item = self.form.note_list_widget.currentItem()
        runHook("search_missing_words")

    def on_note_cancel(self):
        self.clear_note_editors()
        self.form.note_list_widget.takeItem(self.form.note_list_widget.count() - 1)
        self.note_ids.pop()
        self.last_list_item = None
        if not self.note_ids:
            self.toggle_note_creation_widgets_visibility(False)

    def create_list_item_for_preset(self, preset_name, note):
        """
        Create temporory list item for the temporary note. Will be overridden later on note add.
        :param note: temporary note
        """
        if not self.note_ids:
            self.toggle_note_creation_widgets_visibility(True)
        self.note_ids.append(note.id)
        self.form.note_list_widget.addItem(f"New \"{preset_name}\"")
        row_to_select = self.form.note_list_widget.count() - 1
        self.form.note_list_widget.setCurrentRow(row_to_select)
        self.last_list_item = self.form.note_list_widget.currentItem()

    def delete_editor(self):
        """
        Delete singleton editor object for memory management.
        """
        if hasattr(self, "editor") and self.editor is not None:
            self.editor.cleanup()
            del self.editor

    def closeEvent(self, event):
        remHook("load_word", self.load_word)
        self.delete_editor()
        event.accept()
