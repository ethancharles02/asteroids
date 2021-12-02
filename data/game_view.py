import arcade

from data import constants

from data.control_actors_action import ControlActorsAction
from data.draw_actors_action import DrawActorsAction
from data.handle_collisions_action import HandleCollisionsAction
from data.move_actors_action import MoveActorsAction
from data.output_service import OutputService
from data.game_controller import GameController
from data.button import Button

from data.player import Player


class GameView(arcade.View):
    """
    The game is in charge of bringing everything together and putting it into the arcade window

    Attributes:
        window
        main_menu
    """

    def __init__(self, window: arcade.Window, main_menu):
        """
        The class constructor
        """
        super().__init__(window=window)
        
        self.window = window
        self.main_menu = main_menu

        self._cast = {}
        self._output_service = OutputService()
        self._draw_actors_action = DrawActorsAction(self._output_service)

        self._control_actors_action = ControlActorsAction()

        self._move_actors_action = MoveActorsAction()

        self._handle_collisions_action = HandleCollisionsAction()

        self._game_controller = GameController(self._cast, 0, constants.LEVEL_SCALING)

        self.background = None

        self.held_keys = set()

        self.total_time = 0

        self.game_over = False
        self.show_upgrade_screen = False

    def on_show(self):
        """
        Set up the game and initialize the variables.
        """
        
        self._cast["players"] = []
        self._cast["players"].append(Player("assets/playerShip1_orange.png", constants.SPRITE_SCALING))
        self._cast["players"][0].position = (constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

        self._cast["asteroids"] = arcade.SpriteList()
        self._cast["particles"] = arcade.SpriteList()


        self.upgrade_screen = arcade.load_texture(constants.UPGRADE_SCREEN)
        self.upgrades = [
            "ship_turn_speed",
            "ship_acceleration",
            "laser_speed",
            "laser_upgrade"
        ]

        button_dy = -70
        self.text_dy = button_dy
        button_x_off = 100
        button_y_off = 150
        self.text_level_x_off = -150
        self.text_x_off = -40
        self.text_y_off = button_y_off

        continue_button_dy = -50
        continue_button_y_off = -25

        self.buttons = arcade.SpriteList(is_static=True)
        for i, _ in enumerate(self.upgrades, 1):
            self.buttons.append(Button(font_size=20, text="Upgrade", text_color="black", color=(217, 217, 217), margin_width = 40, margin_height = 20, button_fill=(217, 217, 217), outline="white", edge_thickness=5, selectable=False))
            self.buttons[-1].position = (constants.SCREEN_WIDTH / 2 + button_x_off, constants.SCREEN_HEIGHT / 2 + button_dy * i + button_y_off)
        
        self.continue_button = Button(font_size=20, text="Continue", text_color="black", color=(217, 217, 217), margin_width = 40, margin_height = 20, button_fill=(217, 217, 217), outline="white", edge_thickness=5, selectable=False)
        self.continue_button.position = (constants.SCREEN_WIDTH / 2 + button_x_off, constants.SCREEN_HEIGHT / 2 + continue_button_dy * (len(self.buttons) + 1) + continue_button_y_off)

        self.background = arcade.load_texture("assets/stars.png")
        
        

    def on_draw(self):
        """
        Render the screen.
        """
        
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0,
            constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT,
            self.background)

        self._draw_actors_action.execute(self._cast)

        output = f"Level: {self._game_controller.level + 1}"
        arcade.draw_text(output, 0, 17, arcade.color.WHITE, 15)

        if self._cast["players"]:
            output = f"Score: {self._cast['players'][0].score}"
            arcade.draw_text(output, 0, 0, arcade.color.WHITE, 15)
        
        if self.game_over:
            arcade.draw_text("Game Over!", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 + 25,
                arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_text("Click: Restart", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 25,
                arcade.color.WHITE, font_size=15, anchor_x="center")
            arcade.draw_text("ESC: Return to Menu", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 40,
                arcade.color.WHITE, font_size=15, anchor_x="center")
        elif self.show_upgrade_screen:
            self.upgrade_screen.draw_scaled(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)

            for i, upgrade in enumerate(self.upgrades, 1):
                arcade.draw_text(f'Level: {self._cast["players"][0].upgrades[upgrade][0]}', constants.SCREEN_WIDTH / 2 + self.text_level_x_off, constants.SCREEN_HEIGHT / 2 + self.text_dy * i - 8 + self.text_y_off,
                arcade.color.BLACK, font_size=15, anchor_x="center")

                arcade.draw_text(" ".join(upgrade.split("_")).capitalize(), constants.SCREEN_WIDTH / 2 + self.text_x_off, constants.SCREEN_HEIGHT / 2 + self.text_dy * i + self.text_y_off,
                arcade.color.BLACK, font_size=15, anchor_x="center")

                arcade.draw_text(f'Cost: {self._cast["players"][0].upgrades[upgrade][1]} Points', constants.SCREEN_WIDTH / 2 + self.text_x_off, constants.SCREEN_HEIGHT / 2 + self.text_dy * i - 17 + self.text_y_off,
                arcade.color.BLACK, font_size=15, anchor_x="center")

            self.buttons.draw()
            self.continue_button.draw()


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        """
        # if key == arcade.key.UP:
        #     self._game_controller._next_level()
        self.held_keys.add(key)
        self._control_actors_action.execute(self.window, self.main_menu, self._cast, self.held_keys, key, 0, lock_controls=self.game_over or self.show_upgrade_screen)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
        self._control_actors_action.execute(self.window, self.main_menu, self._cast, self.held_keys, key, 1, lock_controls=self.game_over or self.show_upgrade_screen)
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """
        Called whenever a mouse key is pressed
        """
        if self.game_over:
            self.window.show_view(GameView(self.window, self.main_menu))
        
        elif self.show_upgrade_screen:
            for button in self.buttons:
                if button.coords_in_hitbox(_x, _y):
                    upgrade = self.upgrades[self.buttons.index(button)]
                    if self._cast["players"][0].score >= self._cast["players"][0].upgrades[upgrade][1]:
                        self._cast["players"][0].score -= self._cast["players"][0].upgrades[upgrade][1]
                        self._cast["players"][0].upgrade(upgrade)
                    return
            if self.continue_button.coords_in_hitbox(_x, _y):
                self.show_upgrade_screen = False

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        self.total_time += delta_time

        if not self._cast["players"]:
            self.game_over = True
        if self._game_controller.execute(delta_time):
            self.show_upgrade_screen = True
        
        if not self.show_upgrade_screen:
            self._move_actors_action.execute(self._cast, delta_time)
            self._handle_collisions_action.execute(self, self._cast)

        self._cast["particles"].update()