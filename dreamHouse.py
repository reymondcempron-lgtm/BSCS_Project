
from vpython import *
from math import sin, cos, pi



scene = canvas(title="MY DREAM HOUSE", width=1200, height=760,
               background=vector(0.90, 0.94, 0.98))
scene.autoscale = False
scene.ambient = vector(0.42, 0.42, 0.42)



white      = vector(0.95, 0.95, 0.93)
offwhite   = vector(0.86, 0.86, 0.84)
concrete   = vector(0.78, 0.78, 0.77)
charcoal   = vector(0.13, 0.14, 0.15)
graphite   = vector(0.27, 0.28, 0.30)
stone_gray = vector(0.60, 0.60, 0.60)
wood_deck  = vector(0.68, 0.42, 0.23)
wood_dark  = vector(0.50, 0.29, 0.15)
wood_slat  = vector(0.80, 0.60, 0.38)
glass_lit  = vector(1.00, 0.80, 0.50)     
glass_day  = vector(0.55, 0.72, 0.82)     
cream_lit  = vector(0.97, 0.80, 0.55)
cream_dark = vector(0.42, 0.41, 0.40)
curtain    = vector(0.93, 0.87, 0.76)
leaf       = vector(0.18, 0.44, 0.17)
leaf_light = vector(0.36, 0.62, 0.26)
water      = vector(0.20, 0.70, 0.84)
pool_floor = vector(0.12, 0.50, 0.64)
warm       = vector(1.00, 0.78, 0.42)
sofa_c     = vector(0.30, 0.29, 0.28)
cushion    = vector(0.88, 0.82, 0.72)
wicker     = vector(0.64, 0.60, 0.54)
soil       = vector(0.30, 0.27, 0.24)


lights = []          
pool_lights = []       
glass_panes = []       
back_walls = []        
ripple_rings = []      
door_parts = []        


door_is_open = False
door_busy = False
door_progress = 0.0
door_travel = 1.85
animations_running = True
lights_on = True


def V(p):
    return vector(*p)

def bx(pos, size, color, opacity=1.0):
    return box(pos=V(pos), size=V(size), color=color, opacity=opacity)

def cyc(pos, axis, radius, color, **kwargs):
    return cylinder(pos=V(pos), axis=V(axis), radius=radius,
                    color=color, **kwargs)

def sp(pos, radius, color, **kwargs):
    return sphere(pos=V(pos), radius=radius, color=color, **kwargs)

def add_bulb(pos, r=0.14):
    b = sp(pos, r, warm, emissive=True)
    lights.append(b)
    return b

def glazing(x0, x1, y0, y1, z, mull=(), transom=None, t=0.11):
    """Glass pane with a dark frame, optional vertical mullions and a transom."""
    w, h = x1 - x0, y1 - y0
    cx, cyy = (x0 + x1) / 2, (y0 + y1) / 2
    pane = bx((cx, cyy, z), (w, h, 0.06), glass_lit, 0.40)
    glass_panes.append(pane)
    for x in (x0, x1) + tuple(mull):
        bx((x, cyy, z + 0.04), (t, h + t, 0.12), charcoal)
    for y in (y0, y1):
        bx((cx, y, z + 0.04), (w + t, t, 0.12), charcoal)
    if transom is not None:
        bx((cx, transom, z + 0.04), (w, t * 0.8, 0.12), charcoal)
    return pane

def interior_back(pos, size):
    w = bx(pos, size, cream_lit)
    back_walls.append(w)
    return w

def rail_x(x0, x1, z, yb=5.43, h=1.1, posts=9):
    """Steel railing running along the X axis."""
    xm, L = (x0 + x1) / 2, x1 - x0
    bx((xm, yb + h, z), (L, 0.08, 0.08), charcoal)
    bx((xm, yb + 0.05, z), (L, 0.08, 0.08), charcoal)
    for k in range(4):
        bx((xm, yb + 0.25 + k * 0.22, z), (L, 0.03, 0.03), graphite)
    for i in range(posts):
        bx((x0 + i * L / (posts - 1), yb + h / 2, z), (0.07, h, 0.07), charcoal)

def rail_z(z0, z1, x, yb=5.43, h=1.1, posts=6):
    """Steel railing running along the Z axis."""
    zm, L = (z0 + z1) / 2, z1 - z0
    bx((x, yb + h, zm), (0.08, 0.08, L), charcoal)
    bx((x, yb + 0.05, zm), (0.08, 0.08, L), charcoal)
    for k in range(4):
        bx((x, yb + 0.25 + k * 0.22, zm), (0.03, 0.03, L), graphite)
    for i in range(posts):
        bx((x, yb + h / 2, z0 + i * L / (posts - 1)), (0.07, h, 0.07), charcoal)

def potted_plant(x, y, z, s=1.0):
    cyc((x, y, z), (0, 0.6 * s, 0), 0.34 * s, offwhite)
    for dx, dy, dz, r in [(0, 1.0, 0, 0.5), (0.3, 0.85, 0.1, 0.38),
                          (-0.28, 0.9, -0.1, 0.40), (0.05, 1.25, 0.15, 0.34),
                          (-0.10, 0.8, 0.3, 0.35)]:
        sp((x + dx * s, y + dy * s, z + dz * s), r * s,
           leaf if dx > 0 else leaf_light)

def grass_clump(x, y, z, h=1.1, n=9):
    for i in range(n):
        a = 2 * pi * i / n
        tilt = 0.45 + 0.10 * (i % 3)
        axis = vector(cos(a) * tilt * h * 0.6,
                      h * (0.80 + 0.10 * (i % 3)),
                      sin(a) * tilt * h * 0.6)
        cylinder(pos=vector(x, y, z), axis=axis, radius=0.05,
                 color=leaf if i % 2 else leaf_light)

def chair(x, z, face=1, y=0.2, col=wicker):
    bx((x, y + 0.45, z), (0.55, 0.10, 0.55), col)
    bx((x, y + 0.85, z - 0.27 * face), (0.55, 0.70, 0.08), col)
    for dx in (-0.22, 0.22):
        for dz in (-0.22, 0.22):
            bx((x + dx, y + 0.22, z + dz), (0.06, 0.44, 0.06), charcoal)

def table(x, z, w, d, y=0.2, top=offwhite, h=0.8):
    bx((x, y + h, z), (w, 0.10, d), top)
    for dx in (-w / 2 + 0.1, w / 2 - 0.1):
        for dz in (-d / 2 + 0.1, d / 2 - 0.1):
            bx((x + dx, y + h / 2, z + dz), (0.07, h, 0.07), charcoal)

def sofa_zface(x, z, w, y=0.2, face=1, col=sofa_c):
    """Sofa whose seat faces +z (face=1) or -z (face=-1)."""
    bx((x, y + 0.45, z), (w, 0.5, 1.1), col)
    bx((x, y + 0.95, z - 0.45 * face), (w, 0.9, 0.22), col)
    for dx in (-w / 2, w / 2):
        bx((x + dx, y + 0.65, z), (0.2, 0.8, 1.1), col)
    for k in (-1, 0, 1):
        bx((x + k * w / 3.3, y + 0.76, z + 0.05 * face), (w / 3.6, 0.12, 0.85), cushion)

def sofa_xface(x, z, d, y=0.2, face=1, col=sofa_c):
    """Sofa whose seat faces +x (face=1) or -x (face=-1)."""
    bx((x, y + 0.45, z), (1.1, 0.5, d), col)
    bx((x - 0.45 * face, y + 0.95, z), (0.22, 0.9, d), col)
    for dz in (-d / 2, d / 2):
        bx((x, y + 0.65, z + dz), (1.1, 0.8, 0.2), col)
    for k in (-1, 0, 1):
        bx((x + 0.05 * face, y + 0.76, z + k * d / 3.3), (0.85, 0.12, d / 3.6), cushion)

def floor_lamp(x, y, z, h=2.4):
    cyc((x, y, z), (0, h, 0), 0.04, charcoal)
    cyc((x, y, z), (0, 0.05, 0), 0.22, charcoal)
    add_bulb((x, y + h + 0.12, z), 0.17)


def build_base():
    # concrete plinth (top surface at y = 0)
    bx((0, -0.45, 4.5), (38, 0.9, 22), concrete)

    bx((1, 0.1, 3), (28, 0.2, 6), wood_deck)           
    bx((-9.5, 0.1, 9), (7, 0.2, 6), wood_deck)        
    bx((10, 0.1, 9), (10, 0.2, 6), wood_deck)         
    bx((-0.5, 0.1, 11.5), (11, 0.2, 1), wood_deck)     

    for z in (1, 2, 3, 4, 5):
        bx((1, 0.205, z), (28, 0.012, 0.03), wood_dark)
    for z in (7, 8, 9, 10, 11):
        bx((-9.5, 0.205, z), (7, 0.012, 0.03), wood_dark)
        bx((10, 0.205, z), (10, 0.012, 0.03), wood_dark)
    bx((-0.5, 0.205, 11.5), (11, 0.012, 0.03), wood_dark)

def build_pool():
    bx((-0.5, 0.03, 8.5), (10.9, 0.06, 4.9), pool_floor)
    bx((-0.5, 0.10, 8.5), (10.9, 0.10, 4.9), water, 0.80)

    bx((-0.5, 0.21, 5.95), (11.4, 0.04, 0.30), offwhite)
    bx((-0.5, 0.21, 11.05), (11.4, 0.04, 0.30), offwhite)
    for x in (-6.05, 5.05):
        bx((x, 0.21, 8.5), (0.30, 0.04, 5.3), offwhite)

    for x, z in [(-5.7, 7.0), (-5.7, 10.0), (4.7, 7.0), (4.7, 10.0)]:
        pool_lights.append(sp((x, 0.12, z), 0.15, vector(0.55, 0.92, 1.0), emissive=True))

    for i in range(5):
        ring = sphere(pos=vector(-4.5 + i * 1.9, 0.17, 7.2 + (i % 2) * 1.6),
                      radius=0.22, color=vector(0.60, 0.92, 1.0), opacity=0.45)
        ripple_rings.append((ring, i * 1.23))

def build_planters():
    bx((-13.8, 0.35, 11.6), (6.0, 0.7, 4.0), graphite)
    bx((-13.8, 0.72, 11.6), (5.6, 0.06, 3.6), soil)
    for x, z, h in [(-15.6, 11.0, 1.4), (-14.4, 12.3, 1.2), (-13.2, 10.9, 1.1),
                    (-12.2, 12.2, 1.0), (-15.2, 12.6, 0.9)]:
        grass_clump(x, 0.75, z, h)
    for x, z in [(-12.3, 11.0), (-13.8, 12.6), (-14.8, 11.6)]:
        sp((x, 0.80, z), 0.14, stone_gray)

    bx((12.0, 0.35, 13.4), (9.0, 0.7, 2.2), graphite)
    bx((12.0, 0.72, 13.4), (8.6, 0.06, 1.8), soil)
    for x, z, h in [(8.4, 13.4, 1.0), (9.8, 13.1, 1.3), (11.3, 13.5, 1.0),
                    (12.8, 13.1, 1.4), (14.2, 13.5, 1.2), (15.5, 13.2, 1.0)]:
        grass_clump(x, 0.75, z, h)


    potted_plant(5.5, 0.2, 6.2, 0.9)

def build_patio_furniture():
    table(1.6, 3.2, 3.2, 1.6, top=offwhite, h=0.85)
    for x in (0.4, 1.6, 2.8):
        chair(x, 2.15, face=-1)
        chair(x, 4.25, face=1)
    cyc((1.6, 1.05, 3.2), (0, 0.18, 0), 0.12, leaf_light)

    bx((10.9, 0.24, 3.3), (5.4, 0.03, 4.2), vector(0.56, 0.53, 0.49))      # rug
    sofa_zface(10.9, 1.0, 5.2, face=1)
    sofa_xface(7.7, 3.6, 3.0, face=1)
    sofa_xface(14.1, 3.6, 3.0, face=-1)
    table(10.9, 3.6, 2.4, 1.4, y=0.2, top=wood_deck, h=0.5)


def build_sliding_door():
    """Centre ground-floor glass door (x 0 -> 1.9) that slides to the right."""
    z, x0, x1, y0, y1 = 0.12, 0.0, 1.9, 0.3, 4.8
    parts = []
    pane = bx(((x0 + x1) / 2, (y0 + y1) / 2, z), (x1 - x0, y1 - y0, 0.05), glass_lit, 0.40)
    glass_panes.append(pane)
    parts.append(pane)
    for x in (x0 + 0.05, x1 - 0.05):
        parts.append(bx((x, (y0 + y1) / 2, z), (0.10, y1 - y0, 0.09), charcoal))
    for y in (y0 + 0.05, y1 - 0.05):
        parts.append(bx(((x0 + x1) / 2, y, z), (x1 - x0, 0.10, 0.09), charcoal))
    parts.append(bx((x0 + 0.22, 2.5, z + 0.06), (0.04, 0.9, 0.04), vector(0.85, 0.85, 0.85)))
    for p in parts:
        door_parts.append((p, p.pos.x))

def build_left_block():
    bx((-14.0, 2.5, -3), (2.0, 5.0, 6), white)              
    bx((-4.3, 2.5, -3), (1.0, 5.0, 6), white)                
    bx((-8.9, 4.90, -3), (8.2, 0.2, 6), white)              
    interior_back((-8.9, 2.6, -5.95), (8.2, 4.8, 0.1))
    bx((-8.9, 0.22, -3), (8.2, 0.04, 6), wood_deck)          
    glazing(-13.0, -4.8, 0.3, 4.8, 0.0, mull=(-10.3, -7.6))
    for x in (-12.6, -5.2):
        bx((x, 2.6, -0.35), (0.5, 4.2, 0.12), curtain)

    bx((-9.75, 5.2, -1.5), (11.5, 0.4, 9), charcoal)
    bx((-9.75, 5.43, 0.45), (11.3, 0.05, 4.8), wood_deck)
    bx((-14.15, 5.43, -4.0), (2.5, 0.05, 4.0), wood_deck)
    rail_x(-15.4, -4.1, 2.9, posts=12)
    rail_z(-6.0, 2.9, -15.4, posts=10)
    rail_x(-15.4, -12.9, -5.9, posts=4)

    bx((-12.1, 7.5, -4), (1.6, 4.2, 4), white)             
    bx((-4.45, 7.5, -4), (0.9, 4.2, 4), wood_slat)           
    interior_back((-8.1, 7.5, -5.95), (6.4, 4.1, 0.1))
    bx((-8.1, 5.43, -4), (6.4, 0.04, 4), wood_deck)
    glazing(-11.3, -4.9, 5.5, 9.5, -2.0, mull=(-8.9, -7.2))
    bx((-5.4, 7.4, -2.35), (0.5, 3.6, 0.12), curtain)

    bx((-9.0, 9.75, -3), (10.4, 0.30, 6.0), charcoal)
    bx((-9.0, 10.03, -3), (10.4, 0.26, 6.0), white)
    bx((-7.55, 11.5, -4.5), (1.8, 2.7, 1.8), stone_gray)
    bx((-7.55, 12.95, -4.5), (2.1, 0.20, 2.1), charcoal)
    bx((-7.55, 13.05, -4.5), (0.9, 0.06, 0.9), vector(0.05, 0.05, 0.05))

    potted_plant(-13.3, 5.45, -1.0, 1.25)
    for x, z in [(-13.6, 1.5), (-12.3, 0.5)]:                
        bx((x, 5.75, z), (0.8, 0.14, 1.9), cushion)
        bx((x, 6.1, z - 0.9), (0.8, 0.55, 0.12), cushion)
        for dx in (-0.35, 0.35):
            for dz in (-0.8, 0.8):
                bx((x + dx, 5.6, z + dz), (0.06, 0.28, 0.06), charcoal)
    potted_plant(-5.0, 5.45, 2.2, 0.8)

def build_centre_block():
    bx((4.5, 2.5, -3), (1.4, 5.0, 6), white)              
    bx((0, 4.90, -3), (7.6, 0.2, 6), white)
    interior_back((0, 2.6, -5.95), (7.6, 4.8, 0.1))
    bx((0, 0.22, -3), (7.6, 0.04, 6), wood_deck)
    glazing(-3.8, 0.0, 0.3, 4.8, 0.0, mull=(-1.9,))
    glazing(1.9, 3.8, 0.3, 4.8, 0.0)
    bx((0.95, 4.80, 0.04), (1.9, 0.11, 0.12), charcoal)     
    bx((0.95, 0.30, 0.04), (1.9, 0.11, 0.12), charcoal)     
    build_sliding_door()

    bx((0.6, 5.2, -2), (9.2, 0.4, 8), charcoal)
    bx((0.6, 5.43, 0.0), (9.0, 0.05, 3.8), wood_deck)
    rail_x(-4.0, 5.2, 1.9, posts=10)
    potted_plant(-2.8, 5.45, 0.9, 0.95)

    bx((-3.2, 8.15, -4), (1.6, 5.5, 4), graphite)            
    bx((4.4, 8.15, -4), (1.6, 5.5, 4), white)                
    interior_back((0.6, 8.15, -5.95), (6.0, 5.3, 0.1))
    bx((0.6, 5.43, -4), (6.0, 0.04, 4), wood_deck)
    glazing(-2.4, 3.6, 5.5, 10.7, -2.0, mull=(-0.4, 1.6), transom=9.3)
    for x in (-2.0, 3.2):
        bx((x, 8.0, -2.35), (0.5, 4.8, 0.12), curtain)

    bx((-0.15, 11.05, -2.5), (13.1, 0.30, 7.0), charcoal)
    bx((-0.15, 11.60, 0.95), (13.1, 1.10, 0.20), graphite)
    bx((-0.15, 12.12, -2.6), (12.8, 0.22, 6.4), white)

def build_right_block():
    bx((5.8, 2.5, -3), (1.2, 5.0, 6), white)                
    bx((12.8, 2.5, -3), (1.2, 5.0, 6), white)               
    bx((9.3, 4.70, -3), (5.8, 0.6, 6), white)              
    interior_back((9.3, 2.4, -5.95), (5.8, 4.4, 0.1))
    bx((9.3, 0.22, -3), (5.8, 0.04, 6), wood_deck)
    glazing(6.4, 12.2, 0.3, 4.4, 0.0, mull=(8.3, 10.3))
    for x in (6.8, 11.8):
        bx((x, 2.4, -0.35), (0.5, 3.8, 0.12), curtain)

    bx((8.4, 5.2, -1.4), (6.3, 0.4, 9.2), charcoal)
    bx((12.45, 5.2, -3), (1.9, 0.4, 6), charcoal)
    rail_x(12.0, 13.3, -0.1, posts=4)

    bx((12.7, 7.5, -4), (1.4, 4.2, 4), white)               
    bx((8.7, 9.2, -4), (6.6, 0.8, 4), white)                 
    interior_back((8.6, 7.1, -5.95), (6.8, 3.4, 0.1))
    bx((8.6, 5.43, -4), (6.8, 0.04, 4), wood_deck)
    glazing(5.2, 12.0, 5.5, 8.8, -2.0, mull=(7.5, 9.8))
    bx((5.8, 7.2, -2.35), (0.5, 3.0, 0.12), curtain)
    bx((11.5, 7.2, -2.35), (0.5, 3.0, 0.12), curtain)

    bx((9.3, 9.72, -2.8), (8.9, 0.24, 6.4), charcoal)
    bx((9.3, 9.98, -2.8), (8.6, 0.28, 6.0), white)

    potted_plant(10.6, 5.45, 0.3, 1.1)
    bx((8.6, 5.75, 0.9), (2.0, 0.16, 0.9), cushion)
    bx((8.6, 6.15, 0.45), (2.0, 0.6, 0.12), cushion)
    for x in (7.7, 9.5):
        for dz in (0.55, 1.25):
            bx((x, 5.6, dz), (0.06, 0.3, 0.06), charcoal)

def build_pergola():
    x0, x1, zf, yt = 4.8, 15.8, 7.6, 4.3
    xm, L = (x0 + x1) / 2, x1 - x0

    for x in (x0 + 0.15, x1 - 0.15):
        bx((x, yt, zf / 2), (0.28, 0.30, zf), charcoal)      # side beams
    bx((xm, yt, zf), (L, 0.30, 0.28), charcoal)              # front beam
    bx((xm, yt, 0.1), (L, 0.30, 0.28), charcoal)             # back beam
    for x in (5.9, 15.3):
        bx((x, yt / 2, zf), (0.30, yt, 0.30), charcoal)      # front posts
    bx((15.3, yt / 2, 0.3), (0.30, yt, 0.30), charcoal)      # back-right post

    z = 0.6
    while z < zf - 0.2:
        bx((xm, yt + 0.22, z), (L, 0.14, 0.28), wood_slat)
        z += 0.55

    for x in (7.0, 10.3, 13.6):
        for z in (2.0, 5.8):
            add_bulb((x, yt - 0.25, z), 0.12)

def build_interiors():
    bx((-9.0, 0.25, -3.2), (5.5, 0.02, 3.5), vector(0.86, 0.76, 0.62))    
    sofa_zface(-9.5, -4.8, 4.5, face=-1)
    sofa_xface(-6.4, -2.8, 1.6, face=-1)
    table(-9.5, -2.8, 2.4, 1.2, y=0.2, top=wood_dark, h=0.5)
    floor_lamp(-12.2, 0.2, -5.2)
    add_bulb((-8.9, 4.65, -3.0), 0.18)

    sofa_zface(-1.4, -4.8, 3.6, face=-1)
    bx((2.0, 0.60, -5.6), (3.0, 0.8, 0.5), wood_dark)
    potted_plant(3.2, 0.2, -4.4, 1.0)
    add_bulb((0.0, 4.65, -3.0), 0.18)

    sofa_zface(9.3, -4.8, 3.2, face=-1)
    table(9.3, -2.8, 1.8, 1.0, y=0.2, top=wood_dark, h=0.5)
    add_bulb((9.3, 4.35, -3.0), 0.18)

    table(-8.1, -4.0, 2.4, 1.4, y=5.45, top=offwhite, h=0.8)
    for x in (-8.8, -7.4):
        chair(x, -4.9, face=-1, y=5.45)
        chair(x, -3.1, face=1, y=5.45)
    floor_lamp(-10.6, 5.45, -5.2)
    add_bulb((-8.1, 9.25, -4.0), 0.18)

    bx((0.6, 5.95, -4.6), (3.6, 0.5, 2.6), cushion)
    bx((0.6, 6.75, -5.8), (3.6, 1.5, 0.2), wood_dark)
    for x in (-0.4, 1.6):
        bx((x, 6.35, -5.3), (0.9, 0.22, 0.5), white)
    for x in (-2.0, 3.2):
        bx((x, 5.95, -5.5), (0.6, 0.5, 0.6), wood_dark)
    add_bulb((0.6, 10.3, -4.0), 0.18)

    sofa_zface(8.6, -4.8, 3.4, y=5.45, face=-1)
    table(8.6, -3.0, 1.6, 0.9, y=5.45, top=wood_dark, h=0.5)
    add_bulb((8.6, 9.2, -4.0), 0.18)

def build_house():
    build_left_block()
    build_centre_block()
    build_right_block()
    build_pergola()
    build_interiors()

build_base()
build_pool()
build_planters()
build_house()
build_patio_furniture()

distant_light(direction=vector(-0.35, -0.85, -0.55), color=vector(0.90, 0.88, 0.82))
distant_light(direction=vector(0.70, -0.30, -0.50), color=vector(0.45, 0.52, 0.62))

scene.center = vector(0, 5.0, 3.0)
scene.range = 17
scene.forward = vector(-0.12, -0.40, -1.0)


def apply_lighting():
    for g in glass_panes:
        g.color = glass_lit if lights_on else glass_day
        g.opacity = 0.42 if lights_on else 0.30
    for w in back_walls:
        w.color = cream_lit if lights_on else cream_dark
    for b in lights:
        b.visible = lights_on
    for b in pool_lights:
        b.visible = lights_on
    light_button.text = "Lights: ON" if lights_on else "Lights: OFF"

def update_door(p):
    for obj, home_x in door_parts:
        obj.pos.x = home_x + door_travel * p

def set_door_open(want_open):
    """Smoothly slide the centre glass door open or closed."""
    global door_is_open, door_busy, door_progress
    if door_busy:
        return
    door_busy = True
    target = 1.0 if want_open else 0.0
    direction = 1 if target > door_progress else -1

    steps = 45
    while abs(door_progress - target) > 0.001:
        rate(60)
        door_progress += direction / steps
        door_progress = max(0.0, min(1.0, door_progress))
        update_door(door_progress)
        if abs(door_progress - target) < 1.0 / steps:
            door_progress = target

    door_progress = target
    update_door(door_progress)
    door_is_open = (target == 1.0)
    door_busy = False
    door_button.text = "Close door" if door_is_open else "Open door"

def toggle_door(btn):
    set_door_open(not door_is_open)

def toggle_lights(btn):
    global lights_on
    lights_on = not lights_on
    apply_lighting()

def toggle_animations(btn):
    global animations_running
    animations_running = not animations_running
    btn.text = "Pause motion" if animations_running else "Resume motion"

def reset_scene(btn):
    global lights_on
    if door_busy:
        return
    if door_is_open:
        set_door_open(False)
    lights_on = True
    apply_lighting()
    print("Scene reset: door closed, lights on.")

scene.append_to_caption("\n\n")
door_button = button(text="Open door", bind=toggle_door)
scene.append_to_caption("   ")
light_button = button(text="Lights: ON", bind=toggle_lights)
scene.append_to_caption("   ")
motion_button = button(text="Pause motion", bind=toggle_animations)
scene.append_to_caption("   ")
button(text="Reset", bind=reset_scene)
scene.append_to_caption("\nDrag: rotate | Wheel: zoom | Right-drag: pan\n")

time_phase = 0.0
while True:
    rate(40)
    if not animations_running:
        continue
    time_phase += 0.045

    for ring, phase in ripple_rings:
        pulse = 0.75 + 0.25 * sin(time_phase * 1.25 + phase)
        ring.radius = 0.16 + 0.07 * pulse
        ring.opacity = 0.28 + 0.20 * (0.5 + 0.5 * sin(time_phase + phase))
        ring.pos.y = 0.17 + 0.012 * sin(time_phase + phase)

    if lights_on:
        glow = 0.72 + 0.28 * (0.5 + 0.5 * sin(time_phase * 1.4))
        for bulb in lights:
            bulb.color = vector(1.0, 0.73 * glow, 0.36 * glow)