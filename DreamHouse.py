
from vpython import *

scene = canvas(
    title="MY DREAM HOUSE",
    width=1200,
    height=750,
    background=vector(0.65, 0.82, 0.96)
)

scene.center = vector(0, 4, 0)
scene.camera.pos = vector(24, 18, 30)
scene.range = 40
scene.autoscale = False
scene.userspin = True
scene.userzoom = True
scene.userpan = False

ivory = vector(0.93, 0.90, 0.82)
white = vector(0.97, 0.96, 0.91)
roof_color = vector(0.13, 0.16, 0.18)
glass = vector(0.12, 0.38, 0.52)
wood = vector(0.34, 0.19, 0.11)
light_wood = vector(0.58, 0.38, 0.23)
grass = vector(0.22, 0.43, 0.19)
water = vector(0.04, 0.48, 0.78)
gold = vector(0.95, 0.72, 0.30)
stone = vector(0.55, 0.52, 0.46)
black = vector(0.08, 0.09, 0.10)
sage = vector(0.35, 0.49, 0.34)

box(pos=vector(0, -0.35, 0), size=vector(70, 0.5, 70), color=grass)
box(pos=vector(0, 0, 0), size=vector(14, 0.4, 12), color=stone)
box(pos=vector(0, 2.2, 0), size=vector(13, 4, 11), color=ivory)
box(pos=vector(0, 6.2, 0), size=vector(13, 4, 11), color=white)
box(pos=vector(0, 4.25, 0), size=vector(13.2, 0.18, 11.2), color=stone)
box(pos=vector(0, 8.35, 0), size=vector(14, 0.35, 12), color=roof_color)
box(pos=vector(0, 8.15, 5.85), size=vector(14, 0.18, 0.22), color=black)
box(pos=vector(0, 8.15, -5.85), size=vector(14, 0.18, 0.22), color=black)

def make_window(x, y, z, width, height, front=True):
    frame_z = z + (0.10 if front else -0.10)
    glass_z = z + (0.035 if front else -0.035)

    box(
        pos=vector(x, y, glass_z),
        size=vector(width, height, 0.08),
        color=glass,
        opacity=0.82
    )

    for px in [-width / 2, width / 2]:
        box(
            pos=vector(x + px, y, frame_z),
            size=vector(0.10, height + 0.12, 0.10),
            color=white
        )

    for py in [-height / 2, height / 2]:
        box(
            pos=vector(x, y + py, frame_z),
            size=vector(width + 0.12, 0.10, 0.10),
            color=white
        )

    box(
        pos=vector(x, y, frame_z + (0.025 if front else -0.025)),
        size=vector(0.055, height, 0.06),
        color=white
    )

make_window(-4.1, 2.35, 5.56, 2.5, 2.2)
make_window(4.1, 2.35, 5.56, 2.5, 2.2)
make_window(-4.2, 6.25, 5.56, 2.6, 2.3)
make_window(4.2, 6.25, 5.56, 2.6, 2.3)

box(pos=vector(0, 2.0, 5.58), size=vector(1.65, 3.45, 0.16), color=wood)
box(pos=vector(0, 2.0, 5.68), size=vector(1.35, 3.15, 0.045), color=light_wood)
sphere(pos=vector(0.55, 2.0, 5.76), radius=0.075, color=gold)

box(pos=vector(0, 3.95, 6.05), size=vector(3.4, 0.16, 1.25), color=roof_color)
box(pos=vector(0, 3.83, 6.05), size=vector(3.5, 0.07, 1.3), color=light_wood)

for x in [-1.45, 1.45]:
    cylinder(
        pos=vector(x, 0.25, 6.45),
        axis=vector(0, 3.55, 0),
        radius=0.09,
        color=white
    )

for i in range(3):
    box(
        pos=vector(0, 0.20 + i * 0.28, 6.35 + i * 0.42),
        size=vector(3.2, 0.25, 0.85),
        color=white
    )

box(pos=vector(0, 6.25, 5.61), size=vector(1.75, 3.25, 0.13), color=black)
box(pos=vector(-0.42, 6.25, 5.70), size=vector(0.78, 3.02, 0.055), color=glass, opacity=0.78)
box(pos=vector(0.42, 6.25, 5.70), size=vector(0.78, 3.02, 0.055), color=glass, opacity=0.78)
box(pos=vector(0, 6.25, 5.76), size=vector(0.055, 3.02, 0.05), color=white)
box(pos=vector(-0.12, 6.2, 5.79), size=vector(0.035, 0.45, 0.035), color=gold)
box(pos=vector(0.12, 6.2, 5.79), size=vector(0.035, 0.45, 0.035), color=gold)
box(pos=vector(0, 4.55, 6.35), size=vector(5.6, 0.22, 2.0), color=stone)

for x in [-2.55, -1.3, 0, 1.3, 2.55]:
    cylinder(
        pos=vector(x, 4.68, 7.28),
        axis=vector(0, 1.05, 0),
        radius=0.045,
        color=black
    )

for x in [-1.9, 0, 1.9]:
    box(
        pos=vector(x, 5.15, 7.28),
        size=vector(1.85, 0.88, 0.045),
        color=glass,
        opacity=0.35
    )

box(pos=vector(0, 5.68, 7.28), size=vector(5.3, 0.10, 0.12), color=black)
box(pos=vector(-2.8, 5.1, 6.35), size=vector(0.15, 1.1, 1.9), color=ivory)
box(pos=vector(2.8, 5.1, 6.35), size=vector(0.15, 1.1, 1.9), color=ivory)

for z in [-2.8, 1.2]:
    box(pos=vector(6.56, 6.2, z), size=vector(0.08, 2.1, 2.2), color=glass, opacity=0.8)
    box(pos=vector(6.62, 6.2, z - 1.1), size=vector(0.10, 2.2, 0.10), color=white)
    box(pos=vector(6.62, 6.2, z + 1.1), size=vector(0.10, 2.2, 0.10), color=white)

box(pos=vector(-14, 0.05, -1), size=vector(10, 0.2, 11), color=stone)

for z in range(-5, 4, 2):
    box(
        pos=vector(-14, 0.17, z),
        size=vector(9.7, 0.025, 0.06),
        color=light_wood
    )

box(pos=vector(-14, 4.0, -1), size=vector(9, 0.25, 9), color=wood)

for x in [-18, -16, -14, -12, -10]:
    box(
        pos=vector(x, 4.17, -1),
        size=vector(0.16, 0.12, 9),
        color=light_wood
    )

for x in [-18, -10]:
    for z in [-5, 3]:
        box(
            pos=vector(x, 2, z),
            size=vector(0.25, 4, 0.25),
            color=wood
        )

box(pos=vector(-14, 0.85, -3.8), size=vector(4.5, 0.55, 1.5), color=vector(0.78, 0.75, 0.66))
box(pos=vector(-14, 1.45, -4.4), size=vector(4.5, 0.9, 0.3), color=vector(0.55, 0.57, 0.50))

for x in [-16.15, -11.85]:
    box(
        pos=vector(x, 1.2, -3.8),
        size=vector(0.3, 0.8, 1.5),
        color=wood
    )

for x in [-15.3, -14, -12.7]:
    box(
        pos=vector(x, 1.2, -3.5),
        size=vector(1.05, 0.15, 0.8),
        color=white
    )

box(pos=vector(-14, 0.75, -0.5), size=vector(2.8, 0.15, 1.5), color=light_wood)

for x in [-15.1, -12.9]:
    for z in [-1, 0]:
        box(
            pos=vector(x, 0.4, z),
            size=vector(0.12, 0.7, 0.12),
            color=wood
        )

cylinder(
    pos=vector(-14, 0.9, -0.5),
    axis=vector(0, 0.45, 0),
    radius=0.18,
    color=sage
)

for x in [-17, -11]:
    box(pos=vector(x, 0.65, 1.5), size=vector(1.3, 0.2, 1.3), color=light_wood)
    box(pos=vector(x, 1.25, 2.05), size=vector(1.3, 1.2, 0.15), color=wood)

for x in [-18.5, -9.5]:
    cylinder(
        pos=vector(x, 0.2, -4.5),
        axis=vector(0, 0.8, 0),
        radius=0.45,
        color=stone
    )
    sphere(pos=vector(x, 1.35, -4.5), radius=0.75, color=sage)

for x in [-17, -14, -11]:
    sphere(pos=vector(x, 3.75, -1), radius=0.15, color=gold, emissive=True)
    local_light(pos=vector(x, 3.65, -1), color=gold)

for x in [-19, -9]:
    for z in [-2, 1]:
        cylinder(
            pos=vector(x, 0.2, z),
            axis=vector(0, 0.5, 0),
            radius=0.18,
            color=wood
        )
        sphere(pos=vector(x, 0.9, z), radius=0.55, color=sage)

box(pos=vector(-14, -0.05, 10), size=vector(9, 0.15, 12), color=stone)

for z in range(5, 16, 2):
    box(pos=vector(-14, 0.04, z), size=vector(8.8, 0.02, 0.05), color=white)

box(pos=vector(14, 0, 3), size=vector(12, 0.3, 9), color=white)
box(pos=vector(14, 0.17, 3), size=vector(11.4, 0.08, 8.4), color=water, opacity=0.8)

for x in [10, 18]:
    box(pos=vector(x, 0.6, 9), size=vector(2, 0.25, 3), color=white)
    box(pos=vector(x, 1.1, 7.7), size=vector(2, 0.9, 0.2), color=white)
    cylinder(pos=vector(x, 0.15, 8), axis=vector(0, 0.3, 0), radius=0.08, color=wood)

def make_umbrella(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 2.5, 0), radius=0.07, color=wood)
    cone(pos=vector(x, 2.5, z), axis=vector(0, 0.7, 0), radius=1.6, color=vector(0.90, 0.85, 0.72))

make_umbrella(21, 8)

def make_tree(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 3, 0), radius=0.35, color=wood)
    sphere(pos=vector(x, 4.2, z), radius=1.6, color=vector(0.12, 0.42, 0.16))
    sphere(pos=vector(x - 0.8, 4, z), radius=1, color=vector(0.18, 0.50, 0.20))
    sphere(pos=vector(x + 0.8, 4, z), radius=1, color=vector(0.18, 0.50, 0.20))
    sphere(pos=vector(x, 5.1, z), radius=0.8, color=sage)

make_tree(-20, -12)
make_tree(-20, 12)
make_tree(22, -12)
make_tree(23, 14)
make_tree(-23, 0)

for i in range(7):
    box(pos=vector(0, 0.02, 9 + i * 1.5), size=vector(3, 0.15, 1.1), color=vector(0.68, 0.64, 0.55))

for x in [-10, 10]:
    for z in [-8, 8]:
        cylinder(pos=vector(x, 0, z), axis=vector(0, 0.55, 0), radius=0.06, color=wood)
        sphere(pos=vector(x, 0.65, z), radius=0.22, color=gold, emissive=True)

for x in [-25, 25]:
    for z in range(-22, 24, 4):
        box(pos=vector(x, 0.8, z), size=vector(0.18, 1.6, 0.18), color=white)

    box(pos=vector(x, 0.65, 0), size=vector(0.2, 0.12, 45), color=wood)

for z in [-22, 22]:
    for x in range(-25, 26, 4):
        box(pos=vector(x, 0.8, z), size=vector(0.18, 1.6, 0.18), color=white)

    box(pos=vector(0, 0.65, z), size=vector(50, 0.12, 0.2), color=wood)

sphere(pos=vector(-25, 25, -25), radius=3, color=vector(1, 0.85, 0.35), emissive=True)

scene.center = vector(0, 4, 0)
scene.range = 40
scene.userspin = True
scene.userzoom = True
scene.userpan = False

scene.caption = "MY DREAM HOUSE"

MIN_ZOOM = 5
MAX_ZOOM = 65

while True:
    rate(30)

    if scene.range < MIN_ZOOM:
        scene.range = MIN_ZOOM
    elif scene.range > MAX_ZOOM:
        scene.range = MAX_ZOOM

