from aqt.qt import *


class ModelFieldTree(QDialog):
    def __init__(self, mw, model_fields):
        super().__init__()
        self.mw = mw
        self.model_fields = model_fields
        self.selected_items = []
        self.setWindowTitle("Notes and Fields")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.render()
        self.exec_()

    def render(self):
        self.render_select_all_none_buttons()
        self.render_tree()
        self.render_buttons()

    def render_select_all_none_buttons(self):
        self.select_btn_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all)
        self.select_none_btn = QPushButton("Select None")
        self.select_none_btn.clicked.connect(self.select_none)

        self.select_btn_layout.addStretch(1)
        self.select_btn_layout.addWidget(self.select_all_btn)
        self.select_btn_layout.addWidget(self.select_none_btn)
        self.layout.addLayout(self.select_btn_layout)

    def get_all_items(self, onlyChecked=False):
        items = []
        num_models = self.tree.topLevelItemCount()
        for i in range(num_models):
            model = self.tree.topLevelItem(i)
            if onlyChecked and model.checkState(0) == Qt.Unchecked:
                continue
            model_dict = {"name": model.text(0), "state": model.checkState(0)}
            fields = []
            for j in range(model.childCount()):
                field = model.child(j)
                if onlyChecked and field.checkState(0) == Qt.Unchecked:
                    continue
                field_dict = {"name": field.text(0), "state": field.checkState(0)}
                fields.append(field_dict)
            model_dict["fields"] = fields
            items.append(model_dict)
        return items

    def select_all(self):
        num_models = self.tree.topLevelItemCount()
        for i in range(num_models):
            self.tree.topLevelItem(i).setCheckState(0, Qt.Checked)

    def select_none(self):
        num_models = self.tree.topLevelItemCount()
        for i in range(num_models):
            self.tree.topLevelItem(i).setCheckState(0, Qt.Unchecked)

    def render_tree(self):
        self.tree = QTreeWidget()
        for model in self.model_fields:
            model_tree_item = QTreeWidgetItem(self.tree, [model["name"]])
            for field in model["fields"]:
                field_tree_item = QTreeWidgetItem(model_tree_item, [field["name"]])
                field_tree_item.setCheckState(0, field["state"])
            model_tree_item.setCheckState(0, model["state"])
            model_tree_item.setFlags(model_tree_item.flags() | Qt.ItemIsAutoTristate)
            model_tree_item.setExpanded(True)

        self.layout.addWidget(self.tree)

    def render_buttons(self):
        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(btns)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.button_box)
        self.layout.addLayout(self.btn_layout)

    def accept(self):
        self.all_items = self.get_all_items()
        self.selected_items = self.get_all_items(True)
        super().accept()
