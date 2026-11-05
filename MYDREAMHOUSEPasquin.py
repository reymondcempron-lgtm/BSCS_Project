import os, sys, subprocess, traceback

try:
    from vpython import *
except Exception:
    print("VPython not ready - installing it now (first run only)...")
    os.environ["AUTOBAHN_USE_NVX"] = "0"
    subprocess.call([sys.executable, "-m", "pip", "install", "vpython", "setuptools<81"])
    try:
        from vpython import *
    except Exception:
        traceback.print_exc()
        input("\nCould not load VPython. Copy the error above, then press Enter...")
        sys.exit(1)
import random
import math

random.seed(7)

import sys, traceback


def _show_error(exc_type, exc, tb):
    print("\n==== ERROR in my_dreamhouse.py ====")
    traceback.print_exception(exc_type, exc, tb)
    input("\nPress Enter to close...")


sys.excepthook = _show_error
print("Building 'my dreamhouse'... your browser will open the scene in a new tab.")
print("Keep this window open while viewing. Press Ctrl+C to stop.")

AUTO_OPEN = False
if AUTO_OPEN:
    import threading, webbrowser, time
    threading.Thread(
        target=lambda: (time.sleep(2.5), webbrowser.open("http://localhost:9000")),
        daemon=True).start()

scene.title = "deandra dream house"
scene.width = 1280
scene.height = 720
scene.background = vector(0.62, 0.66, 0.95)
scene.center = vector(0, 5, 0)
scene.forward = vector(0, -0.04, -1)
scene.range = 11
scene.ambient = vector(0.45, 0.42, 0.5)
scene.lights = []
distant_light(direction=vector(-0.4, -0.5, -1), color=vector(1.0, 0.85, 0.7))
distant_light(direction=vector(0.6, -0.3, -0.5), color=vector(0.45, 0.45, 0.6))

label(pos=vector(0, 14.2, 0), text="deandra dream house", height=26, color=color.white,
      box=False, line=False, opacity=0, font="serif")


def hexc(h):
    return vector(int(h[1:3], 16) / 255, int(h[3:5], 16) / 255, int(h[5:7], 16) / 255)


WHITE = hexc("#f7f3ea")
CREAM = hexc("#efe6d2")
ROOF = hexc("#4b4a55")
GRASS = hexc("#4f9a2e")
WOOD = hexc("#8a5a2b")
GLOW = vector(1.0, 0.82, 0.45)
STONE = hexc("#d9cfb8")

LIGHT_SCALE = 0.15
_local_light = local_light


def local_light(pos, color):
    return _local_light(pos=pos, color=color * LIGHT_SCALE)


def slab(p0, p1, p2, p3, col, up=True):
    n = norm(cross(p1 - p0, p3 - p0))
    if (up and n.y < 0) or (not up and n.z < 0):
        n = -n
    vs = [vertex(pos=p, normal=n, color=col) for p in (p0, p1, p2, p3)]
    quad(v0=vs[0], v1=vs[1], v2=vs[2], v3=vs[3])


def tri(p0, p1, p2, col):
    n = norm(cross(p1 - p0, p2 - p0))
    if n.z < 0:
        n = -n
    tri_ = triangle(v0=vertex(pos=p0, normal=n, color=col),
                    v1=vertex(pos=p1, normal=n, color=col),
                    v2=vertex(pos=p2, normal=n, color=col))


def gable_roof(cx, y0, zf, w, d, h, o=0.6):
    """Front-facing gable: wall triangle + two dark roof slopes + white trim."""
    zfo, zb = zf + o, zf - d - o
    xl, xr = cx - w / 2 - o, cx + w / 2 + o
    slab(vector(xl, y0, zfo), vector(cx, y0 + h, zfo), vector(cx, y0 + h, zb),
         vector(xl, y0, zb), ROOF)
    slab(vector(xr, y0, zfo), vector(cx, y0 + h, zfo), vector(cx, y0 + h, zb),
         vector(xr, y0, zb), ROOF)
    tri(vector(cx - w / 2, y0, zf + 0.03), vector(cx + w / 2, y0, zf + 0.03),
        vector(cx, y0 + h * (1 - 0.0), zf + 0.03), CREAM)
    for sgn in (-1, 1):
        cylinder(pos=vector(cx + sgn * (w / 2 + o), y0, zfo),
                 axis=vector(-sgn * (w / 2 + o), h, 0), radius=0.09, color=WHITE)


def siding(cx, cy, zf, w, h, step=0.45):
    y = cy - h / 2 + step
    while y < cy + h / 2:
        box(pos=vector(cx, y, zf + 0.01), size=vector(w, 0.03, 0.03),
            color=hexc("#cfc7b4"))
        y += step


def window(cx, cy, z, w, h, nx=3, ny=2, glow=True):
    box(pos=vector(cx, cy, z), size=vector(w + 0.3, h + 0.3, 0.1), color=WHITE)
    box(pos=vector(cx, cy, z + 0.04), size=vector(w, h, 0.06),
        color=GLOW if glow else hexc("#9fc4e8"), emissive=glow)
    for i in range(1, nx):
        box(pos=vector(cx - w / 2 + i * w / nx, cy, z + 0.09),
            size=vector(0.07, h, 0.05), color=WHITE)
    for j in range(1, ny):
        box(pos=vector(cx, cy - h / 2 + j * h / ny, z + 0.09),
            size=vector(w, 0.07, 0.05), color=WHITE)


def tree(x, z, trunk_h, trunk_r, canopy_r, cy, n=26, lean=0.0):
    cylinder(pos=vector(x, 0, z), axis=vector(lean, trunk_h, 0), radius=trunk_r,
             color=hexc("#6b4423"))
    cylinder(pos=vector(x - trunk_r * 0.9, 0, z + 0.3), axis=vector(0, 0.6, 0),
             radius=trunk_r * 1.3, color=hexc("#6b4423"))
    for sgn in (-1, 1):
        cylinder(pos=vector(x + lean, trunk_h * 0.7, z),
                 axis=vector(sgn * canopy_r * 0.5, canopy_r * 0.55, 0),
                 radius=trunk_r * 0.35, color=hexc("#6b4423"))
    greens = ["#3f7d20", "#4f9a2e", "#6aab35", "#2f6a1a", "#88b840"]
    for _ in range(n):
        a = random.uniform(0, 2 * pi)
        b = random.uniform(0, pi)
        r = canopy_r * random.uniform(0.2, 1.0)
        p = vector(x + lean + r * sin(b) * cos(a) * 1.1,
                   cy + r * cos(b) * 0.7,
                   z + r * sin(b) * sin(a) * 0.8)
        sphere(pos=p, radius=canopy_r * random.uniform(0.28, 0.42),
               color=hexc(random.choice(greens)))


def flower_bed(cx, cz, w, d, n, palette, hmax=0.9):
    for _ in range(n):
        p = vector(cx + random.uniform(-w / 2, w / 2), random.uniform(0.25, hmax),
                   cz + random.uniform(-d / 2, d / 2))
        sphere(pos=p, radius=random.uniform(0.15, 0.28), color=hexc(random.choice(palette)))
    for _ in range(n // 3):
        p = vector(cx + random.uniform(-w / 2, w / 2), 0.25,
                   cz + random.uniform(-d / 2, d / 2))
        sphere(pos=p, radius=0.4, color=hexc("#3a8a2a"))


def adirondack(x, z):
    box(pos=vector(x, 0.65, z), size=vector(1.0, 0.1, 1.0), color=WHITE)
    b = box(pos=vector(x, 1.25, z - 0.5), size=vector(1.0, 1.4, 0.1), color=WHITE)
    b.rotate(angle=radians(-18), axis=vector(1, 0, 0))
    for sx in (-0.55, 0.55):
        box(pos=vector(x + sx, 0.95, z), size=vector(0.12, 0.08, 1.0), color=WHITE)
        for sz in (-0.4, 0.4):
            box(pos=vector(x + sx * 0.8, 0.45, z + sz), size=vector(0.08, 0.35, 0.08), color=WHITE)


box(pos=vector(0, -0.05, 0), size=vector(80, 0.1, 40), color=GRASS)
box(pos=vector(-35, 0.0, -20), size=vector(30, 0.06, 40), color=hexc("#8fa6d8"))
box(pos=vector(-30, 1.0, -34), size=vector(40, 2, 1), color=hexc("#5b7a66"))
box(pos=vector(25, 1.2, -34), size=vector(45, 2.4, 1), color=hexc("#5b7a66"))
sphere(pos=vector(-24, 3.5, -33), radius=1.1, color=vector(1, 0.9, 0.6), emissive=True)

box(pos=vector(0, 2.2, -5.85), size=vector(14, 4.4, 0.3), color=WHITE)
box(pos=vector(-6.85, 2.2, -3), size=vector(0.3, 4.4, 6), color=WHITE)
box(pos=vector(6.85, 2.2, -3), size=vector(0.3, 4.4, 6), color=WHITE)
box(pos=vector(-3.95, 2.2, -0.15), size=vector(6.1, 4.4, 0.3), color=WHITE)
box(pos=vector(3.95, 2.2, -0.15), size=vector(6.1, 4.4, 0.3), color=WHITE)
box(pos=vector(0, 3.9, -0.15), size=vector(1.8, 1.0, 0.3), color=WHITE)
box(pos=vector(0, 4.35, -3), size=vector(13.7, 0.1, 5.7), color=hexc("#fbf8f0"))
box(pos=vector(0, 0.65, -3), size=vector(13.7, 0.1, 5.7), color=hexc("#b98a58"))

box(pos=vector(-2.5, 5.9, -2.3), size=vector(6, 3.0, 5), color=CREAM)
siding(-2.5, 5.9, 0.2, 6, 3.0)
gable_roof(-2.5, 7.4, 0.2, 6, 5, 3.0)
window(-2.5, 8.0, 0.25, 2.6, 1.6, nx=3, ny=2)

box(pos=vector(3.5, 6.2, -4.5), size=vector(5, 3.6, 6), color=CREAM)
siding(3.5, 6.2, -1.5, 5, 3.6)
gable_roof(3.5, 8.0, -1.5, 5, 6, 2.8)
window(3.5, 9.3, -1.45, 1.3, 1.0, nx=2, ny=2)
window(2.3, 6.4, -1.45, 0.9, 1.6, nx=2, ny=3)
window(5.0, 6.4, -1.45, 0.9, 1.6, nx=2, ny=3)

box(pos=vector(0, 0.35, 2), size=vector(15, 0.7, 4), color=WHITE)
slab(vector(-7.8, 4.6, 0), vector(7.8, 4.6, 0), vector(7.8, 4.0, 4.5),
     vector(-7.8, 4.0, 4.5), ROOF)
box(pos=vector(0, 3.95, 4.5), size=vector(15.6, 0.25, 0.1), color=WHITE)
box(pos=vector(0, 3.9, 2.2), size=vector(15, 0.1, 4.5), color=WHITE)

for x in (-7, -5.2, -2.4, 2.4, 5.2, 7):
    box(pos=vector(x, 2.35, 3.8), size=vector(0.45, 3.3, 0.45), color=WHITE)
    box(pos=vector(x, 0.85, 3.8), size=vector(0.7, 0.3, 0.7), color=WHITE)

for (xa, xb) in ((-7, -2.4), (2.4, 7)):
    mid = (xa + xb) / 2
    box(pos=vector(mid, 1.75, 3.8), size=vector(xb - xa, 0.1, 0.15), color=WHITE)
    box(pos=vector(mid, 0.9, 3.8), size=vector(xb - xa, 0.1, 0.15), color=WHITE)
    x = xa + 0.3
    while x < xb:
        box(pos=vector(x, 1.3, 3.8), size=vector(0.08, 0.9, 0.08), color=WHITE)
        x += 0.3

window(-4.6, 2.4, 0.05, 3.4, 1.9, nx=4, ny=2)
window(4.6, 2.4, 0.05, 3.4, 1.9, nx=4, ny=2)
for sx in (-4.6, 4.6):
    box(pos=vector(sx, 2.4, -0.32), size=vector(3.4, 1.9, 0.02), color=GLOW, emissive=True)
    for k in range(1, 4):
        box(pos=vector(sx - 1.7 + k * 0.85, 2.4, -0.33), size=vector(0.06, 1.9, 0.02), color=WHITE)
    box(pos=vector(sx, 2.4, -0.33), size=vector(3.4, 0.06, 0.02), color=WHITE)
for sx in (-0.97, 0.97):
    box(pos=vector(sx, 2.1, -0.15), size=vector(0.15, 2.8, 0.4), color=WHITE)
box(pos=vector(0.9, 2.05, -1.1), size=vector(0.08, 2.7, 1.6), color=WOOD)
sphere(pos=vector(0.9, 2.0, -1.8), radius=0.07, color=color.yellow)
for sx in (-1.8, 1.8):
    sphere(pos=vector(sx, 2.8, 0.25), radius=0.17, color=GLOW, emissive=True)
local_light(pos=vector(0, 3.6, 2.5), color=vector(0.8, 0.55, 0.25))
local_light(pos=vector(-5, 3.6, 2.5), color=vector(0.6, 0.4, 0.2))
local_light(pos=vector(5, 3.6, 2.5), color=vector(0.6, 0.4, 0.2))

FLOOR_Y = 0.7
WOODD = hexc("#6b4a2b")
SAGE = hexc("#87ceeb")
QUARTZ = hexc("#f2f0ea")
CABINET = hexc("#f6f5f1")
STEEL = hexc("#cfd4d8")
DARK = hexc("#2b2b2f")
TERRA = hexc("#c9784f")


def fbox(x, y, z, w, h, d, col, glow=False):
    return box(pos=vector(x, FLOOR_Y + y, z), size=vector(w, h, d), color=col, emissive=glow)


def fcyl(x, y, z, r, h, col, glow=False):
    return cylinder(pos=vector(x, FLOOR_Y + y, z), axis=vector(0, h, 0), radius=r,
                    color=col, emissive=glow)


def fsph(x, y, z, r, col, glow=False):
    return sphere(pos=vector(x, FLOOR_Y + y, z), radius=r, color=col, emissive=glow)


fbox(0, 1.8, -5.69, 13.4, 3.6, 0.02, SAGE)
fbox(-6.69, 1.8, -3, 0.02, 3.6, 5.4, SAGE)
fbox(6.69, 1.8, -3, 0.02, 3.6, 5.4, SAGE)
fbox(-3.875, 1.8, -0.31, 5.65, 3.6, 0.02, SAGE)
fbox(3.875, 1.8, -0.31, 5.65, 3.6, 0.02, SAGE)
fbox(0, 3.2, -0.31, 2.1, 1.0, 0.02, SAGE)
fbox(0, 0.08, -5.67, 13.4, 0.16, 0.04, WHITE)
fbox(-6.67, 0.08, -3, 0.04, 0.16, 5.4, WHITE)
fbox(6.67, 0.08, -3, 0.04, 0.16, 5.4, WHITE)

PX = -2.7
fbox(PX, 1.8, -4.35, 0.15, 3.6, 2.7, SAGE)
fbox(PX, 1.8, -1.05, 0.15, 3.6, 1.5, SAGE)
fbox(PX, 3.2, -2.4, 0.15, 1.0, 1.2, SAGE)
for sz in (-3.0, -1.8):
    fbox(PX, 1.35, sz, 0.2, 2.7, 0.08, WHITE)
fbox(PX, 2.72, -2.4, 0.2, 0.08, 1.28, WHITE)

fbox(-4.6, 0.02, -2.2, 2.6, 0.03, 1.4, hexc("#e9dcc3"))
fbox(-4.9, 0.25, -4.35, 2.0, 0.5, 2.7, WOODD)
fbox(-4.9, 0.62, -4.3, 1.9, 0.24, 2.55, hexc("#f4f1ea"))
fbox(-4.9, 0.76, -3.7, 1.95, 0.1, 1.7, hexc("#d9a5a0"))
fbox(-5.4, 0.82, -5.25, 0.7, 0.14, 0.4, WHITE)
fbox(-4.4, 0.82, -5.25, 0.7, 0.14, 0.4, WHITE)
fbox(-4.9, 0.8, -5.66, 2.2, 1.6, 0.08, WOODD)
for nx in (-6.3, -3.5):
    fbox(nx, 0.3, -5.4, 0.5, 0.6, 0.5, WOODD)
    fcyl(nx, 0.6, -5.4, 0.05, 0.25, WHITE)
    fcyl(nx, 0.82, -5.4, 0.13, 0.2, GLOW, True)
fbox(-6.35, 1.25, -1.3, 0.7, 2.5, 1.4, hexc("#e8e2d4"))
fbox(-5.995, 1.25, -1.3, 0.01, 2.5, 0.02, color.gray(0.6))
for hz in (-1.4, -1.2):
    fbox(-5.97, 1.2, hz, 0.04, 0.3, 0.04, color.gray(0.4))
fbox(-4.9, 2.6, -5.67, 1.5, 0.9, 0.04, WHITE)
fbox(-4.9, 2.6, -5.65, 1.3, 0.7, 0.03, hexc("#e9a47c"))
fbox(-4.9, 2.4, -5.64, 1.3, 0.25, 0.03, hexc("#8fb8e8"))
fsph(-4.9, 3.55, -3.0, 0.18, GLOW, True)
local_light(pos=vector(-4.7, 3.9, -3.0), color=vector(0.6, 0.5, 0.35))

fbox(0, 0.02, -1.0, 1.4, 0.03, 0.9, hexc("#6d2b2b"))
fbox(-0.2, 0.02, -3.8, 3.4, 0.03, 2.2, TERRA)
fbox(-0.2, 0.03, -3.8, 3.0, 0.03, 1.8, hexc("#e8d5b8"))
SOF = hexc("#d9cbb0")
fbox(-0.4, 0.3, -5.2, 2.4, 0.5, 0.9, SOF)
fbox(-0.4, 0.95, -5.5, 2.4, 0.8, 0.25, SOF)
fbox(-1.55, 0.55, -5.2, 0.25, 0.8, 0.9, SOF)
fbox(0.75, 0.55, -5.2, 0.25, 0.8, 0.9, SOF)
fbox(-0.9, 0.62, -5.1, 0.8, 0.14, 0.7, hexc("#b9c9a6"))
fbox(0.1, 0.62, -5.1, 0.8, 0.14, 0.7, hexc("#b9c9a6"))
fbox(-1.15, 0.9, -5.3, 0.4, 0.4, 0.12, TERRA)
fbox(0.4, 0.9, -5.3, 0.4, 0.4, 0.12, hexc("#6f8f9f"))
fbox(-0.4, 0.4, -3.9, 1.2, 0.08, 0.6, WOODD)
for lx in (-0.9, 0.1):
    for lz in (-4.1, -3.7):
        fbox(lx, 0.18, lz, 0.06, 0.36, 0.06, WOODD)
fbox(-0.6, 0.47, -3.9, 0.3, 0.06, 0.2, hexc("#2e86c1"))
fcyl(-0.1, 0.44, -3.9, 0.07, 0.2, WHITE)
fsph(-0.1, 0.72, -3.9, 0.1, hexc("#ef6fa5"))
ARM = hexc("#b9a88a")
fbox(-1.95, 0.28, -3.7, 0.8, 0.4, 0.8, ARM)
fbox(-2.3, 0.75, -3.7, 0.15, 0.9, 0.8, ARM)
fbox(-1.95, 0.55, -4.05, 0.8, 0.12, 0.1, ARM)
fbox(-1.95, 0.55, -3.35, 0.8, 0.12, 0.1, ARM)
fbox(1.65, 1.2, -5.5, 1.0, 2.4, 0.4, WOODD)
book_cols = ["#c0392b", "#2e86c1", "#27ae60", "#f1c40f", "#8e44ad", "#e67e22"]
for row in range(3):
    for i in range(4):
        fbox(1.65 - 0.36 + i * 0.24, 0.45 + row * 0.75, -5.45, 0.18, 0.55, 0.28,
             hexc(book_cols[(i + row) % 6]))
fcyl(-2.3, 0, -5.3, 0.03, 1.6, DARK)
fcyl(-2.3, 1.55, -5.3, 0.2, 0.3, GLOW, True)
fcyl(-2.2, 0, -0.8, 0.25, 0.5, WHITE)
fsph(-2.2, 0.9, -0.8, 0.4, hexc("#3a8a2a"))
fbox(-0.4, 2.5, -5.67, 1.6, 1.0, 0.04, WHITE)
fbox(-0.4, 2.5, -5.65, 1.4, 0.8, 0.03, hexc("#4f9a2e"))
fbox(-0.4, 2.65, -5.64, 1.4, 0.4, 0.03, hexc("#8fb8e8"))
fsph(-0.2, 3.55, -3.5, 0.2, GLOW, True)
local_light(pos=vector(-0.2, 3.9, -3.5), color=vector(0.65, 0.5, 0.3))
local_light(pos=vector(-2.3, 2.6, -5.0), color=vector(0.4, 0.3, 0.2))

fbox(4.55, 0.005, -3, 4.3, 0.01, 5.4, hexc("#e9e7e2"))
for tx in range(0, 5):
    fbox(2.4 + tx * 1.075, 0.011, -3, 0.015, 0.002, 5.4, hexc("#d4d1ca"))
fbox(4.2, 0.45, -5.325, 3.4, 0.9, 0.75, CABINET)
fbox(4.2, 0.93, -5.3, 3.5, 0.04, 0.85, QUARTZ)
for cx in (2.9, 3.6, 4.3, 5.0, 5.7):
    fbox(cx - 0.35, 0.45, -4.945, 0.015, 0.8, 0.01, hexc("#dcdad4"))
    fbox(cx, 0.75, -4.935, 0.2, 0.025, 0.02, color.gray(0.45))
fbox(4.2, 1.95, -5.69, 3.5, 0.55, 0.02, hexc("#f4f4f0"))
for k in range(0, 12):
    fbox(2.5 + k * 0.3, 1.95, -5.68, 0.01, 0.55, 0.01, hexc("#e0ded8"))
fbox(4.2, 1.95, -5.68, 3.5, 0.01, 0.01, hexc("#e0ded8"))
fbox(3.4, 0.96, -5.3, 0.8, 0.01, 0.45, STEEL)
fcyl(3.4, 0.95, -5.55, 0.025, 0.35, STEEL)
cylinder(pos=vector(3.4, FLOOR_Y + 1.3, -5.55), axis=vector(0, 0, 0.2), radius=0.025, color=STEEL)
fbox(5.0, 0.96, -5.3, 0.8, 0.015, 0.6, DARK)
for bx in (4.8, 5.2):
    for bz in (-5.15, -5.45):
        fcyl(bx, 0.97, bz, 0.12, 0.01, color.gray(0.15))
fbox(5.0, 3.0, -5.45, 0.9, 0.3, 0.5, STEEL)
fbox(5.0, 3.45, -5.55, 0.3, 0.6, 0.25, STEEL)
fbox(3.5, 2.65, -5.5, 2.0, 0.8, 0.4, CABINET)
fbox(3.5, 2.65, -5.295, 0.015, 0.8, 0.01, hexc("#dcdad4"))
for hx in (3.2, 3.8):
    fbox(hx, 2.4, -5.28, 0.025, 0.2, 0.02, color.gray(0.45))
fbox(6.25, 0.95, -5.3, 0.85, 1.9, 0.8, STEEL)
fbox(6.25, 1.25, -4.895, 0.8, 0.01, 0.01, color.gray(0.55))
fbox(6.0, 1.5, -4.88, 0.03, 0.5, 0.03, color.gray(0.4))
fbox(6.0, 0.6, -4.88, 0.03, 0.4, 0.03, color.gray(0.4))
fbox(4.3, 0.45, -3.6, 2.0, 0.9, 0.9, CABINET)
fbox(4.3, 0.93, -3.6, 2.3, 0.05, 1.1, QUARTZ)
for sx in (3.6, 4.3, 5.0):
    fcyl(sx, 0.0, -2.85, 0.025, 0.62, color.gray(0.35))
    fcyl(sx, 0.62, -2.85, 0.19, 0.05, hexc("#b9a88a"))
fcyl(3.7, 0.955, -3.6, 0.17, 0.06, WHITE)
for fx, fz, fc in ((3.65, -3.58, "#e74c3c"), (3.75, -3.62, "#f1c40f"), (3.7, -3.55, "#27ae60")):
    fsph(fx, 1.05, fz, 0.06, hexc(fc))
for px in (3.9, 4.7):
    cylinder(pos=vector(px, FLOOR_Y + 3.7, -3.6), axis=vector(0, -0.65, 0), radius=0.01, color=DARK)
    fsph(px, 3.0, -3.6, 0.16, GLOW, True)
fcyl(5.7, 0, -1.5, 0.45, 0.78, color.gray(0.9))
fcyl(5.7, 0.78, -1.5, 0.5, 0.04, WHITE)
fcyl(5.7, 0.82, -1.5, 0.04, 0.18, WHITE)
fsph(5.7, 1.08, -1.5, 0.09, hexc("#ef6fa5"))
for cx, cz in ((4.95, -1.5), (6.35, -1.5)):
    fbox(cx, 0.45, cz, 0.45, 0.06, 0.45, hexc("#d8c9a8"))
    fbox(cx + (-0.2 if cx < 5.7 else 0.2), 0.8, cz, 0.06, 0.7, 0.45, hexc("#d8c9a8"))
    for dx in (-0.18, 0.18):
        for dz in (-0.18, 0.18):
            fbox(cx + dx, 0.22, cz + dz, 0.05, 0.45, 0.05, WOODD)
local_light(pos=vector(4.3, 3.9, -3.0), color=vector(0.75, 0.65, 0.45))
local_light(pos=vector(4.5, 3.9, -1.0), color=vector(0.5, 0.45, 0.35))

box(pos=vector(0, 0.15, 4.6), size=vector(4.4, 0.3, 1.2), color=STONE)
box(pos=vector(0, 0.45, 4.3), size=vector(4.0, 0.3, 0.6), color=STONE)

for sx in (-2.2, 2.2):
    cylinder(pos=vector(sx, 0.7, 3.2), axis=vector(0, 0.7, 0), radius=0.5, color=WHITE)
    sphere(pos=vector(sx, 1.65, 3.2), radius=0.55, color=hexc("#3a8a2a"))
for sx in (-5.2, 5.2):
    cylinder(pos=vector(sx, 3.0, 4.2), axis=vector(0, 0.9, 0), radius=0.02, color=color.gray(0.3))
    sphere(pos=vector(sx, 2.8, 4.2), radius=0.5, color=hexc("#ee6fa0"))
    sphere(pos=vector(sx + 0.15, 3.0, 4.2), radius=0.3, color=hexc("#f7a8c8"))

z = 5.3
while z < 9.2:
    box(pos=vector(0, 0.03, z), size=vector(2.6, 0.06, 0.9), color=STONE)
    z += 1.0

pink = ["#ef6fa5", "#f7a8c8", "#e9568f"]
mixed = ["#ef6fa5", "#f7a8c8", "#ff9b3d", "#ffd23d", "#e9568f"]

x = -23.0
while x < 23.1:
    if abs(x) > 2.7:
        box(pos=vector(x, 0.75, 9), size=vector(0.22, 1.5, 0.08), color=WHITE)
    x += 0.45
for (xa, xb) in ((-23, -3.5), (3.5, 23)):
    for yy in (0.4, 1.1):
        box(pos=vector((xa + xb) / 2, yy, 8.95), size=vector(xb - xa, 0.1, 0.06), color=WHITE)

for side in (-1, 1):
    xx = 0.2
    while xx < 2.5:
        hh = 1.3 + 0.55 * (1 - (xx / 2.5) ** 2)
        box(pos=vector(side * xx, hh / 2, 9.1), size=vector(0.2, hh, 0.07), color=WHITE)
        xx += 0.4
    box(pos=vector(side * 1.3, 0.45, 9.05), size=vector(2.6, 0.1, 0.06), color=WHITE)
    box(pos=vector(side * 1.3, 1.15, 9.05), size=vector(2.6, 0.1, 0.06), color=WHITE)

for sx in (-3.1, 3.1):
    box(pos=vector(sx, 0.95, 9), size=vector(1.0, 1.9, 1.0), color=hexc("#d8c9a8"))
    box(pos=vector(sx, 2.0, 9), size=vector(1.25, 0.22, 1.25), color=hexc("#efe3c8"))
    box(pos=vector(sx, 2.25, 9), size=vector(0.5, 0.3, 0.5), color=color.gray(0.2))
    sphere(pos=vector(sx, 2.75, 9), radius=0.32, color=GLOW, emissive=True)
    local_light(pos=vector(sx, 2.75, 9.3), color=vector(0.7, 0.5, 0.2))

for sx in (-23, 23):
    zz = 8.5
    while zz > -8:
        box(pos=vector(sx, 0.75, zz), size=vector(0.08, 1.5, 0.22), color=WHITE)
        zz -= 0.45

flower_bed(-5.5, 5.4, 4.0, 1.4, 45, pink)
flower_bed(-2.0, 5.6, 2.0, 1.2, 25, pink)
flower_bed(2.0, 5.6, 2.0, 1.2, 25, pink)
flower_bed(5.8, 5.4, 4.0, 1.4, 45, ["#ff9b3d", "#ffd23d", "#ef6fa5", "#ff7a3d"])
flower_bed(-18, 6.5, 8, 1.4, 50, mixed)
flower_bed(18, 4.5, 8, 2.0, 55, mixed)
flower_bed(15, -2.5, 5, 2.5, 40, mixed, hmax=1.5)

cylinder(pos=vector(-12, 0.0, 6.5), axis=vector(0, 0.05, 0), radius=3.0, color=hexc("#2e86c1"))
for i in range(16):
    a = i * 2 * pi / 16
    sphere(pos=vector(-12 + 3.1 * cos(a), 0.3, 6.5 + 3.1 * sin(a) * 0.9),
           radius=random.uniform(0.35, 0.6), color=hexc(random.choice(["#8c8c8c", "#a3a3a3", "#7a7a7a"])))
for (kx, kz) in ((-12.8, 6.4), (-11.0, 7.0)):
    ellipsoid(pos=vector(kx, 0.12, kz), size=vector(0.7, 0.14, 0.28), color=hexc("#ff7a1a"))

box(pos=vector(13, 0.15, 5), size=vector(7.5, 0.3, 5), color=hexc("#8a5a2b"))
adirondack(11.2, 5.2)
adirondack(14.6, 5.2)
cylinder(pos=vector(12.9, 0.3, 5.2), axis=vector(0, 0.8, 0), radius=0.4, color=WHITE)
sphere(pos=vector(12.9, 1.25, 5.2), radius=0.25, color=hexc("#ee6fa0"))

tree(-15, 2, 8.5, 1.1, 7.5, 13.0, n=34, lean=1.0)
tree(17, -1, 5.5, 0.6, 4.5, 9.5, n=22, lean=-0.4)
tree(-7, -8, 3.5, 0.35, 3.0, 6.5, n=14)
tree(-20, -3, 2.5, 0.25, 2.2, 4.6, n=10)

scene.caption = ("<b>Controls:</b> press <b>V</b> (or Enter) to walk around / return to orbit view, "
                 "<b>I</b> to jump inside.<br>"
                 "<b>Walk mode:</b> W/S = forward/back, A/D = sidestep, Left/Right arrows = turn, "
                 "Up/Down arrows = look.<br>"
                 "<b>Orbit mode:</b> right-drag to rotate, scroll to zoom.<br>")

EYE = 2.4
walk = {"on": False, "x": 0.0, "z": 6.5, "yaw": 0.0, "pitch": 0.0}
orbit = {}


def can_walk(x, z):
    if abs(x) > 20 or z < -8 or z > 14:
        return False
    if -7.0 < x < 7.0 and -6.05 < z < 0.0:
        if abs(x + 2.7) < 0.25 and not (-3.0 < z < -1.8):
            return False
        return (abs(x) < 6.6 and -5.6 < z < -0.35) or (abs(x) < 0.85 and z >= -0.35)
    if 3.5 < z < 4.1 and 2.2 < abs(x) < 7.2:
        return False
    if z > 8.6 and abs(x) > 2.4:
        return False
    return True


def update_cam():
    yaw, pitch = walk["yaw"], walk["pitch"]
    d = vector(sin(yaw) * cos(pitch), sin(pitch), -cos(yaw) * cos(pitch))
    scene.camera.pos = vector(walk["x"], EYE, walk["z"])
    scene.camera.axis = d * 3


def toggle_walk():
    if not walk["on"]:
        orbit["pos"] = vector(scene.camera.pos)
        orbit["axis"] = vector(scene.camera.axis)
        scene.userspin = scene.userzoom = scene.userpan = False
        walk.update(on=True, x=0.0, z=6.5, yaw=0.0, pitch=0.0)
        update_cam()
    else:
        scene.userspin = scene.userzoom = scene.userpan = True
        scene.camera.pos = orbit["pos"]
        scene.camera.axis = orbit["axis"]
        walk["on"] = False


def on_key(evt):
    k = evt.key
    if k in ("v", "V", "enter", "\n"):
        toggle_walk()
        return
    if k in ("i", "I"):
        if not walk["on"]:
            toggle_walk()
        walk.update(x=0.0, z=-1.5, yaw=0.0, pitch=0.0)
        update_cam()
        return
    if not walk["on"]:
        return
    step, turn = 0.25, 0.08
    yaw = walk["yaw"]
    fx, fz = sin(yaw), -cos(yaw)
    rx, rz = cos(yaw), sin(yaw)
    nx, nz = walk["x"], walk["z"]
    if k in ("w", "W"):
        nx += fx * step; nz += fz * step
    elif k in ("s", "S"):
        nx -= fx * step; nz -= fz * step
    elif k in ("a", "A"):
        nx -= rx * step; nz -= rz * step
    elif k in ("d", "D"):
        nx += rx * step; nz += rz * step
    elif k == "left":
        walk["yaw"] -= turn
    elif k == "right":
        walk["yaw"] += turn
    elif k == "up":
        walk["pitch"] = min(0.6, walk["pitch"] + 0.05)
    elif k == "down":
        walk["pitch"] = max(-0.6, walk["pitch"] - 0.05)
    if can_walk(nx, nz):
        walk["x"], walk["z"] = nx, nz
    elif can_walk(nx, walk["z"]):
        walk["x"] = nx
    elif can_walk(walk["x"], nz):
        walk["z"] = nz
    update_cam()


scene.bind("keydown", on_key)

while True:
    rate(30)
