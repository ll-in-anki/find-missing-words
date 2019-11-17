from aqt import mw
from aqt.qt import *
from anki.hooks import addHook, remHook

from ..utils import list_chooser
from ..forms import config_sentence_preset as sentence_form
from ..config.properties import SentenceTypes


class SentencePreset(QWidget):
    def __init__(self, config, sentence_preset, note_type, on_update=None, on_delete=None, parent=None):
        super().__init__(parent)
        self.config = config
        self.sentence_preset = sentence_preset
        self.note_type = note_type
        self.on_update = on_update
        self.on_delete = on_delete
        self.mw = mw

        self.form = sentence_form.Ui_Form()
        self.form.setupUi(self)
        if "sentence_type" in self.sentence_preset:
            type_description = SentenceTypes[self.sentence_preset["sentence_type"]].value
            self.form.sentence_type_combo_box.setCurrentText(type_description)
        self.render_sentence_destination()
        self.form.delete_button.clicked.connect(self.delete)
        self.form.sentence_type_combo_box.currentTextChanged.connect(self.update_sentence_preset_type)
        addHook("sentence_preset.update_destination_fields", self.update_sentence_destination_fields)
        addHook("find_missing_words_config.tear_down", self.tear_down)

    def render_sentence_destination(self):
        fields = [field["name"] for field in mw.col.models.byName(self.note_type)["flds"]]
        choice = self.sentence_preset.get("sentence_destination", fields[1])
        self.sentence_destination_chooser = list_chooser.ListChooser("Sentence Destination Field", fields,
                                                                     choice=choice,
                                                                     callback=self.update_sentence_destination,
                                                                     parent=self)
        self.layout().insertWidget(1, self.sentence_destination_chooser)
        if "sentence_destination" not in self.sentence_preset:
            self.update_sentence_destination(choice)

    def update_sentence_preset_type(self, text):
        sentence_type = SentenceTypes(text).name
        self.sentence_preset["sentence_type"] = sentence_type
        self.on_update(self.sentence_preset)

    def update_sentence_destination_fields(self, fields):
        self.sentence_destination_chooser.set_choices(fields)

    def update_sentence_destination(self, choice):
        self.sentence_preset["sentence_destination"] = choice
        self.on_update(self.sentence_preset)

    def tear_down(self):
        remHook("sentence_preset.update_destination_fields", self.update_sentence_destination_fields)
        remHook("find_missing_words_config.remHooks", self.tear_down)

    def delete(self):
        self.tear_down()
        self.on_delete(self)
