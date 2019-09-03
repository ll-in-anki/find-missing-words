from aqt.qt import *


class ModelFieldTree(QDialog):
    def __init__(self, mw, model_fields, window_title="Chooser"):
        super().__init__()
        self.mw = mw
        self.model_fields = model_fields
        self.selected_items = []
        self.setWindowTitle(window_title)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.render()
        self.exec_()

    def render(self):
        # self.render_filter()
        self.render_select_all_none_buttons()
        self.render_tree()
        self.render_buttons()

    def render_filter(self):
        self.horizontalLayout = QHBoxLayout()                         
        self.label = QLabel("Filter:")                                   
        self.horizontalLayout.addWidget(self.label)                             
        self.filter = QLineEdit()                               
        self.filter.textEdited.connect(self.redraw)
        self.horizontalLayout.addWidget(self.filter)                            
        self.layout.addLayout(self.horizontalLayout)

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

    def get_all_items(self):
        items = []
        num_items = self.tree.topLevelItemCount()
        for i in range(num_items):
            item = self.tree.topLevelItem(i)
            items.append(item)
        return items

    def select_all(self):
        for item in self.get_all_items():
            item.setCheckState(0, Qt.Checked)

    def select_none(self):
        for item in self.get_all_items():
            item.setCheckState(0, Qt.Unchecked)

    def create_tree_items(self):
        tree_items = []
        for item in self.items:
            tree_item = QTreeWidgetItem([""] + item)
            tree_item.setData(1, 0, item)
            tree_items.append(tree_item)
        return tree_items

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

    def get_selected_items(self):
        return [item for item in self.get_all_items() if item.checkState(0) == Qt.Checked]

    def redraw(self):
        self.tree.clear()
        self.tree.addTopLevelItems(self.create_tree_items())
        filtered_fields = [item for item in self.tree.findItems(self.filter.text(), Qt.MatchContains, column=1)].copy()
        # filtered_models = [item for item in self.tree.findItems(self.filter.text(), Qt.MatchContains, column=2)]
        self.tree.clear()
        self.tree.addTopLevelItems(filtered_fields)
        # self.tree.addTopLevelItems(filtered_models)

    def render_buttons(self):
        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(btns)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.button_box)
        self.layout.addLayout(self.btn_layout)

    def accept(self):
        self.selected_items = self.get_selected_items()
        super().accept()

