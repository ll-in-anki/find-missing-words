from aqt.qt import *
from anki.hooks import addHook, remHook
from anki.lang import _


class FieldChooser(QHBoxLayout):
    """
    Mirrors aqt.modelchooser.ModelChooser, except for a model's fields
    """

    def __init__(self, mw, widget, label=True):
        QHBoxLayout.__init__(self)
        self.widget = widget
        self.mw = mw
        self.label = label
        self.setup_fields_button()
        self.update_fields()
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(8)
        addHook("reset", self.on_reset)
        addHook("currentModelChanged", self.update_fields)
        self.widget.setLayout(self)

    def setup_fields_button(self):
        if self.label:
            self.field_label = QLabel(_("Field"))
            self.addWidget(self.field_label)
        self.fields = QPushButton()
        self.fields.setAutoDefault(False)
        self.addWidget(self.fields)
        self.fields.clicked.connect(self.on_field_change)
        # layout
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy(7),
            QSizePolicy.Policy(0))
        self.fields.setSizePolicy(sizePolicy)

    def cleanup(self):
        remHook("reset", self.on_reset)
        remHook("currentModelChanged", self.update_fields)

    def on_reset(self):
        self.update_fields_button()

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def update_fields(self):
        """
        If model changes via modelchooser, reflect appropriate fields in field chooser/button
        """
        current_model = self.mw.col.models.current()
        self.field_names = [field["name"] for field in current_model["flds"]]
        self.current_field_name = self.field_names[0]
        self.update_fields_button()

    def on_field_change(self):
        from aqt.studydeck import StudyDeck
        placeholder = QPushButton(_("N/A"))
        # Button created and disabled so that default "Add new deck" button isn't created by StudyDeck
        placeholder.setEnabled(False)
        def nameFunc():
            return sorted(self.field_names)
        returned_field = StudyDeck(
            self.mw, names=nameFunc,
            accept=_("Choose"), title=_("Choose Field"),
            current=self.current_field_name, parent=self.widget,
            buttons=[placeholder], cancel=True, geomKey="selectField")
        if not returned_field.name:
            return
        self.current_field_name = returned_field.name
        self.update_fields_button()
        self.mw.reset()

    def update_fields_button(self):
        self.fields.setText(self.current_field_name)
