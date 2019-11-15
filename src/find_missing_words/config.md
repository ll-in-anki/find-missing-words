# Find Missing Words - Config

## Search

### `default_deck`

- Type: `string`
- Description: Deck name to search through by default on searches
- Example: `"My French Deck"`

### `default_notes_and_fields`

- Type: `list[dict]`
- Description: list of notes/models and their fields to search on by default
  - Notes must be populated with at least one field
- Example:
    ```json
    [
      {
        "name": "Cloze", 
        "state": 1, 
        "fields": [
          {
            "name": "Text", 
            "state": 2
          }
        ]
      }
    ]
    ```

### `ignored_words` (coming soon)

- Type: `list[string]`
- Description: list of words to ignore, even if you don't have notes for them
- Example: `["I", "me", "the", "you"]`

### Note Creation

### `note_creation_presets`

- Type: `dict`
- Description: Preset notes and fields used for creating notes, indexed by uuid
- Example:
    ```json
    {
      "3d0c26": {
        "preset_id": "3d0c26",
        "preset_name": "My Vocab Preset",
        "preset_data": {
          "note_type": "Cloze",
          "word_destination": "Text",
          "sentences_allowed": true,
          "sentence_presets": {
              "2t2jvs": {
                  "sentence_preset_id": "2t2jvs",
                  "sentence_destination": "The full sentence (no words blanked out)",
                  "sentence_type": "WHOLE"
              },
              "f34ojn": {
                  "sentence_preset_id": "f34ojn",
                  "sentence_destination": "Cloze (Front)",
                  "sentence_type": "CLOZE_REPEAT"
              },
              "32kjgn": {
                  "sentence_preset_id": "32kjgn",
                  "sentence_destination": "Front (Example with word blanked out or missing)",
                  "sentence_type": "BLANK"
              },
              "2kjsgj": {
                  "sentence_preset_id": "2kjsgj",
                  "sentence_destination": "Another front field",
                  "sentence_type": "MISSING"
              }
          }
      }
    }
    ```

