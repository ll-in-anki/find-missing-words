from aqt import mw
from aqt.qt import *
from anki.hooks import runHook

from ..utils import list_chooser, generate_uuid
from ..forms import config_note_preset as preset_form
from ..config.properties import SentenceTypes
from . import sentence_preset


class NotePreset(QWidget):
    """
    Interface to change a note preset, holds basic form fields and a callback fired on every change
    """
    def __init__(self, config, preset, on_update_callback=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.preset = preset
        self.data = preset["preset_data"]
        self.on_update_callback = on_update_callback
        self.mw = mw
        self.note_type = self.data.get("note_type", mw.col.models.current()["name"])

        self.form = preset_form.Ui_Form()
        self.form.setupUi(self)

        self.form.preset_name_input.setText(self.preset["preset_name"])
        self.form.preset_name_input.textEdited.connect(self.update_preset_name)
        if "sentences_allowed" in self.data:
            self.form.sentence_groupbox.setChecked(self.data["sentences_allowed"])

        if "sentence_presets" not in self.data:
            self.add_sentence_preset()
        else:
            self.render_sentence_destination_presets()

        self.render_note_type_chooser()
        self.render_word_destination_chooser()
        self.form.sentence_groupbox.toggled.connect(self.toggle_sentences)
        self.form.add_sentence_preset_button.clicked.connect(self.add_sentence_preset)

    def render_note_type_chooser(self):
        note_types = [model["name"] for model in self.mw.col.models.all()]
        self.note_type_chooser = list_chooser.ListChooser("Note Type", note_types,
                                                          choice=self.note_type,
                                                          callback=self.update_note_type,
                                                          parent=self)
        self.form.note_type_hbox.addWidget(self.note_type_chooser)
        if "note_type" not in self.data:
            self.data["note_type"] = self.note_type
            self.update_preset()

    def render_word_destination_chooser(self):
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        choice = self.data.get("word_destination", fields[0])
        self.word_destination_chooser = list_chooser.ListChooser("Word Destination Field", fields,
                                                                 choice=choice,
                                                                 callback=self.update_word_destination,
                                                                 parent=self)
        self.form.word_destination_hbox.addWidget(self.word_destination_chooser)
        if "word_destination" not in self.data:
            self.update_word_destination(choice)

    def render_sentence_destination_presets(self):
        for preset_id in self.data["sentence_presets"]:
            preset = self.data["sentence_presets"][preset_id]
            preset_widget = sentence_preset.SentencePreset(self.config,
                                                           preset,
                                                           self.note_type,
                                                           on_update=self.update_sentence_preset,
                                                           on_delete=self.delete_sentence_preset,
                                                           parent=self)
            self.form.sentence_groupbox.layout().addWidget(preset_widget)

    def toggle_sentences(self, new_state):
        self.data["sentences_allowed"] = new_state
        self.update_preset()

    def add_sentence_preset(self):
        if "sentence_presets" not in self.data:
            self.data["sentence_presets"] = {}
        preset_id = generate_uuid()
        preset = {
            "sentence_preset_id": preset_id,
            "sentence_type": SentenceTypes.WHOLE.name
        }
        self.data["sentence_presets"][preset_id] = preset
        preset_widget = sentence_preset.SentencePreset(self.config,
                                                       preset,
                                                       self.note_type,
                                                       self.update_sentence_preset,
                                                       self.delete_sentence_preset,
                                                       self)
        self.form.sentence_groupbox.layout().addWidget(preset_widget)

    def update_sentence_preset(self, preset):
        self.data["sentence_presets"][preset["sentence_preset_id"]] = preset
        self.update_preset()

    def delete_sentence_preset(self, preset_widget):
        self.data["sentence_presets"].pop(preset_widget.sentence_preset["sentence_preset_id"])
        self.form.sentence_groupbox.layout().removeWidget(preset_widget)
        preset_widget.deleteLater()

    def update_preset_name(self):
        self.preset["preset_name"] = self.form.preset_name_input.text()
        self.update_preset()

    def update_note_type(self, choice):
        """
        If note type is updated, the word and sentence fields must also stay updated so things don't break.
        Select first field for word (by default) and second field for sentences so that they don't both go to the same
        field and break things.
        :param choice: note type/model string
        """
        self.note_type = choice
        self.data["note_type"] = self.note_type
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        self.word_destination_chooser.set_choices(fields)
        self.update_word_destination(self.word_destination_chooser.choice)
        runHook("sentence_preset.update_destination_fields", fields)
        self.update_preset()

    def update_word_destination(self, choice):
        self.data["word_destination"] = choice
        self.update_preset()

    def update_preset(self):
        if self.on_update_callback:
            self.on_update_callback(self.preset)
