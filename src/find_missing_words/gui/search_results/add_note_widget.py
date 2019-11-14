from anki.lang import _
from aqt.qt import *
from aqt.utils import showWarning, askUser, shortcut, tooltip, openHelp, addCloseShortcut, downArrow
from anki.sound import clearAudioQueue
from anki.hooks import addHook, remHook, runHook
from anki.utils import htmlToTextLine, isMac
import aqt.editor, aqt.modelchooser, aqt.deckchooser

from ..forms import add_note_widget as add_note_form


class AddNoteWidget(QWidget):
    """
    Widget version of the original Anki Add Cards dialog.
    Allows for nesting in parent widget.
    Not much changed other than the QWidget overrides.
    """
    def __init__(self, mw, note=None, on_add_callback=None, on_cancel_callback=None, parent=None):
        super().__init__(parent)
        self.mw = mw
        self.note = note
        self.on_add_callback = on_add_callback
        self.on_cancel_callback = on_cancel_callback
        self.form = add_note_form.Ui_Form()
        self.form.setupUi(self)
        self.setupChoosers()
        self.setupEditor()
        self.setupButtons()
        self.onReset()
        self.history = []
        addHook('reset', self.onReset)
        addHook('currentModelChanged', self.onModelChange)
        addCloseShortcut(self)
        self.show()

    def setupEditor(self):
        self.editor = aqt.editor.Editor(
            self.mw, self.form.editor_widget, self, True)
        self.editor.setNote(self.note)

    def setupChoosers(self):
        self.modelChooser = aqt.modelchooser.ModelChooser(
            self.mw, self.form.model_chooser_widget)
        self.deckChooser = aqt.deckchooser.DeckChooser(
            self.mw, self.form.deck_chooser_widget)

    def helpRequested(self):
        openHelp("addingnotes")

    def setupButtons(self):
        bb = self.form.buttonBox
        ar = QDialogButtonBox.ActionRole
        # add
        self.addButton = bb.addButton(_("Add"), ar)
        self.addButton.clicked.connect(self.addCards)
        self.addButton.setShortcut(QKeySequence("Ctrl+Return"))
        self.addButton.setToolTip(shortcut(_("Add (shortcut: ctrl+enter)")))
        # cancel
        self.cancel_button = QPushButton(_("Cancel"))
        self.cancel_button.setAutoDefault(False)
        bb.addButton(self.cancel_button, QDialogButtonBox.RejectRole)
        self.cancel_button.clicked.connect(self.cancel)
        # help
        self.helpButton = QPushButton(_("Help"), clicked=self.helpRequested)
        self.helpButton.setAutoDefault(False)
        bb.addButton(self.helpButton, QDialogButtonBox.HelpRole)
        # history
        b = bb.addButton(
            _("History")+ " "+downArrow(), ar)
        if isMac:
            sc = "Ctrl+Shift+H"
        else:
            sc = "Ctrl+H"
        b.setShortcut(QKeySequence(sc))
        b.setToolTip(_("Shortcut: %s") % shortcut(sc))
        b.clicked.connect(self.onHistory)
        b.setEnabled(False)
        self.historyButton = b

    def setAndFocusNote(self, note):
        self.editor.setNote(note, focusTo=0)

    def onModelChange(self):
        oldNote = self.editor.note
        note = self.mw.col.newNote()
        if oldNote:
            oldFields = list(oldNote.keys())
            newFields = list(note.keys())
            for n, f in enumerate(note.model()['flds']):
                fieldName = f['name']
                try:
                    oldFieldName = oldNote.model()['flds'][n]['name']
                except IndexError:
                    oldFieldName = None
                # copy identical fields
                if fieldName in oldFields:
                    note[fieldName] = oldNote[fieldName]
                # set non-identical fields by field index
                elif oldFieldName and oldFieldName not in newFields:
                    try:
                        note.fields[n] = oldNote.fields[n]
                    except IndexError:
                        pass
            self.removeTempNote(oldNote)
        self.editor.setNote(note)

    def onReset(self, model=None, keep=False):
        oldNote = self.editor.note
        note = self.mw.col.newNote()
        flds = note.model()['flds']
        # copy fields from old note
        if oldNote:
            if not keep:
                self.removeTempNote(oldNote)
            for n in range(len(note.fields)):
                try:
                    if not keep or flds[n]['sticky']:
                        note.fields[n] = oldNote.fields[n]
                    else:
                        note.fields[n] = ""
                except IndexError:
                    break
        self.setAndFocusNote(note)

    def removeTempNote(self, note):
        if not note or not note.id:
            return
        # we don't have to worry about cards; just the note
        self.mw.col._remNotes([note.id])

    def addHistory(self, note):
        self.history.insert(0, note.id)
        self.history = self.history[:15]
        self.historyButton.setEnabled(True)

    def onHistory(self):
        m = QMenu(self)
        for nid in self.history:
            if self.mw.col.findNotes("nid:%s" % nid):
                fields = self.mw.col.getNote(nid).fields
                txt = htmlToTextLine(", ".join(fields))
                if len(txt) > 30:
                    txt = txt[:30] + "..."
                a = m.addAction(_("Edit \"%s\"") % txt)
                a.triggered.connect(lambda b, nid=nid: self.editHistory(nid))
            else:
                a = m.addAction(_("(Note deleted)"))
                a.setEnabled(False)
        runHook("AddCards.onHistory", self, m)
        m.exec_(self.historyButton.mapToGlobal(QPoint(0,0)))

    def editHistory(self, nid):
        browser = aqt.dialogs.open("Browser", self.mw)
        browser.form.searchEdit.lineEdit().setText("nid:%d" % nid)
        browser.onSearchActivated()

    def addNote(self, note):
        note.model()['did'] = self.deckChooser.selectedId()
        ret = note.dupeOrEmpty()
        if ret == 1:
            showWarning(_(
                "The first field is empty."),
                help="AddItems#AddError")
            return
        if '{{cloze:' in note.model()['tmpls'][0]['qfmt']:
            if not self.mw.col.models._availClozeOrds(
                    note.model(), note.joinedFields(), False):
                if not askUser(_("You have a cloze deletion note type "
                "but have not made any cloze deletions. Proceed?")):
                    return
        cards = self.mw.col.addNote(note)
        if not cards:
            showWarning(_("The input you have provided would make an empty question on all cards."), help="AddItems")
            return
        self.addHistory(note)
        self.mw.requireReset()
        return note

    def addCards(self):
        self.editor.saveNow(self._addCards)

    def _addCards(self):
        self.editor.saveAddModeVars()
        note = self.editor.note
        note = self.addNote(note)
        if not note:
            return
        tooltip(_("Added"), period=500)
        # stop anything playing
        clearAudioQueue()
        self.onReset(keep=True)
        self.mw.col.autosave()
        self.close()
        self.on_add_callback(note)

    def keyPressEvent(self, evt):
        "Show answer on RET or register answer."
        if (evt.key() in (Qt.Key_Enter, Qt.Key_Return)
            and self.editor.tags.hasFocus()):
            evt.accept()
            return
        return super().keyPressEvent(evt)

    def cancel(self):
        can_close = self.confirm_close()
        if can_close:
            self.close()
            self.on_cancel_callback()
        return can_close

    def cleanup(self):
        remHook('reset', self.onReset)
        remHook('currentModelChanged', self.onModelChange)
        clearAudioQueue()
        self.removeTempNote(self.editor.note)
        self.editor.cleanup()
        self.modelChooser.cleanup()
        self.deckChooser.cleanup()
        self.mw.maybeReset()

    def closeEvent(self, event):
        self.cleanup()
        event.accept()

    def confirm_close(self):
        return (self.editor.fieldsAreBlank() or
                askUser(_("Close and lose current input?"), defaultno=True))
