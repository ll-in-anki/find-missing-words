# import the main window object (mw) from aqt
from aqt import mw

# import all of the Qt GUI library
from aqt.qt import *

from .views import tabs


class UI(QWidget):
    def __init__(self):
        super().__init__()
        self.parent = mw
        self.setupMenu()

    def setupMenu(self):
        action = QAction("LL", mw)
        action.triggered.connect(self.showUI)
        mw.form.menuTools.addAction(action)

        # Setup config button
        # mw.addonManager.setConfigAction(addon_id, self.show_config)

    def showUI(self):
        mainLayout = QVBoxLayout()

        # Layout tabs
        self.tabs = tabs.Tabs()
        mainLayout.addWidget(self.tabs)

        # Add an horizontal line
        mainLayout.addWidget(self.hLine())

        # Bottom button(s)
        closeButton = QPushButton("Done")
        closeButton.clicked.connect(self.close)
        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)
        btnLayout.addWidget(closeButton)
        mainLayout.addLayout(btnLayout)

        # Center the window
        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.setLayout(mainLayout)
        self.setWindowTitle("LL")
        self.show()
        self.raise_()
        self.activateWindow()

    def hLine(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line
