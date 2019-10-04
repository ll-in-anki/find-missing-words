from aqt.qt import *
from aqt import mw

from . import list_dialog


class ListChooser(QPushButton):
    """
    Choose a single item from a list of strings
    """
    def __init__(self, title, choices, choice=None, callback=None):
        super().__init__()
        self.mw = mw
        self.title = title
        self.choices = choices
        self.choice = choice
        self.callback = callback
        self.update_button()
        self.clicked.connect(self.on_choice_change)

    def show(self):
        self.show()

    def hide(self):
        self.hide()

    def set_choice(self, choice):
        self.choice = choice
        self.update_button()
        self.callback(self.choice)

    def set_choices(self, choices):
        self.choices = choices
        self.choice = None
        self.update_button()
        self.callback(self.choice)

    def on_choice_change(self):
        returned_list = list_dialog.ListDialog(self.title, self.choices, self.choice)
        if not returned_list.selected_item:
            return
        self.choice = returned_list.selected_item
        self.update_button()
        self.callback(self.choice)

    def update_button(self):
        if not self.choice:
            self.choice = self.choices[0]
        self.setText(self.choice)
        self.mw.reset()
