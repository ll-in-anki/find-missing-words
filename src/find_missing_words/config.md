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

### `ignored_words`

- Type: `list[string]`
- Description: list of words to ignore, even if you don't have notes for them
- Example: `["I", "me", "the", "you"]`

### `previous_filters`

- Type: `list[dict]`
- Description: List of 
- Example:
    ```json
    [
      {
        "deck": "My French Deck",
        "models": [
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
      }
    ]
    ```

### Note Creation

### `note_creation_presets`

- Type: `list[dict]`
- Description: Preset notes and fields used for creating notes
- Example:
    ```json
    [
      {
        "preset_name": "My Vocab Preset",
        "preset_data": {
          "word_destination": {
            "name": "Cloze",
            "state": false,
            "fields": [
              {
                "name": "Text",
                "state:": true
              }
            ]
          }
        }
      }
    ]
    ```

