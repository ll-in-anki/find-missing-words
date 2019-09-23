from aqt.qt import *
from anki.hooks import runHook


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=-1, hspacing=-1, vspacing=-1):
        super().__init__(parent)
        self._hspacing = hspacing
        self._vspacing = vspacing
        self._items = []
        self.setContentsMargins(margin, margin, margin, margin)

    def __del__(self):
        del self._items[:]

    def addItem(self, item):
        self._items.append(item)

    def horizontalSpacing(self):
        if self._hspacing >= 0:
            return self._hspacing
        return self.smartSpacing(
            QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self._vspacing >= 0:
            return self._vspacing
        return self.smartSpacing(
            QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self._items)

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)

    def expandingDirections(self):
        return Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._items:
            size = size.expandedTo(item.minimumSize())
        left, top, right, bottom = self.getContentsMargins()
        size += QSize(left + right, top + bottom)
        return size

    def doLayout(self, rect, testonly):
        left, top, right, bottom = self.getContentsMargins()
        effective = rect.adjusted(+left, +top, -right, -bottom)
        x = effective.x()
        y = effective.y()
        lineheight = 0
        for item in self._items:
            widget = item.widget()
            hspace = self.horizontalSpacing()
            if hspace == -1:
                hspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, Qt.Horizontal)
            vspace = self.verticalSpacing()
            if vspace == -1:
                vspace = widget.style().layoutSpacing(
                    QSizePolicy.PushButton,
                    QSizePolicy.PushButton, Qt.Vertical)
            nextX = x + item.sizeHint().width() + hspace
            if nextX - hspace > effective.right() and lineheight > 0:
                x = effective.x()
                y = y + lineheight + vspace
                nextX = x + item.sizeHint().width() + hspace
                lineheight = 0
            if not testonly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
            x = nextX
            lineheight = max(lineheight, item.sizeHint().height())
        return y + lineheight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        if parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        return parent.spacing()


class Bubble(QLabel):
    def __init__(self, text, known, note_ids):
        super().__init__(text)
        self.word = text
        self.known = known
        self.note_ids = note_ids
        self.setContentsMargins(5, 5, 5, 5)
        self.setCursor(Qt.PointingHandCursor)

    def paintEvent(self, event):
        if not self.known:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.drawRoundedRect(
                0, 0, self.width() - 1, self.height() - 1, 5, 5)
            self.setStyleSheet("background: lightgreen")
        super().paintEvent(event)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        runHook("clear_notes")
        runHook("display_word", self.word)
        runHook("populate_notes", self.note_ids)


class WordSelect(QScrollArea):
    def __init__(self, word_model, parent=None):
        super().__init__()
        self.parent = parent

        widget = QWidget(self)
        self.setWidgetResizable(True)
        self.setWidget(widget)

        widget.setMinimumWidth(50)
        layout = FlowLayout(widget)

        self.words = []
        for word in word_model:
            known = word_model[word]["known"]
            note_ids = word_model[word]["note_ids"]
            word_bubble = Bubble(word, known, note_ids)
            word_bubble.setFixedWidth(word_bubble.sizeHint().width())
            self.words.append(word_bubble)
            layout.addWidget(word_bubble)
