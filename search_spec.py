from expects import expect, equal, be
from mamba import description, it, before
from unittest.mock import MagicMock

from tests.test_utils.anki import mock_anki_modules

mock_anki_modules()

from src.find_missing_words.gui.search import Search


test_name = 'test_name'

with description(Search) as self:
    with before.each:

        self.deck = Search(MagicMock())

    with it('should return name without calling initializer'):

        assert isinstance(self.deck, Search)