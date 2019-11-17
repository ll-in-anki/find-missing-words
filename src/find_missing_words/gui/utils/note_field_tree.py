"""
A hierarchical view for the relationship between note types and their fields.
See docs/data-structures/note_field_tree.md for details on the data structure.
"""

from aqt.qt import *

from ..forms import note_field_tree as tree_form


class NoteFieldTree(QDialog):
    """
    Dialog containing tree widget that organizes notes/models and their fields
    """

    def __init__(self, note_fields, parent=None):
        super().__init__(parent)
        self.note_fields = note_fields
        self.form = tree_form.Ui_Dialog()
        self.form.setupUi(self)

        self.selected_items = []
        self.all_items = []

        self.form.btn_expand_all.clicked.connect(self.expand_all)
        self.form.btn_expand_none.clicked.connect(self.expand_none)
        self.form.btn_select_all.clicked.connect(self.select_all)
        self.form.btn_select_none.clicked.connect(self.select_none)
        self.form.buttonBox.accepted.connect(self.accept)

        self.render_tree()
        self.exec_()

    def get_all_items(self, only_checked=False):
        items = []
        num_notes = self.form.tree_widget.topLevelItemCount()
        for i in range(num_notes):
            note = self.form.tree_widget.topLevelItem(i)
            if only_checked and note.checkState(0) == Qt.Unchecked:
                continue
            note_dict = {"name": note.text(0), "state": note.checkState(0)}
            fields = []
            for j in range(note.childCount()):
                field = note.child(j)
                if only_checked and field.checkState(0) == Qt.Unchecked:
                    continue
                field_dict = {"name": field.text(0), "state": field.checkState(0)}
                fields.append(field_dict)
            note_dict["fields"] = fields
            items.append(note_dict)
        return items

    def select_all(self):
        for i in range(self.form.tree_widget.topLevelItemCount()):
            self.form.tree_widget.topLevelItem(i).setCheckState(0, Qt.Checked)

    def select_none(self):
        for i in range(self.form.tree_widget.topLevelItemCount()):
            self.form.tree_widget.topLevelItem(i).setCheckState(0, Qt.Unchecked)

    def expand_all(self):
        for i in range(self.form.tree_widget.topLevelItemCount()):
            self.form.tree_widget.topLevelItem(i).setExpanded(True)

    def expand_none(self):
        for i in range(self.form.tree_widget.topLevelItemCount()):
            self.form.tree_widget.topLevelItem(i).setExpanded(False)

    def render_tree(self):
        self.form.tree_widget.setHeaderLabel("")
        for note in self.note_fields:
            note_tree_item = QTreeWidgetItem(self.form.tree_widget, [note["name"]])
            for field in note["fields"]:
                field_tree_item = QTreeWidgetItem(note_tree_item, [field["name"]])
                field_tree_item.setCheckState(0, field["state"])
            note_tree_item.setCheckState(0, note["state"])
            note_tree_item.setFlags(note_tree_item.flags() | Qt.ItemIsAutoTristate)
            note_tree_item.setExpanded(False)

    def accept(self):
        self.all_items = self.get_all_items()
        self.selected_items = self.get_all_items(True)
        super().accept()
