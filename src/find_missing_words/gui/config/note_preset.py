from aqt import mw
from aqt.qt import *

from ..utils import list_chooser
from ..forms import config_note_preset as preset_form


class NotePreset(QWidget):
    def __init__(self, config, preset, on_update_callback=None, parent=None):
        super().__init__()
        self.config = config
        self.preset = preset
        self.data = preset["preset_data"]
        self.on_update_callback = on_update_callback
        self.parent = parent
        self.mw = mw
        self.note_type = self.data.get("note_type", mw.col.models.current()["name"])

        self.form = preset_form.Ui_Form()
        self.form.setupUi(self)

        self.form.preset_name_input.setText(self.preset["preset_name"])
        self.form.preset_name_input.textEdited.connect(self.update_preset_name)
        if "sentences_allowed" in self.data:
            self.form.sentence_groupbox.setChecked(self.data["sentences_allowed"])

        self.render_note_type_chooser()
        self.render_word_destination_chooser()
        self.render_sentence_destination_chooser()
        self.form.sentence_groupbox.toggled.connect(self.toggle_sentences)

    def render_note_type_chooser(self):
        note_types = [model["name"] for model in self.mw.col.models.all()]
        self.note_type_chooser = list_chooser.ListChooser("Note Type", note_types,
                                                          choice=self.note_type,
                                                          callback=self.update_note_type)
        self.form.note_type_hbox.addWidget(self.note_type_chooser)
        if "note_type" not in self.data:
            self.data["note_type"] = self.note_type
            self.update_preset()

    def render_word_destination_chooser(self):
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        choice = self.data.get("word_destination", fields[0])
        self.word_destination_chooser = list_chooser.ListChooser("Word Destination Field", fields,
                                                                 choice=choice,
                                                                 callback=self.update_word_destination)
        self.form.word_destination_hbox.addWidget(self.word_destination_chooser)
        if "word_destination" not in self.data:
            self.update_word_destination(choice)

    def render_sentence_destination_chooser(self):
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        choice = self.data.get("sentence_destination", fields[1])
        self.sentence_destination_chooser = list_chooser.ListChooser("Sentence Destination Field", fields,
                                                                     choice=choice,
                                                                     callback=self.update_sentence_destination)
        self.form.sentence_destination_hbox.addWidget(self.sentence_destination_chooser)
        if "sentence_destination" not in self.data:
            self.update_sentence_destination(choice)

    def toggle_sentences(self, new_state):
        self.data["sentences_allowed"] = new_state
        self.update_preset()

    def update_preset_name(self):
        self.preset["preset_name"] = self.form.preset_name_input.text()
        self.update_preset()

    def update_note_type(self, choice):
        self.note_type = choice
        self.data["note_type"] = self.note_type
        self.update_preset()
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        self.word_destination_chooser.set_choices(fields)
        self.update_word_destination(self.word_destination_chooser.choice)
        self.sentence_destination_chooser.set_choices(fields)
        if len(fields) > 1:
            self.sentence_destination_chooser.set_choice(self.sentence_destination_chooser.choices[1])
        self.update_sentence_destination(self.sentence_destination_chooser.choice)

    def update_word_destination(self, choice):
        self.data["word_destination"] = choice
        self.update_preset()

    def update_sentence_destination(self, choice):
        self.data["sentence_destination"] = choice
        self.update_preset()

    def update_preset(self):
        if self.on_update_callback:
            self.on_update_callback(self.preset)
