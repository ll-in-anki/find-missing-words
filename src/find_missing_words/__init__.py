def initialize_addon():

    from .gui.options import initialize_menu_item
    initialize_menu_item()


if __name__ == "__main__":
    initialize_addon()
