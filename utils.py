import math
from panda3d.core import Plane, LPoint3f

EPSILON = 0.0001

CATEGORY_WALL = 0x01
CATEGORY_PLAYER = 0x02
CATEGORY_HUMANOID = 0x04
CATEGORY_ENEMY = 0x08
CATEGORY_PLAYER_PROJECTILE = 0x10
CATEGORY_ENEMY_PROJECTILE = 0x20


def degrees_to_radians(deg: float):
    return deg * (math.pi/180.0)


def radians_to_degrees(deg: float):
    return deg * (180.0/math.pi)


def float_eq(x: float, y: float) -> bool:
    return math.fabs(x - y) < EPSILON


def almost_zero(x: float) -> bool:
    return math.fabs(x) < EPSILON


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


def segment_plane_intersection(p1: LPoint3f, p2: LPoint3f, plane: Plane) -> list[LPoint3f]:
    points = []

    d1 = plane.distToPlane(p1)
    d2 = plane.distToPlane(p2)
    
    p1_on_plane = math.fabs(d1) < EPSILON
    p2_on_plane = math.fabs(d2) < EPSILON

    if p1_on_plane: 
        points.append(p1)

    if p2_on_plane: 
        points.append(p2)

    if p1_on_plane and p2_on_plane:
        return points

    if d1*d2 > EPSILON: return []

    s = d1 - d2
    if almost_zero(s):
        return points

    t = d1 / (d1 - d2)
    intersection_point = p1 + (p2 - p1) * t
    return [intersection_point]


def triangle_plane_intersection(tri: list[LPoint3f], plane: Plane) -> list[LPoint3f] | None:
    intersection_points = []
    ip = segment_plane_intersection(tri[0], tri[1], plane)
    if ip: intersection_points.extend(ip)
    ip = segment_plane_intersection(tri[1], tri[2], plane)
    if ip: intersection_points.extend(ip)
    ip = segment_plane_intersection(tri[2], tri[0], plane)
    if ip: intersection_points.extend(ip)

    return remove_duplicate_points(intersection_points) if len(intersection_points) else None


def remove_duplicate_points(points: list[LPoint3f]) -> list[LPoint3f]:
    final_list = []
    for p in points:
        is_dup = any(x for x in final_list if p.almostEqual(x, EPSILON))
        if not is_dup:
            final_list.append(p)
    return final_list