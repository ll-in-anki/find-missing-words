from aqt import mw
from aqt.qt import *

from .. import note_field_chooser
from ..forms import config_note_preset as preset_form


class NotePreset(QWidget):
    def __init__(self, config, preset, on_update_callback, parent=None):
        super().__init__()
        self.config = config
        self.preset = preset
        self.data = preset["preset_data"]
        self.on_update_callback = on_update_callback
        self.parent = parent
        self.mw = mw

        self.form = preset_form.Ui_Form()
        self.form.setupUi(self)

        self.form.preset_name_input.setText(self.preset["preset_name"])
        self.form.preset_name_input.textEdited.connect(self.update_preset_name)

        self.render_word_destination_note_field_chooser()

    def render_word_destination_note_field_chooser(self):
        self.word_destination_note_field_chooser_parent_widget = QWidget()
        self.word_destination_note_field_chooser = note_field_chooser.NoteFieldChooser(mw,
                                                                                       self.word_destination_note_field_chooser_parent_widget,
                                                                                       self.update_word_destination,
                                                                                       single_selection_mode=True)
        if "word_destination" in self.data:
            self.word_destination_note_field_chooser.set_single_selected_item(self.data["word_destination"])
        self.form.word_destination_hbox.addWidget(self.word_destination_note_field_chooser_parent_widget)

    def update_preset_name(self):
        self.preset["preset_name"] = self.form.preset_name_input.text()
        self.update_preset()

    def update_word_destination(self):
        self.data["word_destination"] = self.word_destination_note_field_chooser.selected_items
        self.update_preset()

    def update_preset(self):
        self.on_update_callback(self.preset)
