from vpython import *

scene = canvas(title="Cerio", width=1200, height=720, background=vec(0.55, 0.72, 0.88))
scene.center = vec(0, 4, 0)
scene.range = 19
scene.forward = vec(0.35, -0.28, -1)
scene.up = vec(0, 1, 0)
scene.autoscale = False
scene.ambient = color.gray(0.55)
scene.lights = []
sun = distant_light(direction=vec(-0.5, -0.8, -0.4), color=color.gray(0.8))
fill = distant_light(direction=vec(0.5, -0.3, 0.5), color=color.gray(0.35))

WHITE = vec(0.91, 0.91, 0.88)
CONCRETE = vec(0.48, 0.49, 0.48)
DARK = vec(0.10, 0.12, 0.15)
BLACK = vec(0.035, 0.045, 0.055)
WOOD = vec(0.48, 0.29, 0.15)
LIGHTWOOD = vec(0.69, 0.49, 0.29)
GLASS = vec(0.48, 0.72, 0.82)
FLOOR = vec(0.73, 0.69, 0.61)
GRASS = vec(0.20, 0.43, 0.19)
LEAF = vec(0.12, 0.38, 0.16)
WARM = vec(1.0, 0.78, 0.42)

lights = []
day_objects = []
night_mode = False

def block(x, y, z, sx, sy, sz, col, opacity=1):
    return box(pos=vec(x, y, z), size=vec(sx, sy, sz), color=col, opacity=opacity)

def lamp(x, y, z, sx=0.35, sz=0.35):
    obj = block(x, y, z, sx, 0.07, sz, WARM)
    lights.append(obj)
    return obj

def glass_panel(x, y, z, sx, sy, sz, opacity=0.28):
    return block(x, y, z, sx, sy, sz, GLASS, opacity)

def tree(x, z, h=5):
    cylinder(pos=vec(x, 0, z), axis=vec(0, h * 0.55, 0), radius=0.18, color=WOOD)
    for i in range(7):
        a = i * 2 * pi / 7
        dx = cos(a)
        dz = sin(a)
        ellipsoid(pos=vec(x + dx * 0.8, h * 0.7, z + dz * 0.8), axis=vec(1.2, 0.8, 1.2), length=1.4, height=1.3, width=1.3, color=LEAF)
    sphere(pos=vec(x, h * 0.85, z), radius=0.9, color=LEAF)

def plant(x, z, scale=1):
    cylinder(pos=vec(x, 0, z), axis=vec(0, 0.35 * scale, 0), radius=0.25 * scale, color=DARK)
    for i in range(6):
        a = i * pi / 3
        ellipsoid(pos=vec(x + cos(a) * 0.25 * scale, 0.65 * scale, z + sin(a) * 0.25 * scale), axis=vec(cos(a), 1, sin(a)), length=0.8 * scale, height=0.7 * scale, width=0.25 * scale, color=LEAF)

block(0, -0.35, 0, 40, 0.5, 40, GRASS)
block(0, -0.08, 13, 40, 0.12, 12, vec(0.22, 0.23, 0.25))
block(0, 0.02, 7, 40, 0.08, 1.2, vec(0.72, 0.72, 0.69))
block(0, 0.01, 6.2, 40, 0.06, 0.12, WHITE)

block(6, 0.02, 4, 7, 0.08, 13, vec(0.67, 0.67, 0.65))
block(6, 0.07, 4, 0.06, 0.02, 13, CONCRETE)
block(-2, 0.03, 7, 5, 0.08, 5, LIGHTWOOD)
block(-2, 0.08, 4.5, 1.5, 0.02, 5, CONCRETE)

block(0, 0.25, 0, 17, 0.5, 12, CONCRETE)
block(0, 2.5, -5.5, 17, 5, 0.3, WHITE)
block(-8.35, 2.5, 0, 0.3, 5, 11, WHITE)
block(8.35, 2.5, 0, 0.3, 5, 11, WHITE)
block(0, 2.5, 5.5, 17, 5, 0.3, WHITE)

block(0, 5.15, 0, 17, 0.3, 12, DARK)
block(0, 7.7, -5.5, 17, 5, 0.3, WHITE)
block(-8.35, 7.7, 0, 0.3, 5, 11, WHITE)
block(8.35, 7.7, 0, 0.3, 5, 11, WHITE)
block(0, 7.7, 5.5, 17, 5, 0.3, WHITE)

block(-2.5, 10.35, -0.5, 12, 0.3, 11, DARK)
block(4.5, 10.5, -0.5, 7, 0.3, 11, DARK)
block(-2.5, 10.55, -0.5, 11.5, 0.12, 10.5, WHITE)

block(-2.5, 2.7, 5.32, 11.5, 4.2, 0.08, GLASS, 0.22)
block(4.2, 2.7, 5.32, 4.3, 4.2, 0.08, GLASS, 0.22)
block(-2.5, 7.9, 5.32, 11.5, 4.1, 0.08, GLASS, 0.22)
block(4.2, 7.9, 5.32, 4.3, 4.1, 0.08, GLASS, 0.22)

for x in [-7.5, -4.5, -1.5, 1.5, 4.5, 7.5]:
    block(x, 2.7, 5.25, 0.09, 4.3, 0.12, BLACK)
    block(x, 7.8, 5.25, 0.09, 4.2, 0.12, BLACK)

block(-5.5, 5.1, 0, 5.5, 0.2, 12, WOOD)
block(5.5, 5.1, 0, 5.5, 0.2, 12, WOOD)

block(-5.3, 5.1, 5.9, 5.8, 0.25, 1.0, DARK)
block(-5.3, 5.1, 7.5, 5.8, 0.25, 1.0, DARK)
block(-5.3, 5.8, 6.7, 5.8, 1.2, 0.08, GLASS, 0.25)

block(5.6, 5.25, 1.2, 5.1, 0.25, 1.0, WOOD)
block(5.6, 5.55, 1.2, 5.1, 0.08, 1.0, GLASS, 0.25)
for x in [3.1, 5.6, 8.1]:
    block(x, 6.2, 1.2, 0.06, 1.8, 0.06, DARK)

block(-5.8, 2.8, 0, 4.0, 0.08, 3.5, FLOOR)
block(-1.0, 2.8, 0, 4.8, 0.08, 3.5, FLOOR)
block(5.5, 2.8, 0, 5.0, 0.08, 3.5, FLOOR)

block(-5.5, 0.85, 0, 3.8, 1.0, 1.1, vec(0.35, 0.36, 0.39))
block(-5.5, 1.45, -0.45, 3.8, 0.3, 0.35, vec(0.35, 0.36, 0.39))
block(-5.5, 1.45, 0.45, 3.8, 0.3, 0.35, vec(0.35, 0.36, 0.39))
block(-5.5, 1.45, 0, 0.35, 0.3, 1.1, vec(0.35, 0.36, 0.39))
block(-3.3, 1.1, -2.1, 1.7, 0.15, 1.0, LIGHTWOOD)
block(-3.3, 0.55, -2.1, 0.12, 1.1, 0.12, DARK)
block(-3.3, 1.7, -2.1, 0.12, 1.1, 0.12, DARK)
block(-5.5, 2.8, -5.2, 4.5, 0.1, 0.2, DARK)
block(-5.5, 3.8, -5.05, 2.0, 1.8, 0.12, BLACK)

block(0, 0.8, -3.7, 2.8, 0.9, 1.4, WOOD)
block(0, 1.28, -3.7, 1.2, 0.08, 0.8, WHITE)
for x in [-0.8, 0, 0.8]:
    cylinder(pos=vec(x, 0.3, -2.5), axis=vec(0, 0.65, 0), radius=0.045, color=DARK)
    block(x, 1.0, -2.5, 0.6, 0.12, 0.6, vec(0.82, 0.81, 0.76))

block(5.4, 0.9, -2.0, 3.3, 1.0, 1.2, WOOD)
block(5.4, 1.5, -2.0, 3.3, 0.15, 1.2, WHITE)
block(5.4, 2.1, -2.0, 3.3, 0.08, 1.2, DARK)
for x in [4.2, 5.4, 6.6]:
    block(x, 0.55, -2.0, 0.12, 1.1, 0.12, DARK)

block(-1.5, 2.8, -5.1, 1.5, 0.12, 0.2, DARK)
block(-1.5, 3.4, -5.0, 1.1, 1.1, 0.12, WOOD)
block(-1.5, 3.0, -4.9, 0.8, 0.35, 0.05, BLACK)

block(-5.5, 7.6, 0, 4.0, 0.08, 3.5, FLOOR)
block(-5.5, 7.6, -2.0, 4.0, 0.08, 3.5, FLOOR)
block(4.5, 7.6, 0, 4.0, 0.08, 3.5, FLOOR)

block(-5.2, 6.0, 0, 2.5, 0.3, 1.5, WOOD)
block(-5.2, 6.25, 0.5, 2.0, 0.18, 0.8, WHITE)
block(-5.2, 6.25, -0.5, 2.0, 0.18, 0.8, WHITE)
block(-5.2, 6.4, 0, 0.12, 0.3, 1.5, DARK)
block(-6.6, 6.3, 0, 0.8, 0.12, 0.8, LIGHTWOOD)
block(-3.8, 6.3, 0, 0.8, 0.12, 0.8, LIGHTWOOD)

block(5.8, 6.0, -2.0, 2.0, 0.3, 1.3, WOOD)
block(5.8, 6.3, -2.0, 1.5, 0.15, 1.0, WHITE)
block(5.8, 6.6, -2.0, 1.5, 0.1, 1.0, vec(0.35, 0.43, 0.52))
block(5.8, 6.3, -3.0, 0.08, 0.6, 0.1, BLACK)

block(-4.0, 5.5, -3.0, 3.0, 0.12, 2.0, WOOD)
block(-4.0, 5.85, -3.0, 2.4, 0.15, 1.7, WHITE)
block(-4.0, 6.0, -3.0, 1.2, 0.08, 1.2, vec(0.35, 0.43, 0.52))

block(0, 0.5, 0, 0.2, 0.1, 0.2, DARK)
block(0, 0.55, 0, 0.12, 0.9, 0.12, DARK)

for x in [-6, -3, 0, 3, 6]:
    lamp(x, 4.9, 0, 0.7, 0.5)
    lamp(x, 9.95, 0, 0.7, 0.5)

block(-2.5, 10.6, -1.5, 8, 0.15, 8, DARK)
block(-2.5, 10.7, -1.5, 7.8, 0.08, 7.8, WHITE)

block(-6.5, 0.4, -5.4, 3.5, 0.25, 1.0, DARK)
block(4.0, 0.4, -5.4, 3.5, 0.25, 1.0, DARK)

for x in [-7.8, 7.8]:
    block(x, 5.3, -4.7, 0.4, 10.2, 0.4, CONCRETE)

block(0, 0.2, 9, 18, 0.4, 0.6, DARK)
block(-9, 0.8, 9, 0.5, 1.6, 0.5, DARK)
block(9, 0.8, 9, 0.5, 1.6, 0.5, DARK)
block(0, 0.8, 9, 18, 1.2, 0.25, DARK)

block(-5.5, 0.8, 9, 5.5, 1.6, 0.12, WOOD)
block(5.5, 0.8, 9, 5.5, 1.6, 0.12, WOOD)

block(6.0, 1.8, 5.5, 5.0, 0.15, 5.0, CONCRETE)
block(6.0, 3.6, 5.5, 5.0, 0.15, 5.0, WHITE)
block(6.0, 5.4, 5.5, 5.0, 0.15, 5.0, CONCRETE)

block(-10, 0.05, 0, 2.5, 0.1, 2.5, LIGHTWOOD)
block(10, 0.05, 0, 2.5, 0.1, 2.5, LIGHTWOOD)

tree(-11, 0, 6)
tree(12, 1, 7)
tree(-12, 7, 5)
tree(12, 8, 5)

for x in [-8, -6, -4, 4, 6, 8]:
    plant(x, 5.8, 1.2)

for x in [-8, -4, 0, 4, 8]:
    cylinder(pos=vec(x, 0, 8), axis=vec(0, 0.65, 0), radius=0.09, color=DARK)
    lamp(x, 0.7, 8, 0.25, 0.25)

def set_day():
    global night_mode
    night_mode = False
    scene.background = vec(0.55, 0.72, 0.88)
    scene.ambient = color.gray(0.55)
    sun.color = color.gray(0.8)
    fill.color = color.gray(0.35)
    for obj in lights:
        obj.color = WARM
        obj.emissive = False

def set_night():
    global night_mode
    night_mode = True
    scene.background = vec(0.025, 0.04, 0.10)
    scene.ambient = color.gray(0.18)
    sun.color = vec(0.12, 0.15, 0.25)
    fill.color = vec(0.05, 0.07, 0.12)
    for obj in lights:
        obj.color = WARM
        obj.emissive = True

def toggle_lighting():
    if night_mode:
        set_day()
    else:
        set_night()

def front_view():
    scene.center = vec(0, 4.5, 0)
    scene.forward = vec(0.02, -0.12, -1)
    scene.range = 19

def side_view():
    scene.center = vec(0, 4.5, 0)
    scene.forward = vec(0.8, -0.3, -0.6)
    scene.range = 20

def top_view():
    scene.center = vec(0, 4, 0)
    scene.forward = vec(0, -1, -0.01)
    scene.up = vec(0, 0, -1)
    scene.range = 21

def overview():
    scene.center = vec(0, 4, 0)
    scene.forward = vec(0.35, -0.28, -1)
    scene.up = vec(0, 1, 0)
    scene.range = 19

scene.append_to_caption("\n\n")
button(text="DAY / NIGHT", bind=lambda _: toggle_lighting())
button(text="FRONT VIEW", bind=lambda _: front_view())
button(text="SIDE VIEW", bind=lambda _: side_view())
button(text="TOP VIEW", bind=lambda _: top_view())
button(text="3D OVERVIEW", bind=lambda _: overview())

overview()