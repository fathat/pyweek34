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


def move_towards(source: float, target: float, rate: float, dt: float) -> float:
    if float_eq(source, target): return target
    
    if source < target:
        return min(source + rate * dt, target)
    else:
        return max(source - rate * dt, target)
        