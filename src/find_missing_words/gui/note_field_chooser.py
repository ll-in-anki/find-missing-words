from aqt.qt import *


class NoteFieldChooser(QHBoxLayout):
    """
    Button to invoke note and field tree, whose text displays current tree selection.
    The chooser is an interface to the note_field_tree.py and handles the data before and after choosing from the tree.
    Influenced by aqt.deckchooser.DeckChooser.
    """
    def __init__(self, mw, widget, on_update_callback=None, single_selection_mode=False):
        QHBoxLayout.__init__(self)
        self.mw = mw
        self.widget = widget
        self.on_update_callback = on_update_callback
        self.single_selection_mode = single_selection_mode
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

    def set_selected_items(self, selected_note_field_items):
        for note in self.note_field_items:
            note_name = note["name"]
            fields = note["fields"]
            for new_note in selected_note_field_items:
                if note_name == new_note["name"]:
                    note["state"] = new_note["state"]
                    new_note_fields = new_note["fields"]
                    for field in fields:
                        for new_field in new_note_fields:
                            if field["name"] == new_field["name"]:
                                field["state"] = new_field["state"]
        self.update_value(selected_note_field_items)

    def set_single_selected_item(self, note_field_item):
        note_name = note_field_item["name"]
        field_name = note_field_item["fields"]
        for note in self.note_field_items:
            if note_name == note["name"]:
                for field in note["fields"]:
                    if field_name == field["name"]:
                        field["state"] = True
        self.update_value(note_field_item)

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
        if self.on_update_callback:
            self.on_update_callback()

    def format_btn_text(self, items):
        if self.single_selection_mode:
            items = [items]
        note_field_list = []
        for note in items:
            name = note["name"]
            fields = ', '.join([field["name"] for field in note["fields"]])
            result = name + '(' + fields + ')'
            note_field_list.append(result)
        return ', '.join(note_field_list)
