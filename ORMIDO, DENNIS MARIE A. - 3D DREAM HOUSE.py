from vpython import *
import random
random.seed(33)
scene.title = "Dream House 3D Vpython"
scene.width = 1200
scene.height = 680
CREAM = vec(0.88, 0.85, 0.78)
WHITE = vec(0.92, 0.91, 0.88)
STONEC = vec(0.46, 0.43, 0.40)
DARKM = vec(0.28, 0.28, 0.30)
BLACK = vec(0.07, 0.07, 0.08)
WOOD = vec(0.50, 0.30, 0.17)
WOOD_D = vec(0.33, 0.19, 0.11)
WOOD_L = vec(0.62, 0.40, 0.22)
GLASS = vec(0.60, 0.72, 0.80)
GLOW = vec(1.0, 0.80, 0.48)
GRASS = vec(0.56, 0.82, 0.38)
LEAF = vec(0.17, 0.46, 0.17)
LEAF2 = vec(0.30, 0.60, 0.22)
PINK = vec(0.92, 0.45, 0.62)
ROAD = vec(0.17, 0.17, 0.19)
PAVE = vec(0.62, 0.61, 0.60)
# ---- interior palette
STEEL = vec(0.72, 0.74, 0.76)
GOLD = vec(0.85, 0.68, 0.30)
MIRROR = vec(0.72, 0.85, 0.92)
FAB1 = vec(0.84, 0.80, 0.72)
FAB2 = vec(0.30, 0.42, 0.46)
FAB3 = vec(0.62, 0.32, 0.24)
NAVY = vec(0.16, 0.24, 0.36)
TILE = vec(0.90, 0.90, 0.88)
TILE_D = vec(0.62, 0.70, 0.72)

glow_items = []
lamp_lights = []
day_only = []
night_only = []
screen_items = []   # (object, day colour, night colour)
entry_parts = []    # Doors that open during WALK INSIDE
walk_active = False
walk_keys = set()
walk_pos = vec(-3.35, 1.70, 7.4)
walk_fy = 0.05
walk_yaw = 0.0
walk_pitch = 0.0

# ------------------------------------------------------------
# COLLISION + FLOOR DATA (used by the walkthrough)
# ------------------------------------------------------------
BLOCKS = []   # (x0,x1,z0,z1,y0,y1,fymin,fymax)
FLOORS = []   # (x0,x1,z0,z1,axis,a0,a1,ya,yb)  axis n=flat, z/x=ramp


def block(x0, x1, z0, z1, y0, y1, fymin=-99.0, fymax=99.0):
    BLOCKS.append((min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1),
                   y0, y1, fymin, fymax))


def floor_flat(x0, x1, z0, z1, y):
    FLOORS.append((min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1),
                   'n', 0.0, 1.0, y, y))


def floor_ramp(x0, x1, z0, z1, axis, a0, a1, ya, yb):
    FLOORS.append((min(x0, x1), max(x0, x1), min(z0, z1), max(z0, z1),
                   axis, a0, a1, ya, yb))


def slab(x0, x1, y0, y1, z0, z1, col, op=1.0, emi=False):
    return box(
        pos=vec((x0+x1)/2, (y0+y1)/2, (z0+z1)/2),
        size=vec(abs(x1-x0), abs(y1-y0), abs(z1-z0)),
        color=col,
        opacity=op,
        emissive=emi
    )


def tint(c, k):
    return vec(min(1.0, c.x*k), min(1.0, c.y*k), min(1.0, c.z*k))


def interior(*a, **k):
    # old dark "fake interior" plates are gone - real rooms exist now
    return None


def glass_frame(x0, x1, y0, y1, z, n, frame=BLACK, t=0.08):
    slab(x0, x1, y0, y1, z, z+0.04, GLASS, 0.22)
    w = (x1-x0)/n
    for i in range(n+1):
        x = x0+i*w
        slab(x-t, x+t, y0-t, y1+t,
             z-0.02, z+0.1, frame)
    slab(x0-t, x1+t, y0-t, y0+t,
         z-0.02, z+0.1, frame)
    slab(x0-t, x1+t, y1-t, y1+t,
         z-0.02, z+0.1, frame)


def win_x(a0, a1, y0, y1, z, n=2, t=0.045, frame=BLACK):
    """window sitting in a wall that runs along X (plane z = const)"""
    slab(a0, a1, y0, y1, z-0.015, z+0.015, GLASS, 0.22)
    w = (a1-a0)/n
    for i in range(n+1):
        x = a0+i*w
        slab(x-t, x+t, y0-t, y1+t, z-0.07, z+0.07, frame)
    slab(a0-t, a1+t, y0-t, y0+t, z-0.07, z+0.07, frame)
    slab(a0-t, a1+t, y1-t, y1+t, z-0.07, z+0.07, frame)


def win_z(a0, a1, y0, y1, x, n=2, t=0.045, frame=BLACK):
    """window sitting in a wall that runs along Z (plane x = const)"""
    slab(x-0.015, x+0.015, y0, y1, a0, a1, GLASS, 0.22)
    w = (a1-a0)/n
    for i in range(n+1):
        z = a0+i*w
        slab(x-0.07, x+0.07, y0-t, y1+t, z-t, z+t, frame)
    slab(x-0.07, x+0.07, y0-t, y0+t, a0-t, a1+t, frame)
    slab(x-0.07, x+0.07, y1-t, y1+t, a0-t, a1+t, frame)


def holed_wall_x(x0, x1, y0, y1, z0, z1, col, holes):
    """wall along X with rectangular openings (hx0,hx1,hy0,hy1)"""
    cx = x0
    for (hx0, hx1, hy0, hy1) in sorted(holes):
        if hx0 > cx:
            slab(cx, hx0, y0, y1, z0, z1, col)
        if hy0 > y0:
            slab(hx0, hx1, y0, hy0, z0, z1, col)
        if hy1 < y1:
            slab(hx0, hx1, hy1, y1, z0, z1, col)
        cx = hx1
    if cx < x1:
        slab(cx, x1, y0, y1, z0, z1, col)


def holed_wall_z(z0, z1, y0, y1, x0, x1, col, holes):
    """wall along Z with openings (hz0,hz1,hy0,hy1)"""
    cz = z0
    for (hz0, hz1, hy0, hy1) in sorted(holes):
        if hz0 > cz:
            slab(x0, x1, y0, y1, cz, hz0, col)
        if hy0 > y0:
            slab(x0, x1, y0, hy0, hz0, hz1, col)
        if hy1 < y1:
            slab(x0, x1, hy1, y1, hz0, hz1, col)
        cz = hz1
    if cz < z1:
        slab(x0, x1, y0, y1, cz, z1, col)


def slab_hole(x0, x1, y0, y1, z0, z1, col, hx0, hx1, hz0, hz1):
    slab(x0, hx0, y0, y1, z0, z1, col)
    slab(hx1, x1, y0, y1, z0, z1, col)
    slab(hx0, hx1, y0, y1, z0, hz0, col)
    slab(hx0, hx1, y0, y1, hz1, z1, col)


def curtains(x0, x1, y0, y1, z, n=4):
    w = (x1-x0)/n
    for i in range(n):
        if i % 2 == 0:
            slab(
                x0+i*w+0.05,
                x0+i*w+w*0.75,
                y0, y1,
                z, z+0.06,
                vec(0.95, 0.92, 0.86), 0.85
            )


def louvers(x0, x1, y0, y1, z,
            pitch=0.24, w=0.13, depth=0.22):
    n = int((x1-x0)/pitch)
    for i in range(n):
        x = x0+i*pitch
        slab(x, x+w, y0, y1, z, z+depth,
             WOOD if i % 3 else WOOD_L)


def stone(x0, x1, y0, y1, z0, z1):
    slab(x0, x1, y0, y1, z0, z1,
         vec(0.40, 0.37, 0.34))
    y = y0
    while y < y1-0.05:
        h = min(random.uniform(0.18, 0.32), y1-y)
        x = x0
        while x < x1-0.05:
            w = min(random.uniform(0.35, 1.0), x1-x)
            g = random.uniform(0.36, 0.60)
            slab(
                x+0.01, x+w-0.01,
                y+0.01, y+h-0.01,
                z1, z1+0.05,
                vec(g, g*0.95, g*0.88)
            )
            x += w
        y += h


def bonsai(x, y, z, s=1.0):
    cylinder(
        pos=vec(x, y, z),
        axis=vec(0.1*s, 0.7*s, 0),
        radius=0.07*s,
        color=WOOD_D
    )
    for dx, dy, r in (
        (-0.4, 0.8, 0.45),
        (0.3, 0.95, 0.5),
        (0.0, 1.2, 0.4)
    ):
        ellipsoid(
            pos=vec(x+dx*s, y+dy*s, z),
            length=r*2.2*s,
            height=r*1.0*s,
            width=r*1.8*s,
            color=vec(0.16, 0.48, 0.20)
        )


def palm(x, z, h=6.0, y0=0.0):
    cylinder(
        pos=vec(x, y0, z),
        axis=vec(0.2, h, 0),
        radius=0.22,
        color=vec(0.45, 0.36, 0.26)
    )
    for k in range(10):
        a = k*2*pi/10
        ellipsoid(
            pos=vec(
                x+0.2+cos(a)*1.3,
                y0+h,
                z+sin(a)*1.3
            ),
            length=3.2,
            height=0.12,
            width=0.7,
            axis=vec(cos(a), -0.35, sin(a)),
            color=vec(0.15, 0.50, 0.14)
        )
    for k in range(4):
        sphere(
            pos=vec(
                x+0.2+cos(k*1.6)*0.2,
                y0+h-0.3,
                z+sin(k*1.6)*0.2
            ),
            radius=0.22,
            color=vec(0.5, 0.35, 0.15)
        )


def tree(x, z, h, r, col=None):
    cylinder(
        pos=vec(x, 0, z),
        axis=vec(0, h, 0),
        radius=0.4,
        color=vec(0.28, 0.2, 0.14)
    )
    for _ in range(12):
        sphere(
            pos=vec(
                x+random.uniform(-r, r)*0.8,
                h+random.uniform(-0.8, r),
                z+random.uniform(-r, r)*0.8
            ),
            radius=random.uniform(1.3, 2.3)*r/3,
            color=col or vec(
                0.10, random.uniform(0.32, 0.46), 0.12
            )
        )


def plumeria(x, y, z, h=3.0, s=1.0):
    cylinder(
        pos=vec(x, y, z),
        axis=vec(0.2, h, 0.1),
        radius=0.12,
        color=vec(0.45, 0.38, 0.30)
    )
    for _ in range(10):
        sphere(
            pos=vec(
                x+random.uniform(-1.2, 1.2)*s,
                y+h+random.uniform(-0.2, 1.3),
                z+random.uniform(-0.8, 0.8)
            ),
            radius=random.uniform(0.35, 0.6)*s,
            color=vec(0.32, 0.62, 0.26)
        )


def shrubs(x0, x1, z0, z1, y, n, cols, rmin=0.22, rmax=0.5):
    for _ in range(n):
        sphere(
            pos=vec(
                random.uniform(x0, x1),
                y+random.uniform(0.1, 0.5),
                random.uniform(z0, z1)
            ),
            radius=random.uniform(rmin, rmax),
            color=random.choice(cols)
        )


def grass_tuft(x, z, y=0.0, s=1.0,
               col=vec(0.28, 0.55, 0.22)):
    for k in range(5):
        a = k*2*pi/5
        cone(
            pos=vec(x, y, z),
            axis=vec(cos(a)*0.4*s, 0.9*s, sin(a)*0.4*s),
            radius=0.04*s,
            color=col
        )


def agave(x, z, s=1.0, y=0.0):
    for k in range(9):
        a = k*2*pi/9
        cone(
            pos=vec(x, y+0.1, z),
            axis=vec(cos(a)*0.9*s, 1.0*s, sin(a)*0.9*s),
            radius=0.07*s,
            color=vec(0.35, 0.55, 0.30)
        )


def lamp(x, z, h=0.9):
    slab(x-0.1, x+0.1, 0, h, z-0.1, z+0.1,
         vec(0.18, 0.16, 0.14))
    top = slab(
        x-0.14, x+0.14, h, h+0.22,
        z-0.14, z+0.14,
        vec(0.85, 0.82, 0.70)
    )
    glow_items.append(
        (top, vec(0.85, 0.82, 0.70), False, 1.0)
    )


def downlight(x, y, z):
    s = sphere(
        pos=vec(x, y, z),
        radius=0.09,
        color=vec(0.8, 0.8, 0.75)
    )
    glow_items.append(
        (s, vec(0.8, 0.8, 0.75), False, 1.0)
    )


# ------------------------------------------------------------
# Rotatable "frame" so furniture can face any direction
# local +z = the way the furniture faces, local +x = its width
# rot 0 faces +z (front yard), 1 faces +x, 2 faces -z, 3 faces -x
# ------------------------------------------------------------
class F:
    def __init__(s, x, z, rot=0, y=0.0):
        s.x = x
        s.z = z
        s.y = y
        s.r = rot % 4
        s.ax, s.az, s.bx, s.bz = {
            0: (1, 0, 0, 1),
            1: (0, -1, 1, 0),
            2: (-1, 0, 0, -1),
            3: (0, 1, -1, 0)}[s.r]

    def w(s, lx, lz):
        return (s.x + lx*s.ax + lz*s.bx,
                s.z + lx*s.az + lz*s.bz)

    def b(s, lx0, lx1, y0, y1, lz0, lz1, col,
          op=1.0, emi=False, solid=False):
        xa, za = s.w(lx0, lz0)
        xb, zb = s.w(lx1, lz1)
        if solid:
            block(xa, xb, za, zb, s.y+y0, s.y+y1, s.y-0.6, s.y+0.8)
        return slab(min(xa, xb), max(xa, xb), s.y+y0, s.y+y1,
                    min(za, zb), max(za, zb), col, op, emi)

    def blk(s, lx0, lx1, y0, y1, lz0, lz1):
        xa, za = s.w(lx0, lz0)
        xb, zb = s.w(lx1, lz1)
        block(xa, xb, za, zb, s.y+y0, s.y+y1, s.y-0.6, s.y+0.8)

    def cyl(s, lx, lz, y0, h, r, col, op=1.0, emi=False):
        x, z = s.w(lx, lz)
        return cylinder(pos=vec(x, s.y+y0, z), axis=vec(0, h, 0),
                        radius=r, color=col, opacity=op, emissive=emi)

    def sph(s, lx, y, lz, r, col, op=1.0, emi=False):
        x, z = s.w(lx, lz)
        return sphere(pos=vec(x, s.y+y, z), radius=r, color=col,
                      opacity=op, emissive=emi)

    def cn(s, lx, lz, y0, h, r, col):
        x, z = s.w(lx, lz)
        return cone(pos=vec(x, s.y+y0, z), axis=vec(0, h, 0),
                    radius=r, color=col)

    def ell(s, lx, y, lz, sx, sy, sz, col):
        x, z = s.w(lx, lz)
        if s.r % 2 == 1:
            sx, sz = sz, sx
        return ellipsoid(pos=vec(x, s.y+y, z), length=sx, height=sy,
                         width=sz, color=col)


def glow(o, dc):
    glow_items.append((o, dc, False, 1.0))
    return o


# ============================================================
# EXTERIOR  (same as before, with real windows cut in)
# ============================================================
LX0, LX1, LZ0, LZ1 = -19.0, 17.0, -14.0, 22.0
slab(LX0-0.5, LX1+0.5, -0.9, 0.0,
     LZ0-0.5, LZ1+0.5, vec(0.34, 0.31, 0.28))
slab(LX0, LX1, 0.0, 0.05, LZ0, LZ1,
     vec(0.83, 0.80, 0.73))
for i in range(1, 24):
    slab(LX0, LX1, 0.05, 0.055,
         LZ0+i*1.5-0.02, LZ0+i*1.5+0.02,
         vec(0.70, 0.67, 0.60))
    slab(LX0+i*1.5-0.02, LX0+i*1.5+0.02,
         0.05, 0.055, LZ0, LZ1,
         vec(0.70, 0.67, 0.60))
LAWN = (-1.0, 14.0, 7.0, 15.2)
slab(
    LAWN[0]-0.25, LAWN[1]+0.25, 0.0, 0.14,
    LAWN[2]-0.25, LAWN[3]+0.25,
    vec(0.50, 0.46, 0.41)
)
slab(
    LAWN[0], LAWN[1], 0.14, 0.17,
    LAWN[2], LAWN[3], GRASS
)
for i in range(8):
    slab(
        LAWN[0], LAWN[1], 0.17, 0.175,
        LAWN[2]+i*1.0, LAWN[2]+i*1.0+0.5,
        vec(0.63, 0.87, 0.46)
    )
slab(-13.5, -7.0, 0.05, 0.1, 4.5, LZ1, PAVE)
for i in range(32):
    slab(
        -13.5, -7.0, 0.1, 0.11,
        4.6+i*0.55, 4.63+i*0.55,
        vec(0.48, 0.47, 0.46)
    )
for i in range(8):
    slab(
        -13.5+i*0.83, -13.47+i*0.83,
        0.1, 0.11, 4.5, LZ1,
        vec(0.48, 0.47, 0.46)
    )
slab(-4.8, -1.9, 0.05, 0.1, 4.5, LZ1,
     vec(0.90, 0.90, 0.88))
for _ in range(260):
    sphere(
        pos=vec(
            random.uniform(-4.8, -1.9),
            0.12,
            random.uniform(4.6, LZ1-0.2)
        ),
        radius=random.uniform(0.04, 0.09),
        color=random.choice([
            vec(0.92, 0.92, 0.9),
            vec(0.8, 0.8, 0.78)
        ])
    )
for i in range(15):
    slab(-4.0, -2.8, 0.1, 0.16,
         5.0+i*1.12, 5.8+i*1.12,
         vec(0.66, 0.64, 0.60))
WZ = 4.5
stone(-14.5, -13.4, 0, 4.7, 3.4, WZ)
slab(-13.4, -6.0, 3.5, 4.2, 3.4, WZ, WHITE)
slab(-13.4, -7.0, 0, 3.5, 3.6, WZ-0.1,
     vec(0.32, 0.32, 0.34))
for gx0, gx1 in ((-13.3, -10.25), (-10.15, -7.1)):
    slab(gx0, gx1, 0.14, 3.4, WZ-0.1, WZ, DARKM)
    for k in range(4):
        slab(
            gx0+0.3+k*0.7,
            gx0+0.34+k*0.7,
            0.3, 3.2, WZ, WZ+0.03,
            vec(0.22, 0.22, 0.24)
        )
    off = 1.4 if gx0 < -11 else 0.3
    slab(
        gx0+off, gx0+off+0.1,
        1.4, 2.0, WZ, WZ+0.06,
        vec(0.6, 0.6, 0.55)
    )
slab(-7.0, -6.0, 0, 3.5, 3.4, WZ, WHITE)
slab(-13.4, -6.0, 3.2, 3.5,
     WZ-0.05, WZ+0.08,
     vec(0.80, 0.78, 0.72))
stone(-6.0, -4.9, 0, 3.0, 3.4, WZ-0.1)
slab(-6.0, -4.9, 3.0, 3.5, 3.4, WZ-0.1, WHITE)
# Front entry
slab(-4.9, -4.47, 0, 3.5, 3.2, WZ-0.4, vec(0.60, 0.57, 0.52))
slab(-2.47, -1.8, 0, 3.5, 3.2, WZ-0.4, vec(0.60, 0.57, 0.52))
slab(-4.47, -2.47, 3.13, 3.5, 3.2, WZ-0.4, vec(0.60, 0.57, 0.52))
entry_parts.append(slab(-4.4, -2.5, 0, 3.13, WZ-0.4, WZ-0.3,
                        vec(0.40, 0.25, 0.17)))
for k in range(5):
    entry_parts.append(slab(-4.3, -2.6,
                            0.5+k*0.5, 0.53+k*0.5,
                            WZ-0.3, WZ-0.25, vec(0.28, 0.17, 0.12)))
entry_parts.append(slab(-3.4, -3.3, 1.2, 1.7,
                        WZ-0.3, WZ-0.2, vec(0.7, 0.7, 0.65)))
stone(-2.5, -1.8, 0, 4.2, 3.0, WZ)
slab(-5.7, -1.4, 4.2, 4.45, 1.8, WZ+0.5,
     vec(0.20, 0.17, 0.15))
slab(-5.5, -1.6, 4.1, 4.2, 1.8, WZ+0.4, WOOD_L)
slab(-5.7, -5.5, 0, 4.2, WZ+0.2, WZ+0.4, BLACK)
downlight(-4.6, 4.05, WZ+0.1)
downlight(-3.0, 4.05, WZ+0.1)
for _ in range(34):
    sphere(
        pos=vec(
            random.uniform(-7.6, -5.2),
            random.uniform(4.4, 5.4),
            random.uniform(3.0, 4.2)
        ),
        radius=random.uniform(0.15, 0.3),
        color=random.choice([
            PINK,
            vec(0.85, 0.30, 0.55),
            vec(0.4, 0.62, 0.3)
        ])
    )
slab(-7.6, -5.2, 4.2, 4.5, 2.6, 4.4,
     vec(0.55, 0.52, 0.48))

# ---- front facade, right side: now with real windows
WIN_A = (3.4, 5.5, 0.9, 2.5)      # study window
WIN_B = (7.5, 12.0, 0.9, 2.6)     # dining window
holed_wall_x(-1.8, 6.0, 0, 3.5, 3.0, WZ, WHITE, [WIN_A])
win_x(3.4, 5.5, 0.9, 2.5, 3.75, 2)
slab(3.3, 5.6, 0.82, 0.9, 3.0, WZ+0.1, CREAM)
slab(-1.8, 6.0, 2.55, 2.95,
     WZ-0.02, WZ+0.06,
     vec(0.38, 0.27, 0.20))
slab(-1.8, 6.0, 3.30, 3.5,
     WZ-0.02, WZ+0.05,
     vec(0.60, 0.58, 0.52))
slab(-1.7, -1.55, 3.35, 3.8,
     WZ-0.1, WZ,
     vec(0.55, 0.5, 0.45))
stone(5.9, 6.8, 0, 4.1, 3.0, WZ)
holed_wall_x(6.8, 13.0, 0, 3.5, 3.0, WZ,
             vec(0.78, 0.76, 0.72), [WIN_B])
win_x(7.5, 12.0, 0.9, 2.6, 3.75, 4)
slab(7.4, 12.1, 0.82, 0.9, 3.0, WZ+0.1, CREAM)
for k in range(7):
    lx = 6.8+k*0.9
    if 7.45 < lx < 12.05:
        slab(lx, lx+0.03, 0.2, 0.9, WZ, WZ+0.03,
             vec(0.58, 0.57, 0.55))
        slab(lx, lx+0.03, 2.6, 3.3, WZ, WZ+0.03,
             vec(0.58, 0.57, 0.55))
    else:
        slab(lx, lx+0.03, 0.2, 3.3, WZ, WZ+0.03,
             vec(0.58, 0.57, 0.55))
slab(6.8, 13.0, 3.2, 3.5,
     WZ-0.05, WZ+0.06,
     vec(0.70, 0.68, 0.64))
slab(12.0, 12.2, 0.2, 3.3,
     WZ, WZ+0.03,
     vec(0.5, 0.5, 0.5))

# ---- hollow ground-floor shell with windows on every side
HOUSE_WALL = vec(0.88, 0.85, 0.78)
STAIR_HOLE = (5.6, 8.6, -7.0, -0.8)     # x0,x1,z0,z1 of the main stair well
slab(-14, 13, 0.0, 0.21, -12, 2.8, vec(0.67, 0.61, 0.53))      # floor
slab_hole(-14, 13, 4.12, 4.4, -12, 2.8, HOUSE_WALL, *STAIR_HOLE)  # ceiling
holed_wall_z(-12, 2.8, 0.2, 4.13, -14, -13.72, HOUSE_WALL,
             [(-7.8, -5.0, 0.9, 3.2), (-3.4, -0.4, 0.9, 3.2)])
win_z(-7.8, -5.0, 0.9, 3.2, -13.86, 2)
win_z(-3.4, -0.4, 0.9, 3.2, -13.86, 2)
holed_wall_z(-12, 2.8, 0.2, 4.13, 12.72, 13, HOUSE_WALL,
             [(-9.6, -6.4, 1.35, 3.0), (-3.4, -0.4, 0.9, 3.0)])
win_z(-9.6, -6.4, 1.35, 3.0, 12.86, 2)
win_z(-3.4, -0.4, 0.9, 3.0, 12.86, 2)
holed_wall_x(-14, 13, 0.2, 4.13, -12, -11.72, HOUSE_WALL,
             [(-3.7, -2.1, 2.1, 3.0), (0.6, 3.4, 1.0, 2.8), (7.3, 9.9, 1.35, 2.6)])
win_x(-3.7, -2.1, 2.1, 3.0, -11.86, 2)
win_x(0.6, 3.4, 1.0, 2.8, -11.86, 3)
win_x(7.3, 9.9, 1.35, 2.6, -11.86, 2)
# front wall (door gap x -4.45 .. -2.48)
slab(-14, -4.45, 0.2, 4.12, 2.58, 2.8, HOUSE_WALL)
holed_wall_x(-2.48, 13, 0.2, 3.58, 2.58, 2.8, HOUSE_WALL, [WIN_A, WIN_B])
slab(-4.45, -2.48, 3.15, 4.12, 2.58, 2.8, HOUSE_WALL)
slab(-2.48, 13, 4.11, 4.4, 2.58, 2.8, HOUSE_WALL)
# clerestory glass band above the front wall (light from the front)
for x0, x1, n in (
    (-1.4, 2.4, 3),
    (2.8, 6.2, 3),
    (6.6, 12.8, 5)
):
    glass_frame(
        x0, x1, 3.65, 4.15,
        2.75, n, BLACK, 0.05
    )

# ============================================================
# TOWER (left, double height) - now a real lounge + mezzanine
# ============================================================
slab(-11.3, -10.6, 4.4, 11.4, -3, 1.0, WHITE)
slab(-4.5, -3.6, 4.4, 9.8, -3, 1.0, WHITE)
slab(-11.3, -3.6, 4.4, 5.2, -9, 1.8,
     vec(0.28, 0.26, 0.25))
slab(-11.3, -3.6, 5.2, 5.7, -9, -0.1, vec(0.46, 0.32, 0.20))   # lounge floor
slab(-11.3, -5.5, 11.2, 11.5, -5.5, 1.2, WHITE)                # roof (lounge part)
slab(-11.3, -5.5, 12.95, 13.1, -9, -5.5, WHITE)                # roof raised over the stairs
slab(-11.3, -5.5, 11.4, 12.95, -9.20, -8.96, WHITE)            # back wall up to the raised roof
slab(-11.4, -11.3, 11.4, 12.95, -9, -5.5, WHITE)               # left wall up to the raised roof
slab(-11.3, -5.5, 11.5, 12.95, -5.55, -5.5, WHITE)             # side wall of the raised part
# front: wood louvres in front of a real glass wall
slab(-10.6, -4.5, 5.7, 11.2, -0.12, -0.04, GLASS, 0.26)
slab(-10.6, -4.5, 5.2, 5.7, -0.15, 0.12, vec(0.25, 0.16, 0.10))
slab(-10.6, -4.5, 8.45, 8.55, -0.14, -0.02, BLACK)
louvers(
    -10.6, -4.5, 5.3, 11.1,
    0.15, 0.24, 0.13, 0.22
)
for x in (-10.6, -8.6, -6.6, -4.55):
    slab(
        x-0.05, x+0.05, 5.2, 11.2,
        0.05, 0.42, vec(0.25, 0.16, 0.10)
    )
slab(-10.6, -4.5, 5.2, 5.35,
     0.05, 0.42, vec(0.25, 0.16, 0.10))
slab(-10.6, -4.5, 11.05, 11.2,
     0.05, 0.42, vec(0.25, 0.16, 0.10))
slab(-10.5, -5.5, 11.4, 12.0, -3, 0.9,
     vec(0.30, 0.50, 0.25))
for x in [-10.3+i*0.5 for i in range(10)]:
    sphere(
        pos=vec(x, 12.1, 0.4),
        radius=0.3,
        color=LEAF2
    )
bonsai(-9.3, 12.0, -0.3, 1.4)
# left wall with a tall window
holed_wall_z(-9, 1.0, 4.4, 11.4, -11.4, -11.3, WHITE,
             [(-8.0, -4.4, 6.3, 10.3)])
win_z(-8.0, -4.4, 6.3, 10.3, -11.35, 3)
# right wall of tower (door to the courtyard bridge at z -6.4 .. -5.0)
slab(-3.7, -3.6, 5.7, 9.8, -9, -8.5, WHITE)
slab(-3.7, -3.6, 5.7, 9.8, -7.2, -3.0, WHITE)
slab(-3.7, -3.6, 8.05, 9.8, -8.5, -7.2, WHITE)
# courtyard glass rails (front + back)
slab(-3.6, -1.2, 5.7, 6.7, -0.06, 0.0, GLASS, 0.28)
slab(-3.6, -1.2, 5.7, 6.7, -9.0, -8.94, GLASS, 0.28)

# ---- courtyard strip between tower and the right wing
slab(-3.6, -1.2, 4.4, 5.2, -9, 1.8,
     vec(0.28, 0.26, 0.25))
slab(-3.6, -1.2, 5.2, 5.7, -9, 0.0, vec(0.52, 0.49, 0.44))
slab(-3.6, -1.7, 5.2, 6.2, -1.0, 1.2,
     vec(0.50, 0.45, 0.38))
for _ in range(14):
    sphere(
        pos=vec(
            random.uniform(-3.5, -1.8),
            random.uniform(6.3, 6.6),
            random.uniform(-0.5, 1.0)
        ),
        radius=0.3,
        color=LEAF
    )
plumeria(-2.6, 6.2, -0.2, 3.2, 1.2)
stone(-1.6, -1.2, 4.4, 10.0, 0.0, 1.2)

# ============================================================
# RIGHT WING (second floor) + roof terrace + sky room
# ============================================================
HOLE = STAIR_HOLE
slab_hole(-1.2, 13.3, 4.4, 5.7, -12, 3.0, WHITE, *HOLE)
slab_hole(-1.2, 13.3, 4.4, 4.6, -12, 3.0, vec(0.30, 0.28, 0.27), *HOLE)
slab(-1.2, 13.3, 5.7, 6.6, 2.9, 3.0,
     vec(0.7, 0.85, 0.92), 0.3)
slab(-1.2, 13.3, 6.55, 6.62,
     2.88, 3.04,
     vec(0.8, 0.8, 0.8))
for k in range(12):
    slab(
        -1.2+k*1.21,
        -1.15+k*1.21,
        5.7, 6.6, 2.92, 2.98,
        vec(0.8, 0.8, 0.8)
    )
glass_frame(-1.1, 3.8, 5.7, 8.2, 0.0, 3, BLACK, 0.08)
curtains(-1.1, 3.8, 5.7, 8.2, -0.3, 6)
glass_frame(3.9, 11.3, 5.7, 8.2, 0.0, 4, BLACK, 0.08)
slab(11.3, 13.3, 4.6, 8.2, -9, 0.6, WHITE)
# left wall of the wing, with the door to the courtyard (z -6.4 .. -5.0)
slab(-1.2, -1.1, 5.7, 8.2, -9, -8.5, WHITE)
slab(-1.2, -1.1, 5.7, 8.2, -7.2, 0.6, WHITE)
slab(-1.2, -1.1, 8.05, 8.2, -8.5, -7.2, WHITE)
slab(4.2, 6.2, 5.7, 6.1, 0.3, 1.5,
     vec(0.35, 0.34, 0.33))
bonsai(5.2, 6.1, 0.9, 1.3)
slab(-1.2, 13.3, 8.2, 9.8, -10, 2.4, WHITE)
slab(-1.2, 13.3, 8.2, 8.35, 2.4, 2.45,
     vec(0.30, 0.28, 0.27))
for x in range(0, 14, 2):
    downlight(x-0.2, 8.1, 1.5)
slab(5.6, 13.3, 9.8, 10.1, 0, 2.2,
     vec(0.40, 0.38, 0.35))
shrubs(
    5.7, 13.2, 0.2, 2.1, 10.0, 60,
    [LEAF, LEAF2, vec(0.2, 0.5, 0.2)],
    0.2, 0.4
)
slab(-1.2, 3.0, 9.8, 10.1, 0, 1.2,
     vec(0.40, 0.38, 0.35))
shrubs(-1.1, 2.9, 0.1, 1.1, 10.0, 25,
       [LEAF, LEAF2], 0.2, 0.4)
# sky room floor (cantilevers into the tower, joins the bridge)
slab(-5.3, -1.2, 9.4, 9.8, -8.55, 1.0,
     vec(0.88, 0.86, 0.80))
glass_frame(-4.8, 5.6, 9.8, 12.9, -0.5, 6, BLACK, 0.07)
curtains(-4.8, 5.6, 9.8, 12.7, -0.62, 8)
shrubs(
    -1.5, 5.5, -0.3, 0.9, 9.8, 45,
    [LEAF, LEAF2, PINK,
     vec(0.95, 0.55, 0.2),
     vec(0.9, 0.3, 0.3)],
    0.2, 0.4
)
bonsai(5.8, 9.8, 0.5, 1.4)
sphere(
    pos=vec(6.3, 10.9, 0.5),
    radius=0.8,
    color=vec(0.22, 0.50, 0.22)
)
for x in (-5.7, -1.5, 2.0, 5.2):
    slab(x-0.12, x+0.12, 9.8, 13.1,
         -0.3, 0.0, BLACK)
slab(-8.3, 9.7, 13.05, 13.6, -9, 4.0,
     vec(0.22, 0.15, 0.11))
slab(-8.3, 9.7, 12.95, 13.05, -9, 4.0, WOOD_L)
for i in range(30):
    slab(
        -8.3, 9.7, 12.93, 12.97,
        -9+i*0.44, -8.95+i*0.44,
        vec(0.38, 0.22, 0.12)
    )
slab(-8.3, 9.7, 12.2, 12.95, 2.8, 4.0, WOOD, 0.0)
slab(-8.3, 9.7, 13.2, 13.55, 3.9, 4.05,
     vec(0.15, 0.10, 0.08))
for x in range(-8, 10, 2):
    for z in (0.5, 2.2):
        downlight(x, 12.9, z)

# tower back wall + windows
slab(-11.3, -3.6, 4.4, 5.35, -9.20, -8.96, CREAM)
slab(-11.3, -3.6, 9.90, 11.4, -9.20, -8.96, WHITE)
for x0, x1 in (
    (-11.3, -10.91),
    (-8.55, -8.26),
    (-6.06, -5.76),
    (-3.95, -3.6)
):
    slab(x0, x1, 5.35, 9.90, -9.20, -8.96, CREAM)
for x0, x1, panes in (
    (-10.91, -8.55, 3),
    (-8.26, -6.06, 3),
    (-5.76, -3.95, 2)
):
    glass_frame(
        x0, x1, 5.35, 9.90,
        -9.24, panes, BLACK, 0.065
    )
slab(-11.3, -3.6, 9.86, 10.04,
     -9.27, -9.17, WOOD_D)
# wing back wall + windows
slab(-1.2, 11.3, 5.7, 6.17, -9.18, -8.92, WHITE)
slab(-1.2, 11.3, 7.95, 8.25, -9.18, -8.92, WHITE)
for x0, x1 in (
    (-1.2, -0.67),
    (3.50, 3.92),
    (6.64, 7.00),
    (10.83, 11.3)
):
    slab(x0, x1, 6.17, 7.95, -9.18, -8.92, WHITE)
for x0, x1 in (
    (-0.67, 3.50),
    (7.00, 10.83)
):
    glass_frame(
        x0, x1, 6.17, 7.95,
        -9.25, 4, BLACK, 0.06
    )
slab(3.92, 6.64, 6.17, 7.95,
     -9.20, -8.92, WOOD_D)
louvers(
    3.99, 6.59, 6.24, 7.88,
    -9.38, 0.24, 0.12, 0.16
)
# sky room rear wall + windows
slab(-5.45, 5.80, 9.8, 10.33,
     -8.65, -8.44, WHITE)
slab(-5.45, 5.80, 12.35, 12.99,
     -8.65, -8.44, WOOD_D)
for x0, x1 in (
    (-5.45, -4.89),
    (-1.32, -1.06),
    (2.15, 2.42),
    (5.18, 5.80)
):
    slab(x0, x1, 10.33, 12.35,
         -8.65, -8.44, CREAM)
for x0, x1, panes in (
    (-4.89, -1.32, 3),
    (-1.06, 2.15, 3),
    (2.42, 5.18, 3)
):
    glass_frame(
        x0, x1, 10.33, 12.35,
        -8.73, panes, BLACK, 0.055
    )
# sky room side walls (left one has a door onto the mezzanine bridge)
slab(-5.51, -5.30, 9.8, 12.95, -5.2, -2.4, WHITE)                 # TV wall only
slab(-5.44, -5.40, 9.82, 10.82, -5.5, -5.2, GLASS, 0.28)          # open side: glass balustrade
slab(-5.44, -5.40, 9.82, 10.82, -2.4, -0.62, GLASS, 0.28)
slab(-5.51, -5.30, 9.8, 12.95, -8.55, -8.45, WHITE)
slab(5.66, 5.87, 9.8, 12.95,
     -8.55, -0.62, WHITE)
slab(-5.52, 5.89, 12.93, 13.02,
     -8.72, -8.50, BLACK)
# mezzanine bridge (tower stair -> sky room)
slab(-6.2, -5.3, 9.6, 9.82, -8.96, -5.5, vec(0.46, 0.32, 0.20))
slab(-5.3, 5.66, 9.8, 9.82, -8.44, -0.55, vec(0.46, 0.32, 0.20))

palm(8.1, 2.0, 6.4, 3.4)
palm(12.3, 2.0, 5.0, 3.4)
palm(-15.0, 3.0, 10.5, 0.0)
for xx, zz in ((-9.5, 3.4), (-8.4, 3.0)):
    agave(xx, zz, 0.8, 3.5)
slab(-1.8, 12.5, 0.0, 0.3, WZ, WZ+2.0,
     vec(0.25, 0.17, 0.11))
shrubs(
    -1.6, 12.2, WZ+0.1, WZ+1.9, 0.2, 120,
    [LEAF, LEAF2, vec(0.2, 0.5, 0.2),
     PINK, vec(0.95, 0.65, 0.75),
     vec(0.95, 0.9, 0.9)],
    0.14, 0.32
)
for _ in range(30):
    grass_tuft(
        random.uniform(-1.5, 12),
        random.uniform(WZ+0.2, WZ+1.8),
        0.25,
        random.uniform(0.8, 1.5)
    )
for x in (0.5, 2.7, 4.6, 8.0, 10.2):
    agave(x, WZ+1.0, 0.7, 0.25)
for x, z in (
    (-0.5, 7.6),
    (1.2, 7.6),
    (6.7, 7.6),
    (9.6, 7.6),
    (12.2, 7.6)
):
    sphere(
        pos=vec(x, 0.77, z),
        radius=0.6,
        color=vec(0.18, 0.48, 0.18)
    )
cylinder(
    pos=vec(6.0, 0.17, 11.4),
    axis=vec(0, 0.5, 0),
    radius=1.9,
    color=vec(0.66, 0.63, 0.58)
)
cylinder(
    pos=vec(6.0, 0.62, 11.4),
    axis=vec(0, 0.06, 0),
    radius=1.55,
    color=vec(0.45, 0.65, 0.72)
)
cylinder(
    pos=vec(6.0, 0.62, 11.4),
    axis=vec(0, 1.3, 0),
    radius=0.13,
    color=vec(0.72, 0.70, 0.66)
)
for k in range(10):
    a = k*2*pi/10
    sphere(
        pos=vec(
            6.0+cos(a)*0.55,
            1.55-0.25*sin(k*0.9),
            11.4+sin(a)*0.55
        ),
        radius=0.06,
        color=vec(0.85, 0.94, 1.0)
    )
plumeria(12.0, 0.17, 12.8, 3.0, 1.1)
slab(-18.6, -14.8, 0.05, 0.3, 5.0, 9.5,
     vec(0.25, 0.17, 0.11))
shrubs(
    -18.5, -14.9, 5.1, 9.4, 0.25, 40,
    [LEAF, LEAF2, PINK,
     vec(0.95, 0.55, 0.15),
     vec(0.9, 0.25, 0.3)],
    0.15, 0.35
)
for x, z in (
    (-17.6, 6.5),
    (-16.0, 8.0),
    (-15.4, 6.0)
):
    agave(x, z, 1.0, 0.25)
palm(-17.0, 7.5, 5.0)
slab(13.6, 16.6, 0.05, 0.3, 5.0, 9.5,
     vec(0.25, 0.17, 0.11))
shrubs(
    13.7, 16.5, 5.1, 9.4, 0.25, 40,
    [LEAF, LEAF2, PINK, vec(0.95, 0.9, 0.9)],
    0.15, 0.35
)
palm(15.2, 7.0, 4.2)
slab(LX1-1.5, LX1-0.45, 0.05, 0.3, 10.0, 21.0,
     vec(0.25, 0.17, 0.11))
shrubs(
    LX1-1.4, LX1-0.55, 10.2, 20.8, 0.25, 36,
    [LEAF, LEAF2, PINK, vec(0.95, 0.6, 0.2)],
    0.15, 0.32
)
slab(LX0+0.45, LX0+1.5, 0.05, 0.3, 11.0, 21.0,
     vec(0.25, 0.17, 0.11))
shrubs(
    LX0+0.55, LX0+1.4, 11.2, 20.8, 0.25, 30,
    [LEAF, LEAF2, PINK, vec(0.95, 0.6, 0.2)],
    0.15, 0.32
)
for lx, lz in (
    (-14.1, 12.0), (-14.1, 17.0),
    (-6.4, 12.0), (-6.4, 17.0),
    (-5.3, 20.0), (-1.4, 14.0),
    (-1.4, 19.0)
):
    lamp(lx, lz, 0.9)
for px in (-5.6, -1.2):
    slab(
        px-0.4, px+0.4, 0, 0.8,
        WZ+0.5, WZ+1.3,
        vec(0.38, 0.36, 0.34)
    )
    for k in range(6):
        a = k*pi/3
        cone(
            pos=vec(px, 0.8, WZ+0.9),
            axis=vec(cos(a)*0.7, 1.2, sin(a)*0.7),
            radius=0.06,
            color=vec(0.15, 0.45, 0.18)
        )
shrubs(
    -6.2, -4.9, WZ+0.2, WZ+1.0,
    0.0, 10, [LEAF, LEAF2], 0.2, 0.35
)
for lx, lz in (
    (-5.0, 7.5), (-1.8, 7.5),
    (2.0, 7.0), (5.5, 7.0),
    (9.0, 7.0), (12.0, 7.0),
    (-14.2, 9.5), (-6.5, 9.8),
    (-4.5, 10.2)
):
    lamp(lx, lz, 0.9)
GZ = LZ1-0.3
PW = vec(0.86, 0.83, 0.76)
CAPC = vec(0.94, 0.92, 0.88)


def wall_run(x0, x1, z0, z1, h=2.4):
    slab(x0, x1, 0, h, z0, z1, PW)
    slab(
        x0-0.08, x1+0.08, h, h+0.16,
        z0-0.08, z1+0.08, CAPC
    )


wall_run(LX0, LX0+0.45, LZ0, LZ1)
wall_run(LX1-0.45, LX1, LZ0, LZ1)
wall_run(LX0, LX1, LZ0, LZ0+0.45)
for z in range(-12, 21, 4):
    slab(
        LX0+0.45, LX0+0.5,
        0.2, 2.3, z, z+0.05,
        vec(0.7, 0.67, 0.6)
    )
    slab(
        LX1-0.5, LX1-0.45,
        0.2, 2.3, z, z+0.05,
        vec(0.7, 0.67, 0.6)
    )
FW0, FW1 = GZ-0.25, GZ+0.25
wall_run(LX0, -14.3, FW0, FW1)
wall_run(-6.2, -5.1, FW0, FW1)
wall_run(-1.7, LX1, FW0, FW1)
for a, b in (
    (-18.2, -15.0),
    (2.5, 7.0),
    (9.0, 15.5)
):
    slab(
        a-0.1, b+0.1, 0.25, 2.15,
        FW1, FW1+0.05, BLACK
    )
    louvers(
        a, b, 0.35, 2.05,
        FW1+0.05, 0.22, 0.12, 0.12
    )


def gate_pillar(x0, x1, h=3.7):
    stone(x0, x1, 0, h, GZ-0.35, GZ+0.35)
    slab(
        x0-0.15, x1+0.15, h, h+0.2,
        GZ-0.5, GZ+0.5, CAPC
    )
    lan = slab(
        x0+0.15, x1-0.15,
        h+0.2, h+0.75,
        GZ-0.2, GZ+0.2,
        vec(0.85, 0.82, 0.70)
    )
    glow_items.append(
        (lan, vec(0.85, 0.82, 0.70), False, 1.0)
    )
    slab(
        x0+0.1, x1-0.1,
        h+0.75, h+0.85,
        GZ-0.3, GZ+0.3, CAPC
    )


gate_pillar(-14.3, -13.3)
gate_pillar(-7.2, -6.2)
gate_pillar(-5.1, -4.2)
gate_pillar(-2.6, -1.7)
for a, b in (
    (-13.3, -10.25),
    (-10.25, -7.2)
):
    slab(
        a+0.03, b-0.03,
        0.12, 3.1,
        GZ-0.06, GZ+0.06,
        BLACK
    )
    n = int((b-a-0.3)/0.22)
    for i in range(n):
        x = a+0.17+i*0.22
        slab(
            x, x+0.13,
            0.28, 2.95,
            GZ+0.08, GZ+0.2,
            WOOD if i % 3 else WOOD_L
        )
    for y in (0.2, 1.5, 2.9):
        slab(
            a+0.03, b-0.03,
            y, y+0.1,
            GZ+0.05, GZ+0.24,
            BLACK
        )
slab(-10.32, -10.18, 0.12, 3.1,
     GZ, GZ+0.26, BLACK)
for hx in (-10.55, -9.95):
    slab(
        hx-0.03, hx+0.03,
        1.2, 1.9,
        GZ+0.2, GZ+0.3,
        vec(0.8, 0.65, 0.3)
    )
slab(-13.3, -7.2, 3.3, 3.75,
     GZ-0.3, GZ+0.3, WOOD_D)
slab(-13.3, -7.2, 3.75, 3.85,
     GZ-0.3, GZ+0.3, BLACK)
for x in (-12.4, -10.7, -8.9, -8.0):
    downlight(x, 3.27, GZ+0.15)
slab(-4.15, -2.65, 0.1, 2.6,
     GZ-0.06, GZ+0.06, BLACK)
for i in range(6):
    x = -4.0+i*0.24
    slab(
        x, x+0.14,
        0.25, 2.5,
        GZ+0.08, GZ+0.2,
        WOOD if i % 2 else WOOD_L
    )
for y in (0.2, 1.2, 2.45):
    slab(-4.15, -2.65, y, y+0.1,
         GZ+0.05, GZ+0.24, BLACK)
slab(-3.0, -2.95, 1.1, 1.7,
     GZ+0.2, GZ+0.3,
     vec(0.8, 0.65, 0.3))
slab(-5.1, -1.7, 2.75, 2.95,
     GZ-0.4, GZ+1.0, WOOD_L)
slab(-5.1, -1.7, 2.95, 3.05,
     GZ-0.4, GZ+1.0, BLACK)
downlight(-4.2, 2.7, GZ+0.7)
downlight(-2.6, 2.7, GZ+0.7)
slab(-4.95, -4.35, 1.6, 2.0,
     GZ+0.35, GZ+0.4,
     vec(0.8, 0.65, 0.3))
for px in (-14.4, -6.4):
    slab(
        px-0.4, px+0.4, 0.0, 0.7,
        GZ-1.6, GZ-0.8,
        vec(0.38, 0.36, 0.34)
    )
    cone(
        pos=vec(px, 0.7, GZ-1.2),
        axis=vec(0, 2.0, 0),
        radius=0.55,
        color=vec(0.10, 0.36, 0.14)
    )
for px in (0.5, 3.2, 5.9, 8.6, 11.3, 14.0):
    slab(
        px-0.35, px+0.35, 0, 0.6,
        GZ-1.5, GZ-0.8,
        vec(0.38, 0.36, 0.34)
    )
    sphere(
        pos=vec(px, 1.1, GZ-1.15),
        radius=0.55,
        color=vec(0.18, 0.48, 0.18)
    )
# ============================================================
# INTERIOR  -  HELPERS
# ============================================================
GF = 0.225      # ground floor surface
UF = 5.7        # second floor surface
SF = 9.82       # sky room surface
LV = {'g': (-1.0, 4.5), 'u': (4.5, 8.0), 't': (4.5, 9.0), 's': (9.0, 30.0)}
CURT = vec(0.93, 0.89, 0.82)
BOOKC = [vec(0.55, 0.20, 0.18), vec(0.20, 0.34, 0.50), vec(0.85, 0.75, 0.50),
         vec(0.25, 0.45, 0.30), vec(0.70, 0.45, 0.20), vec(0.90, 0.90, 0.85),
         vec(0.35, 0.25, 0.45)]
ARTC = [vec(0.20, 0.45, 0.50), vec(0.88, 0.65, 0.25), vec(0.72, 0.36, 0.26),
        vec(0.92, 0.88, 0.80), vec(0.25, 0.30, 0.42)]
FAB1L = vec(0.92, 0.89, 0.83)
STEELD = vec(0.45, 0.46, 0.48)
MARBLE = vec(0.93, 0.93, 0.91)
WATER = vec(0.55, 0.78, 0.86)


def wb(x0, x1, z0, z1, lv):
    block(x0, x1, z0, z1, 0, 0, LV[lv][0], LV[lv][1])


def sl(x0, x1, y0, y1, z0, z1, col, lv=None, op=1.0, emi=False):
    if lv:
        wb(x0, x1, z0, z1, lv)
    return slab(x0, x1, y0, y1, z0, z1, col, op, emi)


def glow(o, dc):
    glow_items.append((o, dc, False, 1.0))
    return o


def add_light(x, y, z):
    lamp_lights.append(local_light(pos=vec(x, y, z), color=color.black))


def rail(p0, p1, r=0.025, col=STEEL):
    return cylinder(pos=p0, axis=p1-p0, radius=r, color=col)


def books(f, lx0, lx1, y, lz0, lz1):
    x = lx0
    while x < lx1-0.1:
        w = random.uniform(0.05, 0.11)
        h = random.uniform(0.20, 0.32)
        f.b(x, min(x+w, lx1), y, y+h, lz0, lz1, random.choice(BOOKC))
        x += w+0.006


def rug(x0, x1, z0, z1, y, c1, c2):
    slab(x0, x1, y, y+0.012, z0, z1, c1)
    slab(x0+0.25, x1-0.25, y+0.012, y+0.016, z0+0.25, z1-0.25, c2)
    slab(x0+0.45, x1-0.45, y+0.016, y+0.02, z0+0.45, z1-0.45, c1)


def pot_plant(x, z, y=GF, s=1.0, kind=0, solid=True):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.45*s, 0), radius=0.26*s,
             color=vec(0.40, 0.38, 0.36))
    cylinder(pos=vec(x, y+0.45*s, z), axis=vec(0, 0.03, 0), radius=0.23*s,
             color=vec(0.20, 0.13, 0.08))
    if kind == 0:
        for k in range(9):
            a = k*2*pi/9
            cone(pos=vec(x, y+0.47*s, z),
                 axis=vec(cos(a)*0.55*s, 1.0*s, sin(a)*0.55*s),
                 radius=0.08*s, color=LEAF if k % 2 else LEAF2)
    elif kind == 1:
        cylinder(pos=vec(x, y+0.47*s, z), axis=vec(0.03, 1.2*s, 0),
                 radius=0.04*s, color=WOOD_D)
        for k in range(11):
            a = k*2.4
            ellipsoid(pos=vec(x+cos(a)*0.3*s, y+(0.9+k*0.1)*s, z+sin(a)*0.3*s),
                      length=0.42*s, height=0.07*s, width=0.28*s,
                      axis=vec(cos(a), 0.4, sin(a)),
                      color=LEAF if k % 2 else LEAF2)
    else:
        cylinder(pos=vec(x, y+0.47*s, z), axis=vec(0.05, 1.3*s, 0),
                 radius=0.05*s, color=vec(0.45, 0.36, 0.26))
        for k in range(8):
            a = k*2*pi/8
            ellipsoid(pos=vec(x+0.05+cos(a)*0.4*s, y+1.7*s, z+sin(a)*0.4*s),
                      length=1.0*s, height=0.05*s, width=0.18*s,
                      axis=vec(cos(a), -0.35, sin(a)), color=LEAF)
    if solid:
        block(x-0.3*s, x+0.3*s, z-0.3*s, z+0.3*s, 0, 0, y-0.6, y+0.8)


def table_lamp(x, y, z, col=vec(0.92, 0.88, 0.78)):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.22, 0), radius=0.04, color=GOLD)
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.03, 0), radius=0.09, color=GOLD)
    sh = cylinder(pos=vec(x, y+0.2, z), axis=vec(0, 0.24, 0), radius=0.15, color=col)
    glow(sh, col)


def floor_lamp(x, z, y=GF, h=1.65, light=False):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.03, 0), radius=0.17, color=BLACK)
    cylinder(pos=vec(x, y, z), axis=vec(0, h, 0), radius=0.02, color=GOLD)
    sh = cylinder(pos=vec(x, y+h-0.1, z), axis=vec(0, 0.36, 0), radius=0.22,
                  color=vec(0.94, 0.90, 0.80))
    glow(sh, vec(0.94, 0.90, 0.80))
    block(x-0.2, x+0.2, z-0.2, z+0.2, 0, 0, y-0.6, y+0.8)
    if light:
        add_light(x, y+h+0.2, z)


def chandelier(x, ytop, z, drop=1.0, r=0.7, tiers=2):
    rail(vec(x, ytop-drop, z), vec(x, ytop, z), 0.025, GOLD)
    for t in range(tiers):
        rr = r*(1-0.3*t)
        yy = ytop-drop-0.32*t
        ring(pos=vec(x, yy, z), axis=vec(0, 1, 0), radius=rr, thickness=0.025,
             color=GOLD)
        n = 8-t
        for k in range(n):
            a = k*2*pi/n+t*0.4
            bx = x+cos(a)*rr
            bz = z+sin(a)*rr
            cylinder(pos=vec(bx, yy, bz), axis=vec(0, 0.16, 0), radius=0.015,
                     color=GOLD)
            b = sphere(pos=vec(bx, yy+0.22, bz), radius=0.065,
                       color=vec(0.95, 0.92, 0.82))
            glow(b, vec(0.95, 0.92, 0.82))
            c = sphere(pos=vec(bx, yy-0.08, bz), radius=0.04, color=vec(0.85, 0.93, 1.0),
                       opacity=0.7)
    sphere(pos=vec(x, ytop-drop-0.32*tiers+0.1, z), radius=0.09, color=GOLD)


def art(f, lx, y, w, h, style=0):
    f.b(lx-w/2-0.04, lx+w/2+0.04, y-0.04, y+h+0.04, 0, 0.05, WOOD_D)
    f.b(lx-w/2, lx+w/2, y, y+h, 0.05, 0.055, vec(0.93, 0.90, 0.84))
    k = 3 if style == 0 else 2
    ww = w/k
    for i in range(k):
        c = ARTC[(i+style) % len(ARTC)]
        hh = h*random.uniform(0.35, 0.8)
        f.b(lx-w/2+i*ww+0.04, lx-w/2+(i+1)*ww-0.04, y+0.06, y+0.06+hh,
            0.055, 0.065, c)
    f.cyl(lx, 0.06, y+h*0.65, 0.01, w*0.12, ARTC[(style+1) % len(ARTC)])


def mirror(f, lx, y, w, h, frame=GOLD):
    f.b(lx-w/2-0.05, lx+w/2+0.05, y-0.05, y+h+0.05, 0, 0.05, frame)
    f.b(lx-w/2, lx+w/2, y, y+h, 0.05, 0.058, MIRROR)
    f.b(lx-w/2+w*0.12, lx-w/2+w*0.18, y+h*0.12, y+h*0.85, 0.058, 0.062,
        vec(0.96, 0.99, 1.0))
    f.b(lx-w/2+w*0.24, lx-w/2+w*0.27, y+h*0.12, y+h*0.6, 0.058, 0.062,
        vec(0.96, 0.99, 1.0))


def tv(f, lx, y, w, h):
    f.b(lx-w/2, lx+w/2, y, y+h, 0, 0.06, BLACK)
    sc = f.b(lx-w/2+0.04, lx+w/2-0.04, y+0.04, y+h-0.04, 0.06, 0.066,
             vec(0.08, 0.12, 0.15))
    screen_items.append((sc, vec(0.08, 0.12, 0.15)))


def drapes_x(x0, x1, y0, y1, z, d=1):
    w = min(0.6, (x1-x0)/3)
    slab(x0-0.12, x0-0.12+w, y0, y1, z+d*0.10, z+d*0.19, CURT)
    slab(x1+0.12-w, x1+0.12, y0, y1, z+d*0.10, z+d*0.19, CURT)
    slab(x0-0.2, x1+0.2, y1, y1+0.04, z+d*0.08, z+d*0.2, BLACK)
    slab(x0, x1, y0, y1, z+d*0.2, z+d*0.21, CURT, 0.22)


def drapes_z(z0, z1, y0, y1, x, d=1):
    w = min(0.6, (z1-z0)/3)
    slab(x+d*0.10, x+d*0.19, y0, y1, z0-0.12, z0-0.12+w, CURT)
    slab(x+d*0.10, x+d*0.19, y0, y1, z1+0.12-w, z1+0.12, CURT)
    slab(x+d*0.08, x+d*0.2, y1, y1+0.04, z0-0.2, z1+0.2, BLACK)
    slab(x+d*0.2, x+d*0.21, y0, y1, z0, z1, CURT, 0.22)


def sill_x(x0, x1, y, z, d):
    slab(x0-0.06, x1+0.06, y-0.04, y, z, z+d*0.22, WHITE)


def sill_z(z0, z1, y, x, d):
    slab(x, x+d*0.22, y-0.04, y, z0-0.06, z1+0.06, WHITE)


def plates(x, y, z, n=4, r=0.13, col=WHITE):
    for i in range(n):
        cylinder(pos=vec(x, y+i*0.022, z), axis=vec(0, 0.018, 0), radius=r, color=col)


def mug(x, y, z, col=WHITE):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.1, 0), radius=0.04, color=col)


def vase(x, y, z, col=vec(0.30, 0.45, 0.50), flowers=True):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.28, 0), radius=0.07, color=col)
    if flowers:
        for k in range(5):
            a = k*1.3
            sphere(pos=vec(x+cos(a)*0.09, y+0.40+0.03*k, z+sin(a)*0.09), radius=0.06,
                   color=random.choice([PINK, vec(0.95, 0.85, 0.45), vec(0.95, 0.95, 0.9)]))


def fruit_bowl(x, y, z):
    cylinder(pos=vec(x, y, z), axis=vec(0, 0.07, 0), radius=0.17, color=vec(0.85, 0.80, 0.70))
    for k, c in enumerate([vec(0.85, 0.25, 0.20), vec(0.95, 0.75, 0.2),
                           vec(0.45, 0.70, 0.25), vec(0.95, 0.5, 0.15), vec(0.85, 0.25, 0.20)]):
        a = k*1.26
        sphere(pos=vec(x+cos(a)*0.08, y+0.12, z+sin(a)*0.08), radius=0.06, color=c)


def chair(f, col=WOOD_D, cush=FAB1):
    f.b(-0.22, 0.22, 0.42, 0.47, -0.22, 0.22, col, solid=True)
    f.b(-0.2, 0.2, 0.47, 0.52, -0.2, 0.2, cush)
    f.b(-0.22, 0.22, 0.52, 1.0, -0.25, -0.20, col)
    for sx in (-0.19, 0.19):
        for sz in (-0.19, 0.19):
            f.b(sx-0.025, sx+0.025, 0, 0.42, sz-0.025, sz+0.025, col)


def stool(f, h=0.68):
    f.cyl(0, 0, h, 0.05, 0.19, vec(0.30, 0.20, 0.14))
    f.cyl(0, 0, 0, h, 0.02, STEEL)
    f.cyl(0, 0, 0.25, 0.02, 0.15, STEEL)
    f.blk(-0.2, 0.2, 0, h, -0.2, 0.2)


def sofa(f, w=3.0, col=FAB1, cush=FAB1L, accent=FAB2):
    f.b(-w/2, w/2, 0.10, 0.42, -0.45, 0.45, col, solid=True)
    f.b(-w/2, w/2, 0.42, 1.0, -0.45, -0.22, col)
    f.b(-w/2, -w/2+0.25, 0.42, 0.72, -0.22, 0.45, col)
    f.b(w/2-0.25, w/2, 0.42, 0.72, -0.22, 0.45, col)
    n = max(2, int((w-0.5)/0.85))
    cw = (w-0.5)/n
    for i in range(n):
        x = -w/2+0.25+i*cw
        f.b(x+0.02, x+cw-0.02, 0.42, 0.58, -0.22, 0.43, cush)
        f.b(x+0.04, x+cw-0.04, 0.58, 0.95, -0.24, -0.12, cush)
    f.b(-w/2+0.3, -w/2+0.75, 0.58, 1.0, 0.0, 0.14, accent)
    f.b(w/2-0.75, w/2-0.3, 0.58, 0.98, -0.02, 0.12, FAB3)
    for sx in (-w/2+0.1, w/2-0.1):
        f.b(sx-0.03, sx+0.03, 0, 0.1, -0.35, -0.29, BLACK)
        f.b(sx-0.03, sx+0.03, 0, 0.1, 0.35, 0.41, BLACK)


def armchair(f, col=FAB2, cush=FAB1L):
    f.b(-0.48, 0.48, 0.10, 0.42, -0.45, 0.45, col, solid=True)
    f.b(-0.48, 0.48, 0.42, 1.0, -0.45, -0.25, col)
    f.b(-0.48, -0.32, 0.42, 0.70, -0.25, 0.45, col)
    f.b(0.32, 0.48, 0.42, 0.70, -0.25, 0.45, col)
    f.b(-0.32, 0.32, 0.42, 0.56, -0.25, 0.43, cush)
    f.b(-0.3, 0.3, 0.56, 0.92, -0.27, -0.17, cush)
    for sx in (-0.4, 0.4):
        for sz in (-0.38, 0.38):
            f.b(sx-0.03, sx+0.03, 0, 0.1, sz-0.03, sz+0.03, WOOD_D)


def coffee_table(f, w=1.4, d=0.8, h=0.42, col=WOOD_D):
    f.b(-w/2, w/2, h-0.05, h, -d/2, d/2, col, solid=True)
    f.b(-w/2+0.08, w/2-0.08, 0.14, 0.17, -d/2+0.08, d/2-0.08, WOOD_L)
    for sx in (-w/2+0.06, w/2-0.06):
        for sz in (-d/2+0.06, d/2-0.06):
            f.b(sx-0.03, sx+0.03, 0, h-0.05, sz-0.03, sz+0.03, BLACK)


def nightstand(f, col=WOOD_L):
    f.b(-0.25, 0.25, 0.1, 0.62, -0.22, 0.22, col, solid=True)
    f.b(-0.22, 0.22, 0.45, 0.57, 0.22, 0.235, WOOD_D)
    f.b(-0.22, 0.22, 0.2, 0.32, 0.22, 0.235, WOOD_D)
    f.b(-0.06, 0.06, 0.5, 0.52, 0.235, 0.26, GOLD)
    f.b(-0.06, 0.06, 0.25, 0.27, 0.235, 0.26, GOLD)
    for sx in (-0.22, 0.22):
        for sz in (-0.19, 0.19):
            f.b(sx-0.02, sx+0.02, 0, 0.1, sz-0.02, sz+0.02, BLACK)


def bed(f, w=2.0, l=2.2, sheet=vec(0.90, 0.88, 0.84), blanket=FAB2):
    f.b(-w/2-0.06, w/2+0.06, 0.12, 0.45, -l/2, l/2+0.04, WOOD_D, solid=True)
    f.b(-w/2, w/2, 0.45, 0.68, -l/2+0.08, l/2, sheet)
    f.b(-w/2-0.01, w/2+0.01, 0.55, 0.72, 0.15, l/2+0.02, blanket)
    f.b(-w/2-0.01, w/2+0.01, 0.55, 0.69, 0.78, 0.98, vec(0.85, 0.78, 0.6))
    f.b(-w/2-0.15, w/2+0.15, 0.1, 1.55, -l/2-0.14, -l/2, vec(0.50, 0.40, 0.34))
    f.b(-w/2-0.1, w/2+0.1, 0.55, 1.4, -l/2-0.02, -l/2+0.06, vec(0.62, 0.54, 0.46))
    for sx in (-w/4, w/4):
        f.b(sx-0.38, sx+0.38, 0.68, 0.82, -l/2+0.12, -l/2+0.5, vec(0.96, 0.95, 0.92))
        f.b(sx-0.28, sx+0.28, 0.72, 0.9, -l/2+0.5, -l/2+0.62, FAB3)


def wardrobe(f, w, h=2.3, d=0.6, mirrors=(1, 3), n=4):
    f.b(-w/2, w/2, 0.0, h, 0.0, d, vec(0.86, 0.83, 0.77), solid=True)
    pw = w/n
    for i in range(n):
        xa = -w/2+i*pw
        if i in mirrors:
            f.b(xa+0.03, xa+pw-0.03, 0.08, h-0.08, d, d+0.02, MIRROR)
            f.b(xa+pw*0.2, xa+pw*0.28, 0.4, h-0.5, d+0.02, d+0.025, vec(0.96, 0.99, 1.0))
        else:
            f.b(xa+0.03, xa+pw-0.03, 0.08, h-0.08, d, d+0.03, WOOD_L)
        f.b(xa+pw-0.12, xa+pw-0.09, 0.9, 1.3, d+0.03, d+0.05, GOLD)


def bookcase(f, w, h, rows, d=0.35):
    f.b(-w/2, w/2, 0, h, 0.0, d, WOOD_D, solid=True)
    f.b(-w/2+0.04, w/2-0.04, 0.08, h-0.04, 0.04, d+0.01, vec(0.42, 0.28, 0.18))
    for i in range(rows):
        y = 0.1+i*(h-0.3)/rows
        f.b(-w/2+0.04, w/2-0.04, y, y+0.03, 0.04, d+0.02, WOOD_L)
        if i % 3 == 2:
            vase(f.w(-w/4, 0.12)[0], f.y+y+0.03, f.w(-w/4, 0.12)[1], col=FAB2, flowers=False)
        else:
            books(f, -w/2+0.07, w/2-0.07, y+0.03, 0.1, d-0.03)


def table_rect(x0, x1, z0, z1, y, col, legcol=BLACK, lv='g'):
    sl(x0, x1, y-0.07, y, z0, z1, col, lv)
    for xx in (x0+0.12, x1-0.2):
        for zz in (z0+0.1, z1-0.18):
            slab(xx, xx+0.08, GF if y < 3 else y-0.9, y-0.07, zz, zz+0.08, legcol)


def cabinet(x0, x1, y0, y1, z0, z1, col, face, n, lv='g', dcol=None):
    sl(x0, x1, y0, y1, z0, z1, col, lv)
    dcol = dcol or tint(col, 0.82)
    if face in ('z+', 'z-'):
        zf = z1 if face == 'z+' else z0
        s = 1 if face == 'z+' else -1
        w = (x1-x0)/n
        for i in range(n):
            xa = x0+i*w
            slab(xa+0.02, xa+w-0.02, y0+0.05, y1-0.03, zf, zf+s*0.025, dcol)
            slab(xa+w/2-0.09, xa+w/2+0.09, y1-0.17, y1-0.14, zf+s*0.025, zf+s*0.05, STEEL)
    else:
        xf = x1 if face == 'x+' else x0
        s = 1 if face == 'x+' else -1
        w = (z1-z0)/n
        for i in range(n):
            za = z0+i*w
            slab(xf, xf+s*0.025, y0+0.05, y1-0.03, za+0.02, za+w-0.02, dcol)
            slab(xf+s*0.025, xf+s*0.05, y1-0.17, y1-0.14, za+w/2-0.09, za+w/2+0.09, STEEL)


def downlights(pts, y):
    for (x, z) in pts:
        s = cylinder(pos=vec(x, y, z), axis=vec(0, 0.03, 0), radius=0.11,
                     color=vec(0.9, 0.9, 0.85))
        glow(s, vec(0.9, 0.9, 0.85))


def cove(x0, x1, z0, z1, y):
    """warm LED cove strip around a room just under its ceiling"""
    c = vec(0.96, 0.92, 0.82)
    for (a0, a1, b0, b1) in ((x0, x1, z0, z0+0.07), (x0, x1, z1-0.07, z1),
                             (x0, x0+0.07, z0, z1), (x1-0.07, x1, z0, z1)):
        o = slab(a0, a1, y, y+0.05, b0, b1, c)
        glow(o, c)


def skirt(x0, x1, z0, z1, y, col=vec(0.95, 0.93, 0.88)):
    h = 0.13
    slab(x0, x1, y, y+h, z0, z0+0.03, col)
    slab(x0, x1, y, y+h, z1-0.03, z1, col)
    slab(x0, x0+0.03, y, y+h, z0, z1, col)
    slab(x1-0.03, x1, y, y+h, z0, z1, col)


def planks(x0, x1, z0, z1, y, base, line, step=0.7, along='z'):
    slab(x0, x1, y-0.004, y+0.003, z0, z1, base)
    if along == 'z':
        n = int((z1-z0)/step)
        for i in range(1, n+1):
            z = z0+i*step
            slab(x0, x1, y+0.003, y+0.006, z-0.012, z+0.012, line)
    else:
        n = int((x1-x0)/step)
        for i in range(1, n+1):
            x = x0+i*step
            slab(x-0.012, x+0.012, y+0.003, y+0.006, z0, z1, line)


def tiles(x0, x1, z0, z1, y, c1, c2, size=0.9):
    slab(x0, x1, y-0.004, y+0.003, z0, z1, c1)
    nx = int((x1-x0)/size)
    nz = int((z1-z0)/size)
    for i in range(nx):
        for j in range(nz):
            if (i+j) % 2:
                slab(x0+i*size, x0+(i+1)*size, y+0.003, y+0.006,
                     z0+j*size, z0+(j+1)*size, c2)


def stair_rails(xa, xb, z0, z1, ya, yb, axis, n, h=0.95):
    """balusters + slanted handrail along both long sides"""
    pass


# ============================================================
# GROUND FLOOR  (x -13.72..12.72, z -11.72..2.58)
# ============================================================
GX0, GX1, GZ0, GZ1 = -13.72, 12.72, -11.72, 2.58

# --- floor finishes
planks(GX0, 5.5, GZ0, GZ1, GF, vec(0.58, 0.42, 0.28), vec(0.44, 0.30, 0.19), 0.7)
tiles(5.5, GX1, GZ0, GZ1, GF, vec(0.90, 0.89, 0.85), vec(0.62, 0.62, 0.60), 0.9)
slab(-6.0, -1.5, GF, GF+0.008, -2.0, GZ1, MARBLE)
for (a, b, c, d) in ((-6.0, -1.5, -2.0, -1.94), (-6.0, -5.94, -2.0, GZ1),
                     (-1.56, -1.5, -2.0, GZ1)):
    slab(a, b, GF+0.008, GF+0.012, c, d, vec(0.45, 0.40, 0.32))
slab(-4.2, -2.7, GF+0.008, GF+0.014, -1.8, 2.3, vec(0.50, 0.20, 0.22))
slab(-4.05, -2.85, GF+0.014, GF+0.017, -1.65, 2.15, vec(0.85, 0.75, 0.55))
skirt(GX0, GX1, GZ0, GZ1, GF)
cove(GX0, GX1, GZ0, GZ1, 4.06)

# --- solid outer walls (collision)
wb(-14.4, -13.72, -12.0, 2.8, 'g')
wb(12.72, 13.4, -12.0, 2.8, 'g')
wb(-14.4, 13.4, -12.0, -11.72, 'g')
wb(-14.7, -4.45, 2.56, 4.6, 'g')
wb(-2.45, 13.2, 2.56, 4.6, 'g')
block(4.1, 7.9, 9.5, 13.3, 0, 0, -1.0, 1.0)     # fountain pond

# --- window sills + curtains (ground)
sill_z(-7.8, -5.0, 0.9, GX0, 1)
sill_z(-3.4, -0.4, 0.9, GX0, 1)
drapes_z(-7.8, -5.0, GF+0.05, 3.4, GX0, 1)
drapes_z(-3.4, -0.4, GF+0.05, 3.4, GX0, 1)
sill_z(-9.6, -6.4, 1.35, GX1-0.22, 1)
sill_z(-3.4, -0.4, 0.9, GX1-0.22, 1)
sill_x(0.6, 3.4, 1.0, GZ0, 1)
drapes_x(0.6, 3.4, 0.9, 3.2, GZ0, 1)
sill_x(-3.7, -2.1, 2.1, GZ0, 1)
sill_x(3.4, 5.5, 0.9, GZ1-0.22, 1)
sill_x(7.5, 12.0, 0.9, GZ1-0.22, 1)
sill_x(7.3, 9.9, 1.35, GZ0, 1)
drapes_x(3.4, 5.5, 0.9, 3.4, GZ1-0.05, -1)

# ------------------------------------------------------------
# CR / COMFORT ROOM (toilet + shower)  x -13.72..-10.4, z -11.72..-8.6
# ------------------------------------------------------------
PWALL = vec(0.90, 0.88, 0.82)
sl(-10.45, -10.35, GF, 4.12, GZ0, -8.6, PWALL, 'g')
sl(GX0, -11.9, GF, 4.12, -8.65, -8.55, PWALL, 'g')
sl(-10.9, -10.35, GF, 4.12, -8.65, -8.55, PWALL, 'g')
sl(-11.9, -10.9, 2.4, 4.12, -8.65, -8.55, PWALL)
slab(-11.93, -11.87, GF, 2.4, -8.68, -8.52, WOOD_D)
slab(-10.93, -10.87, GF, 2.4, -8.68, -8.52, WOOD_D)
slab(-11.93, -10.87, 2.37, 2.43, -8.68, -8.52, WOOD_D)
sl(-11.95, -11.88, GF, 2.35, -8.6, -7.8, WOOD_L, 'g')          # open door leaf
slab(-11.98, -11.95, 1.0, 1.1, -8.2, -8.0, GOLD)
tiles(GX0, -10.45, GZ0, -8.65, GF+0.006, vec(0.70, 0.78, 0.80), vec(0.55, 0.66, 0.70), 0.55)
slab(GX0, GX0+0.04, GF, 2.5, GZ0, -8.65, vec(0.78, 0.84, 0.85))
slab(GX0, -10.45, GF, 2.5, GZ0, GZ0+0.04, vec(0.78, 0.84, 0.85))
slab(-10.49, -10.45, GF, 2.5, GZ0, -8.65, vec(0.78, 0.84, 0.85))
for yy in (0.8, 1.4, 2.0):
    slab(GX0, GX0+0.045, yy, yy+0.02, GZ0, -8.65, vec(0.55, 0.66, 0.70))
    slab(GX0, -10.45, yy, yy+0.02, GZ0, GZ0+0.045, vec(0.55, 0.66, 0.70))
slab(GX0, -10.45, 2.5, 2.56, GZ0, -8.65, WHITE)
# shower stall
slab(GX0+0.04, -12.3, GF, GF+0.07, GZ0+0.04, -10.1, WHITE)
slab(GX0+0.04, -12.9, GF, 2.25, -10.13, -10.09, GLASS, op=0.28)
slab(-12.34, -12.3, GF, 2.25, GZ0+0.04, -10.1, GLASS, op=0.28)
wb(GX0, -12.25, GZ0, -10.05, 'g')
for (a, b, c, d) in ((GX0+0.04, -12.9, -10.15, -10.07), (-12.36, -12.28, GZ0+0.04, -10.07)):
    slab(a, b, 2.2, 2.28, c, d, STEEL)
slab(GX0+0.04, -12.28, 0.0+GF, GF+0.001, GZ0+0.04, -10.1, WHITE)
rail(vec(-13.0, GF+0.1, GZ0+0.06), vec(-13.0, 2.2, GZ0+0.06), 0.02, STEEL)
rail(vec(-13.0, 2.2, GZ0+0.06), vec(-13.0, 2.2, GZ0+0.4), 0.02, STEEL)
cylinder(pos=vec(-13.0, 2.17, GZ0+0.4), axis=vec(0, 0.03, 0), radius=0.2, color=STEEL)
rail(vec(-13.5, 1.0, GZ0+0.05), vec(-13.5, 1.6, GZ0+0.05), 0.015, STEEL)
slab(-13.4, -13.0, 1.2, 1.5, GZ0+0.04, GZ0+0.12, WHITE)
for k in range(5):
    sphere(pos=vec(-13.0+0.1*sin(k*2.0), 2.0-0.3*k, GZ0+0.4+0.05*k), radius=0.025,
           color=vec(0.8, 0.92, 1.0), opacity=0.5)
# toilet
t = F(-11.5, GZ0, 0, GF)
t.b(-0.2, 0.2, 0.0, 0.05, 0.1, 0.62, WHITE)
t.b(-0.22, 0.22, 0.45, 0.95, 0.0, 0.2, WHITE)
t.b(-0.04, 0.04, 0.95, 0.98, 0.07, 0.13, STEEL)
t.ell(0, 0.28, 0.38, 0.42, 0.36, 0.6, WHITE)
t.cyl(0, 0.38, 0.46, 0.03, 0.22, WHITE)
t.blk(-0.3, 0.3, 0.0, 0.8, 0.0, 0.7)
t.b(0.32, 0.36, 0.55, 0.75, 0.0, 0.1, STEEL)
t.b(-0.5, -0.35, 0.65, 0.68, 0.0, 0.05, STEEL)
# vanity (left wall)
v = F(GX0, -9.4, 1, GF)
v.b(0.0, 0.5, 0.0, 0.85, -0.6, 0.6, WOOD_L, solid=True)
v.b(0.0, 0.52, 0.85, 0.9, -0.62, 0.62, WHITE)
v.b(0.0, 0.52, 0.0, 0.85, -0.6, 0.6, WOOD_L)
v.b(0.1, 0.45, 0.9, 0.93, -0.25, 0.25, vec(0.88, 0.90, 0.92))
v.cyl(0.08, 0, 0.9, 0.25, 0.015, STEEL)
v.b(0.0, 0.05, 1.3, 2.35, -0.55, 0.55, MIRROR)
v.b(-0.02, 0.0, 1.28, 2.37, -0.58, 0.58, GOLD)
for zz in (-0.35, 0.35):
    sc = v.b(0.0, 0.1, 2.0, 2.25, zz-0.05, zz+0.05, vec(0.95, 0.9, 0.8))
    glow(sc, vec(0.95, 0.9, 0.8))
v.b(0.15, 0.38, 0.9, 0.98, -0.45, -0.3, vec(0.9, 0.9, 0.95))
pot_plant(GX0+0.55, -8.9, GF+0.93, 0.3, 0, solid=False)
# towel bar & towels, mat
rail(vec(-10.6, 1.35, -10.4), vec(-10.6, 1.35, -9.4), 0.015, STEEL)
slab(-10.62, -10.57, 0.7, 1.35, -10.35, -9.9, vec(0.85, 0.88, 0.9))
slab(-10.62, -10.57, 0.8, 1.35, -9.85, -9.45, vec(0.55, 0.70, 0.75))
slab(-12.1, -11.0, GF+0.006, GF+0.02, -10.6, -9.95, vec(0.80, 0.85, 0.86))
downlights([(-12.2, -10.2), (-11.2, -9.3)], 4.08)
add_light(-12.0, 3.6, -10.2)

# ------------------------------------------------------------
# LIVING ROOM
# ------------------------------------------------------------
rug(-11.5, -5.1, -10.0, -3.4, GF, vec(0.32, 0.40, 0.42), vec(0.82, 0.77, 0.66))
# TV feature wall
louvers(-10.9, -5.7, GF, 3.7, GZ0, 0.20, 0.12, 0.16)
sl(-10.9, -5.7, 3.7, 3.8, GZ0, GZ0+0.2, WOOD_D)
sl(-10.5, -6.1, GF, 0.6, GZ0+0.16, -11.1, WOOD_D, 'g')
sl(-10.5, -6.1, 0.6, 0.64, GZ0+0.16, -11.05, WHITE)
for xx in (-10.45, -6.55):
    sl(xx, xx+0.04, 0.64, 0.9, -11.5, -11.46, BLACK)
tvf = F(-8.3, -11.55, 0, GF)
tv(tvf, 0, 0.95, 2.7, 1.55)
tvf.b(-1.0, 1.0, 0.64-GF+0.2, 0.64-GF+0.28, 0.0, 0.14, vec(0.12, 0.12, 0.13))
glow_strip = slab(-1.45, 1.45, GF+2.55, GF+2.58, -11.58, -11.52, vec(1.0, 0.85, 0.55))
glow(glow_strip, vec(0.35, 0.30, 0.24))
vase(-10.0, 0.66, -11.35, vec(0.75, 0.55, 0.30), True)
vase(-6.6, 0.66, -11.35, FAB2, False)
# sofa group
sf = F(-8.3, -3.9, 2, GF)
sofa(sf, 3.6)
coffee_table(F(-8.3, -6.5, 0, GF), 1.5, 0.85)
cf = F(-8.3, -6.5, 0, GF)
cf.b(-0.45, 0.45, 0.42, 0.44, -0.25, 0.25, WOOD_L)
vase(-8.55, 0.44+GF-0.0, -6.55, vec(0.30, 0.45, 0.50), True)
books(cf, 0.1, 0.45, 0.44, -0.1, 0.2)
mug(-7.8, GF+0.44, -6.35, vec(0.8, 0.4, 0.3))
armchair(F(-11.55, -6.5, 1, GF))
armchair(F(-5.05, -6.5, 3, GF), FAB3)
for (x, z) in ((-10.35, -3.35), (-6.25, -3.35)):
    cylinder(pos=vec(x, GF, z), axis=vec(0, 0.55, 0), radius=0.26, color=WOOD_D)
    cylinder(pos=vec(x, GF+0.55, z), axis=vec(0, 0.03, 0), radius=0.3, color=GOLD)
    table_lamp(x, GF+0.58, z)
    block(x-0.3, x+0.3, z-0.3, z+0.3, 0, 0, -0.4, 0.9)
# behind-sofa console
cons = F(-8.3, -2.55, 0, GF)
cons.b(-1.2, 1.2, 0.62, 0.68, 0.0, 0.38, WOOD_D, solid=True)
for sx in (-1.15, 1.1):
    cons.b(sx, sx+0.05, 0, 0.62, 0.02, 0.08, BLACK)
    cons.b(sx, sx+0.05, 0, 0.62, 0.3, 0.36, BLACK)
table_lamp(-9.2, GF+0.68, -2.35)
table_lamp(-7.4, GF+0.68, -2.35)
vase(-8.3, GF+0.68, -2.35, vec(0.85, 0.80, 0.70), True)
# left wall decor
floor_lamp(-13.1, -4.15, GF, 1.75, True)
pot_plant(-13.1, -8.1, GF, 1.2, 1)
pot_plant(-13.1, 0.4, GF, 1.3, 2)
# upright piano (front wall)
pf = F(-11.6, 2.2, 2, GF)
pf.b(-0.95, 0.95, 0.0, 1.35, -0.38, 0.35, vec(0.10, 0.10, 0.12), solid=True)
pf.b(-0.95, 0.95, 0.72, 0.78, 0.35, 0.58, vec(0.14, 0.14, 0.15))
pf.b(-0.9, 0.9, 0.78, 0.82, 0.36, 0.56, vec(0.96, 0.95, 0.9))
for k in range(18):
    pf.b(-0.88+k*0.1, -0.88+k*0.1+0.05, 0.82, 0.86, 0.4, 0.5, BLACK)
pf.b(-0.8, 0.8, 1.0, 1.25, 0.35, 0.37, vec(0.06, 0.06, 0.07))
pf.b(-0.75, 0.75, 0.0, 0.08, 0.2, 0.55, BLACK)
pb = F(-11.6, 1.2, 2, GF)
pb.b(-0.4, 0.4, 0.40, 0.48, -0.2, 0.2, vec(0.10, 0.10, 0.12), solid=True)
for sx in (-0.34, 0.34):
    for sz in (-0.14, 0.14):
        pb.b(sx-0.02, sx+0.02, 0, 0.4, sz-0.02, sz+0.02, BLACK)
art(F(-11.6, GZ1-0.01, 2, GF), 0, 1.6, 1.4, 0.9, 1)
art(F(-9.6, GZ1-0.01, 2, GF), 0, 1.7, 0.7, 0.9, 0)
# bar cart
bc = F(-6.9, 1.7, 0, GF)
bc.b(-0.4, 0.4, 0.62, 0.66, -0.2, 0.2, GOLD, solid=True)
bc.b(-0.4, 0.4, 0.28, 0.31, -0.2, 0.2, GOLD)
for sx in (-0.38, 0.38):
    for sz in (-0.18, 0.18):
        bc.b(sx-0.015, sx+sx*0+0.015, 0.05, 0.66, sz-0.015, sz+0.015, GOLD)
for k in range(3):
    bc.cyl(-0.25+k*0.22, 0, 0.66, 0.28, 0.035, vec(0.20, 0.45, 0.30) if k != 1 else vec(0.55, 0.3, 0.15))
# living chandelier + lights
chandelier(-8.3, 4.1, -6.0, 1.1, 0.85, 3)
add_light(-8.3, 3.2, -6.0)
add_light(-11.5, 3.2, 0.5)

# ------------------------------------------------------------
# FOYER / ENTRY
# ------------------------------------------------------------
cs = F(-5.3, GZ1, 2, GF)
cs.b(-0.7, 0.7, 0.72, 0.78, 0.0, 0.4, WOOD_D, solid=True)
for sx in (-0.66, 0.6):
    cs.b(sx, sx+0.06, 0, 0.72, 0.02, 0.08, GOLD)
    cs.b(sx, sx+0.06, 0, 0.72, 0.3, 0.36, GOLD)
cs.b(-0.6, 0.6, 0.35, 0.37, 0.05, 0.35, WOOD_L)
mirror(cs, 0, 1.25, 0.9, 1.25)
table_lamp(-5.75, GF+0.78, 2.3)
vase(-4.95, GF+0.78, 2.3, vec(0.85, 0.78, 0.60), True)
mug(-5.3, GF+0.78, 2.35, GOLD)
bn = F(-1.2, GZ1, 2, GF)
bn.b(-0.8, 0.8, 0.38, 0.46, 0.0, 0.42, WOOD_L, solid=True)
bn.b(-0.78, 0.78, 0.46, 0.56, 0.02, 0.4, FAB2)
bn.b(-0.8, 0.8, 0.0, 0.38, 0.0, 0.42, vec(0.22, 0.15, 0.10))
bn.b(-0.7, 0.7, 1.45, 1.6, 0.0, 0.07, WOOD_D)
for k in range(5):
    bn.b(-0.6+k*0.3-0.02, -0.6+k*0.3+0.02, 1.35, 1.46, 0.07, 0.15, GOLD)
art(bn, 0, 1.75, 1.1, 0.7, 2)
stool_f = F(-1.0, 1.2, 0, GF)
pot_plant(-1.0, 0.4, GF, 1.2, 1)
cylinder(pos=vec(-6.1, GF, 0.6), axis=vec(0, 0.55, 0), radius=0.12, color=vec(0.2, 0.3, 0.35))
rail(vec(-6.08, GF+0.5, 0.6), vec(-6.0, GF+1.0, 0.65), 0.012, WOOD_D)
chandelier(-3.5, 4.1, 0.9, 0.8, 0.55, 2)
add_light(-3.5, 3.3, 0.9)
downlights([(-5.0, -0.8), (-2.2, -0.8), (-5.0, 1.6), (-2.2, 1.6)], 4.08)

# ------------------------------------------------------------
# DINING ROOM
# ------------------------------------------------------------
rug(-0.9, 4.7, -9.8, -4.5, GF, vec(0.25, 0.36, 0.38), vec(0.85, 0.80, 0.68))
table_rect(0.2, 3.6, -7.95, -6.45, GF+0.78, WOOD_D, BLACK)
slab(0.35, 3.45, GF+0.78, GF+0.8, -7.4, -7.0, vec(0.85, 0.80, 0.70))
for x in (0.7, 1.3, 2.5, 3.1):
    plates(x, GF+0.8, -7.7, 1, 0.12)
    plates(x, GF+0.8, -6.7, 1, 0.12)
    mug(x+0.2, GF+0.8, -7.65, vec(0.25, 0.38, 0.45))
for x in (1.5, 2.3):
    cylinder(pos=vec(x, GF+0.8, -7.2), axis=vec(0, 0.22, 0), radius=0.02, color=vec(0.95, 0.92, 0.85))
    sp = sphere(pos=vec(x, GF+1.05, -7.2), radius=0.03, color=vec(1.0, 0.8, 0.4))
    glow(sp, vec(1.0, 0.8, 0.4))
vase(1.9, GF+0.8, -7.2, vec(0.30, 0.45, 0.50), True)
for x in (0.8, 1.9, 3.0):
    chair(F(x, -8.6, 0, GF), WOOD_D, vec(0.35, 0.45, 0.48))
    chair(F(x, -5.8, 2, GF), WOOD_D, vec(0.35, 0.45, 0.48))
chair(F(-0.15, -7.2, 1, GF), WOOD_L, vec(0.62, 0.32, 0.24))
chair(F(3.95, -7.2, 3, GF), WOOD_L, vec(0.62, 0.32, 0.24))
chandelier(1.9, 4.1, -7.2, 1.3, 1.0, 3)
add_light(1.9, 3.2, -7.2)
# sideboard + wine hutch (back wall)
cabinet(0.9, 3.1, GF, 0.95, GZ0, -11.2, WOOD_D, 'z+', 3, 'g')
sl(0.85, 3.15, 0.95, 1.0, GZ0, -11.17, MARBLE)
table_lamp(1.2, 1.0, -11.5)
table_lamp(2.8, 1.0, -11.5)
vase(2.0, 1.0, -11.5, vec(0.85, 0.80, 0.70), True)
cabinet(-1.3, 0.4, GF, 2.3, GZ0, -11.3, WOOD_D, 'z+', 2, 'g')
sl(-1.28, 0.38, 1.0, 2.2, -11.3, -11.28, GLASS, None, 0.3)
for yy in (1.0, 1.5):
    slab(-1.25, 0.35, yy, yy+0.03, -11.68, -11.3, WOOD_L)
    for k in range(6):
        cylinder(pos=vec(-1.15+k*0.25, yy+0.03, -11.55), axis=vec(0, 0.28, 0), radius=0.035,
                 color=vec(0.15, 0.35, 0.2) if k % 2 else vec(0.45, 0.12, 0.15))
art(F(4.4, GZ0+0.02, 0, GF), 0, 1.3, 1.0, 1.0, 2)
downlights([(0.0, -9.5), (3.5, -9.5), (0.0, -4.2), (3.5, -4.2)], 4.08)

# ------------------------------------------------------------
# STUDY NOOK (front wall, right of foyer)
# ------------------------------------------------------------
dk = F(4.45, GZ1, 2, GF)
dk.b(-1.0, 1.0, 0.72, 0.77, 0.0, 0.72, WOOD_L, solid=True)
dk.b(-1.0, -0.65, 0.0, 0.72, 0.02, 0.7, WOOD_D)
dk.b(0.65, 1.0, 0.0, 0.72, 0.02, 0.7, WOOD_D)
for yy in (0.15, 0.4, 0.62):
    dk.b(0.7, 0.95, yy, yy+0.03, 0.7, 0.72, GOLD)
dk.b(-0.4, 0.4, 0.77, 0.79, 0.15, 0.35, BLACK)
mon = dk.b(-0.35, 0.35, 1.0, 1.4, 0.34, 0.38, BLACK)
sc = dk.b(-0.32, 0.32, 1.03, 1.37, 0.38, 0.385, vec(0.10, 0.15, 0.2))
screen_items.append((sc, vec(0.10, 0.15, 0.2)))
dk.b(-0.04, 0.04, 0.79, 1.0, 0.35, 0.39, STEEL)
table_lamp(*dk.w(-0.8, 0.5)[:1], GF+0.77, dk.w(-0.8, 0.5)[1])
mug(*dk.w(0.6, 0.4)[:1], GF+0.77, dk.w(0.6, 0.4)[1], vec(0.8, 0.5, 0.3))
chair(F(4.45, 1.1, 0, GF), BLACK, vec(0.30, 0.30, 0.33))
bk = F(1.6, GZ1, 2, GF)
bookcase(bk, 2.7, 2.3, 5)
armchair(F(0.9, 0.2, 0, GF), FAB3)
floor_lamp(-0.4, -0.5, GF, 1.6)
slab(0.3, 1.5, GF, GF+0.02, -0.4, 0.9, vec(0.55, 0.50, 0.42))
downlights([(1.5, -1.0), (4.4, 0.0)], 4.08)

# ------------------------------------------------------------
# GROUND STAIRS - floating stone slabs + pebble bed + tree
# ------------------------------------------------------------
_rng = random.Random(77)          # own random so the rest of the house stays the same
NST = 14
RISE = (UF-GF)/NST
DZ = 5.8/NST
SX0, SX1 = 5.75, 8.0              # slab width (x range)
SLAB_T = 0.24                     # thick chunky slabs like the photo
STONE_TOP = vec(0.36, 0.24, 0.17)
STONE_SIDE = vec(0.25, 0.16, 0.11)
STEELBLK = vec(0.08, 0.08, 0.09)

# --- the floating slabs
for i in range(NST):
    za = -0.8-i*DZ
    zb = za-DZ-0.04
    top = GF+(i+1)*RISE
    slab(SX0, SX1, top-SLAB_T, top-0.03, zb, za, STONE_SIDE)
    slab(SX0+0.01, SX1-0.01, top-0.03, top, zb+0.01, za-0.01, STONE_TOP)
    if i % 2 == 0:                # warm LED strip under every 2nd slab (glows at night)
        g = slab(SX0+0.15, SX1-0.15, top-SLAB_T-0.02, top-SLAB_T,
                 zb+0.06, za-0.06, vec(0.30, 0.24, 0.18))
        glow(g, vec(0.30, 0.24, 0.18))
# top landing
slab(5.6, 8.6, UF-0.24, UF, -7.0, -6.55, STONE_SIDE)
slab(5.6, 8.6, UF-0.03, UF, -7.0, -6.55, STONE_TOP)

# --- open side: black posts + 2 steel cables + wood handrail
RX = SX1-0.06
for i in range(0, NST, 2):
    top = GF+(i+1)*RISE
    zm = -0.8-(i+0.5)*DZ
    rail(vec(RX, top, zm), vec(RX, top+0.95, zm), 0.014, BLACK)
za0 = -0.8-0.5*DZ
zb0 = -0.8-(NST-0.5)*DZ
ya0 = GF+RISE
yb0 = GF+NST*RISE
rail(vec(RX, ya0+0.95, za0), vec(RX, yb0+0.95, zb0), 0.03, WOOD_D)
for hh in (0.32, 0.64):
    rail(vec(RX, ya0+hh, za0), vec(RX, yb0+hh, zb0), 0.008, STEEL)
rail(vec(RX, yb0+0.95, zb0), vec(RX, yb0+0.95, -7.0), 0.03, WOOD_D)

# --- river-pebble bed under the stairs
slab(5.5, 8.7, GF, GF+0.07, -6.7, -0.85, vec(0.50, 0.40, 0.28))        # bronze edge
slab(5.6, 8.6, GF+0.07, GF+0.10, -6.6, -0.95, vec(0.22, 0.21, 0.20))   # dark base
for _ in range(520):
    r = _rng.uniform(0.07, 0.12)
    g = _rng.uniform(0.22, 0.55)
    ellipsoid(pos=vec(_rng.uniform(5.68, 8.52), GF+0.10+r*0.35,
                      _rng.uniform(-6.52, -1.03)),
              length=r*2.4, height=r*1.2, width=r*2.0,
              color=vec(g, g*1.02, g*1.06))

# --- clean potted plants in the middle + bottom of the stairs
pot_plant(7.15, -5.4, GF+0.1, 1.5, 2, solid=False)   # tall palm  (back)
# low zen feature (all below 0.9 m so nothing touches the stairs)
PY = GF+0.10
cylinder(pos=vec(6.8, PY, -3.7), axis=vec(0, 0.32, 0), radius=0.46, color=vec(0.48, 0.45, 0.40))   # stone bowl
cylinder(pos=vec(6.8, PY+0.30, -3.7), axis=vec(0, 0.02, 0), radius=0.38, color=WATER)             # water
for k in range(4):
    a = k*pi/2+0.4
    ellipsoid(pos=vec(6.8+cos(a)*0.50, PY+0.34, -3.7+sin(a)*0.50),
              length=0.22, height=0.14, width=0.18, color=vec(0.30, 0.29, 0.28))
for (cx, cz, n) in ((7.45, -3.1, 4), (6.35, -4.55, 3)):                     # stacked stone cairns
    for k in range(n):
        r = 0.20-0.04*k
        ellipsoid(pos=vec(cx+0.02*k, PY+0.09+0.15*k, cz), length=r*2.2, height=0.16, width=r*2.0,
                  color=vec(0.32+0.05*k, 0.31+0.05*k, 0.30+0.05*k))
for (lx, lz) in ((7.5, -4.6), (6.3, -2.9)):                                 # low glowing lanterns
    cylinder(pos=vec(lx, PY, lz), axis=vec(0, 0.05, 0), radius=0.14, color=BLACK)
    lg = cylinder(pos=vec(lx, PY+0.05, lz), axis=vec(0, 0.42, 0), radius=0.11, color=vec(0.95, 0.90, 0.78))
    glow(lg, vec(0.95, 0.90, 0.78))
pot_plant(7.40, -2.5, GF+0.1, 1.0, 0, solid=False)   # small      (front)

# --- seating nook on the west side of the stairs (replaces the wall)
rug(4.3, 5.5, -6.2, -2.4, GF, vec(0.30, 0.38, 0.40), vec(0.85, 0.80, 0.68))
bn2 = F(5.15, -4.3, 3, GF)                      # long upholstered bench facing west
bn2.b(-1.0, 1.0, 0.0, 0.40, -0.25, 0.25, WOOD_D, solid=True)
bn2.b(-0.98, 0.98, 0.40, 0.52, -0.23, 0.23, FAB2)
bn2.b(-0.98, 0.98, 0.52, 0.95, 0.17, 0.25, FAB2)
for sx in (-0.55, 0.55):
    bn2.b(sx-0.2, sx+0.2, 0.52, 0.66, -0.16, 0.10, FAB3)
cylinder(pos=vec(4.55, GF, -5.75), axis=vec(0, 0.5, 0), radius=0.26, color=WOOD_D)    # round side table
cylinder(pos=vec(4.55, GF+0.5, -5.75), axis=vec(0, 0.04, 0), radius=0.3, color=GOLD)
table_lamp(4.55, GF+0.54, -5.75)
block(4.2, 4.9, -6.1, -5.4, 0, 0, -0.4, 0.9)
cylinder(pos=vec(4.55, GF, -2.85), axis=vec(0, 0.5, 0), radius=0.26, color=WOOD_D)
cylinder(pos=vec(4.55, GF+0.5, -2.85), axis=vec(0, 0.04, 0), radius=0.3, color=GOLD)
vase(4.55, GF+0.54, -2.85, vec(0.85, 0.80, 0.70), True)
block(4.2, 4.9, -3.2, -2.5, 0, 0, -0.4, 0.9)
floor_lamp(5.25, -6.4, GF, 1.7, True)

# --- foot of the stairs: stone side table + lamp + vase
cylinder(pos=vec(8.95, GF, -0.45), axis=vec(0, 0.55, 0), radius=0.3, color=vec(0.50, 0.46, 0.40))
cylinder(pos=vec(8.95, GF+0.55, -0.45), axis=vec(0, 0.04, 0), radius=0.34, color=GOLD)
table_lamp(8.95, GF+0.59, -0.45)
vase(9.15, GF+0.59, -0.35, vec(0.30, 0.45, 0.50), True)
block(8.6, 9.3, -0.8, -0.1, 0, 0, -0.4, 0.9)
# low floating bench under the high end of the stairs
sl(6.0, 7.9, GF+0.1, GF+0.42, -6.45, -6.0, WOOD_L, None)
slab(6.0, 7.9, GF+0.42, GF+0.52, -6.45, -6.0, FAB1L)
for xx in (6.3, 7.5):
    slab(xx, xx+0.45, GF+0.52, GF+0.7, -6.4, -6.2, FAB3)

# --- collision: under-stair bed is closed for ground walkers; open side is railed
block(5.6, 8.6, -6.6, -1.2, 0, 0, -1.0, 0.35)
block(5.45, 5.62, -6.7, -1.1, 0, 0, 0.5, 99.0)         # left (beam side)
block(7.98, 8.12, -6.7, -1.1, 0, 0, 0.5, 99.0)         # right (cable side)
block(5.6, 8.6, -0.9, -0.7, 0, 0, 4.5, 99.0)           # upper front edge
add_light(7.1, 3.0, -3.5)

# wine / plants at under-stair rear
# ------------------------------------------------------------
# KITCHEN  (right side, x 5.7..12.72)
# ------------------------------------------------------------
KB = vec(0.20, 0.28, 0.34)
KW = vec(0.92, 0.90, 0.85)
TILEW = vec(0.88, 0.90, 0.90)
# pantry tower + coffee bar
cabinet(5.7, 7.2, GF, 2.4, GZ0, -11.1, KW, 'z+', 2, 'g')
slab(5.7, 7.2, 2.4, 4.12, GZ0, -11.1, KW)
# sink run
cabinet(7.3, 9.9, GF, 0.95, GZ0, -10.82, KB, 'z+', 3, 'g')
sl(7.25, 9.95, 0.95, 1.0, GZ0, -10.78, MARBLE)
slab(8.0, 9.1, 0.995, 1.006, -11.55, -10.97, STEELD)
cylinder(pos=vec(8.55, 1.0, -11.55), axis=vec(0, 0.32, 0), radius=0.018, color=STEEL)
cylinder(pos=vec(8.55, 1.32, -11.55), axis=vec(0, 0, 0.2), radius=0.018, color=STEEL)
slab(9.35, 9.85, 1.0, 1.02, -11.6, -11.2, WOOD_L)
for k in range(4):
    cylinder(pos=vec(9.45+k*0.1, 1.02, -11.4), axis=vec(0, 0.2, 0), radius=0.04, color=WHITE)
plates(7.6, 1.0, -11.4, 3, 0.12, vec(0.85, 0.88, 0.9))
slab(7.3, 9.9, 1.0, 1.35, GZ0, GZ0+0.03, TILEW)
# cooktop + hood
cabinet(9.9, 11.7, GF, 0.95, GZ0, -10.82, KB, 'z+', 3, 'g')
sl(9.85, 11.75, 0.95, 1.0, GZ0, -10.78, MARBLE)
slab(10.3, 11.3, 1.0, 1.015, -11.6, -10.95, BLACK)
for (bx, bz) in ((10.55, -11.4), (11.05, -11.4), (10.55, -11.15), (11.05, -11.15)):
    cylinder(pos=vec(bx, 1.015, bz), axis=vec(0, 0.012, 0), radius=0.09, color=STEELD)
cylinder(pos=vec(10.55, 1.015, -11.4), axis=vec(0, 0.14, 0), radius=0.11, color=STEEL)
cylinder(pos=vec(10.55, 1.155, -11.4), axis=vec(0, 0.02, 0), radius=0.115, color=STEELD)
slab(10.1, 11.5, 2.0, 2.3, GZ0, -11.2, STEEL)
slab(10.55, 11.05, 2.3, 4.12, GZ0, -11.45, STEEL)
slab(9.9, 11.7, 1.0, 2.0, GZ0, GZ0+0.03, TILEW)
for yy in (1.3, 1.6, 1.9):
    slab(9.9, 11.7, yy, yy+0.012, GZ0, GZ0+0.035, vec(0.7, 0.74, 0.74))
rail(vec(10.0, 1.8, -11.6), vec(11.6, 1.8, -11.6), 0.012, STEEL)
for k in range(4):
    rail(vec(10.2+k*0.4, 1.8, -11.6), vec(10.2+k*0.4, 1.45, -11.6), 0.012, STEEL)
    cylinder(pos=vec(10.2+k*0.4, 1.28, -11.6), axis=vec(0, 0.012, 0), radius=0.1, color=STEELD)
# fridge
sl(11.72, 12.7, GF, 2.1, GZ0, -10.82, STEEL, 'g')
slab(11.74, 12.68, 1.4, 1.42, -10.82, -10.80, BLACK)
slab(11.74, 12.68, 0.9, 0.92, -10.82, -10.80, BLACK)
slab(12.2, 12.22, 0.9, 2.08, -10.82, -10.80, BLACK)
slab(12.1, 12.14, 1.45, 1.95, -10.80, -10.76, STEELD)
slab(12.3, 12.34, 1.45, 1.95, -10.80, -10.76, STEELD)
slab(12.1, 12.14, 0.4, 1.2, -10.80, -10.76, STEELD)
slab(12.3, 12.34, 0.4, 1.2, -10.80, -10.76, STEELD)
sl(11.72, 12.7, 2.2, 3.1, GZ0, -11.3, KW)
for xx in (12.2,):
    slab(xx, xx+0.02, 2.2, 3.1, -11.3, -11.28, vec(0.7, 0.7, 0.68))
# right-wall run
cabinet(11.82, 12.7, GF, 0.95, -10.7, -4.0, KB, 'x-', 7, 'g')
sl(11.77, 12.72, 0.95, 1.0, -10.75, -3.95, MARBLE)
slab(12.68, 12.72, 1.0, 1.35, -10.7, -4.0, TILEW)
mw = slab(12.2, 12.65, 1.0, 1.3, -10.3, -9.7, vec(0.18, 0.18, 0.2))
slab(12.18, 12.2, 1.04, 1.26, -10.25, -9.95, vec(0.1, 0.14, 0.16))
cylinder(pos=vec(12.4, 1.0, -9.2), axis=vec(0, 0.2, 0), radius=0.09, color=STEEL)       # kettle
slab(12.2, 12.55, 1.0, 1.2, -8.8, -8.4, vec(0.75, 0.2, 0.2))                           # toaster
cylinder(pos=vec(12.4, 1.0, -7.6), axis=vec(0, 0.28, 0), radius=0.15, color=WHITE)       # rice cooker
fruit_bowl(12.3, 1.0, -6.9)
slab(12.1, 12.6, 1.0, 1.03, -5.7, -5.0, WOOD_L)                                         # cutting board
slab(12.35, 12.5, 1.03, 1.3, -5.0, -4.8, WOOD_D)                                        # knife block
mug(12.3, 1.0, -6.3, vec(0.8, 0.4, 0.3))
mug(12.4, 1.0, -6.1, vec(0.25, 0.38, 0.45))
# open shelves with plates + glasses
for yy in (1.55, 2.05):
    slab(12.45, 12.72, yy, yy+0.04, -5.9, -4.1, WOOD_L)
    for k in range(4):
        plates(12.6, yy+0.04, -5.7+k*0.45, 4, 0.11, vec(0.9, 0.92, 0.94) if k % 2 else vec(0.25, 0.38, 0.45))
for k in range(6):
    cylinder(pos=vec(12.55, 2.09, -5.8+k*0.28), axis=vec(0, 0.14, 0), radius=0.03,
             color=vec(0.8, 0.9, 0.95), opacity=0.6)
slab(12.45, 12.72, 2.55, 2.59, -5.9, -4.1, WOOD_L)
for k in range(5):
    cylinder(pos=vec(12.6, 2.59, -5.7+k*0.35), axis=vec(0, 0.2, 0), radius=0.05,
             color=random.choice([vec(0.3, 0.5, 0.35), vec(0.7, 0.45, 0.25)]))
# oven tower
sl(11.82, 12.72, GF, 2.2, -4.0, -3.15, STEEL, 'g')
slab(11.78, 11.82, 0.6, 1.3, -3.95, -3.2, vec(0.08, 0.1, 0.12))
slab(11.78, 11.82, 1.45, 2.1, -3.95, -3.2, vec(0.08, 0.1, 0.12))
slab(11.76, 11.8, 1.38, 1.42, -3.95, -3.2, STEELD)
# breakfast banquette + table
sl(12.0, 12.72, GF, 0.5, -3.0, -0.9, WOOD_D, 'g')
slab(12.0, 12.72, 0.5, 0.6, -3.0, -0.9, FAB2)
slab(12.62, 12.72, 0.6, 0.95, -3.0, -0.9, FAB2)
slab(12.05, 12.35, 0.6, 0.85, -2.7, -2.3, FAB3)
cylinder(pos=vec(11.3, GF, -1.95), axis=vec(0, 0.52, 0), radius=0.05, color=BLACK)
cylinder(pos=vec(11.3, GF+0.52, -1.95), axis=vec(0, 0.04, 0), radius=0.55, color=WOOD_L)
block(10.7, 11.9, -2.6, -1.3, 0, 0, -1, 1.2)
vase(11.3, GF+0.56, -1.95, vec(0.85, 0.80, 0.70), True)
chair(F(10.45, -1.95, 1, GF), WOOD_D, FAB1L)
chair(F(11.3, -0.95, 2, GF), WOOD_D, FAB1L)
rail(vec(11.3, 4.12, -1.95), vec(11.3, 2.7, -1.95), 0.01, GOLD)
g = cylinder(pos=vec(11.3, 2.4, -1.95), axis=vec(0, 0.3, 0), radius=0.28, color=vec(0.95, 0.9, 0.8))
glow(g, vec(0.95, 0.9, 0.8))
# island
cabinet(8.9, 10.8, GF, 0.95, -9.3, -7.7, KB, 'z+', 3, 'g')
sl(8.8, 10.9, 0.95, 1.04, -9.4, -7.55, MARBLE)
fruit_bowl(9.4, 1.04, -8.5)
slab(9.9, 10.6, 1.04, 1.07, -8.9, -8.5, WOOD_L)
plates(10.3, 1.07, -8.7, 2, 0.1, WHITE)
vase(10.6, 1.04, -9.1, vec(0.5, 0.65, 0.55), True)
for xx in (9.25, 9.85, 10.45):
    stool(F(xx, -7.1, 0, GF))
for xx in (9.3, 9.85, 10.4):
    rail(vec(xx, 4.12, -8.5), vec(xx, 2.75, -8.5), 0.01, GOLD)
    g = sphere(pos=vec(xx, 2.6, -8.5), radius=0.17, color=vec(0.95, 0.9, 0.8), opacity=0.92)
    glow(g, vec(0.95, 0.9, 0.8))
add_light(9.85, 2.9, -8.5)
add_light(10.8, 3.2, -2.0)
pot_plant(6.3, -10.2, GF, 1.1, 0, solid=False)
downlights([(8.2, -6.0), (10.2, -5.5), (11.5, -9.0), (8.2, -10.0), (11.0, -1.0), (7.0, -9.0), (5.0, -2.0)], 4.08)

# ============================================================
# SECOND FLOOR (wing)  x -1.1..11.3 , z -8.92..0 , ceiling 8.2
# ============================================================
WX0, WX1, WZ0, WZ1 = -1.1, 11.3, -8.92, 0.0
PCOL = vec(0.93, 0.91, 0.86)
planks(WX0, 5.5, WZ0, WZ1, UF, vec(0.64, 0.50, 0.36), vec(0.50, 0.38, 0.26), 0.7)
planks(5.5, WX1, WZ0, -6.94, UF, vec(0.64, 0.50, 0.36), vec(0.50, 0.38, 0.26), 0.7)
planks(-1.2, 13.3, 0.05, 2.85, UF, vec(0.58, 0.45, 0.32), vec(0.42, 0.32, 0.22), 0.45)
tiles(8.76, WX1, -6.94, WZ1, UF, vec(0.84, 0.88, 0.88), vec(0.66, 0.74, 0.76), 0.6)
slab(5.5, 8.7, UF, UF+0.01, -0.8, 0.0, vec(0.64, 0.50, 0.36))
skirt(WX0, 5.5, WZ0, WZ1, UF)
cove(WX0, WX1, WZ0, WZ1, 8.14)

# --- walls of the wing (collision)
wb(-1.3, 11.3, -9.3, WZ0, 'u')                  # back wall
wb(11.3, 13.4, -9.3, 0.7, 'u')                  # right wall block
wb(-1.3, 3.95, -0.15, 0.15, 'u')                # front glass left part
wb(5.4, 13.4, -0.15, 0.15, 'u')                 # front glass right part
wb(-1.6, -1.3, 0.1, 3.2, 'u')                   # terrace left edge
wb(-1.6, 13.5, 2.85, 3.2, 'u')                  # terrace front rail
wb(13.3, 13.6, 0.6, 3.2, 'u')                   # terrace right edge
wb(-1.25, -1.05, -9.2, -8.5, 'u')               # left wall + door gap -8.5..-7.2
wb(-1.25, -1.05, -7.2, 0.7, 'u')
# --- partitions
def pwall(x0, x1, z0, z1, h0=UF, h1=8.2):
    sl(x0, x1, h0, h1, z0, z1, PCOL, 'u')


pwall(-1.1, 0.3, -7.06, -6.94)
pwall(1.5, 5.44, -7.06, -6.94)
pwall(8.76, 9.3, -7.06, -6.94)
pwall(10.4, 11.3, -7.06, -6.94)
pwall(5.44, 5.56, -7.0, 0.0)
pwall(8.64, 8.76, -7.0, 0.0)
sl(0.3, 1.5, UF+2.1, 8.2, -7.06, -6.94, PCOL)
sl(9.3, 10.4, UF+2.1, 8.2, -7.06, -6.94, PCOL)
for (a, b) in ((0.3, 1.5), (9.3, 10.4)):
    slab(a-0.05, a, UF, UF+2.1, -7.1, -6.9, WOOD_D)
    slab(b, b+0.05, UF, UF+2.1, -7.1, -6.9, WOOD_D)
    slab(a-0.05, b+0.05, UF+2.1, UF+2.16, -7.1, -6.9, WOOD_D)
slab(1.45, 1.5, UF, UF+2.1, -6.9, -6.0, WOOD_L)                   # bedroom door open
slab(9.3, 9.36, UF, UF+2.1, -7.9, -7.0, WOOD_L)                   # bath door open
slab(1.38, 1.42, UF+1.0, UF+1.1, -6.3, -6.2, GOLD)
slab(9.3, 9.34, UF+1.0, UF+1.1, -7.8, -7.7, GOLD)
# stairwell edge guards on the 2nd floor
block(5.6, 8.6, -0.9, -0.7, 0, 0, 4.5, 99.0)

# ---------------- HALL (z -8.92..-7.0)
slab(-0.6, 10.9, UF, UF+0.012, -8.3, -7.65, vec(0.28, 0.40, 0.42))
slab(-0.5, 10.8, UF+0.012, UF+0.016, -8.2, -7.75, vec(0.85, 0.80, 0.68))
hc = F(5.3, WZ0, 0, UF)
hc.b(-0.8, 0.8, 0.72, 0.78, 0.0, 0.4, WOOD_D, solid=True)
for sx in (-0.76, 0.7):
    hc.b(sx, sx+0.06, 0, 0.72, 0.02, 0.08, GOLD)
    hc.b(sx, sx+0.06, 0, 0.72, 0.3, 0.36, GOLD)
mirror(hc, 0, 1.0, 1.0, 1.6)
vase(4.8, UF+0.78, -8.7, vec(0.85, 0.78, 0.60), True)
table_lamp(5.9, UF+0.78, -8.7)
bh = F(3.0, -7.06, 2, UF)
bh.b(-0.9, 0.9, 0.38, 0.46, 0.0, 0.42, WOOD_L, solid=True)
bh.b(-0.88, 0.88, 0.46, 0.56, 0.02, 0.4, FAB2)
bh.b(-0.88, -0.1, 0.56, 0.58, 0.02, 0.4, FAB3)
art(bh, 0, 1.45, 1.4, 0.8, 0)
drapes_x(-0.67, 3.5, 6.17, 7.95, WZ0, 1)
drapes_x(7.0, 10.83, 6.17, 7.95, WZ0, 1)
sill_x(-0.67, 3.5, 6.17, WZ0, 1)
sill_x(7.0, 10.83, 6.17, WZ0, 1)
add_light(5.5, 7.6, -8.0)
downlights([(-0.2, -8.0), (4.0, -8.0), (6.5, -8.0), (6.5, -7.4), (10.5, -8.0)], 8.15)

# ---------------- MASTER BEDROOM (x -1.1..5.4, z -6.94..0)
sl(-1.1, -0.98, UF, 8.2, -6.9, -0.1, vec(0.40, 0.46, 0.48))
for k in range(18):
    slab(-0.98, -0.95, UF, 8.2, -6.7+k*0.36, -6.67+k*0.36, vec(0.30, 0.34, 0.36))
rug(-0.8, 3.4, -5.9, -1.1, UF, vec(0.80, 0.76, 0.68), vec(0.40, 0.48, 0.52))
bed(F(0.05, -3.5, 1, UF), 2.0, 2.3, vec(0.92, 0.90, 0.86), FAB2)
nightstand(F(-0.85, -4.85, 1, UF))
nightstand(F(-0.85, -2.15, 1, UF))
table_lamp(-0.85, UF+0.62, -4.85)
table_lamp(-0.85, UF+0.62, -2.15)
for zz in (-4.85, -2.15):
    rail(vec(-0.6, 8.2, zz), vec(-0.6, 7.2, zz), 0.008, GOLD)
    g = sphere(pos=vec(-0.6, 7.1, zz), radius=0.14, color=vec(0.95, 0.9, 0.8))
    glow(g, vec(0.95, 0.9, 0.8))
add_light(-0.6, 7.0, -3.5)
art(F(-1.1, -3.5, 1, UF), 0, 1.75, 1.7, 0.85, 1)
ot = F(1.75, -3.5, 1, UF)
ot.b(-0.8, 0.8, 0.0, 0.42, -0.25, 0.25, vec(0.55, 0.32, 0.26), solid=True)
ot.b(-0.8, 0.8, 0.42, 0.5, -0.25, 0.25, FAB1L)
wardrobe(F(3.55, -6.94, 0, UF), 3.4)
dr = F(5.44, -3.6, 3, UF)
dr.b(-0.9, 0.9, 0.0, 0.85, 0.0, 0.5, WOOD_L, solid=True)
for sx in (-0.6, 0.0, 0.6):
    dr.b(sx-0.28, sx+0.28, 0.1, 0.78, 0.5, 0.52, WOOD_D)
    dr.b(sx-0.08, sx+0.08, 0.6, 0.63, 0.52, 0.55, GOLD)
tv(dr, 0, 1.15, 1.4, 0.8)
table_lamp(*dr.w(-0.7, 0.25)[:1], UF+0.85, dr.w(-0.7, 0.25)[1])
vase(*dr.w(0.7, 0.25)[:1], UF+0.85, dr.w(0.7, 0.25)[1], vec(0.85, 0.8, 0.7), True)
armchair(F(0.5, -0.9, 0, UF), FAB3)
cylinder(pos=vec(1.4, UF, -0.8), axis=vec(0, 0.5, 0), radius=0.22, color=GOLD)
table_lamp(1.4, UF+0.5, -0.8)
block(1.1, 1.7, -1.1, -0.5, 0, 0, UF-0.6, UF+0.8)
floor_lamp(-0.55, -0.5, UF, 1.65, True)
pot_plant(3.2, -0.5, UF, 1.2, 1)
chandelier(2.3, 8.2, -3.5, 0.5, 0.65, 2)
add_light(2.3, 7.5, -3.5)
# --- east wall of the master bedroom: paintings + extra furniture
mb_shelf = F(5.44, -5.7, 3, UF)                      # low bookcase / credenza under a painting
bookcase(mb_shelf, 1.0, 1.1, 3, 0.38)
art(F(5.44, -5.7, 3, UF), 0, 1.5, 0.95, 0.85, 0)
vase(*mb_shelf.w(0.0, 0.2)[:1], UF+1.1, mb_shelf.w(0.0, 0.2)[1], vec(0.85, 0.8, 0.7), True)
art(F(5.44, -4.9, 3, UF), 0, 1.25, 0.4, 0.7, 2)      # slim painting left of the TV
art(F(5.44, -2.3, 3, UF), 0, 1.25, 0.4, 0.7, 1)      # slim painting right of the TV
mb_chair = F(4.9, -1.2, 3, UF)                       # reading chair + painting + lamp
armchair(mb_chair, FAB2)
art(F(5.44, -1.2, 3, UF), 0, 1.35, 1.1, 0.9, 1)
cylinder(pos=vec(4.9, UF, -0.35), axis=vec(0, 0.5, 0), radius=0.22, color=WOOD_D)
cylinder(pos=vec(4.9, UF+0.5, -0.35), axis=vec(0, 0.04, 0), radius=0.26, color=GOLD)
table_lamp(4.9, UF+0.54, -0.35)
block(4.65, 5.15, -0.6, -0.1, 0, 0, UF-0.6, UF+0.9)
# sliding door frame + handle (opening onto the terrace)
slab(3.9, 3.98, UF, 8.1, -0.1, 0.1, BLACK)
slab(5.4, 5.46, UF, 8.1, -0.1, 0.1, BLACK)
slab(5.0, 5.04, 6.6, 7.2, 0.08, 0.14, GOLD)
downlights([(0.5, -6.0), (4.5, -6.0), (4.5, -1.0), (2.2, -1.0)], 8.15)

# ---------------- BATHROOM (x 8.76..11.3, z -6.94..0)
BWT = vec(0.86, 0.90, 0.90)
slab(11.26, 11.3, UF, UF+2.5, -6.94, 0.0, BWT)
slab(8.76, 8.8, UF, UF+2.5, -6.94, 0.0, BWT)
for yy in (0.6, 1.2, 1.8):
    slab(11.255, 11.3, UF+yy, UF+yy+0.02, -6.94, 0.0, vec(0.6, 0.7, 0.72))
    slab(8.76, 8.805, UF+yy, UF+yy+0.02, -6.94, 0.0, vec(0.6, 0.7, 0.72))
slab(8.76, 11.3, UF+2.5, UF+2.56, -6.94, 0.0, WHITE)
slab(8.8, 11.26, 5.9, 8.15, -0.14, -0.11, vec(0.95, 0.97, 0.98), 0.5)       # frosted glass
# shower
slab(10.2, 11.3, UF, UF+0.07, -6.9, -5.4, WHITE)
slab(10.2, 10.9, UF, UF+2.2, -5.42, -5.38, GLASS, 0.28)
slab(10.18, 10.22, UF, UF+2.2, -6.9, -5.4, GLASS, 0.28)
slab(10.2, 10.9, UF+2.18, UF+2.24, -5.44, -5.36, STEEL)
wb(10.15, 11.3, -6.95, -5.35, 'u')
rail(vec(11.2, UF+0.9, -6.2), vec(11.2, UF+2.15, -6.2), 0.02, STEEL)
rail(vec(11.2, UF+2.15, -6.2), vec(10.85, UF+2.15, -6.2), 0.02, STEEL)
cylinder(pos=vec(10.85, UF+2.12, -6.2), axis=vec(0, 0.03, 0), radius=0.2, color=STEEL)
slab(11.18, 11.3, UF+1.3, UF+1.34, -6.8, -6.4, STEEL)
for k in range(3):
    cylinder(pos=vec(11.22, UF+1.34, -6.7+k*0.15), axis=vec(0, 0.18, 0), radius=0.03,
             color=[vec(0.3, 0.55, 0.7), vec(0.85, 0.7, 0.3), vec(0.9, 0.9, 0.9)][k])
for k in range(5):
    sphere(pos=vec(10.9+0.05*sin(k*2.0), UF+2.0-0.35*k, -6.2+0.04*k), radius=0.02,
           color=vec(0.8, 0.92, 1.0), opacity=0.5)
# toilet (right wall)
def toilet(f):
    f.b(-0.2, 0.2, 0.0, 0.05, 0.1, 0.62, WHITE)
    f.b(-0.22, 0.22, 0.45, 0.95, 0.0, 0.2, WHITE)
    f.b(-0.04, 0.04, 0.95, 0.98, 0.07, 0.13, STEEL)
    f.ell(0, 0.28, 0.38, 0.42, 0.36, 0.6, WHITE)
    f.cyl(0, 0.38, 0.46, 0.03, 0.22, WHITE)
    f.blk(-0.3, 0.3, 0.0, 0.8, 0.0, 0.7)
    f.b(0.32, 0.36, 0.55, 0.75, 0.0, 0.1, STEEL)


toilet(F(11.3, -4.3, 3, UF))
# freestanding tub
sl(10.25, 11.25, UF, UF+0.62, -2.75, -0.45, WHITE, 'u')
slab(10.33, 11.17, UF+0.58, UF+0.6, -2.67, -0.53, WATER)
slab(10.2, 11.3, UF+0.62, UF+0.66, -2.8, -0.4, WHITE)
rail(vec(10.75, UF+0.6, -2.7), vec(10.75, UF+1.0, -2.7), 0.02, STEEL)
rail(vec(10.75, UF+1.0, -2.7), vec(10.75, UF+0.9, -2.5), 0.02, STEEL)
for k in range(6):
    sphere(pos=vec(10.45+0.12*k, UF+0.68, -1.6+0.1*sin(k*2)), radius=0.05, color=WHITE, opacity=0.85)
slab(9.5, 10.15, UF+0.012, UF+0.02, -2.5, -1.2, vec(0.80, 0.84, 0.86))
# vanity
def vanity(f, w, basins=1):
    f.b(-w/2, w/2, 0.0, 0.82, 0.0, 0.5, WOOD_L, solid=True)
    f.b(-w/2-0.02, w/2+0.02, 0.82, 0.88, -0.02, 0.52, WHITE)
    n = max(2, int(w/0.5))
    cw = w/n
    for i in range(n):
        xa = -w/2+i*cw
        f.b(xa+0.02, xa+cw-0.02, 0.05, 0.78, 0.5, 0.52, WOOD_D)
        f.b(xa+cw/2-0.08, xa+cw/2+0.08, 0.7, 0.73, 0.52, 0.55, GOLD)
    for k in range(basins):
        lx = -w/4*(basins-1)+k*(w/2)*(basins-1) if basins > 1 else 0
        f.ell(lx, 0.88, 0.27, 0.42, 0.12, 0.36, vec(0.95, 0.95, 0.97))
        f.cyl(lx, 0.08, 0.88, 0.2, 0.012, STEEL)
        f.b(lx-0.01, lx+0.01, 1.06, 1.09, 0.08, 0.2, STEEL)
    mirror(f, 0, 1.25, w*0.92, 1.2)
    for sx in (-w/2-0.05, w/2+0.05):
        sc = f.b(sx-0.04, sx+0.04, 1.75, 2.1, 0.0, 0.1, vec(0.95, 0.9, 0.8))
        glow(sc, vec(0.95, 0.9, 0.8))


vanity(F(8.76, -4.1, 1, UF), 1.8, 2)
rail(vec(8.85, UF+1.3, -2.0), vec(8.85, UF+1.3, -1.2), 0.015, STEEL)
slab(8.82, 8.88, UF+0.7, UF+1.3, -1.95, -1.5, vec(0.85, 0.88, 0.9))
slab(8.82, 8.88, UF+0.8, UF+1.3, -1.45, -1.25, vec(0.55, 0.70, 0.75))
pot_plant(9.6, -0.5, UF, 0.8, 0, solid=False)
cove(8.76, WX1, -6.94, 0.0, 8.14)
downlights([(9.6, -5.5), (10.0, -3.0), (10.0, -1.0)], 8.15)
add_light(9.8, 7.5, -3.5)

# ---------------- STAIRWELL GLASS / PLANT at the front
pot_plant(7.1, -0.4, UF, 1.4, 2, solid=False)

# ============================================================
# COURTYARD (between tower and wing, y = UF)
# ============================================================
planks(-3.6, -1.2, -8.95, -0.1, UF, vec(0.56, 0.42, 0.30), vec(0.40, 0.30, 0.20), 0.4)
wb(-3.7, -1.2, -0.1, 0.25, 'u')
wb(-3.7, -1.2, -9.3, -8.9, 'u')
wb(-3.6, -1.7, -1.0, 0.3, 'u')
bc2 = F(-2.4, -8.88, 0, UF)
bc2.b(-0.8, 0.8, 0.40, 0.46, 0.0, 0.4, WOOD_L, solid=True)
bc2.b(-0.8, 0.8, 0.46, 0.5, 0.02, 0.38, FAB2)
for sx in (-0.7, 0.7):
    bc2.b(sx-0.03, sx+0.03, 0, 0.4, 0.05, 0.35, BLACK)
cylinder(pos=vec(-2.4, UF, -5.0), axis=vec(0, 0.5, 0), radius=0.4, color=WOOD_D)
cylinder(pos=vec(-2.4, UF+0.5, -5.0), axis=vec(0, 0.04, 0), radius=0.45, color=GOLD)
block(-2.9, -1.9, -5.5, -4.5, 0, 0, UF-0.6, UF+0.9)
fruit_bowl(-2.4, UF+0.54, -5.0)
chair(F(-3.2, -5.0, 1, UF), WOOD_D, FAB1L)
chair(F(-1.6, -5.0, 3, UF), WOOD_D, FAB1L)
armchair(F(-3.0, -6.2, 1, UF), FAB3)                  # lounge chair (was tall palm)
floor_lamp(-3.3, -6.95, UF, 1.7, True)
cylinder(pos=vec(-1.75, UF, -2.3), axis=vec(0, 0.5, 0), radius=0.22, color=WOOD_D)   # side table (was agave)
cylinder(pos=vec(-1.75, UF+0.5, -2.3), axis=vec(0, 0.04, 0), radius=0.26, color=GOLD)
vase(-1.75, UF+0.54, -2.3, vec(0.30, 0.45, 0.50), True)
block(-2.05, -1.45, -2.6, -2.0, 0, 0, UF-0.6, UF+0.9)
bc3 = F(-3.35, -3.1, 1, UF)                            # cushioned bench by the wall (was bonsai)
bc3.b(-0.8, 0.8, 0.0, 0.42, 0.0, 0.40, WOOD_L, solid=True)
bc3.b(-0.78, 0.78, 0.42, 0.52, 0.02, 0.38, FAB2)
bc3.b(-0.5, -0.1, 0.52, 0.72, 0.1, 0.3, FAB3)
art(F(-3.59, -3.1, 1, UF), 0, 1.3, 1.1, 0.8, 0)
add_light(-2.4, 7.0, -4.5)

# ============================================================
# TERRACE (front of second floor)
# ============================================================
sofa(F(8.0, 0.85, 0, UF), 2.8, vec(0.78, 0.74, 0.66), vec(0.93, 0.90, 0.84), FAB2)
coffee_table(F(8.0, 1.9, 0, UF), 1.3, 0.7)
armchair(F(10.6, 1.55, 0, UF), vec(0.78, 0.74, 0.66))
armchair(F(5.9, 1.55, 0, UF), vec(0.78, 0.74, 0.66))
rail(vec(8.0, UF, 2.4), vec(8.0, UF+2.3, 2.4), 0.03, BLACK)
cone(pos=vec(8.0, UF+2.3, 2.4), axis=vec(0, 0.45, 0), radius=1.7, color=vec(0.93, 0.89, 0.78))
block(7.9, 8.1, 2.3, 2.5, 0, 0, UF-0.6, UF+0.9)
pot_plant(12.4, 1.2, UF, 1.5, 2)
pot_plant(-0.5, 1.2, UF, 1.5, 2)
pot_plant(2.4, 2.4, UF, 1.2, 1)
pot_plant(4.6, 2.4, UF, 1.2, 0)
vase(8.0, UF+0.42, 1.9, vec(0.8, 0.5, 0.3), True)
# ============================================================
# TOWER LOUNGE  (double height, x -11.3..-3.7, z -9..-0.2)
# ============================================================
planks(-11.3, -3.7, -9.0, -0.2, UF, vec(0.50, 0.36, 0.24), vec(0.38, 0.26, 0.17), 0.5, 'x')
skirt(-11.3, -3.7, -8.96, -0.2, UF)
cove(-11.3, -3.7, -8.96, -0.2, 11.1)
# collision shell of the tower
wb(-11.6, -11.2, -9.3, 1.1, 't')
wb(-11.5, -3.5, -9.3, -8.96, 't')
wb(-3.75, -3.55, -9.3, -8.5, 't')
wb(-3.75, -3.55, -7.2, -3.0, 't')
wb(-4.55, -3.55, -3.0, 1.1, 't')
wb(-11.5, -3.5, -0.3, 0.3, 't')
wb(-11.3, -10.6, -3.0, 1.1, 't')
rug(-10.0, -5.0, -6.0, -1.7, UF, vec(0.58, 0.30, 0.26), vec(0.88, 0.82, 0.68))
sofa(F(-9.9, -3.85, 1, UF), 2.8, FAB1, FAB1L, FAB2)
sofa(F(-5.3, -3.85, 3, UF), 2.8, vec(0.35, 0.45, 0.48), FAB1L, FAB3)
coffee_table(F(-7.6, -3.85, 0, UF), 1.6, 1.0, 0.42, WOOD_D)
vase(-7.7, UF+0.42, -3.9, vec(0.3, 0.45, 0.5), True)
fruit_bowl(-7.3, UF+0.42, -3.7)
books(F(-7.6, -3.85, 0, UF), 0.4, 0.7, 0.42, -0.3, 0.0)
armchair(F(-7.6, -5.3, 0, UF), FAB3)
armchair(F(-9.2, -1.15, 2, UF), vec(0.30, 0.42, 0.46))
pot_plant(-4.3, -1.0, UF, 1.7, 2)
pot_plant(-10.3, -1.0, UF, 1.7, 2)
floor_lamp(-6.4, -0.9, UF, 1.8, True)
# bookcase wall with ladder
bookcase(F(-3.72, -5.1, 3, UF), 3.6, 4.7, 7, 0.35)
rail(vec(-4.15, UF, -3.6), vec(-4.05, UF+3.6, -3.6), 0.02, WOOD_L)
rail(vec(-4.15, UF, -3.2), vec(-4.05, UF+3.6, -3.2), 0.02, WOOD_L)
for k in range(8):
    rail(vec(-4.15+0.014*k, UF+0.3+0.45*k, -3.6), vec(-4.15+0.014*k, UF+0.3+0.45*k, -3.2), 0.015, WOOD_L)
# art on pillar + chandelier
art(F(-10.6, -1.2, 1, UF), 0, 1.4, 1.5, 1.0, 1)
chandelier(-7.5, 11.2, -3.9, 1.3, 1.25, 4)
add_light(-7.5, 9.6, -3.9)
add_light(-10.0, 7.5, -1.5)
for z in (-7.5, -5.5):
    g = sphere(pos=vec(-4.4, 8.6, z), radius=0.12, color=vec(0.95, 0.9, 0.8))
    glow(g, vec(0.95, 0.9, 0.8))
drapes_z(-8.0, -4.4, 6.3, 10.3, -11.3, 1)
sill_z(-8.0, -4.4, 6.3, -11.3, 1)

# ---- tower staircase (x -11.0 -> -6.2, z -8.55..-7.25) up to the sky bridge
NT = 11
DXS = 4.8/NT
RT = (SF-UF)/NT
for i in range(NT):
    xa = -11.0+i*DXS
    xb = xa+DXS
    top = UF+(i+1)*RT
    slab(xa, xb, top-SLAB_T, top-0.03, -8.95, -7.30, STONE_SIDE)          # chunky slab fixed into the wall
    slab(xa+0.01, xb-0.01, top-0.03, top, -8.94, -7.31, STONE_TOP)
    if i % 2 == 0:
        g = slab(xa+0.06, xb-0.06, top-SLAB_T-0.02, top-SLAB_T, -8.85, -7.45, vec(0.30, 0.24, 0.18))
        glow(g, vec(0.30, 0.24, 0.18))
    if i % 4 == 0:
        rail(vec(xa+DXS/2, top, -7.35), vec(xa+DXS/2, top+0.95, -7.35), 0.014, BLACK)
rail(vec(-11.0+DXS/2, UF+RT+0.95, -7.35), vec(-6.2-DXS/2, SF+0.95, -7.35), 0.03, WOOD_D)
for hh in (0.32, 0.64):
    rail(vec(-11.0+DXS/2, UF+RT+hh, -7.35), vec(-6.2-DXS/2, SF+hh, -7.35), 0.008, STEEL)
# pebble bed under the stairs with low stone accents
slab(-10.2, -6.3, UF, UF+0.03, -8.9, -7.35, vec(0.22, 0.21, 0.20))
for _ in range(170):
    r = _rng.uniform(0.06, 0.10)
    g = _rng.uniform(0.22, 0.55)
    ellipsoid(pos=vec(_rng.uniform(-10.1, -6.4), UF+0.03+r*0.35, _rng.uniform(-8.85, -7.4)),
              length=r*2.4, height=r*1.2, width=r*2.0, color=vec(g, g*1.02, g*1.06))
for (cx, cz, n) in ((-8.9, -8.2, 4), (-7.1, -7.7, 3)):
    for k in range(n):
        r = 0.18-0.035*k
        ellipsoid(pos=vec(cx+0.02*k, UF+0.12+0.14*k, cz), length=r*2.2, height=0.15, width=r*2.0,
                  color=vec(0.32+0.05*k, 0.31+0.05*k, 0.30+0.05*k))
for (lx, lz) in ((-9.8, -7.8), (-8.0, -8.3)):
    cylinder(pos=vec(lx, UF+0.03, lz), axis=vec(0, 0.05, 0), radius=0.13, color=BLACK)
    lg = cylinder(pos=vec(lx, UF+0.08, lz), axis=vec(0, 0.38, 0), radius=0.10, color=vec(0.95, 0.90, 0.78))
    glow(lg, vec(0.95, 0.90, 0.78))
slab(-6.2, -5.5, SF, SF+1.0, -7.06, -7.0, GLASS, 0.28)
slab(-6.2, -5.5, SF+0.98, SF+1.02, -7.1, -6.96, GOLD)
block(-10.2, -6.3, -8.95, -7.25, 0, 0, 5.0, 6.0)         # under the stairs
block(-10.2, -6.3, -8.62, -8.55, 0, 0, 6.1, 9.6)         # stair side rails
block(-10.2, -6.3, -7.25, -7.18, 0, 0, 6.1, 9.6)
block(-6.2, -5.5, -7.1, -6.98, 0, 0, 9.0, 99.0)           # landing glass rail

# ============================================================
# SKY ROOM  (floor y 9.82, x -5.3..5.66, z -8.44..-0.62)
# ============================================================
cove(-5.3, 5.66, -8.44, -0.62, 12.86)
_sk = vec(0.95, 0.93, 0.88)
slab(-5.3, 5.66, SF, SF+0.13, -8.44, -8.41, _sk)          # rear
slab(-5.3, 5.66, SF, SF+0.13, -0.65, -0.62, _sk)          # front
slab(5.63, 5.66, SF, SF+0.13, -8.44, -0.62, _sk)          # east
slab(-5.3, -5.27, SF, SF+0.13, -5.2, -2.4, _sk)           # west: only behind the TV
# open landing: glass balustrade so the stairs going down are visible
slab(-6.24, -6.20, 9.82, 10.82, -7.06, -5.46, GLASS, 0.28)
slab(-6.2, -5.7, 9.82, 10.82, -5.50, -5.46, GLASS, 0.28)
rail(vec(-6.22, 10.82, -7.06), vec(-6.22, 10.82, -5.46), 0.03, GOLD)
rail(vec(-6.22, 10.82, -5.48), vec(-5.7, 10.82, -5.48), 0.03, GOLD)
rail(vec(-5.42, 10.82, -5.5), vec(-5.42, 10.82, -5.2), 0.03, GOLD)
rail(vec(-5.42, 10.82, -2.4), vec(-5.42, 10.82, -0.62), 0.03, GOLD)
wb(-5.7, -5.3, -5.5, -0.3, 's')
block(-6.28, -6.18, -7.0, -5.4, 0, 0, 9.0, 99.0)      # landing glass rail (west)
block(-6.2, -5.7, -5.55, -5.45, 0, 0, 9.0, 99.0)      # landing glass rail (south)
wb(-5.7, -5.3, -8.7, -8.45, 's')
wb(5.66, 5.95, -8.7, -0.3, 's')
wb(-5.7, 5.95, -8.8, -8.44, 's')
wb(-5.7, 5.95, -0.7, -0.3, 's')
rug(-4.2, 3.2, -6.2, -1.3, SF, vec(0.30, 0.38, 0.42), vec(0.85, 0.80, 0.68))
# cinema wall (left wall)
# TV mounted on the wall (no cabinet / shelf sticking out)
slab(-5.30, -5.24, SF+1.0, SF+2.45, -5.1, -2.5, BLACK)
_tvs = slab(-5.24, -5.234, SF+1.04, SF+2.41, -5.06, -2.54, vec(0.08, 0.12, 0.15))
screen_items.append((_tvs, vec(0.08, 0.12, 0.15)))
glow(slab(-5.30, -5.20, SF+2.55, SF+2.58, -5.1, -2.5, vec(0.95, 0.85, 0.65)), vec(0.35, 0.30, 0.24))
# sectional sofa facing TV
sofa(F(1.6, -3.8, 3, SF), 3.6, vec(0.30, 0.40, 0.44), vec(0.45, 0.55, 0.58), FAB3)
coffee_table(F(-1.3, -3.8, 1, SF), 1.6, 0.9, 0.38, vec(0.85, 0.82, 0.76))
for (x, z) in ((-1.4, -5.6), (-1.4, -2.0)):
    cylinder(pos=vec(x, SF, z), axis=vec(0, 0.4, 0), radius=0.32, color=FAB3)
    cylinder(pos=vec(x, SF+0.4, z), axis=vec(0, 0.04, 0), radius=0.32, color=FAB1L)
    block(x-0.35, x+0.35, z-0.35, z+0.35, 0, 0, SF-0.6, SF+0.8)
vase(-1.3, SF+0.4, -3.8, vec(0.3, 0.45, 0.5), True)
# bar + stools
cabinet(2.4, 5.2, SF, SF+0.55, -8.44, -8.0, vec(0.20, 0.26, 0.30), 'z+', 4, 's')
sl(2.35, 5.25, SF+0.55, SF+0.6, -8.46, -7.96, MARBLE)
for k in range(6):
    cylinder(pos=vec(2.6+k*0.4, SF+0.6, -8.25), axis=vec(0, 0.28+0.04*(k % 3), 0), radius=0.04,
             color=[vec(0.2, 0.4, 0.25), vec(0.55, 0.3, 0.12), vec(0.7, 0.7, 0.75)][k % 3], opacity=0.85)
for k in range(3):
    cylinder(pos=vec(3.0+k*0.5, SF+0.6, -8.05), axis=vec(0, 0.12, 0), radius=0.035,
             color=vec(0.85, 0.92, 0.95), opacity=0.55)
cabinet(2.0, 5.2, SF, SF+1.05, -7.25, -6.85, vec(0.20, 0.26, 0.30), 'z+', 4, 's')
sl(1.9, 5.3, SF+1.05, SF+1.1, -7.3, -6.75, MARBLE)
for xx in (2.5, 3.5, 4.5):
    stool(F(xx, -6.25, 0, SF), 0.72)
    rail(vec(xx, 12.86, -7.0), vec(xx, 11.5, -7.0), 0.008, GOLD)
    g = sphere(pos=vec(xx, 11.4, -7.0), radius=0.13, color=vec(0.95, 0.9, 0.8), opacity=0.9)
    glow(g, vec(0.95, 0.9, 0.8))
add_light(3.5, 11.3, -7.0)
# daybed by the front glass + telescope + reading corner
sl(3.2, 5.3, SF, SF+0.35, -2.9, -1.3, WOOD_D, 's')
slab(3.2, 5.3, SF+0.35, SF+0.5, -2.9, -1.3, FAB1L)
slab(3.2, 5.3, SF+0.5, SF+0.9, -2.9, -2.7, FAB1L)
for xx in (3.5, 4.7):
    slab(xx, xx+0.5, SF+0.5, SF+0.65, -2.7, -2.4, FAB3)
cylinder(pos=vec(3.0, SF, -3.4), axis=vec(0, 0.5, 0), radius=0.2, color=WOOD_D)
table_lamp(3.0, SF+0.5, -3.4)
rail(vec(-3.0, SF+1.1, -1.6), vec(-3.4, SF, -1.3), 0.025, BLACK)
rail(vec(-3.0, SF+1.1, -1.6), vec(-2.6, SF, -1.3), 0.025, BLACK)
rail(vec(-3.0, SF+1.1, -1.6), vec(-3.0, SF, -2.0), 0.025, BLACK)
cylinder(pos=vec(-3.1, SF+1.1, -1.7), axis=vec(0.5, 0.25, 0.9), radius=0.07, color=vec(0.85, 0.85, 0.88))
block(-3.5, -2.5, -2.1, -1.2, 0, 0, SF-0.6, SF+0.8)
armchair(F(-4.2, -1.6, 0, SF), FAB3)
floor_lamp(-4.9, -2.6, SF, 1.8, True)
pot_plant(-4.8, -6.0, SF, 1.6, 2)
pot_plant(5.0, -0.95, SF, 1.5, 1)
pot_plant(-1.2, -0.95, SF, 1.2, 0)
chandelier(0.0, 12.86, -4.0, 1.0, 1.1, 3)
add_light(0.0, 11.8, -4.0)
add_light(-3.0, 11.5, -1.6)
downlights([(-3.5, -7.0), (-1.0, -7.0), (1.5, -7.0), (4.5, -3.0), (-3.5, -4.0), (2.5, -1.5)], 12.85)
art(F(5.66, -3.0, 3, SF), 0, 1.4, 1.6, 0.9, 1)

# ============================================================
# WALK DATA  -  where the floor is (so you can climb stairs)
# ============================================================
floor_flat(-18.2, 15.9, -11.25, 21.0, 0.05)         # whole plot / yard
floor_flat(GX0, GX1, GZ0, GZ1, GF)                  # ground floor
floor_ramp(5.6, 8.0, -6.6, -0.8, 'z', -0.8, -6.6, GF, UF)
floor_flat(5.6, 8.6, -7.0, -6.6, UF)
# second floor pieces (the stair hole x 5.6..8.6, z -7.0..-0.8 stays open)
floor_flat(-1.3, 5.6, -8.92, 2.9, UF)
floor_flat(8.6, 13.3, -8.92, 2.9, UF)
floor_flat(5.6, 8.6, -8.92, -7.0, UF)
floor_flat(5.6, 8.6, -0.8, 2.9, UF)
floor_flat(-3.7, -1.2, -8.92, -0.05, UF)            # courtyard
floor_flat(-11.3, -3.6, -9.0, -0.2, UF)             # tower lounge
floor_ramp(-11.0, -6.2, -8.55, -7.25, 'x', -11.0, -6.2, UF, SF)
floor_flat(-6.2, -5.3, -8.9, -5.5, SF)              # bridge landing
floor_flat(-5.3, 5.66, -8.44, -0.62, SF)            # sky room
# ============================================================
# SKY, SUN, MOON, STARS + LIGHTS
# ============================================================
sun = sphere(pos=vec(70, 60, -140), radius=8,
             color=vec(1.0, 0.95, 0.7), emissive=True)
day_only.append(sun)
moon = sphere(pos=vec(-70, 65, -140), radius=5.5,
              color=vec(0.92, 0.94, 1.0), emissive=True)
night_only.append(moon)
for _ in range(150):
    a = random.uniform(0, 2*pi)
    el = random.uniform(0.25, 1.2)
    night_only.append(
        sphere(
            pos=vec(150*cos(el)*cos(a), 150*sin(el)+10,
                    -abs(150*cos(el)*sin(a))-30),
            radius=0.4, color=color.white, emissive=True
        )
    )
scene.lights = []
key = distant_light(direction=vec(-0.4, -0.8, -0.6), color=vec(1.0, 0.95, 0.85))
fill = distant_light(direction=vec(0.6, -0.3, 0.5), color=vec(0.35, 0.38, 0.42))


def set_mode(night):
    if night:
        scene.background = vec(0.04, 0.06, 0.15)
        scene.ambient = vec(0.46, 0.47, 0.52)          # was 0.35 -> gamay ra nga taas
        key.color = vec(0.24, 0.28, 0.44)              # was 0.16,0.20,0.34 (moonlight)
        key.direction = vec(0.4, -0.8, -0.5)
        fill.color = vec(0.12, 0.14, 0.22)             # was 0.07,0.08,0.13
        for o, dc, de, do in glow_items:
            o.color = GLOW
            o.emissive = True
            o.opacity = 1.0
        for l in lamp_lights:
            l.color = vec(1.0, 0.78, 0.45)             # was 1.0,0.7,0.35 -> mas bright ug mas warm-white
        for o, dc in screen_items:
            o.color = vec(0.45, 0.68, 0.90)
            o.emissive = True
    else:
        scene.background = vec(0.60, 0.74, 0.88)
        scene.ambient = vec(0.40, 0.40, 0.38)
        key.color = vec(1.0, 0.95, 0.85)
        key.direction = vec(-0.4, -0.8, -0.6)
        fill.color = vec(0.35, 0.38, 0.42)
        for o, dc, de, do in glow_items:
            o.color = dc
            o.emissive = de
            o.opacity = do
        for l in lamp_lights:
            l.color = color.black
        for o, dc in screen_items:
            o.color = dc
            o.emissive = False
    for o in day_only:
        o.visible = not night
    for o in night_only:
        o.visible = night


def go_day(b=None):
    set_mode(False)


def go_night(b=None):
    set_mode(True)


def set_view(center, fwd, rng):
    global walk_active
    walk_active = False
    walk_keys.clear()
    for piece in entry_parts:
        piece.visible = True
    scene.userspin = True
    scene.userzoom = True
    scene.up = vec(0, 1, 0)
    scene.center = center
    scene.forward = fwd
    scene.range = rng


def view_front(b=None):
    set_view(vec(-1, 6.0, 4), vec(0.0, -0.16, -1), 15)


def view_gate(b=None):
    set_view(vec(-4, 3.0, 12), vec(0.12, -0.14, -1), 11)


def view_left(b=None):
    set_view(vec(-1, 4.5, 4), vec(0.8, -0.28, -0.6), 20)


def view_right(b=None):
    set_view(vec(-1, 4.5, 4), vec(-0.8, -0.28, -0.6), 20)


def view_yard(b=None):
    set_view(vec(-1, 0.5, 11), vec(0.0, -0.7, -0.7), 14)


def view_top(b=None):
    set_view(vec(-1, 0, 4), vec(0, -1, -0.001), 21)


# ============================================================
# FIRST-PERSON WALKTHROUGH
#   W/S forward/back   A/D strafe   arrows = look
#   E = open/close the main door   Esc = exit
#   Walk up the stairs! Ground floor -> 2nd floor -> tower -> sky room
# ============================================================
EYE = 1.65
WALK_R = 0.28


def apply_walk_camera():
    look = vec(sin(walk_yaw)*cos(walk_pitch),
               sin(walk_pitch), -cos(walk_yaw)*cos(walk_pitch))
    scene.camera.pos = vec(walk_pos.x, walk_fy+EYE, walk_pos.z)
    scene.camera.axis = look*4.0


def floor_at(x, z, fy):
    best = None
    for (x0, x1, z0, z1, ax, a0, a1, ya, yb) in FLOORS:
        if x0 <= x <= x1 and z0 <= z <= z1:
            if ax == 'n':
                h = ya
            else:
                t = ((z if ax == 'z' else x)-a0)/(a1-a0)
                t = max(0.0, min(1.0, t))
                h = ya+(yb-ya)*t
            if h <= fy+0.62 and (best is None or h > best):
                best = h
    return best


def blocked(x, z, fy):
    r = WALK_R
    for (x0, x1, z0, z1, y0, y1, f0, f1) in BLOCKS:
        if f0 <= fy <= f1 and x0-r < x < x1+r and z0-r < z < z1+r:
            return True
    if entry_parts and entry_parts[0].visible and fy < 1.0:
        if -4.45-r < x < -2.45+r and 3.9 < z < 4.5:
            return True
    return False


def step_walk(px, pz, fy, dx, dz):
    for (mx, mz) in ((dx, dz), (dx, 0.0), (0.0, dz)):
        if mx == 0.0 and mz == 0.0:
            continue
        nx = px+mx
        nz = pz+mz
        if not (-18.2 < nx < 15.9 and -11.25 < nz < 21.0):
            continue
        h = floor_at(nx, nz, fy)
        if h is None:
            continue
        nfy = h if h >= fy else max(h, fy-0.25)
        if blocked(nx, nz, nfy):
            continue
        return nx, nz, nfy
    return px, pz, fy


def walk_inside(b=None):
    global walk_active, walk_pos, walk_fy, walk_yaw, walk_pitch
    walk_active = True
    walk_pos = vec(-3.35, 0, 7.4)
    walk_fy = 0.05
    walk_yaw = 0.0
    walk_pitch = 0.0
    walk_keys.clear()
    for piece in entry_parts:
        piece.visible = False
    scene.userspin = False
    scene.userzoom = False
    scene.autoscale = False
    scene.up = vec(0, 1, 0)
    apply_walk_camera()


def exit_walk(b=None):
    view_front()


def key_down(evt):
    if walk_active:
        k = evt.key.lower()
        if k == 'escape':
            exit_walk()
        elif k == 'e':
            for obj in entry_parts:
                obj.visible = not obj.visible
        else:
            walk_keys.add(k)


def key_up(evt):
    walk_keys.discard(evt.key.lower())


scene.bind('keydown', key_down)
scene.bind('keyup', key_up)


def walk_update():
    global walk_pos, walk_fy, walk_yaw, walk_pitch
    if not walk_active:
        return
    dt = 1.0/30.0
    if 'left' in walk_keys:
        walk_yaw -= 1.6*dt
    if 'right' in walk_keys:
        walk_yaw += 1.6*dt
    if 'up' in walk_keys:
        walk_pitch = min(0.95, walk_pitch+0.8*dt)
    if 'down' in walk_keys:
        walk_pitch = max(-0.95, walk_pitch-0.8*dt)
    fwd = vec(sin(walk_yaw), 0, -cos(walk_yaw))
    rgt = vec(cos(walk_yaw), 0, sin(walk_yaw))
    d = vec(0, 0, 0)
    if 'w' in walk_keys:
        d += fwd
    if 's' in walk_keys:
        d -= fwd
    if 'a' in walk_keys:
        d -= rgt
    if 'd' in walk_keys:
        d += rgt
    if mag(d) > 0:
        d = norm(d)*3.3*dt
        nx, nz, nfy = step_walk(walk_pos.x, walk_pos.z, walk_fy, d.x, d.z)
        walk_pos = vec(nx, 0, nz)
        walk_fy = nfy
    elif walk_fy > 0:
        h = floor_at(walk_pos.x, walk_pos.z, walk_fy)
        if h is not None and h < walk_fy:
            walk_fy = max(h, walk_fy-0.25)
    apply_walk_camera()


scene.append_to_caption("\n")
button(text="DAYLIGHT", bind=go_day)
button(text="NIGHT", bind=go_night)
scene.append_to_caption("   ")
button(text="FRONT", bind=view_front)
button(text="GATE", bind=view_gate)
button(text="LEFT ANGLE", bind=view_left)
button(text="RIGHT ANGLE", bind=view_right)
button(text="FRONT YARD", bind=view_yard)
button(text="TOP", bind=view_top)
scene.append_to_caption("   ")
button(text="WALK INSIDE", bind=walk_inside)
button(text="EXIT WALK", bind=exit_walk)
scene.append_to_caption(
    "   <span style='display:inline-block; "
    "vertical-align:middle; margin-left:20px; "
    "font-family:Arial; font-size:15px; "
    "font-weight:bold; color:#222; "
    "line-height:1.4;'>"
    "</span>"
)
scene.append_to_caption(
    "\n<span style='font-family:Arial; font-size:15px; font-weight:bold; color:#222;'>"
    "SUBMITTED BY: DENNIS MARIE ORMIDO"
    "</span>\n Right-drag: rotate  |  "
    "Scroll: zoom  |  "
    "Shift+drag: pan | WALK INSIDE: W A S D move, arrow keys look, E door, Esc exit"
    " | Take the STAIRS up: 2nd floor bedroom + bath, tower lounge, sky room\n"
)
set_mode(False)
view_front()
while True:
    rate(30)
    walk_update()