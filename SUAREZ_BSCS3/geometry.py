"""Pure Python house coordinates, solid-wall collision and staircase math.

The x/z plane is the ground.  +z points toward the front garden.
Numbers are approximately metres.  No VPython dependency: easy to test.
"""
from math import cos, pi, sin

HOUSE_X = 11.0
HOUSE_Z = 8.0
LOT_X = 35.5
LOT_Z = 29.5
EYE_HEIGHT = 2.12
TOWER_X = -7.55
TOWER_Z = -12.80
DECK_Y = 10.55
STAIR_TURNS = 3
STAIR_RADIUS = 1.72
STAIR_START = pi / 2

# Solid walls in ground plan: (minimum x, maximum x, minimum z, maximum z)
# Doorways are deliberately left out. Windows remain solid for walking.
WALLS = [
    # Front: 2.5-metre opening at x=0 for front door.
    (-11.1, -1.32, 7.88, 8.12), (1.32, 11.1, 7.88, 8.12),
    # Back: open rear door connecting bedroom to observatory.
    (-11.1, -8.55, -8.12, -7.88), (-6.60, 11.1, -8.12, -7.88),
    # Sides
    (-11.13, -10.87, -8.1, 8.1), (10.87, 11.13, -8.1, 8.1),
    # Rear rooms: bedroom, bath, study; openings at bedroom/bath/study doors.
    (-10.87, -4.85, -1.25, -1.07),
    (-3.32, -1.50, -1.25, -1.07),
    (0.02, 4.03, -1.25, -1.07),
    (5.66, 10.87, -1.25, -1.07),
    # Interior bedroom/bath and bath/study dividing walls.
    (-2.82, -2.64, -7.92, -1.2),
    (2.64, 2.82, -7.92, -1.2),
    # Corridor walls to the tower; keep the passage clear.
    (-9.23, -9.00, -10.5, -8.0),
    (-6.14, -5.91, -10.5, -8.0),
]

POOL = (14.0, 28.0, -8.4, 3.5)


def clamp(value, lo, hi):
    return min(max(value, lo), hi)


def intersects(x, z, walls=WALLS, radius=0.28):
    """True when first-person camera's horizontal collision circle hits a wall."""
    if not (-LOT_X + radius < x < LOT_X - radius and
            -LOT_Z + radius < z < LOT_Z - radius):
        return True
    for x0, x1, z0, z1 in walls:
        if x0-radius < x < x1+radius and z0-radius < z < z1+radius:
            return True
    x0, x1, z0, z1 = POOL
    return x0-radius < x < x1+radius and z0-radius < z < z1+radius


def slide(old_x, old_z, dx, dz, walls=WALLS):
    """Separate x/z collision tests enable smooth movement along walls."""
    x = old_x + dx
    if intersects(x, old_z, walls):
        x = old_x
    z = old_z + dz
    if intersects(x, z, walls):
        z = old_z
    return x, z


def stair(t):
    """Position along winding staircase. t=0 ground, t=1 observation deck."""
    t = clamp(t, 0.0, 1.0)
    a = STAIR_START + t * 2*pi*STAIR_TURNS
    return (TOWER_X + STAIR_RADIUS*cos(a),
            0.55 + t * (DECK_Y - 0.55),
            TOWER_Z + STAIR_RADIUS*sin(a))


def stair_entrance(x, z):
    return abs(x - TOWER_X) < 1.10 and -11.75 < z < -10.48


def within_deck(x, z, margin=.40):
    return (TOWER_X-2.22+margin < x < TOWER_X+2.22-margin and
            TOWER_Z-2.24+margin < z < TOWER_Z+2.24-margin)


def look_vector(yaw, pitch):
    return (sin(yaw)*cos(pitch), sin(pitch), -cos(yaw)*cos(pitch))


def rotate_from_mouse(yaw, pitch, dx, dy, sensitivity=.004, pitch_limit=1.38):
    """Convert pixel mouse displacement to first-person yaw/pitch."""
    return (yaw + dx*sensitivity,
            clamp(pitch - dy*sensitivity, -pitch_limit, pitch_limit))


def angles_from_axis(x, y, z):
    """Read view direction after native VPython camera rotation."""
    from math import atan2, hypot
    return atan2(x, -z), atan2(y, hypot(x, z))
