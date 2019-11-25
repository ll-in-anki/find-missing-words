
# print(f"Name is: '{__name__}'")
if __name__ != "src.find_missing_words":

    def addon_reloader_before():
        """
        Remove any instance(s) of the addon in the Anki Tools menu to prevent duplicates
        """
        from .gui.options import cleanup_menu_items
        cleanup_menu_items()


    def addon_reloader_after():
        """
        Add hook for AnkiAddonReloader to auto-show the addon after reloading to save clicks
        """
        from .gui.options import invoke_addon_window
        invoke_addon_window()


    def initialize_addon():
        from .gui.options import initialize_menu_item, initialize_config_menu_item
        initialize_menu_item()
        initialize_config_menu_item()


    initialize_addon()
