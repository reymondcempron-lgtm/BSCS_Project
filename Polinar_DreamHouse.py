from vpython import *


scene = canvas(title="<b>Mark Laurence Polinar_MY DREAM HOUSE</b>", width=1100, height=650)
scene.background = vector(0.53, 0.81, 0.92)
scene.ambient = vector(0.55, 0.55, 0.55)
scene.center = vector(4, 3.8, 2)
scene.forward = vector(-0.5, -0.18, -1)
scene.autoscale = False
scene.range = 12
scene.caption = ("Right-drag: rotate    Scroll: zoom    Shift+drag: pan\n\n")


WHITE    = vector(0.95, 0.95, 0.93)
DARK     = vector(0.20, 0.22, 0.26)
DARK_LT  = vector(0.30, 0.32, 0.36)
ROOF     = vector(0.28, 0.31, 0.36)
ROOF_TOP = vector(0.85, 0.86, 0.88)
WOOD     = vector(0.65, 0.40, 0.20)
WOOD_D   = vector(0.45, 0.26, 0.12)
WOOD_L   = vector(0.76, 0.58, 0.38)
STONE    = vector(0.63, 0.62, 0.60)
CONCRETE = vector(0.55, 0.55, 0.56)
FRAME    = vector(0.07, 0.07, 0.08)
WARM     = vector(1.00, 0.82, 0.50)
GLASS    = vector(0.70, 0.85, 0.95)
GRASS    = vector(0.30, 0.60, 0.22)
GRASS2   = vector(0.36, 0.66, 0.28)
HEDGE    = vector(0.15, 0.42, 0.15)
BUSH     = vector(0.20, 0.50, 0.20)
LEAF     = vector(0.18, 0.52, 0.20)
TRUNK    = vector(0.40, 0.27, 0.15)
LAMP     = vector(1.00, 0.92, 0.55)


def block(x0, x1, y0, y1, z0, z1, col, opac=1):
    return box(pos=vector((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
               size=vector(x1 - x0, y1 - y0, z1 - z0),
               color=col, opacity=opac)


def window(x0, x1, y0, y1, z, cols, rows):
    block(x0, x1, y0, y1, z, z + 0.03, WARM)
    block(x0, x1, y0, y1, z + 0.03, z + 0.06, GLASS, 0.35)
    t = 0.08
    block(x0, x1, y0, y0 + t, z, z + 0.10, FRAME)
    block(x0, x1, y1 - t, y1, z, z + 0.10, FRAME)
    block(x0, x0 + t, y0, y1, z, z + 0.10, FRAME)
    block(x1 - t, x1, y0, y1, z, z + 0.10, FRAME)
    for i in range(1, cols):
        x = x0 + (x1 - x0) * i / cols
        block(x - 0.03, x + 0.03, y0, y1, z, z + 0.10, FRAME)
    for j in range(1, rows):
        y = y0 + (y1 - y0) * j / rows
        block(x0, x1, y - 0.03, y + 0.03, z, z + 0.10, FRAME)


def side_window(xf, z0, z1, y0, y1):
    block(xf, xf + 0.04, y0, y1, z0, z1, WARM)
    block(xf + 0.04, xf + 0.07, y0, y1, z0, z1, GLASS, 0.35)
    t = 0.07
    block(xf, xf + 0.10, y0, y0 + t, z0, z1, FRAME)
    block(xf, xf + 0.10, y1 - t, y1, z0, z1, FRAME)
    block(xf, xf + 0.10, y0, y1, z0, z0 + t, FRAME)
    block(xf, xf + 0.10, y0, y1, z1 - t, z1, FRAME)
    ym = (y0 + y1) / 2
    block(xf, xf + 0.10, ym - 0.03, ym + 0.03, z0, z1, FRAME)


def slats(x0, x1, y0, y1, z, step=0.22):
    y = y0 + step
    while y < y1:
        block(x0, x1, y, y + 0.03, z, z + 0.02, WOOD_D)
        y = y + step


def bollard_light(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 0.7, 0), radius=0.09, color=DARK)
    sphere(pos=vector(x, 0.8, z), radius=0.13, color=LAMP)


def tree(x, z, height):
    cylinder(pos=vector(x, -0.7, z), axis=vector(0, height, 0), radius=0.25, color=TRUNK)
    sphere(pos=vector(x, height + 1.0, z), radius=2.0, color=LEAF)
    sphere(pos=vector(x + 1.1, height + 0.4, z + 0.3), radius=1.4, color=BUSH)
    sphere(pos=vector(x - 1.0, height + 0.5, z - 0.4), radius=1.4, color=BUSH)


def pot(x, z):
    cylinder(pos=vector(x, 0.1, z), axis=vector(0, 0.6, 0), radius=0.3, color=DARK)
    sphere(pos=vector(x, 1.0, z), radius=0.45, color=BUSH)


block(-45, 45, -1.0, -0.7, -45, 45, GRASS2)
block(-11.5, 19.5, -0.7, -0.1, -6, 9, CONCRETE)
block(-11.0, 19.0, -0.1, 0.0, -5.5, 8.5, GRASS)


block(-11.5, 9.1, 0, 0.2, 8.5, 9, CONCRETE)
block(13.9, 19.5, 0, 0.2, 8.5, 9, CONCRETE)
block(-11.5, 19.5, 0, 0.2, -6, -5.5, CONCRETE)
block(-11.5, -11, 0, 0.2, -5.5, 8.5, CONCRETE)
block(19.0, 19.5, 0, 0.2, -5.5, 8.5, CONCRETE)


block(-7, 3, 0, 0.1, 1.0, 8.2, WOOD_L)
x = -6.75
while x < 3:
    block(x, x + 0.03, 0.1, 0.105, 1.0, 8.2, WOOD_D)
    x = x + 0.45


block(-4.0, -1.2, 0, 3.2, -4, 2.0, WHITE)
block(1.2, 8.0, 0, 3.2, -4, 2.0, WHITE)
block(-1.2, 1.2, 0, 3.2, -4, 0.0, WARM)


block(-4.0, -2.5, 0, 3.2, 2.0, 2.1, WOOD)
slats(-4.0, -2.5, 0, 3.2, 2.1)


block(-1.2, 1.2, 0, 3.1, 1.0, 1.04, GLASS, 0.30)
block(-1.2, 1.2, 3.1, 3.2, 0.0, 1.1, FRAME)
block(-1.2, -1.12, 0, 3.1, 1.0, 1.1, FRAME)
block(1.12, 1.2, 0, 3.1, 1.0, 1.1, FRAME)
block(-0.04, 0.04, 0, 3.1, 1.0, 1.1, FRAME)
block(-1.2, 1.2, 0.0, 0.05, 0.0, 1.0, vector(0.8, 0.75, 0.65))
sphere(pos=vector(0.25, 1.1, 1.08), radius=0.04, color=DARK)

block(-0.6, 0.6, 0.55, 0.62, 0.3, 0.9, WOOD)
block(-0.05, 0.05, 0.05, 0.55, 0.55, 0.65, WOOD_D)
block(-1.15, -0.5, 0.05, 2.2, 0.0, 0.4, vector(0.80, 0.70, 0.50))
cylinder(pos=vector(0, 3.1, 0.6), axis=vector(0, -0.7, 0), radius=0.01, color=DARK)
sphere(pos=vector(0, 2.35, 0.6), radius=0.14, color=LAMP)


block(1.2, 2.0, 0, 3.2, 3.2, 4.0, WHITE)


block(2.0, 4.8, 0, 3.2, 2.0, 2.1, WOOD)
slats(2.0, 4.8, 0, 3.2, 2.1)


block(4.8, 8.0, 0, 3.2, 2.0, 2.1, STONE)
window(5.4, 6.0, 0.9, 2.6, 2.1, 1, 2)
window(6.6, 7.2, 0.9, 2.6, 2.1, 1, 2)


block(8.0, 8.1, 0, 3.2, -4, 2.0, STONE)


block(-1.9, -1.7, 2.0, 2.3, 2.0, 2.1, DARK)
sphere(pos=vector(-1.8, 2.15, 2.15), radius=0.1, color=LAMP)
block(2.95, 3.15, 2.0, 2.3, 2.1, 2.2, DARK)
sphere(pos=vector(3.05, 2.15, 2.25), radius=0.1, color=LAMP)


block(-10.0, -7.5, 0, 4.6, -3, 2.5, WHITE)
window(-9.6, -8.0, 0.4, 1.8, 2.5, 1, 1)
window(-9.6, -8.0, 2.6, 4.2, 2.5, 1, 2)
block(-10.0, -7.5, 2.0, 2.15, 2.5, 3.5, WHITE)
block(-10.0, -7.5, 2.15, 3.1, 3.45, 3.5, GLASS, 0.35)
block(-10.0, -7.5, 3.05, 3.12, 3.4, 3.55, FRAME)
block(-10.0, -7.5, 4.6, 4.75, -3.2, 2.7, DARK)


block(-7.5, -5.5, 0, 6.6, -4, 3.0, DARK)
x = -7.5
while x < -5.5:
    block(x, x + 0.04, 0, 6.6, 3.0, 3.03, DARK_LT)
    x = x + 0.25
block(-8.2, -3.8, 6.6, 6.9, -4.3, 3.4, ROOF)


block(-5.5, -4.0, 0, 6.6, -4, 2.55, WHITE)
window(-5.5, -4.0, 0.3, 6.2, 2.55, 2, 5)


block(-4.0, 8.3, 3.2, 3.7, -4.3, 4.0, WHITE)
block(-3.9, 8.2, 3.7, 3.76, 2.0, 3.9, WOOD_L)


block(-4.0, 8.0, 3.7, 8.0, -4, 2.0, WHITE)


window(-2.0, 6.5, 3.9, 5.6, 2.0, 6, 2)


window(-0.8, 3.8, 6.5, 7.5, 2.0, 4, 1)


side_window(8.0, -3.4, -0.4, 4.2, 6.0)


block(-4.0, 8.3, 3.76, 4.7, 3.93, 3.97, GLASS, 0.35)
block(-4.0, 8.3, 4.70, 4.78, 3.90, 4.00, vector(0.25, 0.26, 0.28))
block(8.26, 8.30, 3.76, 4.70, 2.0, 4.0, GLASS, 0.35)
for i in range(9):
    px = -3.9 + 1.5 * i
    block(px - 0.04, px + 0.04, 3.76, 4.75, 3.90, 4.00, vector(0.70, 0.70, 0.72))


block(6.9, 8.2, 3.76, 4.25, 2.4, 3.8, DARK)
sphere(pos=vector(7.2, 4.55, 3.0), radius=0.38, color=BUSH)
sphere(pos=vector(7.7, 4.60, 3.4), radius=0.40, color=LEAF)
sphere(pos=vector(7.5, 4.45, 2.7), radius=0.33, color=BUSH)
sphere(pos=vector(8.0, 4.50, 3.0), radius=0.30, color=LEAF)


block(-2.5, 7.0, 5.85, 5.90, 2.0, 3.8, WOOD)
block(-2.5, 7.0, 5.90, 6.20, 2.0, 3.8, WHITE)
block(-2.5, 7.0, 6.20, 6.28, 2.0, 3.8, DARK)
for lx in (-1.5, 0.5, 2.5, 4.5, 6.5):
    sphere(pos=vector(lx, 5.82, 3.3), radius=0.07, color=LAMP)


block(-4.6, 9.0, 7.95, 8.0, -4.9, 4.4, WOOD)
block(-5.0, 9.2, 8.0, 8.45, -5.2, 4.6, ROOF)
block(-4.8, 9.0, 8.45, 8.50, -5.0, 4.4, ROOF_TOP)
for lx in (-1.5, 0.0, 1.5, 3.0, 4.5, 6.0, 7.5):
    sphere(pos=vector(lx, 7.93, 3.4), radius=0.08, color=LAMP)


block(3.5, 8.5, 0, 0.7, 7.4, 8.2, HEDGE)
block(14.5, 19.0, 0, 0.7, 7.4, 8.2, HEDGE)
block(18.3, 19.0, 0, 0.7, -5.0, 7.4, HEDGE)
block(-11.0, -7.0, 0, 0.5, 8.0, 8.5, HEDGE)


ellipsoid(pos=vector(5.0, 1.1, 6.5), size=vector(1.6, 2.4, 1.6), color=BUSH)
ellipsoid(pos=vector(7.0, 1.0, 6.2), size=vector(1.5, 2.2, 1.5), color=HEDGE)
ellipsoid(pos=vector(8.2, 0.8, 5.5), size=vector(1.3, 1.8, 1.3), color=BUSH)
ellipsoid(pos=vector(15.8, 0.9, 5.0), size=vector(1.4, 2.0, 1.4), color=BUSH)
ellipsoid(pos=vector(17.2, 0.8, 4.2), size=vector(1.3, 1.8, 1.3), color=HEDGE)


for i in range(6):
    sx = 4.6 + 0.75 * i
    sphere(pos=vector(sx, 0.35, 3.0), radius=0.35, color=BUSH if i % 2 == 0 else LEAF)
for fx, fz in ((5.0, 3.3), (6.5, 3.3), (7.7, 3.2)):
    sphere(pos=vector(fx, 0.72, fz), radius=0.08, color=vector(1.0, 0.45, 0.6))


cylinder(pos=vector(-8.8, 0, 4.5), axis=vector(0, 3.2, 0), radius=0.13, color=TRUNK)
for i in range(8):
    a = i * pi / 4
    cone(pos=vector(-8.8, 3.2, 4.5),
         axis=vector(1.5 * cos(a), -0.6, 1.5 * sin(a)),
         radius=0.12, color=LEAF)
sphere(pos=vector(-8.8, 3.25, 4.5), radius=0.2, color=BUSH)


for px, pz in ((-9.8, 5.5), (-7.8, 5.6), (-9.6, 3.4), (-7.6, 3.6)):
    sphere(pos=vector(px, 0.3, pz), radius=0.3, color=BUSH)


pot(-2.0, 3.5)
pot(2.8, 3.0)


tree(-16, 2, 3.0)
tree(25, 1, 3.5)
tree(-14, -9, 3.5)
tree(24, -10, 3.0)
tree(-19, 12, 2.8)


for bx in (-6.0, -3.0, 0.0, 2.8):
    bollard_light(bx, 8.35)
bollard_light(8.6, 8.35)
bollard_light(14.5, 8.35)
bollard_light(18.6, 8.35)
bollard_light(-10.5, 8.35)


ellipsoid(pos=vector(-30, 25, -60), size=vector(22, 5, 7), color=color.white)
ellipsoid(pos=vector(-22, 27, -62), size=vector(14, 4, 6), color=color.white)
ellipsoid(pos=vector(25, 30, -70), size=vector(26, 6, 8), color=color.white)
ellipsoid(pos=vector(40, 24, -55), size=vector(16, 4, 6), color=color.white)


def sports_car(cx, cz):
    CAR      = vector(0.82, 0.05, 0.07)
    CAR_DARK = vector(0.05, 0.05, 0.06)
    CAR_GLS  = vector(0.10, 0.14, 0.20)
    SILVER   = vector(0.80, 0.80, 0.83)

    def part(dx0, dx1, y0, y1, dz0, dz1, col, opac=1):
        return block(cx + dx0, cx + dx1, y0, y1, cz + dz0, cz + dz1, col, opac)

    part(-0.90, 0.90, 0.15, 0.28, -2.1, 2.1, CAR_DARK)
    part(-0.95, 0.95, 0.28, 0.72, -2.2, 2.2, CAR)
    part(-0.90, 0.90, 0.72, 0.80, 0.7, 2.2, CAR)
    part(-0.90, 0.90, 0.72, 0.80, -2.2, -1.7, CAR)

    part(-0.78, 0.78, 0.72, 1.12, -1.0, 0.0, CAR_GLS, 0.85)
    part(-0.80, 0.80, 1.12, 1.18, -1.0, 0.0, CAR)
    for side in (-1, 1):
        px0 = 0.76 if side == 1 else -0.80
        part(px0, px0 + 0.04, 0.72, 1.12, -1.0, -0.9, CAR)
        part(px0, px0 + 0.04, 0.72, 1.12, -0.1, 0.0, CAR)

    windshield = box(pos=vector(cx, 0.95, cz + 0.35), size=vector(1.5, 0.04, 0.8),
                     color=CAR_GLS, opacity=0.85)
    windshield.rotate(angle=0.55, axis=vector(1, 0, 0), origin=windshield.pos)
    rear_glass = box(pos=vector(cx, 0.95, cz - 1.35), size=vector(1.4, 0.04, 0.8),
                     color=CAR_GLS, opacity=0.85)
    rear_glass.rotate(angle=-0.55, axis=vector(1, 0, 0), origin=rear_glass.pos)

    part(-0.15, 0.15, 0.80, 0.81, 0.7, 2.2, WHITE)
    part(-0.15, 0.15, 1.18, 1.19, -1.0, 0.0, WHITE)
    part(-0.15, 0.15, 0.80, 0.81, -2.2, -1.7, WHITE)

    part(-0.80, 0.80, 0.95, 0.99, -2.15, -1.90, CAR_DARK)
    part(-0.65, -0.60, 0.80, 0.95, -2.10, -2.00, CAR_DARK)
    part(0.60, 0.65, 0.80, 0.95, -2.10, -2.00, CAR_DARK)

    part(-0.85, -0.45, 0.55, 0.68, 2.18, 2.23, vector(1.0, 1.0, 0.85))
    part(0.45, 0.85, 0.55, 0.68, 2.18, 2.23, vector(1.0, 1.0, 0.85))
    part(-0.50, 0.50, 0.32, 0.50, 2.20, 2.26, CAR_DARK)
    part(-0.85, -0.35, 0.55, 0.68, -2.23, -2.18, vector(1.0, 0.25, 0.25))
    part(0.35, 0.85, 0.55, 0.68, -2.23, -2.18, vector(1.0, 0.25, 0.25))
    part(-0.25, 0.25, 0.38, 0.50, 2.26, 2.27, WHITE)

    part(0.95, 1.05, 0.85, 0.95, 0.20, 0.45, CAR)
    part(-1.05, -0.95, 0.85, 0.95, 0.20, 0.45, CAR)

    for ex in (-0.4, 0.4):
        cylinder(pos=vector(cx + ex, 0.30, cz - 2.2), axis=vector(0, 0, -0.1),
                 radius=0.06, color=SILVER)

    for wz in (1.35, -1.35):
        cylinder(pos=vector(cx - 1.0, 0.34, cz + wz), axis=vector(0.2, 0, 0),
                 radius=0.34, color=CAR_DARK)
        cylinder(pos=vector(cx + 0.8, 0.34, cz + wz), axis=vector(0.2, 0, 0),
                 radius=0.34, color=CAR_DARK)
        cylinder(pos=vector(cx - 1.03, 0.34, cz + wz), axis=vector(0.04, 0, 0),
                 radius=0.21, color=SILVER)
        cylinder(pos=vector(cx + 0.99, 0.34, cz + wz), axis=vector(0.04, 0, 0),
                 radius=0.21, color=SILVER)


block(8.3, 14.7, 0, 3.2, -4, 2.6, WHITE)
block(8.3, 9.1, 0, 3.2, 2.6, 2.7, STONE)
block(13.9, 14.7, 0, 3.2, 2.6, 2.7, WOOD)
slats(13.9, 14.7, 0, 3.2, 2.7)
block(9.1, 13.9, 2.5, 3.2, 2.6, 2.7, WOOD)
slats(9.1, 13.9, 2.5, 3.2, 2.7, 0.17)

block(9.05, 13.95, 0, 2.55, 2.6, 2.66, FRAME)
block(9.1, 13.9, 0, 2.5, 2.66, 2.72, vector(0.80, 0.82, 0.85))
y = 0.5
while y < 2.5:
    block(9.1, 13.9, y, y + 0.04, 2.72, 2.74, vector(0.45, 0.47, 0.50))
    y = y + 0.5
for i in range(4):
    gx = 9.3 + 1.15 * i
    block(gx, gx + 0.95, 1.9, 2.3, 2.72, 2.76, vector(0.15, 0.20, 0.28), 0.85)

block(8.3, 14.9, 3.25, 3.6, -4.3, 3.2, ROOF)
block(8.3, 14.9, 3.2, 3.25, 2.6, 3.2, WOOD)
block(8.4, 14.8, 3.6, 3.65, -4.2, 3.1, ROOF_TOP)
for lx in (9.6, 11.0, 12.4, 13.8):
    sphere(pos=vector(lx, 3.17, 2.9), radius=0.08, color=LAMP)

block(8.55, 8.75, 1.9, 2.2, 2.7, 2.8, DARK)
sphere(pos=vector(8.65, 2.05, 2.85), radius=0.1, color=LAMP)
block(14.25, 14.45, 1.9, 2.2, 2.7, 2.8, DARK)
sphere(pos=vector(14.35, 2.05, 2.85), radius=0.1, color=LAMP)

side_window(14.7, -2.2, -0.6, 0.9, 2.3)
side_window(14.7, 0.2, 1.8, 0.9, 2.3)

block(9.1, 13.9, -0.1, 0.06, 2.6, 9.0, vector(0.70, 0.70, 0.72))
zz = 3.5
while zz < 8.5:
    block(9.1, 13.9, 0.06, 0.065, zz, zz + 0.03, vector(0.45, 0.45, 0.47))
    zz = zz + 1.5

sports_car(11.5, 5.4)


def helicopter(cx, cz):
    HELI_W  = vector(0.98, 0.98, 1.00)
    STRIPE  = vector(0.10, 0.22, 0.55)
    HELI_GL = vector(0.12, 0.18, 0.26)
    METAL   = vector(0.20, 0.20, 0.22)
    RED     = vector(1.00, 0.20, 0.20)
    PAD     = vector(0.25, 0.27, 0.30)
    y0 = 8.56

    cylinder(pos=vector(cx, 8.5, cz), axis=vector(0, 0.06, 0), radius=2.6, color=PAD)
    cylinder(pos=vector(cx, 8.5, cz), axis=vector(0, 0.065, 0), radius=2.5, color=WHITE)
    cylinder(pos=vector(cx, 8.5, cz), axis=vector(0, 0.07, 0), radius=2.35, color=PAD)
    block(cx - 1.1, cx - 0.95, 8.57, 8.58, cz - 1.1, cz + 1.1, WHITE)
    block(cx + 0.95, cx + 1.1, 8.57, 8.58, cz - 1.1, cz + 1.1, WHITE)
    block(cx - 1.1, cx + 1.1, 8.57, 8.58, cz - 0.08, cz + 0.08, WHITE)
    for i in range(8):
        a = i * pi / 4
        sphere(pos=vector(cx + 2.42 * cos(a), 8.6, cz + 2.42 * sin(a)), radius=0.07, color=LAMP)

    ellipsoid(pos=vector(cx, y0 + 0.95, cz + 0.1), size=vector(1.6, 1.5, 2.7), color=HELI_W)
    ellipsoid(pos=vector(cx, y0 + 1.10, cz + 0.95), size=vector(1.35, 1.0, 1.5), color=HELI_GL, opacity=0.85)
    for s in (-1, 1):
        ellipsoid(pos=vector(cx + s * 0.70, y0 + 1.15, cz + 0.45), size=vector(0.30, 0.60, 1.1), color=HELI_GL)
        ellipsoid(pos=vector(cx + s * 0.70, y0 + 1.10, cz - 0.55), size=vector(0.30, 0.50, 0.8), color=HELI_GL)
        ellipsoid(pos=vector(cx + s * 0.69, y0 + 0.75, cz - 0.10), size=vector(0.20, 0.10, 2.4), color=STRIPE)
    sphere(pos=vector(cx, y0 + 0.60, cz + 1.35), radius=0.08, color=LAMP)

    ellipsoid(pos=vector(cx, y0 + 1.70, cz - 0.20), size=vector(0.9, 0.55, 1.6), color=HELI_W)
    cylinder(pos=vector(cx, y0 + 1.75, cz - 1.0), axis=vector(0, 0, -0.2), radius=0.10, color=METAL)
    sphere(pos=vector(cx, y0 + 2.0, cz - 0.7), radius=0.05, color=RED)

    cone(pos=vector(cx, y0 + 1.2, cz - 1.1), axis=vector(0, 0.15, -2.9), radius=0.38, color=HELI_W)
    cylinder(pos=vector(cx, y0 + 1.2, cz - 1.1), axis=vector(0, 0.05, -2.9), radius=0.04, color=STRIPE)
    fin = box(pos=vector(cx, y0 + 1.75, cz - 3.85), size=vector(0.06, 1.0, 0.55), color=HELI_W)
    fin.rotate(angle=-0.4, axis=vector(1, 0, 0), origin=fin.pos)
    block(cx - 0.55, cx + 0.55, y0 + 1.28, y0 + 1.32, cz - 3.90, cz - 3.40, HELI_W)
    block(cx - 0.55, cx - 0.50, y0 + 1.28, y0 + 1.42, cz - 3.90, cz - 3.40, STRIPE)
    block(cx + 0.50, cx + 0.55, y0 + 1.28, y0 + 1.42, cz - 3.90, cz - 3.40, STRIPE)
    cylinder(pos=vector(cx + 0.04, y0 + 1.95, cz - 4.0), axis=vector(0.06, 0, 0), radius=0.07, color=METAL)
    block(cx + 0.08, cx + 0.10, y0 + 1.45, y0 + 2.45, cz - 4.05, cz - 3.95, METAL)
    block(cx + 0.08, cx + 0.10, y0 + 1.90, y0 + 2.00, cz - 4.50, cz - 3.50, METAL)
    sphere(pos=vector(cx, y0 + 2.18, cz - 4.05), radius=0.06, color=RED)

    cylinder(pos=vector(cx, y0 + 1.9, cz - 0.2), axis=vector(0, 0.32, 0), radius=0.08, color=METAL)
    sphere(pos=vector(cx, y0 + 2.25, cz - 0.2), radius=0.18, color=METAL)
    block(cx - 3.2, cx + 3.2, y0 + 2.25, y0 + 2.29, cz - 0.31, cz - 0.09, METAL)
    block(cx - 0.11, cx + 0.11, y0 + 2.29, y0 + 2.33, cz - 3.4, cz + 3.0, METAL)
    block(cx - 3.2, cx - 2.75, y0 + 2.29, y0 + 2.295, cz - 0.31, cz - 0.09, RED)
    block(cx + 2.75, cx + 3.2, y0 + 2.29, y0 + 2.295, cz - 0.31, cz - 0.09, RED)
    block(cx - 0.11, cx + 0.11, y0 + 2.33, y0 + 2.335, cz - 3.4, cz - 2.95, RED)
    block(cx - 0.11, cx + 0.11, y0 + 2.33, y0 + 2.335, cz + 2.55, cz + 3.0, RED)

    for s in (-1, 1):
        cylinder(pos=vector(cx + s * 0.75, y0 + 0.06, cz - 1.5), axis=vector(0, 0, 3.1), radius=0.045, color=METAL)
        cylinder(pos=vector(cx + s * 0.75, y0 + 0.06, cz + 1.6), axis=vector(0, 0.3, 0.25), radius=0.045, color=METAL)
        cylinder(pos=vector(cx + s * 0.75, y0 + 0.06, cz + 0.6), axis=vector(-s * 0.25, 0.5, 0), radius=0.035, color=METAL)
        cylinder(pos=vector(cx + s * 0.75, y0 + 0.06, cz - 0.6), axis=vector(-s * 0.25, 0.5, 0), radius=0.035, color=METAL)
    cylinder(pos=vector(cx - 0.75, y0 + 0.08, cz + 0.6), axis=vector(1.5, 0, 0), radius=0.03, color=METAL)
    cylinder(pos=vector(cx - 0.75, y0 + 0.08, cz - 0.6), axis=vector(1.5, 0, 0), radius=0.03, color=METAL)


helicopter(2.5, -0.2)
while True:
    rate(60)