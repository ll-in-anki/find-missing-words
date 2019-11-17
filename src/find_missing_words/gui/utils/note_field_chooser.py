from aqt.qt import *
from aqt import mw

from .note_field_tree import NoteFieldTree


class NoteFieldChooser(QPushButton):
    """
    Button to invoke note and field tree, whose text displays current tree selection.
    The chooser is an interface to the note_field_tree.py and handles the data before and after choosing from the tree.
    Influenced by aqt.deckchooser.DeckChooser.
    """
    def __init__(self, on_update_callback=None, parent=None):
        super().__init__(parent)
        self.mw = mw
        self.on_update_callback = on_update_callback
        self.note_field_items = []
        self.selected_items = []
        self.btn_text = "None"
        self.clicked.connect(self.invoke_note_field_tree)
        self.setAutoDefault(False)

        self.setup_note_field_data()
        self.update_btn()

    def setup_note_field_data(self):
        all_note_types = self.mw.col.models.all()
        self.note_field_items = []
        for note_type in all_note_types:
            note_dict = {"name": note_type["name"], "state": Qt.Unchecked}
            note_fields = []
            for field in note_type["flds"]:
                field_dict = {"name": field["name"], "state": Qt.Unchecked}
                note_fields.append(field_dict)
            note_dict["fields"] = note_fields
            self.note_field_items.append(note_dict)

    def set_selected_items(self, selected_note_field_items):
        """
        Merge note field tree with another note field tree of checked items
        :param selected_note_field_items: note field tree with checked items
        """
        for note in self.note_field_items:
            note_name = note["name"]
            fields = note["fields"]
            for new_note in selected_note_field_items:
                if note_name == new_note["name"]:
                    note["state"] = new_note["state"]
                    new_note_fields = new_note["fields"]
                    for field in fields:
                        for new_field in new_note_fields:
                            if field["name"] == new_field["name"]:
                                field["state"] = new_field["state"]
        self.update_btn(selected_note_field_items)

    def invoke_note_field_tree(self):
        ret = NoteFieldTree(self.note_field_items, self)
        self.note_field_items = ret.all_items
        self.update_btn(ret.selected_items)

    def update_btn(self, selected_items=None):
        """
        Make choice, update chooser button text with formatted text no longer than 15 chars
        :param selected_items: note/field tree selection
        """
        if not selected_items:
            self.btn_text = "None"
        else:
            formatted_selected_items = self.format_btn_text(selected_items)
            if len(formatted_selected_items) > 15:
                self.btn_text = formatted_selected_items[:15] + '...'
            else:
                self.btn_text = formatted_selected_items
            self.setToolTip(formatted_selected_items)
        self.selected_items = selected_items
        self.setText(self.btn_text)
        if self.on_update_callback:
            self.on_update_callback()

    @staticmethod
    def format_btn_text(items):
        """
        Format: Note Type (Field1, Field 2), Note Type 2, ...
        :param items: note/field tree selection
        :return: formatted string of the tree selection
        """
        note_field_list = []
        for note in items:
            name = note["name"]
            fields = ', '.join([field["name"] for field in note["fields"]])
            result = name + '(' + fields + ')'
            note_field_list.append(result)
        return ', '.join(note_field_list)
