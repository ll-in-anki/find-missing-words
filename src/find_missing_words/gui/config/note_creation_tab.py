from aqt import mw
from aqt.qt import *

from ..forms import config_note_creation_tab as note_creation_form
from . import note_preset
from .properties import ConfigProperties


class NoteCreationTab(QDialog):
    def __init__(self, config, parent=None):
        super().__init__()
        self.config = config
        self.parent = parent
        self.mw = mw

        self.form = note_creation_form.Ui_Form()
        self.form.setupUi(self)
        self.note_creation_presets = mw.addonManager.getConfig(__name__)[ConfigProperties.NOTE_CREATION_PRESETS.value]
        self.render_note_creation_settings()

    def render_note_creation_settings(self):
        self.populate_note_creation_presets()
        self.form.note_preset_list_widget.itemClicked.connect(self.display_note_creation_preset)
        self.form.btn_preset_add.clicked.connect(self.add_note_creation_preset)
        self.form.btn_preset_remove.clicked.connect(self.remove_note_creation_preset)

    def populate_note_creation_presets(self):
        presets = self.config[ConfigProperties.NOTE_CREATION_PRESETS.value]
        for preset in presets:
            self.form.note_preset_list_widget.addItem(preset["preset_name"])

    def add_note_creation_preset(self):
        preset_name = "New Preset"
        preset = {
            "preset_name": preset_name,
            "preset_data": {}
        }
        note_preset_widget = note_preset.NotePreset(preset)
        note_preset_widget.form.preset_name_input.selectAll()
        self.form.note_preset_stack.addWidget(note_preset_widget)
        self.form.note_preset_list_widget.addItem(preset_name)
        self.current_index = self.form.note_preset_list_widget.count() - 1
        self.form.note_preset_stack.setCurrentIndex(self.current_index)

    def remove_note_creation_preset(self):
        pass

    def display_note_creation_preset(self):
        self.clear_note_creation_preset_widgets()
        self.current_index = self.form.note_preset_list_widget.currentRow()
        preset = self.note_creation_presets[self.current_index]
        note_preset_widget = note_preset.NotePreset(preset)
        self.form.note_stacked_widget.addWidget(note_preset_widget)
        self.form.note_stacked_widget.setCurrentIndex(self.current_index)

    def clear_note_creation_preset_widgets(self):
        """
        Close any note creator preset widget instances (usually just one)
        """
        for i in range(self.form.note_preset_stack.count()):
            widget = self.form.note_preset_stack.widget(i)
            if widget:
                self.form.note_preset_stack.removeWidget(widget)
                widget.deleteLater()
