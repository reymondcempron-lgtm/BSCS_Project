from vpython import *
import math


scene = canvas(
    title="Jaicten's DreamHouse",
    width=1200,
    height=720,
    background=vector(0.55, 0.66, 0.78)
)

scene.autoscale = False
scene.userspin = False
scene.userpan = False
scene.userzoom = False
scene.ambient = vector(0.52, 0.52, 0.52)
scene.fov = math.pi / 3

WHITE = vector(0.91, 0.90, 0.86)
MARBLE = vector(0.83, 0.82, 0.78)
MARBLE_DARK = vector(0.66, 0.66, 0.63)
BLACK = vector(0.055, 0.065, 0.075)
CHARCOAL = vector(0.12, 0.13, 0.14)
WOOD = vector(0.32, 0.19, 0.12)
WOOD_LIGHT = vector(0.49, 0.31, 0.19)
GLASS = vector(0.48, 0.62, 0.69)
GLASS_DARK = vector(0.12, 0.18, 0.21)
CONCRETE = vector(0.48, 0.48, 0.46)
PAVING = vector(0.59, 0.58, 0.55)
ASPHALT = vector(0.16, 0.17, 0.18)
GRASS = vector(0.18, 0.30, 0.16)
LEAF = vector(0.13, 0.28, 0.13)
LEAF_LIGHT = vector(0.27, 0.39, 0.19)
GOLD = vector(0.95, 0.69, 0.32)
WARM_LIGHT = vector(1.0, 0.77, 0.48)
RED = vector(0.75, 0.08, 0.08)
LINEN = vector(0.93, 0.92, 0.88)
SOFA = vector(0.30, 0.32, 0.34)
SOFA_LIGHT = vector(0.42, 0.44, 0.46)
ACCENT = vector(0.62, 0.42, 0.22)
WATER = vector(0.20, 0.58, 0.72)
STEEL = vector(0.62, 0.64, 0.66)
SOLAR = vector(0.08, 0.12, 0.24)

house = []
roof = []
windows = []
garage = []
landscape = []
lights = []
cars = []
stairs = []
furniture = []
GLOW_IDS = set()

FL0 = 0.84                              
SLAB_BOT = 4.45                                                     
FL1 = 4.85                             
FLOOR1 = 4.88                           
CEIL = 8.68                             
T = 0.3                                      


def block(group, pos, size, color, opacity=1, glow=False):
    obj = box(
        pos=vector(*pos),
        size=vector(*size),
        color=color,
        opacity=opacity
    )
    if glow:
        GLOW_IDS.add(id(obj))
        try:
            obj.emissive = True
        except Exception:
            pass
    group.append(obj)
    return obj


def cylinder_obj(group, pos, axis, radius, color, glow=False):
    obj = cylinder(
        pos=vector(*pos),
        axis=vector(*axis),
        radius=radius,
        color=color
    )
    if glow:
        GLOW_IDS.add(id(obj))
        try:
            obj.emissive = True
        except Exception:
            pass
    group.append(obj)
    return obj


def sphere_obj(group, pos, radius, color, glow=False):
    obj = sphere(pos=vector(*pos), radius=radius, color=color)
    if glow:
        GLOW_IDS.add(id(obj))
        try:
            obj.emissive = True
        except Exception:
            pass
    group.append(obj)
    return obj


def ellipsoid_obj(group, pos, size, color):
    obj = ellipsoid(pos=vector(*pos), size=vector(*size), color=color)
    group.append(obj)
    return obj


def seg(group, axis, u0, u1, y0, y1, fixed, t, color, opacity=1):
    if u1 - u0 <= 0.001 or y1 - y0 <= 0.001:
        return None
    um = (u0 + u1) / 2
    ym = (y0 + y1) / 2
    if axis == "x":
        return block(group, (um, ym, fixed), (u1 - u0, y1 - y0, t), color, opacity)
    return block(group, (fixed, ym, um), (t, y1 - y0, u1 - u0), color, opacity)


def wall(group, axis, u0, u1, y0, y1, fixed, t, color, openings=()):
    cursor = u0
    for (a0, a1, b0, b1) in sorted(openings):
        seg(group, axis, cursor, a0, y0, y1, fixed, t, color)                            
        seg(group, axis, a0, a1, y0, b0, fixed, t, color)                          
        seg(group, axis, a0, a1, b1, y1, fixed, t, color)                          
        cursor = a1
    seg(group, axis, cursor, u1, y0, y1, fixed, t, color)


def add_window(axis, a0, a1, b0, b1, cols, rows, fixed, t, face):
    f = 0.1
    d = t + 0.1

    seg(windows, axis, a0, a1, b0, b1, fixed, 0.04, GLASS, 0.32)

    seg(windows, axis, a0, a0 + f, b0, b1, fixed, d, BLACK)
    seg(windows, axis, a1 - f, a1, b0, b1, fixed, d, BLACK)
    seg(windows, axis, a0 + f, a1 - f, b0, b0 + f, fixed, d, BLACK)
    seg(windows, axis, a0 + f, a1 - f, b1 - f, b1, fixed, d, BLACK)

    for i in range(1, cols):
        u = a0 + (a1 - a0) * i / cols
        seg(windows, axis, u - 0.035, u + 0.035, b0, b1, fixed, 0.12, BLACK)
    for j in range(1, rows):
        y = b0 + (b1 - b0) * j / rows
        seg(windows, axis, a0, a1, y - 0.035, y + 0.035, fixed, 0.12, BLACK)

    um = (a0 + a1) / 2
    length = (a1 - a0) + 0.3
    off = face * (t / 2 + 0.13)
    if axis == "x":
        block(windows, (um, b0 - 0.04, fixed + off), (length, 0.08, 0.26), MARBLE_DARK)
    else:
        block(windows, (fixed + off, b0 - 0.04, um), (0.26, 0.08, length), MARBLE_DARK)


def facade(group, axis, u0, u1, y0, y1, fixed, t, color, face, wins=()):
    """wins: list of (a0, a1, b0, b1, cols, rows)"""
    wall(group, axis, u0, u1, y0, y1, fixed, t, color, [w[:4] for w in wins])
    for w in wins:
        add_window(axis, w[0], w[1], w[2], w[3], w[4], w[5], fixed, t, face)


block(landscape, (0, -0.5, 0), (110, 1, 100), GRASS)

block(landscape, (0, 0.03, 15.7), (110, 0.06, 2.8), PAVING)
block(landscape, (0, 0.04, 17.12), (110, 0.08, 0.16), MARBLE_DARK)
block(landscape, (0, 0.02, 22.55), (110, 0.04, 10.8), ASPHALT)
for x in range(-48, 49, 8):
    block(landscape, (x, 0.05, 22.55), (3.5, 0.02, 0.2), WHITE)

block(landscape, (5.5, 0.025, 10.85), (11.4, 0.05, 6.9), CONCRETE)
for z in [9.1, 10.8, 12.5]:
    block(landscape, (5.5, 0.052, z), (11.4, 0.006, 0.05), vector(0.34, 0.34, 0.33))

block(landscape, (-4.7, 0.03, 12.75), (2.8, 0.06, 3.1), PAVING)


block(house, (0, 0.35, -2.6), (23.2, 0.7, 10), MARBLE_DARK)
block(house, (-5.95, 0.35, 5.0), (11.3, 0.7, 5.2), MARBLE_DARK)
block(house, (0, 0.77, -2.5), (22.8, 0.14, 9.8), MARBLE)
block(house, (-5.85, 0.77, 4.9), (11.1, 0.14, 5.0), MARBLE)

block(house, (-5.85, 0.35, 8.7), (11.1, 0.7, 2.6), MARBLE_DARK)
block(house, (-5.85, 0.77, 8.7), (11.1, 0.14, 2.6), MARBLE)

block(garage, (5.8, 0.06, 5.0), (11.6, 0.12, 5.2), CONCRETE)

block(stairs, (-4.7, 0.28, 10.3), (7.0, 0.56, 0.6), MARBLE)
block(stairs, (-4.7, 0.14, 10.9), (7.0, 0.28, 0.6), MARBLE)


facade(house, "x", -11.4, 11.4, FL0, SLAB_BOT, -7.25, T, MARBLE, -1, [
    (-10.0, -4.0, 1.4, 3.9, 4, 1),
    (2.0, 9.0, 1.4, 3.9, 4, 1)
])

facade(house, "z", -7.1, 7.1, FL0, SLAB_BOT, -11.25, T, MARBLE, -1, [
    (-5.8, -1.4, 1.4, 3.9, 3, 1)
])

facade(house, "z", -7.1, 2.4, FL0, SLAB_BOT, 11.25, T, MARBLE, 1, [
    (-6.0, -2.6, 1.4, 3.9, 3, 1)
])

wall(house, "x", -11.4, -0.3, FL0, SLAB_BOT, 7.25, T, MARBLE, [
    (-10.4, -5.2, 1.4, 4.0),
    (-3.9, -2.5, FL0, 3.5)
])
add_window("x", -10.4, -5.2, 1.4, 4.0, 4, 1, 7.25, T, 1)

wall(house, "x", -4.5, -1.9, FL0, SLAB_BOT, 7.43, 0.06, CHARCOAL, [(-3.9, -2.5, FL0, 3.5)])

seg(house, "x", -3.9, -3.8, FL0, 3.5, 7.25, 0.36, BLACK)
seg(house, "x", -2.6, -2.5, FL0, 3.5, 7.25, 0.36, BLACK)
seg(house, "x", -3.8, -2.6, 3.4, 3.5, 7.25, 0.36, BLACK)
seg(house, "x", -3.8, -2.6, FL0, 3.4, 7.25, 0.1, WOOD)
for x in [-3.45, -2.95]:
    seg(house, "x", x - 0.02, x + 0.02, FL0, 3.4, 7.25, 0.14, BLACK)
sphere_obj(house, (-2.75, 2.0, 7.34), 0.07, GOLD)

for x in [-4.75, -1.65]:
    block(lights, (x, 2.7, 7.48), (0.12, 0.35, 0.1), WARM_LIGHT, glow=True)

wall(garage, "z", 2.4, 7.4, 0.12, SLAB_BOT, -0.15, T, CHARCOAL)
wall(garage, "x", 0.0, 11.1, 0.12, SLAB_BOT, 2.55, T, CHARCOAL)
wall(garage, "z", 2.4, 7.4, 0.12, SLAB_BOT, 11.25, T, CHARCOAL)

for x in [2.8, 5.6, 8.3]:
    block(lights, (x, 4.41, 5.0), (1.6, 0.04, 0.16), WARM_LIGHT, glow=True)

wall(house, "z", -7.1, 2.4, FL0, SLAB_BOT, -0.15, T, WHITE, [(-3.0, -1.0, FL0, 3.1)])

wall(house, "x", -9.6, -3.6, FL0, 3.7, -3.6, 0.2, WOOD)


block(house, (0, 4.65, 0), (23.6, 0.4, 15.6), MARBLE)
block(house, (0, FL1 + 0.015, 0), (22.4, 0.03, 14.2), WOOD_LIGHT)               


facade(house, "x", -11.4, 11.4, FL1, CEIL, 7.25, T, MARBLE, 1, [
    (-9.0, -3.0, 5.4, 8.1, 4, 2),
    (1.0, 7.4, 5.4, 8.1, 4, 2)
])

block(house, (-1.0, 6.765, 7.43), (4.0, 3.83, 0.06), WHITE)
block(house, (9.4, 6.765, 7.43), (4.0, 3.83, 0.06), CHARCOAL)
for i in range(12):
    block(house, (7.75 + i * 0.3, 6.765, 7.49), (0.1, 3.83, 0.05), WOOD_LIGHT)

facade(house, "x", -11.4, 11.4, FL1, CEIL, -7.25, T, MARBLE, -1, [
    (-10.0, -4.0, 5.4, 8.1, 4, 2),
    (2.0, 9.5, 5.4, 8.1, 5, 2)
])

facade(house, "z", -7.1, 7.1, FL1, CEIL, -11.25, T, MARBLE, -1, [
    (-6.2, -4.4, 6.4, 8.0, 2, 1),
    (0.0, 5.0, 5.4, 8.1, 3, 2)
])

facade(house, "z", -7.1, 7.1, FL1, CEIL, 11.25, T, MARBLE, 1, [
    (-6.0, -2.6, 5.4, 8.1, 3, 2),
    (1.5, 5.5, 5.4, 8.1, 3, 2)
])

wall(house, "z", -7.1, 7.1, FL1, CEIL, 0.0, 0.2, WHITE, [(1.6, 3.0, FL1, FL1 + 2.3)])
wall(house, "x", -11.1, -0.1, FL1, CEIL, -3.5, 0.18, WHITE, [(-6.4, -5.2, FL1, FL1 + 2.3)])
wall(house, "x", 0.1, 11.1, FL1, CEIL, -1.0, 0.18, WHITE, [(8.0, 9.2, FL1, FL1 + 2.3)])


block(house, (-5.2, 4.65, 8.9), (13.2, 0.4, 2.2), MARBLE)
block(house, (-5.2, 4.5, 10.0), (13.2, 0.14, 0.06), CHARCOAL)

block(windows, (-5.2, 5.4, 9.9), (13.0, 1.1, 0.05), GLASS, 0.3)
block(windows, (-11.7, 5.4, 8.85), (0.05, 1.1, 2.1), GLASS, 0.3)
block(windows, (1.3, 5.4, 8.85), (0.05, 1.1, 2.1), GLASS, 0.3)
block(windows, (-5.2, 5.98, 9.9), (13.2, 0.06, 0.12), BLACK)
block(windows, (-11.75, 5.98, 8.85), (0.12, 0.06, 2.2), BLACK)
block(windows, (1.35, 5.98, 8.85), (0.12, 0.06, 2.2), BLACK)
for x in [-11.75, -8.5, -5.2, -1.9, 1.35]:
    block(windows, (x, 5.4, 9.9), (0.07, 1.15, 0.1), BLACK)

block(landscape, (-5.2, 5.05, 9.5), (4.0, 0.4, 0.5), CHARCOAL)
for i in range(9):
    ellipsoid_obj(
        landscape,
        (-6.9 + i * 0.42, 5.4 + (i % 3) * 0.1, 9.5),
        (0.6, 0.55 + (i % 3) * 0.12, 0.5),
        LEAF_LIGHT if i % 2 == 0 else LEAF
    )

cylinder_obj(furniture, (-9.4, 4.85, 9.0), (0, 0.55, 0), 0.04, BLACK)
cylinder_obj(furniture, (-9.4, 5.4, 9.0), (0, 0.04, 0), 0.6, MARBLE)
for dx in [-0.95, 0.95]:
    block(furniture, (-9.4 + dx, 5.1, 9.0), (0.45, 0.5, 0.45), BLACK)
    block(furniture, (-9.4 + dx, 5.45, 9.0), (0.45, 0.06, 0.45), WOOD_LIGHT)


block(roof, (0, 8.85, 0), (25.5, 0.35, 17.5), BLACK)                          
block(roof, (0, 8.655, 0), (25.4, 0.04, 17.4), WOOD)                            

for z in [-8.65, 8.65]:
    block(roof, (0, 9.15, z), (25.5, 0.25, 0.2), CHARCOAL)
for x in [-12.65, 12.65]:
    block(roof, (x, 9.15, 0), (0.2, 0.25, 17.3), CHARCOAL)

for x in [-8, -5, -2]:
    for z in [-4.5, -2.0]:
        block(roof, (x, 9.07, z), (2.6, 0.07, 2.0), SOLAR)
        block(roof, (x, 9.11, z), (2.62, 0.01, 0.04), STEEL)

block(roof, (6, 9.1, 3), (3.6, 0.14, 2.6), GLASS, 0.5)
for dx in [-1.8, 1.8]:
    block(roof, (6 + dx, 9.1, 3), (0.1, 0.16, 2.7), BLACK)
for dz in [-1.3, 1.3]:
    block(roof, (6, 9.1, 3 + dz), (3.7, 0.16, 0.1), BLACK)

for x in [-10, -5, 0, 5, 10]:
    cylinder_obj(roof, (x, 8.635, 8.1), (0, -0.03, 0), 0.1, WARM_LIGHT, glow=True)
for x in [-8, -4]:
    for z in [-1, 2, 5]:
        cylinder_obj(roof, (x, 8.635, z), (0, -0.03, 0), 0.1, WARM_LIGHT, glow=True)
for x in [3, 6, 9]:
    for z in [-4, 1, 4]:
        cylinder_obj(roof, (x, 8.635, z), (0, -0.03, 0), 0.1, WARM_LIGHT, glow=True)


block(house, (-12.0, 1.8, 4.3), (0.3, 3.6, 5.2), vector(0.30, 0.28, 0.25))
block(house, (-12.0, 3.65, 4.3), (0.4, 0.1, 5.4), MARBLE_DARK)
for i in range(11):
    y = 0.2 + i * 0.32
    base = 0.36 + 0.07 * math.sin(i * 2.3)
    for j, (z0, z1) in enumerate([(1.7, 3.3), (3.3, 5.2), (5.2, 6.9)]):
        s = base + 0.05 * math.sin(i * 1.7 + j * 2.1)
        block(house, (-12.17, y, (z0 + z1) / 2), (0.06, 0.29, z1 - z0 - 0.03),
              vector(s, s * 0.95, s * 0.88))


def rug(x, z, y0, w, d, color):
    block(furniture, (x, y0 + 0.015, z), (w, 0.03, d), color)


def sofa(x, z, y0, facing=1, w=3.2, color=SOFA, cushion=SOFA_LIGHT):
    d = facing
    block(furniture, (x, y0 + 0.25, z), (w, 0.5, 1.0), color)
    block(furniture, (x, y0 + 0.7, z - d * 0.42), (w, 0.55, 0.2), color)
    for s in (-1, 1):
        block(furniture, (x + s * (w / 2 - 0.12), y0 + 0.45, z), (0.24, 0.7, 1.0), color)
    seats = 2 if w > 2 else 1
    seat_w = (w - 0.5) / seats
    for i in range(seats):
        cx = x - (w - 0.5) / 2 + seat_w * (i + 0.5)
        block(furniture, (cx, y0 + 0.57, z + d * 0.08), (seat_w - 0.04, 0.14, 0.78), cushion)
    block(furniture, (x - w / 2 + 0.6, y0 + 0.75, z - d * 0.25), (0.5, 0.4, 0.12), ACCENT)


def coffee_table(x, z, y0, w=1.6, d=0.9):
    block(furniture, (x, y0 + 0.2, z), (w - 0.3, 0.36, d - 0.3), CHARCOAL)
    block(furniture, (x, y0 + 0.4, z), (w, 0.06, d), MARBLE)


def plant(x, z, y0, h=1.4):
    cylinder_obj(furniture, (x, y0, z), (0, 0.45, 0), 0.25, CHARCOAL)
    for i in range(5):
        a = i * 1.26
        ellipsoid_obj(
            furniture,
            (x + math.cos(a) * 0.15, y0 + 0.7 + (i % 3) * h * 0.2, z + math.sin(a) * 0.15),
            (0.55, 0.7, 0.55),
            LEAF_LIGHT if i % 2 == 0 else LEAF
        )


def floor_lamp(x, z, y0):
    cylinder_obj(furniture, (x, y0, z), (0, 1.6, 0), 0.03, BLACK)
    sphere_obj(lights, (x, y0 + 1.7, z), 0.2, WARM_LIGHT, glow=True)


def chair(x, z, y0, facing=1):
    block(furniture, (x, y0 + 0.45, z), (0.5, 0.06, 0.5), WOOD_LIGHT)
    for dx in (-0.2, 0.2):
        for dz in (-0.2, 0.2):
            block(furniture, (x + dx, y0 + 0.21, z + dz), (0.05, 0.42, 0.05), BLACK)
    block(furniture, (x, y0 + 0.75, z - facing * 0.22), (0.5, 0.5, 0.05), WOOD_LIGHT)


def stool(x, z, y0):
    cylinder_obj(furniture, (x, y0, z), (0, 0.72, 0), 0.04, BLACK)
    cylinder_obj(furniture, (x, y0 + 0.72, z), (0, 0.06, 0), 0.22, WOOD_LIGHT)


def bed(x, z, y0, head=-1):
    """head = -1: headboard toward -z, head = +1: headboard toward +z"""
    block(furniture, (x, y0 + 0.2, z), (2.2, 0.4, 2.4), WOOD)
    block(furniture, (x, y0 + 0.52, z), (2.0, 0.25, 2.2), LINEN)
    block(furniture, (x, y0 + 0.66, z - head * 0.45), (2.04, 0.05, 1.2), ACCENT)
    for dx in (-0.5, 0.5):
        block(furniture, (x + dx, y0 + 0.74, z + head * 0.85), (0.7, 0.15, 0.4), WHITE)
    block(furniture, (x, y0 + 0.65, z + head * 1.2), (2.4, 1.3, 0.1), WOOD_LIGHT)
    for s in (-1, 1):
        block(furniture, (x + s * 1.5, y0 + 0.25, z + head * 1.0), (0.5, 0.5, 0.45), WOOD_LIGHT)
        sphere_obj(lights, (x + s * 1.5, y0 + 0.62, z + head * 1.0), 0.1, WARM_LIGHT, glow=True)

rug(-7.6, 2.2, FL0, 4.6, 3.6, vector(0.55, 0.52, 0.47))
sofa(-7.6, 4.3, FL0, facing=-1)
coffee_table(-7.6, 2.0, FL0)
block(furniture, (-9.6, FL0 + 0.25, 4.3), (0.55, 0.5, 0.55), WOOD_LIGHT)
sphere_obj(lights, (-9.6, FL0 + 0.62, 4.3), 0.11, WARM_LIGHT, glow=True)
plant(-10.3, 6.3, FL0)
floor_lamp(-5.3, 4.7, FL0)

block(furniture, (-6.6, 2.4, -3.46), (2.4, 1.35, 0.05), BLACK)
block(furniture, (-6.6, FL0 + 0.3, -3.35), (3.0, 0.5, 0.4), WOOD_LIGHT)

block(furniture, (-7.2, FL0 + 0.47, -5.5), (4.0, 0.94, 1.0), WHITE)
block(furniture, (-7.2, FL0 + 0.97, -5.5), (4.1, 0.06, 1.1), MARBLE)
for x in [-8.4, -7.2, -6.0]:
    stool(x, -4.6, FL0)
    cylinder_obj(lights, (x, SLAB_BOT, -5.5), (0, -1.05, 0), 0.012, BLACK)
    sphere_obj(lights, (x, 3.3, -5.5), 0.17, WARM_LIGHT, glow=True)
block(furniture, (-10.6, FL0 + 1.0, -6.4), (0.9, 2.0, 0.8), STEEL)

block(furniture, (-2.2, FL0 + 0.72, -4.5), (2.2, 0.07, 1.0), WOOD)
for dx in (-0.9, 0.9):
    block(furniture, (-2.2 + dx, FL0 + 0.36, -4.5), (0.1, 0.72, 0.8), BLACK)
for dx in (-0.6, 0.6):
    chair(-2.2 + dx, -3.75, FL0, facing=-1)
    chair(-2.2 + dx, -5.25, FL0, facing=1)

for x in [-9, -6, -3]:
    for z in [-6, -1.5, 3, 6]:
        cylinder_obj(lights, (x, SLAB_BOT, z), (0, -0.03, 0), 0.1, WARM_LIGHT, glow=True)

bed(6.0, -5.8, FL0, head=-1)
rug(6.0, -3.6, FL0, 3.4, 2.2, vector(0.45, 0.42, 0.38))
plant(9.8, -1.0, FL0)

bed(-6.2, -2.1, FLOOR1, head=-1)
rug(-6.2, -0.6, FLOOR1, 4.2, 3.2, vector(0.36, 0.34, 0.32))
block(furniture, (-0.4, FLOOR1 + 1.15, -2.1), (0.5, 2.3, 2.0), WOOD_LIGHT)               
sofa(-4.2, 3.6, FLOOR1, facing=1, w=1.3)                                                  
plant(-9.2, 6.2, FLOOR1)
floor_lamp(-2.5, 6.3, FLOOR1)

block(furniture, (-9.2, FLOOR1 + 0.3, -6.0), (1.8, 0.6, 0.9), WHITE)
block(furniture, (-3.0, FLOOR1 + 0.45, -6.7), (1.6, 0.9, 0.5), WOOD_LIGHT)
block(furniture, (-3.0, FLOOR1 + 1.5, -6.95), (1.2, 0.9, 0.04), GLASS, 0.6)

rug(4.2, 2.6, FLOOR1, 4.6, 3.6, vector(0.50, 0.44, 0.36))
sofa(4.0, 1.1, FLOOR1, facing=1, w=3.4)
coffee_table(4.0, 3.0, FLOOR1)
sofa(6.9, 3.6, FLOOR1, facing=-1, w=1.3)
plant(1.5, 6.3, FLOOR1)
plant(7.0, 6.4, FLOOR1)

block(furniture, (9.4, FLOOR1 + 0.75, 6.3), (1.8, 0.06, 0.8), WOOD)
for dx in (-0.8, 0.8):
    block(furniture, (9.4 + dx, FLOOR1 + 0.37, 6.3), (0.06, 0.74, 0.7), BLACK)
chair(9.4, 5.4, FLOOR1, facing=1)
sphere_obj(lights, (9.9, FLOOR1 + 0.95, 6.3), 0.1, WARM_LIGHT, glow=True)

bed(5.5, -2.35, FLOOR1, head=1)
rug(5.5, -3.9, FLOOR1, 3.6, 2.4, vector(0.40, 0.38, 0.35))
block(furniture, (0.35, FLOOR1 + 1.15, -4.8), (0.5, 2.3, 2.2), WOOD_LIGHT)               
plant(10.2, -6.4, FLOOR1)

def make_car(x, z, body_color):
    y0 = 0.12
    block(cars, (x, y0 + 0.65, z), (2.0, 0.65, 4.5), body_color)                       
    block(cars, (x, y0 + 1.2, z - 0.3), (1.74, 0.5, 2.2), GLASS_DARK, 0.9)                     
    block(cars, (x, y0 + 1.47, z - 0.3), (1.8, 0.07, 2.2), body_color)                 
    block(cars, (x, y0 + 0.55, z + 2.26), (0.9, 0.2, 0.04), BLACK)                       

    for side in (-1, 1):
        block(cars, (x + side * 0.7, y0 + 0.75, z + 2.26), (0.5, 0.15, 0.04), WARM_LIGHT, glow=True)
        block(cars, (x + side * 0.7, y0 + 0.75, z - 2.26), (0.5, 0.12, 0.04), RED, glow=True)
        for wz in (z - 1.4, z + 1.4):
            cylinder_obj(cars, (x + side * 0.85, y0 + 0.38, wz), (side * 0.2, 0, 0), 0.38, BLACK)
            cylinder_obj(cars, (x + side * 1.04, y0 + 0.38, wz), (side * 0.03, 0, 0), 0.22, MARBLE_DARK)


make_car(2.8, 5.1, vector(0.17, 0.18, 0.20))
make_car(8.3, 5.1, vector(0.88, 0.88, 0.84))



def shrub(x, z, scale=1):
    for i in range(5):
        angle = i * 1.256
        ellipsoid_obj(
            landscape,
            (x + math.cos(angle) * 0.35 * scale, 0.35 * scale, z + math.sin(angle) * 0.35 * scale),
            (0.85 * scale, 0.65 * scale, 0.85 * scale),
            LEAF if i % 2 == 0 else LEAF_LIGHT
        )


def tree(x, z, height=5):
    cylinder_obj(landscape, (x, 0, z), (0, height, 0), 0.22, WOOD)
    for i in range(7):
        angle = i * 0.9
        ellipsoid_obj(
            landscape,
            (x + math.cos(angle) * 0.8, height + (i % 2) * 0.35, z + math.sin(angle) * 0.8),
            (1.5, 1.3, 1.5),
            LEAF if i % 2 == 0 else LEAF_LIGHT
        )


for x, z, s in [
    (-12.5, 8.5, 0.9), (-12.5, 10.5, 0.9), (-12.5, 12.5, 0.9),
    (-10.5, 12.2, 0.8), (-9.6, 10.9, 0.7),
    (-1.0, 11.9, 0.7), (-1.0, 13.3, 0.7),
    (-13.2, -1, 0.9), (-13.2, -4, 0.9),
    (12.6, 11, 0.9), (13.2, 8.5, 0.9), (12.6, 6, 0.9)
]:
    shrub(x, z, s)

for x, z, h in [(-18, 5, 5), (17, 7, 5), (-18, -7, 4), (18, -8, 5), (12, -15, 4.5), (-16, 15, 4.5)]:
    tree(x, z, h)

for x, z in [(-13.5, 9), (-13.5, 12), (-6.6, 12.2), (-2.8, 12.2), (12.8, 10), (13.5, 7), (-16, 4)]:
    cylinder_obj(landscape, (x, 0, z), (0, 0.65, 0), 0.07, BLACK)
    sphere_obj(lights, (x, 0.7, z), 0.12, WARM_LIGHT, glow=True)


block(landscape, (-2.9, 0.04, -12.8), (14.2, 0.08, 10.4), PAVING)
block(landscape, (-2.9, 0.075, -13.3), (11.2, 0.02, 5.4), WATER, 0.88)
for z in [-10.55, -16.05]:
    block(landscape, (-2.9, 0.1, z), (11.6, 0.06, 0.25), MARBLE)
for x in [-8.6, 2.8]:
    block(landscape, (x, 0.1, -13.3), (0.25, 0.06, 5.8), MARBLE)

for x in [-6.5, -4.0]:
    block(landscape, (x, 0.23, -9.1), (0.8, 0.3, 2.0), WHITE)
    block(landscape, (x, 0.40, -9.1), (0.82, 0.03, 0.5), ACCENT)


USE_COMPOUND = True


def optimize_scene():
    if not USE_COMPOUND:
        return

    for group in (house, garage, landscape, furniture, stairs, cars, windows, lights, roof):
        keep = []
        buckets = {}

        for obj in group:
            if id(obj) in GLOW_IDS or obj.opacity < 1:
                keep.append(obj)
                continue
            key = (round(obj.color.x, 3), round(obj.color.y, 3), round(obj.color.z, 3))
            buckets.setdefault(key, []).append(obj)

        for key, objs in buckets.items():
            if len(objs) < 2:
                keep.extend(objs)
                continue
            try:
                merged = compound(objs)
                merged.color = vector(*key)
                for o in objs:
                    o.visible = False
                keep.append(merged)
            except Exception:
                keep.extend(objs)

        group[:] = keep


optimize_scene()


VIEW_DIST = 40                                                 
MOVE_SPEED = 0.30
BOOST = 2.6
ACCEL = 0.14                                               
LOOK_GAIN = 0.80                                                             
INVERT_LOOK = False                                            
FLY_TIME = 1.2                                             

FPS = 60                                                                                    
FRAME_K = 60.0 / FPS                                      
MOVE_KEYS = {"w", "a", "s", "d", "q", "e"}


def vcopy(v):
    return vector(v.x, v.y, v.z)


cam_pos = vector(27, 13, 35)
yaw = 0.0
pitch = 0.0
vel = vector(0, 0, 0)
tween = None

keys_pressed = set()
dragging = False
last_u = None
last_v = None


def forward_vec():
    cp = math.cos(pitch)
    return vector(math.sin(yaw) * cp, math.sin(pitch), -math.cos(yaw) * cp)


def right_vec():
    return vector(math.cos(yaw), 0, math.sin(yaw))


def apply_camera():
    scene.camera.pos = vcopy(cam_pos)
    scene.camera.axis = forward_vec() * VIEW_DIST


def aim(position, target):
    d = target - position
    return math.atan2(d.x, -d.z), math.asin(max(-1.0, min(1.0, d.y / mag(d))))


def set_view(position, target):
    global cam_pos, yaw, pitch, vel, tween
    position = vector(*position)
    target = vector(*target)
    cam_pos = position
    yaw, pitch = aim(position, target)
    vel = vector(0, 0, 0)
    tween = None
    apply_camera()


def fly_to(name):
    global tween
    position, target = VIEWS[name]
    position = vector(*position)
    target = vector(*target)
    y1, p1 = aim(position, target)
    dyaw = (y1 - yaw + math.pi) % (2 * math.pi) - math.pi
    tween = {
        "t": 0.0,
        "p0": vcopy(cam_pos), "p1": position,
        "y0": yaw, "dy": dyaw,
        "a0": pitch, "a1": p1
    }


VIEWS = {
    "front": ((27, 13, 35), (0, 4, 2)),
    "aerial": ((28, 34, 36), (0, 3, 0)),
    "entrance": ((-18, 8, 25), (-5, 3, 5)),
    "garage": ((20, 8, 24), (5, 2, 5)),
    "balcony": ((18, 12, 23), (0, 6, 7)),
    "interior": ((-3.4, 3.0, 6.3), (-8, 1.8, -2)),
    "pool": ((-22, 9, -30), (-3, 2, -8)),
}

roof_visible = True


def toggle_roof():
    global roof_visible
    roof_visible = not roof_visible
    for obj in roof:
        obj.visible = roof_visible


def mouse_down(evt):
    global dragging, last_u, last_v
    dragging = True
    last_u = None
    last_v = None


def mouse_up(evt):
    global dragging
    dragging = False


scene.bind("mousedown", mouse_down)
scene.bind("mouseup", mouse_up)


def update_look():
    """Turn the camera in place using the mouse ray in camera space,
    so dragging never translates or orbits the camera."""
    global yaw, pitch, last_u, last_v

    if not dragging:
        return False

    ray = scene.mouse.ray
    if ray is None or mag(ray) < 0.001:
        return False

    f = forward_vec()
    r = right_vec()
    u = cross(r, f)
    df = dot(ray, f)
    if df < 0.05:
        return False

    cu = dot(ray, r) / df
    cv = dot(ray, u) / df

    if last_u is None:
        last_u, last_v = cu, cv
        return False

    sign = -1 if INVERT_LOOK else 1
    yaw += sign * (math.atan(cu) - math.atan(last_u)) * LOOK_GAIN
    pitch += sign * (math.atan(cv) - math.atan(last_v)) * LOOK_GAIN
    pitch = max(-1.45, min(1.45, pitch))
    last_u, last_v = cu, cv
    return True


def key_down(evt):
    key = evt.key.lower()
    fresh = key not in keys_pressed
    keys_pressed.add(key)

    if not fresh:
        return

    presets = {"1": "front", "2": "aerial", "3": "entrance", "4": "garage",
               "5": "balcony", "6": "interior", "7": "pool"}
    if key in presets:
        fly_to(presets[key])
    elif key == "r":
        toggle_roof()


def key_up(evt):
    keys_pressed.discard(evt.key.lower())


scene.bind("keydown", key_down)
scene.bind("keyup", key_up)


def update_move():
    global cam_pos, vel

    fwd_h = vector(math.sin(yaw), 0, -math.cos(yaw))
    right = right_vec()
    wish = vector(0, 0, 0)

    if "w" in keys_pressed:
        wish = wish + fwd_h
    if "s" in keys_pressed:
        wish = wish - fwd_h
    if "d" in keys_pressed:
        wish = wish + right
    if "a" in keys_pressed:
        wish = wish - right
    if "q" in keys_pressed:
        wish = wish + vector(0, 1, 0)
    if "e" in keys_pressed:
        wish = wish - vector(0, 1, 0)

    speed = MOVE_SPEED * FRAME_K * (BOOST if "shift" in keys_pressed else 1.0)
    if mag(wish) > 0:
        wish = norm(wish) * speed

    vel = vel + (wish - vel) * (1 - (1 - ACCEL) ** FRAME_K)
    if mag(vel) < 0.002 and mag(wish) == 0:
        vel = vector(0, 0, 0)
        return False

    p = cam_pos + vel
    cam_pos = vector(
        max(-70, min(70, p.x)),
        max(0.6, min(70, p.y)),
        max(-70, min(70, p.z))
    )
    return True


def step_camera():
    global cam_pos, yaw, pitch, tween, vel

    if tween is not None:
        if (keys_pressed & MOVE_KEYS) or dragging:
            tween = None
        else:
            tween["t"] += 1.0 / (FPS * FLY_TIME)
            s = min(tween["t"], 1.0)
            e = s * s * (3 - 2 * s)
            cam_pos = tween["p0"] + (tween["p1"] - tween["p0"]) * e
            yaw = tween["y0"] + tween["dy"] * e
            pitch = tween["a0"] + (tween["a1"] - tween["a0"]) * e
            vel = vector(0, 0, 0)
            if s >= 1.0:
                tween = None
            apply_camera()
            return

    looked = update_look()
    moved = update_move()
    if looked or moved:
        apply_camera()



scene.append_to_caption("\n\n")

button(text="Front", bind=lambda b: fly_to("front"))
button(text="Aerial", bind=lambda b: fly_to("aerial"))
button(text="Entrance", bind=lambda b: fly_to("entrance"))
button(text="Garage", bind=lambda b: fly_to("garage"))
button(text="Balcony", bind=lambda b: fly_to("balcony"))
button(text="Interior", bind=lambda b: fly_to("interior"))
button(text="Pool", bind=lambda b: fly_to("pool"))

scene.append_to_caption("\n")
button(text="Toggle Roof", bind=lambda b: toggle_roof())

scene.append_to_caption(
    "\n\n"
    "DRONE CONTROLS (click the scene once so it receives the keyboard)\n"
    "LEFT MOUSE DRAG: look around only (the camera never moves from the mouse)\n"
    "W / A / S / D: fly forward / left / back / right\n"
    "Q / E: up / down      SHIFT: boost\n"
    "1-7: camera presets (front, aerial, entrance, garage, balcony, interior, pool)\n"
    "R: toggle roof"
)


set_view((27, 13, 35), (0, 4, 2))

print("Jaicten's DreamHouse is running!")
print("Drag = look, WASD = fly, Q/E = up/down, Shift = boost")

while True:
    rate(FPS)
    step_camera()