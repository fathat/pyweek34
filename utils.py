import math

EPSILON = 0.001


def float_eq(x: float, y: float) -> bool:
    return math.fabs(x - y) < EPSILON


def not_zero(x: float) -> bool:
    return not float_eq(x, 0.0)