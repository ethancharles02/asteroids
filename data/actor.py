from data import constants
from math import sin, cos, radians
from arcade import Sprite

class Actor(Sprite):
    """A visible, moveable thing that participates in the game. The responsibility of Actor is to keep track of its appearance, position 
    and velocity in 2d space.

    Attributes:
        _velocity (Point): The actor's speed and direction.
    """

    def __init__(self, sprite = "", sprite_scaling = constants.SPRITE_SCALING):
        """The class constructor."""
        super().__init__(sprite, sprite_scaling)

        self._width = self.width
        self.radius = 0
        self._update_radius()
        self._speed = 0
        self.acceleration = 0

    def on_update(self, delta_time: float = 1/60):
        self.angle += self.change_angle * delta_time
        self.update_velocity(delta_time)
        self.position = [self._position[0] + self.change_x * delta_time, self._position[1] + self.change_y * delta_time]

        self.loop_around_screen()
    
    def loop_around_screen(self):
        if self.position[0] - self.radius > constants.SCREEN_WIDTH:
            self.position[0] = 0 - self.radius
        if self.position[0] + self.radius < 0:
            self.position[0] = constants.SCREEN_WIDTH + self.radius

        if self.position[1] - self.radius > constants.SCREEN_HEIGHT:
            self.position[1] = 0 - self.radius
        if self.position[1] + self.radius < 0:
            self.position[1] = constants.SCREEN_HEIGHT + self.radius

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def update_velocity(self, delta_time):
        self.velocity = [self.velocity[0] + self.acceleration * delta_time * cos(radians(self.angle)), self.velocity[1] + self.acceleration * delta_time * sin(radians(self.angle))]

    def set_speed(self, speed):
        self._speed = speed
        self.velocity = [speed * cos(radians(self.angle)), speed * sin(radians(self.angle))]

    def get_speed(self):
        return self._speed

    def _update_radius(self):
        self.radius = self.width if self.width > self.height else self.height

    # Overridden methods
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self._width = new_width
        self._update_radius()
