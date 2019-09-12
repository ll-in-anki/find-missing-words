# import the main window object (mw) from aqt
from aqt import mw

# import all of the Qt GUI library
from aqt.qt import *

from .views import tabs


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.parent = mw
        self.setup_menu()

    def setup_menu(self):
        action = QAction("LL", mw)
        action.triggered.connect(self.render)
        mw.form.menuTools.addAction(action)

        # Setup config button
        # mw.addonManager.setConfigAction(addon_id, self.show_config)

    def render(self):
        main_layout = QVBoxLayout()

        # Layout tabs
        self.tabs = tabs.Tabs()
        main_layout.addWidget(self.tabs)

        # Center the window
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.setLayout(main_layout)
        self.setWindowTitle("LL")
        self.show()
        self.raise_()
        self.activateWindow()
