import enum


class ConfigProperties(enum.Enum):
    FILTER_DECK = "filter_on_deck"
    FILTER_NOTE_FIELDS = "filter_on_note_fields"
    DECK = "default_deck"
    NOTE_FIELDS = "default_notes_and_fields"
    IGNORED_WORDS = "ignored_words"
    PREVIOUS_FILTERS = "previous_filters"
    NOTE_CREATION_PRESETS = "note_creation_presets"


class SentenceTypes(enum.Enum):
    WHOLE = "Whole sentence"
    BLANK = "Word blanked out"
    MISSING = "Word removed"
    CLOZE_REPEAT = "Word clozed (reuse cloze for all occurrences)"
    CLOZE_SEPARATE = "Word clozed (separate cloze for each occurrence)"
