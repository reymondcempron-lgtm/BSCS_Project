from vpython import *

scene.title = "My 3D Dream House"
scene.width = 1000
scene.height = 650
scene.background = vector(0.55, 0.78, 0.95)
scene.forward = vector(-0.35, -0.3, -1)
scene.center = vector(0, 4, 6)
scene.range = 28

scene.ambient = color.gray(0.35)
scene.lights = []
distant_light(direction=vector(0.3, 0.5, 0.8), color=color.gray(0.5))
distant_light(direction=vector(-0.4, 0.3, -0.5), color=color.gray(0.2))

white = vector(0.94, 0.92, 0.88)
wall = vector(0.88, 0.85, 0.8)
dark = vector(0.1, 0.12, 0.15)
stone = vector(0.38, 0.33, 0.3)
stone_line = vector(0.18, 0.16, 0.15)
light_stone = vector(0.72, 0.7, 0.66)
marble = vector(0.86, 0.84, 0.8)
wood = vector(0.62, 0.34, 0.16)
trunk_wood = vector(0.4, 0.26, 0.12)
glass = vector(0.65, 0.85, 0.95)
hedge = vector(0.12, 0.42, 0.15)
leaf = vector(0.1, 0.55, 0.15)
steel = vector(0.75, 0.77, 0.8)
warm = vector(1, 0.9, 0.6)
gold = vector(0.8, 0.65, 0.3)
F2 = 4.4
G = 0.08


def B(x0, x1, y0, y1, z0, z1, c, **kw):
    if abs(x1 - x0) < 0.005 or abs(y1 - y0) < 0.005 or abs(z1 - z0) < 0.005:
        return None
    return box(pos=vector((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
               size=vector(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)), color=c, **kw)


def front_wall(x0, x1, y0, y1, za, zb, c, ox0, ox1, oy0, oy1):
    B(x0, ox0, y0, y1, za, zb, c)
    B(ox1, x1, y0, y1, za, zb, c)
    B(ox0, ox1, y0, oy0, za, zb, c)
    B(ox0, ox1, oy1, y1, za, zb, c)


def glassw(x0, x1, y0, y1, z, vert=(), hor=()):
    B(x0, x1, y0, y1, z - 0.03, z + 0.03, glass, opacity=0.08)
    B(x0 - 0.06, x1 + 0.06, y1 - 0.04, y1 + 0.06, z - 0.07, z + 0.07, dark)
    B(x0 - 0.06, x1 + 0.06, y0 - 0.06, y0 + 0.04, z - 0.07, z + 0.07, dark)
    B(x0 - 0.06, x0 + 0.04, y0 - 0.06, y1 + 0.06, z - 0.07, z + 0.07, dark)
    B(x1 - 0.04, x1 + 0.06, y0 - 0.06, y1 + 0.06, z - 0.07, z + 0.07, dark)
    for m in vert:
        B(m - 0.03, m + 0.03, y0, y1, z - 0.06, z + 0.06, dark)
    for h in hor:
        B(x0, x1, h - 0.03, h + 0.03, z - 0.06, z + 0.06, dark)


def door_x(x, d, zc, y0, w=1.0, h=2.3):
    B(x, x + d * 0.06, y0, y0 + h + 0.1, zc - w / 2 - 0.1, zc + w / 2 + 0.1, dark)
    B(x + d * 0.06, x + d * 0.1, y0, y0 + h, zc - w / 2, zc + w / 2, wood)
    B(x + d * 0.1, x + d * 0.12, y0 + 0.2, y0 + 1.0, zc - w / 2 + 0.12, zc + w / 2 - 0.12, wood * 0.8)
    B(x + d * 0.1, x + d * 0.12, y0 + 1.2, y0 + h - 0.2, zc - w / 2 + 0.12, zc + w / 2 - 0.12, wood * 0.8)
    B(x + d * 0.12, x + d * 0.2, y0 + 1.05, y0 + 1.15, zc + w / 2 - 0.35, zc + w / 2 - 0.1, gold)
    sphere(pos=vector(x + d * 0.16, y0 + 1.1, zc + w / 2 - 0.15), radius=0.06, color=gold)


def slide_handles(xc, y0, z):
    for dx in (-0.14, 0.14):
        B(xc + dx - 0.02, xc + dx + 0.02, y0 + 0.8, y0 + 1.7, z - 0.1, z - 0.06, steel)


def lounger(x, zc, c):
    for lx in (-0.3, 0.3):
        for lz in (-0.85, 0.65):
            B(x + lx - 0.025, x + lx + 0.025, 7.56, 7.8, zc + lz - 0.025, zc + lz + 0.025, white)
    B(x - 0.35, x + 0.35, 7.8, 7.88, zc - 0.9, zc + 0.7, c)
    sn, cs = 0.57, 0.82
    box(pos=vector(x, 7.88 + 0.45 * sn, zc + 0.7 + 0.45 * cs), axis=vector(0, sn, cs), size=vector(0.9, 0.08, 0.7), color=c)
    B(x - 0.34, x + 0.34, 7.88, 7.9, zc - 0.3, zc + 0.2, color.white)


def umbrella(x, z, c):
    cylinder(pos=vector(x, 7.56, z), axis=vector(0, 2.5, 0), radius=0.04, color=steel)
    cone(pos=vector(x, 9.7, z), axis=vector(0, 0.6, 0), radius=1.6, color=c, shininess=0.05)
    ring(pos=vector(x, 9.7, z), axis=vector(0, 1, 0), radius=1.6, thickness=0.04, color=color.white)
    sphere(pos=vector(x, 10.35, z), radius=0.07, color=gold)


def plant(x, y, z):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.45, 0), radius=0.28, color=dark)
    for dx, dy, dz, r in [(0, 0.95, 0, 0.4), (0.2, 0.65, 0.15, 0.3), (-0.2, 0.7, -0.15, 0.3)]:
        sphere(pos=vector(x + dx, y + dy, z + dz), radius=r, color=leaf, shininess=0.05)


def chair(x, z, d, y, c):
    for dx in (-1, 1):
        for dz in (-1, 1):
            B(x + dx * 0.18 - 0.02, x + dx * 0.18 + 0.02, y, y + 0.42, z + dz * 0.18 - 0.02, z + dz * 0.18 + 0.02, dark)
    B(x - 0.22, x + 0.22, y + 0.42, y + 0.47, z - 0.22, z + 0.22, c)
    zb = z + d * 0.2
    B(x - 0.22, x + 0.22, y + 0.47, y + 0.95, zb - 0.02, zb + 0.02, c)


def chandelier(x, y, z, top, r):
    cylinder(pos=vector(x, y, z), axis=vector(0, top - y, 0), radius=0.02, color=dark)
    ring(pos=vector(x, y, z), axis=vector(0, 1, 0), radius=r, thickness=0.03, color=gold)
    for k in range(8):
        a = radians(45 * k)
        sphere(pos=vector(x + r * cos(a), y + 0.08, z + r * sin(a)), radius=0.08, color=warm, emissive=True)
    sphere(pos=vector(x, y - 0.1, z), radius=0.14, color=warm, emissive=True)


def lamp(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 0.8, 0), radius=0.07, color=color.gray(0.2))
    sphere(pos=vector(x, 0.9, z), radius=0.15, color=vector(1, 0.95, 0.7), emissive=True)


def lantern(x, z, h=1.6):
    box(pos=vector(x, 0.15, z), size=vector(0.6, 0.3, 0.6), color=stone)
    cylinder(pos=vector(x, 0.3, z), axis=vector(0, h, 0), radius=0.06, color=dark)
    box(pos=vector(x, h + 0.6, z), size=vector(0.5, 0.6, 0.5), color=vector(1, 0.8, 0.4), emissive=True)
    for cx in [-0.27, 0.27]:
        for cz in [-0.27, 0.27]:
            box(pos=vector(x + cx, h + 0.6, z + cz), size=vector(0.06, 0.66, 0.06), color=dark)
    box(pos=vector(x, h + 0.3, z), size=vector(0.6, 0.06, 0.6), color=dark)
    cone(pos=vector(x, h + 0.9, z), axis=vector(0, 0.4, 0), radius=0.45, color=dark)
    sphere(pos=vector(x, h + 1.35, z), radius=0.08, color=dark)


def tree(x, z, h=3):
    cylinder(pos=vector(x, 0, z), axis=vector(0, h, 0), radius=0.35, color=trunk_wood, shininess=0.05)
    sphere(pos=vector(x, h + 0.9, z), radius=1.7, color=leaf, shininess=0.05)
    sphere(pos=vector(x + 1.0, h + 0.4, z + 0.3), radius=1.2, color=leaf * 0.85, shininess=0.05)
    sphere(pos=vector(x - 1.0, h + 0.5, z - 0.3), radius=1.2, color=leaf * 1.15, shininess=0.05)
    sphere(pos=vector(x + 0.2, h + 0.5, z + 1.0), radius=1.1, color=leaf * 0.95, shininess=0.05)
    sphere(pos=vector(x - 0.2, h + 1.9, z), radius=1.0, color=leaf * 1.1, shininess=0.05)


def pine(x, z, h=6):
    cylinder(pos=vector(x, 0, z), axis=vector(0, h * 0.3, 0), radius=0.25, color=trunk_wood, shininess=0.05)
    cone(pos=vector(x, h * 0.2, z), axis=vector(0, h * 0.55, 0), radius=1.8, color=vector(0.05, 0.4, 0.15), shininess=0.05)
    cone(pos=vector(x, h * 0.5, z), axis=vector(0, h * 0.5, 0), radius=1.3, color=vector(0.05, 0.45, 0.18), shininess=0.05)


def make_cloud(x, y, z):
    parts = []
    for dx, dy, r in [(0, 0, 2), (2, 0.4, 2.4), (4.2, 0, 1.9), (1.6, -0.3, 1.8)]:
        parts.append(sphere(pos=vector(x + dx, y + dy, z), radius=r, color=color.white))
    return compound(parts)


ground = box(pos=vector(0, -0.05, 4), size=vector(60, 0.1, 50), color=vector(0.25, 0.55, 0.2), shininess=0.05)

# ---------------- LEFT WING: GARAGE + BEDROOM ----------------
B(-14, -4, 0, 4.2, -4, 4, white)
B(-12.2, -5.8, 0, 3.05, 4.0, 4.06, dark)
B(-12.1, -5.9, 0, 3.0, 4.02, 4.12, vector(0.1, 0.1, 0.12), shininess=0.3)
for gy in [0.75, 1.5, 2.25]:
    B(-12.1, -5.9, gy - 0.025, gy + 0.025, 4.12, 4.16, vector(0.25, 0.25, 0.28))

B(-14.2, -3.8, 4.2, 4.4, -4, 5, white)
B(-14, -4, F2, 7.2, -4, -3.8, wall)
B(-14, -13.8, F2, 7.2, -4, 2, wall)
B(-4.2, -4, F2, 7.2, -4, 2, wall)
front_wall(-14, -4, F2, 7.2, 1.8, 2.0, wall, -11.2, -5.6, F2 + 0.02, 6.9)
glassw(-11.2, -5.6, F2 + 0.02, 6.9, 1.9, vert=(-9.8, -8.4, -7.0))
slide_handles(-8.4, F2, 2.0)
B(-14.2, -3.8, 7.2, 7.5, -4.3, 2.3, dark)
for i in range(5):
    B(-13.2 + 0.4 * i - 0.075, -13.2 + 0.4 * i + 0.075, F2, 7.2, 2.0, 2.2, wood)
B(-14.2, -3.8, F2, 5.4, 4.93, 4.98, glass, opacity=0.15)
B(-14.2, -3.8, 5.38, 5.44, 4.9, 5.02, dark)
B(-14.18, -14.13, F2, 5.4, 2.0, 5.0, glass, opacity=0.15)

B(-13.8, -4.2, F2, F2 + 0.02, -3.8, 1.8, vector(0.72, 0.55, 0.36))
B(-11.9, -6.1, F2 + 0.02, F2 + 0.05, -3.1, 1.1, vector(0.55, 0.62, 0.65))
B(-10.8, -7.2, F2, F2 + 0.4, -3.8, 0.6, wood)
B(-10.7, -7.3, F2 + 0.4, F2 + 0.7, -3.7, 0.5, vector(0.97, 0.97, 0.95))
B(-11.1, -6.9, F2 + 0.2, F2 + 2.0, -3.8, -3.6, wood)
B(-10.725, -7.275, F2 + 0.7, F2 + 0.82, -2.2, 0.4, vector(0.2, 0.42, 0.5))
B(-10.45, -9.15, F2 + 0.7, F2 + 0.95, -3.55, -2.85, color.white)
B(-8.85, -7.55, F2 + 0.7, F2 + 0.95, -3.55, -2.85, color.white)
B(-10.6, -7.4, F2, F2 + 0.5, 0.65, 1.35, vector(0.3, 0.3, 0.33))
for tx in [-11.6, -6.4]:
    B(tx - 0.45, tx + 0.45, F2, F2 + 0.8, -3.8, -3.0, wood)
    cylinder(pos=vector(tx, F2 + 0.8, -3.4), axis=vector(0, 0.35, 0), radius=0.06, color=dark)
    sphere(pos=vector(tx, F2 + 1.25, -3.4), radius=0.22, color=vector(1, 0.9, 0.6), emissive=True)
B(-13.8, -12.8, F2, F2 + 2.6, -3.5, -0.5, vector(0.9, 0.88, 0.84))
for wz in [-2.75, -2.0, -1.25]:
    B(-12.82, -12.78, F2 + 0.1, F2 + 2.5, wz - 0.015, wz + 0.015, dark)
for wz in [-2.1, -1.9]:
    B(-12.82, -12.76, F2 + 1.0, F2 + 1.5, wz - 0.025, wz + 0.025, dark)

door_x(-4.3, -1, 0.4, F2 + 0.02)

# ---------------- CENTER TOWER ----------------
for px in [-3.4, 3.4]:
    box(pos=vector(px, 4.9, 0), size=vector(1.8, 9.8, 9), color=stone)
    for i in range(19):
        box(pos=vector(px, 0.5 + 0.5 * i, 4.51), size=vector(1.8, 0.04, 0.02), color=stone_line)
        jx = px + (0.45 if i % 2 == 0 else -0.45)
        box(pos=vector(jx, 0.5 + 0.5 * i - 0.25, 4.51), size=vector(0.04, 0.46, 0.02), color=stone_line)
B(-4.7, 4.7, 9.8, 10.1, -4.8, 4.8, dark)

B(-2.5, 2.5, 0, 1.0, -4, 3, marble)
B(-2.5, 2.5, 0, 9.8, -4.2, -4.0, white)
front_wall(-2.5, 2.5, 0, 4.2, 2.8, 3.0, white, -2.1, 2.1, 1.0, 4.0)
glassw(-2.1, 2.1, 1.0, 4.0, 2.9, vert=(-0.9, 0, 0.9), hor=(3.3,))
B(-1.05, 1.05, 3.4, 3.55, 2.95, 3.12, dark)
B(-1.05, -0.9, 1.0, 3.55, 2.95, 3.12, dark)
B(0.9, 1.05, 1.0, 3.55, 2.95, 3.12, dark)
B(-0.01, 0.01, 1.0, 3.4, 2.95, 3.12, dark)
for s_ in (-1, 1):
    x0_ = 0.02 if s_ > 0 else -0.9
    x1_ = 0.9 if s_ > 0 else -0.02
    B(x0_, x1_, 1.02, 3.4, 3.0, 3.1, wood)
    B(x0_ + 0.14, x1_ - 0.14, 1.3, 2.0, 3.1, 3.12, wood * 0.75)
    B(x0_ + 0.14, x1_ - 0.14, 2.2, 3.2, 3.1, 3.12, glass, opacity=0.35)
    B(s_ * 0.12 - 0.02, s_ * 0.12 + 0.02, 1.8, 2.7, 3.1, 3.2, gold)
B(-1.1, 1.1, 1.0, 1.04, 3.2, 4.0, vector(0.2, 0.2, 0.22))
front_wall(-2.5, 2.5, 4.2, 9.8, 2.8, 3.0, white, -2.1, 2.1, F2 + 0.02, 9.0)
glassw(-2.1, 2.1, F2 + 0.02, 9.0, 2.9, vert=(-1.05, 0, 1.05), hor=(7.0,))
slide_handles(0, F2, 3.0)
B(-2.5, 2.5, F2, F2 + 1.0, 4.35, 4.4, glass, opacity=0.15)
B(-2.55, 2.55, F2 + 0.98, F2 + 1.04, 4.32, 4.44, dark)

B(-0.9, 2.5, 4.2, 4.4, -4, 3, marble)
B(-2.5, -0.9, 4.2, 4.4, -4, -2.28, marble)
B(-2.5, -0.9, 4.2, 4.4, 1.2, 3, marble)

B(-2.5, 2.5, 4.2, 4.4, 3.0, 4.4, white)
for dx in [-1.5, 0, 1.5]:
    sphere(pos=vector(dx, 4.15, 3.9), radius=0.1, color=vector(1, 0.95, 0.7), emissive=True)

# entrance hall + stair
B(-0.6, 2.0, 1.0, 1.03, -1.6, 1.9, vector(0.45, 0.2, 0.18))
for i in range(16):
    top = 1.0 + 0.2 * (i + 1)
    za = 2.2 - 0.28 * i
    B(-2.5, -0.9, 1.0, top - 0.05, za - 0.28, za, white)
    B(-2.5, -0.9, top - 0.05, top, za - 0.31, za, wood)
    cylinder(pos=vector(-0.92, top, za - 0.14), axis=vector(0, 0.9, 0), radius=0.02, color=dark)
cylinder(pos=vector(-0.92, 2.1, 2.06), axis=vector(0, 3.0, -4.2), radius=0.04, color=dark)
cylinder(pos=vector(-0.92, 1.0, 2.2), axis=vector(0, 1.3, 0), radius=0.07, color=wood)
sphere(pos=vector(-0.92, 2.35, 2.2), radius=0.11, color=gold)

B(-1.0, 1.6, 1.75, 1.85, -3.95, -3.45, wood)
for lx in (-0.95, 1.55):
    for lz in (-3.9, -3.5):
        B(lx - 0.04, lx + 0.04, 1.0, 1.75, lz - 0.04, lz + 0.04, dark)
B(-1.0, 1.6, 2.2, 3.8, -4.0, -3.97, dark)
B(-0.9, 1.5, 2.3, 3.7, -3.97, -3.94, vector(0.75, 0.85, 0.9), shininess=0.9)
cylinder(pos=vector(0.3, 1.85, -3.7), axis=vector(0, 0.4, 0), radius=0.12, color=vector(0.2, 0.4, 0.6))
sphere(pos=vector(0.3, 2.35, -3.7), radius=0.2, color=vector(0.9, 0.4, 0.5))
B(1.5, 2.3, 1.0, 1.45, -0.8, 0.8, vector(0.3, 0.3, 0.33))
plant(2.0, 1.0, 2.2)
plant(-0.2, 1.0, -3.5)
chandelier(0.3, 3.3, 0, 4.2, 0.55)

# living room (upper center)
B(-0.7, 2.3, F2, F2 + 0.05, -2.9, 1.5, vector(0.9, 0.86, 0.78))
B(-0.7, 2.3, F2, F2 + 0.45, -3.95, -3.0, vector(0.3, 0.36, 0.42))
B(-0.7, 2.3, F2 + 0.45, F2 + 1.0, -3.95, -3.6, vector(0.3, 0.36, 0.42))
B(-0.7, -0.5, F2 + 0.45, F2 + 0.7, -3.6, -3.0, vector(0.3, 0.36, 0.42))
B(2.1, 2.3, F2 + 0.45, F2 + 0.7, -3.6, -3.0, vector(0.3, 0.36, 0.42))
for cx in (-0.2, 0.8, 1.7):
    B(cx - 0.4, cx + 0.4, F2 + 0.45, F2 + 0.62, -3.6, -3.05, vector(0.45, 0.52, 0.58))
for ax in (0.1, 1.7):
    B(ax - 0.4, ax + 0.4, F2, F2 + 0.45, 0.9, 1.7, vector(0.62, 0.34, 0.16))
    B(ax - 0.4, ax + 0.4, F2 + 0.45, F2 + 1.0, 1.55, 1.7, vector(0.62, 0.34, 0.16))
    B(ax - 0.34, ax + 0.34, F2 + 0.45, F2 + 0.58, 0.95, 1.55, vector(0.93, 0.9, 0.82))
B(0.1, 1.5, F2 + 0.35, F2 + 0.42, -2.1, -1.0, wood)
for lx in (0.15, 1.45):
    for lz in (-2.05, -1.05):
        B(lx - 0.03, lx + 0.03, F2 + 0.05, F2 + 0.35, lz - 0.03, lz + 0.03, dark)
cylinder(pos=vector(0.8, F2 + 0.42, -1.55), axis=vector(0, 0.25, 0), radius=0.1, color=vector(0.2, 0.4, 0.6))
for k, ax in enumerate((-0.2, 0.6, 1.4)):
    B(ax - 0.3, ax + 0.3, F2 + 2.0, F2 + 3.2, -4.0, -3.95, vector(0.8 - 0.1 * k, 0.65, 0.35 + 0.1 * k))
cylinder(pos=vector(2.2, F2, -2.6), axis=vector(0, 1.8, 0), radius=0.03, color=dark)
sphere(pos=vector(2.2, F2 + 1.9, -2.6), radius=0.2, color=warm, emissive=True)
plant(-1.9, F2, 2.3)
plant(2.0, F2, 2.3)
chandelier(0.9, 7.6, -0.5, 9.8, 0.8)

# ---------------- RIGHT WING: GUEST ROOM (LOWER) + KITCHEN/DINING (UPPER) ----------------
B(4, 12, 0, 4.2, -4, -3.8, white)
B(11.8, 12, 0, 4.2, -4, 4, white)
front_wall(4, 12, 0, 4.2, 3.8, 4.0, white, 5.2, 10.8, 0.9, 3.5)
glassw(5.2, 10.8, 0.9, 3.5, 3.9, vert=(6.6, 8.0, 9.4))
B(4.3, 11.8, 0, G, -3.8, 3.8, vector(0.72, 0.56, 0.38))
B(3.8, 12.2, 4.2, 4.4, -4, 5, white)

B(5.7, 10.3, G, G + 0.03, -3.0, 1.5, vector(0.55, 0.5, 0.45))
B(6.2, 9.8, G, G + 0.4, -3.8, -0.2, wood)
B(6.3, 9.7, G + 0.4, G + 0.7, -3.7, -0.3, color.white)
B(6.0, 10.0, G + 0.2, G + 1.9, -3.8, -3.6, wood)
B(6.3, 9.7, G + 0.7, G + 0.82, -2.2, -0.3, vector(0.5, 0.35, 0.3))
B(6.55, 7.85, G + 0.7, G + 0.95, -3.55, -2.85, color.white)
B(8.15, 9.45, G + 0.7, G + 0.95, -3.55, -2.85, color.white)
for cx in (5.5, 10.5):
    B(cx - 0.4, cx + 0.4, G, G + 0.7, -3.8, -3.0, wood)
    cylinder(pos=vector(cx, G + 0.7, -3.4), axis=vector(0, 0.3, 0), radius=0.05, color=dark)
    sphere(pos=vector(cx, G + 1.1, -3.4), radius=0.2, color=vector(1, 0.9, 0.6), emissive=True)
B(7.2, 8.8, G + 2.2, G + 3.2, -3.8, -3.75, vector(0.75, 0.6, 0.35))
B(10.8, 11.8, G, G + 2.6, 0.5, 3.0, vector(0.9, 0.88, 0.84))
for wz in (1.3, 2.2):
    B(10.76, 10.8, G + 0.1, G + 2.5, wz - 0.015, wz + 0.015, dark)
B(4.5, 6.5, G + 0.72, G + 0.77, 2.4, 3.4, wood)
for lx in (4.55, 6.45):
    for lz in (2.45, 3.35):
        B(lx - 0.03, lx + 0.03, G, G + 0.72, lz - 0.03, lz + 0.03, dark)
chair(5.5, 1.9, -1, G, dark)
plant(10.9, G, 3.3)
door_x(4.3, 1, 0.2, G + 0.03)

B(4, 12, F2, 7.2, -4, -3.8, white)
B(11.8, 12, F2, 7.2, -4, 3, white)
front_wall(4, 12, F2, 7.2, 2.8, 3.0, white, 5.0, 11.0, F2 + 0.02, 6.9)
glassw(5.0, 11.0, F2 + 0.02, 6.9, 2.9, vert=(6.5, 8.0, 9.5))
slide_handles(8.0, F2, 3.0)
B(3.8, 12.2, 7.2, 7.5, -4.3, 3.3, dark)
B(4.3, 11.8, F2, F2 + 0.02, -3.8, 2.8, vector(0.82, 0.8, 0.76))

B(4.3, 10.4, F2, F2 + 0.9, -3.8, -3.1, vector(0.25, 0.27, 0.3))
B(4.3, 10.4, F2 + 0.9, F2 + 0.95, -3.8, -3.05, vector(0.85, 0.85, 0.83))
B(4.3, 5.9, F2 + 1.9, F2 + 2.7, -3.8, -3.4, wood)
B(7.1, 8.8, F2 + 1.9, F2 + 2.7, -3.8, -3.4, wood)
B(5.9, 7.1, F2 + 1.7, F2 + 2.7, -3.8, -3.3, steel)
for bx in (6.2, 6.8):
    for bz in (-3.65, -3.35):
        cylinder(pos=vector(bx, F2 + 0.95, bz), axis=vector(0, 0.03, 0), radius=0.12, color=dark)
B(8.3, 9.3, F2 + 0.93, F2 + 0.97, -3.6, -3.2, vector(0.5, 0.52, 0.55))
cylinder(pos=vector(8.8, F2 + 0.95, -3.7), axis=vector(0, 0.4, 0), radius=0.025, color=steel)
cylinder(pos=vector(8.8, F2 + 1.35, -3.7), axis=vector(0, 0, 0.3), radius=0.025, color=steel)
B(10.5, 11.7, F2, F2 + 2.3, -3.8, -2.9, steel)
B(10.6, 10.66, F2 + 0.9, F2 + 1.8, -2.9, -2.85, dark)

B(5.8, 9.2, F2, F2 + 0.95, -2.0, -0.8, vector(0.25, 0.27, 0.3))
B(5.7, 9.3, F2 + 0.95, F2 + 1.02, -2.1, -0.7, vector(0.85, 0.85, 0.83))
for sx in (6.4, 7.5, 8.6):
    cylinder(pos=vector(sx, F2, -0.2), axis=vector(0, 0.7, 0), radius=0.05, color=dark)
    cylinder(pos=vector(sx, F2 + 0.7, -0.2), axis=vector(0, 0.08, 0), radius=0.25, color=wood)
for px in (6.5, 8.5):
    cylinder(pos=vector(px, 6.6, -1.4), axis=vector(0, 0.6, 0), radius=0.015, color=dark)
    sphere(pos=vector(px, 6.5, -1.4), radius=0.22, color=warm, emissive=True)

B(5.9, 10.1, F2 + 0.02, F2 + 0.05, 0.2, 2.6, vector(0.6, 0.62, 0.58))
B(6.3, 9.7, F2 + 0.72, F2 + 0.8, 0.7, 2.1, wood)
for lx in (6.4, 9.6):
    for lz in (0.8, 2.0):
        B(lx - 0.04, lx + 0.04, F2, F2 + 0.72, lz - 0.04, lz + 0.04, dark)
for cx in (6.9, 8.0, 9.1):
    chair(cx, 0.35, -1, F2, vector(0.3, 0.3, 0.33))
    chair(cx, 2.45, 1, F2, vector(0.3, 0.3, 0.33))
B(7.0, 9.0, 6.5, 6.56, 1.25, 1.55, dark)
B(7.0, 9.0, 6.46, 6.5, 1.25, 1.55, warm, emissive=True)
for px in (7.2, 8.8):
    cylinder(pos=vector(px, 6.56, 1.4), axis=vector(0, 0.64, 0), radius=0.015, color=dark)
B(11.75, 11.8, F2 + 1.5, F2 + 2.5, -1.5, 0.5, vector(0.75, 0.6, 0.35))
plant(11.1, F2, 2.3)
door_x(4.3, 1, 0.6, F2 + 0.05)

# rooftop pool deck above the kitchen / dining wing
B(4.3, 12.0, 7.5, 7.56, -4.1, 3.1, vector(0.85, 0.82, 0.76))
B(4.3, 12.1, 7.56, 8.56, 3.12, 3.16, glass, opacity=0.18)
B(4.3, 12.16, 8.54, 8.6, 3.08, 3.2, dark)
B(12.04, 12.1, 7.56, 8.56, -4.2, 3.16, glass, opacity=0.18)
B(12.0, 12.16, 8.54, 8.6, -4.2, 3.2, dark)
B(4.3, 12.1, 7.56, 8.56, -4.2, -4.14, glass, opacity=0.18)
B(4.3, 12.16, 8.54, 8.6, -4.2, -4.08, dark)
B(5.0, 5.25, 7.5, 7.9, -3.4, 0.4, light_stone)
B(10.75, 11.0, 7.5, 7.9, -3.4, 0.4, light_stone)
B(5.0, 11.0, 7.5, 7.9, -3.4, -3.15, light_stone)
B(5.0, 11.0, 7.5, 7.9, 0.15, 0.4, light_stone)
B(5.25, 10.75, 7.5, 7.8, -3.15, 0.15, vector(0.1, 0.6, 0.9), opacity=0.9, shininess=0.6)
for lx_ in (10.1, 10.5):
    cylinder(pos=vector(lx_, 7.8, 0.28), axis=vector(0, 0.8, 0), radius=0.03, color=steel)
for ry_ in (7.95, 8.2, 8.45):
    B(10.1, 10.5, ry_ - 0.015, ry_ + 0.015, 0.25, 0.31, steel)
sphere(pos=vector(7.6, 7.95, -1.5), radius=0.3, color=vector(0.95, 0.3, 0.3))
sphere(pos=vector(6.4, 7.9, -2.4), radius=0.2, color=vector(1, 0.85, 0.2))
for k_, x_ in enumerate((5.7, 6.9, 9.3, 10.5)):
    lounger(x_, 1.35, vector(0.3, 0.6, 0.85) if k_ % 2 == 0 else vector(0.95, 0.5, 0.4))
umbrella(6.3, 1.4, vector(0.9, 0.3, 0.25))
umbrella(9.9, 1.4, vector(0.95, 0.8, 0.2))
B(7.6, 8.4, 7.56, 8.0, 1.0, 1.7, wood)
cylinder(pos=vector(8.0, 8.0, 1.35), axis=vector(0, 0.2, 0), radius=0.1, color=vector(0.95, 0.6, 0.2))
plant(11.5, 7.56, -3.6)
plant(4.8, 7.56, -3.6)

B(4.0, 12.0, F2, F2 + 1.0, 4.93, 4.98, glass, opacity=0.15)
B(4.0, 12.2, F2 + 0.98, F2 + 1.04, 4.9, 5.02, dark)
B(12.15, 12.2, F2, F2 + 1.0, 3.0, 5.0, glass, opacity=0.15)

for sx in [-13.4, 12.4]:
    box(pos=vector(sx, 2.8, 4.04), size=vector(0.3, 0.5, 0.08), color=dark)
    sphere(pos=vector(sx, 2.8, 4.1), radius=0.1, color=vector(1, 0.95, 0.7), emissive=True)

# ---------------- PORCH, STEPS, GARDEN ----------------
box(pos=vector(0, 0.5, 4.575), size=vector(8.4, 1.0, 3.15), color=light_stone)
for i in range(4):
    h = 0.25 * (i + 1)
    box(pos=vector(0, h / 2, 8.6 - 0.7 * i), size=vector(7, h, 0.7), color=light_stone * (0.95 + 0.03 * i))
for sx in [-1, 1]:
    box(pos=vector(sx * 4.2, 0.6, 7.55), size=vector(1.4, 1.2, 2.8), color=vector(0.6, 0.58, 0.55))
    for k in range(9):
        a = radians(40 * k)
        cone(pos=vector(sx * 4.2, 1.2, 7.55), axis=vector(0.9 * cos(a), 1.1, 0.9 * sin(a)), radius=0.12,
             color=vector(0.2, 0.5 + 0.03 * (k % 3), 0.25))

box(pos=vector(-9, 0.03, 10.9), size=vector(6.4, 0.06, 13.8), color=color.gray(0.55))
box(pos=vector(0, 0.03, 12.975), size=vector(4.2, 0.06, 9.45), color=vector(0.75, 0.72, 0.68))
box(pos=vector(0, 0.04, 18.5), size=vector(60, 0.08, 1.6), color=color.gray(0.8))
box(pos=vector(0, 0.02, 21.5), size=vector(60, 0.05, 4.5), color=color.gray(0.25))
for lx in range(-28, 29, 4):
    box(pos=vector(lx, 0.06, 21.5), size=vector(2, 0.02, 0.15), color=color.yellow)

box(pos=vector(-5.2, 0.5, 11), size=vector(1.0, 1.0, 13), color=hedge, shininess=0.05)
box(pos=vector(8, 0.45, 7.5), size=vector(8, 0.9, 1.2), color=hedge, shininess=0.05)
box(pos=vector(-9, 0.45, 18.0), size=vector(6.4, 0.9, 0.8), color=hedge, shininess=0.05)

box(pos=vector(-24, 1.1, 0.5), size=vector(0.15, 2.2, 33), color=dark)
box(pos=vector(24, 1.1, 0.5), size=vector(0.15, 2.2, 33), color=dark)

for lx in [-2.4, 2.4]:
    for lz in [10, 13.5, 17]:
        lamp(lx, lz)

for lz in [-2, 2, 6, 10]:
    lantern(-15.5, lz)
    lantern(13.5, lz)

entrance_light = local_light(pos=vector(0, 4, 5), color=vector(0.5, 0.4, 0.25))

tree(18, 10, 3)
tree(-18, 10, 3.2)
tree(-4.5, 15, 2.5)
pine(21, -8, 7)
pine(-21, -6, 7)
pine(-20, 2, 6)
pine(22, 4, 6)

clouds = [make_cloud(-26, 20, -25), make_cloud(0, 24, -28), make_cloud(20, 19, -24)]

rz = 21.5
car_body = box(pos=vector(0, 0.6, rz), size=vector(3, 0.8, 1.4), color=color.red)
car_top = box(pos=vector(-0.2, 1.3, rz), size=vector(1.6, 0.7, 1.3), color=color.blue)
wheels = []
for wx in [-1, 1]:
    for wz in [-0.7, 0.7]:
        wheels.append(cylinder(pos=vector(wx, 0.3, rz + wz - 0.1), axis=vector(0, 0, 0.2),
                               radius=0.3, color=color.black))
car = compound([car_body, car_top] + wheels)
car.pos.x = -30

sun = sphere(pos=vector(-30, 4, -30), radius=2.5, color=color.yellow, emissive=True)

t = 1.2
sun_speed = 0.0004

while True:
    rate(60)

    t += sun_speed
    if t > pi:
        t = 0.05
    day = sin(t)
    sun.pos = vector(-30 * cos(t), 4 + 22 * day, -30)
    sun.color = vector(1, 0.55 + 0.45 * day, 0.2 + 0.3 * day) * 0.85
    scene.background = vector(0.55, 0.78, 0.95) * (0.3 + 0.7 * day)

    car.pos.x += 0.12
    if car.pos.x > 32:
        car.pos.x = -32

    for c in clouds:
        c.pos.x += 0.015
        if c.pos.x > 40:
            c.pos.x = -40
