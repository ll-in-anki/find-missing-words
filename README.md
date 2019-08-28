# anki-LL

An Anki add-on for language learning.

## Development

- Helps to create a symlink to the anki plugin folder so you only have to edit one set of files
    - (As admin) `mklink /d <path to folder in anki addons> <path to actual addon/cloned folder>`
        - i.e. `mklink /d "%APPDATA%\Roaming\Anki2\addons21\anki-LL" "<path to this folder>"`
        - `ln -s ...` on Linux/Mac
- Run anki from the command line to view debug info easily
    - `anki-console.exe`
- Use [our forked addon reloader](https://github.com/ll-in-anki/AnkiAddonReloader) so you don't have to wait for Anki to restart
- Guidelines and help in [the wiki](https://github.com/ll-in-anki/anki-LL/wiki/Qt---Notes-and-Guidelines).
