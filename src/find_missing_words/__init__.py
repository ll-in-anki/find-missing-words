def addon_reloader_after():
    """
    Add hook for AnkiAddonReloader to auto-show the addon after reloading to save clicks
    """
    from .gui.options import invoke_addon_window
    invoke_addon_window()


def initialize_addon():
    from .gui.options import initialize_menu_item
    initialize_menu_item()


initialize_addon()
