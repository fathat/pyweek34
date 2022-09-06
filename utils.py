import math

EPSILON = 0.001


def degrees_to_radians(deg: float):
    return deg * (math.pi/180.0)


def radians_to_degrees(deg: float):
    return deg * (180.0/math.pi)


def float_eq(x: float, y: float) -> bool:
    return math.fabs(x - y) < EPSILON


def not_zero(x: float) -> bool:
    return math.fabs(x) > 0.0


# Smoothing rate dictates the proportion of source remaining after one second
def damp(source: float, smoothing: float, dt: float) -> float:
    return source * math.pow(smoothing, dt)


CATEGORY_WALL = 0x01
CATEGORY_PLAYER = 0x02
CATEGORY_HUMANOID = 0x04
CATEGORY_ENEMY = 0x08
CATEGORY_PLAYER_PROJECTILE = 0x10
CATEGORY_ENEMY_PROJECTILE = 0x20