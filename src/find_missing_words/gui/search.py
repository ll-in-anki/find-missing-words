from aqt import mw

from aqt.qt import *

from .forms import search as search_form


class Search(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.parent = parent
        # Set up UI from pre-generated UI form:
        self.form = search_form.Ui_MainWindow()
        self.form.setupUi(self)
