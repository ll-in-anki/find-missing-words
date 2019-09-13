# Find Missing Words - Addon Development

## Steps

1. Clone this repo
1. Install [ll-in-anki's fork of aab](https://github.com/ll-in-anki/anki-addon-builder)
1. Run `aab build` the clone destination
1. Setup a symlink to the build
    - `ln -s <clone dir>/build/dist/find_missing_words/ find_missing_words`
1. Edit files in src, run `aab build` on the clone dir on change

## Tips

- Use [our forked addon reloader](https://github.com/ll-in-anki/AnkiAddonReloader) so you don't have to wait for Anki to restart
- Guidelines and help in [the wiki](https://github.com/ll-in-anki/anki-LL/wiki/Qt---Notes-and-Guidelines).
  - Especially useful is PyCharm's 'Attach to Process' so you can use a debugger for the files in `build/dist`
