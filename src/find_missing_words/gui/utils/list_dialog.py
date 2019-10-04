from aqt.qt import *

from ..forms import list_dialog as list_dialog_form


class ListDialog(QDialog):
    def __init__(self, window_title, items, selected_item=None):
        super().__init__()
        self.form = list_dialog_form.Ui_Dialog()
        self.form.setupUi(self)
        self.setWindowTitle(window_title)
        self.items = items
        self.selected_item = selected_item
        self.populate_list()
        self.exec_()

    def populate_list(self):
        self.form.list_widget.addItems(self.items)
        if self.selected_item:
            self.set_current_item(self.selected_item)

    def get_current_item(self):
        return self.form.list_widget.currentItem().text()

    def set_current_item(self, item_text):
        if item_text in self.items:
            self.form.list_widget.setCurrentRow(self.items.index(item_text))

    def accept(self):
        self.selected_item = self.get_current_item()
        super().accept()
