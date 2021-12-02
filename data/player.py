from data.actor import Actor
from data import constants
from data.laser import Laser

from arcade import SpriteList
from math import floor

class Player(Actor):
    """
    The player class holds all data on the ship they control and their upgrades.
    It also holds data on their lasers they have shot

    Methods:
        __init__():
        key_input():
        set_name(name):
    """
    
    def __init__(self, 
        sprite = "", 
        sprite_scaling = constants.SPRITE_SCALING, 
        keys : dict = constants.DEFAULT_KEYS,
        laser_sprite = "assets/laserBlue01.png"):
        """
        Class constructor, initializes private attributes for name and guess
        """
        super().__init__(sprite, sprite_scaling)

        self.keys = keys
        self.keys_set = set(keys.keys())
        
        # Deprecated value, may add later in a new update
        # self.health = 0
        self.score = 0
        self.upgrades = {
            "ship_turn_speed": [1, 20],
            "ship_acceleration": [1, 20],
            "laser_speed": [1, 20],
            "laser_upgrade": [1, 20]
        }

        self.laser_sprite = laser_sprite
        self.laser_list = SpriteList()

        self.orig_laser_bonus_count = constants.DEFAULT_BONUS_LASER_COUNT
        self.laser_bonus_count = self.orig_laser_bonus_count
        self.orig_laser_damage = constants.LASER_DAMAGE
        self.laser_max_angle = constants.LASER_MAX_ANGLE
        self.laser_damage = self.orig_laser_damage
        self.laser_speed_factor = 1 + (constants.LASER_SPEED_SCALING * (self.upgrades["laser_speed"][0] - 1))

        self.orig_acceleration_rate = constants.PLAYER_ACCELERATION_RATE
        self.orig_turn_speed = constants.PLAYER_TURN_SPEED
        self.acceleration_rate = constants.PLAYER_ACCELERATION_RATE
        self.turn_speed = constants.PLAYER_TURN_SPEED
        
    
    def key_input(self, held_keys : set, key="", key_type=0):
        command_list = [self.keys[key] for key in self.keys_set.intersection(held_keys)]
        key_command = ""
        if key in self.keys:
            key_command = self.keys[key]
        if "up" in command_list:
            self.set_acceleration(self.acceleration_rate)
        elif "down" in command_list:
            self.set_acceleration(-self.acceleration_rate)
        else:
            self.set_acceleration(0)

        if "left" in command_list:
            self.change_angle = self.turn_speed
        elif "right" in command_list:
            self.change_angle = -self.turn_speed
        else:
            self.change_angle = 0

        if key_command == "shoot" and key_type == 0:
            num_lasers = self.laser_bonus_count + 1
            angle_dx = (self.laser_max_angle * 2) / (num_lasers + 1)
            new_lasers = [Laser(self.center_x, self.center_y, (self.angle + self.laser_max_angle) - angle_dx * (i + 1), self.laser_sprite, laser_damage=self.laser_damage) for i in range(num_lasers)]
            for laser in new_lasers:
                laser.speed *= self.laser_speed_factor
                self.laser_list.append(laser)
                laser.fire()
                
    def queue_lasers_death(self):
        for laser in self.laser_list:
            laser.time_alive = laser.life + 1

    def _update_stats(self):
        self.acceleration_rate = self.orig_acceleration_rate * (1 + constants.PLAYER_ACCELERATION_SCALING * (self.upgrades["ship_acceleration"][0] - 1))
        self.turn_speed = self.orig_turn_speed * (1 + constants.PLAYER_TURN_SPEED_SCALING * (self.upgrades["ship_turn_speed"][0] - 1))
        self.laser_speed_factor = 1 + (constants.LASER_SPEED_SCALING * (self.upgrades["laser_speed"][0] - 1))
        self.laser_bonus_count = self.upgrades["laser_upgrade"][0] // constants.LASER_BONUS_LEVEL
        self.laser_damage = self.orig_laser_damage * (1 + constants.LASER_DAMAGE_SCALING * (self.upgrades["laser_upgrade"][0] - 1))

    # Overridden methods:
    def on_update(self, delta_time : float = 1/60):
        super().on_update(delta_time)
        for laser in self.laser_list:
            if laser.alive:
                laser.on_update(delta_time)
            else:
                self.laser_list.remove(laser)

    def draw(self):
        self.laser_list.draw()
        super().draw()
    
    def upgrade(self, upgrade):
        if upgrade in self.upgrades:
            self.upgrades[upgrade][0] += 1
            self.upgrades[upgrade][1] = floor(self.upgrades[upgrade][1] * constants.PLAYER_UPGRADE_COST_SCALING)
        self._update_stats()
    