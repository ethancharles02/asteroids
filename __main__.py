# TODO add firing limit to the player or some way to punish spamming
# TODO fix asteroid counting in the main menu, reset to zero when returned to the main menu
# TODO adjust points gained to be reflective of the size and health of the asteroid

# program entry point
import arcade

# from data.game_view import GameView
from data.main_menu_view import MainMenuView
from data import constants

def main():
    """ Main method """
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    main_menu_view = MainMenuView(window)
    window.show_view(main_menu_view)
    arcade.run()

if __name__ == "__main__":
    main()