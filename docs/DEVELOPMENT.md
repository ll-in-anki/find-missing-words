# Find Missing Words - Addon Development

## Installation

1. Clone this repo
1. Install [ll-in-anki's fork of aab](https://github.com/ll-in-anki/anki-addon-builder)
1. Run `aab build` in the clone dir
1. Setup a symlink to the build in Anki addons dir
    - `ln -s <clone dir>/build/dist/find_missing_words/ ~/.local/share/Anki2/addons21/find_missing_words`
    
## Usage

1. For code changes, edit files in src/
1. Run `aab build` in the clone dir
1. Reload addon in Anki (see bottom for reloader link) or restart Anki

### Qt Designer UI Files

UI files are used to speed up visual development and reduce extra code in the business logic.

1. Install Qt Designer
    - `sudo apt install build-essentials qtcreator`
1. Open Qt Designer and start a UI file
    - Not MainWindows, opt for Widgets or Dialogs
1. Save to `designer/` in this repo
    - i.e. `designer/my_component.ui`
1. Create file in `src/find_missing_words/gui`
    - i.e. `src/find_missing_words/gui/my_component.py`
1. Import and setup the ui form in a class
    ```python
    from aqt import mw
   
    from .forms import my_component as my_component_form
   
    # Inherit whichever Qt window you chose in the designer
    # Could be QDialog or QWidget
    class ComponentName(QDialog):
        def __init__(self, parent=None):
            super().__init__()
            self.parent = parent or mw
   
            # Check the compiled UI file's class to call on the next line
            # Could be Ui_Form or Ui_Dialog
            self.form = component_form.Ui_Form()
            self.form.setupUi(self)
    ```
1. Invoke the UI in Anki
    - Not sure of definitive answer yet, but this addon works as follows so far:
        ```python
        # For top-level widgets
        mw.my_top_level_widget = local_widget_var_name = MyWidget()
        local_widget_var_name.show()
        
        # For dialogs called within the addon
        self.exec_()  # at the bottom of  __init__())
        ```
1. Rebuild addon using `aab build` in the project's root

If you want to alter the UI, open up the .ui file in Qt Designer and adjust. The XML inside the .ui file will be what gets updated and committed to git.

## Tips

- Use [our forked addon reloader](https://github.com/ll-in-anki/AnkiAddonReloader) so you don't have to wait for Anki to restart
- Guidelines and help in [the wiki](https://github.com/ll-in-anki/anki-LL/wiki/Qt---Notes-and-Guidelines).
  - Especially useful is PyCharm's 'Attach to Process' so you can use a debugger for the files in `build/dist`
