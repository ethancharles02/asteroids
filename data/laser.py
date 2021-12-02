from data.actor import Actor
from data import constants
from math import cos, sin, radians

class Laser(Actor):
    def __init__(self,  ship_x, ship_y, ship_angle, sprite = "assets/laserBlue01.png", sprite_scaling = constants.SPRITE_SCALING, laser_damage = 1):
        super().__init__(sprite, sprite_scaling)

        self.position = (ship_x, ship_y)
        self.life = 10
        self.time_alive = 0
        self.alive = True
        self.angle = ship_angle
        self.speed = constants.LASER_SPEED
        self.damage = laser_damage
        
    def fire(self):
        self.velocity[0] = cos(radians(self.angle)) * self.speed
        self.velocity[1] = sin(radians(self.angle)) * self.speed
    
    def on_update(self, delta_time):
        super().on_update(delta_time)
        self.time_alive += delta_time

    def loop_around_screen(self):
        if self.time_alive >= self.life:
            off_left_edge = self.position[0] + self.radius < 0
            off_right_edge = self.position[0] - self.radius > constants.SCREEN_WIDTH
            off_bottom_edge = self.position[1] + self.radius < 0
            off_top_edge = self.position[1] - self.radius > constants.SCREEN_HEIGHT
            if off_left_edge or off_bottom_edge or off_right_edge or off_top_edge:
                self.alive = False
        else:
            super().loop_around_screen()