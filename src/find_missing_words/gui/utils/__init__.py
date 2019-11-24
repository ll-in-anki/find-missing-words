from . import *

import uuid
import re

token_regex = r"(\b[^\s]+\b)"


def split_words(text):
    return re.split(token_regex, text)


def is_word(text):
    return re.match(token_regex, text)


def clear_layout(layout):
    for i in reversed(range(layout.count())):
        widget = layout.itemAt(i).widget()
        layout.removeWidget(widget)
        widget.deleteLater()


def clear_stacked_widget(stacked_widget):
    for i in reversed(range(stacked_widget.count())):
        widget = stacked_widget.widget(i)
        if widget:
            stacked_widget.removeWidget(widget)
            widget.deleteLater()


def print_object_tree(obj, indent=0):
    print("  " * indent, obj)
    for child in obj.children():
        print_object_tree(child, indent+1)


def generate_uuid():
    """
    Unique id given to each preset for easy addressing
    """
    return str(uuid.uuid4().hex)[-6:]