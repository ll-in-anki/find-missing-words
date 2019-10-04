import uuid

from aqt import mw
from aqt.qt import *

from ..forms import config_note_creation_tab as note_creation_form
from .. import utils
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
        self.presets = self.config[ConfigProperties.NOTE_CREATION_PRESETS.value]
        self.order = []
        self.render_note_creation_settings()

    def render_note_creation_settings(self):
        self.populate_presets()
        self.form.note_preset_list_widget.itemClicked.connect(self.display_preset)
        self.form.btn_preset_add.clicked.connect(self.add_preset)
        self.form.btn_preset_remove.clicked.connect(self.remove_preset)

    def populate_presets(self):
        for preset_id in self.presets:
            self.order.append(preset_id)
            self.form.note_preset_list_widget.addItem(self.presets[preset_id]["preset_name"])

    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4().hex)[-6:]

    def add_preset(self):
        preset_name = "New Preset"
        preset_id = self.generate_uuid()
        preset = {
            "preset_id": preset_id,
            "preset_name": preset_name,
            "preset_data": {}
        }
        self.presets[preset_id] = preset
        mw.addonManager.writeConfig(__name__, self.config)
        self.order.append(preset_id)
        self.form.note_preset_list_widget.addItem(preset_name)
        self.current_index = self.form.note_preset_list_widget.count() - 1
        self.form.note_preset_list_widget.setCurrentRow(self.current_index)
        self.display_preset()

    def update_preset(self, preset):
        self.update_list(preset)
        self.presets[preset["preset_id"]] = preset
        mw.addonManager.writeConfig(__name__, self.config)

    def update_list(self, preset):
        list_item = self.form.note_preset_list_widget.currentItem()
        list_item.setText(preset["preset_name"])

    def remove_preset(self):
        if len(self.order) == 0:
            return
        self.current_index = self.form.note_preset_list_widget.currentRow()
        preset_id = self.order[self.current_index]

        widget = self.form.note_preset_stack.currentWidget()
        if widget is not None:
            self.form.note_preset_stack.removeWidget(widget)
            widget.deleteLater()

        self.presets.pop(preset_id)
        self.order.pop(self.current_index)
        item = self.form.note_preset_list_widget.takeItem(self.current_index)
        del item
        mw.addonManager.writeConfig(__name__, self.config)

    def display_preset(self):
        self.clear_preset_widgets()
        self.current_index = self.form.note_preset_list_widget.currentRow()
        preset_id = self.order[self.current_index]
        preset = self.presets[preset_id]
        note_preset_widget = note_preset.NotePreset(self.config, preset, self.update_preset, parent=self)
        self.form.note_preset_stack.addWidget(note_preset_widget)
        self.form.note_preset_stack.setCurrentIndex(self.current_index)

    def clear_preset_widgets(self):
        """
        Close any note creator preset widget instances (usually just one)
        """
        utils.clear_stacked_widget(self.form.note_preset_stack)
