
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

app = Ursina(
    title="Japanese Modern Dream House - 3D Visualization",
    borderless=False,
    fullscreen=False,
    size=(1280, 720),
    vsync=True
)

Entity.default_shader = lit_with_shadows_shader
window.color = color.rgb(185, 211, 225)
window.fps_counter.enabled = True


WALL = color.hex('#e9e6dc')
CONCRETE = color.hex('#aaa99f')
DARK = color.hex('#252b2c')
WOOD = color.hex('#8b5a35')
WOOD_LIGHT = color.hex('#b98250')
GLASS = color.rgba(65, 105, 119, 185)
FLOOR = color.hex('#d8d2c5')
GRASS = color.hex('#6f8756')
LEAF = color.hex('#527b48')
WATER = color.hex('#328fa3')
STONE = color.hex('#777b78')
FABRIC = color.hex('#dedbd2')
GOLD = color.hex('#d6ad68')


world = Entity()
landscape = Entity(parent=world)
floor1 = Entity(parent=world)
floor2 = Entity(parent=world)
floor3 = Entity(parent=world)
roof_group = Entity(parent=world)


def cube(parent, position, scale, tint, collider=None, rotation=(0, 0, 0)):
    return Entity(
        parent=parent, model='cube', position=position, scale=scale,
        color=tint, collider=collider, rotation=rotation
    )

def make_tree(x, z, height=3.5):
    tree = Entity(parent=landscape, position=(x, 0, z))
    Entity(parent=tree, model='cylinder', scale=(0.28, height, 0.28),
           position=(0, height / 2, 0), color=color.hex('#6b5038'))
    for i, s in enumerate((1.8, 1.5, 1.25)):
        Entity(parent=tree, model='sphere', scale=(s, s * .72, s),
               position=(0, height * .72 + i * .45, 0),
               color=color.hex(('#456d43', '#527c4a', '#638c55')[i]))
    return tree

def make_shrub(x, z, scale=1):
    Entity(parent=landscape, model='sphere', position=(x, .45 * scale, z),
           scale=(.9 * scale, .8 * scale, .9 * scale), color=LEAF)

def make_lamp(x, z):
    Entity(parent=landscape, model='cube', position=(x, .75, z),
           scale=(.45, 1.5, .45), color=color.hex('#d8cbb0'))
    Entity(parent=landscape, model='cube', position=(x, 1.15, z),
           scale=(.48, .45, .48), color=color.hex('#f4dfad'), unlit=True)

def make_window(parent, x, y, z, width, height, depth=.09):
    cube(parent, (x, y, z), (width, height, depth), DARK)
    cube(parent, (x, y, z + depth * .55), (width - .12, height - .12, .025), GLASS)
    cube(parent, (x, y, z + depth), (.045, height, .035), color.hex('#87999a'))
    cube(parent, (x, y, z + depth), (width, .045, .035), color.hex('#87999a'))

def make_slatted_screen(parent, x, y, z, width, height, spacing=.22):
    count = max(2, int(width / spacing))
    for i in range(count):
        xx = x - width / 2 + i * width / (count - 1)
        cube(parent, (xx, y, z), (.055, height, .10), WOOD)

def make_balcony(parent, x, y, z, width, depth):
    cube(parent, (x, y, z), (width, .22, depth), WOOD_LIGHT)
    front_z = z + depth / 2
    cube(parent, (x, y + .62, front_z), (width, .07, .07), DARK)
    for i in range(17):
        xx = x - width / 2 + i * width / 16
        cube(parent, (xx, y + .31, front_z), (.045, .62, .045), DARK)


cube(landscape, (0, -.35, 0), (200, .5, 200), color.hex('#78905e'))
cube(landscape, (0, -.04, 1), (28, .18, 34), GRASS)

for i in range(8):
    cube(landscape, (-1.5, .08, 12 - i * 1.65), (2.1, .18, 1.0),
         color.hex('#c7c2b5'))


cube(landscape, (8.2, .04, 5.5), (7.0, .2, 17), color.hex('#aaa99f'))
for z in range(-2, 14, 2):
    cube(landscape, (8.2, .15, z), (6.8, .025, .035), color.hex('#c9c8bd'))


cube(landscape, (-8.0, .10, 5.5), (6.4, .55, 10.0), STONE)
cube(landscape, (-8.0, .34, 5.5), (5.8, .12, 9.4), WATER)
# Pool deck
cube(landscape, (-8.0, .02, 11.0), (8.0, .18, 2.2), color.hex('#c8c2b5'))


cube(landscape, (-5.0, .02, -5.0), (5.4, .12, 5.0), color.hex('#c9c2b2'))
for x, z in [(-6.7, -6.1), (-5.3, -5.0), (-3.9, -3.9)]:
    Entity(parent=landscape, model='sphere', position=(x, .18, z),
           scale=(.75, .22, .55), color=color.hex('#888982'))
make_tree(-5.0, -5.0, 2.5)


for x, z, s in [(-11, -5, 1.0), (-10.5, 12, 1.1), (2.0, 13, .9),
                (11.5, 12, 1.2), (-11.5, 1, .8), (1.5, -11, 1.0)]:
    make_tree(x, z, 3.2 * s)
for x, z in [(-3, 12), (-5, 13), (2, 10), (11, 5), (-10, -2), (2, -10)]:
    make_shrub(x, z, .8)


make_lamp(-10.5, 8)
make_lamp(-3.0, 9)
make_lamp(2.0, -7)


for x in range(-12, 14, 4):
    cube(landscape, (x, .55, 17), (3.8, 1.1, .25), CONCRETE)
for z in range(-13, 17, 4):
    cube(landscape, (-13.5, .55, z), (.25, 1.1, 3.8), CONCRETE)
    cube(landscape, (13.5, .55, z), (.25, 1.1, 3.8), CONCRETE)


cube(floor1, (0, .22, 0), (10, .35, 15), FLOOR, 'box')


cube(floor1, (-4.85, 1.95, 0), (.3, 3.3, 14.8), WALL, 'box')
cube(floor1, (4.85, 1.95, -1.2), (.3, 3.3, 12.4), WALL, 'box')
cube(floor1, (0, 1.95, -7.25), (10, 3.3, .3), WALL, 'box')
# Front feature wall and large sliding glass doors
cube(floor1, (-1.6, 1.9, 7.25), (6.5, 3.1, .16), DARK)
cube(floor1, (-1.6, 1.9, 7.36), (6.25, 2.9, .035), GLASS)
for x in (-4.65, -2.7, -.7, 1.55):
    cube(floor1, (x, 1.9, 7.42), (.07, 3.0, .06), DARK)

cube(floor1, (-1.5, .18, 8.5), (7.4, .25, 3.0), CONCRETE)
cube(floor1, (-1.5, 3.45, 8.2), (7.5, .22, 2.7), DARK)
for x in (-4.7, 1.7):
    cube(floor1, (x, 1.8, 8.2), (.25, 3.3, .25), WOOD)


cube(floor1, (-2.4, .55, 2.0), (3.0, .65, 1.0), FABRIC)
cube(floor1, (-2.4, .95, 2.45), (3.0, .35, .18), FABRIC)
cube(floor1, (-2.4, .18, -.1), (2.8, .08, 2.0), color.hex('#b5a995'))
cube(floor1, (-2.4, .55, -.1), (1.3, .35, .8), WOOD_LIGHT)

cube(floor1, (-4.55, 1.7, 1.0), (.12, 2.6, 3.8), WOOD)
cube(floor1, (-4.43, 1.8, 1.0), (.08, 1.2, 2.3), DARK)


cube(floor1, (1.5, .95, -1.8), (2.5, .12, 1.25), WOOD)
for x in (.55, 2.45):
    for z in (-2.55, -1.05):
        cube(floor1, (x, .48, z), (.48, .85, .48), FABRIC)

cube(floor1, (2.5, .65, -5.1), (3.2, 1.25, 1.0), WALL)
cube(floor1, (2.5, 1.32, -5.1), (3.35, .12, 1.1), color.hex('#5d625f'))
cube(floor1, (4.45, 1.2, -3.9), (.55, 2.2, 3.2), WOOD)
for z in (-5.0, -3.9, -2.8):
    cube(floor1, (1.1, .5, z), (.45, .8, .45), WOOD)


cube(floor1, (2.7, 1.8, -.1), (4.1, 3.0, .14), WALL)
cube(floor1, (2.7, 1.8, -2.0), (.14, 3.0, 3.8), WALL)


garage = Entity(parent=floor1, position=(8.0, 0, -1.0))
cube(garage, (0, .18, 0), (5.8, .35, 9.0), CONCRETE)
cube(garage, (0, 3.15, -4.35), (5.8, .25, .25), DARK)
cube(garage, (0, 1.65, 4.35), (5.8, 3.0, .18), DARK)
cube(garage, (0, 1.65, 4.47), (5.55, 2.75, .04), color.hex('#777b78'))
for x in (-2.5, -1.5, -.5, .5, 1.5, 2.5):
    cube(garage, (x, 1.65, 4.52), (.035, 2.7, .025), color.hex('#b9b9b1'))

car = Entity(parent=garage, position=(0, 0, -1.0))
cube(car, (0, .65, 0), (2.2, .75, 4.0), color.hex('#d6d9d6'))
cube(car, (0, 1.15, -.25), (1.75, .7, 2.0), color.hex('#8da5aa'))
for x in (-1.0, 1.0):
    for z in (-1.25, 1.25):
        Entity(parent=car, model='cylinder', position=(x, .35, z),
               scale=(.42, .22, .42), rotation=(0, 0, 90), color=DARK)


patio = Entity(parent=landscape, position=(7.5, 0, 10.0))
cube(patio, (0, .15, 0), (7.0, .25, 4.8), color.hex('#c8c2b5'))
cube(patio, (0, 1.0, -1.65), (5.2, 1.6, .7), WOOD)
cube(patio, (0, 1.85, -1.65), (5.3, .12, .8), color.hex('#565b59'))
cube(patio, (1.6, 1.35, -1.65), (1.1, .7, .65), DARK)
cube(patio, (-1.4, .65, .6), (2.4, .12, 1.0), WOOD)
for x in (-2.2, 2.2):
    cube(patio, (x, 1.3, 1.9), (.18, 2.6, .18), WOOD)
cube(patio, (0, 2.6, 1.9), (4.5, .18, .18), WOOD)


cube(floor2, (0, 3.65, 0), (10, .35, 15), FLOOR, 'box')

cube(floor2, (-4.85, 5.25, 0), (.3, 3.0, 14.8), WALL, 'box')
cube(floor2, (4.85, 5.25, -1.2), (.3, 3.0, 12.4), WALL, 'box')
cube(floor2, (0, 5.25, -7.25), (10, 3.0, .3), WALL, 'box')

cube(floor2, (-1.5, 5.2, 7.25), (6.8, 2.8, .16), DARK)
cube(floor2, (-1.5, 5.2, 7.36), (6.55, 2.6, .035), GLASS)
make_slatted_screen(floor2, -1.5, 5.2, 7.48, 6.2, 2.65, .32)

make_balcony(floor2, -1.2, 3.95, 9.0, 7.8, 3.3)

cube(floor2, (-1.5, 4.35, 8.5), (2.0, .45, .8), FABRIC)
cube(floor2, (1.0, 4.35, 8.5), (1.0, .45, .8), WOOD)


cube(floor2, (-2.2, 4.15, 1.8), (2.8, .35, 3.0), WOOD)
cube(floor2, (-2.2, 4.42, 1.8), (2.65, .22, 2.8), FABRIC)
cube(floor2, (-2.2, 5.0, .35), (2.7, .95, .15), WALL)

cube(floor2, (2.0, 4.15, -4.7), (2.2, .35, 2.5), WOOD)
cube(floor2, (2.0, 4.42, -4.7), (2.1, .22, 2.35), FABRIC)

cube(floor2, (3.7, 4.25, 1.0), (1.5, .75, .65), WALL)
cube(floor2, (3.7, 4.68, 1.0), (1.55, .08, .7), color.hex('#8caaa9'))
# Hallway divider
cube(floor2, (0.0, 5.15, -1.0), (.14, 2.8, 5.0), WALL)


make_window(floor2, 4.98, 5.2, -4.0, .08, 1.5, .08)


cube(floor3, (0, 7.05, 0), (9.5, .35, 14.5), FLOOR, 'box')
cube(floor3, (-4.65, 8.55, 0), (.25, 2.8, 14.3), WALL, 'box')
cube(floor3, (4.65, 8.55, -1.2), (.25, 2.8, 12.0), WALL, 'box')
cube(floor3, (0, 8.55, -7.0), (9.5, 2.8, .25), WALL, 'box')

cube(floor3, (-1.0, 8.5, 7.0), (6.7, 2.5, .12), DARK)
cube(floor3, (-1.0, 8.5, 7.09), (6.45, 2.3, .035), GLASS)

cube(floor3, (-1.8, 7.65, 2.0), (2.8, .55, 1.0), FABRIC)
cube(floor3, (2.1, 7.55, -3.5), (2.0, .12, 1.0), WOOD)
cube(floor3, (2.1, 8.0, -3.5), (1.8, .75, .08), DARK)

make_balcony(floor3, -1.0, 7.25, 8.6, 6.5, 2.4)


cube(roof_group, (0, 10.15, 0), (10.5, .35, 16), DARK)
cube(roof_group, (0, 10.36, 0), (10.0, .08, 15.5), WOOD_LIGHT)

for x in (-5.0, 5.0):
    cube(roof_group, (x, 10.75, 0), (.22, .85, 15.5), WALL)
cube(roof_group, (0, 10.75, -7.7), (10.0, .85, .22), WALL)

for x in (-3.5, 3.5):
    for z in (-2.5, 2.5):
        cube(roof_group, (x, 12.0, z), (.18, 3.0, .18), WOOD)
for z in (-2.5, 2.5):
    cube(roof_group, (0, 13.45, z), (7.2, .18, .18), WOOD)
for x in range(-3, 4):
    cube(roof_group, (x, 13.42, 0), (.12, .14, 5.0), WOOD)

cube(roof_group, (-2.3, 10.75, 4.5), (2.4, .5, .9), FABRIC)
cube(roof_group, (2.2, 10.55, -4.5), (1.0, .65, 1.0), WOOD)
for x in (-4.2, 4.2):
    cube(roof_group, (x, 10.75, 4.8), (1.0, .65, 1.0), color.hex('#514c42'))
    Entity(parent=roof_group, model='sphere', position=(x, 11.45, 4.8),
           scale=(1.0, .9, 1.0), color=LEAF)


sun = DirectionalLight(shadow_map_resolution=(2048, 2048), y=30, z=20, x=25, shadows=True)
sun.look_at(Vec3(0, 4, 0))
ambient = AmbientLight(color=color.rgba(125, 130, 140, 255))
sky = Sky(color=color.rgb(160, 195, 225))


orbit_pivot = Entity(position=(0, 5.0, 0), rotation=(14, 145, 0))
orbit_distance = 39

player = FirstPersonController(
    position=(0, 1.8, 18),
    speed=5,
    mouse_sensitivity=Vec2(40, 40),
    enabled=False
)
player.cursor.enabled = False
player.gravity = 0.5

camera.parent = orbit_pivot
camera.position = (0, 0, -orbit_distance)
camera.rotation = Vec3(0, 0, 0)
camera.fov = 40

MODE = "ORBIT"
ROOF_ON = True
TIME_MODE = 0


title = Text(
    text="JAPANESE MODERN DREAM HOUSE | 3 FLOORS",
    position=(-.86, .46), scale=1.05, color=color.hex('#f0d7ad')
)
status = Text(
    text="ORBIT VIEW  |  Arrow keys rotate  |  Mouse wheel zoom",
    position=(-.86, .42), scale=.75, color=color.white
)
help_text = Text(
    text=("CONTROLS\n"
          "ARROWS  Rotate house\n"
          "MOUSE WHEEL  Zoom\n"
          "TAB  Walk / Orbit\n"
          "WASD + MOUSE  Walk and look\n"
          "1 / 2 / 3  Isolate floor\n"
          "4  Show all floors\n"
          "R  Toggle rooftop\n"
          "L  Change lighting\n"
          "H  Reset camera"),
    position=(-.86, .20), scale=.68, color=color.white, background=True
)

def toggle_camera():
    global MODE
    if MODE == "ORBIT":
        MODE = "WALK"
        orbit_pivot.enabled = False
        player.position = (0, 1.8, 19)
        player.rotation_y = 180
        player.camera_pivot.rotation_x = 0
        player.enabled = True
        mouse.locked = True
        status.text = "WALK MODE  |  WASD move  |  Mouse look  |  TAB return"
        status.color = color.hex('#a7e6b0')
    else:
        MODE = "ORBIT"
        player.enabled = False
        mouse.locked = False
        orbit_pivot.enabled = True
        camera.parent = orbit_pivot
        camera.position = (0, 0, -orbit_distance)
        camera.rotation = Vec3(0, 0, 0)
        camera.fov = 40
        status.text = "ORBIT VIEW  |  Arrow keys rotate  |  Mouse wheel zoom"
        status.color = color.white

def toggle_roof():
    global ROOF_ON
    ROOF_ON = not ROOF_ON
    roof_group.enabled = ROOF_ON

def show_floor(n):
    floor1.enabled = (n in (1, 4))
    floor2.enabled = (n in (2, 4))
    floor3.enabled = (n in (3, 4))
    roof_group.enabled = ROOF_ON if n == 4 else False

def cycle_lighting():
    global TIME_MODE
    TIME_MODE = (TIME_MODE + 1) % 4
    if TIME_MODE == 0:
        sky.color = color.rgb(160, 195, 225)
        sun.color = color.white
        sun.position = (25, 30, 20)
        ambient.color = color.rgba(125, 130, 140, 255)
    elif TIME_MODE == 1:
        sky.color = color.rgb(244, 174, 112)
        sun.color = color.rgb(255, 190, 130)
        sun.position = (30, 12, 10)
        ambient.color = color.rgba(115, 90, 75, 255)
    elif TIME_MODE == 2:
        sky.color = color.rgb(115, 75, 90)
        sun.color = color.rgb(220, 125, 105)
        sun.position = (20, 7, 5)
        ambient.color = color.rgba(75, 65, 90, 255)
    else:
        sky.color = color.rgb(12, 22, 42)
        sun.color = color.rgb(90, 110, 170)
        sun.position = (-20, 25, -20)
        ambient.color = color.rgba(45, 55, 85, 255)

Button(text="Walk / Orbit [TAB]", scale=(.19, .045), position=(.77, .44),
       color=color.hex('#725b48'), on_click=toggle_camera)
Button(text="Rooftop [R]", scale=(.19, .045), position=(.77, .38),
       color=color.hex('#4c6470'), on_click=toggle_roof)
Button(text="Lighting [L]", scale=(.19, .045), position=(.77, .32),
       color=color.hex('#9a7650'), on_click=cycle_lighting)


def input(key):
    global orbit_distance
    if key == 'tab':
        toggle_camera()
    elif key == 'r':
        toggle_roof()
    elif key == '1':
        show_floor(1)
    elif key == '2':
        show_floor(2)
    elif key == '3':
        show_floor(3)
    elif key == '4':
        show_floor(4)
    elif key == 'l':
        cycle_lighting()
    elif key == 'h':
        if MODE == "ORBIT":
            orbit_pivot.rotation = (14, 145, 0)
            orbit_distance = 39
            camera.position = (0, 0, -orbit_distance)
            camera.fov = 40
        else:
            player.position = (0, 1.8, 19)
            player.rotation_y = 180
            player.camera_pivot.rotation_x = 0
    elif MODE == "ORBIT" and key in ('scroll up', 'scroll down'):
        orbit_distance = clamp(orbit_distance + (3 if key == 'scroll down' else -3), 19, 55)
        camera.z = -orbit_distance

def update():
    if MODE == "ORBIT":
        orbit_pivot.rotation_y += (
            held_keys['right arrow'] - held_keys['left arrow']
        ) * 55 * time.dt
        orbit_pivot.rotation_x = clamp(
            orbit_pivot.rotation_x +
            (held_keys['up arrow'] - held_keys['down arrow']) * 35 * time.dt,
            3, 65
        )

app.run()
