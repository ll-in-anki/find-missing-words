from aqt.qt import *


class MultiChooser(QDialog):
    def __init__(self, list_items, window_title):
        super().__init__()
        self.list_items = list_items
        self.setWindowTitle("HELLO!")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.render()
        self.exec_()

    def render(self):
        self.render_filter()
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

    def get_list_items(self):
        return self.list.selectedItems()

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
