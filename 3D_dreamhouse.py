
import math
import random
from vpython import (
    canvas, vector as V, box, sphere, cylinder, cone, pyramid,
    distant_light, local_light, rate, button, color
)

TITLE = ("NAME: DEOGRACIAS P. BALILI | COURSE: BSCS 3 | "
         "SUBJECT: GRAPHIC AND COMPUTING | 3D DREAM HOUSE")

scene = canvas(
    title=TITLE,
    width=1180,
    height=740,
    background=V(0.12, 0.16, 0.28),
    autoscale=False
)
scene.lights = []
scene.ambient = V(0.35, 0.38, 0.48)

SUN_LIGHT = distant_light(direction=V(0.2, -0.6, -0.7), color=V(0.40, 0.45, 0.65))
distant_light(direction=V(-0.4, 0.3, 0.6), color=V(0.20, 0.24, 0.38))

def c(r, g, b):
    return V(r / 255.0, g / 255.0, b / 255.0)

WALL_CREAM    = c(246, 244, 239)
WALL_WHITE    = c(252, 252, 254)
WOOD_CEDAR    = c(184, 118, 62)
WOOD_SOFFIT   = c(168, 108, 54)
WOOD_DARK     = c(110, 68, 38)
STONE_GREY    = c(118, 114, 110)
STONE_DARK    = c(82, 80, 78)
FRAME_BLACK   = c(28, 30, 34)
GLASS_PANE    = c(195, 220, 238)
CURTAIN_WHITE = c(248, 248, 250)
TRUCK_BLACK   = c(22, 24, 28)
AMBER_LIGHT   = c(255, 218, 125)
WARM_WHITE    = c(255, 244, 205)
GOLDEN_GLOW   = c(255, 195, 80)
LEAF_GREEN    = c(50, 125, 52)
PINE_GREEN    = c(38, 92, 42)
ASPHALT_GREY  = c(88, 92, 100)
PAVEMENT_GREY = c(190, 188, 182)

lamp_bulbs    = []
window_glass  = []
lantern_caps  = []
sconce_bulbs  = []
spot_lights   = []
strip_lights  = []
gate_left     = []
gate_right    = []

def cube(x, y, z, sx, sy, sz, col, opacity=1.0, emissive=False):
    return box(pos=V(x, y, z), size=V(sx, sy, sz), color=col,
               opacity=opacity, emissive=emissive)

def post(x, y0, y1, z, r, col):
    return cylinder(pos=V(x, y0, z), axis=V(0, y1 - y0, 0), radius=r, color=col)

def sconce(x, y, z, facing="z"):
    cube(x, y, z, 0.12, 0.44, 0.08, FRAME_BLACK)
    b_top = sphere(pos=V(x, y + 0.20, z + (0.05 if facing == "z" else 0)),
                   radius=0.065, color=AMBER_LIGHT, emissive=True)
    b_bot = sphere(pos=V(x, y - 0.20, z + (0.05 if facing == "z" else 0)),
                   radius=0.065, color=AMBER_LIGHT, emissive=True)
    sconce_bulbs.extend([b_top, b_bot])

def downlight(x, y, z):
    cylinder(pos=V(x, y, z), axis=V(0, -0.03, 0), radius=0.12, color=FRAME_BLACK)
    b = cylinder(pos=V(x, y - 0.015, z), axis=V(0, -0.025, 0), radius=0.09,
                 color=WARM_WHITE, emissive=True)
    lamp_bulbs.append(b)

def build_site():
    cube(0, -0.25, 12.5, 34.0, 0.20, 7.5, ASPHALT_GREY)
    cube(0, -0.08, 12.5, 32.0, 0.04, 0.12, c(245, 245, 245), emissive=True)
    cube(0, -0.10, 8.9, 34.0, 0.12, 0.40, c(150, 148, 145))
    cube(0, -0.05, 4.0, 32.0, 0.12, 9.5, PAVEMENT_GREY)
    cube(-13.0, -0.02, 4.0, 5.5, 0.10, 9.0, c(55, 128, 52))
    cube(13.0, -0.02, 4.0, 5.5, 0.10, 9.0, c(55, 128, 52))

    for step in range(8):
        t = step / 7.0
        zy = 8.5 - t * 9.0
        yh = 2.2 + t * 2.1
        cube(-14.2, yh / 2.0, zy, 0.35, yh, 1.4, WALL_WHITE)
        cube(14.2, yh / 2.0, zy, 0.35, yh, 1.4, WALL_WHITE)

    for i, (tx, tz) in enumerate([(-12.8, 7.2), (-13.0, 4.8), (-13.2, 2.4), (-13.4, 0.0),
                                  (12.8, 7.2), (13.0, 4.8), (13.2, 2.4), (13.4, 0.0)]):
        h = 2.2 + (0.5 if abs(tz) < 3.0 else 0.0)
        cylinder(pos=V(tx, 0, tz), axis=V(0, 0.5, 0), radius=0.14, color=WOOD_DARK)
        cone(pos=V(tx, 0.4, tz), axis=V(0, h * 0.55, 0), radius=0.75, color=PINE_GREEN)
        cone(pos=V(tx, 0.4 + h * 0.3, tz), axis=V(0, h * 0.50, 0), radius=0.60, color=LEAF_GREEN)
        cone(pos=V(tx, 0.4 + h * 0.55, tz), axis=V(0, h * 0.45, 0), radius=0.42, color=c(58, 142, 60))
        sp = sphere(pos=V(tx, 0.08, tz + 0.3), radius=0.07, color=AMBER_LIGHT, emissive=True)
        spot_lights.append(sp)

    cube(0, -0.05, -5.8, 32.0, 0.12, 10.5, PAVEMENT_GREY)
    cube(-13.0, -0.02, -5.8, 5.5, 0.10, 10.5, c(55, 128, 52))
    cube(13.0, -0.02, -5.8, 5.5, 0.10, 10.5, c(55, 128, 52))
    cube(0, -0.25, -13.5, 34.0, 0.20, 6.0, ASPHALT_GREY)
    cube(0, -0.10, -11.0, 34.0, 0.12, 0.40, c(150, 148, 145))

    cube(-14.2, 1.4, -5.6, 0.35, 2.8, 10.4, WALL_WHITE)
    cube(14.2, 1.4, -5.6, 0.35, 2.8, 10.4, WALL_WHITE)
    cube(-14.2, 2.85, -5.6, 0.45, 0.10, 10.4, STONE_DARK)
    cube(14.2, 2.85, -5.6, 0.45, 0.10, 10.4, STONE_DARK)

    for s_step in range(6):
        sz = -7.3 - s_step * 0.65
        cube(0, 0.02, sz, 2.4, 0.04, 0.50, c(205, 208, 214))

    for tx, tz in [(-12.8, -3.0), (-13.0, -6.5), (-13.2, -9.5),
                   (12.8, -3.0), (13.0, -6.5), (13.2, -9.5),
                   (-8.5, -9.6), (-5.0, -9.6), (5.0, -9.6), (8.5, -9.6)]:
        cylinder(pos=V(tx, 0, tz), axis=V(0, 0.4, 0), radius=0.12, color=WOOD_DARK)
        cone(pos=V(tx, 0.35, tz), axis=V(0, 1.4, 0), radius=0.65, color=PINE_GREEN)
        cone(pos=V(tx, 0.85, tz), axis=V(0, 1.2, 0), radius=0.52, color=LEAF_GREEN)
        cone(pos=V(tx, 1.35, tz), axis=V(0, 1.0, 0), radius=0.38, color=c(58, 142, 60))
        sp = sphere(pos=V(tx, 0.08, tz + 0.25), radius=0.07, color=AMBER_LIGHT, emissive=True)
        spot_lights.append(sp)

def build_gate_and_fence():
    p_x = [-14.2, -9.8, 4.6, 14.2]
    for px in p_x:
        cube(px, 1.25, 8.5, 1.2, 2.5, 1.1, WALL_WHITE)
        cube(px, 2.55, 8.5, 1.35, 0.12, 1.25, STONE_DARK)
        cap = cube(px, 2.70, 8.5, 0.85, 0.18, 0.70, WARM_WHITE, emissive=True)
        lantern_caps.append(cap)
        cube(px, 2.82, 8.5, 0.92, 0.06, 0.78, FRAME_BLACK)
        sconce(px, 1.35, 9.10)

    for min_x, max_x in [(-13.6, -10.4), (5.2, 13.6)]:
        cx = (min_x + max_x) / 2.0
        w = max_x - min_x
        cube(cx, 1.0, 8.5, w, 2.0, 0.55, WALL_WHITE)
        cube(cx, 2.05, 8.5, w + 0.08, 0.10, 0.65, STONE_DARK)
        cube(cx, 1.10, 8.5, w - 0.35, 1.10, 0.62, STONE_GREY)
        for row in range(5):
            ry = 0.65 + row * 0.22
            cube(cx, ry, 8.82, w - 0.40, 0.02, 0.02, STONE_DARK)
        cube(cx, 0.18, 9.15, w - 0.2, 0.35, 0.65, c(62, 45, 32))
        step_f = (w - 0.8) / 3.0
        for fi in range(4):
            fx = min_x + 0.4 + fi * step_f
            sphere(pos=V(fx, 0.42, 9.25), radius=0.28, color=LEAF_GREEN)
            sphere(pos=V(fx + 0.15, 0.48, 9.30), radius=0.18, color=c(245, 130, 160))
            sphere(pos=V(fx - 0.15, 0.46, 9.28), radius=0.16, color=c(255, 210, 90))
            sp = sphere(pos=V(fx, 0.12, 9.55), radius=0.06, color=AMBER_LIGHT, emissive=True)
            spot_lights.append(sp)

    gw = 6.6
    lx = -5.9
    rx = 0.7
    gate_left.append(cube(lx, 1.15, 8.48, gw, 2.1, 0.04, c(15, 16, 18)))
    gate_left.append(cube(lx, 2.15, 8.52, gw, 0.12, 0.08, FRAME_BLACK))
    gate_left.append(cube(lx, 0.15, 8.52, gw, 0.14, 0.08, FRAME_BLACK))
    gate_left.append(cube(-9.15, 1.15, 8.52, 0.14, 2.1, 0.08, FRAME_BLACK))
    gate_left.append(cube(-2.65, 1.15, 8.52, 0.14, 2.1, 0.08, FRAME_BLACK))
    for k in range(12):
        gy = 0.28 + k * (1.75 / 11.0)
        gate_left.append(cube(lx, gy, 8.53, gw - 0.15, 0.11, 0.05, c(28, 30, 36)))
        gate_left.append(cube(lx, gy + 0.06, 8.55, gw - 0.15, 0.015, 0.02, c(170, 175, 185)))
    gate_left.append(cylinder(pos=V(-2.80, 0.90, 8.60), axis=V(0, 0.55, 0), radius=0.035, color=c(235, 238, 245)))

    gate_right.append(cube(rx, 1.15, 8.48, gw, 2.1, 0.04, c(15, 16, 18)))
    gate_right.append(cube(rx, 2.15, 8.52, gw, 0.12, 0.08, FRAME_BLACK))
    gate_right.append(cube(rx, 0.15, 8.52, gw, 0.14, 0.08, FRAME_BLACK))
    gate_right.append(cube(-2.55, 1.15, 8.52, 0.14, 2.1, 0.08, FRAME_BLACK))
    gate_right.append(cube(3.95, 1.15, 8.52, 0.14, 2.1, 0.08, FRAME_BLACK))
    for k in range(12):
        gy = 0.28 + k * (1.75 / 11.0)
        gate_right.append(cube(rx, gy, 8.53, gw - 0.15, 0.11, 0.05, c(28, 30, 36)))
        gate_right.append(cube(rx, gy + 0.06, 8.55, gw - 0.15, 0.015, 0.02, c(170, 175, 185)))
    gate_right.append(cylinder(pos=V(-2.40, 0.90, 8.60), axis=V(0, 0.55, 0), radius=0.035, color=c(235, 238, 245)))

    for sx, sz_door in [(-14.2, 3.8), (14.2, 3.8)]:
        cube(sx, 1.15, sz_door, 0.08, 2.1, 2.2, FRAME_BLACK)
        cube(sx, 1.15, sz_door, 0.04, 2.0, 2.1, c(18, 20, 24))
        for k in range(11):
            sy = 0.32 + k * (1.65 / 10.0)
            cube(sx + (0.02 if sx > 0 else -0.02), sy, sz_door, 0.05, 0.10, 2.05, c(28, 30, 36))
            cube(sx + (0.04 if sx > 0 else -0.04), sy + 0.05, sz_door, 0.02, 0.015, 2.05, c(170, 175, 185))
        cylinder(pos=V(sx + (0.06 if sx > 0 else -0.06), 0.95, sz_door + 0.8),
                 axis=V(0, 0.35, 0), radius=0.025, color=c(225, 230, 240))

    cube(0.0, 1.10, -10.8, 28.4, 2.2, 0.45, WALL_WHITE)
    cube(0.0, 2.25, -10.8, 28.5, 0.10, 0.55, STONE_DARK)
    for sx in [-8.5, 0.0, 8.5]:
        cube(sx, 1.15, -10.8, 5.8, 1.10, 0.52, STONE_GREY)
        sconce(sx, 1.45, -11.1)

def build_architecture():
    cube(0, 3.8, -3.5, 22.0, 7.6, 7.2, WALL_CREAM)
    cube(-7.6, 1.8, -3.4, 6.8, 3.6, 6.8, c(35, 38, 44))
    cube(-7.6, 0.02, -3.4, 6.6, 0.04, 6.6, c(185, 182, 178))
    cube(-11.1, 1.8, -0.05, 0.35, 3.6, 0.4, WALL_WHITE)
    downlight(-7.6, 3.58, -1.8)
    downlight(-7.6, 3.58, -4.5)

    cube(0.0, 1.8, 0.04, 6.8, 3.2, 0.10, FRAME_BLACK)
    cube(0.0, 1.8, -0.05, 6.6, 3.1, 0.05, c(255, 240, 195), emissive=True)
    g1 = cube(0.0, 1.8, 0.07, 6.6, 3.1, 0.04, GLASS_PANE, opacity=0.82)
    window_glass.append(g1)
    for p in range(5):
        px = -3.2 + p * (6.4 / 4.0)
        cube(px, 1.8, 0.10, 0.08, 3.1, 0.04, FRAME_BLACK)
    for cx in [-2.4, -0.8, 0.8, 2.4]:
        cube(cx, 1.8, 0.02, 1.4, 3.0, 0.02, CURTAIN_WHITE, opacity=0.88)

    cube(5.5, 0.08, 0.45, 3.8, 0.16, 0.85, c(195, 192, 186))
    cube(5.5, 0.04, 0.95, 4.2, 0.08, 0.55, c(170, 168, 162))
    cube(5.5, 0.17, 0.65, 1.6, 0.02, 0.70, c(45, 42, 38))

    cylinder(pos=V(3.7, 0.16, 0.5), axis=V(0, 0.55, 0), radius=0.20, color=c(32, 34, 38))
    sphere(pos=V(3.7, 0.85, 0.5), radius=0.32, color=LEAF_GREEN)
    cylinder(pos=V(7.3, 0.16, 0.5), axis=V(0, 0.55, 0), radius=0.20, color=c(32, 34, 38))
    sphere(pos=V(7.3, 0.85, 0.5), radius=0.32, color=LEAF_GREEN)

    cube(5.5, 1.75, 0.04, 3.6, 3.2, 0.12, FRAME_BLACK)
    cube(5.5, 2.62, 0.06, 3.4, 0.08, 0.08, FRAME_BLACK)
    cube(5.5, 2.92, -0.05, 3.3, 0.48, 0.04, c(255, 240, 195), emissive=True)
    g_tr = cube(5.5, 2.92, 0.05, 3.3, 0.48, 0.04, GLASS_PANE, opacity=0.75)
    window_glass.append(g_tr)
    cube(5.5, 1.45, -0.10, 3.4, 2.7, 0.04, c(255, 235, 195), emissive=True)

    cube(4.75, 1.35, 0.07, 1.30, 2.30, 0.06, c(22, 24, 28))
    g_d1 = cube(4.75, 1.35, 0.09, 1.05, 2.05, 0.03, GLASS_PANE, opacity=0.80)
    window_glass.append(g_d1)
    cube(4.75, 1.35, 0.11, 0.04, 2.05, 0.03, FRAME_BLACK)
    cube(4.75, 1.35, 0.11, 1.05, 0.04, 0.03, FRAME_BLACK)
    cylinder(pos=V(5.30, 0.85, 0.16), axis=V(0, 0.90, 0), radius=0.026, color=c(235, 238, 245))
    cube(5.30, 0.92, 0.12, 0.03, 0.03, 0.08, c(200, 205, 215))
    cube(5.30, 1.68, 0.12, 0.03, 0.03, 0.08, c(200, 205, 215))

    cube(6.25, 1.35, 0.07, 1.30, 2.30, 0.06, c(22, 24, 28))
    g_d2 = cube(6.25, 1.35, 0.09, 1.05, 2.05, 0.03, GLASS_PANE, opacity=0.80)
    window_glass.append(g_d2)
    cube(6.25, 1.35, 0.11, 0.04, 2.05, 0.03, FRAME_BLACK)
    cube(6.25, 1.35, 0.11, 1.05, 0.04, 0.03, FRAME_BLACK)
    cylinder(pos=V(5.70, 0.85, 0.16), axis=V(0, 0.90, 0), radius=0.026, color=c(235, 238, 245))
    cube(5.70, 0.92, 0.12, 0.03, 0.03, 0.08, c(200, 205, 215))
    cube(5.70, 1.68, 0.12, 0.03, 0.03, 0.08, c(200, 205, 215))

    downlight(5.5, 3.58, 0.2)

    cube(-4.0, 1.8, 0.12, 0.65, 3.6, 0.20, WALL_WHITE)
    sconce(-4.0, 2.0, 0.24)
    cube(3.5, 1.8, 0.12, 0.65, 3.6, 0.20, WALL_WHITE)
    sconce(3.5, 2.0, 0.24)

    cube(9.8, 4.3, -2.5, 2.8, 8.6, 5.4, STONE_GREY)
    for row in range(18):
        sy = 0.3 + row * 0.45
        col = STONE_DARK if row % 2 == 0 else STONE_GREY
        cube(9.8, sy, 0.22, 2.82, 0.04, 0.04, col)
    sconce(9.8, 2.0, 0.26)
    sconce(9.8, 5.8, 0.26)

    for fx in [8.65, 9.15, 9.65]:
        cube(fx, 4.4, 0.32, 0.12, 8.8, 0.25, FRAME_BLACK)

    cube(-1.8, 3.75, 1.1, 20.4, 0.30, 2.6, WALL_WHITE)
    cube(-1.8, 3.62, 1.1, 20.2, 0.05, 2.5, WOOD_SOFFIT)

    cube(-1.8, 4.95, 2.35, 20.2, 0.08, 0.08, FRAME_BLACK)
    cube(-1.8, 3.95, 2.35, 20.2, 0.06, 0.06, FRAME_BLACK)
    g_rail = cube(-1.8, 4.45, 2.35, 20.0, 0.92, 0.03, GLASS_PANE, opacity=0.72)
    window_glass.append(g_rail)
    for i in range(15):
        rx = -11.6 + i * (19.8 / 14.0)
        cube(rx, 4.45, 2.35, 0.06, 0.95, 0.06, FRAME_BLACK)

    cube(-9.8, 5.6, 0.20, 2.6, 3.4, 0.35, WOOD_CEDAR)
    for slat in range(12):
        sx = -11.0 + slat * (2.4 / 11.0)
        cube(sx, 5.6, 0.40, 0.08, 3.4, 0.05, WOOD_DARK)
    sconce(-9.8, 5.8, 0.45)

    cube(-4.5, 5.6, 0.22, 5.8, 3.2, 0.10, FRAME_BLACK)
    cube(-4.5, 5.6, 0.12, 5.6, 3.1, 0.05, c(255, 240, 195), emissive=True)
    g3 = cube(-4.5, 5.6, 0.25, 5.6, 3.1, 0.04, GLASS_PANE, opacity=0.82)
    window_glass.append(g3)
    for p in range(5):
        px = -7.2 + p * (5.4 / 4.0)
        cube(px, 5.6, 0.28, 0.08, 3.1, 0.04, FRAME_BLACK)
    for cx in [-6.4, -4.5, -2.6]:
        cube(cx, 5.6, 0.18, 1.4, 3.0, 0.02, CURTAIN_WHITE, opacity=0.88)

    cube(-1.1, 5.6, 0.26, 0.75, 3.4, 0.22, WALL_WHITE)
    sconce(-1.1, 5.8, 0.38)

    cube(2.6, 5.6, 0.22, 5.8, 3.2, 0.10, FRAME_BLACK)
    cube(2.6, 5.6, 0.12, 5.6, 3.1, 0.05, c(255, 240, 195), emissive=True)
    g4 = cube(2.6, 5.6, 0.25, 5.6, 3.1, 0.04, GLASS_PANE, opacity=0.82)
    window_glass.append(g4)
    for p in range(5):
        px = -0.1 + p * (5.4 / 4.0)
        cube(px, 5.6, 0.28, 0.08, 3.1, 0.04, FRAME_BLACK)
    for cx in [0.7, 2.6, 4.5]:
        cube(cx, 5.6, 0.18, 1.4, 3.0, 0.02, CURTAIN_WHITE, opacity=0.88)

    cube(6.4, 5.6, 0.26, 1.4, 3.4, 0.22, WALL_WHITE)
    sconce(6.4, 5.8, 0.38)

    for px in [-10.5, -1.1, 4.8]:
        cylinder(pos=V(px, 3.9, 1.8), axis=V(0, 0.55, 0), radius=0.28, color=WALL_WHITE)
        sphere(pos=V(px, 4.8, 1.8), radius=0.52, color=LEAF_GREEN)
        sphere(pos=V(px, 5.2, 1.8), radius=0.38, color=c(68, 165, 72))

    cube(-1.8, 7.55, -2.8, 21.6, 0.12, 10.2, WOOD_SOFFIT)
    cube(-1.8, 7.72, -2.8, 22.0, 0.22, 10.6, WALL_WHITE)
    cube(-1.8, 7.88, -2.8, 22.2, 0.14, 10.8, FRAME_BLACK)

    cube(-2.0, 7.35, 1.1, 20.0, 0.12, 2.6, WOOD_SOFFIT)
    cube(-2.0, 7.55, 1.1, 20.2, 0.35, 2.8, WALL_WHITE)
    cube(-2.0, 7.85, 1.1, 20.4, 0.25, 2.9, FRAME_BLACK)
    for lx in [-8.5, -4.5, 0.5, 4.5]:
        downlight(lx, 7.28, 1.1)

    s1 = cube(-2.0, 7.98, 2.56, 20.2, 0.06, 0.06, AMBER_LIGHT, emissive=True)
    strip_lights.append(s1)

    for layer in range(10):
        t = layer / 9.0
        ly = 7.96 + t * 1.65
        lx_span = 19.8 * (1.0 - t * 0.42)
        lz_span = 9.4 * (1.0 - t * 0.52)
        col = c(40, 44, 52) if layer % 2 == 0 else c(30, 33, 40)
        cube(-2.2, ly, -2.8, lx_span, 0.17, lz_span, col)

    cube(-2.2, 9.80, -2.8, 11.5, 0.16, 0.45, FRAME_BLACK)

    for rib_i in range(9):
        rib_x = -7.2 + rib_i * (10.0 / 8.0)
        cube(rib_x, 8.85, 0.8, 0.06, 1.6, 0.08, c(22, 24, 28))
        cube(rib_x, 8.85, -6.4, 0.06, 1.6, 0.08, c(22, 24, 28))

    cube(9.8, 8.75, -2.5, 2.8, 0.5, 5.4, STONE_GREY)
    cube(9.8, 9.05, -2.5, 2.9, 0.15, 5.5, STONE_DARK)
    s2 = cube(9.8, 8.65, 0.28, 2.85, 0.06, 0.06, AMBER_LIGHT, emissive=True)
    strip_lights.append(s2)

    post(-12.4, 0.0, 7.8, -7.8, 0.08, FRAME_BLACK)
    post(8.8, 0.0, 7.8, -7.8, 0.08, FRAME_BLACK)

def build_truck():
    bx, by, bz = -7.5, 0.65, -3.2
    cube(bx, by + 0.15, bz, 2.1, 0.75, 4.8, TRUCK_BLACK)
    cube(bx, by + 0.65, bz - 0.4, 2.0, 0.65, 2.2, TRUCK_BLACK)
    cube(bx, by + 0.68, bz + 0.72, 1.9, 0.58, 0.06, c(30, 32, 38))
    cube(bx, by + 0.68, bz - 1.52, 1.9, 0.58, 0.06, c(30, 32, 38))
    cube(bx + 1.01, by + 0.68, bz - 0.4, 0.04, 0.52, 2.0, c(30, 32, 38))
    cube(bx - 1.01, by + 0.68, bz - 0.4, 0.04, 0.52, 2.0, c(30, 32, 38))
    cube(bx, by + 0.25, bz + 2.42, 1.7, 0.35, 0.06, c(40, 42, 48))
    sphere(pos=V(bx, by + 0.25, bz + 2.46), radius=0.10, color=c(220, 222, 225))
    hl_l = sphere(pos=V(bx - 0.82, by + 0.25, bz + 2.42), radius=0.14, color=WARM_WHITE, emissive=True)
    hl_r = sphere(pos=V(bx + 0.82, by + 0.25, bz + 2.42), radius=0.14, color=WARM_WHITE, emissive=True)
    lamp_bulbs.extend([hl_l, hl_r])

    for wx, wz in [(-1.05, 1.3), (1.05, 1.3), (-1.05, -1.4), (1.05, -1.4)]:
        cylinder(pos=V(bx + wx - (0.12 if wx > 0 else -0.12), by - 0.25, bz + wz),
                 axis=V(0.24 if wx > 0 else -0.24, 0, 0), radius=0.42, color=c(20, 20, 22))
        cylinder(pos=V(bx + wx - (0.14 if wx > 0 else -0.14), by - 0.25, bz + wz),
                 axis=V(0.28 if wx > 0 else -0.28, 0, 0), radius=0.24, color=c(160, 165, 172))

def build_all():
    build_site()
    build_architecture()
    build_truck()
    build_gate_and_fence()

build_all()

night = True
gates_open = False

def toggle_night(_=None):
    global night
    night = not night
    if night:
        scene.background = V(0.12, 0.16, 0.28)
        scene.ambient = V(0.35, 0.38, 0.48)
        SUN_LIGHT.color = V(0.40, 0.45, 0.65)
        for b in lamp_bulbs:
            b.emissive = True
        for b in sconce_bulbs:
            b.emissive = True
        for b in lantern_caps:
            b.emissive = True
            b.color = WARM_WHITE
        for b in spot_lights:
            b.emissive = True
        for b in strip_lights:
            b.emissive = True
    else:
        scene.background = V(0.85, 0.90, 0.96)
        scene.ambient = V(0.65, 0.65, 0.68)
        SUN_LIGHT.color = V(1.0, 0.98, 0.92)
        for b in lamp_bulbs:
            b.emissive = False
        for b in sconce_bulbs:
            b.emissive = False
        for b in lantern_caps:
            b.emissive = False
            b.color = c(220, 224, 228)
        for b in spot_lights:
            b.emissive = False
        for b in strip_lights:
            b.emissive = False

def toggle_gate(_=None):
    global gates_open
    gates_open = not gates_open
    step = 5.5 if gates_open else -5.5
    for p in gate_left:
        p.pos.x -= step
    for p in gate_right:
        p.pos.x += step

def look(forward, centre, view_range):
    scene.forward = forward
    scene.center  = centre
    scene.range   = view_range

def go_front(_=None):
    look(V(0.0, -0.05, -0.99), V(-0.5, 2.8, 3.5), 13.0)

def go_front_gate(_=None):
    look(V(0.0, -0.02, -0.99), V(-2.6, 1.6, 8.5), 7.0)

def go_isometric(_=None):
    look(V(0.62, -0.38, -0.68), V(0.0, 3.2, 0.0), 18.0)

def go_carport(_=None):
    look(V(0.35, -0.15, -0.92), V(-7.0, 2.0, -1.0), 6.5)

def go_terrace(_=None):
    look(V(-0.25, -0.18, -0.95), V(-1.5, 5.2, 1.2), 7.0)

def go_aerial(_=None):
    look(V(-0.02, -1.0, -0.12), V(0.0, 2.0, 0.0), 22.0)

def go_backyard(_=None):
    look(V(0.0, -0.22, 0.97), V(0.0, 2.6, -7.0), 13.0)

def go_main_door(_=None):
    look(V(0.0, -0.06, -0.99), V(5.5, 1.8, 0.0), 5.5)

def key_pressed(evt):
    k = evt.key.lower()
    if k == "l":
        toggle_night()
    elif k == "g":
        toggle_gate()
    elif k == "1":
        go_front()
    elif k == "2":
        go_isometric()
    elif k == "3":
        go_carport()
    elif k == "4":
        go_terrace()
    elif k == "5":
        go_aerial()
    elif k == "6":
        go_backyard()
    elif k == "7":
        go_main_door()
    elif k == "8":
        go_front_gate()

scene.bind("keydown", key_pressed)

scene.caption = "Mouse: drag to orbit  |  Scroll to zoom  |  Keys: [L] Day/Night  [G] Gate  [1] to [8] Camera Views\n"

button(text="Front Gate & View", bind=go_front)
button(text="Gate Close-Up", bind=go_front_gate)
button(text="3D Isometric", bind=go_isometric)
button(text="Carport & Truck", bind=go_carport)
button(text="2nd-Floor Balcony", bind=go_terrace)
button(text="Top View", bind=go_aerial)
button(text="Back Yard", bind=go_backyard)
button(text="Main Door", bind=go_main_door)
scene.append_to_caption("\n")
button(text="Day / Night", bind=toggle_night)
button(text="Gate Open / Close", bind=toggle_gate)

go_front()

tick = 0
while True:
    rate(60)
    tick += 1
