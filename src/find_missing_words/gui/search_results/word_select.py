"""
Module for the word select pane displayed on the left side of the search results window.
Displays the text from the search window and highlights the words not found in the search query.
"""

from aqt.qt import *
from anki.hooks import runHook

from .. import utils


class WordSelect(QTextBrowser):
    STYLE = """
    body {
        line-height: 1.5;
    }
    a {
        color: black;
        text-decoration: none !important;
    }
    .unknown {
        background: lightgreen;
    }
    """

    def __init__(self, text, word_model, parent=None):
        super().__init__(parent)
        self.text = text
        self.word_model = word_model
        self.build()
        self.setOpenLinks(False)
        self.anchorClicked.connect(self.intercept_click)

    def build(self):
        self.html = self.build_html()
        self.setText(self.html)

    def build_html(self):
        html = "<html><head><style type='text/css'>" + WordSelect.STYLE + "</style></head><body>"
        tokens = utils.split_words(self.text)
        for token in tokens:
            if not utils.is_word(token):
                # Not a word, don't allow clicking
                html += token
                continue
            known = self.word_model[token]["known"]
            if known:
                html += f"<a href='{token}'>{token}</a>"
            else:
                html += f"<a class='unknown' href='{token}'>{token}</a>"
        html += "</body></html>"
        return html

    def set_word_model(self, word_model):
        self.word_model = word_model

    def intercept_click(self, link):
        word = link.toString()
        note_ids = self.word_model[word]["note_ids"]
        known = self.word_model[word]["known"]
        runHook("load_word", word, note_ids, known)

    def ignore_word(self, word):
        for token in self.word_model:
            if token.lower() == word.lower():
                self.word_model[token]["known"] = True
        self.build()
