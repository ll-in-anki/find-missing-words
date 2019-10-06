import uuid

from aqt import mw
from aqt.qt import *

from ..forms import config_note_creation_tab as note_creation_form
from .. import utils
from . import note_preset
from .properties import ConfigProperties


class NoteCreationTab(QDialog):
    """
    Config dialog tab for users to define where missing words (and the contextual sentences) are to go.
    A preset holds a name, note type/model, and word destination.
    If the user wants to save sentences, it will also save sentence destination.
    """
    def __init__(self, config, parent=None):
        super().__init__()
        self.config = config
        self.parent = parent
        self.mw = mw

        self.form = note_creation_form.Ui_Form()
        self.form.setupUi(self)
        self.clear_preset_widgets()
        self.presets = self.config[ConfigProperties.NOTE_CREATION_PRESETS.value]
        self.order = []
        self.render_note_creation_settings()

    def render_note_creation_settings(self):
        self.populate_presets()
        self.form.note_preset_list_widget.itemClicked.connect(self.display_preset)
        self.form.btn_preset_add.clicked.connect(self.add_preset)
        self.form.btn_preset_remove.clicked.connect(self.remove_preset)

    def populate_presets(self):
        """
        Generate the list widget and the linked stacked widget which holds all the presets.
        """
        for preset_id in self.presets:
            self.order.append(preset_id)
            preset = self.presets[preset_id]
            self.form.note_preset_list_widget.addItem(preset["preset_name"])
            note_preset_widget = note_preset.NotePreset(self.config, preset, self.update_preset)
            self.form.note_preset_stack.addWidget(note_preset_widget)
        self.form.note_preset_list_widget.setCurrentRow(0)
        self.display_preset()

    @staticmethod
    def generate_uuid():
        """
        Unique id given to each preset for easy addressing
        """
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
        self.order.append(preset_id)
        self.form.note_preset_list_widget.addItem(preset_name)
        self.current_index = self.form.note_preset_list_widget.count() - 1
        self.form.note_preset_list_widget.setCurrentRow(self.current_index)
        note_preset_widget = note_preset.NotePreset(self.config, preset, self.update_preset)
        self.form.note_preset_stack.addWidget(note_preset_widget)
        self.display_preset()

    def update_preset(self, preset):
        self.update_list(preset)
        self.presets[preset["preset_id"]] = preset

    def update_list(self, preset):
        """
        Update preset text in the list widget on preset name change
        :param preset: preset object
        """
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

    def display_preset(self):
        self.current_index = self.form.note_preset_list_widget.currentRow()
        self.form.note_preset_stack.setCurrentIndex(self.current_index)

    def save_presets(self):
        """
        Save action from parent config dialog; save all presets from the stacked widget
        """
        for i in reversed(range(self.form.note_preset_stack.count())):
            note_preset_widget = self.form.note_preset_stack.widget(i)
            preset = note_preset_widget.preset
            self.presets[preset["preset_id"]] = preset
            mw.addonManager.writeConfig(__name__, self.config)

    def clear_preset_widgets(self):
        """
        Close any note creator preset widget instances
        """
        utils.clear_stacked_widget(self.form.note_preset_stack)
