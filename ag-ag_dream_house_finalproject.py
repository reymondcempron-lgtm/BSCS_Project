# Seaside Dream House - final project
# A two-story house on a hill by the sea, built with VPython.
# Run with: python ag-ag_dream_house_finalproject.py

from collections import namedtuple
import math
import random
import time
from types import SimpleNamespace

from vpython import (box, button, color, compound, cone, cylinder,
                     distant_light, ellipsoid, local_light, points, quad, rate,
                     scene, sphere, triangle, vector, vertex)

# =============================================================================
# 1. SETTINGS AND COLORS
# =============================================================================

# Heights and sizes, in meters. Y points up, the sea is toward +z, and the
# front door faces -z.
FLOOR2_Y = 3.4
WALL_TOP_Y = 6.8
RIDGE_Y = 11.5
SEA_Y = -28
WALL_THICK = 0.2
HOUSE_X = 7
HOUSE_Z = 5.5

DOOR_WIDTH = 1.6
DOOR_TOP = 2.4
WINDOW_WIDTH = 1.2
WINDOW_SILL = 1.0
WINDOW_TOP = 2.3

# Stairs run along the middle wall, climbing toward +x.
STAIR_LOW_X = -4.8
STAIR_HIGH_X = 0.6
STAIR_ZMIN = -1.7
STAIR_ZMAX = -0.1

# Same seed every run, so the scenery always looks the same.
RANDOM_SEED = 7

# An opening is a doorway when its sill is 0, otherwise it is a window.
Opening = namedtuple("Opening", "center width sill top")
# A wall runs along one axis ("x" or "z") and stays at "fixed" on the other.
Wall = namedtuple("Wall", "level axis fixed start end openings")
# A rectangle on the floor plan.
Rect = namedtuple("Rect", "xmin zmin xmax zmax")


def door(center):
    return Opening(center, DOOR_WIDTH, 0, DOOR_TOP)


def window(center):
    return Opening(center, WINDOW_WIDTH, WINDOW_SILL, WINDOW_TOP)


OUTER_WALLS = [
    # Ground floor
    Wall(0, "x", -5.5, -7, 7, [window(-5), door(-2), window(3), window(5.5)]),
    Wall(0, "x", 5.5, -7, 7, [window(-4.5), window(-2), door(0), window(3), window(5.5)]),
    Wall(0, "z", -7, -5.5, 5.5, [window(-3)]),
    Wall(0, "z", 7, -5.5, 5.5, [window(-2.75), window(2.75)]),
    # Upper floor
    Wall(1, "x", -5.5, -7, 7, [window(-5), window(-2), window(1.5), window(5)]),
    Wall(1, "x", 5.5, -7, 7, [window(-4.5), window(-1.5), window(2), door(4), window(6)]),
    Wall(1, "z", -7, -5.5, 5.5, [window(-3), window(0.9)]),
    Wall(1, "z", 7, -5.5, 5.5, [window(-2.75), window(2.75)]),
]

INNER_WALLS = [
    # Ground floor
    Wall(0, "x", 0, -7, 7, [door(-6), door(4)]),
    Wall(0, "z", 1, -5.5, 5.5, [door(-2.75), door(2.75)]),
    # Upper floor
    Wall(1, "x", 0, -7, 7, [door(-6), door(2)]),
    Wall(1, "z", 3, -5.5, 0, [door(-2.75)]),
    Wall(1, "z", 1, 0, 5.5, []),
]

WALLS = OUTER_WALLS + INNER_WALLS

# =============================================================================
# 2. HELPER FUNCTIONS
# =============================================================================

# Named groups of objects, so one button can change a whole group at once.
GROUP_NAMES = ["outer_walls", "siding", "upper_floor", "roof", "deck",
               "night_only", "day_only", "glass", "lamps", "fixtures"]
groups = {name: [] for name in GROUP_NAMES}

# Each object's starting position and opacity, so toggles can restore them.
originals = {}


def remember(obj):
    originals[id(obj)] = (vector(obj.pos), obj.opacity)


def register(obj, group_names):
    """Saves an object's starting values and adds it to the named groups."""
    remember(obj)
    for name in group_names:
        groups[name].append(obj)
    return obj


def make_box(group_names, **box_kwargs):
    return register(box(**box_kwargs), group_names)


def wall_segments(wall):
    """Splits a wall around its openings.

    Returns (start, end, y_bottom, y_top) pieces, with the solid parts between
    openings, plus the parts above and below each opening.
    """
    bottom = wall.level * FLOOR2_Y
    top = bottom + FLOOR2_Y
    pieces = []
    position = wall.start
    for opening in sorted(wall.openings):
        left = round(opening.center - opening.width / 2, 6)
        right = round(opening.center + opening.width / 2, 6)
        pieces.append((position, left, bottom, top))
        if opening.sill > 0:
            pieces.append((left, right, bottom, round(bottom + opening.sill, 6)))
        pieces.append((left, right, round(bottom + opening.top, 6), top))
        position = right
    pieces.append((position, wall.end, bottom, top))
    return pieces


def smoothstep(low, high, value):
    """Goes smoothly from 0 at low to 1 at high."""
    t = max(0, min(1, (value - low) / (high - low)))
    return t * t * (3 - 2 * t)


def rgb(red, green, blue):
    return vector(red, green, blue)


# =============================================================================
# 3. LAND AND SEA
# =============================================================================

HILLTOP_RADIUS = 13
TERRAIN_RINGS = 40
TERRAIN_SECTORS = 72
SEA_COLUMNS = 30
SEA_ROWS = 16
PINE_COUNT = 30
BUSH_COUNT = 12
FLOWER_COUNT = 150

SEA_BLUE = (0.09, 0.30, 0.52)

# Where the wooden stairs run from the veranda down the hillside.
STAIRS_X = 3
STAIRS_START_Z = 8.5
STAIRS_END_Z = 38

# Each animated sea point: (vertex object, x, z, how strongly it shimmers)
sea_points = []


def terrain_height(x, z):
    """Height of the ground: a flat hilltop, slopes, and a ring of mountains."""
    r = math.hypot(x, z)
    if r <= HILLTOP_RADIUS:
        return 0
    # How much this direction faces the sea: 0 on land, 1 toward the sea.
    sea_side = smoothstep(0.15, 0.55, z / r)
    land = -25 * smoothstep(HILLTOP_RADIUS, 100, r)
    shore = -45 * smoothstep(HILLTOP_RADIUS, 120, r)
    # Two ridges, with a height that changes around the circle.
    angle = math.atan2(x, z)
    near_ridge = 85 * math.exp(-((r - 190) / 45) ** 2) * (0.8 + 0.2 * math.sin(5 * angle + 1))
    far_ridge = 150 * math.exp(-((r - 290) / 55) ** 2) * (0.8 + 0.2 * math.sin(8 * angle))
    mountains = near_ridge + far_ridge
    bumps = (0.5 * math.sin(0.31 * x) * math.cos(0.27 * z)
             + 1.6 * math.sin(0.07 * x + 1) * math.sin(0.09 * z)) * smoothstep(HILLTOP_RADIUS, 30, r)
    return land * (1 - sea_side) + shore * sea_side + mountains * (1 - sea_side) + bumps


def wave_height(x, z, t):
    """Height of the water above sea level at time t."""
    return (0.35 * math.sin(0.09 * x + 0.05 * z + 1.1 * t)
            + 0.25 * math.sin(0.04 * x - 0.13 * z + 0.7 * t))


def terrain_color(x, y, z):
    """Sand near the water, grass on the slopes, and blue-gray far away."""
    shade = random.uniform(-0.04, 0.04)
    if y < SEA_Y + 3:
        red, green, blue = 0.62, 0.56, 0.40
    else:
        red, green, blue = 0.27 + shade, 0.50 + shade * 2, 0.17 + shade
    rocky = smoothstep(35, 75, y)
    red += (0.42 - red) * rocky
    green += (0.42 - green) * rocky
    blue += (0.40 - blue) * rocky
    haze = smoothstep(110, 300, math.hypot(x, z)) * 0.72
    return rgb(red + (0.55 - red) * haze, green + (0.66 - green) * haze, blue + (0.80 - blue) * haze)


def terrain_normal(x, z):
    step = 0.5
    slope_x = (terrain_height(x + step, z) - terrain_height(x - step, z)) / (2 * step)
    slope_z = (terrain_height(x, z + step) - terrain_height(x, z - step)) / (2 * step)
    return vector(-slope_x, 1, -slope_z).hat


def terrain_radii():
    """Ring sizes: close together near the house, far apart at the mountains."""
    radii = [0.05, 5, HILLTOP_RADIUS]
    steps = TERRAIN_RINGS - len(radii)
    growth = (400 / HILLTOP_RADIUS) ** (1 / steps)
    for i in range(1, steps + 1):
        radii.append(HILLTOP_RADIUS * growth ** i)
    return radii


def build_terrain():
    rings = []
    for radius in terrain_radii():
        ring = []
        for sector in range(TERRAIN_SECTORS):
            angle = 2 * math.pi * sector / TERRAIN_SECTORS
            x, z = radius * math.cos(angle), radius * math.sin(angle)
            y = terrain_height(x, z)
            ring.append(vertex(pos=vector(x, y, z), normal=terrain_normal(x, z),
                               color=terrain_color(x, y, z)))
        rings.append(ring)
    quads = []
    for inner, outer in zip(rings, rings[1:]):
        for sector in range(TERRAIN_SECTORS):
            following = (sector + 1) % TERRAIN_SECTORS
            quads.append(quad(vs=[inner[sector], outer[sector], outer[following], inner[following]]))
    return compound(quads, shininess=0)


def sea_color(shimmer_strength, height):
    """Lighter on wave tops. The edges match the plain sea underneath."""
    light = 0.16 * height * shimmer_strength
    return rgb(SEA_BLUE[0] + light, SEA_BLUE[1] + light, SEA_BLUE[2] + light)


def build_sea():
    cylinder(pos=vector(0, SEA_Y - 1, 0), axis=vector(0, 0.5, 0), radius=400,
             color=rgb(*SEA_BLUE), shininess=0.6)
    sea_points.clear()
    grid = []
    for row in range(SEA_ROWS):
        z = 60 + (380 - 60) * row / (SEA_ROWS - 1)
        line = []
        for column in range(SEA_COLUMNS):
            x = -260 + 520 * column / (SEA_COLUMNS - 1)
            strength = (smoothstep(0, 3, min(column, SEA_COLUMNS - 1 - column))
                        * smoothstep(0, 3, SEA_ROWS - 1 - row))
            point = vertex(pos=vector(x, SEA_Y, z), normal=vector(0, 1, 0),
                           color=sea_color(strength, 0))
            line.append(point)
            sea_points.append((point, x, z, strength))
        grid.append(line)
    for near, far in zip(grid, grid[1:]):
        for column in range(SEA_COLUMNS - 1):
            quad(vs=[near[column], near[column + 1], far[column + 1], far[column]])


def update_sea(t):
    for point, x, z, strength in sea_points:
        height = wave_height(x, z, t)
        point.pos = vector(x, SEA_Y + 0.4 + height * strength, z)
        point.color = sea_color(strength, height)


def build_distant_hills():
    """Low hills on the far side of the water."""
    for x, width, height in [(-250, 170, 11), (-90, 210, 15), (80, 150, 9), (235, 190, 13)]:
        ellipsoid(pos=vector(x * 0.9, SEA_Y, 345), size=vector(width, height * 2, 50),
                  color=rgb(0.52, 0.62, 0.72))


def plant_spots(count, min_radius, max_radius, tall=False):
    """Random spots on land, away from the house, veranda, and hillside stairs.

    Tall plants also stay out of the way of the front and sea-side views.
    """
    spots = []
    while len(spots) < count:
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(min_radius, max_radius)
        x, z = radius * math.cos(angle), radius * math.sin(angle)
        if -8 < x < 8 and -7 < z < 17:
            continue
        if abs(x - STAIRS_X) < 2.5 and 8 < z < STAIRS_END_Z + 2:
            continue
        if terrain_height(x, z) <= SEA_Y + 2:
            continue
        if tall and ((-28 < x < 6 and z < -6) or (-28 < x < 28 and z > 12)):
            continue
        spots.append((x, z))
    return spots


def pine_parts(x, z):
    scale = random.uniform(0.8, 1.4)
    y = terrain_height(x, z)
    parts = [cylinder(pos=vector(x, y, z), axis=vector(0, 2 * scale, 0), radius=0.3 * scale,
                      color=rgb(0.30, 0.20, 0.12), shininess=0)]
    green = rgb(0.07, random.uniform(0.25, 0.34), 0.15)
    for tier in range(3):
        parts.append(cone(pos=vector(x, y + (1.3 + 1.7 * tier) * scale, z),
                          axis=vector(0, (3.8 - 0.5 * tier) * scale, 0),
                          radius=(2.2 - 0.5 * tier) * scale, color=green, shininess=0))
    return parts


def bush_parts(x, z):
    y = terrain_height(x, z)
    parts = []
    for _ in range(6):
        parts.append(sphere(pos=vector(x + random.uniform(-0.9, 0.9), y + random.uniform(0.4, 1.1),
                                       z + random.uniform(-0.9, 0.9)),
                            radius=random.uniform(0.6, 0.95), color=rgb(0.20, 0.38, 0.17),
                            shininess=0))
    for _ in range(14):
        parts.append(sphere(pos=vector(x + random.uniform(-1.2, 1.2),
                                       y + random.uniform(0.7, 2),
                                       z + random.uniform(-1.2, 1.2)),
                            radius=random.uniform(0.15, 0.3),
                            color=rgb(0.90, random.uniform(0.38, 0.55), 0.70), shininess=0))
    return parts


def build_plants():
    pines = []
    for x, z in plant_spots(PINE_COUNT, 18, 75, tall=True):
        pines += pine_parts(x, z)
    compound(pines, shininess=0)
    bushes = []
    for x, z in plant_spots(BUSH_COUNT, 15, 34, tall=True):
        bushes += bush_parts(x, z)
    compound(bushes, shininess=0)
    flower_colors = [rgb(1, 1, 1), rgb(0.62, 0.48, 0.90), rgb(1, 0.85, 0.25)]
    flowers = []
    for x, z in plant_spots(FLOWER_COUNT, 14, 50):
        flowers.append(sphere(pos=vector(x, terrain_height(x, z) + 0.18, z), radius=0.09,
                              color=random.choice(flower_colors)))
    compound(flowers, shininess=0)


def build_land():
    build_terrain()
    build_sea()
    build_distant_hills()
    build_plants()


# =============================================================================
# 4. HOUSE EXTERIOR
# =============================================================================

WHITE_SIDING = rgb(0.93, 0.93, 0.90)
SIDING_LINE = rgb(0.80, 0.80, 0.78)
DARK_FRAME = rgb(0.13, 0.12, 0.13)
GLASS_DAY = rgb(0.55, 0.70, 0.80)
GLASS_OPACITY = 0.4
ROOF_DARK = rgb(0.24, 0.21, 0.20)
ROOF_LINE = rgb(0.17, 0.15, 0.15)
BRICK_RED = rgb(0.58, 0.20, 0.15)
MORTAR = rgb(0.42, 0.35, 0.32)
FLOOR_WOOD = rgb(0.55, 0.38, 0.23)

SIDING_SPACING = 0.4
FLOOR_TOP = 0.02    # Just above the grass, so the two surfaces don't flicker.


def upper_if(level, group_names):
    """Upper-floor parts also join upper_floor, so they lift with it."""
    return group_names + ["upper_floor"] if level == 1 else group_names


def wall_box(wall, start, end, bottom, top, thickness=WALL_THICK, offset=0, **kwargs):
    """Makes the arguments for a box that lies along a wall."""
    middle = (start + end) / 2
    height = (bottom + top) / 2
    if wall.axis == "x":
        pos = vector(middle, height, wall.fixed + offset)
        size = vector(end - start, top - bottom, thickness)
    else:
        pos = vector(wall.fixed + offset, height, middle)
        size = vector(thickness, top - bottom, end - start)
    return dict(pos=pos, size=size, **kwargs)


def outward(wall):
    """Which way the outside of an outer wall faces: +1 or -1."""
    return 1 if wall.fixed > 0 else -1


def build_outer_walls():
    for wall in OUTER_WALLS:
        for start, end, bottom, top in wall_segments(wall):
            make_box(upper_if(wall.level, ["outer_walls"]),
                     **wall_box(wall, start, end, bottom, top, color=WHITE_SIDING))
    # Corner boards fill the small gap where two walls meet.
    for x in (-HOUSE_X, HOUSE_X):
        for z in (-HOUSE_Z, HOUSE_Z):
            for level in (0, 1):
                make_box(upper_if(level, ["outer_walls"]),
                         pos=vector(x, (level + 0.5) * FLOOR2_Y, z),
                         size=vector(0.32, FLOOR2_Y, 0.32), color=WHITE_SIDING)


def build_siding():
    """Thin lines on the walls that look like long overlapping boards."""
    for wall in OUTER_WALLS:
        lines = []
        bottom = wall.level * FLOOR2_Y
        rows = int(FLOOR2_Y / SIDING_SPACING)
        for row in range(1, rows + 1):
            y = bottom + row * SIDING_SPACING - 0.1
            position = wall.start
            for opening in sorted(wall.openings):
                if bottom + opening.sill < y < bottom + opening.top:
                    lines.append(box(**wall_box(wall, position, opening.center - opening.width / 2,
                                                y, y + 0.035, thickness=0.02,
                                                offset=outward(wall) * 0.11, color=SIDING_LINE)))
                    position = opening.center + opening.width / 2
            lines.append(box(**wall_box(wall, position, wall.end, y, y + 0.035, thickness=0.02,
                                        offset=outward(wall) * 0.11, color=SIDING_LINE)))
        register(compound(lines), upper_if(wall.level, ["siding"]))


def build_windows_and_doors():
    for wall in OUTER_WALLS:
        side = outward(wall)
        bottom = wall.level * FLOOR2_Y
        frames = []
        for opening in wall.openings:
            left = opening.center - opening.width / 2
            right = opening.center + opening.width / 2
            base = bottom + opening.sill
            top = bottom + opening.top
            trim = dict(thickness=0.08, offset=side * 0.1, color=DARK_FRAME)
            frames.append(box(**wall_box(wall, left - 0.07, left + 0.03, base, top, **trim)))
            frames.append(box(**wall_box(wall, right - 0.03, right + 0.07, base, top, **trim)))
            frames.append(box(**wall_box(wall, left - 0.07, right + 0.07, top - 0.03, top + 0.07, **trim)))
            if opening.sill == 0:
                continue
            frames.append(box(**wall_box(wall, left - 0.1, right + 0.1, base - 0.07, base + 0.03, **trim)))
            frames.append(box(**wall_box(wall, left, right, (base + top) / 2 - 0.025, (base + top) / 2 + 0.025, **trim)))
            frames.append(box(**wall_box(wall, opening.center - 0.025, opening.center + 0.025, base, top, **trim)))
            make_box(upper_if(wall.level, ["glass"]),
                     **wall_box(wall, left, right, base, top, thickness=0.03, offset=side * 0.05,
                                color=GLASS_DAY, opacity=GLASS_OPACITY))
        register(compound(frames), upper_if(wall.level, []))


def build_floors():
    box(pos=vector(0, FLOOR_TOP - 0.1, 0), size=vector(14, 0.2, 11), color=FLOOR_WOOD, shininess=0.2)
    # The upper floor is four slabs around the hole for the stairs.
    slabs = [Rect(-HOUSE_X, -HOUSE_Z, HOUSE_X, STAIR_ZMIN),
             Rect(STAIR_HIGH_X, STAIR_ZMIN, HOUSE_X, STAIR_ZMAX),
             Rect(-HOUSE_X, STAIR_ZMIN, STAIR_LOW_X, STAIR_ZMAX),
             Rect(-HOUSE_X, STAIR_ZMAX, HOUSE_X, HOUSE_Z)]
    for slab in slabs:
        make_box(["upper_floor"],
                 pos=vector((slab.xmin + slab.xmax) / 2, FLOOR2_Y - 0.1, (slab.zmin + slab.zmax) / 2),
                 size=vector(slab.xmax - slab.xmin, 0.2, slab.zmax - slab.zmin),
                 color=FLOOR_WOOD, shininess=0.2)


def slope_slab(group_names, low, high, length, along, thickness=0.18, color=ROOF_DARK):
    """A flat roof panel that runs from a low edge up to a high edge.

    low and high are the middles of those edges. along says which way the
    panel's long edges run, and length is how long they are.
    """
    up_slope = high - low
    across = along.hat
    side = vector(across.y * up_slope.z - across.z * up_slope.y,
                  across.z * up_slope.x - across.x * up_slope.z,
                  across.x * up_slope.y - across.y * up_slope.x).hat
    if side.y < 0:
        side = side * -1
    return make_box(group_names, pos=(low + high) / 2, axis=across * length,
                    size=vector(length, thickness, up_slope.mag), up=side, color=color,
                    shininess=0.15)


def build_main_roof():
    overhang = 0.6
    run = HOUSE_Z
    rise = RIDGE_Y - WALL_TOP_Y
    eave_y = WALL_TOP_Y - overhang * rise / run
    lines = []
    for side in (-1, 1):
        low = vector(0, eave_y, side * (run + overhang))
        high = vector(0, RIDGE_Y, 0)
        slope_slab(["roof"], low, high, 2 * HOUSE_X + 2 * overhang, vector(1, 0, 0))
        # Rows of shingles.
        for row in range(1, 12):
            t = row / 12
            y = eave_y + (RIDGE_Y - eave_y) * t + 0.1
            z = side * (run + overhang) * (1 - t)
            lines.append(box(pos=vector(0, y, z), size=vector(2 * HOUSE_X + 2 * overhang, 0.03, 0.05),
                             color=ROOF_LINE))
    register(compound(lines), ["roof"])
    # A flat ceiling closes off the attic.
    make_box(["roof"], pos=vector(0, WALL_TOP_Y + 0.05, 0), size=vector(14, 0.1, 11), color=rgb(0.9, 0.9, 0.87))


def gable_triangle(left, right, peak, normal):
    corners = [vertex(pos=point, normal=normal, color=WHITE_SIDING) for point in (left, right, peak)]
    return triangle(vs=corners)


def build_gables():
    """The triangular wall sections under the ends of the roof."""
    triangles = []
    for x in (-HOUSE_X, HOUSE_X):
        triangles.append(gable_triangle(vector(x, WALL_TOP_Y, -HOUSE_Z), vector(x, WALL_TOP_Y, HOUSE_Z),
                                        vector(x, RIDGE_Y, 0), vector(1 if x > 0 else -1, 0, 0)))
    # Cross gable: the second, forward-facing roof section over the front.
    center = -2
    half = 3
    peak_y = 10
    triangles.append(gable_triangle(vector(center - half, WALL_TOP_Y, -HOUSE_Z),
                                    vector(center + half, WALL_TOP_Y, -HOUSE_Z),
                                    vector(center, peak_y, -HOUSE_Z), vector(0, 0, -1)))
    register(compound(triangles), ["roof"])
    overhang = 0.6
    ridge_end_z = -(RIDGE_Y - peak_y) * HOUSE_Z / (RIDGE_Y - WALL_TOP_Y)
    front_z = -HOUSE_Z - overhang
    length = ridge_end_z - front_z
    middle_z = (ridge_end_z + front_z) / 2
    eave_drop = overhang * (peak_y - WALL_TOP_Y) / half
    for side in (-1, 1):
        low = vector(center + side * (half + overhang), WALL_TOP_Y - eave_drop, middle_z)
        slope_slab(["roof"], low, vector(center, peak_y, middle_z), length, vector(0, 0, 1))
    # Small attic windows.
    for pos, thin_axis in [(vector(center, 8.1, -HOUSE_Z - 0.03), "z"),
                           (vector(-HOUSE_X - 0.03, 8.8, 0), "x"),
                           (vector(HOUSE_X + 0.03, 8.8, 0), "x")]:
        frame_size = vector(1.2, 1.3, 0.05) if thin_axis == "z" else vector(0.05, 1.3, 1.2)
        pane_size = vector(0.9, 1.0, 0.08) if thin_axis == "z" else vector(0.08, 1.0, 0.9)
        make_box(["roof"], pos=pos, size=frame_size, color=DARK_FRAME)
        make_box(["roof", "glass"], pos=pos, size=pane_size, color=GLASS_DAY, opacity=0.9)


def build_chimney(x, z, bottom, top, group_names):
    make_box(group_names, pos=vector(x, (bottom + top) / 2, z), size=vector(0.9, top - bottom, 1.2),
             color=BRICK_RED, shininess=0.05)
    bands = []
    y = bottom + 0.35
    while y < top:
        bands.append(box(pos=vector(x, y, z), size=vector(0.92, 0.03, 1.22), color=MORTAR))
        y += 0.35
    register(compound(bands), group_names)


def build_chimneys():
    # The side chimney runs up the outside wall from the living room fireplace.
    build_chimney(-7.55, 2.75, 0, FLOOR2_Y, [])
    build_chimney(-7.55, 2.75, FLOOR2_Y, 12.5, ["roof"])
    build_chimney(5, -2.5, WALL_TOP_Y, 12.5, ["roof"])
    for x, z in [(-7.55, 2.75), (5, -2.5)]:
        make_box(["roof"], pos=vector(x, 12.55, z), size=vector(1.1, 0.15, 1.4), color=MORTAR)


def build_entry():
    """Small roof over the front door, and the door itself standing open."""
    center = -2
    slope_slab([], vector(center, 2.75, -7.3), vector(center, 3.3, -HOUSE_Z), 3.4, vector(1, 0, 0))
    for side in (-1, 1):
        cylinder(pos=vector(center + side * 1.5, 0, -7.1), axis=vector(0, 2.85, 0), radius=0.07,
                 color=WHITE_SIDING)
    box(pos=vector(center - DOOR_WIDTH / 2 - 0.03, DOOR_TOP / 2, -HOUSE_Z - DOOR_WIDTH / 2 - 0.1),
        size=vector(0.06, DOOR_TOP - 0.02, DOOR_WIDTH), color=rgb(0.20, 0.25, 0.30))


def hillside_stair_spots():
    """The z position of each step going down the hill."""
    count = int((STAIRS_END_Z - STAIRS_START_Z) / 0.7)
    return [STAIRS_START_Z + 0.35 + 0.7 * step for step in range(count)]


def build_railing(start, end, group_names, top=0.95):
    """A white rail with thin posts, from one point on the floor to another."""
    run = end - start
    parts = [box(pos=(start + end) / 2 + vector(0, top, 0), axis=run,
                 size=vector(run.mag, 0.06, 0.08), color=WHITE_SIDING)]
    count = max(1, int(run.mag / 0.35))
    for post in range(count + 1):
        spot = start + run * (post / count)
        parts.append(box(pos=spot + vector(0, top / 2, 0), size=vector(0.05, top, 0.05),
                         color=WHITE_SIDING))
    register(compound(parts), group_names)


def build_veranda():
    west, east = -1, 7
    box(pos=vector((west + east) / 2, FLOOR_TOP - 0.1, 7), size=vector(east - west, 0.2, 3),
        color=FLOOR_WOOD, shininess=0.2)
    # Posts stay on the ground. The deck above rests on them.
    for x, z in [(west + 0.1, 8.4), (1.2, 8.4), (4.8, 8.4), (east - 0.1, 8.4),
                 (west + 0.1, 5.7), (east - 0.1, 5.7)]:
        cylinder(pos=vector(x, 0, z), axis=vector(0, FLOOR2_Y - 0.2, 0), radius=0.1,
                 color=WHITE_SIDING)
    # Railings, with a gap at the top of the hillside stairs.
    gap = DOOR_WIDTH / 2
    build_railing(vector(west, 0, 8.5), vector(STAIRS_X - gap, 0, 8.5), [])
    build_railing(vector(STAIRS_X + gap, 0, 8.5), vector(east, 0, 8.5), [])
    build_railing(vector(east, 0, 5.6), vector(east, 0, 8.5), [])
    steps = []
    for z in hillside_stair_spots():
        y = terrain_height(STAIRS_X, z)
        steps.append(box(pos=vector(STAIRS_X, y + 0.04, z), size=vector(DOOR_WIDTH, 0.14, 0.62),
                         color=rgb(0.42, 0.30, 0.20), shininess=0.1))
    compound(steps)


def build_exterior():
    build_floors()
    build_outer_walls()
    build_siding()
    build_windows_and_doors()
    build_main_roof()
    build_gables()
    build_chimneys()
    build_entry()
    build_veranda()


# =============================================================================
# 5. ROOMS AND FURNITURE
# =============================================================================

INNER_WALL = rgb(0.90, 0.86, 0.76)
WOOD = rgb(0.45, 0.29, 0.16)
DARK_WOOD = rgb(0.28, 0.17, 0.10)
FABRIC_BLUE = rgb(0.25, 0.38, 0.55)
FABRIC_RED = rgb(0.62, 0.25, 0.22)
LINEN = rgb(0.93, 0.91, 0.85)
COUNTER = rgb(0.80, 0.78, 0.72)
STEEL = rgb(0.62, 0.64, 0.66)
PORCELAIN = rgb(0.95, 0.96, 0.97)
TILE = rgb(0.68, 0.74, 0.76)

# Everything drawn in this section, for checking which floor it belongs to.
room_parts = []
# The small bulbs on the deck.
string_lights = []

# One entry per piece of furniture: (floor, parts).
# Each part is (x, height above the floor, z, width x, height, depth z, color).
FURNITURE = [
    # ---------- Entry hall ----------
    (0, [(-2, 0, -3.6, 2.2, 0.02, 3, FABRIC_RED)]),                        # rug
    (0, [(0.35, 0, -5.1, 1.1, 0.8, 0.6, WOOD)]),    # side table
    (0, [(-6.65, 0, -4.4, 0.5, 0.5, 1.4, DARK_WOOD)]),  # bench
    # ---------- Living room ----------
    (0, [
        (-6.7, 0, 2.75, 0.5, 1.7, 1.8, BRICK_RED),           # fireplace
        (-6.46, 0.15, 2.75, 0.04, 0.8, 1.0, rgb(0.04, 0.03, 0.03)),  # firebox
        (-6.65, 1.7, 2.75, 0.7, 0.1, 2.1, DARK_WOOD),        # mantel
    ]),
    (0, [(-4.3, 0, 2.75, 2.8, 0.02, 3.2, FABRIC_BLUE)]),                   # rug
    (0, [(-4.95, 0, 2.75, 0.7, 0.4, 1.2, WOOD)]),  # coffee table
    (0, [
        (-3, 0, 2.75, 1.0, 0.45, 2.3, FABRIC_RED),           # sofa seat
        (-2.65, 0.45, 2.75, 0.3, 0.45, 2.3, FABRIC_RED),     # sofa back
        (-3, 0.45, 1.75, 1.0, 0.25, 0.3, FABRIC_RED),        # sofa arm
        (-3, 0.45, 3.75, 1.0, 0.25, 0.3, FABRIC_RED),        # sofa arm
    ]),
    (0, [(0.65, 0, 0.85, 0.45, 2.1, 1.5, DARK_WOOD)]),  # bookshelf
    (0, [(0.41, 0.75, 0.85, 0.02, 0.3, 1.3, FABRIC_BLUE),                  # book rows
               (0.41, 1.4, 0.85, 0.02, 0.3, 1.3, FABRIC_RED)]),
    (0, [
        (-5.6, 0, 5.05, 0.15, 1.5, 0.15, DARK_WOOD),         # floor lamp pole
        (-5.6, 1.5, 5.05, 0.5, 0.35, 0.5, LINEN),            # lamp shade
    ]),
    # ---------- Kitchen ----------
    (0, [(4, 0.005, -2.75, 5.9, 0.01, 5.3, TILE)]),                        # tile floor
    (0, [(6.6, 0, -3.2, 0.6, 0.9, 4.4, COUNTER)]),     # side counter
    (0, [(4.15, 0, -5.1, 4.3, 0.9, 0.6, COUNTER)]),    # front counter
    (0, [
        (3, 0.9, -5.1, 0.7, 0.02, 0.45, STEEL),              # sink
        (3, 0.92, -5.28, 0.05, 0.3, 0.05, STEEL),            # faucet
        (6.6, 0.9, -2.75, 0.55, 0.03, 0.75, rgb(0.08, 0.08, 0.09)),  # stove top
    ]),
    (0, [(6.42, 0, -0.55, 0.95, 2.0, 0.8, STEEL)]),  # fridge
    # ---------- Dining room ----------
    (0, [
        (4, 0.72, 3.2, 2.4, 0.06, 1.1, WOOD),                # table top
        (4, 0, 3.2, 0.3, 0.72, 0.5, DARK_WOOD),              # table leg
        (3, 0.42, 2.35, 0.45, 0.06, 0.45, DARK_WOOD),        # chair seats and backs
        (3, 0, 2.35, 0.08, 0.42, 0.08, DARK_WOOD),
        (3, 0.42, 2.14, 0.45, 0.55, 0.05, DARK_WOOD),
        (5, 0.42, 2.35, 0.45, 0.06, 0.45, DARK_WOOD),
        (5, 0, 2.35, 0.08, 0.42, 0.08, DARK_WOOD),
        (5, 0.42, 2.14, 0.45, 0.55, 0.05, DARK_WOOD),
        (3, 0.42, 4.05, 0.45, 0.06, 0.45, DARK_WOOD),
        (3, 0, 4.05, 0.08, 0.42, 0.08, DARK_WOOD),
        (3, 0.42, 4.26, 0.45, 0.55, 0.05, DARK_WOOD),
        (5, 0.42, 4.05, 0.45, 0.06, 0.45, DARK_WOOD),
        (5, 0, 4.05, 0.08, 0.42, 0.08, DARK_WOOD),
        (5, 0.42, 4.26, 0.45, 0.55, 0.05, DARK_WOOD),
    ]),
    (0, [(6.65, 0, 2.75, 0.5, 0.9, 1.9, DARK_WOOD)]),  # sideboard
    # ---------- Landing ----------
    (1, [(-6.5, 0, -5.05, 0.8, 0.75, 0.7, WOOD)]),  # side table
    (1, [(-3.1, 0, -5.1, 0.8, 1.8, 0.5, DARK_WOOD)]),  # shelf
    (1, [
        (2.35, 0, -5, 0.5, 0.45, 0.5, BRICK_RED),            # plant pot
        (2.35, 0.45, -5, 0.65, 0.8, 0.65, rgb(0.20, 0.42, 0.18)),  # plant
    ]),
    # ---------- Bathroom ----------
    (1, [(5, 0.005, -2.75, 3.9, 0.01, 5.3, TILE)]),                        # tile floor
    (1, [
        (5.95, 0, -0.55, 1.9, 0.55, 0.9, PORCELAIN),         # tub
        (5.95, 0.5, -0.55, 1.6, 0.06, 0.6, rgb(0.55, 0.75, 0.85)),  # water
    ]),
    (1, [
        (6.45, 0, -4.8, 0.7, 0.42, 0.55, PORCELAIN),         # toilet
        (6.75, 0.42, -4.8, 0.2, 0.5, 0.55, PORCELAIN),       # tank
    ]),
    (1, [
        (4, 0, -5.15, 1.2, 0.8, 0.5, WOOD),                  # sink cabinet
        (4, 0.8, -5.15, 0.6, 0.06, 0.38, PORCELAIN),         # sink
        (4, 1.1, -5.38, 0.8, 0.9, 0.02, rgb(0.75, 0.86, 0.92)),  # mirror
    ]),
    # ---------- Bedroom 2 ----------
    (1, [(-2.5, 0, 2.4, 3, 0.02, 2.6, FABRIC_BLUE)]),                      # rug
    (1, [
        (-3, 0, 4.3, 1.8, 0.45, 2.2, DARK_WOOD),             # bed frame
        (-3, 0.45, 4.2, 1.7, 0.2, 2.0, LINEN),               # mattress
        (-3, 0.65, 3.85, 1.72, 0.05, 1.25, FABRIC_BLUE),     # blanket
        (-3, 0.65, 4.95, 1.3, 0.14, 0.45, PORCELAIN),        # pillow
        (-3, 0, 5.38, 1.8, 0.95, 0.08, DARK_WOOD),           # headboard
    ]),
    (1, [(-1.65, 0, 5.08, 0.6, 0.55, 0.6, WOOD)]),    # nightstand
    (1, [(0.62, 0, 1.2, 0.6, 2.0, 1.4, DARK_WOOD)]),  # wardrobe
    # ---------- Bedroom 1, with the doorway to the deck ----------
    (1, [
        (5.85, 0, 2.4, 2.2, 0.45, 1.8, DARK_WOOD),           # bed frame
        (5.75, 0.45, 2.4, 2.0, 0.2, 1.7, LINEN),             # mattress
        (5.4, 0.65, 2.4, 1.25, 0.05, 1.72, FABRIC_RED),      # blanket
        (6.45, 0.65, 2.4, 0.45, 0.14, 1.3, PORCELAIN),       # pillow
        (6.88, 0, 2.4, 0.08, 0.95, 1.8, DARK_WOOD),          # headboard
    ]),
    (1, [(6.62, 0, 3.75, 0.6, 0.55, 0.6, WOOD)]),     # nightstand
    (1, [(1.42, 0, 4.6, 0.6, 2.0, 1.4, DARK_WOOD)]),  # wardrobe
]

# One ceiling light per room: (floor, x, z)
CEILING_LIGHTS = [(0, -3, -2.75), (0, -3, 2.75), (0, 4, -2.75), (0, 4, 2.75),
                  (1, -3, -2.75), (1, 5, -2.75), (1, -3, 2.75), (1, 4, 2.75)]


def add_furniture(level, parts):
    floor_y = level * FLOOR2_Y + FLOOR_TOP
    for x, height, z, width, tall, depth, part_color in parts:
        part = make_box(upper_if(level, []), pos=vector(x, floor_y + height + tall / 2, z),
                        size=vector(width, tall, depth), color=part_color, shininess=0.2)
        room_parts.append(part)


def build_inner_walls():
    for wall in INNER_WALLS:
        for start, end, bottom, top in wall_segments(wall):
            make_box(upper_if(wall.level, []),
                     **wall_box(wall, start, end, bottom, top, color=INNER_WALL, shininess=0.1))


def build_stairs():
    steps = 16
    run = (STAIR_HIGH_X - STAIR_LOW_X) / steps
    width = STAIR_ZMAX - STAIR_ZMIN
    middle_z = (STAIR_ZMIN + STAIR_ZMAX) / 2
    for step in range(steps):
        top = FLOOR2_Y * (step + 1) / steps
        room_parts.append(box(pos=vector(STAIR_LOW_X + run * (step + 0.5), top / 2, middle_z),
                              size=vector(run, top, width), color=WOOD, shininess=0.2))
    # Slanted handrail with posts on the stairs themselves.
    rail_height = 0.9
    cylinder(pos=vector(STAIR_LOW_X, rail_height, STAIR_ZMIN),
             axis=vector(STAIR_HIGH_X - STAIR_LOW_X, FLOOR2_Y, 0), radius=0.04, color=WHITE_SIDING)
    for step in range(0, steps, 3):
        x = STAIR_LOW_X + run * (step + 0.5)
        floor_y = FLOOR2_Y * (step + 1) / steps
        cylinder(pos=vector(x, floor_y, STAIR_ZMIN), axis=vector(0, rail_height, 0), radius=0.03,
                 color=WHITE_SIDING)
    # Guard rails around the opening on the upper floor.
    rails = [Rect(STAIR_LOW_X, STAIR_ZMIN - 0.03, STAIR_HIGH_X, STAIR_ZMIN + 0.03),
             Rect(STAIR_LOW_X - 0.03, STAIR_ZMIN, STAIR_LOW_X + 0.03, 0)]
    for rail in rails:
        make_box(["upper_floor"],
                 pos=vector((rail.xmin + rail.xmax) / 2, FLOOR2_Y + 0.92, (rail.zmin + rail.zmax) / 2),
                 size=vector(rail.xmax - rail.xmin, 0.06, rail.zmax - rail.zmin), color=WHITE_SIDING)
        make_box(["upper_floor"],
                 pos=vector((rail.xmin + rail.xmax) / 2, FLOOR2_Y + 0.45, (rail.zmin + rail.zmax) / 2),
                 size=vector(rail.xmax - rail.xmin, 0.9, rail.zmax - rail.zmin),
                 color=WHITE_SIDING, opacity=0.35)


def build_room_lights():
    """One real light per floor, and a glowing fixture on each room's ceiling."""
    for level, y in ((0, FLOOR2_Y - 0.5), (1, WALL_TOP_Y - 0.5)):
        lamp = local_light(pos=vector(0, y, 0), color=color.black)
        register(lamp, upper_if(level, ["lamps"]))
    for level, x, z in CEILING_LIGHTS:
        y = (level + 1) * FLOOR2_Y - 0.2 - (0.1 if level == 0 else 0.05)
        fixture = sphere(pos=vector(x, y, z), radius=0.18, color=LINEN)
        # The ceiling is the upper floor's underside, so every fixture lifts with it.
        register(fixture, ["fixtures", "upper_floor"])


def build_fire():
    """Flames in the fireplace, lit at night."""
    flame = ellipsoid(pos=vector(-6.42, 0.5, 2.75), size=vector(0.12, 0.65, 0.7),
                      color=rgb(1, 0.5, 0.12), emissive=True)
    groups["night_only"].append(flame)


def build_rooms():
    room_parts.clear()
    build_inner_walls()
    build_stairs()
    for level, parts in FURNITURE:
        add_furniture(level, parts)
    build_room_lights()
    build_fire()


# =============================================================================
# 6. STARGAZING DECK
# =============================================================================

DECK_WEST = -1
DECK_EAST = 7
DECK_FRONT_Z = 8.5
BULB_WARM = rgb(1, 0.82, 0.48)


def deck_box(**box_kwargs):
    return make_box(["deck"], **box_kwargs)


def build_lounge_chair(x, z):
    floor_y = FLOOR2_Y
    cushion = rgb(0.86, 0.80, 0.68)
    deck_box(pos=vector(x, floor_y + 0.3, z), size=vector(0.7, 0.1, 1.2), color=cushion)
    # The backrest leans back, so you can look up at the sky.
    deck_box(pos=vector(x, floor_y + 0.62, z - 0.82), size=vector(0.75, 0.1, 0.7),
             up=vector(0, 0.55, 0.55), color=cushion)
    for side_x in (x - 0.3, x + 0.3):
        for leg_z in (z - 0.5, z + 0.5):
            deck_box(pos=vector(side_x, floor_y + 0.13, leg_z), size=vector(0.06, 0.26, 0.06),
                     color=DARK_WOOD)


def build_telescope(x, z):
    floor_y = FLOOR2_Y
    head = vector(x, floor_y + 1.2, z)
    for dx, dz in [(0.4, 0), (-0.25, 0.32), (-0.25, -0.32)]:
        foot = vector(x + dx, floor_y, z + dz)
        register(cylinder(pos=foot, axis=head - foot, radius=0.025, color=rgb(0.15, 0.15, 0.17)),
                 ["deck"])
    # The tube points up over the sea.
    direction = vector(-0.2, 0.6, 0.77).hat
    register(cylinder(pos=head - direction * 0.55, axis=direction * 1.3, radius=0.09,
                      color=rgb(0.86, 0.87, 0.90), shininess=0.7), ["deck"])
    register(cylinder(pos=head + direction * 0.75, axis=direction * 0.12, radius=0.11,
                      color=rgb(0.12, 0.12, 0.14)), ["deck"])
    register(cylinder(pos=head - direction * 0.67, axis=direction * 0.12, radius=0.05,
                      color=rgb(0.12, 0.12, 0.14)), ["deck"])


def build_string_lights():
    string_lights.clear()
    height = FLOOR2_Y + 1.45
    corners = [vector(DECK_WEST, height, 5.7), vector(DECK_WEST, height, DECK_FRONT_Z),
               vector(DECK_EAST, height, DECK_FRONT_Z), vector(DECK_EAST, height, 5.7)]
    for corner in corners:
        deck_box(pos=corner - vector(0, 0.72, 0), size=vector(0.05, 1.45, 0.05), color=WHITE_SIDING)
    for start, end in zip(corners, corners[1:]):
        register(cylinder(pos=start, axis=end - start, radius=0.008, color=rgb(0.1, 0.1, 0.1)),
                 ["deck"])
        count = int((end - start).mag / 0.8)
        for bulb in range(1, count):
            spot = start + (end - start) * (bulb / count) - vector(0, 0.07, 0)
            light = sphere(pos=spot, radius=0.04, color=BULB_WARM)
            string_lights.append(register(light, ["deck"]))


def build_deck():
    middle_x = (DECK_WEST + DECK_EAST) / 2
    middle_z = (HOUSE_Z + DECK_FRONT_Z) / 2
    width = DECK_EAST - DECK_WEST
    depth = DECK_FRONT_Z - HOUSE_Z
    # This floor is also the veranda's roof.
    deck_box(pos=vector(middle_x, FLOOR2_Y - 0.1, middle_z), size=vector(width, 0.2, depth),
             color=rgb(0.56, 0.40, 0.25), shininess=0.15)
    planks = []
    for row in range(1, int(depth / 0.3)):
        planks.append(box(pos=vector(middle_x, FLOOR2_Y + 0.003, HOUSE_Z + row * 0.3),
                          size=vector(width, 0.006, 0.025), color=rgb(0.34, 0.23, 0.14)))
    register(compound(planks), ["deck"])
    floor = vector(0, FLOOR2_Y, 0)
    build_railing(floor + vector(DECK_WEST, 0, 5.6), floor + vector(DECK_WEST, 0, DECK_FRONT_Z), ["deck"])
    build_railing(floor + vector(DECK_WEST, 0, DECK_FRONT_Z), floor + vector(DECK_EAST, 0, DECK_FRONT_Z), ["deck"])
    build_railing(floor + vector(DECK_EAST, 0, DECK_FRONT_Z), floor + vector(DECK_EAST, 0, 5.6), ["deck"])
    # Two chairs facing the sea, with a small table between them.
    build_lounge_chair(0.3, 7.3)
    build_lounge_chair(2.1, 7.3)
    deck_box(pos=vector(1.2, FLOOR2_Y + 0.45, 7.4), size=vector(0.5, 0.05, 0.5), color=DARK_WOOD)
    deck_box(pos=vector(1.2, FLOOR2_Y + 0.22, 7.4), size=vector(0.08, 0.44, 0.08), color=DARK_WOOD)
    build_telescope(5.5, 7.8)
    build_string_lights()


# =============================================================================
# 7. SKY, DAY/NIGHT, AND VIEW CONTROLS
# =============================================================================

STAR_COUNT = 1200
CLOUD_COUNT = 9
SKY_RADIUS = 360

SKY_DAY = rgb(0.55, 0.75, 0.95)
SKY_NIGHT = rgb(0.015, 0.025, 0.07)
SUN_DAY = rgb(0.78, 0.76, 0.70)
SUN_NIGHT = rgb(0.13, 0.15, 0.24)
FILL_DAY = rgb(0.34, 0.36, 0.40)
FILL_NIGHT = rgb(0.03, 0.03, 0.06)
AMBIENT_DAY = rgb(0.42, 0.42, 0.42)
AMBIENT_NIGHT = rgb(0.16, 0.17, 0.23)
WINDOW_GLOW = rgb(1, 0.80, 0.45)
# VPython lights shine through walls and don't fade with distance, so the room
# lamps stay soft. Any brighter and they light up the mountains too.
LAMP_GLOW = rgb(0.17, 0.14, 0.09)

sun = None
fill_light = None


def star_positions():
    """Spots for the stars, on a big dome above the horizon."""
    stars = random.Random(RANDOM_SEED)
    positions = []
    for _ in range(STAR_COUNT):
        angle = stars.uniform(0, 2 * math.pi)
        height = stars.uniform(0.03, 1)
        across = math.sqrt(1 - height * height)
        positions.append((SKY_RADIUS * across * math.cos(angle), SKY_RADIUS * height,
                          SKY_RADIUS * across * math.sin(angle)))
    return positions


def build_stars_and_moon():
    positions = [vector(x, y, z) for x, y, z in star_positions()]
    # Most stars are faint, and a few are bright.
    bright = points(pos=positions[:120], radius=1.0, size_units="world",
                    color=rgb(1, 1, 0.92), emissive=True)
    medium = points(pos=positions[120:500], radius=0.7, size_units="world",
                    color=rgb(0.85, 0.89, 1), emissive=True)
    faint = points(pos=positions[500:], radius=0.45, size_units="world",
                   color=rgb(0.66, 0.70, 0.86), emissive=True)
    moon = sphere(pos=vector(-110, 160, 270), radius=13, color=rgb(0.96, 0.95, 0.85), emissive=True)
    groups["night_only"] += [bright, medium, faint, moon]


def build_clouds():
    white = rgb(1, 1, 1)
    for _ in range(CLOUD_COUNT):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(130, 300)
        center = vector(distance * math.cos(angle), random.uniform(70, 125), distance * math.sin(angle))
        puffs = []
        for _ in range(7):
            brightness = random.uniform(0.9, 1)
            puffs.append(ellipsoid(pos=center + vector(random.uniform(-30, 30), random.uniform(-3, 7),
                                                       random.uniform(-14, 14)),
                                   size=vector(random.uniform(22, 38), random.uniform(14, 24),
                                               random.uniform(18, 30)),
                                   color=white * brightness, emissive=True))
        groups["day_only"].append(compound(puffs, emissive=True))


def build_sky():
    global sun, fill_light
    sun = distant_light(direction=vector(-0.5, 0.8, -0.6), color=SUN_DAY)
    fill_light = distant_light(direction=vector(0.45, 0.5, 0.8), color=FILL_DAY)
    build_stars_and_moon()
    build_clouds()
    apply_time_of_day(False)


def apply_time_of_day(is_night):
    """Switches the sky, lighting, stars, windows, and lamps."""
    scene.background = SKY_NIGHT if is_night else SKY_DAY
    scene.ambient = AMBIENT_NIGHT if is_night else AMBIENT_DAY
    sun.color = SUN_NIGHT if is_night else SUN_DAY
    fill_light.color = FILL_NIGHT if is_night else FILL_DAY
    for obj in groups["night_only"]:
        obj.visible = is_night
    for obj in groups["day_only"]:
        obj.visible = not is_night
    for pane in groups["glass"]:
        pane.color = WINDOW_GLOW if is_night else GLASS_DAY
        pane.emissive = is_night
    for light in groups["fixtures"] + string_lights:
        light.color = WINDOW_GLOW if is_night else LINEN
        light.emissive = is_night
    for lamp in groups["lamps"]:
        lamp.color = LAMP_GLOW if is_night else color.black


# ----- See-through walls and Open house -----

SEE_THROUGH_OPACITY = 0.25
OPEN_LIFT = 8
LIFTED_GROUPS = ["upper_floor", "roof", "deck"]

state = SimpleNamespace(see_through=False, opened=False, night=False)
buttons = {}


def reset_state():
    state.see_through = False
    state.opened = False
    state.night = False


def apply_house_state():
    """Sets the house to match the state, working from each object's starting
    values, so clicking many times can never make anything drift."""
    lift = vector(0, OPEN_LIFT if state.opened else 0, 0)
    moved = set()
    for name in LIFTED_GROUPS:
        for obj in groups[name]:
            if id(obj) not in moved:
                moved.add(id(obj))
                obj.pos = originals[id(obj)][0] + lift
    for wall in groups["outer_walls"]:
        wall.opacity = SEE_THROUGH_OPACITY if state.see_through else originals[id(wall)][1]
    for lines in groups["siding"]:
        lines.visible = not state.see_through
    refresh_labels()


def toggle_see_through():
    state.see_through = not state.see_through
    apply_house_state()


def toggle_open_house():
    state.opened = not state.opened
    apply_house_state()


def toggle_night():
    state.night = not state.night
    apply_time_of_day(state.night)
    refresh_labels()


# ----- Preset views -----

VIEW_FOV = math.pi / 4      # A little zoomed in, to frame the house.
WIDE_FOV = math.pi / 3      # A natural view for standing inside the house.
FIRST_PERSON_DISTANCE = 40  # VPython hides things nearer than 1/100 of the camera's
                            # distance and farther than 10 times it, so this
                            # shows everything from 0.4 m to 400 m away.


def camera_looking_at(eye, target, fov):
    """Returns (center, forward, range, fov) for a camera at eye."""
    offset = target - eye
    return (target, offset.hat, offset.mag * math.tan(fov / 2), fov)


def camera_from_eye(eye, forward, fov=WIDE_FOV):
    """Returns (center, forward, range, fov) for someone standing at eye."""
    direction = forward.hat
    return (eye + direction * FIRST_PERSON_DISTANCE, direction,
            FIRST_PERSON_DISTANCE * math.tan(fov / 2), fov)


VIEWS = {
    "front": camera_looking_at(vector(-16, 8, -40), vector(0, 5, 0), VIEW_FOV),
    "sea_side": camera_looking_at(vector(14, 6, 46), vector(3, 4, 6), VIEW_FOV),
    "aerial": camera_looking_at(vector(0, 90, -50), vector(0, 0, 0), VIEW_FOV),
    "stargazing": camera_from_eye(vector(3.2, 4.9, 5.9), vector(0, 0.27, 1)),
}


def room_camera(eye, target):
    """A close camera, so the mouse rotates it around the middle of the room."""
    return camera_looking_at(eye, target, WIDE_FOV)


# Each room: button name, label, and camera. Indoor cameras stand close to what
# they look at, so through a window they only see as far as the yard. The veranda
# and deck use the far-seeing camera, to keep the sea and stars in view.
GROUND_ROOMS = [
    ("entry_hall", "Entry hall", room_camera(vector(0.2, 1.6, -3.7), vector(-2.6, 1.2, -2.6))),
    ("living_room", "Living room", room_camera(vector(-5.6, 1.6, 0.9), vector(-3.5, 1.0, 2.6))),
    ("kitchen", "Kitchen", room_camera(vector(1.8, 1.6, -0.8), vector(4.2, 1.1, -3))),
    ("dining_room", "Dining room", room_camera(vector(1.8, 1.6, 0.8), vector(3.8, 1.0, 2.8))),
    ("veranda", "Veranda", camera_from_eye(vector(3, 1.6, 6.2), vector(0, 0, 1))),
]
UPPER_ROOMS = [
    ("landing", "Landing", room_camera(vector(2.4, 5, -3.8), vector(-0.3, 4.5, -2.4))),
    ("bedroom_1", "Bedroom 1", room_camera(vector(1.8, 5, 0.8), vector(4.2, 4.3, 2.6))),
    ("bedroom_2", "Bedroom 2", room_camera(vector(-0.4, 5, 0.8), vector(-2.6, 4.3, 3))),
    ("bathroom", "Bathroom", room_camera(vector(3.6, 5, -0.8), vector(5.2, 4.4, -3))),
    ("deck", "Deck", camera_from_eye(vector(6.3, 5, 6), vector(-0.75, 0.02, 0.66))),
]

CAMERAS = dict(VIEWS)
for room_name, _, room_view in GROUND_ROOMS + UPPER_ROOMS:
    CAMERAS[room_name] = room_view

# These cameras stand on the upper floor or deck, so they rise when it does.
RISES_WITH_UPPER_FLOOR = {"stargazing"} | {room[0] for room in UPPER_ROOMS}


def apply_camera(camera):
    center, forward, view_range, fov = camera
    scene.fov = fov
    scene.forward = forward
    scene.range = view_range
    scene.center = center


def set_view(name):
    center, forward, view_range, fov = CAMERAS[name]
    if name in RISES_WITH_UPPER_FLOOR and state.opened:
        center = center + vector(0, OPEN_LIFT, 0)
    apply_camera((center, forward, view_range, fov))


# ----- Buttons -----

def refresh_labels():
    if not buttons:
        return
    buttons["see_through"].text = "See-through walls: " + ("ON" if state.see_through else "off")
    buttons["open_house"].text = "Open house: " + ("ON" if state.opened else "off")
    buttons["night"].text = "Switch to day" if state.night else "Switch to night"


def add_room_row(title, rooms):
    scene.append_to_title("\n<b>" + title + ":</b>  ")
    for name, label, _ in rooms:
        add_button(name, lambda view=name: set_view(view))
        buttons[name].text = label
        scene.append_to_title("  ")


def add_button(name, click):
    # The buttons sit above the 3D view, so they fit on small screens too.
    buttons[name] = button(text=name, bind=lambda _: click(), pos=scene.title_anchor)


def build_controls():
    buttons.clear()
    scene.append_to_title("\n<b>House:</b>  ")
    add_button("see_through", toggle_see_through)
    scene.append_to_title("  ")
    add_button("open_house", toggle_open_house)
    scene.append_to_title("  ")
    add_button("night", toggle_night)
    scene.append_to_title("     <b>Views:</b>  ")
    for name, label in [("front", "Front"), ("sea_side", "Sea side"),
                        ("aerial", "Aerial"), ("stargazing", "Stargazing")]:
        add_button(name, lambda view=name: set_view(view))
        buttons[name].text = label
        scene.append_to_title("  ")
    add_room_row("Ground floor", GROUND_ROOMS)
    add_room_row("Upper floor", UPPER_ROOMS)
    scene.append_to_title("\n\n")
    scene.append_to_caption("\nDrag with the right mouse button to rotate, and scroll to zoom.\n")
    refresh_labels()


# =============================================================================
# 8. BUILDING THE SCENE AND RUNNING THE ANIMATION
# =============================================================================


def build_scene():
    """Creates every object in the scene."""
    random.seed(RANDOM_SEED)
    for members in groups.values():
        members.clear()
    originals.clear()
    reset_state()
    # Clear VPython's default lights first, since this removes every light so far.
    scene.lights = []
    build_land()
    build_rooms()
    build_exterior()
    build_deck()
    build_sky()


WAVE_UPDATE_SECONDS = 0.15
last_wave_update = None


def animation_step(now):
    """Runs one frame of animation. now is the time in seconds."""
    global last_wave_update
    if last_wave_update is None or now - last_wave_update >= WAVE_UPDATE_SECONDS:
        update_sea(now)
        last_wave_update = now


def setup_scene():
    scene.width = 1150
    scene.height = 560
    scene.autoscale = False
    scene.title = "Seaside Dream House"
    build_scene()
    build_controls()
    set_view("front")


def run_animation():
    start = time.time()
    while True:
        rate(30)
        animation_step(time.time() - start)


def main():
    setup_scene()
    run_animation()


if __name__ == "__main__":
    main()
