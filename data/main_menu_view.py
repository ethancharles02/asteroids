"""
The main menu view module holds the GUI for the games main menu.
"""

import arcade
from data import constants
from data.game_view import GameView
from data.game_controller import GameController
from data.move_actors_action import MoveActorsAction
from data.output_service import OutputService
from data.draw_actors_action import DrawActorsAction
from data.button import Button

class MainMenuView(arcade.View):
    """
    The Main Menu View is used to create and display the play button and background of the main menu in the game.
    """
    def __init__(self, window: arcade.Window):
        """
        The class constructor
        """
        super().__init__(window=window)
        self._cast = {}
        self._game_controller = GameController(self._cast, is_main_menu=True)
        self._move_actors_action = MoveActorsAction()

        self._output_service = OutputService()
        self._draw_actors_action = DrawActorsAction(self._output_service)

        self.view_screen = arcade.load_texture(constants.MAIN_MENU)

        self.window = window

    def on_show(self):
        """
        Designs the buttons for the main menu
        """
        self._cast["asteroids"] = arcade.SpriteList()
        self._cast["particles"] = arcade.SpriteList()

        self.play_button = Button(text="PLAY", text_color="black", color=(217, 217, 217), margin_width = 40, margin_height = 20, button_fill=(217, 217, 217), outline="white", edge_thickness=5, selectable=False)
        self.play_button.position = (constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 35)

        self.background = arcade.load_texture("assets/stars.png")

    def on_draw(self):
        """
        Displays the buttons on the main menu
        """
        arcade.start_render()
        
        arcade.draw_lrwh_rectangle_textured(0, 0,
            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
            self.background)

        self.view_screen.draw_scaled(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        self.play_button.draw()
        self._draw_actors_action.execute(self._cast)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed

        Args:
            key: Library used in the constant module
        """
        if key == constants.ESCAPE_KEY:
            self.window.close()


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Determine the active conditions on the constants of the game when a button is selected
        
        Args:
            _x: x axis position of the mouse press
            _y: y axis position of the mouse press
            _button: Conditions created from button press
        """
        
        if _button == 1:
            clicked_asteroids = arcade.get_sprites_at_point((_x, _y), self._cast["asteroids"])
            if clicked_asteroids:
                asteroid_destroyed = clicked_asteroids[0].damage(1, self._cast)
                if asteroid_destroyed != False:
                    self._game_controller._spawned_asteroids -= 1

        if self.play_button.coords_in_hitbox(_x, _y):
            game_view = GameView(self.window, self)
            self.window.show_view(game_view)

    def on_update(self, delta_time: float):
        self._move_actors_action.execute(self._cast, delta_time)
        self._game_controller.execute(delta_time)
        self._cast["particles"].update()