from vpython import *
import random
import math

scene = canvas(title='MY DREAM HOUSE', width=1150, height=730,
               background=vector(0.55, 0.78, 0.98))
scene.center = vector(0, 4.5, 0)
scene.range = 17.5
scene.forward = vector(-1.25, -0.5, -1.45)
scene.autoscale = False

IVORY = vector(0.29, 0.32, 0.36)
WHITE = vector(0.91, 0.93, 0.94)
TAUPE = vector(0.20, 0.23, 0.27)
WOOD = vector(0.42, 0.24, 0.14)
DARK_WOOD = vector(0.28, 0.15, 0.08)
DARK = vector(0.18, 0.19, 0.20)
GLASS = vector(0.25, 0.50, 0.62)
STONE = vector(0.45, 0.48, 0.51)
GREEN = vector(0.25, 0.52, 0.22)
DARK_GREEN = vector(0.15, 0.36, 0.14)
MULCH = vector(0.24, 0.18, 0.14)
LIGHT = vector(1.0, 0.82, 0.48)
PAVER = vector(0.70, 0.70, 0.72)
WATER_DAY = vector(0.10, 0.60, 0.78)
WATER_NIGHT = vector(0.05, 0.40, 0.65)

lamps = []         
glass_list = []     
head_lights = []
cloud_list = []
star_list = []


def b(x, y, z, sx, sy, sz, shade, **kwargs):
    return box(pos=vector(x, y, z), size=vector(sx, sy, sz), color=shade, **kwargs)


def add_lamp_bulb(x, y, z, rad=0.11):
    l = sphere(pos=vector(x, y, z), radius=rad, color=LIGHT, emissive=True)
    lamps.append(l)
    return l


def stone_tiles(x1, x2, y1, y2, z, tile_w=0.53, tile_h=0.26):
    random.seed(int(abs(x1 * 100) + y1 * 9))
    y = y1
    r = 0
    while y < y2 - 0.02:
        x = x1 + (-tile_w / 2 if r % 2 else 0)
        while x < x2:
            a, c = max(x, x1), min(x + tile_w - 0.035, x2)
            if c > a:
                shade = random.choice([STONE, vector(0.68, 0.65, 0.59),
                                       vector(0.53, 0.51, 0.47), vector(0.75, 0.70, 0.64)])
                b((a + c) / 2, min(y + tile_h / 2, y2), z, c - a, min(tile_h - 0.025, y2 - y), 0.035, shade)
            x += tile_w
        y += tile_h
        r += 1


def front_window(x, z, w=1.7, h=2.35, y=2.45):
    b(x, y, z, w + 0.24, h + 0.22, 0.13, WHITE)
    b(x, y, z + 0.10, w + 0.08, h + 0.08, 0.12, DARK)
    g = b(x, y, z + 0.19, w - 0.10, h - 0.11, 0.055, GLASS, opacity=0.83, shininess=0.9)
    glass_list.append((g, 0.83))
    b(x, y, z + 0.24, 0.085, h - 0.07, 0.065, DARK)
    b(x, y + 0.15, z + 0.24, w - 0.05, 0.075, 0.065, DARK)
    b(x, y + h / 2 + 0.17, z + 0.20, w + 0.48, 0.18, 0.54, IVORY)    
    b(x, y - h / 2 - 0.16, z + 0.14, w + 0.30, 0.10, 0.30, WHITE)       


def side_window(z, y=2.4):
    x = -5.43
    b(x, y, z, 0.12, 2.25, 1.35, WHITE)
    b(x - 0.09, y, z, 0.10, 2.10, 1.22, DARK)
    g = b(x - 0.16, y, z, 0.045, 1.96, 1.08, GLASS, opacity=0.85)
    glass_list.append((g, 0.85))
    b(x - 0.21, y, z, 0.05, 1.96, 0.07, DARK)
    b(x - 0.21, y + 0.18, z, 0.05, 0.065, 1.12, DARK)

SIDEWALK_JOINT = vector(0.36, 0.37, 0.39)
b(0, -0.32, 0, 40, 0.45, 30, SIDEWALK_JOINT)
_rng = random.Random(3)
for ix in range(-19, 20, 2):
    for iz in range(-14, 15, 2):
        g = _rng.uniform(0.60, 0.72)                     
        b(ix, -0.075, iz, 1.92, 0.04, 1.92, vector(g, g, g + 0.015))
b(-2.5, 0.01, 4.8, 6.0, 0.06, 2.5, MULCH)                
b(6.0, 0.01, 4.8, 3.0, 0.06, 2.5, MULCH)

for i in range(6):
    b(3.05, -0.02, 6.7 + i * 0.8, 1.8, 0.04, 0.55, PAVER)

for i in range(12):
    b(-8.2, -0.02, -5.0 + i * 1.2, 1.4, 0.04, 0.8, PAVER)
    b(-6.4, -0.02, -5.0 + i * 1.2, 1.4, 0.04, 0.8, PAVER)

b(0, -0.015, 0, 16.5, 0.07, 13.5, PAVER)


random.seed(11)
for bx in [-5.2, -4.1, -3.0, -1.9, 5.2, 6.3, 7.2]:
    sphere(pos=vector(bx, 0.22, 5.1), radius=random.uniform(0.35, 0.48), color=DARK_GREEN)


FLOWER_COLORS = [vector(0.95, 0.45, 0.65), vector(1.0, 0.85, 0.25),
                 vector(1.0, 0.55, 0.2), vector(0.70, 0.55, 0.95), vector(0.95, 0.95, 0.95)]
for _ in range(26):
    sphere(pos=vector(random.uniform(-5.3, 0.3), 0.12, random.choice([random.uniform(4.1, 4.6),
                                                                      random.uniform(5.6, 5.9)])),
           radius=0.09, color=random.choice(FLOWER_COLORS))
for _ in range(14):
    sphere(pos=vector(random.uniform(6.0, 7.4), 0.12, random.uniform(3.8, 6.0)),
           radius=0.09, color=random.choice(FLOWER_COLORS))


def pine_tree(tx, tz, height=4.8):
    cylinder(pos=vector(tx, 0, tz), axis=vector(0, 0.9, 0), radius=0.2, color=DARK_WOOD)
    for i in range(3):
        cone(pos=vector(tx, 0.7 + i * height * 0.26, tz),
             axis=vector(0, height * 0.42, 0), radius=1.25 - i * 0.30,
             color=vector(0.13 + i * 0.02, 0.34 + i * 0.03, 0.13))


def round_tree(tx, tz, height=4.4):
    cylinder(pos=vector(tx, 0, tz), axis=vector(0, height * 0.55, 0), radius=0.24, color=DARK_WOOD)
    top = height * 0.62
    for dx, dy, dz, r in [(0, 0.8, 0, 1.25), (0.7, 0.3, 0.3, 0.95), (-0.7, 0.35, -0.3, 0.95),
                          (0.2, 0.2, -0.8, 0.9), (-0.2, 0.25, 0.8, 0.9)]:
        sphere(pos=vector(tx + dx, top + dy, tz + dz), radius=r,
               color=vector(0.20 + random.uniform(0, 0.06), 0.48 + random.uniform(0, 0.08), 0.20))


pine_tree(-11.5, 7.5, 5.2)
pine_tree(-11.5, -5.5, 4.8)
round_tree(11.5, 7.5, 5.0)
round_tree(11.5, -7.5, 4.8)
round_tree(-4.0, -8.5, 4.4)
pine_tree(2.5, -9.0, 4.6)


for hx in range(-12, 13):
    sphere(pos=vector(hx * 0.95, 0.55, -10.1), radius=0.65, color=DARK_GREEN)
b(0, 0.05, -10.1, 25, 0.10, 1.3, MULCH)                

CURB = vector(0.80, 0.80, 0.80)
YELLOW = vector(0.95, 0.80, 0.15)


def tree_pit(x, z):
    b(x, -0.03, z, 1.7, 0.05, 1.7, DARK)                   
    b(x, -0.02, z, 1.4, 0.05, 1.4, MULCH)                 


for tx_, tz_ in [(-11.5, 7.5), (-11.5, -5.5), (11.5, 7.5), (11.5, -7.5), (-4.0, -8.5),
                 (2.5, -9.0), (-8.5, 13.3), (17.0, 13.3)]:
    tree_pit(tx_, tz_)
round_tree(-8.5, 13.3, 3.8)                               
round_tree(17.0, 13.3, 3.8)

def city_lamp(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 4.6, 0), radius=0.09, color=DARK)
    b(x, 4.62, z + 0.45, 0.12, 0.10, 0.9, DARK)
    add_lamp_bulb(x, 4.50, z + 0.85, 0.16)


for lx in [-12.5, -3.5, 13.5]:
    city_lamp(lx, 14.2)


cylinder(pos=vector(-6.5, 0, 14.3), axis=vector(0, 0.6, 0), radius=0.14, color=vector(0.75, 0.10, 0.10))
sphere(pos=vector(-6.5, 0.66, 14.3), radius=0.15, color=vector(0.75, 0.10, 0.10))
cylinder(pos=vector(-6.72, 0.4, 14.3), axis=vector(0.44, 0, 0), radius=0.06, color=vector(0.75, 0.10, 0.10))

b(-0.5, 0.50, 13.3, 2.0, 0.08, 0.5, WOOD)
b(-0.5, 0.85, 13.05, 2.0, 0.5, 0.06, WOOD)
for dx in [-0.8, 0.8]:
    b(-0.5 + dx, 0.25, 13.3, 0.08, 0.5, 0.45, DARK)
cylinder(pos=vector(-2.4, 0, 13.4), axis=vector(0, 0.9, 0), radius=0.28, color=DARK_GREEN)
cylinder(pos=vector(-2.4, 0.9, 13.4), axis=vector(0, 0.05, 0), radius=0.30, color=DARK)


for cx, cz in [(-10.2, 1.5), (-10.2, -4.5), (-5.6, -4.5)]:
    b(cx, 1.6, cz, 0.22, 3.2, 0.22, DARK)

b(-7.9, 3.25, -1.5, 5.2, 0.18, 6.8, WOOD)
b(-7.9, 3.38, -1.5, 5.4, 0.10, 7.0, DARK)
for i in range(9):
    b(-10.2, 1.6, -4.0 + i * 0.65, 0.06, 3.1, 0.12, WOOD)


b(-7.9, 3.10, -1.5, 0.5, 0.05, 0.5, DARK)
add_lamp_bulb(-7.9, 3.02, -1.5, 0.12)


def build_car(cx, cz, body):
    b(cx, 0.58, cz, 1.9, 0.52, 4.3, body)                               
    b(cx, 1.07, cz - 0.2, 1.62, 0.48, 2.3, body)                       
    b(cx, 1.10, cz - 0.2, 1.67, 0.34, 2.05, vector(0.08, 0.12, 0.16), opacity=0.9)  
    for dx, x0 in [(0.95, 0.83), (-0.95, -1.05)]:
        for dz in [1.4, -1.4]:
            cylinder(pos=vector(cx + x0, 0.38, cz + dz), axis=vector(0.22, 0, 0),
                     radius=0.38, color=vector(0.06, 0.06, 0.07))
    for dx in [-0.6, 0.6]:
        hl = b(cx + dx, 0.66, cz + 2.16, 0.38, 0.14, 0.05, vector(1.0, 0.97, 0.8), emissive=True)
        head_lights.append(hl)
        b(cx + dx, 0.66, cz - 2.16, 0.38, 0.12, 0.05, vector(0.8, 0.05, 0.05), emissive=True)


build_car(-7.3, -1.5, vector(0.62, 0.07, 0.10))

b(0, 2.55, -0.3, 10.8, 4.4, 8.1, IVORY)
for x in [-5.30, 5.30]:
    b(x, 2.2, 0.3, 0.09, 2.8, 1.9, TAUPE)
for z in [-2.4, 0.1]:
    side_window(z)

b(-4.52, 2.12, 3.80, 1.27, 2.90, 0.10, TAUPE)
b(-0.20, 1.85, 3.81, 1.15, 2.8, 0.10, TAUPE)
front_window(-3.0, 3.87, 1.55, 2.10, 2.37)
front_window(0.45, 3.88, 1.72, 2.16, 2.42)

stone_tiles(-5.35, -0.35, 0.70, 1.48, 3.92)
stone_tiles(0.95, 5.35, 0.70, 1.43, 3.92)
for z in [-3.7, -1.1, 1.5]:
    for y in [0.88, 1.16, 1.44]:
        b(-5.48, y, z, 0.04, 0.24, 1.1, STONE)


b(3.05, 0.68, 5.12, 5.2, 0.22, 3.75, PAVER)
b(3.05, 0.74, 5.12, 5.1, 0.08, 3.62, WHITE)
for n in range(3):
    b(3.07, 0.12 + n * 0.19, 8.06 - n * 0.51, 3.80, 0.20, 0.78,
      vector(0.76 + n * 0.03, 0.74 + n * 0.03, 0.73 + n * 0.03))


b(2.12, 2.23, 3.89, 1.85, 3.15, 0.14, DARK)
door_pivot = vector(1.30, 2.23, 3.99)
door_leaf = b(2.12, 2.23, 3.99, 1.66, 2.96, 0.08, WOOD)
door_stripes = []
for k in range(4):
    door_stripes.append(b(2.12, 1.26 + k * 0.55, 4.045, 1.44, 0.032, 0.015, DARK_WOOD))
door_handle = b(2.76, 2.16, 4.08, 0.07, 0.48, 0.08, LIGHT)
door_open = False


def toggle_door():
    global door_open
    ang = 1.35 if not door_open else -1.35
    door_leaf.rotate(angle=ang, axis=vector(0, 1, 0), origin=door_pivot)
    door_handle.rotate(angle=ang, axis=vector(0, 1, 0), origin=door_pivot)
    for st in door_stripes:
        st.rotate(angle=ang, axis=vector(0, 1, 0), origin=door_pivot)
    door_open = not door_open

b(3.27, 2.25, 3.94, 0.37, 3.12, 0.08, DARK)
sl = b(3.27, 2.25, 4.01, 0.22, 2.92, 0.025, GLASS)
glass_list.append((sl, 1.0))


b(0, 4.70, -0.15, 11.2, 0.26, 8.6, TAUPE)
b(0, 6.80, -0.30, 10.8, 4.0, 8.1, IVORY)

for s in range(14):
    b(-4.9 + s * 0.13, 6.75, 3.85, 0.065, 3.4, 0.06, WOOD)

b(0.86, 6.70, 3.83, 0.72, 3.60, 0.11, TAUPE)
front_window(-3.03, 3.90, 2.0, 2.48, 6.65)
front_window(3.05, 3.90, 2.3, 2.50, 6.70)
for z in [-2.4, 0.2]:
    side_window(z, 6.72)


b(-0.40, 8.91, -0.50, 12.5, 0.29, 10.20, WOOD)
b(-0.40, 9.16, -0.50, 12.8, 0.26, 10.46, WHITE)
b(-0.40, 9.31, -0.50, 13.05, 0.12, 10.70, TAUPE)


for px in [-3.6, -1.6, 0.4, 2.4, 4.4]:
    for pz in [-2.8, -1.0]:
        panel = b(px, 9.62, pz, 1.8, 0.06, 1.1, vector(0.08, 0.14, 0.30), shininess=0.9)
        panel.rotate(angle=radians(18), axis=vector(1, 0, 0))
        b(px, 9.45, pz, 0.08, 0.26, 0.08, DARK)


b(2.35, 4.43, 5.03, 7.4, 0.20, 5.30, WOOD)
b(2.35, 4.60, 5.03, 7.70, 0.22, 5.56, WHITE)
b(2.35, 4.77, 5.03, 7.90, 0.14, 5.70, TAUPE)
b(2.35, 4.86, 5.03, 7.98, 0.075, 5.76, WHITE)

FLOOR_TOP = 4.90
RAIL_TOP = 6.30
MID_Y = (FLOOR_TOP + RAIL_TOP) / 2
TX1, TX2 = -1.42, 6.18      
TZ1, TZ2 = 3.90, 7.75       


def rail_run(x1, z1, x2, z2, n):
    along_x = abs(x2 - x1) > abs(z2 - z1)
    length = abs(x2 - x1) if along_x else abs(z2 - z1)
    for i in range(n + 1):                                   
        t = i / n
        b(x1 + (x2 - x1) * t, MID_Y, z1 + (z2 - z1) * t, 0.11, RAIL_TOP - FLOOR_TOP, 0.11, DARK)
    seg = length / n - 0.11
    for i in range(n):                                      
        t = (i + 0.5) / n
        ax, az = x1 + (x2 - x1) * t, z1 + (z2 - z1) * t
        if along_x:
            b(ax, 5.68, az, seg, 1.10, 0.04, GLASS, opacity=0.30)
            b(ax, FLOOR_TOP + 0.10, az, seg + 0.11, 0.20, 0.10, DARK)
        else:
            b(ax, 5.68, az, 0.04, 1.10, seg, GLASS, opacity=0.30)
            b(ax, FLOOR_TOP + 0.10, az, 0.10, 0.20, seg + 0.11, DARK)
    cx, cz = (x1 + x2) / 2, (z1 + z2) / 2             
    if along_x:
        b(cx, RAIL_TOP + 0.03, cz, length + 0.2, 0.07, 0.15, WOOD)
    else:
        b(cx, RAIL_TOP + 0.03, cz, 0.15, 0.07, length + 0.2, WOOD)


rail_run(TX1, TZ2, TX2, TZ2, 5)      
rail_run(TX1, TZ1, TX1, TZ2, 3)      
rail_run(TX2, TZ1, TX2, TZ2, 3)      
for cx_, cz_ in [(TX1, TZ2), (TX2, TZ2)]:
    add_lamp_bulb(cx_, RAIL_TOP + 0.16, cz_, 0.07)    


for i, mx in enumerate([1.9, 2.7]):
    for j, mz in enumerate([4.8, 5.6, 6.4]):
        shade = [vector(0.25, 0.65, 0.35), vector(0.95, 0.75, 0.20),
                 vector(0.30, 0.55, 0.90), vector(0.90, 0.40, 0.35)][(i + j) % 4]
        b(mx, FLOOR_TOP + 0.02, mz, 0.78, 0.04, 0.78, shade)


b(0.2, 4.98, 6.2, 1.9, 0.30, 0.8, WHITE)
b(0.2, 5.25, 6.55, 1.9, 0.45, 0.20, WHITE)
b(3.9, 5.02, 6.4, 0.9, 0.06, 0.9, WOOD) 
cylinder(pos=vector(3.9, 4.88, 6.4), axis=vector(0, 0.14, 0), radius=0.08, color=DARK)


for x in [4.0, 5.3]:
    b(x, 5.08, 4.25, 0.55, 0.35, 0.48, TAUPE)
    sphere(pos=vector(x, 5.46, 4.25), radius=0.31, color=GREEN)


for x, z in [(0.35, 7.13), (5.42, 7.13)]:
    b(x, 1.46, z, 0.95, 1.45, 0.95, STONE)
    stone_tiles(x - 0.45, x + 0.45, 0.76, 2.12, z + 0.49, 0.34, 0.20)
    b(x, 3.27, z, 0.67, 2.35, 0.67, IVORY)
    b(x, 2.20, z, 0.78, 0.25, 0.78, TAUPE)
    b(x, 4.15, z, 0.80, 0.24, 0.80, TAUPE)
    b(x, 4.37, z, 0.87, 0.14, 0.87, WHITE)
b(5.05, 1.05, 5.75, 0.6, 0.75, 1.9, IVORY)

for x, y, z in [(-0.1, 2.95, 4.04), (3.7, 2.95, 4.04), (0.35, 4.25, 6.88), (5.42, 4.25, 6.88)]:
    b(x, y, z, 0.23, 0.31, 0.12, DARK)
    add_lamp_bulb(x, y - 0.07, z + 0.11)

for x, z in [(0, 7.0), (2.1, 7.0), (4.3, 7.0)]:
    b(x, 4.30, z, 0.36, 0.025, 0.36, DARK)
    add_lamp_bulb(x, 4.27, z, 0.13)

for i in range(3):
    b(2.05, 0.28 + i * 0.19, 8.06 - i * 0.51, 0.08, 0.08, 0.22, DARK)
    add_lamp_bulb(2.11, 0.28 + i * 0.19, 8.06 - i * 0.51, 0.05)


cylinder(pos=vector(6.2, 0, 10.4), axis=vector(0, 3.8, 0), radius=0.08, color=DARK)
b(5.8, 3.8, 10.4, 0.9, 0.10, 0.22, DARK)
add_lamp_bulb(5.45, 3.72, 10.4, 0.14)


for bx, bz in [(1.7, 9.0), (4.4, 9.0), (1.7, 10.2), (4.4, 10.2)]:
    cylinder(pos=vector(bx, 0, bz), axis=vector(0, 0.55, 0), radius=0.07, color=DARK)
    add_lamp_bulb(bx, 0.62, bz, 0.09)

b(9.0, 0.03, -1.0, 6.6, 0.08, 9.0, vector(0.80, 0.78, 0.74))          
POOL_X, POOL_Z, POOL_W, POOL_L = 9.0, -1.2, 4.6, 6.4
water = b(POOL_X, 0.07, POOL_Z, POOL_W, 0.06, POOL_L, WATER_DAY, opacity=0.88, shininess=1.0)
cope_c = vector(0.93, 0.93, 0.92)
b(POOL_X, 0.085, POOL_Z + POOL_L / 2 + 0.15, POOL_W + 0.6, 0.06, 0.3, cope_c)
b(POOL_X, 0.085, POOL_Z - POOL_L / 2 - 0.15, POOL_W + 0.6, 0.06, 0.3, cope_c)
b(POOL_X - POOL_W / 2 - 0.15, 0.085, POOL_Z, 0.3, 0.06, POOL_L, cope_c)
b(POOL_X + POOL_W / 2 + 0.15, 0.085, POOL_Z, 0.3, 0.06, POOL_L, cope_c)
for lz in [POOL_Z - 2.0, POOL_Z + 2.0]:
    add_lamp_bulb(POOL_X - POOL_W / 2 - 0.15, 0.17, lz, 0.07)
    add_lamp_bulb(POOL_X + POOL_W / 2 + 0.15, 0.17, lz, 0.07)


for lx in [POOL_X - 0.3, POOL_X + 0.3]:
    cylinder(pos=vector(lx, 0.1, POOL_Z + POOL_L / 2 + 0.2), axis=vector(0, 0.6, 0), radius=0.03,
             color=vector(0.8, 0.8, 0.85))

for lz in [-2.6, 0.2]:
    b(11.75, 0.30, lz, 0.8, 0.12, 1.9, WHITE)
    for dx in [-0.33, 0.33]:
        for dz in [-0.8, 0.8]:
            b(11.75 + dx, 0.14, lz + dz, 0.08, 0.2, 0.08, DARK)
    back = b(11.75, 0.50, lz - 1.0, 0.8, 0.10, 0.7, WHITE)
    back.rotate(angle=radians(-35), axis=vector(1, 0, 0))
cylinder(pos=vector(11.75, 0.1, -1.2), axis=vector(0, 2.3, 0), radius=0.05, color=DARK)
cone(pos=vector(11.75, 2.4, -1.2), axis=vector(0, -0.55, 0), radius=0.9, color=vector(0.9, 0.35, 0.25))
b(11.75, 0.35, -1.2, 0.5, 0.5, 0.5, WOOD)

GX, GZ = -8.5, -7.6
b(GX, 0.06, GZ, 3.4, 0.12, 3.4, WOOD)
for dx in [-1.5, 1.5]:
    for dz in [-1.5, 1.5]:
        b(GX + dx, 1.3, GZ + dz, 0.16, 2.5, 0.16, WHITE)
b(GX, 2.5, GZ, 3.5, 0.12, 3.5, TAUPE)
pyramid(pos=vector(GX, 2.56, GZ), axis=vector(0, 1.3, 0), size=vector(1.3, 3.6, 3.6), color=WOOD)
cylinder(pos=vector(GX, 0.12, GZ), axis=vector(0, 0.7, 0), radius=0.07, color=DARK)
cylinder(pos=vector(GX, 0.82, GZ), axis=vector(0, 0.06, 0), radius=0.6, color=WHITE)
for ang in range(0, 360, 90):
    cx_ = GX + 1.05 * math.cos(math.radians(ang))
    cz_ = GZ + 1.05 * math.sin(math.radians(ang))
    b(cx_, 0.42, cz_, 0.38, 0.06, 0.38, DARK_WOOD)
    b(cx_, 0.22, cz_, 0.30, 0.26, 0.30, DARK)
cylinder(pos=vector(GX, 2.4, GZ), axis=vector(0, -0.3, 0), radius=0.02, color=DARK)
add_lamp_bulb(GX, 2.0, GZ, 0.14)

night_mode = False
FENCE_Z = 10.75
FENCE_X = 12.45
FENCE_BACK = -10.75


def fence_front(x_start, x_end, z):
    for rail_y in [0.55, 1.65]:
        b((x_start + x_end) / 2, rail_y, z, x_end - x_start, 0.09, 0.10, DARK)
    x = x_start + 0.18
    while x < x_end:
        b(x, 1.12, z, 0.07, 1.65, 0.085, DARK)
        x += 0.43


GATE_LEFT, GATE_RIGHT = 1.05, 5.05
fence_front(-FENCE_X, GATE_LEFT, FENCE_Z)
fence_front(GATE_RIGHT, FENCE_X, FENCE_Z)
fence_front(-FENCE_X, FENCE_X, FENCE_BACK)
for side_x in [-FENCE_X, FENCE_X]:
    for rail_y in [0.55, 1.65]:
        b(side_x, rail_y, 0, 0.10, 0.09, FENCE_Z - FENCE_BACK, DARK)
    zz = FENCE_BACK + 0.2
    while zz < FENCE_Z:
        b(side_x, 1.12, zz, 0.085, 1.65, 0.07, DARK)
        zz += 0.43

for post_x, post_z in [(-FENCE_X, FENCE_Z), (FENCE_X, FENCE_Z),
                       (-FENCE_X, FENCE_BACK), (FENCE_X, FENCE_BACK),
                       (GATE_LEFT, FENCE_Z), (GATE_RIGHT, FENCE_Z)]:
    b(post_x, 1.06, post_z, 0.38, 2.12, 0.38, STONE)
    b(post_x, 2.16, post_z, 0.50, 0.13, 0.50, TAUPE)
for post_x in [GATE_LEFT, GATE_RIGHT]:
    add_lamp_bulb(post_x, 2.36, FENCE_Z, 0.1)


def gate_panel(x1, x2):
    pieces = []
    for x in [x1, x2]:
        pieces.append(b(x, 1.10, FENCE_Z, 0.10, 1.75, 0.11, DARK))
    for y in [0.26, 1.96]:
        pieces.append(b((x1 + x2) / 2, y, FENCE_Z, x2 - x1, 0.10, 0.12, DARK))
    x = x1 + 0.27
    while x < x2:
        pieces.append(b(x, 1.10, FENCE_Z, 0.075, 1.65, 0.10, DARK))
        x += 0.38
    return pieces


left_gate = gate_panel(GATE_LEFT + 0.16, 3.02)
right_gate = gate_panel(3.08, GATE_RIGHT - 0.16)
gate_is_open = False


def toggle_gate():
    global gate_is_open
    a = 1.15 if not gate_is_open else -1.15
    for item in left_gate:
        item.rotate(angle=a, axis=vector(0, 1, 0), origin=vector(GATE_LEFT + 0.16, 0, FENCE_Z))
    for item in right_gate:
        item.rotate(angle=-a, axis=vector(0, 1, 0), origin=vector(GATE_RIGHT - 0.16, 0, FENCE_Z))
    gate_is_open = not gate_is_open

sun = sphere(pos=vector(-35, 22, -45), radius=3.5, color=vector(1.0, 0.92, 0.55), emissive=True)
moon = sphere(pos=vector(-25, 22, -50), radius=2.6, color=vector(0.92, 0.94, 1.0), emissive=True,
              visible=False)

random.seed(5)
for _ in range(170):
    az = random.uniform(0, 2 * math.pi)
    el = random.uniform(math.radians(10), math.radians(80))
    r = 70
    st = sphere(pos=vector(r * math.cos(el) * math.cos(az), r * math.sin(el), r * math.cos(el) * math.sin(az)),
                radius=random.uniform(0.10, 0.25), color=color.white, emissive=True, visible=False)
    star_list.append(st)


def make_cloud(theta, radius, height):
    parts = []
    for off, size in [(vector(0, 0, 0), vector(7, 2.6, 3.4)), (vector(3.2, -0.3, 0.4), vector(5, 2.0, 3.0)),
                      (vector(-3.2, -0.4, -0.3), vector(5, 2.0, 3.0)), (vector(0.5, 0.9, 0), vector(4, 2.0, 2.6))]:
        p = sphere(pos=vector(0, 0, 0), size=size, color=color.white, emissive=True, opacity=0.92)
        parts.append((p, off))
    cloud_list.append({'theta': theta, 'r': radius, 'y': height, 'parts': parts,
                       'speed': random.uniform(0.0004, 0.0008)})


for i in range(9):
    make_cloud(i * 2 * math.pi / 9 + random.uniform(-0.2, 0.2), random.uniform(48, 58), random.uniform(24, 34))

sun_light = distant_light(direction=vector(-1, -2, -1), color=color.white)
scene.ambient = vector(0.63, 0.63, 0.63)


def toggle_lights():
    global night_mode
    night_mode = not night_mode
    if night_mode:
        scene.background = vector(0.04, 0.06, 0.14)
        scene.ambient = vector(0.22, 0.24, 0.32)
        sun_light.color = vector(0.22, 0.26, 0.45)
        sun.visible = False
        moon.visible = True
        for s in star_list:
            s.visible = True
        for lp in lamps:
            lp.color = vector(1.0, 0.90, 0.65)
        for g, _ in glass_list:
            g.color = vector(1.0, 0.82, 0.45)
            g.opacity = 0.96
            g.emissive = True
        for cl in cloud_list:
            for p, _ in cl['parts']:
                p.color = vector(0.20, 0.23, 0.33)
                p.emissive = False
        water.emissive = True
    else:
        scene.background = vector(0.55, 0.78, 0.98)
        scene.ambient = vector(0.63, 0.63, 0.63)
        sun_light.color = color.white
        sun.visible = True
        moon.visible = False
        for s in star_list:
            s.visible = False
        for lp in lamps:
            lp.color = LIGHT
        for g, op in glass_list:
            g.color = GLASS
            g.opacity = op
            g.emissive = False
        for cl in cloud_list:
            for p, _ in cl['parts']:
                p.color = color.white
                p.emissive = True
        water.emissive = False


   
def set_view(fwd, rng=17.5, ctr=vector(0, 4.5, 0)):
    scene.forward = fwd
    scene.range = rng
    scene.center = ctr


def keyInput(evt):
    k = evt.key.lower()
    if k == 'g':
        toggle_gate()
    elif k == 'l':
        toggle_lights()
    elif k == 'd':
        toggle_door()
    elif k == '1':
        set_view(vector(-1.25, -0.5, -1.45))
    elif k == '2':
        set_view(vector(0, -0.25, -1), 16)
    elif k == '3':
        set_view(vector(-0.6, -1.6, -0.9), 22, vector(0, 2, 0))
    elif k == '4':
        set_view(vector(-1, -0.35, 0.15), 18, vector(4, 3, 0))


scene.bind('keydown', keyInput)

scene.caption = ('\nTWO-STOREY MODERN HOUSE  -  ENHANCED EDITION\n'
                 'Rotate: Left-drag | Zoom: Mouse Wheel | Pan: Right-drag\n'
                 'Hotkeys: [L] Day/Night | [G] Entrance Gate | [D] Front Door\n'
                 'Views: [1] Hero | [2] Front | [3] Aerial | [4] Pool side\n')

print('Dream House Loaded Successfully!')
 
t = 0
while True:
    rate(60)
    t += 1
 
    for cl in cloud_list:
        cl['theta'] += cl['speed']
        c = vector(cl['r'] * math.cos(cl['theta']), cl['y'], cl['r'] * math.sin(cl['theta']))
        for p, off in cl['parts']:
            p.pos = c + off
   
    base = WATER_NIGHT if night_mode else WATER_DAY
    water.color = vector(base.x + 0.03 * math.sin(t * 0.04),
                         base.y + 0.05 * math.sin(t * 0.06),
                         base.z + 0.04 * math.sin(t * 0.05))

while True:
    rate (60)