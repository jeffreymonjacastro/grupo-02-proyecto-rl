"""Geometría y discretización compartidas por las cuatro tareas."""

import math

FIELD_X = 52.5
FIELD_Y = 34.0
GOAL_X = 52.5
GOAL_HALF_WIDTH = 7.0


def distance(start, end):
    return math.hypot(end[0] - start[0], end[1] - start[1])


def relative_angle(start, end, heading):
    bearing = math.degrees(math.atan2(end[1] - start[1], end[0] - start[0]))
    return (bearing - heading + 180.0) % 360.0 - 180.0


def advance(position, heading, metres):
    angle = math.radians(heading)
    return position[0] + metres * math.cos(angle), position[1] + metres * math.sin(
        angle
    )


def zone(value, limits):
    """Índice de la primera frontera estrictamente mayor que value."""
    return sum(value >= limit for limit in limits)


def angle_zone(angle):
    """Cuatro sectores: frente, izquierda, atrás y derecha."""
    angle = (angle + 180.0) % 360.0 - 180.0
    if -45.0 <= angle < 45.0:
        return 0
    if 45.0 <= angle < 135.0:
        return 1
    if angle >= 135.0 or angle < -135.0:
        return 2
    return 3


def outside_field(position):
    return abs(position[0]) > FIELD_X or abs(position[1]) > FIELD_Y


def segment_distance(point, start, end):
    """Distancia del defensor al segmento que recorre un pase."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return distance(point, start)
    fraction = max(
        0.0,
        min(1.0, ((point[0] - start[0]) * dx + (point[1] - start[1]) * dy) / length_sq),
    )
    nearest = start[0] + fraction * dx, start[1] + fraction * dy
    return distance(point, nearest)
