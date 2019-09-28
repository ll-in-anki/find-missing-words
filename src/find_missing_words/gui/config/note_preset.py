from aqt import mw
from aqt.qt import *

from .. import note_field_chooser
from ..forms import config_note_preset as preset_form
from .properties import ConfigProperties


class NotePreset(QWidget):
    def __init__(self, preset, parent=None):
        super().__init__()
        self.name = preset["preset_name"]
        self.data = preset["preset_data"]
        self.parent = parent
        self.mw = mw

        self.form = preset_form.Ui_Form()
        self.form.setupUi(self)

        self.render_word_destination_note_field_chooser()

    def render_word_destination_note_field_chooser(self):
        self.word_destination_note_field_chooser_parent_widget = QWidget()
        self.word_destination_note_field_chooser = note_field_chooser.NoteFieldChooser(mw,
                                                                                       self.word_destination_note_field_chooser_parent_widget,
                                                                                       self.set_note_creation_preset,
                                                                                       single_selection_mode=True)
        if "word_destination" in self.data:
            self.word_destination_note_field_chooser.set_single_selected_item(self.data["word_destination"])
        self.form.word_destination_hbox.addWidget(self.word_destination_note_field_chooser_parent_widget)

    def set_note_creation_preset(self):
        self.word_destination_note_field = self.word_destination_note_field_chooser.selected_items
        result = {
            "preset_name": self.name,
            "preset_data": {"word_destination": self.word_destination_note_field}
        }
        config = mw.addonManager.getConfig(__name__)
        presets = config[ConfigProperties.NOTE_CREATION_PRESETS]
        presets.append(result)
        config.update({ConfigProperties.NOTE_CREATION_PRESETS.value: presets})
