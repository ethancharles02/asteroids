"""
The particles module holds the classes for creating the explosions
"""
import random
import math
import arcade
from data import constants

class Particle(arcade.SpriteCircle):
    """
    The Particle class creates circles with random speeds and colors (based on a color list)

    Methods: 
        __init__(): initializes the parent class, assigns attributes
        update(): overridden method that updates the position based on velocity (and has a chance of creating additional particles)
    """
    def __init__(self, my_list):
        """
        The class constructor

        Args:
            my_list (list): holds the particles
        """
        color = random.choice(constants.PARTICLE_COLORS)

        super().__init__(constants.PARTICLE_RADIUS, color)

        self.normal_texture = self.texture

        self.my_list = my_list

        speed = random.random() * constants.PARTICLE_SPEED_RANGE + constants.PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

        self.my_alpha = 255

        self.my_list = my_list

    def update(self):
        """
        Updates the particle
        """
        if self.my_alpha <= constants.PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            self.my_alpha -= constants.PARTICLE_FADE_RATE
            self.alpha = self.my_alpha
            self.center_x += self.change_x
            self.center_y += self.change_y
            self.change_y -= constants.PARTICLE_GRAVITY

            if random.random() <= constants.PARTICLE_SPARKLE_CHANCE:
                self.alpha = 255
                self.texture = arcade.make_circle_texture(self.width, arcade.color.WHITE)
            else:
                self.texture = self.normal_texture

            if random.random() <= constants.SMOKE_CHANCE:
                smoke = Smoke(5)
                smoke.position = self.position
                self.my_list.append(smoke)

class Smoke(arcade.SpriteCircle):
    """
    The Smoke class holds information for the smoke particles that are created in explosions

    Methods: 
        __init__(): initializes the parent class, assigns attributes
        update(): overridden method that updates the position based on velocity
    """
    def __init__(self, size):
        """
        The class constructor

        Args:
            size (float): sets the size of the smoke particle
        """
        super().__init__(size, arcade.color.LIGHT_GRAY, soft=True)
        self.change_y = constants.SMOKE_RISE_RATE
        self.scale = constants.SMOKE_START_SCALE

    def update(self):
        """
        Updates the particle
        """
        if self.alpha <= constants.PARTICLE_FADE_RATE:
            self.remove_from_sprite_lists()
        else:
            if self.alpha - constants.SMOKE_FADE_RATE < 0:
                self.alpha = 0
            else:
                self.alpha -= constants.SMOKE_FADE_RATE

            self.center_x += self.change_x
            self.center_y += self.change_y
            self.scale += constants.SMOKE_EXPANSION_RATE