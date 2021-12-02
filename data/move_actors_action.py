from data.action import Action

class MoveActorsAction(Action):
    """A code template for moving actors. The responsibility of this class of
    objects is move any actor that has a velocity more than zero.
    """

    def execute(self, cast, delta_time):
        """Executes the action using the given actors.

        Args:
            cast (dict): The game actors {key: tag, value: list}.
        """
        for group in cast:
            if group != "particles":
                for actor in cast[group]:
                    actor.on_update(delta_time)