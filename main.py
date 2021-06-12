import arcade
import Menu
from GlobalConsts import *

def main():
    # Main method.
    window = arcade.Window(screen_w, screen_h, screen_t)
    start_view = Menu.MainView()
    start_view.setup()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()