from data.action import Action
from data.asteroid import Asteroid
from data import constants

from random import randint, choice
from math import floor

class GameController(Action):
    def __init__(self, cast, level=0, scaling=constants.LEVEL_SCALING, is_main_menu=False):
        self.is_main_menu = is_main_menu
        if is_main_menu:
            self._cast = cast

            self._cur_asteroid_spawn_delay = 2
            self._cur_total_asteroids = 10

            self._spawned_asteroids = 0
            self._time_since_spawn = 0
        else:
            self.level = level
            self.scaling = scaling
            self._cast = cast

            self._asteroid_spawn_delay = 2
            self._total_asteroids = 10

            self._cur_asteroid_spawn_delay = self._asteroid_spawn_delay
            self._cur_total_asteroids = self._total_asteroids

            self._spawned_asteroids = 0
            self._time_since_spawn = 0
    
    def execute(self, delta_time):
        if self.is_main_menu:
            self._time_since_spawn += delta_time
            
            if self._time_since_spawn > self._cur_asteroid_spawn_delay and self._spawned_asteroids < self._cur_total_asteroids:
                self._time_since_spawn = 0
                self._spawn_asteroid()
                self._spawned_asteroids += 1
        else:
            if not self._cast["asteroids"] and self._spawned_asteroids >= self._cur_total_asteroids:

                self._next_level()
                self._cast["players"][0].queue_lasers_death()
                self._spawn_asteroid()

                self._time_since_spawn = 0
                self._spawned_asteroids = 0
                return True
            
            self._time_since_spawn += delta_time

            if self._time_since_spawn > self._cur_asteroid_spawn_delay and self._spawned_asteroids < self._cur_total_asteroids:
                self._time_since_spawn = 0
                self._spawn_asteroid()
                self._spawned_asteroids += 1
                
        return False
    
    def _next_level(self):
        self.level += 1

        self._cur_asteroid_spawn_delay = self._asteroid_spawn_delay / (1 + self.scaling * self.level)
        self._cur_total_asteroids = floor(self._total_asteroids * (1 + self.scaling * self.level))
    
    def _spawn_asteroid(self):
        if self.is_main_menu:
            break_orders = ([3, 2], [2], [])
            self._cast["asteroids"].append(Asteroid(sprite_list = constants.ASTEROID_SPRITE_LIST, break_order=choice(break_orders)))
        else:
            break_order = [randint(2, floor(4 * (1 + (self.scaling) * self.level))) for i in range(randint(0, floor(1 * (1 + self.scaling * self.level))))]
            self._cast["asteroids"].append(Asteroid(sprite_list = constants.ASTEROID_SPRITE_LIST, break_order=break_order))