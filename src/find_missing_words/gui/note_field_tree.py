from aqt import mw
from aqt.qt import *

from .forms import note_field_tree as tree_form


class NoteFieldTree(QDialog):
    def __init__(self, note_fields, parent=None):
        super().__init__()
        self.mw = mw
        self.parent = parent or mw
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
        num_models = self.form.tree_widget.topLevelItemCount()
        for i in range(num_models):
            model = self.form.tree_widget.topLevelItem(i)
            if only_checked and model.checkState(0) == Qt.Unchecked:
                continue
            model_dict = {"name": model.text(0), "state": model.checkState(0)}
            fields = []
            for j in range(model.childCount()):
                field = model.child(j)
                if only_checked and field.checkState(0) == Qt.Unchecked:
                    continue
                field_dict = {"name": field.text(0), "state": field.checkState(0)}
                fields.append(field_dict)
            model_dict["fields"] = fields
            items.append(model_dict)
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
        for model in self.note_fields:
            model_tree_item = QTreeWidgetItem(self.form.tree_widget, [model["name"]])
            for field in model["fields"]:
                field_tree_item = QTreeWidgetItem(model_tree_item, [field["name"]])
                field_tree_item.setCheckState(0, field["state"])
            model_tree_item.setCheckState(0, model["state"])
            model_tree_item.setFlags(model_tree_item.flags() | Qt.ItemIsAutoTristate)
            model_tree_item.setExpanded(False)

    def accept(self):
        self.all_items = self.get_all_items()
        self.selected_items = self.get_all_items(True)
        super().accept()