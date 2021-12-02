from arcade import key

from sys import platform
if platform == "darwin":
    DEFAULT_FONT = "/Library/Fonts/Arial.ttf"
else:
    DEFAULT_FONT = "arial"

SCREEN_TITLE = "Asteroids"
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
SPRITE_SCALING = 1
MAIN_MENU = "assets/mainMenu2.png"
UPGRADE_SCREEN = "assets/upgrades.png"

# Scaling of difficulty for each level increase
LEVEL_SCALING = 0.1

# How fast upgrades increase in cost
PLAYER_UPGRADE_COST_SCALING = 1.2

# How fast the player moves forward and backward
PLAYER_ACCELERATION_RATE = 800
# How much the acceleration upgrade increases acceleration
PLAYER_ACCELERATION_SCALING = 0.1
# How fast the player turns left and right
PLAYER_TURN_SPEED = 135
PLAYER_TURN_SPEED_SCALING = 0.1
DEFAULT_KEYS = {
    key.A: "left",
    key.D: "right",
    key.W: "up",
    key.S: "down",
    key.SPACE: "shoot"
}
# The key that is used to return to the main menu or exit out of the game
ESCAPE_KEY = key.ESCAPE

# How fast laser speed increases with upgrades
LASER_SPEED_SCALING = 0.1
# Default laser speed
LASER_SPEED = 1000
# This is the maximum angle relative to the ship at which the laser can be fired when there are multiple lasers
LASER_MAX_ANGLE = 45
# The amount of levels required to increase the multishot of the ship
LASER_BONUS_LEVEL = 3
# How fast damage increases
LASER_DAMAGE_SCALING = 0.1
# Default laser damage
LASER_DAMAGE = 1
# Starting bonus lasers
DEFAULT_BONUS_LASER_COUNT = 0

ASTEROID_SPIN_RANGE = (-100, 100)
ASTEROID_SPEED_RANGE = (0, 200)
ASTEROID_ANGLE_RANGE = (0, 359)
# Size range is as a percentage, 0.5 to 1.5 would be a range from 50% size to 150% size
ASTEROID_SIZE_RANGE = (0.9, 1.2)
# The units refer to how many singular asteroids make up that size, the small asteroid is 1 since it is the baseline
ASTEROID_SIZE_UNITS = (6, 2, 1)
ASTEROID_SPRITE_LIST = ["assets/meteorGrey_big1.png", "assets/meteorGrey_med1.png", "assets/meteorGrey_small1.png"]
ASTEROID_HEALTHBAR_OFFSET_Y = 35
ASTEROID_HEALTHBAR_WIDTH_FACTOR = 1
ASTEROID_HEALTHBAR_HEIGHT = 20
# The change in color, left is high health, right is low health
ASTEROID_HEALTH_COLOR_CHANGE = ((0, 255, 0), (255, 0, 0))

# Particle constants
PARTICLE_GRAVITY = 0
PARTICLE_FADE_RATE = 12
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 10
PARTICLE_RADIUS = 3
PARTICLE_COLORS = [
    (100, 100, 100),
    (150, 150, 150),
    (160, 160, 160)
]
PARTICLE_SPARKLE_CHANCE = 0.02
SMOKE_START_SCALE = 0.25
SMOKE_EXPANSION_RATE = 0.03
SMOKE_FADE_RATE = 12
SMOKE_RISE_RATE = 0
SMOKE_CHANCE = 0.05