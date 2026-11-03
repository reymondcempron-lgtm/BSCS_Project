
import math
import random
from vpython import (
    canvas, vector as V, box, sphere, cylinder, cone, pyramid, ring,
    distant_light, local_light, rate, button, color
)

random.seed(42)

TITLE = ("NAME: ANTONETTE B. LIBUT | COURSE: BSCS 3 | "
         "SUBJECT: GRAPHIC AND COMPUTING | MY DREAM HOUSE")

scene = canvas(
    title=TITLE,
    width=1180,
    height=740,
    background=V(0.88, 0.93, 0.98),
    autoscale=False
)
scene.lights = []
scene.ambient = V(0.60, 0.60, 0.62)

SUN_LIGHT = distant_light(direction=V(-0.4, -1.0, -0.6), color=V(1.0, 0.97, 0.90))
distant_light(direction=V(0.5, -0.4, 0.7), color=V(0.35, 0.38, 0.48))

def c(r, g, b):
    return V(r / 255.0, g / 255.0, b / 255.0)

ROOF_SLATE    = c(46, 50, 60)
ROOF_RIDGE    = c(36, 40, 48)
FASCIA_WHITE  = c(245, 245, 248)
WALL_CREAM    = c(242, 238, 230)
WALL_WHITE    = c(250, 250, 252)
WOOD_CLAD     = c(182, 122, 74)
WOOD_TRIM     = c(130, 80, 44)
DOOR_WOOD     = c(110, 68, 38)
GLASS_BLUE    = c(165, 210, 235)
GLASS_DARK    = c(80, 110, 130)
FRAME_DARK    = c(38, 42, 48)
SOLAR_BLUE    = c(24, 48, 108)

GRASS_1       = c(102, 172, 82)
GRASS_2       = c(88, 154, 70)
HEDGE_GREEN   = c(42, 112, 52)
TREE_LEAF     = c(52, 138, 58)
SAKURA_PINK   = c(248, 130, 175)
SOIL_BED      = c(92, 64, 46)
CONCRETE_PAVE = c(216, 214, 206)
PAVER_GREY    = c(188, 186, 180)
DRIVEWAY_COL  = c(224, 220, 212)
WALL_STUCCO   = c(228, 224, 215)
STREET_ASPH   = c(68, 70, 78)
WATER_DAY       = c(55, 175, 220)
WATER_NIGHT     = c(50, 225, 248)
POOL_LED_DAY    = c(195, 235, 245)
POOL_LED_NIGHT  = c(90, 255, 255)
STEEL_DARK    = c(48, 52, 60)
IRON_BLACK    = c(28, 30, 34)
AMBER_GLOW    = c(255, 225, 140)

lamp_bulbs   = []
window_glass = []
roof_objects = []
clouds       = []
stars        = []
car_lights   = []
pillar_lanterns = []
sun_parts    = []
birds        = []

def cube(x, y, z, sx, sy, sz, col, opacity=1.0, emissive=False):
    return box(pos=V(x, y, z), size=V(sx, sy, sz), color=col,
               opacity=opacity, emissive=emissive)

def post(x, y0, y1, z, r, col):
    return cylinder(pos=V(x, y0, z), axis=V(0, y1 - y0, 0), radius=r, color=col)

def bulb(x, y, z, r=0.14):
    b = sphere(pos=V(x, y, z), radius=r, color=AMBER_GLOW, emissive=True)
    lamp_bulbs.append(b)
    return b

def architectural_window(x, y, z, w, h, facing="z", panes_x=2, panes_y=1):
    if facing == "z":
        cube(x, y, z, w + 0.22, h + 0.22, 0.10, WALL_WHITE)
        cube(x, y, z + 0.04, w + 0.08, h + 0.08, 0.08, FRAME_DARK)
        g = cube(x, y, z + 0.06, w, h, 0.05, GLASS_BLUE, opacity=0.88)
        for i in range(1, panes_x):
            mx = x - w / 2 + (w * i / panes_x)
            cube(mx, y, z + 0.09, 0.06, h, 0.04, FRAME_DARK)
        for j in range(1, panes_y):
            my = y - h / 2 + (h * j / panes_y)
            cube(x, my, z + 0.09, w, 0.06, 0.04, FRAME_DARK)
    else:
        cube(x, y, z, 0.10, h + 0.22, w + 0.22, WALL_WHITE)
        cube(x + 0.04, y, z, 0.08, h + 0.08, w + 0.08, FRAME_DARK)
        g = cube(x + 0.06, y, z, 0.05, h, w, GLASS_BLUE, opacity=0.88)
        for i in range(1, panes_x):
            mz = z - w / 2 + (w * i / panes_x)
            cube(x + 0.09, y, mz, 0.04, h, 0.06, FRAME_DARK)
        for j in range(1, panes_y):
            my = y - h / 2 + (h * j / panes_y)
            cube(x + 0.09, my, z, 0.04, 0.06, w, FRAME_DARK)
    window_glass.append((g, GLASS_BLUE))
    return g

def wall_sconce(x, y, z, facing="+z"):
    dz = 0.06 if facing == "+z" else -0.06
    cylinder(pos=V(x, y, z), axis=V(0, 0, dz * 0.4), radius=0.22, color=c(35, 34, 38))
    cylinder(pos=V(x, y, z + dz * 0.35), axis=V(0, 0, dz * 0.25), radius=0.20, color=c(215, 175, 110))
    cylinder(pos=V(x, y, z + dz * 0.55), axis=V(0, 0, dz * 0.30), radius=0.15,
             color=c(255, 232, 175), emissive=True)
    bulb(x, y, z + dz * 0.85, 0.075)
    cube(x, y + 0.23, z + dz * 0.5, 0.08, 0.04, 0.06, c(215, 175, 110))
    cube(x, y - 0.23, z + dz * 0.5, 0.08, 0.04, 0.06, c(215, 175, 110))

def build_grounds():
    cube(-1.5, -0.4, 0, 52, 0.8, 38, c(155, 155, 160))

    for ix in range(-7, 6):
        for iz in range(-5, 5):
            col = GRASS_1 if (ix + iz) % 2 == 0 else GRASS_2
            cube(ix * 4 + 2, 0.02, iz * 4 + 1, 4, 0.05, 4, col)

    cube(0, 0.02, 21.5, 64, 0.14, 7.0, STREET_ASPH)
    for x in range(-28, 29, 6):
        cube(x, 0.10, 21.5, 2.8, 0.02, 0.25, c(245, 215, 60))

    cube(-1.5, 0.06, 17.6, 55, 0.12, 1.8, CONCRETE_PAVE)
    for x in range(-28, 26, 4):
        cube(x, 0.13, 17.6, 0.06, 0.02, 1.8, c(160, 160, 160))

    cube(-0.2, 0.07, 10.8, 3.4, 0.06, 9.6, PAVER_GREY)
    for i in range(5):
        cube(-0.2, 0.11, 7.2 + i * 1.8, 3.8, 0.04, 1.1, CONCRETE_PAVE)

    for s in range(3):
        cube(-0.2, 0.16 + s * 0.18, 5.0 - s * 0.45, 4.8 - s * 0.3, 0.20, 0.85, CONCRETE_PAVE)

    cube(12.5, 0.06, 10.5, 12.0, 0.06, 13.5, DRIVEWAY_COL)
    for dz in (5.5, 9.0, 12.5):
        cube(12.5, 0.10, dz, 11.6, 0.02, 0.08, c(175, 170, 160))

def build_mansion():
    cube(-11.5, 1.6, -0.5, 0.20, 3.2, 8.4, WALL_CREAM)
    cube(-4.5, 1.6, -4.7, 14.0, 3.2, 0.20, WALL_CREAM)
    cube(-7.0, 1.6, 3.73, 8.6, 3.1, 0.08, WOOD_CLAD)
    for k in range(11):
        cube(-7.0, 0.30 + k * 0.28, 3.78, 8.6, 0.04, 0.03, WOOD_TRIM)
    architectural_window(-7.0, 1.6, 3.82, 3.2, 1.8, "z", 3, 2)
    wall_sconce(-10.2, 1.8, 3.82)
    wall_sconce(-3.8, 1.8, 3.82)

    cube(-7.0, 0.38, 4.22, 3.50, 0.38, 0.60, c(42, 35, 30))
    cube(-7.0, 0.57, 4.22, 3.62, 0.05, 0.68, c(32, 26, 22))
    cube(-7.0, 0.20, 4.22, 3.56, 0.04, 0.64, c(32, 26, 22))
    cube(-7.0, 0.55, 4.22, 3.42, 0.06, 0.52, c(45, 34, 26))
    for brk_x in (-8.3, -7.0, -5.7):
        cube(brk_x, 0.10, 4.10, 0.06, 0.22, 0.32, IRON_BLACK)

    leaf_tones = [c(40, 105, 48), c(55, 135, 62), c(32, 85, 38), c(65, 150, 72)]
    for f_idx in range(16):
        fx = -8.45 + f_idx * 0.19
        fz = 4.22 + (0.10 if f_idx % 2 == 0 else -0.08)
        fy = 0.62 + (0.05 if (f_idx % 3 == 0) else -0.02)
        sphere(pos=V(fx, fy, fz), radius=0.15 + (f_idx % 3) * 0.02, color=leaf_tones[f_idx % 4])

    for ivy_idx in range(9):
        ix = -8.30 + ivy_idx * 0.33
        sphere(pos=V(ix, 0.52, 4.54), radius=0.10, color=c(45, 115, 52))
        sphere(pos=V(ix + 0.03, 0.40, 4.56), radius=0.08, color=c(55, 130, 60))
        if ivy_idx % 2 == 1:
            sphere(pos=V(ix + 0.02, 0.30, 4.54), radius=0.065, color=c(38, 95, 44))

    lavender_shades = [c(145, 110, 195), c(170, 135, 220), c(125, 90, 180)]
    for lav_i in range(11):
        lx = -8.35 + lav_i * 0.27
        cylinder(pos=V(lx, 0.60, 4.02), axis=V(0, 0.28, 0), radius=0.015, color=c(60, 125, 55))
        cylinder(pos=V(lx, 0.72, 4.02), axis=V(0, 0.22, 0), radius=0.045, color=lavender_shades[lav_i % 3])
        sphere(pos=V(lx, 0.94, 4.02), radius=0.04, color=lavender_shades[(lav_i + 1) % 3])

    palette = [
        c(255, 145, 175),
        c(245, 75, 115),
        c(255, 252, 248),
        c(185, 135, 225),
        c(255, 160, 135),
        c(255, 220, 75),
    ]
    flower_clusters = [
        (-8.35, 0.68, 4.28, 0), (-8.05, 0.73, 4.38, 1), (-7.75, 0.70, 4.22, 2),
        (-7.45, 0.75, 4.34, 0), (-7.15, 0.72, 4.24, 3), (-6.85, 0.76, 4.36, 1),
        (-6.55, 0.71, 4.22, 4), (-6.25, 0.75, 4.35, 0), (-5.95, 0.72, 4.24, 2),
        (-5.65, 0.69, 4.32, 5)
    ]
    for cx, cy, cz, p_idx in flower_clusters:
        f_col = palette[p_idx % len(palette)]
        sphere(pos=V(cx, cy, cz), radius=0.10, color=f_col)
        for pet_ang, (p_dx, p_dy, p_dz) in enumerate([
            (-0.06, 0.03, 0.04), (0.06, 0.03, -0.04),
            (-0.04, -0.03, -0.05), (0.05, -0.02, 0.05)
        ]):
            sphere(pos=V(cx + p_dx, cy + p_dy, cz + p_dz), radius=0.075, color=f_col * 0.95)
        sphere(pos=V(cx, cy + 0.04, cz + 0.02), radius=0.032, color=c(255, 215, 45))

    for al_x in (-8.15, -7.65, -7.10, -6.55, -6.00):
        sphere(pos=V(al_x, 0.44, 4.57), radius=0.045, color=c(255, 255, 255))
        sphere(pos=V(al_x + 0.06, 0.38, 4.56), radius=0.040, color=c(250, 248, 242))

    cube(-2.1, 2.7, 4.3, 0.45, 5.4, 0.45, WALL_WHITE)
    cube(1.7, 2.7, 4.3, 0.45, 5.4, 0.45, WALL_WHITE)
    cube(-2.1, 0.35, 4.3, 0.65, 0.7, 0.65, PAVER_GREY)
    cube(1.7, 0.35, 4.3, 0.65, 0.7, 0.65, PAVER_GREY)

    global door_leaf, door_handle, DOOR_PIVOT
    cube(-0.2, 1.5, 3.75, 2.8, 2.8, 0.10, FRAME_DARK)
    cube(-1.25, 1.5, 3.78, 0.5, 2.6, 0.05, GLASS_DARK, opacity=0.9)
    cube(0.85, 1.5, 3.78, 0.5, 2.6, 0.05, GLASS_DARK, opacity=0.9)
    DOOR_PIVOT = V(-0.95, 1.5, 3.82)
    door_leaf = cube(-0.2, 1.5, 3.82, 1.5, 2.6, 0.08, DOOR_WOOD)
    for d_stripe in range(5):
        cube(-0.2, 0.5 + d_stripe * 0.5, 3.87, 1.4, 0.03, 0.02, WOOD_TRIM)
    door_handle = cube(0.4, 1.45, 3.90, 0.06, 0.45, 0.06, c(240, 210, 140))
    wall_sconce(-1.7, 2.1, 3.85)
    wall_sconce(1.3, 2.1, 3.85)

    cube(11.5, 1.6, -0.5, 0.20, 3.2, 8.4, WALL_CREAM)
    cube(7.0, 1.6, -4.7, 9.0, 3.2, 0.20, WALL_CREAM)
    cube(2.5, 1.6, -0.5, 0.20, 3.2, 8.4, WALL_CREAM)

    cube(7.0, 1.6, 3.73, 8.6, 3.1, 0.08, WOOD_CLAD)
    for k in range(11):
        cube(7.0, 0.30 + k * 0.28, 3.78, 8.6, 0.04, 0.03, WOOD_TRIM)

    cube(7.0, 1.45, 3.80, 5.8, 2.45, 0.06, WALL_WHITE)
    cube(7.0, 1.45, 3.82, 5.9, 2.52, 0.04, FRAME_DARK)
    for g_rib in range(7):
        cube(7.0, 0.45 + g_rib * 0.35, 3.84, 5.7, 0.04, 0.03, c(195, 195, 200))
    wall_sconce(3.6, 1.8, 3.84)
    wall_sconce(10.4, 1.8, 3.84)

    cube(9.8, 0.32, 4.22, 2.60, 0.35, 0.65, c(42, 35, 30))
    cube(9.8, 0.48, 4.22, 2.70, 0.04, 0.72, c(32, 26, 22))
    for rf_i in range(10):
        r_fx = 8.75 + rf_i * 0.22
        sphere(pos=V(r_fx, 0.52, 4.22 + (0.08 if rf_i % 2 == 0 else -0.06)),
               radius=0.14, color=leaf_tones[rf_i % 4])
    for r_cx, r_col_i in [(8.8, 0), (9.1, 2), (9.4, 1), (9.7, 3), (10.0, 4), (10.3, 0), (10.6, 1)]:
        sphere(pos=V(r_cx, 0.62, 4.26), radius=0.10, color=palette[r_col_i])
        sphere(pos=V(r_cx, 0.65, 4.28), radius=0.03, color=c(255, 215, 45))

    cube(14.0, 1.5, -0.5, 5.0, 3.0, 7.8, WALL_CREAM)
    cube(14.0, 1.5, 3.42, 4.6, 2.7, 0.08, FRAME_DARK)
    g_sun = cube(14.0, 1.5, 3.46, 4.4, 2.5, 0.05, GLASS_BLUE, opacity=0.82)
    window_glass.append((g_sun, GLASS_BLUE))
    for m in (-1.4, 0.0, 1.4):
        cube(14.0 + m, 1.5, 3.50, 0.08, 2.5, 0.06, FRAME_DARK)
    wall_sconce(16.0, 1.8, 3.52)
    build_hipped_roof(14.0, 3.1, -0.5, 5.6, 1.4, 8.4, tiers=4)

    cube(0.0, 3.2, -0.5, 23.2, 0.18, 8.6, CONCRETE_PAVE)

    cube(-11.4, 4.5, -0.8, 0.20, 2.6, 7.8, WALL_CREAM)
    cube(-7.0, 4.5, -4.7, 8.8, 2.6, 0.20, WALL_CREAM)
    cube(-2.6, 4.5, -0.8, 0.20, 2.6, 7.8, WALL_CREAM)

    cube(-2.9, 4.22, 3.12, 0.60, 2.05, 0.16, WALL_CREAM)
    cube(-11.1, 4.22, 3.12, 0.60, 2.05, 0.16, WALL_CREAM)

    cube(-7.0, 4.22, 3.12, 7.6, 2.05, 0.08, FRAME_DARK)
    g_terrace_left = cube(-7.0, 4.22, 3.14, 7.4, 1.95, 0.04, GLASS_BLUE, opacity=0.35)
    window_glass.append((g_terrace_left, GLASS_BLUE))

    for mx in (-8.85, -7.0, -5.15):
        cube(mx, 4.22, 3.16, 0.06, 1.95, 0.06, FRAME_DARK)
    cube(-7.0, 4.85, 3.16, 7.4, 0.05, 0.06, FRAME_DARK)

    cylinder(pos=V(-6.85, 3.85, 3.18), axis=V(0, 0.60, 0), radius=0.02, color=c(225, 230, 235))
    cylinder(pos=V(-7.15, 3.85, 3.18), axis=V(0, 0.60, 0), radius=0.02, color=c(225, 230, 235))

    wall_sconce(-3.3, 4.3, 3.18)
    wall_sconce(-10.7, 4.3, 3.18)

    cube(-7.0, 3.15, 3.95, 7.8, 0.18, 1.70, CONCRETE_PAVE)
    cube(-7.0, 3.25, 3.95, 7.4, 0.02, 1.50, c(195, 145, 95))
    for tk in range(5):
        cube(-7.0, 3.26, 3.35 + tk * 0.30, 7.4, 0.01, 0.02, c(150, 95, 55))

    cube(-7.0, 3.75, 4.80, 7.6, 0.80, 0.04, GLASS_BLUE, opacity=0.35)
    cube(-7.0, 4.16, 4.80, 7.7, 0.06, 0.08, WOOD_TRIM)
    for bx in (-3.7, -1.85, 0.0, 1.85, 3.7):
        cube(-7.0 + bx, 3.75, 4.80, 0.06, 0.82, 0.06, FRAME_DARK)

    cube(-3.15, 3.75, 3.96, 0.04, 0.80, 1.68, GLASS_BLUE, opacity=0.35)
    cube(-3.15, 4.16, 3.96, 0.08, 0.06, 1.70, WOOD_TRIM)
    cube(-10.85, 3.75, 3.96, 0.04, 0.80, 1.68, GLASS_BLUE, opacity=0.35)
    cube(-10.85, 4.16, 3.96, 0.08, 0.06, 1.70, WOOD_TRIM)

    cube(-8.6, 3.36, 3.95, 1.65, 0.14, 1.15, c(175, 125, 75))
    cube(-8.6, 3.48, 3.95, 1.55, 0.12, 1.05, c(248, 246, 242))
    cube(-9.35, 3.72, 3.95, 0.14, 0.40, 1.05, c(175, 125, 75))
    cylinder(pos=V(-9.25, 3.65, 3.55), axis=V(0, 0, 0.80), radius=0.09, color=c(60, 160, 175))
    cube(-8.85, 3.66, 3.75, 0.10, 0.22, 0.28, c(245, 165, 185))
    cube(-8.85, 3.66, 4.15, 0.10, 0.22, 0.28, c(245, 215, 110))
    cube(-8.0, 3.56, 3.95, 0.32, 0.06, 0.95, c(120, 180, 170))

    cylinder(pos=V(-4.8, 3.26, 4.2), axis=V(-0.20, 0.82, -0.15), radius=0.02, color=c(95, 62, 38))
    cylinder(pos=V(-4.8, 3.26, 4.2), axis=V(0.24, 0.82, -0.15), radius=0.02, color=c(95, 62, 38))
    cylinder(pos=V(-4.8, 3.26, 4.2), axis=V(0.00, 0.82, 0.26), radius=0.02, color=c(95, 62, 38))
    cylinder(pos=V(-4.8, 4.08, 4.2), axis=V(0, 0.10, 0), radius=0.045, color=c(225, 185, 95))
    cylinder(pos=V(-4.95, 4.04, 3.95), axis=V(0.18, 0.26, 0.55), radius=0.052, color=c(235, 195, 95))
    cylinder(pos=V(-4.77, 4.30, 4.50), axis=V(0.05, 0.08, 0.15), radius=0.068, color=c(245, 215, 110))
    cylinder(pos=V(-4.98, 4.00, 3.87), axis=V(-0.04, -0.06, -0.12), radius=0.028, color=c(45, 45, 50))

    cylinder(pos=V(-6.8, 3.26, 3.95), axis=V(0, 0.32, 0), radius=0.18, color=c(230, 225, 218))
    cylinder(pos=V(-6.8, 3.58, 3.95), axis=V(0, 0.04, 0), radius=0.28, color=c(242, 238, 232))
    cylinder(pos=V(-6.86, 3.62, 3.85), axis=V(0, 0.10, 0), radius=0.045, color=c(250, 250, 250))
    cylinder(pos=V(-6.86, 3.70, 3.85), axis=V(0, 0.015, 0), radius=0.038, color=c(180, 130, 90))
    cube(-6.75, 3.63, 4.02, 0.22, 0.02, 0.16, c(245, 240, 230))
    cube(-6.75, 3.62, 4.02, 0.24, 0.01, 0.18, c(65, 80, 130))

    cylinder(pos=V(-10.4, 3.26, 4.45), axis=V(0, 0.36, 0), radius=0.20, color=c(195, 115, 75))
    cylinder(pos=V(-10.4, 3.62, 4.45), axis=V(0.04, 0.45, -0.02), radius=0.042, color=c(95, 75, 55))
    sphere(pos=V(-10.4, 4.18, 4.45), radius=0.30, color=c(95, 135, 90))
    sphere(pos=V(-10.3, 4.32, 4.40), radius=0.22, color=c(110, 150, 105))
    sphere(pos=V(-10.5, 4.28, 4.50), radius=0.20, color=c(90, 130, 85))

    cube(-0.2, 4.25, -4.7, 5.4, 2.2, 0.20, WALL_CREAM)
    cube(-0.2, 4.25, 3.75, 5.4, 2.2, 0.20, WALL_CREAM)
    cube(-0.2, 3.20, 3.75, 5.4, 0.18, 1.40, CONCRETE_PAVE)
    cube(-0.2, 5.3, 4.3, 4.8, 0.25, 0.65, WALL_WHITE)

    cube(-0.2, 4.20, 3.78, 3.35, 1.95, 0.04, WOOD_CLAD)
    for ck in range(8):
        cube(-0.2, 3.35 + ck * 0.24, 3.81, 3.35, 0.03, 0.02, WOOD_TRIM)

    cube(-0.2, 4.20, 3.83, 1.76, 1.60, 0.05, WALL_WHITE)
    cube(-0.2, 4.20, 3.85, 1.66, 1.50, 0.04, FRAME_DARK)
    g_center_portico = cube(-0.2, 4.20, 3.87, 1.54, 1.38, 0.04, GLASS_BLUE, opacity=0.85)
    window_glass.append((g_center_portico, GLASS_BLUE))
    for pmx in (-0.2 - 0.26, -0.2 + 0.26):
        cube(pmx, 4.20, 3.89, 0.04, 1.38, 0.04, FRAME_DARK)
    cube(-0.2, 4.65, 3.89, 1.54, 0.04, 0.04, FRAME_DARK)

    cube(-0.2, 3.95, 3.98, 1.76, 0.04, 0.04, IRON_BLACK)
    cube(-0.2, 3.42, 3.98, 1.76, 0.04, 0.04, IRON_BLACK)
    for pki in range(10):
        pk_x = -0.95 + pki * 0.17
        cube(pk_x, 3.68, 3.98, 0.025, 0.52, 0.025, IRON_BLACK)
    for b_med in (-0.61, -0.20, 0.21):
        sphere(pos=V(b_med, 3.68, 4.00), radius=0.03, color=c(215, 175, 110))

    cube(-0.2, 3.40, 4.01, 1.54, 0.05, 0.10, c(42, 35, 30))
    for jf_i in range(8):
        jf_x = -0.76 + jf_i * 0.16
        sphere(pos=V(jf_x, 3.46, 4.03), radius=0.05, color=c(55, 135, 62))
        sphere(pos=V(jf_x, 3.41, 4.05), radius=0.038,
               color=c(255, 160, 185) if jf_i % 2 == 0 else c(255, 255, 255))

    wall_sconce(-1.45, 4.25, 3.82)
    wall_sconce(1.05, 4.25, 3.82)

    cube(-0.2, 5.15, 4.15, 3.35, 0.08, 0.14, WALL_WHITE)
    for d_idx in range(11):
        cube(-1.50 + d_idx * 0.26, 5.10, 4.18, 0.08, 0.05, 0.06, WALL_WHITE)

    cube(-0.2, 5.8, 3.8, 3.2, 0.8, 0.12, FRAME_DARK)
    for tw in (-0.9, 0.0, 0.9):
        cube(-0.2 + tw, 5.8, 3.86, 0.7, 0.6, 0.04, GLASS_BLUE, opacity=0.88)

    cube(11.4, 4.5, -0.8, 0.20, 2.6, 7.8, WALL_CREAM)
    cube(7.0, 4.5, -4.7, 8.8, 2.6, 0.20, WALL_CREAM)
    cube(2.6, 4.5, -0.8, 0.20, 2.6, 7.8, WALL_CREAM)

    cube(2.9, 4.22, 3.12, 0.60, 2.05, 0.16, WALL_CREAM)
    cube(11.1, 4.22, 3.12, 0.60, 2.05, 0.16, WALL_CREAM)

    cube(7.0, 4.22, 3.12, 7.6, 2.05, 0.08, FRAME_DARK)
    g_terrace = cube(7.0, 4.22, 3.14, 7.4, 1.95, 0.04, GLASS_BLUE, opacity=0.35)
    window_glass.append((g_terrace, GLASS_BLUE))

    for mx in (5.15, 7.0, 8.85):
        cube(mx, 4.22, 3.16, 0.06, 1.95, 0.06, FRAME_DARK)
    cube(7.0, 4.85, 3.16, 7.4, 0.05, 0.06, FRAME_DARK)

    cylinder(pos=V(6.85, 3.85, 3.18), axis=V(0, 0.60, 0), radius=0.02, color=c(225, 230, 235))
    cylinder(pos=V(7.15, 3.85, 3.18), axis=V(0, 0.60, 0), radius=0.02, color=c(225, 230, 235))

    wall_sconce(3.3, 4.3, 3.18)
    wall_sconce(10.7, 4.3, 3.18)

    cube(7.0, 3.15, 3.95, 7.8, 0.18, 1.70, CONCRETE_PAVE)
    cube(7.0, 3.25, 3.95, 7.4, 0.02, 1.50, c(195, 145, 95))
    for tk in range(5):
        cube(7.0, 3.26, 3.35 + tk * 0.30, 7.4, 0.01, 0.02, c(150, 95, 55))

    cube(7.0, 3.75, 4.80, 7.6, 0.80, 0.04, GLASS_BLUE, opacity=0.35)
    cube(7.0, 4.16, 4.80, 7.7, 0.06, 0.08, WOOD_TRIM)
    for bx in (-3.7, -1.85, 0.0, 1.85, 3.7):
        cube(7.0 + bx, 3.75, 4.80, 0.06, 0.82, 0.06, FRAME_DARK)

    cube(3.15, 3.75, 3.96, 0.04, 0.80, 1.68, GLASS_BLUE, opacity=0.35)
    cube(3.15, 4.16, 3.96, 0.08, 0.06, 1.70, WOOD_TRIM)
    cube(10.85, 3.75, 3.96, 0.04, 0.80, 1.68, GLASS_BLUE, opacity=0.35)
    cube(10.85, 4.16, 3.96, 0.08, 0.06, 1.70, WOOD_TRIM)

    for cdx in (-0.28, 0.28):
        for cdz in (-0.26, 0.26):
            cube(5.4 + cdx, 3.36, 4.0 + cdz, 0.04, 0.20, 0.04, FRAME_DARK)
    cube(5.4, 3.46, 4.0, 0.70, 0.06, 0.65, c(175, 125, 75))
    cube(5.4, 3.52, 4.0, 0.64, 0.08, 0.60, c(248, 246, 242))
    cube(5.4, 3.78, 3.72, 0.64, 0.44, 0.06, c(248, 246, 242))
    cube(5.4, 3.68, 3.78, 0.32, 0.22, 0.06, c(60, 160, 175))

    for cdx in (-0.28, 0.28):
        for cdz in (-0.26, 0.26):
            cube(8.6 + cdx, 3.36, 4.0 + cdz, 0.04, 0.20, 0.04, FRAME_DARK)
    cube(8.6, 3.46, 4.0, 0.70, 0.06, 0.65, c(175, 125, 75))
    cube(8.6, 3.52, 4.0, 0.64, 0.08, 0.60, c(248, 246, 242))
    cube(8.6, 3.78, 3.72, 0.64, 0.44, 0.06, c(248, 246, 242))
    cube(8.6, 3.68, 3.78, 0.32, 0.22, 0.06, c(235, 115, 115))

    cylinder(pos=V(7.0, 3.26, 4.0), axis=V(0, 0.03, 0), radius=0.22, color=c(215, 175, 110))
    cylinder(pos=V(7.0, 3.26, 4.0), axis=V(0, 0.35, 0), radius=0.06, color=c(215, 175, 110))
    cylinder(pos=V(7.0, 3.61, 4.0), axis=V(0, 0.04, 0), radius=0.34, color=c(250, 248, 245))
    cylinder(pos=V(7.0, 3.65, 4.0), axis=V(0, 0.12, 0), radius=0.045, color=c(255, 185, 60), opacity=0.85)

    for px, pz in [(3.6, 4.45), (10.4, 4.45)]:
        cylinder(pos=V(px, 3.26, pz), axis=V(0, 0.30, 0), radius=0.18, color=WALL_WHITE)
        sphere(pos=V(px, 3.65, pz), radius=0.22, color=c(55, 135, 65))

    build_hipped_roof(-7.0, 5.3, 3.4, 9.2, 1.15, 2.8, tiers=4)

    build_hipped_roof(7.0, 5.3, 3.4, 9.2, 1.15, 2.8, tiers=4)

    build_hipped_roof(-0.2, 5.45, 4.1, 5.2, 1.15, 2.0, tiers=3)

    build_hipped_roof(-7.0, 5.7, -0.8, 9.6, 2.7, 8.6, tiers=6)
    add_solar_array(-7.0, 7.3, -0.8, count=4, angle=0.28)

    build_hipped_roof(7.0, 5.7, -0.8, 9.6, 2.7, 8.6, tiers=6)
    add_solar_array(7.0, 7.3, -0.8, count=4, angle=0.28)

    build_hipped_roof(-0.2, 6.4, -1.0, 8.6, 3.3, 8.8, tiers=7)

    dm_b = cube(-0.2, 8.2, 2.4, 4.2, 1.3, 1.2, WALL_CREAM)
    dm_f = cube(-0.2, 8.2, 3.02, 3.8, 1.0, 0.08, FRAME_DARK)
    roof_objects.extend([dm_b, dm_f])
    g_dl = cube(-1.65, 8.2, 2.98, 0.7, 0.9, 0.05, SOLAR_BLUE)
    g_dr = cube(1.25, 8.2, 2.98, 0.7, 0.9, 0.05, SOLAR_BLUE)
    roof_objects.extend([g_dl, g_dr])
    for dw in (-0.6, 0.0, 0.6):
        g_d = cube(-0.2 + dw, 8.2, 3.06, 0.50, 0.85, 0.05, GLASS_BLUE, opacity=0.9)
        window_glass.append((g_d, GLASS_BLUE))
        roof_objects.append(g_d)
    build_hipped_roof(-0.2, 8.85, 2.4, 4.6, 0.95, 1.6, tiers=3)

def build_hipped_roof(cx, base_y, cz, w, h, d, tiers=5):
    f = cube(cx, base_y + 0.06, cz, w + 0.4, 0.12, d + 0.4, FASCIA_WHITE)
    roof_objects.append(f)
    tier_h = h / tiers
    for i in range(tiers):
        t = i / float(tiers)
        cur_w = w * (1.0 - t * 0.65)
        cur_d = d * (1.0 - t * 0.65)
        cur_y = base_y + 0.12 + (i + 0.5) * tier_h
        r_box = cube(cx, cur_y, cz, cur_w, tier_h + 0.02, cur_d, ROOF_SLATE)
        roof_objects.append(r_box)
    top_w = w * (1.0 - 0.65)
    top_d = d * (1.0 - 0.65)
    cap = cube(cx, base_y + 0.12 + tiers * tier_h, cz, top_w, 0.08, top_d, ROOF_RIDGE)
    roof_objects.append(cap)

def add_solar_array(cx, y, cz, count=4, angle=0.20):
    total_w = count * 1.35
    for i in range(count):
        px = cx - total_w / 2 + 0.68 + i * 1.35
        p = cube(px, y, cz, 1.25, 0.06, 1.9, SOLAR_BLUE)
        p.rotate(angle=angle, axis=V(1, 0, 0))
        roof_objects.append(p)
        pf = cube(px, y, cz, 1.29, 0.04, 1.94, c(200, 210, 220))
        pf.rotate(angle=angle, axis=V(1, 0, 0))
        roof_objects.append(pf)

def build_carport_and_vehicles():
    cpx, cpz = 13.5, 9.5
    pw, pd, ph = 9.2, 8.4, 3.4

    for sx in (-pw / 2 + 0.4, pw / 2 - 0.4):
        for sz in (-pd / 2 + 0.4, pd / 2 - 0.4):
            cube(cpx + sx, ph / 2, cpz + sz, 0.35, ph, 0.35, STEEL_DARK)

    cube(cpx, ph, cpz - pd / 2 + 0.4, pw, 0.25, 0.35, STEEL_DARK)
    cube(cpx, ph, cpz + pd / 2 - 0.4, pw, 0.25, 0.35, STEEL_DARK)
    cube(cpx - pw / 2 + 0.4, ph, cpz, 0.35, 0.25, pd, STEEL_DARK)
    cube(cpx + pw / 2 - 0.4, ph, cpz, 0.35, 0.25, pd, STEEL_DARK)

    for l in range(12):
        lz = (cpz - pd / 2 + 0.8) + l * (pd - 1.6) / 11.0
        louver = cube(cpx, ph + 0.16, lz, pw - 0.8, 0.06, 0.45, c(55, 60, 72))
        louver.rotate(angle=0.28, axis=V(1, 0, 0))

    build_mclaren_supercar(cpx, cpz)

    build_sport_bike(cpx - 2.8, cpz)
    build_sport_bike(cpx + 2.8, cpz)

    cube(17.7, 0.24, cpz, 0.32, 0.36, 8.4, WALL_STUCCO)
    cube(17.7, 0.44, cpz, 0.42, 0.06, 8.6, CONCRETE_PAVE)
    g_cp_right = cube(17.7, 1.85, cpz, 0.05, 2.70, 7.6, GLASS_BLUE, opacity=0.35)
    window_glass.append((g_cp_right, GLASS_BLUE))
    cube(17.7, 3.22, cpz, 0.10, 0.08, 7.6, STEEL_DARK)
    cube(17.7, 0.48, cpz, 0.10, 0.08, 7.6, STEEL_DARK)
    cube(17.7, 1.85, cpz, 0.08, 0.06, 7.6, STEEL_DARK)
    for div_i in (1, 2, 3):
        cube(17.7, 1.85, (cpz - 3.8) + div_i * (7.6 / 4.0), 0.08, 2.70, 0.06, STEEL_DARK)

    cube(9.3, 0.24, cpz, 0.32, 0.36, 8.4, WALL_STUCCO)
    cube(9.3, 0.44, cpz, 0.42, 0.06, 8.6, CONCRETE_PAVE)
    g_cp_left = cube(9.3, 1.85, cpz, 0.05, 2.70, 7.6, GLASS_BLUE, opacity=0.35)
    window_glass.append((g_cp_left, GLASS_BLUE))
    cube(9.3, 3.22, cpz, 0.10, 0.08, 7.6, STEEL_DARK)
    cube(9.3, 0.48, cpz, 0.10, 0.08, 7.6, STEEL_DARK)
    cube(9.3, 1.85, cpz, 0.08, 0.06, 7.6, STEEL_DARK)
    for div_i in (1, 2, 3):
        cube(9.3, 1.85, (cpz - 3.8) + div_i * (7.6 / 4.0), 0.08, 2.70, 0.06, STEEL_DARK)

    cube(cpx, 0.12, cpz + 2.6, 2.2, 0.12, 0.20, CONCRETE_PAVE)
    for y_stripe in (-0.7, 0.0, 0.7):
        cube(cpx + y_stripe, 0.13, cpz + 2.6, 0.35, 0.02, 0.22, c(245, 215, 50))
    cube(cpx - 2.8, 0.10, cpz + 1.8, 0.9, 0.10, 0.16, CONCRETE_PAVE)
    cube(cpx + 2.8, 0.10, cpz + 1.8, 0.9, 0.10, 0.16, CONCRETE_PAVE)

def build_mclaren_supercar(x, z):
    ORANGE_CAR = c(225, 95, 20)
    DARK_TRIM  = c(28, 30, 36)

    cube(x, 0.42, z, 2.1, 0.36, 4.4, ORANGE_CAR)
    cube(x, 0.86, z - 0.15, 1.7, 0.45, 2.3, ORANGE_CAR)
    cube(x, 0.90, z - 0.15, 1.74, 0.35, 2.0, c(30, 45, 60), opacity=0.92)
    cube(x, 0.48, z + 1.2, 1.8, 0.22, 1.5, ORANGE_CAR)
    cube(x, 0.32, z + 2.15, 1.9, 0.18, 0.2, DARK_TRIM)
    cube(x, 0.35, z - 2.15, 1.9, 0.20, 0.2, DARK_TRIM)
    cube(x, 0.95, z - 2.1, 1.8, 0.06, 0.35, DARK_TRIM)
    for sp in (-0.6, 0.6):
        cube(x + sp, 0.78, z - 2.1, 0.06, 0.30, 0.10, DARK_TRIM)

    for sx in (-1.02, 1.02):
        for dz in (-1.35, 1.35):
            cylinder(pos=V(x + sx - 0.09, 0.34, z + dz), axis=V(0.18, 0, 0),
                     radius=0.34, color=c(18, 18, 20))
            cylinder(pos=V(x + sx - 0.095, 0.34, z + dz), axis=V(0.19, 0, 0),
                     radius=0.20, color=c(190, 195, 205))

    for sx in (-0.65, 0.65):
        hl = cube(x + sx, 0.52, z + 2.18, 0.38, 0.10, 0.06, c(255, 250, 220), emissive=True)
        car_lights.append(hl)
        tl = cube(x + sx, 0.52, z - 2.18, 0.38, 0.08, 0.06, c(230, 20, 20), emissive=True)
        car_lights.append(tl)

def build_sport_bike(x, z):
    BIKE_BLUE = c(35, 75, 195)
    BIKE_DARK = c(30, 32, 38)

    cube(x, 0.75, z, 0.45, 0.55, 1.6, BIKE_BLUE)
    cube(x, 1.02, z + 0.3, 0.50, 0.22, 0.55, BIKE_DARK)
    cube(x, 1.08, z - 0.7, 0.95, 0.06, 0.06, c(180, 180, 190))
    cube(x, 1.15, z + 0.5, 0.35, 0.25, 0.06, GLASS_BLUE, opacity=0.8)

    for dz in (-0.75, 0.75):
        cylinder(pos=V(x - 0.08, 0.35, z + dz), axis=V(0.16, 0, 0),
                 radius=0.35, color=c(18, 18, 22))
        cylinder(pos=V(x - 0.085, 0.35, z + dz), axis=V(0.17, 0, 0),
                 radius=0.20, color=c(180, 185, 190))

def build_pool_and_garden():
    cube(-16.2, 0.08, -4.8, 10.4, 0.12, 16.0, c(205, 145, 95))
    for k in range(21):
        cube(-16.2, 0.15, -12.4 + k * 0.76, 10.2, 0.02, 0.04, c(150, 95, 55))

    global pool_water, pool_underwater_lights, pool_glow_floor, pool_night_light
    pool_underwater_lights = []

    pool_glow_floor = cube(-15.5, 0.05, -5.8, 6.1, 0.02, 10.1, c(75, 195, 230), opacity=0.95)

    pool_water = cube(-15.5, 0.16, -5.8, 6.4, 0.08, 10.4, WATER_DAY, opacity=0.92)

    cube(-15.5, 0.18, -11.15, 6.8, 0.06, 0.40, WALL_WHITE)
    cube(-15.5, 0.18, -0.45,  6.8, 0.06, 0.40, WALL_WHITE)
    cube(-18.85, 0.18, -5.8,  0.40, 0.06, 11.1, WALL_WHITE)
    cube(-12.15, 0.18, -5.8,  0.40, 0.06, 11.1, WALL_WHITE)

    for uz in (-9.0, -5.8, -2.6):
        cylinder(pos=V(-18.66, 0.08, uz), axis=V(0.03, 0, 0), radius=0.18, color=c(225, 230, 235))
        lens = cylinder(pos=V(-18.64, 0.08, uz), axis=V(0.02, 0, 0), radius=0.14, color=POOL_LED_DAY)
        pool_underwater_lights.append(lens)

    for uz in (-9.0, -5.8, -2.6):
        cylinder(pos=V(-12.34, 0.08, uz), axis=V(-0.03, 0, 0), radius=0.18, color=c(225, 230, 235))
        lens = cylinder(pos=V(-12.36, 0.08, uz), axis=V(-0.02, 0, 0), radius=0.14, color=POOL_LED_DAY)
        pool_underwater_lights.append(lens)

    for ux in (-17.0, -14.0):
        cylinder(pos=V(ux, 0.08, -10.96), axis=V(0, 0, 0.03), radius=0.18, color=c(225, 230, 235))
        lens = cylinder(pos=V(ux, 0.08, -10.94), axis=V(0, 0, 0.02), radius=0.14, color=POOL_LED_DAY)
        pool_underwater_lights.append(lens)

    for ux in (-17.0, -14.0):
        cylinder(pos=V(ux, 0.08, -0.64), axis=V(0, 0, -0.03), radius=0.18, color=c(225, 230, 235))
        lens = cylinder(pos=V(ux, 0.08, -0.66), axis=V(0, 0, -0.02), radius=0.14, color=POOL_LED_DAY)
        pool_underwater_lights.append(lens)

    pool_night_light = local_light(pos=V(-15.5, 0.5, -5.8), color=V(0, 0, 0))

    for step_i in range(3):
        cube(-15.5, 0.12 - step_i * 0.04, -0.9 - step_i * 0.45, 5.8, 0.04, 0.45, c(185, 235, 245))

    for lx_off in (-0.4, 0.4):
        cylinder(pos=V(-15.5 + lx_off, 0.18, -10.9), axis=V(0, 0.65, 0), radius=0.035, color=c(225, 230, 235))
        cylinder(pos=V(-15.5 + lx_off, 0.83, -10.9), axis=V(0, 0, 0.35), radius=0.035, color=c(225, 230, 235))
        cylinder(pos=V(-15.5 + lx_off, 0.83, -10.55), axis=V(0, -0.75, 0), radius=0.035, color=c(225, 230, 235))

    def beach_lounger(bx, bz, facing="north"):
        if facing == "north":
            cube(bx, 0.26, bz, 0.90, 0.16, 2.1, c(65, 48, 38))
            cube(bx, 0.38, bz - 0.20, 0.86, 0.12, 1.4, c(250, 250, 252))
            hr = cube(bx, 0.56, bz + 0.72, 0.86, 0.10, 0.75, c(250, 250, 252))
            hr.rotate(angle=-0.48, axis=V(1, 0, 0))
            cylinder(pos=V(bx - 0.32, 0.72, bz + 0.85), axis=V(0.64, 0, 0), radius=0.10, color=c(55, 145, 215))
        elif facing == "east":
            cube(bx, 0.26, bz, 2.1, 0.16, 0.90, c(65, 48, 38))
            cube(bx + 0.20, 0.38, bz, 1.4, 0.12, 0.86, c(250, 250, 252))
            hr = cube(bx - 0.72, 0.56, bz, 0.75, 0.10, 0.86, c(250, 250, 252))
            hr.rotate(angle=0.48, axis=V(0, 0, 1))
            cylinder(pos=V(bx - 0.85, 0.72, bz - 0.32), axis=V(0, 0, 0.64), radius=0.10, color=c(55, 145, 215))

    for l_idx in range(3):
        lz = -8.5 + l_idx * 2.5
        beach_lounger(-19.6, lz, facing="east")

    beach_lounger(-16.8, 1.8, facing="north")
    beach_lounger(-14.2, 1.8, facing="north")

    for tx, tz in [(-19.8, -7.2), (-15.5, 1.8)]:
        cylinder(pos=V(tx, 0.08, tz), axis=V(0, 0.32, 0), radius=0.26, color=c(250, 248, 245))
        cylinder(pos=V(tx, 0.39, tz), axis=V(0, 0.02, 0), radius=0.28, color=c(215, 175, 110))
        cylinder(pos=V(tx, 0.41, tz), axis=V(0, 0.22, 0), radius=0.08, color=c(255, 145, 55), opacity=0.85)
        cylinder(pos=V(tx, 0.41, tz), axis=V(0.04, 0.28, 0.04), radius=0.016, color=c(240, 50, 70))
        sphere(pos=V(tx + 0.08, 0.62, tz), radius=0.035, color=c(255, 230, 40))

    tbl_x, tbl_z = -18.2, 1.8
    cylinder(pos=V(tbl_x, 0.08, tbl_z), axis=V(0, 0.05, 0), radius=0.55, color=c(35, 34, 38))
    cylinder(pos=V(tbl_x, 0.13, tbl_z), axis=V(0, 0.03, 0), radius=0.46, color=c(215, 175, 110))
    cylinder(pos=V(tbl_x, 0.15, tbl_z), axis=V(0, 0.54, 0), radius=0.18, color=c(215, 175, 110))
    cylinder(pos=V(tbl_x, 0.68, tbl_z), axis=V(0, 0.03, 0), radius=1.06, color=c(215, 175, 110))
    cylinder(pos=V(tbl_x, 0.70, tbl_z), axis=V(0, 0.06, 0), radius=1.02, color=c(252, 250, 248))

    cylinder(pos=V(tbl_x, 0.76, tbl_z), axis=V(0, 0.26, 0), radius=0.18, color=c(235, 238, 245))
    cylinder(pos=V(tbl_x, 0.98, tbl_z), axis=V(0, 0.04, 0), radius=0.19, color=c(225, 228, 235))
    cylinder(pos=V(tbl_x, 0.85, tbl_z), axis=V(0.04, 0.32, 0), radius=0.065, color=c(38, 85, 48))
    cylinder(pos=V(tbl_x + 0.04, 1.15, tbl_z), axis=V(0.02, 0.15, 0), radius=0.03, color=c(235, 195, 95))
    for fx_off in (-0.36, 0.36):
        cylinder(pos=V(tbl_x + fx_off, 0.76, tbl_z + 0.20), axis=V(0, 0.24, 0), radius=0.05,
                 color=c(255, 248, 225), opacity=0.88)
        cylinder(pos=V(tbl_x + fx_off, 0.76, tbl_z + 0.20), axis=V(0, 0.02, 0), radius=0.065,
                 color=c(215, 175, 110))
    cylinder(pos=V(tbl_x, 0.76, tbl_z - 0.35), axis=V(0, 0.06, 0), radius=0.15, color=c(215, 175, 110))
    for s_ang in range(5):
        sa = s_ang * 2 * math.pi / 5.0
        sphere(pos=V(tbl_x + 0.07 * math.cos(sa), 0.84, tbl_z - 0.35 + 0.07 * math.sin(sa)),
               radius=0.05, color=c(225, 42, 60))

    for ch_x, ch_rot in [(tbl_x - 1.35, 1), (tbl_x + 1.35, -1)]:
        for leg_z in (-0.28, 0.28):
            cylinder(pos=V(ch_x, 0.08, tbl_z + leg_z), axis=V(0, 0.44, 0), radius=0.03, color=c(215, 175, 110))
        cylinder(pos=V(ch_x, 0.48, tbl_z), axis=V(0, 0.12, 0), radius=0.42, color=c(250, 248, 245))
        br_x = ch_x - 0.25 * ch_rot
        cube(br_x, 0.80, tbl_z, 0.10, 0.55, 0.78, c(55, 48, 42))

    dx, dz = -18.2, 7.4
    cube(dx, 0.55, dz, 1.6, 1.1, 1.6, c(240, 225, 205))
    build_hipped_roof(dx, 1.1, dz, 1.9, 0.5, 1.9, tiers=3)
    cube(dx, 0.45, dz + 0.81, 0.6, 0.75, 0.04, IRON_BLACK)

    cylinder(pos=V(dx - 1.1, 0.05, dz + 0.8), axis=V(0, 0.10, 0), radius=0.18, color=c(220, 50, 60))
    cylinder(pos=V(dx - 1.1, 0.12, dz + 0.8), axis=V(0, 0.02, 0), radius=0.15, color=c(180, 225, 245))

    DOG_COL = c(225, 155, 65)
    cube(dx + 1.2, 0.38, dz + 0.6, 0.75, 0.40, 0.35, DOG_COL)
    sphere(pos=V(dx + 1.6, 0.62, dz + 0.6), radius=0.22, color=DOG_COL)
    cube(dx + 1.8, 0.58, dz + 0.6, 0.18, 0.14, 0.16, DOG_COL)
    sphere(pos=V(dx + 1.88, 0.62, dz + 0.6), radius=0.05, color=c(20, 20, 20))
    sphere(pos=V(dx + 1.60, 0.70, dz + 0.42), radius=0.09, color=c(195, 125, 45))
    sphere(pos=V(dx + 1.60, 0.70, dz + 0.78), radius=0.09, color=c(195, 125, 45))
    cylinder(pos=V(dx + 1.42, 0.50, dz + 0.6), axis=V(0.08, 0, 0), radius=0.18, color=c(220, 45, 55))
    cylinder(pos=V(dx + 0.82, 0.46, dz + 0.6), axis=V(-0.25, 0.26, 0), radius=0.045, color=DOG_COL)

    front_perimeter_trees = [
        (-21.0, 13.0),
        (-21.0, 9.2),
        (-21.0, 5.4),
    ]
    for tx, tz in front_perimeter_trees:
        cylinder(pos=V(tx, 0, tz), axis=V(0, 2.3, 0), radius=0.24, color=c(95, 62, 38))
        cylinder(pos=V(tx, 1.6, tz), axis=V(-0.5, 0.9, 0.3), radius=0.15, color=c(95, 62, 38))
        cylinder(pos=V(tx, 1.8, tz), axis=V(0.5, 0.8, -0.2), radius=0.14, color=c(95, 62, 38))
        for b_off in [V(0, 2.7, 0), V(-0.7, 2.5, 0.4), V(0.7, 2.6, -0.4),
                      V(0.3, 3.3, 0.3), V(-0.5, 3.1, -0.3), V(0.0, 3.7, 0)]:
            sphere(pos=V(tx, 0, tz) + b_off, radius=random.uniform(1.0, 1.4),
                   color=TREE_LEAF * random.uniform(0.92, 1.12))

    cube(-22.4, 0.85, 0, 0.50, 1.7, 29.0, HEDGE_GREEN)
    cube(-1.5, 0.85, -14.6, 42.0, 1.7, 0.50, HEDGE_GREEN)
    cube(19.6, 0.85, -2.0, 0.60, 1.7, 25.0, HEDGE_GREEN)

    tree_positions = [
        (-12.0, -13.5), (-4.0, -13.5),
        (5.0, -13.5), (14.0, -13.5), (19.0, 7.0)
    ]
    for tx, tz in tree_positions:
        post(tx, 0, 2.5, tz, 0.24, c(90, 58, 36))
        for _ in range(5):
            sphere(pos=V(tx + random.uniform(-0.7, 0.7), 3.2 + random.uniform(0, 1.4),
                         tz + random.uniform(-0.7, 0.7)),
                   radius=random.uniform(1.1, 1.5), color=TREE_LEAF * random.uniform(0.9, 1.1))

    cube(-8.5, 0.05, 9.8, 8.4, 0.08, 5.4, c(226, 222, 215))
    cube(-8.5, 0.06, 9.8, 8.6, 0.03, 5.6, c(185, 175, 165))
    for pj_x in (-11.2, -8.5, -5.8):
        cube(pj_x, 0.07, 9.8, 0.04, 0.02, 5.2, c(165, 155, 145))
    for pj_z in (8.0, 9.8, 11.6):
        cube(-8.5, 0.07, pj_z, 8.2, 0.02, 0.04, c(165, 155, 145))

    ctx, ctz = -8.5, 9.8
    cube(ctx, 0.20, ctz, 2.0, 0.28, 1.2, c(45, 42, 40))
    cube(ctx, 0.40, ctz, 2.4, 0.12, 1.5, c(250, 248, 245))
    cube(ctx, 0.38, ctz, 2.45, 0.03, 1.55, c(215, 175, 110))

    cylinder(pos=V(ctx - 0.45, 0.46, ctz), axis=V(0, 0.38, 0), radius=0.14, color=c(255, 205, 60), opacity=0.82)
    cylinder(pos=V(ctx - 0.45, 0.46, ctz), axis=V(0.06, 0.45, 0), radius=0.02, color=c(240, 60, 80))
    for gx_off, gz_off in [(-0.15, -0.38), (0.25, -0.38), (-0.15, 0.38), (0.25, 0.38)]:
        cylinder(pos=V(ctx + gx_off, 0.46, ctz + gz_off), axis=V(0, 0.18, 0), radius=0.065, color=c(245, 250, 255), opacity=0.8)
        cylinder(pos=V(ctx + gx_off, 0.46, ctz + gz_off), axis=V(0.02, 0.24, 0.02), radius=0.012, color=c(240, 60, 80))
    cylinder(pos=V(ctx + 0.65, 0.46, ctz), axis=V(0, 0.12, 0), radius=0.18, color=c(248, 246, 242))
    sphere(pos=V(ctx + 0.65, 0.54, ctz), radius=0.12, color=c(235, 185, 95))
    cylinder(pos=V(ctx, 0.46, ctz), axis=V(0, 0.10, 0), radius=0.15, color=c(195, 160, 130))
    sphere(pos=V(ctx, 0.60, ctz), radius=0.12, color=c(55, 145, 75))

    def lounge_chair(x, z, facing_angle=0):
        for dx in (-0.38, 0.38):
            for dz in (-0.38, 0.38):
                cube(x + dx, 0.20, z + dz, 0.05, 0.38, 0.05, c(45, 42, 40))
        cube(x, 0.40, z, 0.95, 0.10, 0.95, c(175, 125, 75))
        cube(x, 0.48, z, 0.88, 0.12, 0.88, c(250, 248, 245))
        if facing_angle == 90:
            cube(x - 0.42, 0.80, z, 0.12, 0.60, 0.95, c(175, 125, 75))
            cube(x - 0.38, 0.80, z, 0.08, 0.50, 0.82, c(250, 248, 245))
            cube(x - 0.28, 0.65, z, 0.12, 0.32, 0.42, c(245, 165, 185))
        elif facing_angle == -90:
            cube(x + 0.42, 0.80, z, 0.12, 0.60, 0.95, c(175, 125, 75))
            cube(x + 0.38, 0.80, z, 0.08, 0.50, 0.82, c(250, 248, 245))
            cube(x + 0.28, 0.65, z, 0.12, 0.32, 0.42, c(135, 195, 205))
        elif facing_angle == 180:
            cube(x, 0.80, z + 0.42, 0.95, 0.60, 0.12, c(175, 125, 75))
            cube(x, 0.80, z + 0.38, 0.82, 0.50, 0.08, c(250, 248, 245))
            cube(x, 0.65, z + 0.28, 0.42, 0.32, 0.12, c(245, 165, 185))
        elif facing_angle == 0:
            cube(x, 0.80, z - 0.42, 0.95, 0.60, 0.12, c(175, 125, 75))
            cube(x, 0.80, z - 0.38, 0.82, 0.50, 0.08, c(250, 248, 245))
            cube(x, 0.65, z - 0.28, 0.42, 0.32, 0.12, c(135, 195, 205))

    lounge_chair(ctx - 1.9, ctz - 0.75, facing_angle=90)
    lounge_chair(ctx - 1.9, ctz + 0.75, facing_angle=90)
    lounge_chair(ctx + 1.9, ctz - 0.75, facing_angle=-90)
    lounge_chair(ctx + 1.9, ctz + 0.75, facing_angle=-90)

    cube(ctx, 0.40, ctz + 1.85, 2.2, 0.12, 0.95, c(175, 125, 75))
    cube(ctx, 0.48, ctz + 1.85, 2.1, 0.12, 0.88, c(250, 248, 245))
    cube(ctx, 0.80, ctz + 2.25, 2.2, 0.60, 0.12, c(175, 125, 75))
    cube(ctx, 0.80, ctz + 2.20, 2.0, 0.50, 0.08, c(250, 248, 245))
    cube(ctx - 0.6, 0.65, ctz + 2.10, 0.42, 0.30, 0.12, c(245, 165, 185))
    cube(ctx + 0.6, 0.65, ctz + 2.10, 0.42, 0.30, 0.12, c(135, 195, 205))

    for cpx, cpz in [(-12.3, 7.6), (-4.7, 7.6)]:
        cylinder(pos=V(cpx, 0.06, cpz), axis=V(0, 0.55, 0), radius=0.32, color=WALL_WHITE)
        sphere(pos=V(cpx, 0.85, cpz), radius=0.45, color=c(55, 135, 65))
        for _ in range(4):
            sphere(pos=V(cpx + random.uniform(-0.25, 0.25), 0.95 + random.uniform(0, 0.2),
                         cpz + random.uniform(-0.25, 0.25)), radius=0.12, color=c(245, 135, 175))

    cube(-12.5, 0.22, 13.8, 12.0, 0.32, 1.25, WALL_STUCCO)
    cube(-12.5, 0.39, 13.8, 12.1, 0.05, 1.32, CONCRETE_PAVE)
    cube(-12.5, 0.38, 13.8, 11.8, 0.06, 1.15, SOIL_BED)

    bed_greens = [c(38, 105, 45), c(52, 135, 60), c(32, 85, 36), c(62, 148, 70)]
    for f_idx in range(32):
        fx = -18.1 + f_idx * 0.36
        fz = 13.8 + (0.12 if f_idx % 2 == 0 else -0.10)
        fy = 0.52 + (0.06 if f_idx % 3 == 0 else -0.02)
        sphere(pos=V(fx, fy, fz), radius=0.22 + (f_idx % 3) * 0.03, color=bed_greens[f_idx % 4])

    lav_shades = [c(140, 105, 195), c(110, 130, 220), c(165, 130, 215)]
    for l_idx in range(22):
        lx = -17.9 + l_idx * 0.52
        cylinder(pos=V(lx, 0.55, 13.45), axis=V(0, 0.32, 0), radius=0.018, color=c(55, 120, 50))
        cylinder(pos=V(lx, 0.68, 13.45), axis=V(0, 0.26, 0), radius=0.050, color=lav_shades[l_idx % 3])
        sphere(pos=V(lx, 0.95, 13.45), radius=0.045, color=lav_shades[(l_idx + 1) % 3])

    bloom_palette = [
        c(255, 145, 180),
        c(245, 65, 110),
        c(255, 252, 248),
        c(180, 125, 220),
        c(255, 155, 120),
        c(255, 215, 60),
    ]
    for b_idx in range(28):
        bx = -18.0 + b_idx * 0.41
        bz = 13.82 + (0.14 if b_idx % 2 == 0 else -0.12)
        by = 0.68 + (0.06 if b_idx % 3 == 1 else -0.03)
        b_col = bloom_palette[b_idx % len(bloom_palette)]

        sphere(pos=V(bx, by, bz), radius=0.12, color=b_col)
        for p_dx, p_dy, p_dz in [(-0.07, 0.03, 0.05), (0.07, 0.03, -0.05),
                                 (-0.05, -0.03, -0.06), (0.06, -0.02, 0.06)]:
            sphere(pos=V(bx + p_dx, by + p_dy, bz + p_dz), radius=0.09, color=b_col * 0.95)
        sphere(pos=V(bx, by + 0.04, bz + 0.02), radius=0.036, color=c(255, 215, 45))

    for aly_i in range(16):
        ax = -17.8 + aly_i * 0.72
        sphere(pos=V(ax, 0.44, 14.38), radius=0.055, color=c(255, 255, 255))
        sphere(pos=V(ax + 0.08, 0.38, 14.40), radius=0.048, color=c(250, 248, 242))

    cube(5.0, 0.22, 13.8, 5.2, 0.32, 1.25, WALL_STUCCO)
    cube(5.0, 0.39, 13.8, 5.3, 0.05, 1.32, CONCRETE_PAVE)
    cube(5.0, 0.38, 13.8, 5.0, 0.06, 1.15, SOIL_BED)

    for rf_i in range(15):
        r_fx = 2.6 + rf_i * 0.34
        r_fz = 13.8 + (0.12 if rf_i % 2 == 0 else -0.10)
        r_fy = 0.52 + (0.06 if rf_i % 3 == 0 else -0.02)
        sphere(pos=V(r_fx, r_fy, r_fz), radius=0.22 + (rf_i % 3) * 0.03, color=bed_greens[rf_i % 4])

    for rl_i in range(10):
        rl_x = 2.7 + rl_i * 0.50
        cylinder(pos=V(rl_x, 0.55, 13.45), axis=V(0, 0.32, 0), radius=0.018, color=c(55, 120, 50))
        cylinder(pos=V(rl_x, 0.68, 13.45), axis=V(0, 0.26, 0), radius=0.050, color=lav_shades[rl_i % 3])
        sphere(pos=V(rl_x, 0.95, 13.45), radius=0.045, color=lav_shades[(rl_i + 1) % 3])

    for rb_i in range(12):
        rb_x = 2.7 + rb_i * 0.42
        rb_z = 13.82 + (0.14 if rb_i % 2 == 0 else -0.12)
        rb_y = 0.68 + (0.06 if rb_i % 3 == 1 else -0.03)
        rb_col = bloom_palette[rb_i % len(bloom_palette)]

        sphere(pos=V(rb_x, rb_y, rb_z), radius=0.12, color=rb_col)
        for p_dx, p_dy, p_dz in [(-0.07, 0.03, 0.05), (0.07, 0.03, -0.05),
                                 (-0.05, -0.03, -0.06), (0.06, -0.02, 0.06)]:
            sphere(pos=V(rb_x + p_dx, rb_y + p_dy, rb_z + p_dz), radius=0.09, color=rb_col * 0.95)
        sphere(pos=V(rb_x, rb_y + 0.04, rb_z + 0.02), radius=0.036, color=c(255, 215, 45))

    for ra_i in range(8):
        rax = 2.8 + ra_i * 0.65
        sphere(pos=V(rax, 0.44, 14.38), radius=0.055, color=c(255, 255, 255))
        sphere(pos=V(rax + 0.08, 0.38, 14.40), radius=0.048, color=c(250, 248, 242))

def build_perimeter_fence_and_gate():
    WALL_Y = 0.45
    WALL_H = 0.90
    RAIL_H = 0.95

    def wall_with_railing(x0, z0, x1, z1):
        along_x = abs(x1 - x0) > abs(z1 - z0)
        length = abs(x1 - x0) if along_x else abs(z1 - z0)
        cx = (x0 + x1) / 2.0
        cz = (z0 + z1) / 2.0

        if along_x:
            cube(cx, WALL_Y, cz, length, WALL_H, 0.45, WALL_STUCCO)
            cube(cx, WALL_H + 0.05, cz, length + 0.1, 0.10, 0.55, CONCRETE_PAVE)
            cube(cx, WALL_H + 0.15, cz, length, 0.06, 0.06, IRON_BLACK)
            cube(cx, WALL_H + RAIL_H, cz, length, 0.06, 0.06, IRON_BLACK)
            p_count = int(length / 0.45)
            for p in range(p_count + 1):
                px = x0 + (x1 - x0) * (p / float(p_count))
                cube(px, WALL_H + RAIL_H / 2.0, cz, 0.05, RAIL_H, 0.05, IRON_BLACK)
        else:
            cube(cx, WALL_Y, cz, 0.45, WALL_H, length, WALL_STUCCO)
            cube(cx, WALL_H + 0.05, cz, 0.55, 0.10, length + 0.1, CONCRETE_PAVE)
            cube(cx, WALL_H + 0.15, cz, 0.06, 0.06, length, IRON_BLACK)
            cube(cx, WALL_H + RAIL_H, cz, 0.06, 0.06, length, IRON_BLACK)
            p_count = int(length / 0.45)
            for p in range(p_count + 1):
                pz = z0 + (z1 - z0) * (p / float(p_count))
                cube(cx, WALL_H + RAIL_H / 2.0, pz, 0.05, RAIL_H, 0.05, IRON_BLACK)

    wall_with_railing(-23.5, 15.5, -2.6, 15.5)
    wall_with_railing(2.2, 15.5, 7.8, 15.5)
    wall_with_railing(18.8, 15.5, 20.5, 15.5)
    wall_with_railing(-23.5, -15.5, 20.5, -15.5)
    wall_with_railing(-23.5, -15.5, -23.5, 15.5)
    wall_with_railing(20.5, -15.5, 20.5, 15.5)

    gate_pillars = [
        (-23.5, 15.5), (-2.6, 15.5), (2.2, 15.5),
        (7.8, 15.5), (18.8, 15.5), (20.5, 15.5),
        (-23.5, 7.5), (-23.5, 0.0), (-23.5, -7.5),
        (-23.5, -15.5), (-12.5, -15.5), (-1.5, -15.5), (9.5, -15.5), (20.5, -15.5),
        (20.5, -7.5), (20.5, 0.0), (20.5, 7.5)
    ]
    for px, pz in gate_pillars:
        cube(px, 1.1, pz, 0.65, 2.2, 0.65, WALL_STUCCO)
        cube(px, 2.25, pz, 0.85, 0.15, 0.85, CONCRETE_PAVE)

        cube(px, 2.35, pz, 0.32, 0.05, 0.32, IRON_BLACK)
        cube(px, 2.39, pz, 0.22, 0.03, 0.22, IRON_BLACK)

        g_chamber = cube(px, 2.56, pz, 0.22, 0.30, 0.22, c(220, 225, 230), opacity=0.70, emissive=False)

        b_bulb = sphere(pos=V(px, 2.56, pz), radius=0.08, color=c(180, 170, 150), emissive=False)

        for c_dx in (-0.11, 0.11):
            for c_dz in (-0.11, 0.11):
                cube(px + c_dx, 2.56, pz + c_dz, 0.025, 0.30, 0.025, IRON_BLACK)

        cube(px, 2.73, pz, 0.28, 0.05, 0.28, IRON_BLACK)
        cube(px, 2.78, pz, 0.18, 0.05, 0.18, IRON_BLACK)
        sphere(pos=V(px, 2.83, pz), radius=0.04, color=c(215, 175, 110))

        pillar_lanterns.append((g_chamber, b_bulb))

    global gate_left, gate_right
    gate_left  = []
    gate_right = []

    gate_left.append(cube(-2.4, 1.1, 15.5, 0.10, 2.0, 0.10, IRON_BLACK))
    gate_left.append(cube(-1.3, 0.35, 15.5, 2.2, 0.08, 0.08, IRON_BLACK))
    gate_left.append(cube(-1.3, 1.95, 15.5, 2.2, 0.08, 0.08, IRON_BLACK))
    for k in range(1, 6):
        gate_left.append(cube(-2.4 + k * (2.2 / 6.0), 1.15, 15.5, 0.05, 1.6, 0.05, IRON_BLACK))

    gate_right.append(cube(2.0, 1.1, 15.5, 0.10, 2.0, 0.10, IRON_BLACK))
    gate_right.append(cube(0.9, 0.35, 15.5, 2.2, 0.08, 0.08, IRON_BLACK))
    gate_right.append(cube(0.9, 1.95, 15.5, 2.2, 0.08, 0.08, IRON_BLACK))
    for k in range(1, 6):
        gate_right.append(cube(-0.2 + k * (2.2 / 6.0), 1.15, 15.5, 0.05, 1.6, 0.05, IRON_BLACK))

    global car_gate_left, car_gate_right
    car_gate_left  = []
    car_gate_right = []

    car_gate_left.append(cube(8.05, 1.1, 15.5, 0.12, 2.0, 0.12, IRON_BLACK))
    car_gate_left.append(cube(10.65, 0.35, 15.5, 5.2, 0.08, 0.08, IRON_BLACK))
    car_gate_left.append(cube(10.65, 1.10, 15.5, 5.2, 0.06, 0.06, IRON_BLACK))
    car_gate_left.append(cube(10.65, 1.95, 15.5, 5.2, 0.08, 0.08, IRON_BLACK))
    for k in range(1, 11):
        px = 8.05 + k * (5.2 / 11.0)
        car_gate_left.append(cube(px, 1.15, 15.5, 0.05, 1.6, 0.05, IRON_BLACK))
        car_gate_left.append(cone(pos=V(px, 1.95, 15.5), axis=V(0, 0.18, 0), radius=0.04, color=IRON_BLACK))

    car_gate_right.append(cube(18.55, 1.1, 15.5, 0.12, 2.0, 0.12, IRON_BLACK))
    car_gate_right.append(cube(15.95, 0.35, 15.5, 5.2, 0.08, 0.08, IRON_BLACK))
    car_gate_right.append(cube(15.95, 1.10, 15.5, 5.2, 0.06, 0.06, IRON_BLACK))
    car_gate_right.append(cube(15.95, 1.95, 15.5, 5.2, 0.08, 0.08, IRON_BLACK))
    for k in range(1, 11):
        px = 13.35 + k * (5.2 / 11.0)
        car_gate_right.append(cube(px, 1.15, 15.5, 0.05, 1.6, 0.05, IRON_BLACK))
        car_gate_right.append(cone(pos=V(px, 1.95, 15.5), axis=V(0, 0.18, 0), radius=0.04, color=IRON_BLACK))

def build_sky():
    global sun, moon, sun_parts
    sx, sy, sz = -20.0, 17.0, -12.0
    cam_d = V(0.0 - sx, 12.66 - sy, 20.24 - sz)
    cam_mag = math.sqrt(cam_d.x**2 + cam_d.y**2 + cam_d.z**2)
    cam_n = V(cam_d.x / cam_mag, cam_d.y / cam_mag, cam_d.z / cam_mag)
    r_raw = V(cam_n.z, 0.0, -cam_n.x)
    r_mag = math.sqrt(r_raw.x**2 + r_raw.z**2)
    sun_r = V(r_raw.x / r_mag, 0.0, r_raw.z / r_mag)
    sun_u = V(cam_n.y * sun_r.z, cam_n.z * sun_r.x - cam_n.x * sun_r.z, -cam_n.y * sun_r.x)
    u_mag = math.sqrt(sun_u.x**2 + sun_u.y**2 + sun_u.z**2)
    sun_u = V(sun_u.x / u_mag, sun_u.y / u_mag, sun_u.z / u_mag)

    sun = sphere(pos=V(sx, sy, sz), radius=2.2, color=c(255, 232, 120), emissive=True)
    sun_rim = ring(pos=V(sx, sy, sz), axis=cam_n * 0.1, radius=2.22, thickness=0.18,
                   color=c(255, 203, 80), emissive=True)
    sun_hi = sphere(pos=V(sx, sy, sz) + cam_n * 0.18 - sun_r * 0.35 + sun_u * 0.35,
                    radius=1.45, color=c(255, 247, 175), opacity=0.92, emissive=True)
    sun_parts = [sun, sun_rim, sun_hi]

    for i in range(12):
        ang = i * (2.0 * math.pi / 12.0)
        rdir = math.cos(ang) * sun_r + math.sin(ang) * sun_u
        rpos = V(sx, sy, sz) + rdir * 1.95
        raxis = rdir * 1.55
        sun_parts.append(cone(pos=rpos, axis=raxis, radius=0.52, color=c(255, 204, 75), emissive=True))

    moon = sphere(pos=V(sx, sy, sz), radius=2.2, color=c(240, 242, 255),
                  emissive=True, visible=False)

    for _ in range(150):
        az = random.uniform(0, 2 * math.pi)
        el = random.uniform(math.radians(15), math.radians(82))
        r = 95
        stars.append(sphere(pos=V(r * math.cos(el) * math.cos(az), r * math.sin(el),
                                  r * math.cos(el) * math.sin(az)),
                            radius=random.uniform(0.12, 0.28), color=WALL_WHITE,
                            emissive=True, visible=False))

    cloud_defs = [
        (V(13.5, 17.0, -10.0), 1.15, 1.8, 0.45, 0.009, 0.018, 0.0),
        (V(-4.0, 20.5, -15.0), 0.95, 2.2, 0.40, 0.007, 0.015, 1.8),
        (V(22.0, 19.5, -16.0), 0.85, 1.6, 0.35, 0.010, 0.020, 3.4),
        (V(5.0, 22.0, -20.0), 0.75, 1.4, 0.30, 0.008, 0.016, 4.8),
    ]
    for base_v, s, ax, ay, fx, fy, ph in cloud_defs:
        c_parts = []
        puff_specs = [
            (V(0.2 * s, 1.1 * s, 0), V(3.5 * s, 3.5 * s, 3.2 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(-1.6 * s, 0.65 * s, 0), V(2.9 * s, 2.9 * s, 2.7 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(1.8 * s, 0.55 * s, 0), V(2.8 * s, 2.8 * s, 2.6 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(-2.9 * s, -0.05 * s, 0), V(2.2 * s, 2.2 * s, 2.1 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(2.9 * s, -0.05 * s, 0), V(2.1 * s, 2.1 * s, 2.0 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(0, 0, 0), V(5.6 * s, 1.9 * s, 2.4 * s), WALL_WHITE, V(0.20, 0.24, 0.34)),
            (V(-2.9 * s, -0.32 * s, -0.06), V(2.25 * s, 2.25 * s, 2.0 * s), c(185, 202, 226), V(0.14, 0.17, 0.26)),
            (V(-1.5 * s, -0.38 * s, -0.06), V(2.7 * s, 2.7 * s, 2.2 * s), c(185, 202, 226), V(0.14, 0.17, 0.26)),
            (V(0.6 * s, -0.40 * s, -0.06), V(2.9 * s, 2.9 * s, 2.3 * s), c(185, 202, 226), V(0.14, 0.17, 0.26)),
            (V(2.8 * s, -0.30 * s, -0.06), V(2.2 * s, 2.2 * s, 2.0 * s), c(185, 202, 226), V(0.14, 0.17, 0.26)),
            (V(0, -0.28 * s, -0.06), V(5.8 * s, 1.9 * s, 2.2 * s), c(185, 202, 226), V(0.14, 0.17, 0.26))
        ]
        for off, sz, dc, nc in puff_specs:
            sp = sphere(pos=base_v + off, size=sz, color=dc, emissive=True)
            c_parts.append((sp, off, dc, nc))
        clouds.append({
            "base": base_v,
            "amp_x": ax,
            "amp_y": ay,
            "freq_x": fx,
            "freq_y": fy,
            "phase": ph,
            "parts": c_parts
        })

    bird_specs = [
        (15.0, -6.0, 0.52, 0.0, 0.0, 0.0, 0.045),
        (14.3, -6.8, 0.44, -2.2, -0.7, 0.9, 0.040),
        (14.1, -5.4, 0.44, -1.8, 0.6, 1.7, 0.040),
        (13.6, -6.2, 0.38, -3.8, -0.3, 2.5, 0.035),
    ]
    for by, bz, sp, ox, oy, ph, rad in bird_specs:
        wl = cylinder(pos=V(0, 0, 0), axis=V(-sp * 0.8, sp * 0.5, 0), radius=rad, color=c(45, 48, 55))
        wr = cylinder(pos=V(0, 0, 0), axis=V(sp * 0.8, sp * 0.5, 0), radius=rad, color=c(45, 48, 55))
        birds.append({
            "wl": wl, "wr": wr, "by": by, "bz": bz,
            "span": sp, "ox": ox, "oy": oy, "ph": ph
        })

    for px in (-18.0, -15.5, -13.0):
        cylinder(pos=V(px, 0, -14.2), axis=V(0, 3.2, 0), radius=0.20, color=c(95, 62, 38))
        sphere(pos=V(px, 4.2, -14.2), radius=1.1, color=c(65, 145, 60))
    for rz in (4.0, 7.5, 11.0):
        cylinder(pos=V(19.5, 0, rz), axis=V(0, 3.0, 0), radius=0.18, color=c(95, 62, 38))
        sphere(pos=V(19.5, 3.8, rz), radius=1.0, color=c(65, 145, 60))

build_grounds()
build_mansion()
build_carport_and_vehicles()
build_pool_and_garden()
build_perimeter_fence_and_gate()
build_sky()

night = False
door_open = False
gate_open = False
car_gate_open = False
roof_on = True

def toggle_door(_=None):
    global door_open
    ang = -1.35 if not door_open else 1.35
    door_leaf.rotate(angle=ang, axis=V(0, 1, 0), origin=DOOR_PIVOT)
    door_handle.rotate(angle=ang, axis=V(0, 1, 0), origin=DOOR_PIVOT)
    door_open = not door_open

def toggle_gate(_=None):
    global gate_open
    ang = 1.25 if not gate_open else -1.25
    for part in gate_left:
        part.rotate(angle=ang, axis=V(0, 1, 0), origin=V(-2.4, 0, 15.5))
    for part in gate_right:
        part.rotate(angle=-ang, axis=V(0, 1, 0), origin=V(2.0, 0, 15.5))
    gate_open = not gate_open

def toggle_car_gate(_=None):
    global car_gate_open
    ang = -1.45 if not car_gate_open else 1.45
    for part in car_gate_left:
        part.rotate(angle=ang, axis=V(0, 1, 0), origin=V(8.05, 0, 15.5))
    for part in car_gate_right:
        part.rotate(angle=-ang, axis=V(0, 1, 0), origin=V(18.55, 0, 15.5))
    car_gate_open = not car_gate_open

def toggle_night(_=None):
    global night
    night = not night
    if night:
        scene.background = V(0.04, 0.06, 0.14)
        scene.ambient = V(0.20, 0.22, 0.30)
        SUN_LIGHT.color = V(0.20, 0.24, 0.42)
        for sp in sun_parts:
            sp.visible = False
        moon.visible = True
        for s in stars:
            s.visible = True
        for g, _col in window_glass:
            g.color, g.opacity, g.emissive = AMBER_GLOW, 0.98, True
        for cl in clouds:
            for p, _o, _dc, nc in cl["parts"]:
                p.color, p.emissive = nc, False
        for b in birds:
            b["wl"].visible, b["wr"].visible = False, False
        for cl_light in car_lights:
            cl_light.emissive = True
        for p_glass, p_bulb in pillar_lanterns:
            p_glass.color = c(255, 215, 120)
            p_glass.emissive = True
            p_glass.opacity = 0.95
            p_bulb.color = c(255, 245, 180)
            p_bulb.emissive = True
        for lb in lamp_bulbs:
            lb.color = AMBER_GLOW
            lb.emissive = True
        pool_water.color = WATER_NIGHT
        pool_water.emissive = True
        pool_water.opacity = 0.82
        if "pool_glow_floor" in globals():
            pool_glow_floor.color = c(60, 245, 255)
            pool_glow_floor.emissive = True
        if "pool_underwater_lights" in globals():
            for ul in pool_underwater_lights:
                ul.color = POOL_LED_NIGHT
                ul.emissive = True
        if "pool_night_light" in globals():
            pool_night_light.color = V(0.35, 0.88, 0.98)
    else:
        scene.background = V(0.88, 0.93, 0.98)
        scene.ambient = V(0.60, 0.60, 0.62)
        SUN_LIGHT.color = V(1.0, 0.97, 0.90)
        for sp in sun_parts:
            sp.visible = True
        moon.visible = False
        for s in stars:
            s.visible = False
        for g, col in window_glass:
            g.color, g.opacity, g.emissive = col, 0.88, False
        for cl in clouds:
            for p, _o, dc, _nc in cl["parts"]:
                p.color, p.emissive = dc, True
        for b in birds:
            b["wl"].visible, b["wr"].visible = True, True
        for p_glass, p_bulb in pillar_lanterns:
            p_glass.color = c(220, 225, 230)
            p_glass.emissive = False
            p_glass.opacity = 0.70
            p_bulb.color = c(180, 170, 150)
            p_bulb.emissive = False
        for lb in lamp_bulbs:
            lb.emissive = False
        pool_water.color = WATER_DAY
        pool_water.emissive = False
        pool_water.opacity = 0.92
        if "pool_glow_floor" in globals():
            pool_glow_floor.color = c(75, 195, 230)
            pool_glow_floor.emissive = False
        if "pool_underwater_lights" in globals():
            for ul in pool_underwater_lights:
                ul.color = POOL_LED_DAY
                ul.emissive = False
        if "pool_night_light" in globals():
            pool_night_light.color = V(0, 0, 0)

def set_roof(show):
    global roof_on
    roof_on = show
    for p in roof_objects:
        p.visible = show
    if "roof_btn" in globals():
        roof_btn.text = "Hide Roof" if show else "Show Roof"

def look(forward, centre, view_range):
    scene.forward = forward
    scene.center  = centre
    scene.range   = view_range

def go_reference(_=None):
    look(V(0.0, -0.38, -0.92), V(0.0, 4.3, 0.0), 22.0)

def go_isometric(_=None):
    look(V(0.62, -0.38, -0.68), V(1.0, 3.2, 0.0), 26.0)

def go_front(_=None):
    look(V(0.0, -0.15, -0.99), V(-0.2, 2.5, 3.8), 12.0)

def go_carport(_=None):
    look(V(-0.45, -0.28, -0.85), V(13.5, 1.8, 8.5), 11.0)

def go_pool(_=None):
    look(V(0.78, -0.38, 0.49), V(-16.0, 1.5, -4.5), 15.5)

def go_tambayan(_=None):
    look(V(0.42, -0.35, -0.84), V(-8.5, 1.2, 9.8), 7.5)

def go_terrace(_=None):
    look(V(-0.25, -0.22, -0.94), V(7.0, 4.0, 4.0), 7.0)

def go_left_terrace(_=None):
    look(V(0.25, -0.22, -0.94), V(-7.0, 4.0, 4.0), 7.0)

def go_aerial(_=None):
    look(V(-0.02, -1.0, -0.15), V(0.0, 2.0, 0.0), 28.0)

def key_pressed(evt):
    k = evt.key.lower()
    if k == "l":
        toggle_night()
    elif k == "g":
        toggle_gate()
    elif k == "c":
        toggle_car_gate()
    elif k == "d":
        toggle_door()
    elif k == "1":
        go_reference()
    elif k == "2":
        go_isometric()
    elif k == "3":
        go_front()
    elif k == "4":
        go_carport()
    elif k == "5":
        go_pool()
    elif k == "6":
        go_tambayan()
    elif k == "7":
        go_aerial()
    elif k == "8":
        go_terrace()
    elif k == "9":
        go_left_terrace()

scene.bind("keydown", key_pressed)

scene.caption = "Mouse: drag to orbit  |  Scroll to zoom  |  Keys: [L] Day/Night  [G] Gate\n"

button(text="Exterior", bind=go_reference)
button(text="3D view", bind=go_isometric)
button(text="Pool", bind=go_pool)
button(text="Garden", bind=go_tambayan)
button(text="Carport", bind=go_carport)
button(text="Terrace", bind=go_terrace)
button(text="Top view", bind=go_aerial)
scene.append_to_caption("\n")
button(text="Day / Night", bind=toggle_night)
button(text="Gate", bind=toggle_gate)
button(text="Car gate", bind=toggle_car_gate)

go_reference()

tick = 0
while True:
    rate(60)
    tick += 1
    for cl in clouds:
        ox = cl["amp_x"] * math.sin(tick * cl["freq_x"] + cl["phase"])
        oy = cl["amp_y"] * math.cos(tick * cl["freq_y"] + cl["phase"])
        cur = cl["base"] + V(ox, oy, 0)
        for p, off, _dc, _nc in cl["parts"]:
            p.pos = cur + off
    lead_x = -32.0 + (tick * 0.042) % 64.0
    for b in birds:
        bx = lead_x + b["ox"]
        by = b["by"] + b["oy"] + 0.35 * math.sin(tick * 0.035 + b["ph"])
        bz = b["bz"]
        ang = 0.42 + 0.32 * math.sin(tick * 0.28 + b["ph"])
        bpos = V(bx, by, bz)
        b["wl"].pos, b["wr"].pos = bpos, bpos
        b["wl"].axis = V(-b["span"] * math.cos(ang), b["span"] * math.sin(ang), 0.0)
        b["wr"].axis = V(b["span"] * math.cos(ang), b["span"] * math.sin(ang), 0.0)
    shimmer = 0.03 * math.sin(tick * 0.06)
    if night:
        glow_pulse = 1.0 + 0.05 * math.sin(tick * 0.08)
        pool_water.color = WATER_NIGHT * glow_pulse
        if "pool_glow_floor" in globals():
            pool_glow_floor.color = c(60, 245, 255) * glow_pulse
    else:
        pool_water.color = WATER_DAY * (1.0 + shimmer)
