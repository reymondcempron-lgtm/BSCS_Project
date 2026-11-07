import math
import random

from vpython import (box, button, canvas, compound, cylinder, distant_light,
                     ellipsoid, mag, norm, pyramid, rate, sphere, vector)

random.seed(14)


CAM_TARGET = vector(-0.6, 2.8, 0.0)
CAM_START = vector(-4.0, 6.0, -21.0)
EXTERIOR_RANGE = 17.5
ZOOM_MIN, ZOOM_MAX = 0.8, 45.0

scene = canvas(
    title="NAME:GLENNDHEL JAY DANO  | PROGRAM:BSCS 3 | SUBJECT:GRAPHICS AND VISUAL COMPUTING | INSTRUCTOR:REYMOND CEMPRON",
    width=1280, height=820,
    background=vector(0.46, 0.72, 0.95),
    center=CAM_TARGET,
    range=EXTERIOR_RANGE,
    fov=0.9,
    autoscale=False,
)
scene.caption = ("Mouse: drag to orbit  |  Scroll/pinch: zoom  |  "
                 "Shift-drag/right-drag: pan  |  Use the buttons to step inside\n")

scene.lights = []
distant_light(direction=vector(-0.6, -1.0, -0.4), color=vector(1.00, 0.95, 0.84))
distant_light(direction=vector(0.6, -0.4, 0.8), color=vector(0.42, 0.52, 0.70))
distant_light(direction=vector(0.0, 1.0, 0.0), color=vector(0.20, 0.18, 0.15))
scene.ambient = vector(0.46, 0.48, 0.50)


FLOOR = 0.25
CEILING = 4.09
SLAB_TOP = 0.21


def rgb(r, g, b):
    return vector(r, g, b)


WHITE      = rgb(0.95, 0.94, 0.90)
WARM_WHITE = rgb(0.88, 0.86, 0.80)
CHARCOAL   = rgb(0.09, 0.10, 0.11)
GLASS      = rgb(0.16, 0.30, 0.38)
GLASS_HI   = rgb(0.55, 0.72, 0.80)
STONE      = rgb(0.74, 0.66, 0.53)
STONE_DARK = rgb(0.58, 0.51, 0.40)
CONCRETE   = rgb(0.64, 0.63, 0.59)
ROOF_MID   = rgb(0.42, 0.40, 0.36)
JOINT_LINE = rgb(0.44, 0.44, 0.41)

WOOD_DARK  = rgb(0.30, 0.14, 0.06)
WOOD_LIGHT = rgb(0.52, 0.30, 0.15)
BRASS      = rgb(0.80, 0.68, 0.38)
STEEL      = rgb(0.74, 0.76, 0.78)
CHROME     = rgb(0.85, 0.87, 0.89)

ASPHALT    = rgb(0.17, 0.18, 0.19)
LAWN       = rgb(0.24, 0.52, 0.18)
SOIL       = rgb(0.22, 0.14, 0.09)
BARK       = rgb(0.34, 0.23, 0.14)
BARK_DARK  = rgb(0.22, 0.14, 0.08)
TERRACOTTA = rgb(0.70, 0.38, 0.24)
GREENS = [rgb(0.07, 0.36, 0.14), rgb(0.12, 0.48, 0.18),
          rgb(0.20, 0.58, 0.20), rgb(0.32, 0.66, 0.22)]

FLOOR_WOOD = rgb(0.64, 0.46, 0.27)
FLOOR_LINE = rgb(0.50, 0.34, 0.19)
TILE       = rgb(0.82, 0.81, 0.78)
STONE_TOP  = rgb(0.92, 0.90, 0.86)
WARM_LIGHT = rgb(1.0, 0.90, 0.62)


ROOF_PARTS = []


def _vec(p):
    return p if isinstance(p, vector) else vector(*p)


def block(pos, size, color, opacity=1.0, shininess=0.2, **extra):
    return box(pos=_vec(pos), size=_vec(size), color=color,
               opacity=opacity, shininess=shininess, **extra)


def rod(a, b, radius, color):
    a, b = _vec(a), _vec(b)
    return cylinder(pos=a, axis=b - a, radius=radius, color=color)


def blob(pos, size, color, shininess=0.05):
    return ellipsoid(pos=_vec(pos), size=_vec(size), color=color, shininess=shininess)


def leaf(start, end, width, thickness, color):
    start, end = _vec(start), _vec(end)
    axis = end - start
    return ellipsoid(pos=start + axis / 2, axis=axis, length=mag(axis),
                     height=thickness, width=width, color=color, shininess=0.1)


def jitter(value, amount):
    return value + random.uniform(-amount, amount)


def fblock(origin_x, origin_z, face, forward, y, side, size_fwd, size_up, size_side,
           color, opacity=1.0, shininess=0.15):
    face_x, face_z = face
    world_dx = face_x * forward - face_z * side
    world_dz = face_z * forward + face_x * side
    size = (size_fwd, size_up, size_side) if face_z == 0 else (size_side, size_up, size_fwd)
    return block((origin_x + world_dx, y, origin_z + world_dz), size, color, opacity, shininess)


def furniture_part(origin_x, origin_z, face, shininess=0.15):
    def part(forward, y, side, size_fwd, size_up, size_side, color):
        return fblock(origin_x, origin_z, face, forward, y, side,
                      size_fwd, size_up, size_side, color, shininess=shininess)
    return part


def build_ground():
    block((0, -0.22, 1.5), (44, 0.35, 36), LAWN, shininess=0.02)
    block((0, -0.08, -12.2), (44, 0.28, 7.0), ASPHALT, shininess=0.05)
    block((0, 0.01, -8.15), (44, 0.20, 1.0), rgb(0.74, 0.72, 0.67))
    block((0, 0.10, -4.05), (13.8, 0.20, 7.2), CONCRETE)
    block((0, 0.15, -7.78), (14.2, 0.28, 0.32), rgb(0.80, 0.78, 0.72))

    for x in range(-20, 21, 4):
        block((x, -0.06, -12.2), (1.6, 0.02, 0.14), rgb(0.92, 0.82, 0.30))
    for z in (-6.3, -2.4):
        block((0, 0.205, z), (13.6, 0.008, 0.02), JOINT_LINE)
    for x in (-5.7, 0, 5.7):
        block((x, 0.205, -4.0), (0.02, 0.008, 7.0), rgb(0.46, 0.45, 0.42))

    block((1.0, 0.12, -4.15), (2.8, 0.18, 0.75), rgb(0.74, 0.72, 0.66))
    block((1.0, 0.22, -4.55), (2.5, 0.12, 0.35), rgb(0.80, 0.78, 0.72))


def build_house_shell():
    block((-2.775, 2.05, 1.15), (0.15, 4.10, 8.0), WHITE, shininess=0.1)
    block((5.975, 2.05, 1.15), (0.15, 4.10, 8.0), WARM_WHITE)
    block((1.6, 2.05, 5.2), (8.9, 4.10, 0.2), WARM_WHITE)

    wall_z = -2.88
    block((-2.675, 2.05, wall_z), (0.35, 4.10, 0.20), WHITE)
    block((-1.65, 0.21, wall_z), (1.7, 0.42, 0.20), WHITE)
    block((-1.65, 3.535, wall_z), (1.7, 1.13, 0.20), WHITE)
    block((0.6, 2.05, wall_z), (2.8, 4.10, 0.20), WHITE)
    block((3.8, 0.19, wall_z), (3.6, 0.38, 0.20), WHITE)
    block((3.8, 3.60, wall_z), (3.6, 1.00, 0.20), WHITE)
    block((5.825, 2.05, wall_z), (0.45, 4.10, 0.20), WHITE)
    block((1.6, 0.12, -2.96), (9.0, 0.24, 0.20), rgb(0.35, 0.34, 0.32))
    block((3.55, 4.00, -2.95), (5.0, 0.55, 0.24), WHITE)

    block((0.65, 2.45, -2.93), (2.55, 4.85, 0.42), STONE)
    block((0.65, 4.55, -3.17), (2.55, 0.55, 0.18), rgb(0.80, 0.74, 0.62))
    for y in (0.48, 1.25, 2.05, 2.85, 3.65, 4.30):
        block((0.65, y, -3.151), (2.42, 0.014, 0.014), STONE_DARK)
    for x in (-0.35, 0.0, 1.0, 1.55):
        for y in (0.85, 2.45, 3.85):
            block((x, y, -3.153), (0.014, 0.72, 0.014), STONE_DARK)


def build_roofs():
    first_object = len(scene.objects)

    block((1.8, 4.28, 0.85), (9.8, 0.22, 9.0), CHARCOAL)
    block((1.8, 4.43, 0.92), (9.55, 0.10, 8.72), ROOF_MID)
    block((1.8, 4.52, 0.92), (9.15, 0.10, 8.35), rgb(0.86, 0.83, 0.74))
    block((1.8, 4.32, -3.62), (9.8, 0.25, 0.22), CHARCOAL)

    block((2.9, 5.02, 0.35), (8.8, 0.23, 8.6), CHARCOAL)
    block((2.9, 5.16, 0.38), (8.55, 0.10, 8.35), rgb(0.46, 0.44, 0.39))
    block((2.9, 5.24, 0.38), (8.25, 0.08, 8.05), rgb(0.88, 0.85, 0.76))
    block((2.9, 5.05, -3.95), (8.8, 0.25, 0.22), CHARCOAL)
    for x in (0.0, 3.0, 5.8):
        block((x, 4.65, -3.85), (0.10, 0.75, 0.10), CHARCOAL)

    ROOF_PARTS.extend(scene.objects[first_object:])


def build_carport():
    block((-5.15, 3.75, -0.10), (5.0, 0.20, 7.0), CHARCOAL)
    block((-5.15, 3.88, -0.10), (4.78, 0.09, 6.78), ROOF_MID)
    block((-5.15, 3.95, -0.10), (4.55, 0.07, 6.55), rgb(0.82, 0.78, 0.68))
    block((-5.15, 3.72, -3.05), (4.75, 0.18, 0.18), CHARCOAL)
    for x in (-7.45, -2.95):
        for z in (-2.9, 3.1):
            block((x, 1.9, z), (0.16, 3.8, 0.18), CHARCOAL)

    block((-5.15, 1.9, 3.3), (4.8, 3.8, 0.20), WARM_WHITE)
    block((-5.15, SLAB_TOP / 2, -0.10), (4.8, SLAB_TOP, 6.6), rgb(0.60, 0.59, 0.55))
    for z in (-2.0, 0.0, 2.0):
        block((-5.15, 0.215, z), (4.8, 0.006, 0.02), JOINT_LINE)
    block((-5.15, 0.215, -0.10), (0.02, 0.006, 6.6), JOINT_LINE)
    block((-5.2, 0.27, 2.55), (2.6, 0.12, 0.18), CONCRETE)

    block((-2.87, 1.85, 0.10), (0.04, 3.4, 5.1), WOOD_DARK)
    for i in range(18):
        block((-2.92, 1.85, -2.3 + i * 0.28), (0.06, 3.3, 0.16), WOOD_LIGHT)
    for z in (-1.0, 1.4):
        cylinder(pos=vector(-2.95, 2.9, z), axis=vector(-0.12, 0, 0), radius=0.07,
                 color=rgb(1.0, 0.86, 0.55), emissive=True)


def build_entrance():
    door_x, door_y, door_z = 0.65, 1.55, -3.205
    block((door_x, door_y, door_z), (1.42, 2.85, 0.12), WOOD_DARK, shininess=0.3)
    for y in (0.42, 0.78, 1.14, 1.50, 1.86, 2.22, 2.58):
        block((door_x, y, -3.274), (1.30, 0.018, 0.012), WOOD_LIGHT)
    for x in (0.15, 0.45, 0.82, 1.12):
        block((x, 1.55, -3.278), (0.012, 2.62, 0.012), rgb(0.40, 0.20, 0.09))

    block((1.60, 1.62, -3.22), (0.42, 2.78, 0.10), CHARCOAL)
    block((1.60, 1.62, -3.285), (0.32, 2.66, 0.025), GLASS, 0.75, 0.8)

    cylinder(pos=vector(1.12, 1.55, -3.31), axis=vector(0, 0.22, 0), radius=0.025, color=BRASS)
    sphere(pos=vector(1.12, 1.44, -3.32), radius=0.045, color=BRASS)
    block((0.9, 0.10, -3.28), (2.1, 0.12, 0.55), rgb(0.60, 0.58, 0.52))


def front_window(center_x, width, height, sill, z=-2.95):
    center_y = sill + height / 2
    block((center_x, center_y, z), (width - 0.06, height - 0.06, 0.02),
          rgb(0.55, 0.72, 0.80), 0.22, 0.9)
    block((center_x - width * 0.25, center_y, z - 0.012),
          (width * 0.10, height - 0.2, 0.01), GLASS_HI, 0.16)
    for x in (center_x - width / 2 + 0.03, center_x + width / 2 - 0.03):
        block((x, center_y, z), (0.07, height, 0.12), CHARCOAL)
    for y in (sill + 0.03, sill + height - 0.03):
        block((center_x, y, z), (width, 0.07, 0.12), CHARCOAL)
    for direction in (-1, 1):
        block((center_x + direction * width / 6, center_y, z), (0.035, height, 0.08), CHARCOAL)


def build_windows():
    front_window(-1.65, 1.7, 2.55, 0.42)
    front_window(3.8, 3.6, 2.72, 0.38)
    for x in (2.2, 2.5, 5.1, 5.4):
        block((x, 1.75, -2.62), (0.08, 2.5, 0.03), rgb(0.88, 0.88, 0.84), 0.55)


def build_car():
    cx, cz = -5.2, -0.3
    body_width, body_length = 3.0, 4.7
    front, rear = cz - body_length / 2, cz + body_length / 2
    first_object = len(scene.objects)

    paint = rgb(0.72, 0.07, 0.08)
    paint_dark = rgb(0.45, 0.03, 0.05)
    glass = rgb(0.12, 0.24, 0.30)
    black = rgb(0.03, 0.03, 0.035)
    chrome = rgb(0.82, 0.84, 0.86)

    block((cx, 0.62, cz), (body_width - 0.1, 0.30, body_length - 0.3), black)
    block((cx, 0.98, cz), (body_width, 0.62, body_length), paint, shininess=0.8)
    block((cx, 1.43, cz), (body_width - 0.08, 0.28, body_length - 0.1), paint, shininess=0.8)
    block((cx, 1.62, cz - 1.45), (body_width - 0.30, 0.12, 1.7), paint, shininess=0.8)
    for x in (cx - 0.55, cx + 0.55):
        block((x, 1.685, cz - 1.45), (0.03, 0.01, 1.5), paint_dark)
    block((cx, 1.62, rear - 0.55), (body_width - 0.30, 0.12, 1.0), paint, shininess=0.8)

    block((cx, 1.90, cz + 0.4), (2.4, 0.62, 2.0), rgb(0.05, 0.09, 0.11))
    windshield = block((cx, 1.88, cz - 0.85), (2.4, 0.82, 0.06), glass, 0.92, 0.9)
    windshield.rotate(angle=0.68, axis=vector(1, 0, 0))
    rear_glass = block((cx, 1.88, cz + 1.65), (2.3, 0.78, 0.06), glass, 0.92, 0.9)
    rear_glass.rotate(angle=-0.55, axis=vector(1, 0, 0))
    block((cx, 2.26, cz + 0.45), (2.5, 0.09, 2.2), paint, shininess=0.8)

    for side in (-1, 1):
        glass_x = cx + side * 1.21
        for z in (cz - 0.10, cz + 0.88):
            block((glass_x, 1.90, z), (0.03, 0.52, 0.80), glass, 0.9, 0.9)
        for z in (cz - 0.58, cz + 0.39, cz + 1.38):
            block((glass_x, 1.90, z), (0.07, 0.56, 0.11), paint_dark)
        block((cx + side * 1.505, 1.30, cz), (0.02, 0.035, body_length - 0.4), chrome)
        for z in (cz - 0.55, cz + 0.45):
            block((cx + side * 1.505, 0.98, z), (0.02, 0.60, 0.02), black)
        for z in (cz - 0.40, cz + 0.60):
            block((cx + side * 1.52, 1.32, z), (0.03, 0.05, 0.28), chrome)
        rod((cx + side * 1.40, 1.62, cz - 0.62), (cx + side * 1.58, 1.74, cz - 0.62), 0.03, black)
        ellipsoid(pos=vector(cx + side * 1.66, 1.78, cz - 0.62),
                  size=vector(0.22, 0.20, 0.34), color=paint, shininess=0.8)
    for x in (cx - 0.9, cx + 0.9):
        block((x, 2.34, cz + 0.45), (0.06, 0.07, 1.9), rgb(0.35, 0.36, 0.37))

    for side in (-1, 1):
        for z in (cz - 1.5, cz + 1.5):
            cylinder(pos=vector(cx + side * 1.10, 0.52, z), axis=vector(side * 0.42, 0, 0),
                     radius=0.60, color=black)
            cylinder(pos=vector(cx + side * 1.18, 0.48, z), axis=vector(side * 0.38, 0, 0),
                     radius=0.46, color=rgb(0.05, 0.05, 0.055))
            cylinder(pos=vector(cx + side * 1.55, 0.48, z), axis=vector(side * 0.03, 0, 0),
                     radius=0.31, color=rgb(0.70, 0.72, 0.74), shininess=0.9)
            cylinder(pos=vector(cx + side * 1.58, 0.48, z), axis=vector(side * 0.02, 0, 0),
                     radius=0.09, color=rgb(0.20, 0.21, 0.22))
            for spoke in range(5):
                angle = 2 * math.pi * spoke / 5
                cylinder(pos=vector(cx + side * 1.59, 0.48 + 0.19 * math.sin(angle),
                                    z + 0.19 * math.cos(angle)),
                         axis=vector(side * 0.012, 0, 0), radius=0.045,
                         color=rgb(0.88, 0.89, 0.90))

    block((cx, 0.70, front + 0.02), (body_width + 0.04, 0.42, 0.16), paint_dark, shininess=0.7)
    block((cx, 1.18, front - 0.01), (1.35, 0.34, 0.05), chrome)
    block((cx, 1.18, front - 0.04), (1.20, 0.26, 0.04), black)
    for slat in range(4):
        block((cx, 1.09 + slat * 0.07, front - 0.065), (1.15, 0.015, 0.02), chrome)
    block((cx, 0.75, front - 0.07), (1.9, 0.20, 0.04), black)
    block((cx, 0.52, front - 0.07), (0.52, 0.15, 0.03), rgb(0.92, 0.92, 0.88))
    for side in (-1, 1):
        lamp_x = cx + side * 1.05
        block((lamp_x, 1.40, front + 0.02), (0.66, 0.24, 0.10), rgb(0.96, 0.96, 0.88))
        block((lamp_x, 1.40, front - 0.035), (0.50, 0.14, 0.02), rgb(1.0, 0.98, 0.80), shininess=0.9)
        block((lamp_x, 0.74, front - 0.07), (0.26, 0.13, 0.04), rgb(0.95, 0.90, 0.60))
        block((lamp_x, 1.38, rear - 0.02), (0.62, 0.24, 0.08), rgb(0.80, 0.05, 0.04))
    block((cx, 0.70, rear), (body_width + 0.04, 0.42, 0.16), paint_dark)

    for part in scene.objects[first_object:]:
        part.pos.y += SLAB_TOP


def planting_beds():
    block((4.05, 0.20, -3.65), (4.2, 0.18, 1.2), SOIL)
    block((-2.9, 0.20, -3.55), (2.2, 0.18, 1.0), SOIL)


def ornamental_plant(x, z, scale=1.0, base=0.22):
    for i in range(12):
        angle = 2 * math.pi * i / 12 + random.uniform(-0.12, 0.12)
        length = random.uniform(0.65, 1.25) * scale
        rise = random.uniform(0.45, 1.0) * scale
        start = (x, base, z)
        end = (x + math.cos(angle) * length, base + rise, z + math.sin(angle) * length)
        rod(start, end, 0.016 * scale, rgb(0.22, 0.42, 0.14))
        leaf(start, end, 0.17 * scale, 0.04 * scale, random.choice(GREENS))
    sphere(pos=vector(x, base + 0.2 * scale, z), radius=0.16 * scale, color=GREENS[1])


def shrub(x, z, scale=1.0):
    for _ in range(8):
        blob((x + jitter(0, 0.38 * scale), 0.42 + random.uniform(0, 0.38) * scale,
              z + jitter(0, 0.32 * scale)),
             (0.58 * scale, 0.50 * scale, 0.58 * scale), random.choice(GREENS))


def clipped_bush(x, z):
    for _ in range(4):
        blob((jitter(x, 0.18), 0.35 + random.uniform(0, 0.18), jitter(z, 0.15)),
             (0.38, 0.40, 0.38), random.choice(GREENS))


def garden_light(x, z):
    cylinder(pos=vector(x, 0.22, z), axis=vector(0, 0.42, 0), radius=0.045, color=CHARCOAL)
    cylinder(pos=vector(x, 0.64, z), axis=vector(0, 0.07, 0), radius=0.12,
             color=rgb(0.90, 0.80, 0.52), emissive=True)
    sphere(pos=vector(x, 0.70, z), radius=0.075, color=rgb(1.0, 0.86, 0.55), emissive=True)


def build_garden():
    planting_beds()
    for x, z, scale in [(2.3, -3.8, 0.95), (3.5, -3.95, 1.1), (4.7, -3.9, 1.05),
                        (5.7, -3.4, 1.0), (-3.7, -3.7, 0.85), (-1.9, -3.9, 0.7),
                        (6.9, -1.6, 1.0), (7.6, 0.3, 1.1), (-8.0, -0.7, 1.0)]:
        ornamental_plant(x, z, scale)
    for x, z, scale in [(2.0, -4.1, 0.9), (5.2, -4.1, 0.9), (7.2, -2.2, 1.1),
                        (-7.0, -1.0, 1.1), (-3.9, -4.0, 0.8), (7.4, 1.8, 1.2)]:
        shrub(x, z, scale)
    for x, z in [(-0.15, -4.5), (1.7, -4.55), (2.7, -4.65), (5.9, -4.2)]:
        clipped_bush(x, z)
    for x, z in [(-0.2, -5.4), (1.6, -5.45), (3.0, -5.35), (5.5, -4.8), (-6.8, -4.4)]:
        garden_light(x, z)


_tree_parts = []


def _add(piece):
    _tree_parts.append(piece)
    return piece


def _finish_tree():
    if _tree_parts:
        compound(list(_tree_parts))
        _tree_parts.clear()


def taper(a, b, radius_start, radius_end, color=BARK):
    direction = b - a
    steps = max(2, int(mag(direction) * 2.5))
    for i in range(steps):
        t0, t1 = i / steps, (i + 1) / steps
        p0, p1 = a + direction * t0, a + direction * t1
        radius_mid = radius_start + (radius_end - radius_start) * (t0 + t1) / 2
        _add(cylinder(pos=p0, axis=p1 - p0, radius=radius_mid, color=color, shininess=0.0))
        radius_at_end = radius_start + (radius_end - radius_start) * t1
        if radius_at_end > 0.07:
            _add(sphere(pos=p1, radius=radius_at_end, color=color, shininess=0.0))


def foliage(center, size, count, canopy_bottom, canopy_height):
    for _ in range(count):
        ox, oy, oz = (random.uniform(-1, 1) for _ in range(3))
        if ox * ox + oy * oy + oz * oz > 1:
            continue
        y = center.y + oy * size * 0.75
        shade = int((y - canopy_bottom) / canopy_height * 4 + random.uniform(-0.8, 0.8))
        color = GREENS[max(0, min(3, shade))] * random.uniform(0.85, 1.10)
        leaf_size = random.uniform(0.55, 0.95) * size * 0.75
        _add(blob((center.x + ox * size, y, center.z + oz * size),
                  (leaf_size * 1.2, leaf_size * 0.8, leaf_size * 1.2), color, shininess=0.0))


def branch(start, direction, length, radius, depth, scale):
    direction = norm(direction)
    end = start + direction * length
    taper(start, end, radius, radius * 0.68)
    if depth == 0:
        foliage(end, 1.25 * scale, 10, 4.5 * scale, 6.5 * scale)
        return
    for _ in range(random.choice([2, 3])):
        new_direction = direction + vector(random.uniform(-0.8, 0.8), random.uniform(0.0, 0.7),
                                           random.uniform(-0.8, 0.8))
        branch(end, new_direction, length * 0.78, radius * 0.65, depth - 1, scale)


def build_tree(tx, tz, scale=1.0):
    for i in range(6):
        angle = 2 * math.pi * i / 6 + random.uniform(-0.2, 0.2)
        taper(vector(tx + math.cos(angle) * 0.2 * scale, 0.55 * scale,
                     tz + math.sin(angle) * 0.2 * scale),
              vector(tx + math.cos(angle) * 0.95 * scale, 0.0,
                     tz + math.sin(angle) * 0.95 * scale),
              0.20 * scale, 0.05 * scale, BARK_DARK)

    trunk_offsets = [(0, 0, 0), (0.12, 1.3, 0.05), (0.02, 2.6, 0.20),
                     (-0.10, 3.8, 0.10), (-0.05, 4.6, 0)]
    trunk = [vector(tx + dx * scale, dy * scale, tz + dz * scale) for dx, dy, dz in trunk_offsets]
    trunk_radii = [0.50 * scale, 0.40 * scale, 0.32 * scale, 0.26 * scale, 0.22 * scale]
    for i in range(len(trunk) - 1):
        taper(trunk[i], trunk[i + 1], trunk_radii[i], trunk_radii[i + 1],
              BARK if i % 2 == 0 else rgb(0.40, 0.27, 0.16))
    for y in (0.5, 1.2, 1.9, 2.6, 3.3):
        for _ in range(4):
            angle = random.uniform(0, 2 * math.pi)
            ridge_radius = (0.46 - y * 0.05) * scale
            _add(rod((tx + math.cos(angle) * ridge_radius, y * scale,
                      tz + math.sin(angle) * ridge_radius),
                     (tx + math.cos(angle) * ridge_radius, (y + 0.6) * scale,
                      tz + math.sin(angle) * ridge_radius),
                     0.03 * scale, BARK_DARK))

    for y, angle in ((2.9, 0.8), (3.4, 3.6), (3.9, 5.4)):
        branch(vector(tx, y * scale, tz + 0.1 * scale),
               vector(math.cos(angle), 0.7, math.sin(angle)), 1.5 * scale, 0.11 * scale, 1, scale)
    top = trunk[-1]
    for i in range(5):
        angle = 2 * math.pi * i / 5 + random.uniform(-0.3, 0.3)
        branch(top, vector(math.cos(angle), random.uniform(0.9, 1.3), math.sin(angle)),
               1.6 * scale, 0.17 * scale, 2, scale)
    foliage(vector(tx, 6.4 * scale, tz), 2.6 * scale, 60, 4.5 * scale, 6.5 * scale)

    _add(cylinder(pos=vector(tx, 0.0, tz), axis=vector(0, 0.03, 0), radius=1.6 * scale,
                  color=rgb(0.17, 0.33, 0.12)))
    for _ in range(30):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.5, 2.3) * scale
        _add(blob((tx + math.cos(angle) * distance, 0.05, tz + math.sin(angle) * distance),
                  (0.25, 0.04, 0.16),
                  random.choice([rgb(0.55, 0.42, 0.14), rgb(0.40, 0.30, 0.10), GREENS[0]]),
                  shininess=0.0))
    _finish_tree()


def _palm_frond(top, angle, length, arch, color):
    dx, dz = math.cos(angle), math.sin(angle)
    across_x, across_z = -dz, dx
    segments = 13
    previous = top
    for i in range(1, segments + 1):
        t = i / segments
        point = top + vector(dx * length * t,
                             length * (arch * t - 1.3 * t * t),
                             dz * length * t)
        _add(cylinder(pos=previous, axis=point - previous, radius=max(0.008, 0.03 * (1.1 - t)),
                      color=rgb(0.30, 0.38, 0.14), shininess=0.0))
        leaflet_length = 0.9 * math.sin(math.pi * (0.15 + 0.85 * t))
        if leaflet_length > 0.08:
            for side in (-1, 1):
                tip = point + vector((across_x * side * 0.85 + dx * 0.35) * leaflet_length,
                                     -0.45 * leaflet_length,
                                     (across_z * side * 0.85 + dz * 0.35) * leaflet_length)
                _add(leaf(point, tip, 0.11, 0.012, color * random.uniform(0.85, 1.12)))
        previous = point


def build_palm(x, z, height=5.5, lean=0.6, lean_angle=0.0):
    segments = 9
    lean_x, lean_z = math.cos(lean_angle) * lean, math.sin(lean_angle) * lean
    points = []
    for i in range(segments + 1):
        t = i / segments
        points.append(vector(x + lean_x * t * t * height * 0.35, height * t,
                             z + lean_z * t * t * height * 0.35))
    for i in range(segments):
        radius = 0.24 - 0.10 * (i + 0.5) / segments + (0.015 if i % 2 == 0 else 0.0)
        color = rgb(0.46, 0.36, 0.26) if i % 2 == 0 else rgb(0.38, 0.29, 0.20)
        _add(cylinder(pos=points[i], axis=points[i + 1] - points[i], radius=radius,
                      color=color, shininess=0.0))

    top = points[-1]
    palm_greens = [rgb(0.10, 0.42, 0.14), rgb(0.18, 0.55, 0.18), rgb(0.28, 0.62, 0.20)]
    _add(sphere(pos=top, radius=0.24, color=rgb(0.30, 0.34, 0.14), shininess=0.0))

    for k in range(9):
        angle = 2 * math.pi * k / 9 + random.uniform(-0.15, 0.15)
        _palm_frond(top, angle, random.uniform(2.1, 2.7), random.uniform(0.9, 1.3),
                    random.choice(palm_greens))
    for k in range(5):
        angle = 2 * math.pi * (k + 0.5) / 5 + random.uniform(-0.2, 0.2)
        _palm_frond(top, angle, random.uniform(2.2, 2.6), random.uniform(0.15, 0.35),
                    random.choice(palm_greens) * 0.85)
    for _ in range(2):
        lean_to = vector(random.uniform(-0.2, 0.2), 1.0, random.uniform(-0.2, 0.2))
        _add(leaf(top, top + lean_to * 1.1, 0.12, 0.05, palm_greens[2]))

    for k in range(4):
        angle = 2 * math.pi * k / 4
        _add(sphere(pos=top + vector(math.cos(angle) * 0.22, -0.30, math.sin(angle) * 0.22),
                    radius=0.13, color=rgb(0.36, 0.30, 0.12), shininess=0.0))
    _finish_tree()


def build_trees():
    for tx, tz, scale in [(-10.0, 1.0, 1.0), (11.5, 3.2, 1.0), (-17.0, 5.0, 1.1),
                          (16.5, -1.5, 1.0), (-4.5, 11.0, 1.15), (4.0, 12.5, 1.0),
                          (14.0, 9.5, 1.2), (-12.0, 12.0, 1.0)]:
        build_tree(tx, tz, scale)
    for x, z, height, lean, lean_angle in [(8.8, -4.8, 6.0, 0.7, 0.5), (-9.4, -5.4, 5.5, 0.6, 2.6),
                                           (11.4, -5.6, 5.0, 0.5, 1.2), (-12.0, -3.4, 6.2, 0.7, 4.0)]:
        build_palm(x, z, height, lean, lean_angle)


def fence_run(x0, z0, x1, z1):
    along_x = abs(x1 - x0) > abs(z1 - z0)
    length = abs(x1 - x0) if along_x else abs(z1 - z0)

    def at(distance, y, offset=0.0):
        return (x0 + distance, y, z0 + offset) if along_x else (x0 + offset, y, z0 + distance)

    def size(along, up, across):
        return (along, up, across) if along_x else (across, up, along)

    tones = [rgb(0.62, 0.42, 0.24), rgb(0.56, 0.37, 0.20), rgb(0.68, 0.48, 0.28)]
    parts = []
    for y in (0.40, 1.00):
        parts.append(block(at(length / 2, y, 0.07), size(length, 0.08, 0.05), WOOD_DARK))
    post_count = max(2, round(length / 3) + 1)
    for i in range(post_count):
        distance = length * i / (post_count - 1)
        parts.append(block(at(distance, 0.85), size(0.14, 1.7, 0.14), WOOD_DARK))
        parts.append(block(at(distance, 1.74), size(0.20, 0.05, 0.20), rgb(0.30, 0.19, 0.10)))
    for i in range(int(length / 0.19)):
        distance = 0.10 + i * 0.19
        picket_height = 1.3 + random.uniform(-0.04, 0.04)
        color = random.choice(tones)
        parts.append(block(at(distance, picket_height / 2), size(0.12, picket_height, 0.03),
                           color, shininess=0.1))
        tip = block(at(distance, picket_height), size(0.085, 0.085, 0.03), color,
                    shininess=0.1)
        tip.rotate(angle=math.pi / 4, axis=vector(0, 0, 1) if along_x else vector(1, 0, 0))
        parts.append(tip)
    compound(parts)


def build_fence():
    fence_run(-13.5, 6.5, 13.5, 6.5)
    fence_run(-13.5, -7.0, -13.5, 6.5)
    fence_run(13.5, -7.0, 13.5, 6.5)


def rug(x, z, size_x, size_z, base=rgb(0.88, 0.82, 0.70), accent=rgb(0.72, 0.38, 0.27)):
    block((x, FLOOR + 0.010, z), (size_x, 0.02, size_z), base)
    block((x, FLOOR + 0.014, z), (size_x - 0.35, 0.02, size_z - 0.35), accent)
    block((x, FLOOR + 0.018, z), (size_x - 0.80, 0.02, size_z - 0.80), base)


def wall_art(x, y, z, face, width, height):
    fblock(x, z, face, 0.0, y, 0, 0.05, height, width, rgb(0.10, 0.09, 0.08))
    fblock(x, z, face, 0.03, y, 0, 0.02, height - 0.1, width - 0.1, rgb(0.95, 0.92, 0.84))
    shapes = [rgb(0.20, 0.40, 0.52), rgb(0.85, 0.55, 0.20), rgb(0.55, 0.25, 0.22)]
    for i, color in enumerate(shapes):
        fblock(x, z, face, 0.045, y + (i - 1) * height * 0.18, (i - 1) * width * 0.18,
               0.02, height * 0.28, width * 0.34, color)


def indoor_plant(x, z, scale=1.0, base=FLOOR):
    cylinder(pos=vector(x, base, z), axis=vector(0, 0.45 * scale, 0),
             radius=0.22 * scale, color=TERRACOTTA)
    cylinder(pos=vector(x, base + 0.44 * scale, z), axis=vector(0, 0.02, 0),
             radius=0.20 * scale, color=SOIL)
    for _ in range(10):
        angle = random.uniform(0, 2 * math.pi)
        reach = random.uniform(0.35, 0.65) * scale
        rise = random.uniform(0.8, 1.35) * scale
        leaf((x, base + 0.45 * scale, z),
             (x + math.cos(angle) * reach, base + rise, z + math.sin(angle) * reach),
             0.22 * scale, 0.04 * scale, random.choice(GREENS))


def floor_lamp(x, z):
    cylinder(pos=vector(x, FLOOR, z), axis=vector(0, 0.04, 0), radius=0.18, color=CHARCOAL)
    rod((x, FLOOR, z), (x, FLOOR + 1.5, z), 0.02, CHARCOAL)
    cylinder(pos=vector(x, FLOOR + 1.4, z), axis=vector(0, 0.35, 0), radius=0.22,
             color=WARM_LIGHT, emissive=True)


def pendant(x, z, bottom_y=FLOOR + 2.0):
    rod((x, CEILING, z), (x, bottom_y + 0.25, z), 0.008, CHARCOAL)
    cylinder(pos=vector(x, bottom_y, z), axis=vector(0, 0.25, 0), radius=0.17,
             color=BRASS, shininess=0.6)
    sphere(pos=vector(x, bottom_y + 0.02, z), radius=0.09, color=WARM_LIGHT, emissive=True)


def sofa(origin_x, origin_z, face, length=2.8):
    fabric, dark = rgb(0.30, 0.47, 0.54), rgb(0.19, 0.32, 0.38)
    mustard, coral = rgb(0.86, 0.64, 0.18), rgb(0.85, 0.36, 0.28)
    part = furniture_part(origin_x, origin_z, face, shininess=0.05)

    seats = 3
    inner_length = length - 0.5
    seat_width = inner_length / seats
    part(0, FLOOR + 0.25, 0, 1.0, 0.30, length, dark)
    for i in range(seats):
        side = -inner_length / 2 + seat_width * (i + 0.5)
        part(0.08, FLOOR + 0.49, side, 0.82, 0.18, seat_width - 0.04, fabric)
        part(-0.30, FLOOR + 0.82, side, 0.22, 0.50, seat_width - 0.06, fabric)
    part(-0.42, FLOOR + 0.66, 0, 0.16, 0.62, length, dark)
    for end in (-1, 1):
        part(0, FLOOR + 0.45, end * (length / 2 - 0.12), 1.0, 0.50, 0.24, dark)
        for forward in (-0.42, 0.42):
            part(forward, FLOOR + 0.05, end * (length / 2 - 0.1), 0.08, 0.10, 0.08, WOOD_DARK)
    part(-0.12, FLOOR + 0.78, -inner_length / 2 + 0.2, 0.14, 0.36, 0.36, mustard)
    part(-0.12, FLOOR + 0.78, inner_length / 2 - 0.2, 0.14, 0.36, 0.36, coral)


def armchair(origin_x, origin_z, face, color=rgb(0.78, 0.50, 0.22)):
    dark = color * 0.7
    part = furniture_part(origin_x, origin_z, face, shininess=0.05)

    part(0, FLOOR + 0.25, 0, 0.85, 0.28, 0.85, dark)
    part(0.06, FLOOR + 0.46, 0, 0.68, 0.16, 0.64, color)
    part(-0.34, FLOOR + 0.70, 0, 0.16, 0.66, 0.85, color)
    for end in (-1, 1):
        part(0, FLOOR + 0.42, end * 0.38, 0.85, 0.40, 0.14, dark)
        for forward in (-0.35, 0.35):
            part(forward, FLOOR + 0.05, end * 0.35, 0.07, 0.10, 0.07, WOOD_DARK)


def dining_chair(origin_x, origin_z, face):
    wood, cushion = rgb(0.55, 0.36, 0.20), rgb(0.82, 0.78, 0.68)
    part = furniture_part(origin_x, origin_z, face)

    part(0, FLOOR + 0.45, 0, 0.46, 0.05, 0.46, wood)
    part(0, FLOOR + 0.485, 0, 0.40, 0.03, 0.40, cushion)
    part(-0.21, FLOOR + 0.75, 0, 0.04, 0.50, 0.44, wood)
    for forward in (-0.19, 0.19):
        for side in (-0.19, 0.19):
            part(forward, FLOOR + 0.21, side, 0.05, 0.42, 0.05, wood)


def coffee_table(x, z):
    wood = rgb(0.52, 0.34, 0.19)
    block((x, FLOOR + 0.40, z), (0.8, 0.05, 1.5), wood, shininess=0.4)
    block((x, FLOOR + 0.15, z), (0.65, 0.03, 1.3), rgb(0.40, 0.26, 0.14))
    for sx in (-1, 1):
        for sz in (-1, 1):
            block((x + sx * 0.34, FLOOR + 0.20, z + sz * 0.68), (0.05, 0.40, 0.05), wood)

    cylinder(pos=vector(x, FLOOR + 0.425, z - 0.4), axis=vector(0, 0.28, 0), radius=0.07,
             color=rgb(0.20, 0.50, 0.55), shininess=0.6)
    for _ in range(4):
        angle = random.uniform(0, 2 * math.pi)
        leaf((x, FLOOR + 0.70, z - 0.4),
             (x + math.cos(angle) * 0.25, FLOOR + 1.0, z - 0.4 + math.sin(angle) * 0.25),
             0.12, 0.03, random.choice(GREENS))
    block((x, FLOOR + 0.45, z + 0.3), (0.32, 0.04, 0.42), rgb(0.80, 0.30, 0.25))
    block((x, FLOOR + 0.49, z + 0.3), (0.28, 0.04, 0.38), rgb(0.25, 0.40, 0.55))
    block((x, FLOOR + 0.53, z + 0.3), (0.24, 0.04, 0.34), rgb(0.90, 0.80, 0.55))


def dining_table(x, z, width=1.0, depth=2.0):
    wood = rgb(0.50, 0.32, 0.17)
    block((x, FLOOR + 0.74, z), (width, 0.06, depth), wood, shininess=0.4)
    block((x, FLOOR + 0.69, z), (width - 0.1, 0.05, depth - 0.1), rgb(0.35, 0.22, 0.12))
    for sx in (-1, 1):
        for sz in (-1, 1):
            block((x + sx * (width / 2 - 0.07), FLOOR + 0.355, z + sz * (depth / 2 - 0.07)),
                  (0.08, 0.71, 0.08), wood)
    block((x, FLOOR + 0.775, z), (0.25, 0.01, 1.4), rgb(0.85, 0.80, 0.70))
    cylinder(pos=vector(x, FLOOR + 0.78, z), axis=vector(0, 0.08, 0), radius=0.18, color=WHITE)
    for dx, dz, color in ((0.0, 0.0, rgb(0.95, 0.55, 0.12)),
                          (0.08, 0.06, rgb(0.80, 0.15, 0.12)),
                          (-0.07, 0.05, rgb(0.55, 0.78, 0.20))):
        sphere(pos=vector(x + dx, FLOOR + 0.88, z + dz), radius=0.06, color=color)


def bookshelf(x, z, length=1.4, height=2.1):
    wood = rgb(0.45, 0.29, 0.16)
    book_colors = [rgb(0.70, 0.20, 0.18), rgb(0.20, 0.35, 0.55), rgb(0.85, 0.70, 0.30),
                   rgb(0.25, 0.50, 0.35), rgb(0.85, 0.82, 0.75), rgb(0.40, 0.25, 0.45)]
    block((x + 0.17, FLOOR + height / 2, z), (0.04, height, length), wood)
    for end in (-1, 1):
        block((x, FLOOR + height / 2, z + end * (length / 2 - 0.02)), (0.34, height, 0.04), wood)

    levels = 5
    spacing = (height - 0.06) / (levels - 1)
    for level in range(levels):
        y = FLOOR + 0.03 + level * spacing
        block((x, y, z), (0.34, 0.03, length), wood)
        if level == levels - 1:
            continue
        book_z = z - length / 2 + 0.07
        while book_z < z + length / 2 - 0.12:
            book_width = random.uniform(0.04, 0.08)
            book_height = random.uniform(0.22, 0.34)
            if random.random() < 0.08:
                book_z += 0.12
                continue
            block((x + 0.03, y + 0.015 + book_height / 2, book_z + book_width / 2),
                  (0.22, book_height, book_width), random.choice(book_colors))
            book_z += book_width + 0.01


def nightstand(x, z):
    block((x, FLOOR + 0.225, z), (0.42, 0.45, 0.42), rgb(0.45, 0.29, 0.16))
    block((x + 0.215, FLOOR + 0.28, z), (0.01, 0.01, 0.30), rgb(0.25, 0.15, 0.08))
    cylinder(pos=vector(x, FLOOR + 0.45, z), axis=vector(0, 0.20, 0), radius=0.05,
             color=rgb(0.85, 0.80, 0.70))
    cylinder(pos=vector(x, FLOOR + 0.62, z), axis=vector(0, 0.20, 0), radius=0.13,
             color=WARM_LIGHT, emissive=True)


def bed(origin_x, origin_z, face):
    frame, sheet = rgb(0.45, 0.28, 0.15), rgb(0.92, 0.92, 0.88)
    blanket = rgb(0.25, 0.42, 0.55)
    part = furniture_part(origin_x, origin_z, face, shininess=0.05)

    part(0, FLOOR + 0.20, 0, 2.0, 0.28, 1.5, frame)
    part(0, FLOOR + 0.42, 0, 1.96, 0.16, 1.46, sheet)
    part(0.35, FLOOR + 0.52, 0, 1.25, 0.06, 1.48, blanket)
    part(-0.25, FLOOR + 0.535, 0, 0.12, 0.07, 1.48, rgb(0.85, 0.60, 0.25))
    part(-1.02, FLOOR + 0.62, 0, 0.08, 0.90, 1.6, frame)
    for side in (-0.38, 0.38):
        part(-0.72, FLOOR + 0.56, side, 0.38, 0.12, 0.58, WHITE)


def build_floor_and_ceiling():
    block((1.6, 0.14, 1.16), (8.6, 0.22, 7.9), FLOOR_WOOD, shininess=0.35)
    for i in range(16):
        block((1.6, FLOOR + 0.002, -2.45 + 0.5 * i), (8.6, 0.004, 0.012), FLOOR_LINE)
    block((0.0, FLOOR + 0.004, 4.3), (5.4, 0.008, 1.6), TILE)

    first_object = len(scene.objects)
    block((1.6, 4.12, 1.16), (8.6, 0.06, 7.9), WHITE, shininess=0.05)
    for x in (-1.5, 0.8, 3.1, 5.0):
        for z in (-1.8, 0.4, 2.6, 4.4):
            cylinder(pos=vector(x, 4.088, z), axis=vector(0, -0.012, 0), radius=0.11,
                     color=rgb(1.0, 0.96, 0.85), emissive=True)
    ROOF_PARTS.extend(scene.objects[first_object:])


def build_partitions():
    wall_height = CEILING - FLOOR
    wall_y = FLOOR + wall_height / 2
    block((-0.25, wall_y, -1.0), (0.10, wall_height, 3.5), WHITE)
    block((-2.2, wall_y, 0.70), (1.0, wall_height, 0.10), WHITE)
    block((-0.55, wall_y, 0.70), (0.7, wall_height, 0.10), WHITE)
    block((-1.3, (2.15 + CEILING) / 2, 0.70), (0.8, CEILING - 2.15, 0.10), WHITE)
    for x in (-1.7, -0.9):
        block((x, FLOOR + 0.95, 0.70), (0.05, 1.9, 0.14), CHARCOAL)


def tv_wall():
    wood = rgb(0.35, 0.22, 0.12)
    block((5.86, FLOOR + 1.6, -1.0), (0.04, 2.4, 3.6), wood)
    for i in range(12):
        block((5.84, FLOOR + 1.6, -2.65 + i * 0.3), (0.02, 2.4, 0.02), rgb(0.22, 0.13, 0.07))

    block((5.80, FLOOR + 1.45, -1.0), (0.06, 1.0, 1.8), rgb(0.03, 0.03, 0.035))
    block((5.765, FLOOR + 1.45, -1.0), (0.02, 0.9, 1.65), rgb(0.12, 0.34, 0.60), emissive=True)
    block((5.755, FLOOR + 1.22, -1.0), (0.01, 0.30, 1.65), rgb(0.13, 0.50, 0.22), emissive=True)
    sphere(pos=vector(5.75, FLOOR + 1.70, -0.45), radius=0.09, color=rgb(1.0, 0.92, 0.45),
           emissive=True)

    block((5.55, FLOOR + 0.27, -1.0), (0.5, 0.4, 2.4), rgb(0.30, 0.19, 0.10), shininess=0.3)
    for z in (-2.0, 0.0):
        block((5.55, FLOOR + 0.85, z), (0.28, 0.70, 0.28), rgb(0.08, 0.08, 0.09))
    block((5.55, FLOOR + 0.50, -1.0), (0.30, 0.04, 0.60), rgb(0.85, 0.80, 0.70))
    cylinder(pos=vector(5.55, FLOOR + 0.52, -1.0), axis=vector(0, 0.14, 0), radius=0.08,
             color=rgb(0.78, 0.55, 0.20), shininess=0.6)


def build_living_room():
    rug(4.0, -1.0, 3.4, 3.2)
    sofa(2.75, -1.0, (1, 0))
    coffee_table(4.1, -1.0)
    armchair(4.3, 0.75, (0, -1))
    armchair(4.3, -2.55, (0, 1), rgb(0.35, 0.55, 0.50))
    tv_wall()
    bookshelf(5.7, 1.5)
    floor_lamp(2.3, 0.95)
    indoor_plant(1.6, -2.45, 1.2)
    indoor_plant(5.55, -2.55, 0.9)
    wall_art(-0.19, FLOOR + 1.9, -1.0, (1, 0), 1.6, 1.0)


def build_dining_room():
    dining_table(4.3, 3.4)
    for z in (2.75, 3.4, 4.05):
        dining_chair(3.5, z, (1, 0))
        dining_chair(5.1, z, (-1, 0))
    pendant(4.3, 2.9)
    pendant(4.3, 3.9)

    block((4.1, FLOOR + 0.40, 4.8), (1.9, 0.80, 0.50), rgb(0.42, 0.27, 0.15), shininess=0.3)
    block((4.1, FLOOR + 0.82, 4.8), (1.95, 0.04, 0.54), rgb(0.30, 0.19, 0.10))
    wall_art(4.1, FLOOR + 1.8, 5.08, (0, -1), 1.5, 0.9)
    cylinder(pos=vector(3.5, FLOOR + 0.84, 4.8), axis=vector(0, 0.22, 0), radius=0.07,
             color=rgb(0.85, 0.80, 0.70))
    cylinder(pos=vector(3.5, FLOOR + 1.04, 4.8), axis=vector(0, 0.2, 0), radius=0.14,
             color=WARM_LIGHT, emissive=True)
    cylinder(pos=vector(4.5, FLOOR + 0.84, 4.8), axis=vector(0, 0.25, 0), radius=0.08,
             color=rgb(0.20, 0.45, 0.60), shininess=0.6)
    indoor_plant(5.5, 4.7, 1.3)
    cylinder(pos=vector(5.0, 3.6, 5.07), axis=vector(0, 0, -0.03), radius=0.25, color=WHITE)
    rod((5.0, 3.6, 5.04), (5.0, 3.78, 5.04), 0.012, CHARCOAL)
    rod((5.0, 3.6, 5.04), (5.12, 3.55, 5.04), 0.012, CHARCOAL)


def _kitchen_counters():
    sage = rgb(0.30, 0.38, 0.34)
    block((0.5, FLOOR + 0.45, 4.75), (4.2, 0.9, 0.7), sage, shininess=0.3)
    block((0.5, FLOOR + 0.93, 4.74), (4.26, 0.05, 0.76), STONE_TOP, shininess=0.5)
    for x in (-0.9, -0.2, 0.5, 1.2, 1.9):
        block((x, FLOOR + 0.45, 4.395), (0.012, 0.8, 0.01), rgb(0.12, 0.15, 0.13))
    for i in range(6):
        block((-1.25 + 0.7 * i + 0.3, FLOOR + 0.78, 4.385), (0.02, 0.16, 0.02), BRASS)
    block((0.5, FLOOR + 1.28, 5.085), (4.2, 0.70, 0.02), rgb(0.88, 0.90, 0.88))
    block((-0.9, FLOOR + 2.05, 4.925), (1.4, 0.8, 0.35), WHITE)
    block((2.35, FLOOR + 2.05, 4.925), (0.5, 0.8, 0.35), WHITE)

    block((1.6, FLOOR + 1.85, 4.85), (0.9, 0.12, 0.5), STEEL, shininess=0.6)
    block((1.6, (FLOOR + 1.91 + CEILING) / 2, 4.95), (0.3, CEILING - FLOOR - 1.91, 0.25), STEEL)
    block((-0.1, FLOOR + 0.96, 4.75), (0.7, 0.015, 0.45), rgb(0.55, 0.58, 0.60), shininess=0.7)
    rod((-0.1, FLOOR + 0.96, 4.98), (-0.1, FLOOR + 1.25, 4.98), 0.02, CHROME)
    rod((-0.1, FLOOR + 1.25, 4.98), (-0.1, FLOOR + 1.25, 4.82), 0.02, CHROME)
    block((1.6, FLOOR + 0.958, 4.75), (0.7, 0.012, 0.5), rgb(0.04, 0.04, 0.05), shininess=0.8)
    for dx in (-0.17, 0.17):
        for dz in (-0.12, 0.12):
            cylinder(pos=vector(1.6 + dx, FLOOR + 0.964, 4.75 + dz), axis=vector(0, 0.01, 0),
                     radius=0.09, color=rgb(0.25, 0.25, 0.27))

    block((-2.15, FLOOR + 0.975, 4.7), (0.9, 1.95, 0.8), STEEL, shininess=0.6)
    block((-2.15, FLOOR + 1.25, 4.295), (0.88, 0.012, 0.01), rgb(0.35, 0.36, 0.38))
    block((-1.82, FLOOR + 1.55, 4.285), (0.03, 0.4, 0.03), CHARCOAL)
    block((-1.82, FLOOR + 0.85, 4.285), (0.03, 0.5, 0.03), CHARCOAL)


def _kitchen_island():
    block((0.5, FLOOR + 0.45, 3.0), (2.4, 0.9, 0.85), rgb(0.88, 0.86, 0.80), shininess=0.3)
    block((0.5, FLOOR + 0.93, 3.0), (2.5, 0.05, 0.95), rgb(0.55, 0.36, 0.20), shininess=0.5)
    for x, color in ((-0.3, rgb(0.85, 0.36, 0.28)), (0.5, rgb(0.20, 0.50, 0.55)),
                     (1.3, rgb(0.86, 0.64, 0.18))):
        rod((x, FLOOR, 2.2), (x, FLOOR + 0.68, 2.2), 0.03, CHARCOAL)
        cylinder(pos=vector(x, FLOOR, 2.2), axis=vector(0, 0.03, 0), radius=0.18, color=CHARCOAL)
        cylinder(pos=vector(x, FLOOR + 0.68, 2.2), axis=vector(0, 0.06, 0), radius=0.19,
                 color=color)
    cylinder(pos=vector(1.3, FLOOR + 0.955, 3.0), axis=vector(0, 0.08, 0), radius=0.2,
             color=WHITE)
    for dx, dz, color in ((0.0, 0.0, rgb(0.95, 0.75, 0.10)), (0.09, 0.05, rgb(0.80, 0.15, 0.12)),
                          (-0.08, 0.06, rgb(0.50, 0.75, 0.20))):
        sphere(pos=vector(1.3 + dx, FLOOR + 1.05, 3.0 + dz), radius=0.065, color=color)


def build_kitchen():
    _kitchen_counters()
    _kitchen_island()
    for x in (-0.1, 0.5, 1.1):
        pendant(x, 3.0, FLOOR + 1.95)


def build_bedroom():
    rug(-1.1, -1.15, 1.9, 2.4)
    bed(-1.65, -1.15, (1, 0))
    nightstand(-2.45, -2.2)
    nightstand(-2.45, -0.1)
    wall_art(-2.69, FLOOR + 1.7, -1.15, (1, 0), 1.3, 0.8)
    indoor_plant(-0.55, 0.3, 0.8)


def build_interior():
    build_floor_and_ceiling()
    build_partitions()
    build_living_room()
    build_dining_room()
    build_kitchen()
    build_bedroom()


LAWN_TOP = -0.045
LAWN_X = (-21.0, 21.0)
LAWN_Z = (-7.5, 18.0)
NO_GRASS = [(-6.95, 6.95, -7.7, -0.4),
            (-7.7, 6.2, -3.2, 5.4)]
BLADES_PER_CLUMP = 4


def _grass_allowed(x, z):
    return not any(x0 <= x <= x1 and z0 <= z <= z1 for x0, x1, z0, z1 in NO_GRASS)


def _random_lawn_spot():
    while True:
        x = random.uniform(*LAWN_X)
        z = random.triangular(LAWN_Z[0], LAWN_Z[1], LAWN_Z[0] + 4.0)
        if _grass_allowed(x, z):
            return x, z


def build_lawn_texture():
    stripe_width = 1.4
    centre_z = (LAWN_Z[0] + LAWN_Z[1]) / 2
    x, index = LAWN_X[0], 0
    while x < LAWN_X[1]:
        shade = rgb(0.27, 0.57, 0.20) if index % 2 == 0 else rgb(0.21, 0.47, 0.16)
        block((x + stripe_width / 2, LAWN_TOP, centre_z),
              (stripe_width, 0.02, LAWN_Z[1] - LAWN_Z[0]), shade, shininess=0.0)
        x += stripe_width
        index += 1

    patch_colors = [rgb(0.34, 0.60, 0.18), rgb(0.16, 0.40, 0.14),
                    rgb(0.40, 0.62, 0.20), rgb(0.19, 0.46, 0.15)]
    for _ in range(90):
        x, z = _random_lawn_spot()
        width = random.uniform(1.2, 3.2)
        blob((x, LAWN_TOP + 0.01, z), (width, 0.03, width * random.uniform(0.6, 1.0)),
             random.choice(patch_colors), shininess=0.0)


def build_grass_blades(chunks=8, clumps_per_chunk=200):
    palette = [rgb(0.16, 0.42, 0.10), rgb(0.22, 0.52, 0.13), rgb(0.30, 0.60, 0.16),
               rgb(0.38, 0.66, 0.20), rgb(0.46, 0.60, 0.18)]
    for _ in range(chunks):
        blades = []
        for _ in range(clumps_per_chunk):
            x, z = _random_lawn_spot()
            tone = random.choice(palette)
            for _ in range(BLADES_PER_CLUMP):
                blade_height = random.uniform(0.20, 0.45)
                direction = norm(vector(random.uniform(-0.3, 0.3), 1.0, random.uniform(-0.3, 0.3)))
                blades.append(pyramid(
                    pos=vector(x + random.uniform(-0.10, 0.10), LAWN_TOP - 0.01,
                               z + random.uniform(-0.10, 0.10)),
                    axis=direction * blade_height, length=blade_height,
                    height=random.uniform(0.04, 0.07), width=random.uniform(0.04, 0.07),
                    color=tone * random.uniform(0.8, 1.15), shininess=0.0))
        compound(blades)


def build_grass():
    build_lawn_texture()
    build_grass_blades()


build_ground()
build_house_shell()
build_roofs()
build_carport()
build_entrance()
build_windows()
build_interior()
build_car()
build_garden()
build_trees()
build_fence()
build_grass()


roof_visible = True


def set_view(camera_pos, target, view_range):
    scene.center = target
    scene.camera.pos = camera_pos
    scene.camera.axis = target - camera_pos
    scene.range = view_range


def set_roof_visible(visible):
    global roof_visible
    roof_visible = visible
    for part in ROOF_PARTS:
        part.visible = visible
    roof_button.text = "Hide roof" if visible else "Show roof"


def view_exterior(_button=None):
    set_roof_visible(True)
    set_view(CAM_START, CAM_TARGET, EXTERIOR_RANGE)


def view_living(_button=None):
    set_view(vector(2.0, 1.8, -2.4), vector(5.2, 0.9, 0.2), 4.0)


def view_kitchen(_button=None):
    set_view(vector(3.4, 1.9, 0.8), vector(1.8, 0.9, 4.5), 4.0)


def view_bedroom(_button=None):
    set_view(vector(-0.55, 1.9, -2.5), vector(-2.2, 0.6, -1.2), 3.0)


def view_top(_button=None):
    set_roof_visible(False)
    set_view(vector(1.6, 18.0, -4.0), vector(1.6, 0.0, 1.2), 14.0)


def toggle_roof(_button=None):
    set_roof_visible(not roof_visible)


scene.append_to_caption("\n")
button(text="Exterior", bind=view_exterior)
button(text="Living room", bind=view_living)
button(text="Kitchen & dining", bind=view_kitchen)
button(text="Bedroom", bind=view_bedroom)
button(text="Top view", bind=view_top)
roof_button = button(text="Hide roof", bind=toggle_roof)
scene.append_to_caption("\n")

scene.center = CAM_TARGET
scene.camera.pos = CAM_START
scene.camera.axis = CAM_TARGET - CAM_START
scene.range = EXTERIOR_RANGE

while True:
    rate(120)
    if scene.range < ZOOM_MIN:
        scene.range = ZOOM_MIN
    elif scene.range > ZOOM_MAX:
        scene.range = ZOOM_MAX