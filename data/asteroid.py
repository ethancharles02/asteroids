from data.actor import Actor
from data import constants
from random import randint, choice, uniform
from math import floor, ceil
from data.particles import Particle, Smoke
from arcade import draw_rectangle_filled


class Asteroid(Actor):
    def __init__(self, 
    sprite_list = constants.ASTEROID_SPRITE_LIST,
    break_order = [2, 3],
    sprite_scaling = constants.SPRITE_SCALING,
    spin_range = constants.ASTEROID_SPIN_RANGE,
    speed_range = constants.ASTEROID_SPEED_RANGE,
    random_position = True,
    new_position_off_screen = True,
    angle_range = constants.ASTEROID_ANGLE_RANGE,
    size_range = constants.ASTEROID_SIZE_RANGE,
    automate_size = True,
    max_health = None,
    health_colors = constants.ASTEROID_HEALTH_COLOR_CHANGE):

        len_sprite_list = len(sprite_list)
        len_break_order = len(break_order)

        self.sprite_list = sprite_list
        if len_sprite_list - 1 != len_break_order:
            dx = (len_break_order + 1) / len_sprite_list
            self.sprite_list = [*reversed([sprite_list[-(floor(i / dx) + 1)] for i in range(len_break_order + 1)])]

        self.sprite_scaling = sprite_scaling
        self.size_range = size_range

        sprite_size = sprite_scaling * uniform(*size_range)
        size_changes = constants.ASTEROID_SIZE_UNITS
        weighted_break_order = [break_size * size_changes[constants.ASTEROID_SPRITE_LIST.index(self.sprite_list[-(i + 1)])] for i, break_size in enumerate(reversed(break_order))]
        if automate_size and break_order:
            sprite_size *= sum(weighted_break_order) / size_changes[constants.ASTEROID_SPRITE_LIST.index(self.sprite_list[0])]

        super().__init__(self.sprite_list[0], sprite_size)

        self.break_order = break_order
        self.size_range = size_range
        if random_position:
            if new_position_off_screen:
                position_top = choice([True, False])
                if position_top:
                    self.position = (randint(0, constants.SCREEN_WIDTH), choice([0 - self.radius, constants.SCREEN_HEIGHT + self.radius]))
                else:
                    self.position = (choice([0 - self.radius, constants.SCREEN_WIDTH + self.radius]), randint(0, constants.SCREEN_HEIGHT))
            else:
                self.position = (randint(0, constants.SCREEN_WIDTH), randint(0, constants.SCREEN_HEIGHT))


        self.change_angle = randint(*spin_range)
        self.angle = randint(*angle_range)
        self.set_speed(randint(*speed_range))

        if max_health == None:
            max_health = ceil(sum(weighted_break_order) / 2)
            if max_health <= 0:
                max_health = 1
        self.max_health = max_health
        self.cur_health = self.max_health

        self.health_colors = health_colors
        self.health_color_change = [health_colors[1][i] - health_colors[0][i] for i in range(3)]
        self.health_bar_width = self.radius * constants.ASTEROID_HEALTHBAR_WIDTH_FACTOR
    
    def damage(self, damage, cast):
        self.cur_health -= damage
        if self.cur_health <= 0:
            score = self.split(cast)
            return score
        else:
            return False

    def split(self, cast):
        
        if self.break_order:
            if len(self.sprite_list) == 1:
                self.sprite_list.append(self.sprite_list[0])

            for _ in range(self.break_order[0]):
                cast["asteroids"].append(Asteroid(
                    sprite_list = self.sprite_list[1:],
                    break_order = self.break_order[1:],
                    random_position = False,
                    sprite_scaling=self.sprite_scaling,
                    size_range=self.size_range
                ))
                cast["asteroids"][-1].position = self.position

        add_explosion(cast["particles"], self.position)
        cast["asteroids"].remove(self)
        return self._get_size_value()
    
    def _get_size_value(self):
        size_changes = constants.ASTEROID_SIZE_UNITS
        
        return size_changes[constants.ASTEROID_SPRITE_LIST.index(self.sprite_list[0])]
    
    def _draw_health_bar(self):
        """ Draw the health bar """

        health_percent = self.cur_health / self.max_health
        if health_percent >= 0:
            health_width = self.health_bar_width * health_percent
            color = [self.health_color_change[i] * (1 - health_percent) + self.health_colors[0][i] for i in range(3)]

            draw_rectangle_filled(center_x=self.center_x,
                                            center_y=self.center_y + constants.ASTEROID_HEALTHBAR_OFFSET_Y,
                                            width=health_width,
                                            height=3,
                                            color=color)

    def draw(self):
        super().draw()
        self._draw_health_bar()

def add_explosion(explosions_list, position):
    """
    Adds an explosion to the given list, this pulls from both Particle and Smoke to create it
    """
    for _ in range(constants.PARTICLE_COUNT):
        particle = Particle(explosions_list)
        particle.position = position
        explosions_list.append(particle)

    smoke = Smoke(50)
    smoke.position = position
    explosions_list.append(smoke)