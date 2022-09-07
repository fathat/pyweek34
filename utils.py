import math
from panda3d.core import Plane, LPoint3f

EPSILON = 0.0001

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


def clamp(x, minx, maxx):
    if x > maxx: return maxx
    if x < minx: return minx
    return x

# Smoothing rate dictates the proportion of source remaining after one second
def damp(source: float, smoothing: float, dt: float) -> float:
    return source * math.pow(smoothing, dt)


def slerp(q1, q2, t):
    costheta = q1.dot(q2)
    if costheta < 0.0:
        costheta = -costheta
        q1 = q1.conjugate()
    elif costheta > 1.0:
        costheta = 1.0

    theta = math.acos(costheta)
    if abs(theta) < 0.01:
        return q2

    sintheta = math.sqrt(1.0 - costheta * costheta)
    if abs(sintheta) < 0.01:
        return (q1+q2)*0.5

    r1 = math.sin((1.0 - t) * theta) / sintheta
    r2 = math.sin(t * theta) / sintheta
    return (q1*r1) + (q2*r2)


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


def firstorder_lowpass(prev, curr, dt, tau):
    alpha = 1.0 - math.exp(-dt / tau)
    return prev + alpha * (curr - prev)