from aqt import mw

from aqt.qt import *

from .forms import search as search_form


class Search(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # Set up UI from pre-generated UI form:
        self.form = search_form.Ui_Form()
        self.form.setupUi(self)
        self.show()
        self.raise_()
        self.activateWindow()
