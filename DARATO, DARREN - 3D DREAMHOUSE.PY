"""
Modern 2-storey house in 3D (VPython): exterior, front yard, gates, and a fully furnished interior.

Install :  pip install vpython
Run     :  python modern_house_vpython.py   (opens in your browser)

Outside : right-drag = rotate, scroll = zoom, shift+drag = pan
Buttons : DAYLIGHT / NIGHT, camera views, gates, front door, garage door,
          CUTAWAY (hide roof / 2nd floor to look into the rooms)
Inside  : ENTER HOUSE or pick a room, then (click the 3D view first)
          W/S = forward/back, A/D = sidestep, Left/Right (or Q/E) = turn, Up/Down = look

Rooms - ground floor: foyer, living room, kitchen, dining, powder room, laundry, garage (with car), stairs
        second floor: master bedroom + bath + walk-in closet, bedroom 2 + ensuite, bedroom 3,
                      upper hall, covered lanai, balcony
Axes: x = right, y = up, z = toward the street (house front faces +z)
"""
from vpython import *

# ------------------------------------------------------------------ scene
SKY_DAY = vec(0.62, 0.76, 0.92)
SKY_NIGHT = vec(0.04, 0.06, 0.15)

scene = canvas(title="Modern House - VPython 3D", width=1200, height=680,
               background=SKY_DAY)
scene.autoscale = False   # keep the camera where we put it (house fills the view)
scene.lights = []
scene.ambient = color.gray(0.55)
sun = distant_light(direction=vec(0.35, -0.55, -1), color=color.gray(0.75))
fill = distant_light(direction=vec(-0.6, -0.3, -0.3), color=color.gray(0.25))

# ------------------------------------------------------------------ colors
DARK   = vec(0.36, 0.37, 0.39)
CHAR   = vec(0.22, 0.23, 0.25)
BLACK  = vec(0.07, 0.07, 0.08)
CONC   = vec(0.62, 0.62, 0.60)
PALE   = vec(0.72, 0.72, 0.70)
GLASS  = vec(0.60, 0.78, 0.88)
WARM   = vec(1.00, 0.86, 0.55)    # light ON
LAMP_OFF = vec(0.78, 0.76, 0.68)  # light OFF (daytime)
INTER  = vec(0.93, 0.78, 0.55)    # interior lit
INTER_DAY = vec(0.50, 0.46, 0.42) # interior in daytime
GRASS  = vec(0.25, 0.58, 0.20)
HEDGE  = vec(0.15, 0.42, 0.16)
LEAF   = vec(0.14, 0.50, 0.20)
TRUNK  = vec(0.45, 0.35, 0.25)
WOOD   = vec(0.45, 0.28, 0.14)

LIGHTS = []   # fixtures that glow at night
GLOWS = []    # (unused)
ROOF = []     # objects above y=9 (hidden in cutaway)
UPPER = []    # objects of the 2nd floor (hidden in cutaway 2)


def tag(o, ymin):
    if ymin >= 9.0:
        ROOF.append(o)
    elif ymin >= 4.4:
        UPPER.append(o)
    return o


def blk(x0, x1, y0, y1, z0, z1, col=DARK, op=1.0):
    o = box(pos=vec((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
            size=vec(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)),
            color=col, opacity=op)
    return tag(o, min(y0, y1))


def led(x0, x1, y0, y1, z0, z1):
    o = blk(x0, x1, y0, y1, z0, z1, LAMP_OFF)
    LIGHTS.append(o)
    return o


def glow(x0, x1, y0, y1, z0, z1):
    o = blk(x0, x1, y0, y1, z0, z1, INTER_DAY)
    GLOWS.append(o)
    return o


def glass(x0, x1, y0, y1, z, mullions=0):
    blk(x0, x1, y0, y1, z - 0.03, z + 0.03, GLASS, 0.28)
    blk(x0, x1, y0, y0 + 0.06, z - 0.05, z + 0.05, BLACK)
    blk(x0, x1, y1 - 0.06, y1, z - 0.05, z + 0.05, BLACK)
    blk(x0, x0 + 0.06, y0, y1, z - 0.05, z + 0.05, BLACK)
    blk(x1 - 0.06, x1, y0, y1, z - 0.05, z + 0.05, BLACK)
    for i in range(1, mullions + 1):
        x = x0 + (x1 - x0) * i / (mullions + 1)
        blk(x - 0.03, x + 0.03, y0, y1, z - 0.05, z + 0.05, BLACK)


def downlight(x, y, z):
    o = cylinder(pos=vec(x, y, z), axis=vec(0, -0.06, 0), radius=0.13,
                 color=LAMP_OFF)
    LIGHTS.append(o)
    tag(o, y)


def palm(x, z, h, y0=0.0, lean=0.0):
    top = vec(x + lean, y0 + h, z)
    cylinder(pos=vec(x, y0, z), axis=vec(lean, h, 0), radius=0.22, color=TRUNK)
    n = 9
    for i in range(n):
        a = i * 2 * pi / n
        d = vec(cos(a), 0, sin(a))
        ellipsoid(pos=top + d * 1.3 + vec(0, -0.35, 0),
                  axis=d * 3.0 + vec(0, -0.7, 0),
                  height=0.08, width=0.7, color=LEAF)
    sphere(pos=top, radius=0.3, color=LEAF)


def small_plant(x, y, z, s=1.0):
    for i in range(7):
        a = i * 2 * pi / 7
        d = vec(cos(a), 0, sin(a))
        tag(ellipsoid(pos=vec(x, y + 0.5 * s, z) + d * 0.35 * s + vec(0, 0.15 * s, 0),
                      axis=d * 1.1 * s + vec(0, 0.9 * s, 0),
                      height=0.06, width=0.25 * s, color=LEAF), y)


def shrub(x, y, z, r):
    sphere(pos=vec(x, y + r * 0.6, z), radius=r, color=HEDGE)


# ================================================================ GROUND
blk(-17, 17, -0.5, 0, -13, 9.2, GRASS)
blk(-17, 17, -0.5, 0.10, 9.2, 11.8, vec(0.80, 0.80, 0.78))     # sidewalk
blk(-17, 17, -0.5, 0.15, 11.8, 12.1, vec(0.70, 0.70, 0.68))    # curb
blk(-17, 17, -0.5, 0.02, 12.1, 18, vec(0.25, 0.26, 0.28))      # street

# driveway + joints
blk(4.8, 10.8, 0, 0.05, 0, 9.2, PALE)
blk(4.8, 10.8, 0, 0.08, 9.2, 12.1, PALE)
for z in range(2, 12, 2):
    blk(4.8, 10.8, 0.05, 0.07, z, z + 0.05, vec(0.45, 0.45, 0.44))
blk(7.75, 7.8, 0.05, 0.07, 0, 9.2, vec(0.45, 0.45, 0.44))

# paving strip + path to the pedestrian gate
blk(-12.2, 4.8, 0, 0.05, 5.0, 5.5, PALE)
blk(-2.4, -0.6, 0, 0.05, 5.5, 9.2, PALE)
for z in [6.5, 7.5, 8.5]:
    blk(-2.4, -0.6, 0.05, 0.07, z, z + 0.04, vec(0.45, 0.45, 0.44))
blk(-3.2, 3.2, 0, 0.05, 4.0, 5.0, vec(0.66, 0.66, 0.64))

# ================================================================ HOUSE BODY
blk(-11.3, 4.8, 0, 0.5, -10, 2.0, vec(0.55, 0.55, 0.55))
blk(-11.3, 11.7, 0, 13.4, -10.2, -10.0, DARK)
blk(-11.3, -11.1, 0, 10.55, -10, 2.2, DARK)
blk(11.5, 11.7, 0, 11.4, -10, 1.6, DARK)

# ---------------------------------------------------- GROUND FLOOR (left)
blk(-11.1, -7.7, 0.5, 4.6, -1.5, -0.9, CHAR)
blk(-7.7, 3.0, 3.9, 4.6, -1.2, -0.9, CHAR)
blk(-1.8, -0.7, 0.5, 3.9, -1.2, -0.9, CHAR)
blk(0.8, 1.2, 0.5, 3.9, -1.2, -0.9, CHAR)
blk(2.7, 3.0, 0.5, 3.9, -1.2, -0.9, CHAR)

glass(-7.7, -1.8, 0.5, 3.9, -1.0, mullions=2)

# front door
DOOR = compound([blk(-0.7, 0.8, 0.5, 3.9, -1.05, -0.95, BLACK),
                 blk(-0.58, -0.52, 1.1, 2.9, -0.95, -0.91, vec(0.85, 0.85, 0.85))])
led(-1.45, -1.30, 2.2, 3.3, -0.90, -0.82)                   # wall lamp
blk(-0.7, 0.8, 3.9, 4.6, -1.2, -0.9, CHAR)

# side window
glass(1.2, 2.7, 0.5, 3.9, -1.0)

blk(-9.4, -8.8, 0.5, 4.6, 1.2, 1.8, vec(0.58, 0.58, 0.58))

# ---------------------------------------------------- FIRST-FLOOR SLABS
blk(-11.3, 1.2, 4.6, 5.7, -10, 2.2, DARK)
blk(1.2, 2.95, 4.6, 5.7, -10, -8.4, DARK)      # landing
blk(1.2, 2.95, 4.6, 5.7, -4.4, 2.2, DARK)      # (opening for the stairs between)
blk(2.95, 11.7, 4.6, 5.7, -10, 1.6, DARK)

# ---------------------------------------------------- CONCRETE COLUMN
blk(2.95, 4.8, 0, 9.75, -3.0, 0.5, CONC)
for y in [1.6, 3.2, 4.3, 6.4, 7.8, 9.0]:
    blk(2.95, 4.8, y, y + 0.03, 0.45, 0.52, vec(0.35, 0.35, 0.35))
blk(3.85, 3.88, 0, 9.75, 0.45, 0.52, vec(0.35, 0.35, 0.35))

# ---------------------------------------------------- GARAGE
_gparts = [blk(4.95, 10.1, 0, 3.4, 0.0, 0.10, vec(0.12, 0.12, 0.13))]
for k in range(1, 6):
    _gparts.append(blk(4.95, 10.1, k * 0.57, k * 0.57 + 0.04, 0.10, 0.12, vec(0.22, 0.22, 0.24)))
GDOOR = compound(_gparts)
blk(4.8, 10.8, 3.4, 4.6, -0.1, 0.05, CHAR)
blk(10.8, 11.1, 0, 3.2, -0.5, 0.2, CHAR)
led(10.55, 10.7, 1.4, 1.9, 0.0, 0.12)

# ---------------------------------------------------- 2ND FLOOR - LEFT
glass(-6.5, -2.5, 5.7, 8.4, -1.0, mullions=1)
glass(-1.3, 0.8, 5.7, 8.4, -1.0)
blk(-6.8, 0.95, 8.4, 9.1, -1.2, -1.0, CHAR)
# glass railing
blk(-10.4, 0.9, 5.7, 7.0, 1.77, 1.83, GLASS, 0.25)
blk(-10.4, 0.9, 6.95, 7.0, 1.74, 1.86, vec(0.75, 0.75, 0.78))
blk(-10.4, -10.35, 5.7, 7.0, 0.0, 1.8, GLASS, 0.25)
blk(-9.8, -8.0, 5.7, 6.2, 0.2, 1.0, vec(0.45, 0.45, 0.48))
blk(-6.0, -5.0, 5.7, 6.3, 0.8, 1.6, vec(0.8, 0.8, 0.8))

blk(-8.3, -7.7, 5.7, 9.1, 1.8, 2.4, vec(0.30, 0.31, 0.33))
blk(-10.7, 0.95, 9.1, 10.55, -10, 2.5, DARK)

# ---------------------------------------------------- 2ND FLOOR - RIGHT
blk(0.9, 1.5, 5.7, 11.4, -1.5, 0.8, CHAR)
glass(1.5, 2.8, 5.7, 8.5, -1.0)
glass(4.8, 6.6, 5.7, 8.6, -0.5)
glass(7.9, 9.3, 5.7, 8.6, -0.5)
blk(4.8, 9.3, 8.6, 9.75, -0.6, -0.4, CHAR)
blk(9.3, 10.95, 5.5, 9.75, -0.6, -0.2, CHAR)
blk(3.8, 11.4, 5.5, 6.75, 1.37, 1.43, GLASS, 0.25)
blk(3.8, 11.4, 6.70, 6.75, 1.34, 1.46, vec(0.75, 0.75, 0.78))
blk(11.35, 11.4, 5.5, 6.75, -0.2, 1.4, GLASS, 0.25)

blk(0.9, 11.1, 9.75, 11.4, -10, 2.0, DARK)
blk(2.1, 6.6, 11.4, 11.65, -1.0, 1.0, HEDGE)

# ---------------------------------------------------- TOP FRAME
blk(-0.85, 11.0, 12.8, 13.4, -9, 2.0, DARK)
blk(-0.85, -0.2, 11.3, 13.4, -9, 2.0, DARK)
blk(9.3, 11.0, 11.4, 12.8, -6, 0.5, DARK)
blk(-0.2, 6.95, 11.7, 12.2, -9, -1, vec(0.33, 0.34, 0.36))
blk(-4.5, -0.2, 10.7, 11.3, -10, -4, DARK)

# ---------------------------------------------------- RECESSED LIGHTS (night only)
for x in [-9.5, -7.0, -4.0, -1.5]:
    downlight(x, 9.1, 1.4)
for x in [2.0, 4.0, 6.0, 8.0, 10.0]:
    downlight(x, 9.75, 1.0)
for x in [-9.0, -6.0, -3.0, -0.5]:
    downlight(x, 4.6, 1.2)
for x in [6.0, 8.0, 10.0]:
    downlight(x, 4.55, 0.9)
led(-10.2, 0.5, 9.04, 9.1, 2.2, 2.28)
led(-10.5, -0.5, 4.57, 4.6, 1.0, 1.06)
led(0.0, 0.8, 4.57, 4.6, 0.0, 1.0)

# ================================================================ INTERIOR
# Floor levels: ground floor F = 0.5, second floor F2 = 5.7
F = 0.5
F2 = 5.7
WALLC = vec(0.93, 0.91, 0.86)
CEIL = vec(0.96, 0.96, 0.95)
WOODF = vec(0.62, 0.45, 0.28)
TILE = vec(0.82, 0.84, 0.85)
TILE2 = vec(0.55, 0.60, 0.64)
SOFA = vec(0.40, 0.42, 0.47)
WHITE = vec(0.95, 0.95, 0.95)
STEEL = vec(0.75, 0.77, 0.80)
GRAN = vec(0.18, 0.19, 0.21)
CREAM = vec(0.90, 0.86, 0.78)
NAVY = vec(0.18, 0.25, 0.42)
TEAL = vec(0.12, 0.45, 0.48)
MIRROR = vec(0.72, 0.86, 0.90)
GARW = vec(0.60, 0.61, 0.63)

COLL = []   # collision boxes used in walk mode


def solid(x0, x1, y0, y1, z0, z1):
    COLL.append((min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1),
                 min(z0, z1), max(z0, z1)))


def fur(x0, x1, y0, y1, z0, z1, col):
    o = blk(x0, x1, y0, y1, z0, z1, col)
    solid(x0, x1, y0, y1, z0, z1)
    return o


def wallx(x, z0, z1, y0, y1, gaps=(), col=WALLC, t=0.14, dh=2.5):
    """Wall running along z at position x. gaps = [(za, zb), ...] doorways."""
    cur = z0
    for a, b in sorted(gaps):
        if a > cur:
            fur(x - t / 2, x + t / 2, y0, y1, cur, a, col)
        blk(x - t / 2, x + t / 2, y0 + dh, y1, a, b, col)
        cur = b
    if cur < z1:
        fur(x - t / 2, x + t / 2, y0, y1, cur, z1, col)


def wallz(z, x0, x1, y0, y1, gaps=(), col=WALLC, t=0.14, dh=2.5):
    """Wall running along x at position z. gaps = [(xa, xb), ...] doorways."""
    cur = x0
    for a, b in sorted(gaps):
        if a > cur:
            fur(cur, a, y0, y1, z - t / 2, z + t / 2, col)
        blk(a, b, y0 + dh, y1, z - t / 2, z + t / 2, col)
        cur = b
    if cur < x1:
        fur(cur, x1, y0, y1, z - t / 2, z + t / 2, col)


def floor_(x0, x1, z0, z1, y, col, th=0.02):
    blk(x0, x1, y, y + th, z0, z1, col)


def ceil_(x0, x1, z0, z1, top):
    blk(x0, x1, top - 0.06, top, z0, z1, CEIL)


def panel(x, z, y):
    """Soft ceiling light panel (y = underside of ceiling)."""
    led(x - 0.5, x + 0.5, y - 0.04, y, z - 0.3, z + 0.3)


def lamp(x, y, z):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.5, 0), radius=0.03, color=BLACK)
    led(x - 0.15, x + 0.15, y + 0.5, y + 0.78, z - 0.15, z + 0.15)


def pot(x, y, z, s=1.0, r=0.25):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.4, 0), radius=r,
             color=vec(0.30, 0.31, 0.33))
    small_plant(x, y, z, s)


def table(x0, x1, z0, z1, y, h, col=WOOD):
    blk(x0, x1, y + h - 0.06, y + h, z0, z1, col)
    for lx in (x0 + 0.05, x1 - 0.13):
        for lz in (z0 + 0.05, z1 - 0.13):
            blk(lx, lx + 0.08, y, y + h - 0.06, lz, lz + 0.08, col)
    solid(x0, x1, y + 0.3, y + h, z0, z1)


def chair(x, z, y, side, col=WOOD, cushion=CREAM):
    blk(x - 0.22, x + 0.22, y + 0.42, y + 0.5, z - 0.22, z + 0.22, cushion)
    for lx in (x - 0.2, x + 0.14):
        for lz in (z - 0.2, z + 0.14):
            blk(lx, lx + 0.06, y, y + 0.42, lz, lz + 0.06, col)
    if side == 'N':
        blk(x - 0.22, x + 0.22, y + 0.5, y + 1.0, z - 0.22, z - 0.17, col)
    elif side == 'S':
        blk(x - 0.22, x + 0.22, y + 0.5, y + 1.0, z + 0.17, z + 0.22, col)
    elif side == 'W':
        blk(x - 0.22, x - 0.17, y + 0.5, y + 1.0, z - 0.22, z + 0.22, col)
    else:
        blk(x + 0.17, x + 0.22, y + 0.5, y + 1.0, z - 0.22, z + 0.22, col)
    solid(x - 0.22, x + 0.22, y + 0.3, y + 0.9, z - 0.22, z + 0.22)


def bed(x0, x1, z0, z1, y, head, frame, sheet, blanket):
    fur(x0, x1, y, y + 0.3, z0, z1, frame)
    fur(x0 + 0.03, x1 - 0.03, y + 0.3, y + 0.72, z0 + 0.03, z1 - 0.03, sheet)
    if head == 'W':
        blk(x0, x0 + 0.14, y + 0.3, y + 1.5, z0 - 0.08, z1 + 0.08, frame)
        for zc in (z0 + (z1 - z0) * 0.27, z0 + (z1 - z0) * 0.73):
            blk(x0 + 0.2, x0 + 0.7, y + 0.72, y + 0.84, zc - 0.3, zc + 0.3, WHITE)
        blk(x0 + 1.0, x1 + 0.02, y + 0.72, y + 0.78, z0, z1, blanket)
    elif head == 'E':
        blk(x1 - 0.14, x1, y + 0.3, y + 1.5, z0 - 0.08, z1 + 0.08, frame)
        for zc in (z0 + (z1 - z0) * 0.27, z0 + (z1 - z0) * 0.73):
            blk(x1 - 0.7, x1 - 0.2, y + 0.72, y + 0.84, zc - 0.3, zc + 0.3, WHITE)
        blk(x0 - 0.02, x1 - 1.0, y + 0.72, y + 0.78, z0, z1, blanket)
    else:  # head at north (-z)
        blk(x0 - 0.08, x1 + 0.08, y + 0.3, y + 1.4, z0, z0 + 0.14, frame)
        for xc in (x0 + (x1 - x0) * 0.27, x0 + (x1 - x0) * 0.73):
            blk(xc - 0.3, xc + 0.3, y + 0.72, y + 0.84, z0 + 0.2, z0 + 0.7, WHITE)
        blk(x0, x1, y + 0.72, y + 0.78, z0 + 1.0, z1 + 0.02, blanket)


# ---------------------------------------------------------------- colliders for the shell
solid(-11.3, -11.1, 0, 10.55, -10, 2.2)            # west wall
solid(-11.3, 11.7, 0, 13.4, -10.2, -10.0)          # back wall
solid(-11.1, -0.7, F, 4.6, -1.2, -0.9)             # ground facade (left of door)
solid(0.8, 3.0, F, 4.6, -1.2, -0.9)                # ground facade (right of door)
solid(2.95, 4.8, 0, 9.75, -3.0, 0.5)               # concrete column
solid(-9.4, -8.8, F, 4.6, 1.2, 1.8)                # porch pillar
# 2nd floor facade
solid(-6.5, -2.5, F2, 9.1, -1.1, -0.9)             # master glass (left of door)
solid(-1.3, 0.95, F2, 9.1, -1.1, -0.9)             # master glass (right of door)
solid(0.9, 1.5, F2, 9.75, -1.5, 0.8)
solid(1.5, 2.95, F2, 9.1, -1.1, -0.9)
solid(4.8, 6.6, F2, 9.75, -0.65, -0.35)            # bedroom 2 glass
solid(7.9, 10.95, F2, 9.75, -0.65, -0.2)
# balcony rails
solid(-11.5, -10.3, F2, 7.0, -1.0, 2.4)
solid(-10.4, 0.9, F2, 7.0, 1.74, 1.86)
solid(0.9, 2.95, F2, 7.0, 2.14, 2.26)
solid(2.9, 3.0, F2, 7.0, 1.5, 2.3)
solid(2.95, 3.8, F2, 7.0, 1.54, 1.66)
solid(3.8, 11.4, F2, 7.0, 1.34, 1.46)
solid(11.3, 11.6, F2, 7.0, -0.2, 1.5)
# extra balcony glass between the two slabs
blk(0.9, 2.95, F2, 6.9, 2.17, 2.23, GLASS, 0.25)
blk(2.95, 3.8, F2, 6.8, 1.57, 1.63, GLASS, 0.25)

# ---------------------------------------------------------------- inner wall linings
blk(-11.1, -11.04, F, 4.6, -10.0, -1.2, WALLC)
blk(-11.1, 4.8, F, 4.6, -10.0, -9.95, WALLC)
blk(-6.5, 0.95, F2, 9.1, -10.0, -9.95, WALLC)
blk(0.95, 10.75, F2, 9.75, -10.0, -9.95, WALLC)

# ================================================================ GROUND FLOOR
floor_(-11.1, -1.8, -5.5, -1.2, F, WOODF)           # living
floor_(-11.1, -6.5, -10, -5.5, F, TILE)             # kitchen
floor_(-6.5, -1.8, -10, -5.5, F, WOODF)             # dining
floor_(-1.8, 1.2, -4.6, -1.2, F, TILE2)             # foyer
floor_(1.2, 2.95, -2.2, -1.2, F, TILE2)
floor_(-1.8, 1.2, -8.4, -4.6, F, TILE)              # powder room
floor_(-1.8, 4.8, -10, -8.4, F, TILE)               # service hall
floor_(2.95, 4.8, -8.4, -3.0, F, TILE)              # laundry
floor_(5.0, 10.6, -10, -0.1, 0.0, vec(0.52, 0.52, 0.54), 0.04)   # garage

ceil_(-11.1, 1.2, -10, -1.2, 4.6)
ceil_(1.2, 2.95, -10, -8.4, 4.6)
ceil_(1.2, 2.95, -4.4, -1.2, 4.6)
ceil_(2.95, 4.8, -10, -3.0, 4.6)
ceil_(5.0, 10.6, -10, -0.1, 4.6)

# partitions
wallx(-1.8, -10, -1.2, F, 4.6, gaps=[(-9.85, -8.85), (-4.0, -2.0)])
wallz(-8.4, -1.8, 4.8, F, 4.6, gaps=[(3.35, 4.35)])
wallz(-4.6, -1.8, 1.2, F, 4.6, gaps=[(-0.6, 0.4)])
wallx(1.2, -8.4, -4.6, F, 4.6)

# ---------------------------------------------------------------- LIVING ROOM
floor_(-9.9, -5.0, -5.0, -1.5, F + 0.02, vec(0.50, 0.45, 0.42))             # rug
fur(-6.3, -4.9, F, F + 0.45, -5.0, -1.8, SOFA)                              # sofa
blk(-5.3, -4.9, F + 0.45, F + 1.05, -5.0, -1.8, SOFA)
blk(-6.3, -4.9, F + 0.45, F + 0.75, -5.0, -4.8, SOFA)
blk(-6.3, -4.9, F + 0.45, F + 0.75, -2.0, -1.8, SOFA)
for zc in (-4.3, -3.4, -2.5):
    blk(-6.2, -5.4, F + 0.45, F + 0.58, zc - 0.4, zc + 0.4, vec(0.50, 0.52, 0.57))
blk(-5.5, -5.2, F + 0.65, F + 1.0, -4.8, -4.4, vec(0.85, 0.55, 0.30))
table(-8.6, -7.2, -4.1, -2.7, F, 0.42, WOOD)                                # coffee table
fur(-9.9, -9.0, F, F + 0.45, -5.4, -4.6, NAVY)                              # armchairs
blk(-9.9, -9.0, F + 0.45, F + 1.0, -5.4, -5.2, NAVY)
fur(-9.9, -9.1, F, F + 0.45, -1.9, -1.3, NAVY)
blk(-9.9, -9.1, F + 0.45, F + 1.0, -1.5, -1.3, NAVY)
blk(-11.04, -11.0, F, 4.5, -5.1, -1.3, WOOD)                                 # TV feature wall
fur(-11.0, -10.45, F, F + 0.5, -4.8, -2.0, WOOD)                             # TV unit
blk(-11.0, -10.9, F + 1.1, F + 2.15, -4.4, -2.4, BLACK)                      # TV
fur(-4.5, -3.9, F, F + 0.55, -1.9, -1.35, WOOD)                              # side table
lamp(-4.2, F + 0.55, -1.6)
cylinder(pos=vec(-4.4, F, -5.3), axis=vec(0, 1.6, 0), radius=0.03, color=BLACK)
led(-4.6, -4.2, F + 1.6, F + 1.95, -5.5, -5.1)                               # floor lamp
pot(-2.3, F, -1.7, 1.8)
pot(-10.6, F, -1.6, 1.5)
blk(-1.87, -1.82, F + 1.6, F + 2.9, -5.3, -4.3, TEAL)                        # painting
for x in (-9.5, -7.0, -4.5, -2.6):
    for z in (-4.5, -2.0):
        downlight(x, 4.54, z)
panel(-6.5, -3.2, 4.54)

# ---------------------------------------------------------------- KITCHEN
fur(-11.0, -6.6, F, F + 0.9, -9.95, -9.3, WHITE)
blk(-11.0, -6.55, F + 0.9, F + 0.96, -9.95, -9.25, GRAN)
fur(-11.0, -10.4, F, F + 0.9, -9.3, -6.1, WHITE)
blk(-11.0, -10.35, F + 0.9, F + 0.96, -9.3, -6.05, GRAN)
blk(-11.0, -8.1, F + 2.0, F + 3.0, -9.95, -9.6, vec(0.55, 0.40, 0.25))        # upper cabinets
blk(-11.0, -10.7, F + 2.0, F + 3.0, -9.6, -6.4, vec(0.55, 0.40, 0.25))
fur(-8.2, -7.3, F, F + 2.0, -9.95, -9.2, STEEL)                               # fridge
blk(-7.55, -7.5, F + 0.9, F + 1.6, -9.2, -9.15, BLACK)
blk(-9.7, -8.9, F + 0.96, F + 1.0, -9.8, -9.4, BLACK)                         # cooktop
for bx, bz in ((-9.5, -9.7), (-9.1, -9.7), (-9.5, -9.5), (-9.1, -9.5)):
    cylinder(pos=vec(bx, F + 1.0, bz), axis=vec(0, 0.01, 0), radius=0.08,
             color=vec(0.4, 0.4, 0.4))
blk(-9.8, -8.8, F + 2.7, F + 3.0, -9.95, -9.4, STEEL)                         # hood
blk(-9.5, -9.1, F + 3.0, 4.54, -9.95, -9.7, STEEL)
blk(-10.9, -10.5, F + 0.96, F + 1.0, -8.3, -7.3, STEEL)                       # sink
cylinder(pos=vec(-10.65, F + 0.96, -7.8), axis=vec(0, 0.35, 0), radius=0.025, color=STEEL)
fur(-9.8, -7.6, F, F + 0.92, -8.0, -6.7, vec(0.30, 0.32, 0.36))               # island
blk(-9.9, -7.5, F + 0.92, F + 1.0, -8.1, -6.6, WHITE)
for sx in (-9.4, -8.7, -8.0):
    cylinder(pos=vec(sx, F, -6.2), axis=vec(0, 0.68, 0), radius=0.04, color=BLACK)
    cylinder(pos=vec(sx, F + 0.68, -6.2), axis=vec(0, 0.06, 0), radius=0.2, color=NAVY)
    solid(sx - 0.2, sx + 0.2, F + 0.3, F + 0.8, -6.4, -6.0)
for px_ in (-9.3, -8.2):
    led(px_ - 0.2, px_ + 0.2, F + 2.7, F + 2.9, -7.5, -7.2)                   # pendants
    blk(px_ - 0.02, px_ + 0.02, F + 2.9, 4.54, -7.37, -7.33, BLACK)
for x in (-10.0, -8.5, -7.2):
    downlight(x, 4.54, -6.0)
panel(-8.8, -8.8, 4.54)

# ---------------------------------------------------------------- DINING
floor_(-6.0, -2.5, -9.3, -6.3, F + 0.02, vec(0.70, 0.65, 0.58))
table(-5.5, -3.0, -8.8, -7.2, F, 0.76, WOOD)
for cx in (-5.0, -4.25, -3.5):
    chair(cx, -9.2, F, 'N')
    chair(cx, -6.8, F, 'S')
chair(-5.9, -8.0, F, 'W')
chair(-2.6, -8.0, F, 'E')
fur(-5.5, -3.0, F, F + 0.9, -9.95, -9.55, WOOD)                               # sideboard
cylinder(pos=vec(-3.5, F + 0.9, -9.75), axis=vec(0, 0.35, 0), radius=0.1, color=TEAL)
blk(-5.2, -3.3, F + 1.8, F + 3.0, -9.99, -9.94, vec(0.78, 0.52, 0.28))        # painting
led(-5.0, -3.5, F + 2.9, F + 3.05, -8.1, -7.9)                                # linear pendant
blk(-4.3, -4.2, F + 3.05, 4.54, -8.05, -7.95, BLACK)
pot(-2.3, F, -9.6, 1.5)
for x in (-5.0, -3.5):
    downlight(x, 4.54, -6.2)
panel(-4.2, -8.0, 4.54)

# ---------------------------------------------------------------- FOYER / POWDER ROOM / STAIRS
fur(-1.7, -0.9, F, F + 0.9, -2.0, -1.25, WOOD)                                # shoe cabinet
blk(-1.65, -0.95, F + 1.2, F + 2.4, -1.24, -1.2, MIRROR)
floor_(-0.6, 0.7, -2.2, -1.3, F + 0.02, vec(0.18, 0.18, 0.20), 0.015)        # doormat
led(-0.3, 0.3, F + 2.8, F + 3.0, -2.6, -2.2)
blk(-0.02, 0.02, F + 3.0, 4.54, -2.42, -2.38, BLACK)
pot(0.8, F, -4.0, 1.4, 0.2)
downlight(-0.6, 4.54, -3.5)
downlight(0.6, 4.54, -3.5)

fur(-1.7, -1.0, F, F + 0.45, -7.0, -6.4, WHITE)                               # toilet
blk(-1.7, -1.45, F + 0.45, F + 0.95, -7.0, -6.4, WHITE)
fur(-0.4, 0.9, F, F + 0.85, -8.33, -7.65, WOOD)                               # vanity
blk(-0.1, 0.6, F + 0.85, F + 0.9, -8.25, -7.75, WHITE)
cylinder(pos=vec(0.25, F + 0.9, -8.1), axis=vec(0, 0.25, 0), radius=0.02, color=STEEL)
blk(-0.4, 0.9, F + 1.3, F + 2.5, -8.33, -8.29, MIRROR)
panel(-0.3, -6.5, 4.54)

N_STEPS = 24
TREAD = 6.2 / N_STEPS
RISE = 5.2 / N_STEPS
for i in range(N_STEPS):
    zf = -2.2 - i * TREAD
    top = F + (i + 1) * RISE
    blk(1.2, 2.7, F, top, zf - TREAD, zf, WOODF if i % 2 == 0 else vec(0.55, 0.40, 0.25))
    blk(1.17, 1.23, top, top + 0.9, zf - TREAD, zf, GLASS, 0.3)
    blk(1.15, 1.25, top + 0.88, top + 0.93, zf - TREAD, zf, BLACK)
solid(1.15, 1.25, F, 4.6, -8.4, -2.5)
fur(2.7, 2.95, F, 4.6, -8.4, -2.2, WALLC)
# 1st-floor railings around the stair opening
for (ax, bx, az, bz) in ((1.17, 1.23, -8.4, -4.4), (2.85, 2.9, -8.4, -4.4), (1.2, 2.95, -4.45, -4.4)):
    blk(ax, bx, F2, F2 + 1.0, az, bz, GLASS, 0.3)
    blk(ax - 0.02, bx + 0.02, F2 + 0.98, F2 + 1.03, az, bz, BLACK)
solid(1.15, 1.25, F2, F2 + 1.3, -8.4, -4.4)
solid(2.8, 2.95, F2, F2 + 1.3, -8.4, -4.4)
solid(1.2, 2.95, F2, F2 + 1.3, -4.5, -4.4)

# ---------------------------------------------------------------- LAUNDRY
fur(3.05, 3.7, F, F + 0.9, -7.7, -7.0, WHITE)                                 # washer
cylinder(pos=vec(3.7, F + 0.45, -7.35), axis=vec(0.03, 0, 0), radius=0.2, color=GLASS)
fur(3.05, 3.7, F, F + 0.9, -6.9, -6.2, WHITE)                                 # dryer
cylinder(pos=vec(3.7, F + 0.45, -6.55), axis=vec(0.03, 0, 0), radius=0.2, color=STEEL)
blk(3.05, 3.45, F + 1.4, F + 1.45, -7.8, -6.0, WOOD)
for zc, cc in ((-7.5, vec(0.8, 0.3, 0.3)), (-6.9, vec(0.3, 0.5, 0.8)), (-6.3, vec(0.9, 0.8, 0.3))):
    blk(3.1, 3.4, F + 1.45, F + 1.8, zc - 0.2, zc + 0.2, cc)
fur(4.2, 4.75, F, F + 0.9, -7.8, -6.4, WHITE)                                 # laundry sink
blk(4.25, 4.7, F + 0.9, F + 0.96, -7.7, -6.5, STEEL)
fur(3.05, 3.5, F, F + 2.2, -5.6, -4.4, WOOD)                                  # tall cabinet
cylinder(pos=vec(4.6, F, -4.0), axis=vec(0.05, 1.5, 0.05), radius=0.02, color=WOOD)   # mop
panel(3.9, -6.0, 4.54)

# ---------------------------------------------------------------- GARAGE
fur(10.6, 10.8, 0, 4.6, -10, -0.2, GARW)                                      # east wall
wallx(4.9, -10, -0.2, 0, 4.6, gaps=[(-9.8, -8.8)], col=GARW, t=0.2)           # west wall + door
fur(4.8, 4.95, 0, 4.6, -0.2, 0.05, CHAR)
fur(10.1, 10.8, 0, 4.6, -0.2, 0.05, CHAR)
CAR = vec(0.15, 0.20, 0.45)
fur(6.9, 8.8, 0.35, 1.0, -7.0, -2.4, CAR)                                     # car
blk(7.0, 8.7, 1.0, 1.55, -6.2, -3.6, CAR)
blk(6.98, 8.72, 1.1, 1.5, -5.9, -3.9, vec(0.20, 0.30, 0.40))
solid(6.9, 8.8, 1.0, 1.6, -6.2, -3.6)
for wx_ in (6.85, 8.65):
    for wz_ in (-6.2, -3.2):
        cylinder(pos=vec(wx_, 0.35, wz_), axis=vec(0.15, 0, 0), radius=0.35, color=BLACK)
led(7.0, 7.3, 0.6, 0.8, -2.42, -2.38)
led(8.4, 8.7, 0.6, 0.8, -2.42, -2.38)
for yy in (0.6, 1.2, 1.8):                                                    # shelves
    blk(10.2, 10.58, yy, yy + 0.05, -9.0, -5.0, WOOD)
    for zc in (-8.5, -7.5, -6.5, -5.5):
        blk(10.25, 10.55, yy + 0.05, yy + 0.4, zc - 0.25, zc + 0.25, vec(0.7, 0.55, 0.3))
solid(10.2, 10.58, 0, 2.0, -9.0, -5.0)
fur(9.4, 10.15, 0, 1.3, -9.95, -9.4, vec(0.70, 0.15, 0.12))                   # tool chest
cylinder(pos=vec(5.4, 0, -3.0), axis=vec(0, 1.7, 0), radius=0.3, color=WHITE)  # water heater
solid(5.1, 5.7, 0, 1.7, -3.3, -2.7)
for gx in (6.5, 8.5):
    for gz in (-7.0, -3.0):
        panel(gx, gz, 4.54)

# ================================================================ SECOND FLOOR
floor_(-6.5, 0.95, -6.8, -1.05, F2, WOODF)          # master bedroom
floor_(-6.5, -2.5, -10, -6.8, F2, TILE)             # master bath
floor_(-2.5, 0.95, -10, -6.8, F2, CREAM)            # walk-in closet
floor_(0.95, 1.2, -10, -1.0, F2, WOODF)             # hall
floor_(1.2, 2.95, -10, -8.4, F2, WOODF)
floor_(1.2, 2.95, -4.4, -1.0, F2, WOODF)
floor_(2.95, 4.8, -10, -3.0, F2, WOODF)
floor_(4.8, 10.75, -5.5, -0.5, F2, WOODF)           # bedroom 2
floor_(4.8, 8.0, -10, -5.5, F2, WOODF)              # bedroom 3
floor_(8.0, 10.75, -10, -5.5, F2, TILE)             # ensuite
floor_(-11.1, -6.5, -10, -1.0, F2, vec(0.55, 0.52, 0.48))   # lanai

ceil_(-6.5, 0.95, -10, -1.05, 9.1)
ceil_(0.95, 10.75, -10, -0.5, 9.75)

wallx(-6.5, -10, -1.05, F2, 9.1)
wallx(0.95, -10, -1.5, F2, 9.1, gaps=[(-4.3, -3.3)])
wallz(-6.8, -6.5, 0.95, F2, 9.1, gaps=[(-4.4, -3.3), (-1.55, -0.55)])
wallx(-2.5, -10, -6.8, F2, 9.1)
wallx(4.8, -10, -3.0, F2, 9.75, gaps=[(-4.7, -3.6), (-9.3, -8.2)])
wallz(-5.5, 4.8, 10.75, F2, 9.75, gaps=[(8.95, 9.95)])
wallx(8.0, -10, -5.5, F2, 9.75)
wallx(10.8, -10, -0.2, F2, 9.75, col=CHAR, t=0.2)

# ---------------------------------------------------------------- MASTER BEDROOM
bed(-6.43, -4.2, -5.9, -3.5, F2, 'W', WOOD, WHITE, NAVY)
fur(-6.4, -5.9, F2, F2 + 0.5, -6.55, -6.0, WOOD)
fur(-6.4, -5.9, F2, F2 + 0.5, -3.4, -2.85, WOOD)
lamp(-6.15, F2 + 0.5, -6.3)
lamp(-6.15, F2 + 0.5, -3.1)
floor_(-5.8, -1.8, -5.6, -2.2, F2 + 0.02, vec(0.60, 0.65, 0.68))
fur(0.2, 0.88, F2, F2 + 0.8, -6.2, -4.5, WOOD)                                # dresser
blk(0.8, 0.88, F2 + 1.1, F2 + 2.1, -5.9, -4.8, BLACK)                         # TV
fur(-6.3, -5.5, F2, F2 + 0.45, -2.3, -1.5, TEAL)                              # reading chair
blk(-6.3, -6.1, F2 + 0.45, F2 + 1.0, -2.3, -1.5, TEAL)
cylinder(pos=vec(-5.1, F2, -1.9), axis=vec(0, 0.55, 0), radius=0.25, color=WOOD)
solid(-5.35, -4.85, F2, F2 + 0.6, -2.15, -1.65)
pot(0.5, F2, -1.7, 1.6)
for x in (-5.0, -3.0, -1.0):
    for z in (-5.0, -2.5):
        downlight(x, 9.04, z)
panel(-3.0, -4.0, 9.04)

# master bath
blk(-6.4, -5.5, F2, F2 + 2.2, -8.65, -8.6, GLASS, 0.3)
solid(-6.4, -5.5, F2, F2 + 2.2, -8.65, -8.6)
blk(-4.95, -4.9, F2, F2 + 2.2, -10, -8.6, GLASS, 0.3)
solid(-4.95, -4.9, F2, F2 + 2.2, -10, -8.6)
floor_(-6.4, -4.9, -10, -8.6, F2 + 0.02, TILE2)
cylinder(pos=vec(-6.3, F2 + 2.2, -9.3), axis=vec(0.4, 0, 0), radius=0.03, color=STEEL)
cylinder(pos=vec(-5.9, F2 + 2.2, -9.3), axis=vec(0, -0.1, 0), radius=0.12, color=STEEL)
fur(-4.6, -3.2, F2, F2 + 0.85, -9.95, -9.4, WOOD)
blk(-4.3, -3.5, F2 + 0.85, F2 + 0.9, -9.9, -9.5, WHITE)
blk(-4.6, -3.2, F2 + 1.3, F2 + 2.5, -9.95, -9.91, MIRROR)
fur(-3.3, -2.75, F2, F2 + 0.45, -8.6, -8.0, WHITE)
blk(-2.75, -2.6, F2 + 0.45, F2 + 1.0, -8.6, -8.0, WHITE)
panel(-4.0, -8.0, 9.04)

# walk-in closet
fur(-2.4, 0.9, F2, F2 + 2.4, -9.95, -9.45, vec(0.55, 0.40, 0.25))
clothes = (vec(0.8, 0.3, 0.3), vec(0.3, 0.5, 0.8), vec(0.9, 0.8, 0.3), vec(0.3, 0.7, 0.4), vec(0.9, 0.9, 0.9))
for i in range(12):
    blk(-2.3 + i * 0.27, -2.18 + i * 0.27, F2 + 1.2, F2 + 2.2, -9.45, -9.35, clothes[i % 5])
fur(0.45, 0.88, F2, F2 + 2.4, -9.4, -7.2, WOOD)
fur(-2.43, -2.0, F2, F2 + 2.0, -9.4, -7.2, WOOD)
fur(-1.3, -0.3, F2, F2 + 0.9, -8.8, -8.0, vec(0.85, 0.80, 0.70))
floor_(-1.6, -0.2, -9.0, -7.2, F2 + 0.02, vec(0.70, 0.62, 0.50))
panel(-0.8, -8.2, 9.04)

# ---------------------------------------------------------------- UPPER HALL
fur(1.6, 2.4, F2, F2 + 0.45, -2.2, -1.5, SOFA)                                # reading nook
blk(1.6, 2.4, F2 + 0.45, F2 + 1.0, -1.7, -1.5, SOFA)
cylinder(pos=vec(2.7, F2, -2.0), axis=vec(0, 1.5, 0), radius=0.03, color=BLACK)
led(2.55, 2.85, F2 + 1.5, F2 + 1.85, -2.15, -1.85)
fur(4.55, 4.78, F2, F2 + 2.2, -7.6, -5.0, WOOD)                               # bookshelf
for yy in (0.5, 1.0, 1.5):
    for i in range(8):
        blk(4.5, 4.55, F2 + yy, F2 + yy + 0.38, -7.5 + i * 0.3, -7.3 + i * 0.3, clothes[i % 5])
pot(3.3, F2, -9.6, 1.6)
blk(1.02, 1.07, F2 + 1.5, F2 + 2.7, -9.5, -8.2, TEAL)
panel(3.8, -6.0, 9.69)
panel(3.8, -8.6, 9.69)

# ---------------------------------------------------------------- BEDROOM 2
bed(8.6, 10.7, -4.0, -1.9, F2, 'E', WOOD, WHITE, vec(0.55, 0.35, 0.30))
fur(10.2, 10.7, F2, F2 + 0.5, -4.8, -4.2, WOOD)
fur(10.2, 10.7, F2, F2 + 0.5, -1.7, -1.2, WOOD)
lamp(10.45, F2 + 0.5, -4.5)
lamp(10.45, F2 + 0.5, -1.45)
fur(5.0, 8.6, F2, F2 + 2.6, -5.4, -4.85, WOOD)                                # wardrobe
for i in range(1, 6):
    blk(5.0 + i * 0.6, 5.0 + i * 0.6 + 0.02, F2, F2 + 2.6, -4.87, -4.85, BLACK)
table(5.1, 6.5, -1.9, -1.1, F2, 0.75, WOOD)                                   # desk
chair(5.8, -2.4, F2, 'N')
blk(5.4, 6.0, F2 + 0.75, F2 + 0.77, -1.6, -1.25, BLACK)
blk(5.4, 6.0, F2 + 0.77, F2 + 1.1, -1.65, -1.6, BLACK)
floor_(6.8, 9.6, -4.8, -1.2, F2 + 0.02, vec(0.55, 0.60, 0.55))
pot(10.2, F2, -0.9, 1.7)
for x in (6.0, 8.0):
    for z in (-4.5, -2.0):
        downlight(x, 9.69, z)
panel(7.5, -3.0, 9.69)

# ---------------------------------------------------------------- ENSUITE
fur(8.3, 8.9, F2, F2 + 0.45, -9.0, -8.4, WHITE)
blk(8.1, 8.3, F2 + 0.45, F2 + 1.0, -9.0, -8.4, WHITE)
fur(9.2, 10.5, F2, F2 + 0.85, -9.95, -9.4, WOOD)
blk(9.5, 10.2, F2 + 0.85, F2 + 0.9, -9.9, -9.5, WHITE)
blk(9.2, 10.5, F2 + 1.3, F2 + 2.5, -9.95, -9.91, MIRROR)
blk(9.95, 10.0, F2, F2 + 2.2, -8.5, -6.6, GLASS, 0.3)
solid(9.95, 10.0, F2, F2 + 2.2, -8.5, -6.6)
floor_(10.0, 10.7, -8.5, -6.0, F2 + 0.02, TILE2)
cylinder(pos=vec(10.6, F2 + 2.2, -8.0), axis=vec(0, -0.1, 0), radius=0.12, color=STEEL)
panel(9.3, -7.5, 9.69)

# ---------------------------------------------------------------- BEDROOM 3
bed(5.8, 7.4, -9.9, -7.8, F2, 'N', WOOD, WHITE, TEAL)
fur(7.45, 7.9, F2, F2 + 0.5, -9.9, -9.4, WOOD)
fur(5.25, 5.7, F2, F2 + 0.5, -9.9, -9.4, WOOD)
lamp(7.675, F2 + 0.5, -9.65)
lamp(5.475, F2 + 0.5, -9.65)
fur(7.55, 7.93, F2, F2 + 2.4, -7.2, -5.8, WOOD)
table(5.1, 6.8, -6.3, -5.65, F2, 0.75, WOOD)
chair(5.9, -6.8, F2, 'N')
blk(5.8, 7.4, F2 + 1.5, F2 + 2.5, -9.99, -9.94, vec(0.50, 0.70, 0.80))
panel(6.4, -7.7, 9.69)

# ---------------------------------------------------------------- LANAI (covered terrace)
fur(-10.8, -8.6, F2, F2 + 0.45, -7.2, -5.6, WOOD)
blk(-10.7, -8.7, F2 + 0.45, F2 + 0.6, -7.1, -5.7, CREAM)
blk(-10.8, -10.5, F2 + 0.6, F2 + 1.1, -7.1, -5.7, CREAM)
table(-9.6, -8.8, -4.6, -3.8, F2, 0.45, WOOD)
chair(-10.2, -4.2, F2, 'W')
pot(-10.6, F2, -9.4, 2.0)
pot(-7.0, F2, -9.4, 1.6)


# ================================================================ STEPS & PLANTERS
blk(-6.0, 3.0, 0, 0.40, 2.0, 3.0, vec(0.70, 0.70, 0.68))
blk(-6.5, 3.2, 0, 0.27, 3.0, 4.0, vec(0.72, 0.72, 0.70))
blk(-7.0, 3.4, 0, 0.14, 4.0, 5.0, vec(0.74, 0.74, 0.72))
led(-5.5, 2.5, 0.40, 0.43, 2.9, 3.0)
led(-6.0, 3.0, 0.27, 0.30, 3.9, 4.0)

blk(-11.0, -6.5, 0, 0.7, 1.0, 2.2, vec(0.30, 0.31, 0.33))
blk(-11.0, -6.5, 0.7, 1.05, 1.1, 2.1, HEDGE)
blk(-12.2, -6.8, 0, 0.5, 3.2, 4.2, vec(0.30, 0.31, 0.33))
blk(-12.2, -6.8, 0.5, 0.8, 3.3, 4.1, HEDGE)
blk(2.1, 5.9, 0, 0.7, 2.2, 3.6, vec(0.30, 0.31, 0.33))
blk(2.3, 5.7, 0.7, 0.85, 2.3, 3.5, HEDGE)
small_plant(3.2, 0.75, 2.9, 1.8)
small_plant(4.4, 0.75, 3.0, 1.5)
shrub(5.2, 0.75, 2.9, 0.4)
for px in [-3.0, -2.0]:
    cylinder(pos=vec(px, 0.5, -0.2), axis=vec(0, 0.5, 0), radius=0.22 + 0.08,
             color=vec(0.25, 0.26, 0.28))
    small_plant(px, 1.0, -0.2, 1.0)

# ================================================================ PALMS & PLANTS
palm(-10.0, -2.0, 7.0, 0.5)
palm(8.2, -0.3, 7.4, 0.5, 0.4)
palm(11.4, 3.0, 2.8)
for x, z in [(-11.6, 6), (-10.8, 7.5), (11.8, 6.5), (11.5, 4.8)]:
    shrub(x, 0, z, 0.6)
shrub(-3.4, 0, 6.5, 0.45)
shrub(0.6, 0, 6.5, 0.45)

for bx in [-8.7, 6.9]:
    cylinder(pos=vec(bx, 0, 6.4), axis=vec(0, 0.7, 0), radius=0.12, color=BLACK)
    cap = sphere(pos=vec(bx, 0.72, 6.4), radius=0.11, color=LAMP_OFF)
    LIGHTS.append(cap)

# ================================================================ BOUNDARY WALL + GATES
WALL_Z = 9.0
WH = 1.2
SIDE = 12.5


def pillar(x):
    blk(x - 0.28, x + 0.28, 0, 2.2, WALL_Z - 0.28, WALL_Z + 0.28, CHAR)
    blk(x - 0.34, x + 0.34, 2.2, 2.3, WALL_Z - 0.34, WALL_Z + 0.34, DARK)
    cap = sphere(pos=vec(x, 2.45, WALL_Z), radius=0.15, color=LAMP_OFF)
    LIGHTS.append(cap)


for x in [-SIDE, -2.4, -0.6, 4.6, 10.4, SIDE]:
    pillar(x)

for xa, xb in [(-SIDE, -2.4), (-0.6, 4.6), (10.4, SIDE)]:
    blk(xa, xb, 0, WH, WALL_Z - 0.15, WALL_Z + 0.15, CHAR)
    blk(xa, xb, WH, WH + 0.08, WALL_Z - 0.2, WALL_Z + 0.2, DARK)
    led(xa, xb, 0.6, 0.63, WALL_Z + 0.15, WALL_Z + 0.17)

blk(-SIDE - 0.1, -SIDE + 0.1, 0, 2.4, -10, 9, vec(0.80, 0.80, 0.78))
blk(SIDE - 0.1, SIDE + 0.1, 0, 2.4, -10, 9, vec(0.80, 0.80, 0.78))


def make_gate(x0, x1, z=WALL_Z + 0.35, h=1.9):
    parts = []
    w = x1 - x0
    parts.append(blk(x0, x1, 0.15, 0.30, z - 0.05, z + 0.05, BLACK))
    parts.append(blk(x0, x1, h - 0.15, h, z - 0.05, z + 0.05, BLACK))
    parts.append(blk(x0, x0 + 0.1, 0.15, h, z - 0.05, z + 0.05, BLACK))
    parts.append(blk(x1 - 0.1, x1, 0.15, h, z - 0.05, z + 0.05, BLACK))
    n = int(w / 0.22)
    for i in range(n):
        x = x0 + 0.15 + i * (w - 0.3) / max(n - 1, 1)
        wood = (n * 0.3 < i < n * 0.7)
        parts.append(blk(x - 0.045, x + 0.045, 0.30, h - 0.15,
                         z - 0.04, z + 0.04, WOOD if wood else BLACK))
    return compound(parts)


ped = make_gate(-2.4, -0.6)
drvL = make_gate(4.6, 7.5)
drvR = make_gate(7.5, 10.4)

# ================================================================ DAY / NIGHT
def set_night(night):
    if night:
        scene.background = SKY_NIGHT
        scene.ambient = color.gray(0.22)
        sun.color = vec(0.18, 0.22, 0.38)
        fill.color = vec(0.06, 0.07, 0.12)
    else:
        scene.background = SKY_DAY
        scene.ambient = color.gray(0.55)
        sun.color = color.gray(0.75)
        fill.color = color.gray(0.25)
    for o in LIGHTS:
        o.emissive = night
        o.color = WARM if night else LAMP_OFF
    for o in GLOWS:
        o.emissive = night
        o.color = INTER if night else INTER_DAY


def go_day(b):
    set_night(False)


def go_night(b):
    set_night(True)


# ================================================================ DOORS / GATES / CUTAWAY
PED_HINGE = vec(-2.4, 0, WALL_Z + 0.35)
L_HINGE = vec(4.6, 0, WALL_Z + 0.35)
R_HINGE = vec(10.4, 0, WALL_Z + 0.35)
DOOR_HINGE = vec(-0.7, 0, -1.0)
OPEN_ANGLE = 1.45
G0 = vec(GDOOR.pos.x, GDOOR.pos.y, GDOOR.pos.z)

gate_open = False
door_open = False
garage_open = False
gate_cur = 0.0
door_cur = 0.0
garage_cur = 0.0
cut = 0


def toggle_gate(b):
    global gate_open
    gate_open = not gate_open
    b.text = "CLOSE GATES" if gate_open else "OPEN GATES"


def toggle_door(b):
    global door_open
    door_open = not door_open
    b.text = "CLOSE FRONT DOOR" if door_open else "OPEN FRONT DOOR"


def toggle_garage(b):
    global garage_open
    garage_open = not garage_open
    b.text = "CLOSE GARAGE" if garage_open else "OPEN GARAGE"


def cycle_cut(b):
    global cut
    cut = (cut + 1) % 3
    for o in ROOF:
        o.visible = (cut == 0)
    for o in UPPER:
        o.visible = (cut < 2)
    b.text = ["CUTAWAY: OFF", "CUTAWAY: ROOF OFF", "CUTAWAY: 2ND FLOOR OFF"][cut]


# ================================================================ CAMERA VIEWS (outside)
VIEWS = {
    #            center              forward                  range  up
    "main":  (vec(0, 4.5, 0),   vec(0.22, -0.42, -1),     15.5, vec(0, 1, 0)),
    "front": (vec(0, 5.8, 0),   vec(0.03, -0.07, -1),     14.0, vec(0, 1, 0)),
    "gate":  (vec(3.5, 2.0, 8), vec(0.10, -0.22, -1),      7.5, vec(0, 1, 0)),
    "left":  (vec(0, 4.5, 0),   vec(0.75, -0.40, -0.65),  16.5, vec(0, 1, 0)),
    "right": (vec(0, 4.5, 0),   vec(-0.75, -0.40, -0.65), 16.5, vec(0, 1, 0)),
    "yard":  (vec(0, 1.5, 3),   vec(0.12, -0.30, -1),      9.0, vec(0, 1, 0)),
    "top":   (vec(0, 0, -1),    vec(0, -1, -0.001),       17.0, vec(0, 0, -1)),
}


def set_view(name):
    c, f, r, u = VIEWS[name]
    scene.up = u
    scene.center = c
    scene.forward = f
    scene.range = r


# ================================================================ WALK MODE (explore inside)
EYE = 1.6
RADIUS = 0.32
walk = False
px = 0.0
pz = 0.0
yaw = 0.0        # 0 = looking toward the back of the house (-z)
pitch = 0.0
hcur = F


def stair_h(z):
    t = (-2.2 - z) / 6.2
    if t <= 0:
        return F
    n = min(int(t * N_STEPS) + 1, N_STEPS)
    return F + n * RISE


def ground_h(x, z):
    if 4.85 < x < 10.8 and z < 0.0:
        return 0.0                       # garage
    if -11.3 <= x <= 4.8 and -10 <= z <= 2.0:
        return F                         # house podium
    if 2.0 < z <= 3.0 and -6.0 <= x <= 3.0:
        return 0.4
    if 3.0 < z <= 4.0 and -6.5 <= x <= 3.2:
        return 0.27
    if 4.0 < z <= 5.0 and -7.0 <= x <= 3.4:
        return 0.14
    return 0.0


def target_h(x, z):
    if 1.2 <= x <= 2.95 and -8.4 <= z <= -2.2:
        hs = stair_h(z)
        if hcur < hs + 0.2 or abs(hcur - hs) < 1.0:
            return hs                    # climbing / descending the stairs
    if hcur > 3.0:
        return F2                        # second floor
    return ground_h(x, z)


def blocked(x, z):
    y0 = hcur + 0.3
    y1 = hcur + 1.5
    boxes = list(COLL)
    if not door_open or door_cur < 0.9:
        boxes.append((-0.7, 0.8, F, 3.9, -1.1, -0.9))
    if garage_cur < 0.9:
        boxes.append((4.95, 10.1, 0, 3.4, -0.1, 0.12))
    for (bx0, bx1, by0, by1, bz0, bz1) in boxes:
        if by1 > y0 and by0 < y1:
            if bx0 - RADIUS < x < bx1 + RADIUS and bz0 - RADIUS < z < bz1 + RADIUS:
                return True
    return False


def apply_cam():
    eye = vec(px, hcur + EYE, pz)
    d = vec(sin(yaw) * cos(pitch), sin(pitch), -cos(yaw) * cos(pitch))
    scene.camera.pos = eye
    scene.camera.axis = d * 3


def move(dx, dz):
    global px, pz, hcur
    nx = px + dx
    if not blocked(nx, pz):
        px = nx
    nz = pz + dz
    if not blocked(px, nz):
        pz = nz
    px = max(-12.5, min(12.5, px))
    pz = max(-9.7, min(8.5, pz))
    hcur = target_h(px, pz)


def on_key(evt):
    global yaw, pitch
    if not walk:
        return
    k = evt.key.lower()
    sp = 0.3
    fx, fz = sin(yaw), -cos(yaw)
    rx, rz = cos(yaw), sin(yaw)
    if k == 'w':
        move(fx * sp, fz * sp)
    elif k == 's':
        move(-fx * sp, -fz * sp)
    elif k == 'a':
        move(-rx * sp, -rz * sp)
    elif k == 'd':
        move(rx * sp, rz * sp)
    elif k in ('left', 'q'):
        yaw -= 0.09
    elif k in ('right', 'e'):
        yaw += 0.09
    elif k == 'up':
        pitch = min(pitch + 0.07, 1.0)
    elif k == 'down':
        pitch = max(pitch - 0.07, -1.0)
    apply_cam()


def enter_walk(x, z, yw, up):
    global walk, px, pz, yaw, pitch, hcur
    walk = True
    scene.userspin = False
    scene.userzoom = False
    scene.userpan = False
    scene.up = vec(0, 1, 0)
    scene.fov = 1.25
    px, pz, yaw, pitch = x, z, yw, 0.0
    hcur = F2 if up else ground_h(x, z)
    apply_cam()


def exit_walk(b=None):
    global walk
    walk = False
    scene.userspin = True
    scene.userzoom = True
    scene.userpan = True
    scene.fov = pi / 3
    set_view("main")


scene.bind('keydown', on_key)

ROOMS = [
    ("LIVING", -2.9, -2.2, -1.35, False),
    ("KITCHEN", -6.9, -6.0, -1.0, False),
    ("DINING", -2.4, -6.3, -0.8, False),
    ("POWDER ROOM", -0.1, -4.0, 0.0, False),
    ("LAUNDRY", 3.9, -9.3, pi, False),
    ("GARAGE", 5.5, -9.3, 2.4, False),
    ("MASTER BEDROOM", -0.4, -3.6, -pi / 2, True),
    ("MASTER BATH", -3.9, -7.2, 0.0, True),
    ("WALK-IN CLOSET", -0.7, -7.3, 0.0, True),
    ("UPPER HALL", 3.6, -3.6, 0.0, True),
    ("BEDROOM 2", 6.0, -3.2, 1.2, True),
    ("BEDROOM 3", 5.3, -7.2, 0.7, True),
    ("ENSUITE", 9.4, -6.3, 0.0, True),
    ("LANAI", -8.0, -3.0, -1.0, True),
    ("BALCONY", -3.0, 1.0, pi, True),
]


def make_room_button(label, x, z, yw, up):
    def go(b):
        enter_walk(x, z, yw, up)
    button(text=label, bind=go)
    scene.append_to_caption(" ")


def enter_house(b):
    global door_open
    door_open = True
    enter_walk(0.1, 3.4, 0.0, False)


def make_view_button(label, name):
    def go(b):
        if walk:
            exit_walk()
        set_view(name)
    button(text=label, bind=go)
    scene.append_to_caption(" ")


# ================================================================ BUTTONS
scene.append_to_caption("\n")
button(text="DAYLIGHT", bind=go_day)
button(text="NIGHT", bind=go_night)
scene.append_to_caption("   ")
make_view_button("FRONT", "front")
make_view_button("GATE", "gate")
make_view_button("LEFT ANGLE", "left")
make_view_button("RIGHT ANGLE", "right")
make_view_button("FRONT YARD", "yard")
make_view_button("TOP", "top")
scene.append_to_caption("   ")
button(text="OPEN GATES", bind=toggle_gate)
button(text="OPEN FRONT DOOR", bind=toggle_door)
button(text="OPEN GARAGE", bind=toggle_garage)
button(text="CUTAWAY: OFF", bind=cycle_cut)
scene.append_to_caption("\n\nEXPLORE INSIDE:  ")
button(text="ENTER HOUSE", bind=enter_house)
button(text="EXIT WALK MODE", bind=exit_walk)
scene.append_to_caption("\nGo to room:  ")
for _name, _x, _z, _yw, _up in ROOMS:
    make_room_button(_name, _x, _z, _yw, _up)
scene.append_to_caption(
    "\n\nWalk mode (click the 3D view first):  W/S = forward/back  |  A/D = sidestep  |  "
    "Left/Right or Q/E = turn  |  Up/Down = look up/down\n"
    "Normal mode:  right-drag = rotate  |  scroll = zoom  |  shift+drag = pan\n")

set_view("main")
set_night(False)

# ================================================================ ANIMATION LOOP
while True:
    rate(60)
    tgt = OPEN_ANGLE if gate_open else 0.0
    if abs(tgt - gate_cur) > 0.0005:
        d = max(-0.03, min(0.03, tgt - gate_cur))
        gate_cur += d
        ped.rotate(angle=d, axis=vec(0, 1, 0), origin=PED_HINGE)
        drvL.rotate(angle=d, axis=vec(0, 1, 0), origin=L_HINGE)
        drvR.rotate(angle=-d, axis=vec(0, 1, 0), origin=R_HINGE)
    tgt = 1.0 if door_open else 0.0
    if abs(tgt - door_cur) > 0.0005:
        d = max(-0.03, min(0.03, tgt - door_cur))
        door_cur += d
        DOOR.rotate(angle=d * 1.5, axis=vec(0, 1, 0), origin=DOOR_HINGE)
    tgt = 1.0 if garage_open else 0.0
    if abs(tgt - garage_cur) > 0.0005:
        d = max(-0.02, min(0.02, tgt - garage_cur))
        garage_cur += d
        GDOOR.pos = G0 + vec(0, 3.3 * garage_cur, -0.2 * garage_cur)