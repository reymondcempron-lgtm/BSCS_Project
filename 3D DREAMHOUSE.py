
from vpython import *
import math
import sys



scene = canvas(
    title="MY DREAM HOUSE - 3D WALKTHROUGH",
    width=1200,
    height=750,
    background=vector(0.55, 0.75, 0.95)
)

scene.autoscale = False
scene.range = 18
scene.userspin = False
scene.userzoom = True
scene.center = vector(0, 4, 0)



WHITE = vector(0.95, 0.95, 0.92)
GLASS = vector(0.45, 0.75, 0.85)
WOOD = vector(0.48, 0.32, 0.20)
LIGHT_WOOD = vector(0.68, 0.49, 0.31)
DARK = vector(0.15, 0.17, 0.19)

GREEN = vector(0.15, 0.42, 0.18)
LIGHT_GREEN = vector(0.30, 0.62, 0.25)
DARK_GREEN = vector(0.08, 0.27, 0.11)

STONE = vector(0.65, 0.65, 0.62)
GOLD = vector(0.92, 0.68, 0.28)



def block(pos, size, color, opacity=1):
    return box(
        pos=vector(*pos),
        size=vector(*size),
        color=color,
        opacity=opacity
    )



block(
    (0, -0.25, 0),
    (100, 0.5, 100),
    vector(0.30, 0.55, 0.25)
)

block(
    (0, 0.02, 0),
    (32, 0.05, 32),
    vector(0.35, 0.57, 0.28)
)




block(
    (0, 0.2, 0),
    (14, 0.4, 10),
    vector(0.78, 0.75, 0.68)
)


block(
    (0, 2, -4.0),
    (14, 4, 0.3),
    WHITE
)


for x in [-6.85, 6.85]:
    block(
        (x, 2, 0),
        (0.3, 4, 9.6),
        WHITE
    )


for x in [-4, 4]:
    block(
        (x, 2, 4.8),
        (4, 3.5, 0.08),
        GLASS,
        0.35
    )


for x in [-5.9, -4, -2.1, 2.1, 4, 5.9]:
    block(
        (x, 2, 4.88),
        (0.07, 3.5, 0.05),
        DARK
    )


door = box(
    pos=vector(0, 1.7, 4.95),
    size=vector(1.8, 3.0, 0.12),
    color=WOOD
)

door_handle = sphere(
    pos=vector(0.65, 1.7, 5.05),
    radius=0.08,
    color=GOLD
)

door_open = False


for x in [-6, -1, 1, 6]:
    block(
        (x, 2, 4.9),
        (0.4, 4, 0.5),
        WHITE
    )




block(
    (0, 4.15, 0),
    (15, 0.45, 11),
    WHITE
)


block(
    (0, 6, -4.7),
    (14, 3.5, 0.3),
    WHITE
)


for x in [-6.8, 6.8]:
    block(
        (x, 6, 0),
        (0.3, 3.5, 9),
        WHITE
    )


for x in [-3, 3]:
    block(
        (x, 6, 4.5),
        (5, 3, 0.08),
        GLASS,
        0.4
    )


for x in [-5.4, -3, -0.6, 0.6, 3, 5.4]:
    block(
        (x, 6, 4.58),
        (0.06, 3, 0.05),
        DARK
    )


block(
    (0, 8, 0),
    (15, 0.45, 11),
    WHITE
)



block(
    (0, 4.55, 5.8),
    (13, 0.15, 2),
    WHITE
)


block(
    (0, 5.1, 6.7),
    (12, 1, 0.08),
    GLASS,
    0.35
)

for x in [-6, 6]:
    block(
        (x, 5.1, 5.8),
        (0.08, 1, 1.8),
        GLASS,
        0.35
    )


for x in [-5.8, 5.8]:
    cylinder(
        pos=vector(x, 4.6, 6.7),
        axis=vector(0, 0.9, 0),
        radius=0.05,
        color=DARK
    )



block(
    (-3.5, 0.85, -1),
    (3.5, 0.9, 1.1),
    LIGHT_WOOD
)

block(
    (-3.5, 1.4, -1.5),
    (3.5, 1.0, 0.25),
    WHITE
)


block(
    (0, 0.65, -1),
    (2.2, 0.25, 1.3),
    WOOD
)


block(
    (3.7, 0.9, -2.5),
    (2.5, 0.25, 1.4),
    WOOD
)


for x in [2.8, 4.6]:
    for z in [-3.3, -1.7]:
        block(
            (x, 0.45, z),
            (0.4, 0.8, 0.4),
            LIGHT_WOOD
        )


block(
    (4, 0.65, -5),
    (3.2, 0.5, 2),
    WOOD
)

block(
    (4, 1.0, -5),
    (3.0, 0.2, 1.8),
    WHITE
)



for z in range(7, 15, 2):
    block(
        (0, 0.08, z),
        (3, 0.15, 1.5),
        STONE
    )

for x in [-3, -2.5, 2.5, 3]:
    for z in range(4, 13, 2):
        sphere(
            pos=vector(x, 0.1, z),
            radius=0.15,
            color=WHITE
        )



def create_tree(x, z, scale=1):

    cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, 2*scale, 0),
        radius=0.18*scale,
        color=WOOD
    )

    sphere(
        pos=vector(x, 2.2*scale, z),
        radius=1.1*scale,
        color=GREEN
    )

    sphere(
        pos=vector(x+0.5*scale, 2.5*scale, z),
        radius=0.7*scale,
        color=LIGHT_GREEN
    )

    sphere(
        pos=vector(x-0.5*scale, 2.5*scale, z),
        radius=0.7*scale,
        color=DARK_GREEN
    )


create_tree(-11, 0, 1.5)
create_tree(11, -2, 1.4)
create_tree(-11, 10, 1.2)
create_tree(12, 12, 1.0)



flower_colors = [
    vector(1, 0.3, 0.5),
    vector(1, 0.7, 0.8),
    vector(1, 1, 0.3),
    vector(0.8, 0.4, 0.8)
]

for i in range(35):

    x = -10 + (i % 10) * 2
    z = 7 + (i // 10) * 2

    cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, 0.5, 0),
        radius=0.035,
        color=GREEN
    )

    sphere(
        pos=vector(x, 0.55, z),
        radius=0.16,
        color=flower_colors[i % 4]
    )



cylinder(
    pos=vector(0, 0.2, 15),
    axis=vector(0, 0.25, 0),
    radius=2,
    color=DARK
)

sphere(
    pos=vector(0, 0.8, 15),
    radius=0.45,
    color=vector(1, 0.35, 0.05),
    emissive=True
)


for x in [-3, 3]:
    block(
        (x, 0.55, 15),
        (1, 0.5, 3),
        WOOD
    )


block(
    (11, 0.1, 9),
    (7, 0.2, 5),
    WHITE
)

block(
    (11, 0.22, 9),
    (6.6, 0.08, 4.6),
    vector(0.05, 0.55, 0.85),
    0.75
)



eye = vector(0, 1.7, 22)

yaw = 0.0
pitch = 0.0

keys = set()

def key_down(evt):
    keys.add(evt.key.lower())

def key_up(evt):
    keys.discard(evt.key.lower())

scene.bind("keydown", key_down)
scene.bind("keyup", key_up)



def toggle_door():

    global door_open

    hinge = vector(-0.9, 1.7, 4.95)

    if not door_open:

        door.rotate(
            angle=math.pi/2,
            axis=vector(0, 1, 0),
            origin=hinge
        )

        door_handle.rotate(
            angle=math.pi/2,
            axis=vector(0, 1, 0),
            origin=hinge
        )

        door_open = True

    else:

        door.rotate(
            angle=-math.pi/2,
            axis=vector(0, 1, 0),
            origin=hinge
        )

        door_handle.rotate(
            angle=-math.pi/2,
            axis=vector(0, 1, 0),
            origin=hinge
        )

        door_open = False



def update_camera():

    direction = vector(
        math.sin(yaw) * math.cos(pitch),
        math.sin(pitch),
        -math.cos(yaw) * math.cos(pitch)
    )

    scene.camera.pos = eye
    scene.camera.axis = direction * 10



scene.append_to_caption("""

MY DREAM HOUSE - WALKTHROUGH

CONTROLS:

W = Move Forward
S = Move Backward
A = Move Left
D = Move Right

LEFT / RIGHT = Look Around
UP / DOWN = Look Up and Down

E = Open / Close Front Door
R = Reset Position
ESC = Exit

Walk toward the front door and press E.

Enjoy exploring MY DREAM HOUSE!

""")


door_cooldown = 0

while True:

    rate(60)

    speed = 0.15

    forward = vector(
        math.sin(yaw),
        0,
        -math.cos(yaw)
    )

    right = vector(
        math.cos(yaw),
        0,
        math.sin(yaw)
    )

    movement = vector(0, 0, 0)

    if "w" in keys:
        movement += forward

    if "s" in keys:
        movement -= forward

    if "a" in keys:
        movement -= right

    if "d" in keys:
        movement += right

   

    if mag(movement) > 0:

        proposed = eye + norm(movement) * speed

        proposed.x = max(-22, min(22, proposed.x))
        proposed.z = max(-22, min(22, proposed.z))

        blocked = False

       
        if -4.9 < proposed.z < 4.9:
            if abs(proposed.x) > 6.35:
                blocked = True

       
        if abs(proposed.x) < 6.5:
            if -4.5 < proposed.z < -3.5:
                blocked = True

        
        if 4.5 < proposed.z < 5.35:

            if abs(proposed.x) > 0.95:
                blocked = True

            elif not door_open:
                blocked = True

        if not blocked:
            eye = proposed

   

    if "left" in keys:
        yaw -= 0.035

    if "right" in keys:
        yaw += 0.035

    if "up" in keys:
        pitch += 0.025

    if "down" in keys:
        pitch -= 0.025

    pitch = max(-1.2, min(1.2, pitch))

    

    if "e" in keys and door_cooldown == 0:

        if abs(eye.x) < 3 and 3 < eye.z < 8:

            toggle_door()
            door_cooldown = 20

    door_cooldown = max(0, door_cooldown - 1)

    

    if "r" in keys:

        eye = vector(0, 1.7, 22)
        yaw = 0.0
        pitch = 0.0

        keys.discard("r")


    update_camera()

    

    if "escape" in keys:
        sys.exit()
