import arcade
from data.action import Action

class ControlActorsAction(Action):
    """A code template for controlling actors. The responsibility of this
    class of objects is translate user input into some kind of intent.

    Attributes:
        _input_service (InputService): An instance of InputService.
    """

    def __init__(self):
        """The class constructor.
        
        Args:
            input_service (InputService): An instance of InputService.
        """
        pass

    def execute(self, window, main_menu, cast: dict, held_keys: set, key = "", key_type=0, lock_controls=False):
        """Executes the action using the given actors.

        Args:
            window
            
            main_menu
            
            cast (dict): The game actors {key: tag, value: list}.
            
            held_keys: The keys that are currently held down
            
            key: The key that was just pressed
            
            key_type (int): If the key is down or up
            
            lock_controls (bool): Locks the player controls or not
        """
        if arcade.key.ESCAPE in held_keys:
            window.show_view(main_menu)
        if "players" in cast:
            if not lock_controls:
                for player in cast["players"]:
                    player.key_input(held_keys, key, key_type)
            else:
                for player in cast["players"]:
                    player.key_input(set())