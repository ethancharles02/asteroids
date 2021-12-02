from data.action import Action
from data.asteroid import add_explosion

class HandleCollisionsAction(Action):
    """A code template for handling collisions. The responsibility of this class of objects is to update the game state when actors collide.
    """

    def execute(self, game, cast):
        """Executes the action using the given actors.

        Args:
            game

            cast (dict): The game actors {key: tag, value: list}.
        """
        players = cast["players"]

        for player in players:
            collision_list = player.collides_with_list(cast["asteroids"])
            if collision_list:
                add_explosion(cast["particles"], player.position)
                cast["players"].remove(player)

        for asteroid in cast["asteroids"]:
            for player in players:
                collision_list = asteroid.collides_with_list(player.laser_list)
                if collision_list:
                    laser = collision_list[0]

                    score = cast["asteroids"][cast["asteroids"].index(asteroid)].damage(laser.damage, cast)
                    player.laser_list.remove(laser)

                    if score != False:
                        player.score += score
                    break