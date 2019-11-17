# Find Missing Words in Anki

An Anki add-on for searching through your collection to find gaps in your vocabulary and quickly create notes to fill in those gaps.

This is a similar flow to LingQ or ReadLang. But instead of starting your vocab from scratch, it uses your existing Anki collection to find which words you don't know.

## Demo

![Video demo](https://raw.githubusercontent.com/ll-in-anki/find-missing-words/master/demo.gif)

## Installation

See [AnkiWeb](https://ankiweb.net/shared/info/754868802) for quick install instructions.

Addon code: **754868802**

## Usage

### Search

![](https://i.imgur.com/dPQW4wc.png)

1. Open the "Find Missing Words" addon from the Anki Tools menu
1. Optionally filter your search
    - By deck and/or by models and their fields
    - Check the box next to the filter to enable it, disable to leave search open
    - This filter will determine if the words in the text are considered 'known' or 'missing.'
    - **Note:** including the fields in the search is much more accurate than leaving it blank (all fields).
1. Enter text into the text area
1. Click "Search"

---

Example of model/field filter. I usually add words to these two note types/fields:

![](https://i.imgur.com/KDPYhLp.png)

Search with populated info:

![](https://i.imgur.com/b4JCuvZ.png)

### Word Select

![](https://i.imgur.com/ThY9QJ2.png)
    
Upon search, you are presented with a window that shows the text, with words not found in your query colored green.

#### Known Words

These will not be colored green, but can be clicked on to view the current notes that contain the word.

1. Click on word in left pane
1. In right pane, view the list of notes that contain the word
    - Note: these will only be notes that contain the word _and_ fall within the filter parameters.
1. Click on a note entry in the list
1. Use the editor to make any adjustments, if necessary

#### New Words

1. Click on a green word bubble that holds a new word
    ![](https://i.imgur.com/8lLGJ02.png)
1. In the right pane, notice there are two options
    1. Ignore the word (marks the word as known, removes green highlighting)
    2. Create a note based on a note preset

##### Ignoring

Ignoring a word is handy when you are just starting to use the addon and many little, insignificant words (articles, stop words, proper nouns, words you know by heart) are shown in green. You don't need cards for them, so you can ignore them and they will cease to show up as green from now on.

##### Create Note from Note Preset

Now for the fun part: actually creating notes for missing words.

When you first start out, you won't have any **note creation presets**. A note creation preset is a mapping that tells the extension what you'd like to do with a new word. This includes the location (deck and model/field) as well as the surrounding sentences for context (more on that later).

To create a preset:

1. Click the plus ('+') button
    - This brings up the config (more on that later, too)
    ![](https://i.imgur.com/LYSk5dT.png)
1. On the "Note Creation" tab of the config, click on "Add" at the bottom of the list pane
    ![](https://i.imgur.com/ipm1Ze2.png)
1. Choose a name for your preset
    - E.g. "Fill in the Blank," "New Word Form," "Word Order"
1. Choose a destination for the word 
    1. Note type (the model, e.g. "Basic")
    2. Word destination Field (e.g. "Front")
1. Optionally use the surrounding sentence(s) for context
1. Save, you will be taken back to the Note Creation view
1. Click on the new Note Creation Preset button (e.g. "Fill in the Blank")
    ![](https://i.imgur.com/vkdiUUq.png)
1. View the pre-populated fields, fill in any extra info for your note
    ![](https://i.imgur.com/XdfBXbv.png)

Upon adding a note, the word that was selected (and any duplicates) will be marked as "known" and cease to be highlighted in the word selection view.

![](https://i.imgur.com/eGgdbVc.png)

Clicking on the same word again will bring up the (new) note(s) associated with it. The regular note editor will be used instead of the "Add Note Editor" (notice not "Add" or "Cancel" buttons at the bottom).

![](https://i.imgur.com/1MUVoiS.png)

###### Sentences

For a note creation preset, you can include the surrounding sentences for helpful context.

To add sentences:

1. Enable the sentence box by checking the box next to "Sentences"
1. Pick a field (based on the "Note Type" model fields from above)
1. Pick a sentence configuration type
    1. Whole sentence
    1. Word blanked out (word -> "__")
    1. Word removed (word -> "")
    1. Word clozed (reuse cloze for all occurrences)
        - "{{c1::word}} ... {{c1::Word}} ... {{c1:: word}}"
        - All word occurrences revealed on card flip
    1. Word clozed (separate cloze for each occurrence)
        - "{{c1::word}} ... {{c2::Word}} ... {{c3:: word}}"
        - Helpful for creating multiple cards
1. Optionally add more sentence configurations
    - E.g. one for whole sentence in the "whole sentence" field and another for a "sentence with word blanked out" field
    ![](https://i.imgur.com/KO8Vpo1.png)

### Config

The config has two parts:
    1. Search configuration
    2. Note creation presets
    
We've just discussed #2 above, so here's some info on search configuration:

#### Search Configuration

![](https://i.imgur.com/6mly1qu.png)

This tab of the config lets you set defaults to save time by not having to re-enter the search filters. 

##### Filters

Here, you can set a default deck and note/field combination for future searches. The steps are the same as the above Search section. If you use the same deck and fields for your words in Anki, these are for you.


##### Ignored Words

In this text box, you can enter the words you don't want showing up as 'new' in the word select step.

The words are separated by new lines; and common punctuation is ignored by default. When you ignore words in the Word Select view, they will save to your config and be sorted for you to see here.

**Before and after ignoring a word**:

Clicking "Ignore" in the top right in the Note Creation pane:

![](https://i.imgur.com/JrmgkZP.png)

Seeing the word ignored in the config:

![](https://i.imgur.com/873jwLL.png)

### Saving and Cancelling

Clicking "Cancel" will revert the config to the state/preferences it had when you opened it.
Clicking "Save All" will save any changes on both tabs that were made since opening the config.

## Contributing

- See docs/DEVELOPMENT.md for setup
    - See other files in docs/ for understanding some of the data structures
- Fill out issues and PRs accordingly
    - For issues, make sure to include stack trace(s)

---

Enjoy!
