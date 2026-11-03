"""Interactive Dream House virtual tour built with VPython."""

from vpython import *
import math
import random

scene = canvas(
    title="My Dream House | Interactive 3D Virtual Tour",
    width=1200,
    height=760,
    background=vector(0.74, 0.86, 0.92),
    center=vector(0, 6, 11),
    range=40,
    autoscale=False,
)
scene.up = vector(0, 1, 0)
scene.ambient = vector(0.68, 0.68, 0.70)

GRASS = vector(0.20, 0.44, 0.28)
WALL = vector(0.94, 0.91, 0.82)
WHITE = vector(0.985, 0.985, 0.96)
WOOD = vector(0.38, 0.22, 0.12)
DARK = vector(0.09, 0.13, 0.15)
GLASS = vector(0.28, 0.64, 0.76)
OCEAN = vector(0.05, 0.48, 0.68)

CUTAWAY_OBJECTS = []
INTERIOR_OBJECTS = []
CUTAWAY_ENABLED = False
TV_ON = False
TV_SCREEN = None
CHARACTER_ANIMATION_ON = True
COUPLE = []


def make_box(pos, size, color, **kwargs):
    return box(pos=vector(*pos), size=vector(*size), color=color, **kwargs)


def make_cylinder(pos, axis, radius, color, **kwargs):
    axis_vector = axis if isinstance(axis, vector) else vector(*axis)
    return cylinder(pos=vector(*pos), axis=axis_vector, radius=radius,
                    color=color, **kwargs)


def make_sphere(pos, radius, color, **kwargs):
    return sphere(pos=vector(*pos), radius=radius, color=color, **kwargs)


def make_window_front(x, y, z, width, height):
    make_box((x, y, z), (width, height, 0.16), GLASS,
             opacity=0.82, shininess=0.85)
    frame = 0.16
    for dx in (-width / 2, width / 2):
        make_box((x + dx, y, z - 0.11), (frame, height + frame, 0.12), WHITE)
    for dy in (-height / 2, height / 2):
        make_box((x, y + dy, z - 0.11), (width + frame, frame, 0.12), WHITE)
    make_box((x, y, z - 0.13), (0.09, height, 0.10), WHITE)
    make_box((x, y, z - 0.13), (width, 0.09, 0.10), WHITE)


def make_window_side(x, y, z, width, height, side=1):
    make_box((x, y, z), (0.16, height, width), GLASS,
             opacity=0.82, shininess=0.85)
    frame = 0.14
    for dz in (-width / 2, width / 2):
        make_box((x + side * 0.11, y, z + dz),
                 (0.12, height + frame, frame), WHITE)
    for dy in (-height / 2, height / 2):
        make_box((x + side * 0.11, y + dy, z),
                 (0.12, frame, width + frame), WHITE)


# ---------------------------------------------------------------------------
# LANDSCAPE AND HOUSE EXTERIOR
# ---------------------------------------------------------------------------


def create_landscape():
    make_box((0, -0.35, 2), (110, 0.7, 100), GRASS)
    make_box((0, -0.02, 34), (110, 0.10, 20), vector(0.74, 0.67, 0.52))
    make_box((0, -0.25, 57), (130, 0.18, 34), OCEAN, shininess=0.95)
    for z in range(45, 73, 3):
        make_box((0, -0.145, z), (105, 0.025, 0.12),
                 vector(0.32, 0.72, 0.82), opacity=0.58)

    make_sphere((-44, 12, 82), 6, vector(0.44, 0.47, 0.42), opacity=0.32)
    make_sphere((44, 10, 82), 5, vector(0.48, 0.49, 0.43), opacity=0.28)
    make_sphere((-34, 29, 76), 2.1, vector(1.0, 0.91, 0.62), emissive=True)

    for cx, cy, cz, scale in [(-28, 27, 48, 1.0), (-5, 31, 52, 1.2),
                              (24, 26, 49, 0.9), (42, 33, 58, 1.1)]:
        for ox, oy, r in [(-1.4, 0, 1.6), (0, 0.5, 2.0), (1.6, 0.1, 1.5)]:
            make_sphere((cx + ox * scale, cy + oy * scale, cz),
                        r * scale, vector(0.97, 0.98, 1.0), opacity=0.88)


def create_tree(x, z, height=8, canopy_color=None):
    """Create a recognizable coconut palm from a curved trunk and fronds."""
    if canopy_color is None:
        canopy_color = vector(0.12, 0.42, 0.16)

    crown_y = height * 0.92
    crown_x = x + height * 0.035
    crown_z = z - height * 0.012

    # A slightly curved trunk made from overlapping tapered-looking segments.
    segments = 6
    for index in range(segments):
        y0 = height * index / segments
        y1 = height * (index + 1) / segments
        offset = height * 0.035 * (index + 1) / segments
        make_cylinder((x + offset - height * 0.018, y0, z),
                      (height * 0.035 / segments, y1 - y0, 0),
                      0.30 - index * 0.018, vector(0.48, 0.31, 0.16))

    # Long, layered palm fronds radiate from the crown.
    for angle in range(0, 360, 45):
        radians = math.radians(angle)
        horizontal_x = math.cos(radians)
        horizontal_z = math.sin(radians)
        frond_length = height * 0.42
        end = vector(crown_x + horizontal_x * frond_length,
                     crown_y - height * 0.12 + abs(horizontal_x) * 0.2,
                     crown_z + horizontal_z * frond_length)
        make_cylinder((crown_x, crown_y, crown_z),
                      end - vector(crown_x, crown_y, crown_z),
                      height * 0.055, canopy_color)

        for side in (-1, 1):
            leaflet_x = crown_x + horizontal_x * frond_length * 0.65
            leaflet_z = crown_z + horizontal_z * frond_length * 0.65
            make_sphere((leaflet_x + side * horizontal_z * height * 0.20,
                         crown_y - height * 0.10,
                         leaflet_z - side * horizontal_x * height * 0.20),
                        height * 0.075, vector(0.18, 0.50, 0.18))

    # Coconuts beneath the crown.
    for dx, dz in ((-0.30, 0.05), (0.30, 0.05), (0.05, -0.32)):
        make_sphere((crown_x + dx, crown_y - 0.38, crown_z + dz),
                    height * 0.055, vector(0.48, 0.34, 0.16))


def create_landscaping():
    tree_positions = [
        (-24,-8,10), (-30,5,9), (-22,18,11), (25,-7,10), (31,7,9),
        (24,20,11), (-38,24,9), (38,25,10), (-39,-17,8), (39,-18,9),
        (-14,29,8), (15,30,9), (-19,-18,8), (20,-17,9), (-34,-25,10),
        (34,-24,10), (-44,10,11), (44,12,11), (-27,32,9), (28,34,10),
        (-5,26,8), (7,27,8), (-10,20,7), (11,21,8), (-48,-8,9), (48,-7,9)
    ]
    for i, (x, z, height) in enumerate(tree_positions):
        shade = vector(0.12 + (i % 3) * 0.025,
                       0.31 + (i % 2) * 0.06, 0.14)
        create_tree(x, z, height, shade)

    flower_colors = [vector(0.95,0.28,0.36), vector(1.0,0.72,0.18),
                     vector(0.78,0.42,0.88), vector(1.0,0.88,0.78)]
    random.seed(8)
    for x_start, x_end, z in [(-12,-7,-8), (7,12,-8), (-13,-8,12),
                              (8,13,12), (-21,-15,-3), (15,21,14),
                              (-4,-1,17), (1,4,17)]:
        for _ in range(20):
            x = random.uniform(x_start, x_end)
            zz = z + random.uniform(-1.0, 1.0)
            flower_color = random.choice(flower_colors)
            make_cylinder((x, 0.0, zz), (0, 0.22, 0), 0.035,
                          vector(0.12, 0.38, 0.13))
            make_sphere((x, 0.23, zz), 0.16, flower_color)
            for petal_angle in range(0, 360, 90):
                angle = math.radians(petal_angle)
                make_sphere((x + math.cos(angle) * 0.09,
                             0.25, zz + math.sin(angle) * 0.09),
                            0.055, flower_color)

    for x, z in [(-12,-3),(-14,4),(12,-3),(14,4),(-10,14),(10,14),(-18,17),(18,17)]:
        make_sphere((x, 0.75, z), 0.85, vector(0.17, 0.40, 0.17))


def create_house():
    make_box((0,0.25,0), (19.5,0.5,14.5), vector(0.72,0.70,0.64))
    make_box((0,6.15,0), (19.5,0.35,14.5), WHITE)

    floor_walls = []
    floor_walls.append(make_box((-7.2,3.2,0), (5.1,5.6,12.8), WALL))
    floor_walls.append(make_box((7.2,3.2,0), (5.1,5.6,12.8), WALL))
    floor_walls.append(make_box((0,3.2,5.9), (9.4,5.6,0.9), WALL))
    floor_walls.append(make_box((0,5.55,-5.9), (9.4,0.9,0.9), WALL))

    make_window_front(-4.5,3.2,-6.48,4.2,4.3)
    make_window_front(4.5,3.2,-6.48,4.2,4.3)
    make_box((0,2.55,-6.53), (2.0,4.7,0.22), WOOD)
    make_box((0,2.55,-6.67), (1.55,4.35,0.06),
             vector(0.28,0.54,0.64), opacity=0.7)
    make_sphere((0.67,2.55,-6.78), 0.10, vector(0.85,0.68,0.28))

    make_window_side(9.78,3.4,-2.2,3.2,2.7, side=1)
    make_window_side(-9.78,3.4,1.5,3.5,2.7, side=-1)

    upper = make_box((0,8.85,0.3), (18.4,5.0,12.8), WALL, opacity=0.96)
    make_box((0,7.0,-6.18), (18.3,0.22,0.18), DARK)
    make_window_front(-5.8,9.0,-6.18,4.5,3.1)
    make_window_front(0.0,9.0,-6.18,4.5,3.1)
    make_window_front(5.8,9.0,-6.18,4.5,3.1)

    make_box((0,9.0,6.78), (9.2,3.2,0.13), GLASS,
             opacity=0.82, shininess=0.9)
    for x in (-4.6,0,4.6):
        make_box((x,9.0,6.65), (0.13,3.35,0.12), WHITE)

    roof = make_box((0,11.75,0.2), (20.5,0.55,15.5), DARK)
    roof_top = make_box((0,12.08,0.2), (20.0,0.18,15.0), WHITE)
    CUTAWAY_OBJECTS.extend([upper, roof, roof_top])

    make_box((5.5,13.15,2.8), (7.0,0.18,5.2), WOOD)
    for x in (2.3,4.4,6.5,8.7):
        make_box((x,12.8,2.8), (0.16,1.6,5.2), WOOD)
    for z in (0.3,2.0,3.7,5.3):
        make_box((5.5,13.55,z), (7.0,0.12,0.12), WOOD)

    make_box((0,7.05,8.15), (12.8,0.35,4.1), vector(0.55,0.38,0.25))
    make_box((0,8.92,10.12), (12.8,0.16,0.20), DARK)
    make_box((0,8.0,10.12), (12.5,1.75,0.12),
             vector(0.55,0.78,0.84), opacity=0.42)
    for x in (-6.2,-3.1,0,3.1,6.2):
        make_box((x,8.0,10.12), (0.12,1.85,0.18), DARK)

    make_box((0,5.45,-8.0), (6.8,0.28,3.7), DARK)
    for x in (-2.9,2.9):
        make_box((x,2.7,-9.3), (0.25,5.4,0.25), WHITE)
    for step in range(4):
        make_box((0,0.18+step*0.16,-7.2-step*0.58),
                 (4.2,0.36,1.25), vector(0.72,0.70,0.64))

    make_box((-9.3,3.0,-4.5), (0.22,5.7,3.0), WOOD)
    make_box((9.3,3.0,4.4), (0.22,5.7,3.0), WOOD)
    for x in (-2.0,2.0):
        make_box((x,3.7,-6.75), (0.28,0.65,0.18),
                 vector(0.95,0.78,0.38), emissive=True)
        make_sphere((x,3.7,-6.86), 0.12,
                    vector(1.0,0.83,0.48), emissive=True)


def create_driveway_and_car():
    make_box((0,0.04,-19.0), (17.0,0.12,13.0), vector(0.36,0.38,0.40))
    for z in (-12.0,-10.8,-9.6):
        make_box((0,0.12,z), (4.3,0.16,0.85), vector(0.73,0.72,0.66))
    for x in (-8.3,8.3):
        make_box((x,0.13,-19.0), (0.18,0.16,13.0), WHITE)

    cx, cz = -4.0, -19.0
    car_blue = vector(0.10,0.25,0.52)
    make_box((cx,1.05,cz), (6.2,1.25,2.8), car_blue, shininess=0.85)
    make_box((cx,1.62,cz+0.15), (3.7,1.05,2.45),
             vector(0.12,0.30,0.58), shininess=0.9)
    make_box((cx,2.12,cz-0.15), (1.65,0.78,2.25),
             vector(0.28,0.62,0.75), opacity=0.78)
    make_box((cx,2.55,cz+0.48), (2.7,0.16,2.2), car_blue)
    for x in (cx-2.0,cx+2.0):
        for z_wheel in (cz-1.35,cz+1.35):
            make_cylinder((x,0.75,z_wheel), (0,0,0.35), 0.58, DARK)
            make_cylinder((x,0.75,z_wheel-0.04), (0,0,0.43),
                          0.25, vector(0.68,0.70,0.72))


def create_pool_and_seating():
    make_box((-18,0.08,5), (11.5,0.16,7.0), WHITE)
    make_box((-18,0.17,5), (10.8,0.20,6.3),
             vector(0.16,0.58,0.78), shininess=0.95)
    for x in (-22,-14.8):
        make_box((x,0.58,0.7), (2.4,0.16,4.0), vector(0.58,0.39,0.22))
        make_box((x,1.05,2.15), (2.4,0.85,0.18), vector(0.58,0.39,0.22))

    make_box((15.5,0.12,7.0), (8.0,0.22,6.0), vector(0.72,0.68,0.58))
    make_cylinder((15.5,1.15,7.0), (0,0.12,0), 1.05, WHITE)
    make_cylinder((15.5,0.25,7.0), (0,0.9,0), 0.13, DARK)
    for x in (12.7,18.3):
        make_box((x,0.75,7.0), (1.5,0.25,2.1), vector(0.83,0.82,0.72))
        make_box((x,1.3,7.85), (1.5,1.2,0.22), vector(0.83,0.82,0.72))

    for x, z in ((10.5,9),(20.5,9),(-10.5,-10),(10.5,-10)):
        make_cylinder((x,0,z), (0,1.35,0), 0.09, DARK)
        make_sphere((x,1.45,z), 0.22, vector(1,0.82,0.42), emissive=True)


# ---------------------------------------------------------------------------
# INTERIOR: FLOORS, ROOMS AND FURNITURE
# ---------------------------------------------------------------------------


def add_interior_wall(pos, size, color=WALL, **kwargs):
    obj = make_box(pos, size, color, **kwargs)
    INTERIOR_OBJECTS.append(obj)
    return obj


def create_ground_floor():
    make_box((0,0.58,0), (18.8,0.12,13.8), vector(0.76,0.69,0.58))
    add_interior_wall((-1.0,3.15,-2.0), (0.28,5.3,7.8))
    add_interior_wall((-1.0,3.15,4.75), (0.28,5.3,2.6))
    add_interior_wall((-5.8,3.15,0.0), (0.25,5.3,4.1))
    add_interior_wall((-7.65,3.15,2.0), (3.4,5.3,0.25))
    add_interior_wall((7.7,3.15,3.9), (0.25,5.3,4.8))


def create_staircase():
    for step in range(14):
        make_box((6.6,0.78+step*0.42,-3.3+step*0.42),
                 (3.0,0.28,0.55), vector(0.62,0.48,0.34))
    make_box((5.05,3.45,0), (0.12,0.12,6.0), DARK)
    for z in (-2.8,-1.4,0,1.4,2.8):
        make_cylinder((5.05,3.45,z), (0,1.7,0), 0.035, DARK)


def create_living_room():
    global TV_SCREEN
    make_box((-5.4,1.25,-1.2), (5.4,0.8,2.3), vector(0.72,0.78,0.78))
    make_box((-5.4,1.75,-0.25), (5.4,1.25,0.35), vector(0.68,0.74,0.74))
    make_cylinder((-5.4,0.75,2.0), (0,0.10,0), 1.55, vector(0.30,0.32,0.34))
    make_cylinder((-5.4,0.82,2.0), (0,0.05,0), 1.42, vector(0.72,0.66,0.55))
    make_box((-5.4,3.0,5.45), (4.8,2.7,0.25), DARK)
    TV_SCREEN = make_box((-5.4,3.0,5.28), (4.25,2.15,0.08),
                         vector(0.04,0.08,0.12), emissive=True)


def create_kitchen():
    make_box((5.5,1.05,4.7), (6.5,1.1,1.4), vector(0.69,0.73,0.72))
    make_box((5.5,2.45,4.7), (6.5,1.6,0.55), vector(0.86,0.84,0.78))
    make_box((8.35,2.4,2.8), (1.65,3.7,1.55), vector(0.72,0.75,0.74))
    make_box((3.9,1.65,3.95), (1.8,0.08,1.2), DARK)
    for x in (3.45,4.35):
        for z in (3.55,4.35):
            make_sphere((x,1.72,z), 0.16, vector(0.04,0.04,0.04))
    make_box((5.0,1.15,0.4), (4.0,1.0,1.8), WOOD)
    make_box((5.0,1.70,0.4), (4.2,0.12,2.0), WHITE, shininess=0.75)


def create_dining_room():
    make_cylinder((1.0,0.82,0.0), (0,0.12,0), 2.4, WOOD)
    make_cylinder((1.0,0.88,0.0), (0,0.12,0), 2.2, vector(0.72,0.55,0.34))
    for x, z in [(-1.2,-0.8),(-1.2,0.8),(3.2,-0.8),(3.2,0.8),(0,-2.3),(2,2.3)]:
        make_box((x,1.05,z), (1.0,0.16,1.0), vector(0.72,0.50,0.32))
        make_box((x,1.65,z+0.42), (1.0,0.95,0.18), vector(0.72,0.50,0.32))
    make_cylinder((1.0,3.2,0.0), (0,0.12,0), 0.35, DARK)
    make_sphere((1.0,3.0,0.0), 0.55, vector(1.0,0.82,0.46), emissive=True)


def create_bathrooms():
    make_box((-7.0,0.75,3.8), (1.2,0.3,1.8), WHITE)
    make_box((-7.0,1.55,4.55), (1.2,1.2,0.2), WHITE)
    make_sphere((-7.0,2.05,4.42), 0.3, GLASS)


def create_second_floor():
    make_box((0,6.58,0), (18.8,0.12,13.8), vector(0.76,0.69,0.58))
    add_interior_wall((0,9.0,-1.0), (0.28,4.7,10.5))
    add_interior_wall((-6.0,9.0,1.5), (5.0,4.7,0.25))
    add_interior_wall((6.0,9.0,1.5), (5.0,4.7,0.25))
    make_box((-5.0,7.0,4.7), (1.2,0.3,1.8), WHITE)
    make_box((-5.0,8.0,5.4), (1.2,1.1,0.2), WHITE)


def create_bedrooms():
    make_box((-4.8,7.05,0), (5.2,0.65,6.0), vector(0.42,0.31,0.27))
    make_box((-4.8,7.75,0), (4.8,1.0,5.6), vector(0.82,0.86,0.84))
    make_box((-4.8,8.12,-2.45), (5.0,1.75,0.6), vector(0.52,0.38,0.50))
    make_box((-7.0,7.0,-3.6), (1.2,0.55,1.2), WOOD)
    make_box((-2.5,7.0,-3.6), (1.2,0.55,1.2), WOOD)
    make_box((-8.25,8.9,2.5), (1.8,4.3,3.7), vector(0.42,0.27,0.18))

    make_box((5.0,7.05,0), (4.0,0.65,5.0), WOOD)
    make_box((5.0,7.75,0), (3.7,0.95,4.6), vector(0.48,0.68,0.72))
    make_box((5.0,8.15,-2.05), (4.0,1.5,0.5), vector(0.62,0.55,0.72))

    make_box((7.8,7.65,4.4), (3.2,0.18,1.5), WOOD)
    make_box((7.8,8.55,5.05), (2.1,1.45,0.12), DARK)
    make_box((7.8,7.05,4.4), (1.0,0.65,1.0), vector(0.35,0.50,0.54))


# ---------------------------------------------------------------------------
# HUMAN CHARACTERS
# ---------------------------------------------------------------------------


def create_human_character(name, x, z, shirt, skin, hair, long_hair=False):
    parts = []
    y_ground = 0.5
    parts.append(make_box((x,y_ground+1.75,z), (1.05,1.65,0.55), shirt))
    parts.append(make_sphere((x,y_ground+3.15,z), 0.50, skin))
    parts.append(make_cylinder((x,y_ground+2.55,z), (0,0.35,0), 0.25, skin))
    if long_hair:
        parts.append(make_sphere((x,y_ground+3.28,z-0.05), 0.53, hair))
        parts.append(make_box((x,y_ground+2.95,z-0.32), (0.92,1.05,0.18), hair))
    else:
        parts.append(make_sphere((x,y_ground+3.42,z+0.02), 0.52, hair))

    arms = []
    legs = []
    for side in (-1,1):
        arm = make_cylinder((x+side*0.68,y_ground+1.72,z),
                            (side*0.16,-1.12,0), 0.12, skin)
        leg = make_cylinder((x+side*0.28,y_ground+0.62,z),
                            (0,-1.15,0), 0.20, vector(0.16,0.20,0.27))
        arms.append(arm)
        legs.append(leg)
        parts.extend([arm,leg])
        parts.append(make_box((x+side*0.28,y_ground+0.08,z-0.12),
                              (0.48,0.16,0.75), vector(0.88,0.82,0.70)))
    return {"name":name,"parts":parts,"arms":arms,"legs":legs,
            "x":x,"z":z}


# ---------------------------------------------------------------------------
# CAMERA, NAVIGATION AND TOUR MENU
# ---------------------------------------------------------------------------

ROOMS = {
    "exterior": (vector(0,6,-23), vector(0.05,-0.05,1), 40),
    "enter": (vector(0,2.7,-10.8), vector(0,-0.02,1), 12),
    "ground": (vector(0,3,-15), vector(0,0,1), 22),
    "second": (vector(0,8.7,-15), vector(0,0,1), 20),
    "living": (vector(-5,3,-10.5), vector(0.55,0,1), 10),
    "kitchen": (vector(6.2,3,-10.5), vector(-0.45,0,1), 9),
    "dining": (vector(1,3,-10.2), vector(0,0,1), 9),
    "master": (vector(-5,9,-13), vector(0.55,0,1), 11),
    "second_bedroom": (vector(5.5,9,-13), vector(-0.55,0,1), 10),
    "balcony": (vector(0,9,0), vector(0,-0.05,1), 16),
}

camera_transition = None
camera_transition_step = 0
keys_down = set()


def interpolate_vector(start, end, fraction):
    return start + (end - start) * fraction


def set_camera_view(view_name):
    global camera_transition, camera_transition_step
    pos, axis, view_range = ROOMS[view_name]
    camera_transition = {"start_pos":scene.camera.pos,
                         "start_axis":scene.camera.axis,
                         "start_range":scene.range,
                         "end_pos":pos,"end_axis":axis,
                         "end_range":view_range}
    camera_transition_step = 0


def reset_camera():
    set_camera_view("exterior")


def update_camera_transition():
    global camera_transition, camera_transition_step
    if camera_transition is None:
        return
    camera_transition_step += 1
    fraction = min(1.0, camera_transition_step / 30.0)
    eased = fraction * fraction * (3.0 - 2.0 * fraction)
    scene.camera.pos = interpolate_vector(camera_transition["start_pos"],
                                          camera_transition["end_pos"], eased)
    scene.camera.axis = interpolate_vector(camera_transition["start_axis"],
                                           camera_transition["end_axis"], eased)
    scene.range = camera_transition["start_range"] + (
        camera_transition["end_range"] - camera_transition["start_range"]
    ) * eased
    if fraction >= 1.0:
        camera_transition = None


def handle_keydown(evt):
    key = evt.key.lower()
    keys_down.add(key)
    if key == "r":
        reset_camera()
    elif key == "escape":
        set_camera_view("exterior")


def handle_keyup(evt):
    key = evt.key.lower()
    if key in keys_down:
        keys_down.remove(key)


def update_walkthrough():
    if not keys_down:
        return
    forward = scene.camera.axis.norm()
    right = vector(forward.z, 0, -forward.x).norm()
    movement = vector(0,0,0)
    speed = 0.16
    if "w" in keys_down:
        movement += forward * speed
    if "s" in keys_down:
        movement -= forward * speed
    if "a" in keys_down:
        movement -= right * speed
    if "d" in keys_down:
        movement += right * speed
    if "q" in keys_down:
        movement.y -= speed
    if "e" in keys_down:
        movement.y += speed

    scene.camera.pos += movement
    scene.camera.pos.x = max(-8.6,min(8.6,scene.camera.pos.x))
    scene.camera.pos.z = max(-5.9,min(5.9,scene.camera.pos.z))
    scene.camera.pos.y = max(1.3,min(10.4,scene.camera.pos.y))


def toggle_cutaway():
    global CUTAWAY_ENABLED
    CUTAWAY_ENABLED = not CUTAWAY_ENABLED
    for obj in CUTAWAY_OBJECTS:
        obj.visible = not CUTAWAY_ENABLED


def toggle_tv():
    global TV_ON
    TV_ON = not TV_ON
    if TV_SCREEN is not None:
        TV_SCREEN.color = vector(0.30,0.55,0.75) if TV_ON else vector(0.04,0.08,0.12)
        TV_SCREEN.emissive = TV_ON


def toggle_characters():
    global CHARACTER_ANIMATION_ON
    CHARACTER_ANIMATION_ON = not CHARACTER_ANIMATION_ON


def animate_characters():
    if not CHARACTER_ANIMATION_ON:
        return
    phase = scene.time * 0.7 if hasattr(scene,"time") else 0
    for index, person in enumerate(COUPLE):
        offset = 0.12 * math.sin(phase + index * math.pi)
        for arm in person["arms"]:
            arm.axis.x = 0.16 + offset


def create_tour_menu():
    scene.append_to_caption("\n<b>Dream House Tour</b>\n")
    items = (("EXTERIOR VIEW","exterior"),("ENTER HOUSE","enter"),
             ("GROUND FLOOR","ground"),("SECOND FLOOR","second"),
             ("LIVING ROOM","living"),("KITCHEN","kitchen"),
             ("DINING AREA","dining"),("MASTER BEDROOM","master"),
             ("SECOND BEDROOM","second_bedroom"),("BALCONY","balcony"))
    for label, view_name in items:
        button(text=label, bind=lambda b, view=view_name: set_camera_view(view))
        scene.append_to_caption(" ")
    scene.append_to_caption("\n")
    button(text="ROOF / CUTAWAY MODE", bind=lambda b: toggle_cutaway())
    scene.append_to_caption(" ")
    button(text="TELEVISION", bind=lambda b: toggle_tv())
    scene.append_to_caption(" ")
    button(text="PAUSE / PLAY COUPLE", bind=lambda b: toggle_characters())
    scene.append_to_caption(" ")
    button(text="RESET VIEW", bind=lambda b: reset_camera())
    scene.append_to_caption("\n<br>W/S: forward/back &nbsp; A/D: left/right &nbsp; Q/E: down/up<br>R: reset &nbsp; ESC: exterior\n")


scene.bind("keydown", handle_keydown)
scene.bind("keyup", handle_keyup)

# BUILD
create_landscape()
create_landscaping()
create_house()
create_driveway_and_car()
create_pool_and_seating()
create_ground_floor()
create_staircase()
create_living_room()
create_kitchen()
create_dining_room()
create_bathrooms()
create_second_floor()
create_bedrooms()

COUPLE = [
    create_human_character("Me",13,7,vector(0.18,0.38,0.62),
                           vector(0.88,0.67,0.50),vector(0.18,0.11,0.08)),
    create_human_character("Future partner",14.7,7.5,
                           vector(0.72,0.32,0.48),vector(0.80,0.60,0.45),
                           vector(0.12,0.07,0.05),True),
]

create_tour_menu()
reset_camera()

while True:
    rate(30)
    update_camera_transition()
    update_walkthrough()
    animate_characters()
