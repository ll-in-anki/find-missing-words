# anki-LL

An Anki add-on for language learning.

## Developing

- Helps to create a symlink to the anki plugin folder so you only have to edit one set of files
    - (As admin) `mklink /d <path to folder in anki addons> <path to actual addon/cloned folder>`
        - i.e. `mklink /d "%APPDATA%\Roaming\Anki2\addons21\anki-LL" "<path to this folder>"`
- Run anki from the command line to view debug info easily
    - `anki-console.exe`