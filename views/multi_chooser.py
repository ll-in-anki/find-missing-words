from aqt.qt import *


class MultiChooser(QDialog):
    def __init__(self, list_items, window_title="Chooser", grouped=False):
        super().__init__()
        self.list_items = list_items
        self.setWindowTitle(window_title)
        self.grouped = grouped
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.render()
        self.exec_()

    def render(self):
        self.render_filter()
        if self.grouped:
            self.render_tree()
        else:
            self.render_list()
        self.render_buttons()

    def render_filter(self):
        self.horizontalLayout = QHBoxLayout()                         
        self.label = QLabel("Filter:")                                   
        self.horizontalLayout.addWidget(self.label)                             
        self.filter = QLineEdit()                               
        self.filter.textEdited.connect(self.redraw)
        self.horizontalLayout.addWidget(self.filter)                            
        self.layout.addLayout(self.horizontalLayout)

    def render_list(self):
        self.list = QListWidget()                               
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list.addItems(self.list_items)
        self.layout.addWidget(self.list)

    def render_tree(self):
        self.tree = QTreeWidget()
        self.tree.setColumnCount(1)
        root_items = []
        for root_item in self.list_items:
            child_items = []
            for child_item in self.list_items[root_item]:
                child_items.append(QTreeWidgetItem(root_item, [child_item]))
            root_items.append(QTreeWidgetItem(self.tree, [root_item]))
        self.tree.insertTopLevelItems(None, root_items)

        self.layout.addWidget(self.tree)


    def get_list_items(self):
        return [str(item.text()) for item in self.list.selectedItems()]

    def redraw(self):
        self.list.clear()
        self.list.addItems(self.list_items)
        filtered_items = [str(item.text()) for item in self.list.findItems(self.filter.text(), Qt.MatchContains)]
        self.list.clear()
        self.list.addItems(filtered_items)

    def render_buttons(self):
        btns = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.button_box = QDialogButtonBox(btns)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.btn_layout = QVBoxLayout()
        self.btn_layout.addWidget(self.button_box)
        self.layout.addLayout(self.btn_layout)

    def accept(self):
        self.selected_items = self.get_list_items()
        super().accept()

