from aqt.qt import *


class NoteFieldChooser(QHBoxLayout):
    """
    Button to invoke note and field tree, whose text displays current tree selection
    Influenced by aqt.deckchooser.DeckChooser
    """
    def __init__(self, mw, widget, single_selection_mode=False):
        QHBoxLayout.__init__(self)
        self.widget = widget
        self.single_selection_mode = single_selection_mode
        self.mw = mw
        self.note_field_items = []
        self.selected_items = []
        self.btn_text = "None"

        self.setContentsMargins(0,0,0,0)
        self.setup_note_field_data()
        self.setup_btn()
        self.widget.setLayout(self)

    def setup_note_field_data(self):
        all_note_types = self.mw.col.models.all()
        self.note_field_items = []
        for note_type in all_note_types:
            note_dict = {"name": note_type["name"], "state": Qt.Unchecked}
            note_fields = []
            for field in note_type["flds"]:
                field_dict = {"name": field["name"], "state": Qt.Unchecked}
                note_fields.append(field_dict)
            note_dict["fields"] = note_fields
            self.note_field_items.append(note_dict)

    def setup_btn(self):
        self.btn = QPushButton()
        if self.btn_text:
            self.btn.setText(self.btn_text)
        self.btn.clicked.connect(self.invoke_note_field_tree)
        self.btn.setAutoDefault(False)
        self.addWidget(self.btn)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def invoke_note_field_tree(self):
        from .note_field_tree import NoteFieldTree
        ret = NoteFieldTree(self.note_field_items, self.single_selection_mode, self.widget)
        if ret.selected_items:
            self.note_field_items = ret.all_items
            self.update_value(ret.selected_items)

    def update_value(self, selected_items):
        formatted_selected_items = self.format_btn_text(selected_items)
        if len(formatted_selected_items) > 15:
            self.btn_text = formatted_selected_items[:15] + '...'
        else:
            self.btn_text = formatted_selected_items
        self.btn.setText(self.btn_text)
        self.btn.setToolTip(formatted_selected_items)
        self.selected_items = selected_items

    @staticmethod
    def format_btn_text(items):
        note_field_list = []
        for note in items:
            name = note["name"]
            fields = ', '.join([field["name"] for field in note["fields"]])
            result = name + '(' + fields + ')'
            note_field_list.append(result)
        return ', '.join(note_field_list)
