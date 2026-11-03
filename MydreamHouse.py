import math
import time

from vpython import (canvas, box, cylinder, sphere, ellipsoid, ring, label, cone, pyramid,
                     vertex, quad, triangle, compound, distant_light,
                     vector, color, mag, norm, cross, rate, button,
                     wtext, textures, local_light, text)

try:
    from vpython import bumpmaps
except ImportError:          # very old VPython versions
    bumpmaps = None

# --------------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------------
USE_TEXTURES = True    # stone / timber / rug image textures (set False if slow)
USE_BUMPMAPS = True    # surface relief on stone and stucco
HOUSE_NAME = 'John Reno Dream House'
CANVAS_W, CANVAS_H = 1280, 720      # 16:9

# --------------------------------------------------------------------------
# Colours
# --------------------------------------------------------------------------
def rgb(r, g, b):
    return vector(r / 255, g / 255, b / 255)

STONE       = rgb(246, 232, 206)     # tint for the stone texture
JOINT       = rgb(150, 138, 120)     # mortar joints
STONE_PLAIN = rgb(216, 206, 189)
STONE_TRIM  = rgb(206, 195, 177)
PLINTH      = rgb(163, 152, 134)
STUCCO      = rgb(236, 228, 213)
INT_WALL    = rgb(246, 241, 231)
WOOD_SIDING = rgb(220, 160, 112)     # tint for the wood texture
WOOD_PLAIN  = rgb(138, 88, 53)
WOOD_DARK   = rgb(94, 58, 35)
WOOD_MID    = rgb(122, 74, 44)
WOOD_LIGHT  = rgb(176, 122, 78)
CAPIZ       = rgb(247, 228, 190)
GLASS       = rgb(178, 214, 232)
STEEL       = rgb(31, 27, 24)
BRASS       = rgb(196, 160, 82)
ROOF_A      = rgb(181, 88, 58)
ROOF_B      = rgb(166, 80, 52)
ROOF_C      = rgb(196, 106, 71)
ROOF_D      = rgb(150, 70, 45)
ROOF_LIGHT  = rgb(200, 108, 72)
ROOF_DARK   = rgb(110, 50, 30)
SOFFIT      = rgb(176, 128, 86)
GRASS       = rgb(118, 156, 86)
PAVE        = rgb(204, 196, 180)
PAVE_DARK   = rgb(178, 168, 150)
ASPHALT     = rgb(92, 92, 96)
LEAF        = rgb(78, 122, 64)
LEAF2       = rgb(100, 145, 78)
LEAF_RED    = rgb(142, 47, 50)
FLOOR_WOOD  = rgb(236, 196, 150)
FLOOR_STONE = rgb(226, 214, 192)
FLOOR_TILE  = rgb(232, 228, 218)
FLOOR_BATH  = rgb(214, 228, 230)
FLOOR_SERV  = rgb(206, 200, 188)
DECK        = rgb(205, 160, 112)
SOFA        = rgb(226, 214, 192)
ACCENT      = rgb(176, 88, 58)
ACCENT2     = rgb(64, 98, 96)
LEATHER     = rgb(92, 60, 40)
WHITE       = rgb(246, 246, 243)
BLACK       = rgb(22, 22, 24)
METAL       = rgb(190, 192, 196)
MIRROR      = rgb(214, 226, 232)
COUNTER     = rgb(238, 235, 228)
CABINET     = rgb(108, 78, 54)
CONCRETE    = rgb(176, 172, 164)
CLAY        = rgb(170, 92, 58)
WATER       = rgb(150, 205, 225)
LAMP        = rgb(255, 226, 168)
BEDDING     = rgb(250, 248, 242)
WOOD        = WOOD_PLAIN

BOOK_COLOURS = [rgb(143, 65, 41), rgb(64, 98, 96), rgb(200, 170, 110), rgb(70, 70, 90),
                rgb(170, 120, 70), rgb(120, 40, 40), rgb(225, 210, 180)]
TOWEL_COLOURS = [rgb(240, 236, 226), rgb(210, 226, 228), rgb(232, 210, 196), rgb(245, 245, 240)]
CLOTH_COLOURS = [rgb(240, 236, 226), rgb(60, 70, 90), rgb(176, 88, 58), rgb(130, 140, 120),
                 rgb(30, 30, 34), rgb(210, 190, 160)]


def tex(name, bump=True):
    """Return a VPython texture spec, or None when textures are disabled."""
    if not USE_TEXTURES:
        return None
    f = getattr(textures, name, None)
    if f is None:
        return None
    if bump and USE_BUMPMAPS and bumpmaps is not None:
        b = getattr(bumpmaps, name, None)
        if b is not None:
            return {'file': f, 'bumpmap': b}
    return f


def _stone_tex():
    if not USE_TEXTURES:
        return None
    f = getattr(textures, 'granite', None)
    b = getattr(bumpmaps, 'stucco', None) if (USE_BUMPMAPS and bumpmaps is not None) else None
    if f is None:
        return None
    return {'file': f, 'bumpmap': b} if b else f


T_STONE = _stone_tex()
T_WOOD = tex('wood', bump=False)
T_STUCCO = tex('stucco')
T_RUG = tex('rug', bump=False)
T_GRANITE = tex('granite', bump=False)

# --------------------------------------------------------------------------
# Scene
# --------------------------------------------------------------------------
scene = canvas(title='', width=CANVAS_W, height=CANVAS_H,
               background=rgb(182, 210, 236))
scene.autoscale = False
scene.ambient = color.gray(0.46)
scene.lights = []
SUN = distant_light(direction=vector(0.45, 0.85, 0.55), color=color.gray(0.78))
FILL = distant_light(direction=vector(-0.55, 0.45, -0.6), color=color.gray(0.34))
SKY_DAY, SKY_NIGHT = rgb(182, 210, 236), rgb(10, 16, 34)
WINDOWS = []        # window/door panes that glow at night
NIGHT_LIGHTS = []   # warm interior lights, black during the day
SIGN = []           # house-name lettering
try:
    scene.userpan = True
except Exception:
    pass

OX, OY = 7.0, 5.3            # plan point placed at the world origin


def W(x, y, z):
    """Plan coordinates (x across, y front-back, z height) -> VPython world vector."""
    return vector(x - OX, z, y - OY)


# --------------------------------------------------------------------------
# Object registry: every object belongs to a LEVEL (what floor-switching
# shows or hides) and a KIND (how it reacts to the zoom fade).
#   levels: 'gf' ground floor, 'sf' second floor, 'roof', 'site'
#   kinds : 'ext' exterior walls, 'int' interior walls, 'glass', 'roof',
#           everything else (furniture, floors, ...) never fades
# Small untextured parts are merged into one compound per (level, kind)
# so the browser only has to update a handful of objects when fading.
# --------------------------------------------------------------------------
REG = []          # [obj, level, kind, base_opacity, mode, last_op, last_vis]
BUCKETS = {}      # (level, kind) -> list of objects to compound
LABELS = []       # (label, level)


def reg(obj, level, kind, base=1.0, mode='obj'):
    REG.append([obj, level, kind, base, mode, None, None])
    return obj


def put(obj, level, kind):
    BUCKETS.setdefault((level, kind), []).append(obj)
    return obj


def bx(x0, x1, y0, y1, z0, z1, col, level, kind, texture=None, base=1.0,
       single=False, shiny=0.12, emissive=False):
    """Axis-aligned box from plan extents."""
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    if z1 < z0:
        z0, z1 = z1, z0
    kw = dict(pos=W((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
              size=vector(max(x1 - x0, 0.002), max(z1 - z0, 0.002), max(y1 - y0, 0.002)),
              color=col, shininess=shiny)
    if texture is not None:
        kw['texture'] = texture
    if emissive:
        kw['emissive'] = True
    if base < 1:
        kw['opacity'] = base
    b = box(**kw)
    if texture is not None or base < 1 or single or emissive:
        reg(b, level, kind, base)
    else:
        put(b, level, kind)
    return b


def rod(p0, p1, r, col, level, kind, single=False):
    c = cylinder(pos=p0, axis=p1 - p0, radius=r, color=col, shininess=0.25)
    if single:
        reg(c, level, kind)
    else:
        put(c, level, kind)
    return c


def vcyl(x, y, z0, h, r, col, level, kind='furn'):
    return rod(W(x, y, z0), W(x, y, z0 + h), r, col, level, kind)


def ball(x, y, z, r, col, level, kind='furn', emissive=False):
    s = sphere(pos=W(x, y, z), radius=r, color=col, shininess=0.2, emissive=emissive)
    if emissive:
        reg(s, level, kind)
    else:
        put(s, level, kind)
    return s


def beam(p0, p1, w, h, col, level, kind):
    d = p1 - p0
    b = box(pos=(p0 + p1) / 2, axis=norm(d), size=vector(mag(d), h, w),
            color=col, shininess=0.12)
    put(b, level, kind)
    return b


def lamp_glow(x, y, z, r, level, kind='light'):
    return ball(x, y, z, r, LAMP, level, kind, emissive=True)


# --------------------------------------------------------------------------
# Walls, openings, windows, doors
# --------------------------------------------------------------------------
def wall(axis, c, a0, a1, z0, z1, t, col, level, kind, openings=(), texture=None,
         chunk=1.8, joints=0):
    """A straight wall with rectangular openings.
    axis 'x': the wall runs along plan-x at plan-y = c.
    axis 'y': the wall runs along plan-y at plan-x = c.
    openings: (start, end, sill, head) measured along the wall."""
    def piece(s0, s1, h0, h1):
        if s1 - s0 < 0.005 or h1 - h0 < 0.005:
            return
        n = max(1, int(math.ceil((s1 - s0) / chunk - 1e-6))) if texture is not None else 1
        for i in range(n):
            u0 = s0 + (s1 - s0) * i / n
            u1 = s0 + (s1 - s0) * (i + 1) / n
            if axis == 'x':
                bx(u0, u1, c - t / 2, c + t / 2, h0, h1, col, level, kind, texture=texture)
            else:
                bx(c - t / 2, c + t / 2, u0, u1, h0, h1, col, level, kind, texture=texture)
        if joints:                       # ashlar coursing on the outside face
            off = joints * (t / 2 + 0.006)
            course = 0.36
            k = 1
            while True:
                zk0 = 0.45 + (k - 1) * course
                zk1 = 0.45 + k * course
                if zk0 >= h1:
                    break
                if zk1 > h0 and zk1 < h1 - 0.02:
                    fbox(axis, c, off, 0.012, s0, s1, zk1 - 0.011, zk1 + 0.011, JOINT, level, kind)
                lo, hi = max(h0, zk0), min(h1, zk1)
                if hi - lo > 0.05:
                    a = -0.15 + (0.35 if k % 2 else 0.0)
                    while a < s1:
                        if s0 + 0.04 < a < s1 - 0.04:
                            fbox(axis, c, off, 0.012, a - 0.011, a + 0.011, lo, hi, JOINT, level, kind)
                        a += 0.7
                k += 1

    cur = a0
    for (o0, o1, sill, head) in sorted(openings):
        piece(cur, o0, z0, z1)
        piece(o0, o1, z0, max(z0, sill))
        piece(o0, o1, min(z1, head), z1)
        cur = o1
    piece(cur, a1, z0, z1)


def fbox(axis, c, off, dep, a0, a1, h0, h1, col, level, kind, **kw):
    """A box lying in a wall plane, shifted `off` across the wall."""
    if axis == 'x':
        return bx(a0, a1, c + off - dep / 2, c + off + dep / 2, h0, h1, col, level, kind, **kw)
    return bx(c + off - dep / 2, c + off + dep / 2, a0, a1, h0, h1, col, level, kind, **kw)


def fpt(axis, c, off, a, z):
    return W(a, c + off, z) if axis == 'x' else W(c + off, a, z)


def frame(axis, c, a0, a1, z0, z1, col, level, kind='ext', fw=0.06, dep=0.08,
          off=0.0, mull=(), trans=()):
    fbox(axis, c, off, dep, a0, a1, z1 - fw, z1, col, level, kind)
    fbox(axis, c, off, dep, a0, a1, z0, z0 + fw, col, level, kind)
    fbox(axis, c, off, dep, a0, a0 + fw, z0, z1, col, level, kind)
    fbox(axis, c, off, dep, a1 - fw, a1, z0, z1, col, level, kind)
    for m in mull:
        fbox(axis, c, off, dep, m - fw / 2, m + fw / 2, z0, z1, col, level, kind)
    for tz in trans:
        fbox(axis, c, off, dep, a0, a1, tz - fw / 2, tz + fw / 2, col, level, kind)


def pane(axis, c, a0, a1, z0, z1, col, level, base, off=0.0, t=0.025):
    b = fbox(axis, c, off, t, a0, a1, z0, z1, col, level, 'glass', base=base,
             single=True, shiny=0.85)
    REG[-1][4] = 'window'
    WINDOWS.append((b, vector(col.x, col.y, col.z), col is CAPIZ))
    return b


def gf_window(axis, c, out, a0, a1, sill, head, grille=True, t=0.30, level='gf'):
    """Black-steel window in the stone base, with stone surround and iron grille."""
    pane(axis, c, a0, a1, sill, head, GLASS, level, 0.35)
    frame(axis, c, a0, a1, sill, head, STEEL, level, fw=0.05, dep=0.07,
          mull=[(a0 + a1) / 2], trans=[head - 0.5])
    so = out * (t / 2 + 0.03)
    fbox(axis, c, so, 0.08, a0 - 0.15, a1 + 0.15, head, head + 0.2, STONE_TRIM, level, 'ext')
    fbox(axis, c, so, 0.12, a0 - 0.1, a1 + 0.1, sill - 0.1, sill, STONE_TRIM, level, 'ext')
    fbox(axis, c, so, 0.08, a0 - 0.15, a0, sill, head, STONE_TRIM, level, 'ext')
    fbox(axis, c, so, 0.08, a1, a1 + 0.15, sill, head, STONE_TRIM, level, 'ext')
    if grille:
        go = out * (t / 2 + 0.07)
        n = max(2, int((a1 - a0) / 0.16))
        for k in range(1, n):
            a = a0 + (a1 - a0) * k / n
            rod(fpt(axis, c, go, a, sill), fpt(axis, c, go, a, head), 0.012, STEEL, level, 'ext')
        fbox(axis, c, go, 0.03, a0, a1, sill + 0.25, sill + 0.29, STEEL, level, 'ext')
        fbox(axis, c, go, 0.03, a0, a1, head - 0.3, head - 0.26, STEEL, level, 'ext')


def louver_window(axis, c, out, a0, a1, sill, head, level='gf'):
    """Timber-louvred opening (dirty kitchen, laundry, pantry)."""
    frame(axis, c, a0, a1, sill, head, WOOD_DARK, level, fw=0.06, dep=0.1)
    z = sill + 0.1
    while z < head - 0.08:
        fbox(axis, c, 0, 0.09, a0 + 0.06, a1 - 0.06, z, z + 0.035, WOOD_MID, level, 'ext')
        z += 0.11
    fbox(axis, c, out * 0.16, 0.1, a0 - 0.08, a1 + 0.08, sill - 0.06, sill, STONE_TRIM, level, 'ext')


def capiz_window(axis, c, out, a0, a1, sill, head, n=None, open_idx=(),
                 ventanilla=True, t=0.2, level='sf'):
    """Sliding capiz-shell window panels; ventanilla with balusters below."""
    if n is None:
        n = max(1, int(round((a1 - a0) / 1.0)))
    w = (a1 - a0) / n
    for i in range(n):
        p0 = a0 + i * w
        p1 = p0 + w
        if i in open_idx:                       # slid open: glass behind
            pane(axis, c, p0, p1, sill, head, GLASS, level, 0.3)
            frame(axis, c, p0, p1, sill, head, WOOD_DARK, level, fw=0.05, dep=0.07)
        else:
            pane(axis, c, p0, p1, sill, head, CAPIZ, level, 0.9)
            frame(axis, c, p0, p1, sill, head, WOOD_DARK, level, fw=0.05, dep=0.06,
                  mull=[p0 + (p1 - p0) * k / 4 for k in (1, 2, 3)],
                  trans=[sill + (head - sill) * k / 6 for k in range(1, 6)])
    fbox(axis, c, out * (t / 2 + 0.05), 0.12, a0 - 0.1, a1 + 0.1, sill - 0.07, sill,
         WOOD_DARK, level, 'ext')
    if ventanilla and sill - 4.0 > 0.6:
        fbox(axis, c, out * (t / 2 + 0.015), 0.03, a0, a1, 4.15, 4.68, rgb(58, 36, 22), level, 'ext')
        frame(axis, c, a0, a1, 4.12, 4.71, WOOD_DARK, level, fw=0.04, dep=0.05,
              off=out * (t / 2 + 0.04))
        n2 = max(2, int((a1 - a0) / 0.15))
        for k in range(1, n2):
            a = a0 + (a1 - a0) * k / n2
            rod(fpt(axis, c, out * (t / 2 + 0.05), a, 4.16),
                fpt(axis, c, out * (t / 2 + 0.05), a, 4.67), 0.022, WOOD_LIGHT, level, 'ext')


def glass_door(axis, c, a0, a1, z0, z1, leaves, level, col=WOOD_DARK, fw=0.07):
    pane(axis, c, a0, a1, z0, z1, GLASS, level, 0.3)
    w = (a1 - a0) / leaves
    frame(axis, c, a0, a1, z0, z1, col, level, fw=fw, dep=0.08,
          mull=[a0 + w * k for k in range(1, leaves)], trans=[z1 - 0.45])


def railing(x0, y0, x1, y1, z0, h, level, kind='ext', spacing=0.16,
            col=WOOD_DARK, bal=WOOD_MID):
    """Straight timber railing with turned-baluster look."""
    p0, p1 = W(x0, y0, z0), W(x1, y1, z0)
    length = mag(p1 - p0)
    up_h = vector(0, h, 0)
    beam(p0 + up_h, p1 + up_h, 0.09, 0.07, col, level, kind)                    # top rail
    beam(p0 + vector(0, 0.08, 0), p1 + vector(0, 0.08, 0), 0.06, 0.05, col, level, kind)
    for p in (p0, p1):
        rod(p, p + up_h, 0.05, col, level, kind)
    n = max(2, int(length / spacing))
    for k in range(1, n):
        p = p0 + (p1 - p0) * (k / n)
        rod(p + vector(0, 0.1, 0), p + up_h, 0.02, bal, level, kind)


def door_leaf(x0, x1, y0, y1, z0, z1, level, kind='int', col=WOOD_MID):
    bx(x0, x1, y0, y1, z0, z1, col, level, kind)


# --------------------------------------------------------------------------
# Furniture helpers
# --------------------------------------------------------------------------
def table(x0, x1, y0, y1, z, h, col, level, leg=0.05, top=0.04):
    bx(x0, x1, y0, y1, z + h - top, z + h, col, level, 'furn')
    for (lx, ly) in ((x0 + leg, y0 + leg), (x1 - leg, y0 + leg),
                     (x0 + leg, y1 - leg), (x1 - leg, y1 - leg)):
        bx(lx - leg / 2, lx + leg / 2, ly - leg / 2, ly + leg / 2, z, z + h - top, col, level, 'furn')


def cabinet(x0, x1, y0, y1, z, h, col, level, top=None):
    bx(x0, x1, y0, y1, z, z + h, col, level, 'furn')
    if top is not None:
        bx(x0 - 0.03, x1 + 0.03, y0 - 0.03, y1 + 0.03, z + h, z + h + 0.04, top, level, 'furn')


def chair(cx, cy, z, back, level, col=WOOD, seat=None):
    """back = side of the backrest: 'N' (rear, -y), 'S' (+y), 'W' (-x), 'E' (+x)."""
    s = 0.22
    seat = seat if seat is not None else col
    bx(cx - s, cx + s, cy - s, cy + s, z + 0.42, z + 0.47, seat, level, 'furn')
    for (lx, ly) in ((cx - s + 0.03, cy - s + 0.03), (cx + s - 0.03, cy - s + 0.03),
                     (cx - s + 0.03, cy + s - 0.03), (cx + s - 0.03, cy + s - 0.03)):
        bx(lx - 0.02, lx + 0.02, ly - 0.02, ly + 0.02, z, z + 0.42, col, level, 'furn')
    if back == 'N':
        bx(cx - s, cx + s, cy - s, cy - s + 0.04, z + 0.47, z + 0.95, col, level, 'furn')
    elif back == 'S':
        bx(cx - s, cx + s, cy + s - 0.04, cy + s, z + 0.47, z + 0.95, col, level, 'furn')
    elif back == 'W':
        bx(cx - s, cx - s + 0.04, cy - s, cy + s, z + 0.47, z + 0.95, col, level, 'furn')
    else:
        bx(cx + s - 0.04, cx + s, cy - s, cy + s, z + 0.47, z + 0.95, col, level, 'furn')



def sofa(x0, x1, y0, y1, z, back, level, col=SOFA, pillow=ACCENT):
    """Upholstered sofa or armchair; `back` is the side of the backrest."""
    bx(x0, x1, y0, y1, z + 0.08, z + 0.44, col, level, 'furn')
    bx(x0 + 0.05, x1 - 0.05, y0 + 0.05, y1 - 0.05, z, z + 0.08, WOOD_DARK, level, 'furn')
    t, a = 0.2, 0.15
    if back in ('N', 'S'):
        yb0, yb1 = (y0, y0 + t) if back == 'N' else (y1 - t, y1)
        bx(x0, x1, yb0, yb1, z + 0.08, z + 0.86, col, level, 'furn')
        bx(x0, x0 + a, y0, y1, z + 0.08, z + 0.62, col, level, 'furn')
        bx(x1 - a, x1, y0, y1, z + 0.08, z + 0.62, col, level, 'furn')
        if x1 - x0 > 1.4:
            py0, py1 = (yb1, yb1 + 0.14) if back == 'N' else (yb0 - 0.14, yb0)
            bx(x0 + 0.25, x0 + 0.65, py0, py1, z + 0.44, z + 0.8, pillow, level, 'furn')
            bx(x1 - 0.65, x1 - 0.25, py0, py1, z + 0.44, z + 0.8, pillow, level, 'furn')
    else:
        xb0, xb1 = (x0, x0 + t) if back == 'W' else (x1 - t, x1)
        bx(xb0, xb1, y0, y1, z + 0.08, z + 0.86, col, level, 'furn')
        bx(x0, x1, y0, y0 + a, z + 0.08, z + 0.62, col, level, 'furn')
        bx(x0, x1, y1 - a, y1, z + 0.08, z + 0.62, col, level, 'furn')
        if y1 - y0 > 1.4:
            px0, px1 = (xb1, xb1 + 0.14) if back == 'W' else (xb0 - 0.14, xb0)
            bx(px0, px1, y0 + 0.25, y0 + 0.65, z + 0.44, z + 0.8, pillow, level, 'furn')
            bx(px0, px1, y1 - 0.65, y1 - 0.25, z + 0.44, z + 0.8, pillow, level, 'furn')


def bookshelf(x0, x1, y0, y1, z, h, level, along='y', palette=BOOK_COLOURS, shelves=5):
    for k in range(shelves + 1):
        zz = z + k * (h - 0.03) / shelves
        bx(x0, x1, y0, y1, zz, zz + 0.03, WOOD_DARK, level, 'furn')
    if along == 'y':
        bx(x0, x1, y0, y0 + 0.03, z, z + h, WOOD_DARK, level, 'furn')
        bx(x0, x1, y1 - 0.03, y1, z, z + h, WOOD_DARK, level, 'furn')
        a0, a1 = y0 + 0.05, y1 - 0.05
    else:
        bx(x0, x0 + 0.03, y0, y1, z, z + h, WOOD_DARK, level, 'furn')
        bx(x1 - 0.03, x1, y0, y1, z, z + h, WOOD_DARK, level, 'furn')
        a0, a1 = x0 + 0.05, x1 - 0.05
    gap = (h - 0.03) / shelves
    for k in range(shelves):
        zb = z + k * gap + 0.03
        s, i = a0, 0
        while s + 0.07 < a1:
            hb = gap * (0.55 + 0.07 * ((i * 7 + k * 3) % 5))
            col = palette[(i + k * 2) % len(palette)]
            if along == 'y':
                bx(x0 + 0.03, x1 - 0.03, s, s + 0.07, zb, zb + hb, col, level, 'furn')
            else:
                bx(s, s + 0.07, y0 + 0.03, y1 - 0.03, zb, zb + hb, col, level, 'furn')
            s += 0.085 if (i % 6) != 5 else 0.2
            i += 1


def plant(x, y, z, r=0.32, pot_h=0.42, pot_r=0.18, level='gf', red=False):
    vcyl(x, y, z, pot_h, pot_r, CLAY, level)
    ball(x, y, z + pot_h + r * 0.7, r, LEAF, level)
    ball(x + r * 0.45, y - r * 0.3, z + pot_h + r * 1.1, r * 0.7, LEAF2, level)
    ball(x - r * 0.4, y + r * 0.35, z + pot_h + r * 1.2, r * 0.65, LEAF2, level)
    if red:
        ball(x, y, z + pot_h + r * 1.5, r * 0.5, LEAF_RED, level)


def rug(x0, x1, y0, y1, z, level, col=rgb(205, 170, 140)):
    bx(x0, x1, y0, y1, z, z + 0.012, col, level, 'floor', texture=T_RUG)


def toilet(cx, cy, z, back, level):
    vcyl(cx, cy, z, 0.4, 0.19, WHITE, level)
    vcyl(cx, cy, z + 0.4, 0.03, 0.21, WHITE, level)
    o0, o1 = 0.28, 0.48
    if back == 'N':
        bx(cx - 0.24, cx + 0.24, cy - o1, cy - o0, z + 0.3, z + 0.8, WHITE, level, 'furn')
    elif back == 'S':
        bx(cx - 0.24, cx + 0.24, cy + o0, cy + o1, z + 0.3, z + 0.8, WHITE, level, 'furn')
    elif back == 'W':
        bx(cx - o1, cx - o0, cy - 0.24, cy + 0.24, z + 0.3, z + 0.8, WHITE, level, 'furn')
    else:
        bx(cx + o0, cx + o1, cy - 0.24, cy + 0.24, z + 0.3, z + 0.8, WHITE, level, 'furn')


def basin(x0, x1, y0, y1, z, level):
    bx(x0, x1, y0, y1, z, z + 0.04, WHITE, level, 'furn')
    bx(x0 + 0.06, x1 - 0.06, y0 + 0.06, y1 - 0.06, z + 0.035, z + 0.045, rgb(205, 215, 220), level, 'furn')


def floor_lamp(x, y, z, level, h=1.55):
    vcyl(x, y, z, 0.03, 0.16, BLACK, level)
    vcyl(x, y, z, h, 0.015, BLACK, level)
    lamp_glow(x, y, z + h + 0.08, 0.15, level)


def pendant(x, y, z_light, z_ceiling, level, r=0.14):
    rod(W(x, y, z_light), W(x, y, z_ceiling), 0.008, BLACK, level, 'furn')
    lamp_glow(x, y, z_light, r, level)


def tree(x, y, h=4.0, r=1.4):
    vcyl(x, y, 0, h * 0.6, 0.13, WOOD_DARK, 'site', 'site')
    ball(x, y, h * 0.65, r, LEAF, 'site', 'site')
    ball(x + r * 0.55, y + r * 0.2, h * 0.55, r * 0.7, LEAF2, 'site', 'site')
    ball(x - r * 0.5, y - r * 0.3, h * 0.6, r * 0.75, LEAF2, 'site', 'site')
    ball(x + 0.1, y - 0.1, h * 0.65 + r * 0.6, r * 0.65, LEAF, 'site', 'site')


def floor_area(x0, x1, y0, y1, z, col, level, texture=None, tile=2.0):
    if texture is None:
        bx(x0, x1, y0, y1, z, z + 0.02, col, level, 'floor')
        return
    nx = max(1, int(math.ceil((x1 - x0) / tile - 1e-6)))
    ny = max(1, int(math.ceil((y1 - y0) / tile - 1e-6)))
    for i in range(nx):
        for j in range(ny):
            bx(x0 + (x1 - x0) * i / nx, x0 + (x1 - x0) * (i + 1) / nx,
               y0 + (y1 - y0) * j / ny, y0 + (y1 - y0) * (j + 1) / ny,
               z, z + 0.02, col, level, 'floor', texture=texture)


# --------------------------------------------------------------------------
# Rooms (used for labels, the jump menu and the tour)
# --------------------------------------------------------------------------
ROOMS = [
    dict(name='Foyer (zaguán)',          level='gf', box=(5.0, 8.5, 7.5, 10.0), z=0.45),
    dict(name='Office',                  level='gf', box=(0.0, 5.0, 6.2, 10.0), z=0.45),
    dict(name='Sala (living room)',      level='gf', box=(8.5, 14.0, 5.0, 10.0), z=0.45),
    dict(name='Dining room',             level='gf', box=(8.5, 14.0, 0.0, 5.0), z=0.45),
    dict(name='Kitchen + breakfast bar', level='gf', box=(0.0, 8.5, 0.0, 3.8), z=0.45),
    dict(name='Pantry',                  level='gf', box=(0.0, 2.6, 3.8, 6.2), z=0.45),
    dict(name='Powder room',             level='gf', box=(2.6, 5.0, 3.8, 6.2), z=0.45),
    dict(name='Dirty kitchen',           level='gf', box=(0.0, 5.0, -3.0, 0.0), z=0.30),
    dict(name='Laundry & service',       level='gf', box=(5.0, 8.5, -3.0, 0.0), z=0.30),
    dict(name='Garden patio',            level='gf', box=(8.5, 14.0, -3.0, 0.0), z=0.05),
    dict(name='Caída (upper lounge)',    level='sf', box=(0.0, 8.5, 7.5, 10.6), z=4.0),
    dict(name='Master bedroom',          level='sf', box=(8.5, 14.0, 4.6, 10.6), z=4.0),
    dict(name='Walk-in closet',          level='sf', box=(8.5, 11.0, 0.0, 4.6), z=4.0),
    dict(name='Master T&B',              level='sf', box=(11.0, 14.0, 0.0, 4.6), z=4.0),
    dict(name='Media room',              level='sf', box=(0.0, 5.0, 3.8, 7.5), z=4.0),
    dict(name='Altar & reading nook',    level='sf', box=(0.0, 2.6, 0.0, 3.8), z=4.0),
    dict(name='Common T&B',              level='sf', box=(2.6, 5.0, 0.0, 3.8), z=4.0),
    dict(name='Linen & storage',         level='sf', box=(6.1, 8.5, 0.0, 3.8), z=4.0),
    dict(name='Roof-deck terrace',       level='sf', box=(0.0, 8.5, -3.0, 0.0), z=4.0),
    dict(name='Balcony',                 level='sf', box=(9.2, 13.3, 10.6, 11.8), z=4.0),
]

F1 = 0.47     # top of ground-floor finish
FA = 0.32     # service wing floor
F2 = 4.02     # top of second-floor finish


# ==========================================================================
# BUILD: site
# ==========================================================================
def build_site():
    S = 'site'
    bx(-70, 84, -70, 16.0, -0.06, 0.0, GRASS, S, 'site')
    bx(-70, 84, 16.6, 26, -0.06, 0.01, ASPHALT, S, 'site')
    bx(-70, 84, 16.0, 16.6, -0.06, 0.08, PAVE, S, 'site')
    bx(-70, 84, 26, 26.6, -0.06, 0.08, PAVE, S, 'site')
    bx(-70, 84, 26.6, 90, -0.06, 0.0, GRASS, S, 'site')
    for x in range(-60, 80, 4):                                     # road markings
        bx(x, x + 2, 21.2, 21.35, 0.01, 0.02, WHITE, S, 'site')
    # perimeter: low stucco wall with gate posts
    bx(-3, 5.15, 15.75, 16.0, 0, 0.9, STUCCO, S, 'site')
    bx(8.35, 17, 15.75, 16.0, 0, 0.9, STUCCO, S, 'site')
    bx(-3.25, -3.0, -16.25, 16.0, 0, 0.9, STUCCO, S, 'site')
    bx(17.0, 17.25, -16.25, 16.0, 0, 0.9, STUCCO, S, 'site')
    bx(-3.25, 17.25, -16.25, -16.0, 0, 0.9, STUCCO, S, 'site')
    for gx in (4.95, 8.25):
        bx(gx, gx + 0.3, 15.7, 16.05, 0, 1.4, STONE_PLAIN, S, 'site')
        lamp_glow(gx + 0.15, 15.87, 1.55, 0.12, S)
    # house-name sign on the front wall
    bx(-1.6, 4.6, 15.98, 16.1, 0.12, 0.88, STONE_TRIM, S, 'site')
    bx(-1.68, 4.68, 15.96, 16.12, 0.84, 0.92, WOOD_DARK, S, 'site')
    try:
        t = text(text=HOUSE_NAME, pos=W(1.5, 16.12, 0.33), height=0.3, depth=0.03,
                 align='center', color=BRASS, shininess=0.6)
        reg(t, S, 'sign')
        SIGN.append(t)
    except Exception:
        pass
    # night sky: moon and stars (shown only at night)
    ball(-48, -62, 22, 2.4, rgb(250, 246, 225), 'night', 'sky', emissive=True)
    k = 0
    for i in range(70):
        a = (i * 137.508) % 360 * math.pi / 180
        r = 120 + (i * 53) % 60
        h = 14 + (i * 29) % 55
        ball(7 + r * math.cos(a), 5 + r * math.sin(a), h, 0.25 + 0.12 * (i % 3),
             rgb(255, 250, 235), 'night', 'sky', emissive=True)
    # paving
    bx(5.45, 8.05, 11.2, 15.75, 0, 0.03, PAVE, S, 'site')
    bx(0, 8.5, -5.0, -3.0, 0, 0.03, PAVE_DARK, S, 'site')
    bx(8.5, 14.0, -3.0, 0.0, 0, 0.05, PAVE, 'gf', 'solid')
    # trees and shrubs
    tree(-1.5, 13.4, 4.2, 1.4)
    tree(15.7, 13.8, 3.8, 1.2)
    tree(-1.8, 4.5, 4.2, 1.2)
    tree(-1.6, -4.6, 3.6, 1.1)
    for (x, y) in ((-2.4, 9.0), (-2.4, 0.5), (16.4, 9.5), (16.4, 6.0), (16.4, 1.5)):
        ball(x, y, 0.4, 0.55, LEAF2, S, 'site')
    for x in (0.0, 1.6, 9.6, 11.2, 12.8, 14.4):
        ball(x, 14.6, 0.35, 0.45, LEAF, S, 'site')


# ==========================================================================
# BUILD: backyard (mini pool + mini park & garden), street life, people
# ==========================================================================
POOL_GLOW = []        # (object, day colour, night colour)
GLOW_BULBS = []       # street and garden lamp bulbs (light up at night)
CAR_LIGHTS = []       # head/tail-light compounds of the cars
MOVERS = []           # animated cars and walkers

BAMBOO = rgb(196, 166, 102)
THATCH = rgb(150, 118, 70)
SOIL = rgb(110, 78, 52)
POOL_FLOOR = rgb(46, 132, 168)
POOL_WATER = rgb(120, 205, 232)
POOL_NIGHT = rgb(70, 205, 255)
POLE = rgb(62, 64, 68)
FLOWERS = [rgb(230, 60, 90), rgb(250, 200, 60), rgb(250, 250, 245), rgb(200, 90, 200), rgb(255, 140, 60)]
SKIN = [rgb(176, 122, 88), rgb(150, 100, 70), rgb(196, 146, 110), rgb(120, 80, 56)]
HAIR = [rgb(28, 22, 18), rgb(52, 36, 26), rgb(20, 20, 22)]
SHIRTS = [rgb(176, 88, 58), rgb(64, 98, 140), rgb(240, 236, 226), rgb(90, 140, 90),
          rgb(220, 180, 60), rgb(140, 70, 120), rgb(40, 40, 46)]
CAR_COLOURS = [rgb(180, 30, 40), rgb(240, 240, 236), rgb(30, 60, 120), rgb(40, 40, 44),
               rgb(200, 170, 60), rgb(90, 110, 100)]


def glow_bulb(x, y, z, r):
    b = sphere(pos=W(x, y, z), radius=r, color=color.gray(0.82), shininess=0.6)
    reg(b, 'site', 'site')
    GLOW_BULBS.append(b)
    return b


def light_pool(x, y, z, r, base=0.25):
    """Warm pool of light on the ground, visible only at night."""
    p = cylinder(pos=W(x, y, z), axis=vector(0, 0.01, 0), radius=r, color=LAMP,
                 opacity=base, emissive=True)
    reg(p, 'night', 'beam', base)


def garden_lamp(x, y, h=0.75):
    vcyl(x, y, 0, h, 0.04, STEEL, 'site', 'site')
    vcyl(x, y, h + 0.16, 0.04, 0.12, STEEL, 'site', 'site')
    glow_bulb(x, y, h + 0.08, 0.1)
    light_pool(x, y, 0.03, 1.3, 0.22)


def bench(x0, x1, y0, y1, back, level='site'):
    bx(x0, x1, y0, y1, 0.42, 0.47, WOOD_MID, level, 'furn')
    for (lx, ly) in ((x0 + 0.06, y0 + 0.06), (x1 - 0.06, y0 + 0.06),
                     (x0 + 0.06, y1 - 0.06), (x1 - 0.06, y1 - 0.06)):
        bx(lx - 0.03, lx + 0.03, ly - 0.03, ly + 0.03, 0, 0.42, STEEL, level, 'furn')
    if back == 'W':
        bx(x0, x0 + 0.05, y0, y1, 0.47, 0.9, WOOD_MID, level, 'furn')
    elif back == 'E':
        bx(x1 - 0.05, x1, y0, y1, 0.47, 0.9, WOOD_MID, level, 'furn')
    elif back == 'N':
        bx(x0, x1, y0, y0 + 0.05, 0.47, 0.9, WOOD_MID, level, 'furn')
    else:
        bx(x0, x1, y1 - 0.05, y1, 0.47, 0.9, WOOD_MID, level, 'furn')


def lounger(x0, x1, y0, y1, z, level='site'):
    """Sun lounger along plan-y with its raised back at the y0 end."""
    bx(x0, x1, y0, y1, z + 0.12, z + 0.3, WOOD_LIGHT, level, 'furn')
    bx(x0 + 0.05, x1 - 0.05, y0 + 0.5, y1 - 0.05, z + 0.3, z + 0.36, WHITE, level, 'furn')
    cx = (x0 + x1) / 2
    beam(W(cx, y0 + 0.5, z + 0.3), W(cx, y0 + 0.07, z + 0.78), (x1 - x0) - 0.08, 0.08, WHITE, level, 'furn')
    for (lx, ly) in ((x0 + 0.06, y0 + 0.1), (x1 - 0.06, y0 + 0.1),
                     (x0 + 0.06, y1 - 0.1), (x1 - 0.06, y1 - 0.1)):
        bx(lx - 0.03, lx + 0.03, ly - 0.03, ly + 0.03, z, z + 0.12, WOOD_DARK, level, 'furn')


def banana(x, y, h=2.6):
    vcyl(x, y, 0, h, 0.1, rgb(120, 140, 70), 'site', 'site')
    for k in range(6):
        a = k * math.pi / 3 + 0.3
        d = vector(math.cos(a), 0, math.sin(a))
        e = ellipsoid(pos=W(x, y, h) + d * 0.62 + vector(0, 0.12, 0), axis=d * 1.3 + vector(0, 0.3, 0),
                      size=vector(1.3, 0.05, 0.42), color=LEAF2 if k % 2 else LEAF)
        put(e, 'site', 'site')


def build_backyard():
    S = 'site'
    # ---------------- Mini pool with sun deck
    for (x0, x1, y0, y1) in ((8.3, 15.8, -11.0, -8.3), (8.3, 15.8, -4.3, -3.4),
                             (8.3, 8.9, -8.3, -4.3), (14.9, 15.8, -8.3, -4.3)):
        bx(x0, x1, y0, y1, 0, 0.12, DECK, S, 'site', texture=T_WOOD)
    for (x0, x1, y0, y1) in ((8.9, 14.9, -8.3, -8.0), (8.9, 14.9, -4.6, -4.3),
                             (8.9, 9.2, -8.0, -4.6), (14.6, 14.9, -8.0, -4.6)):
        bx(x0, x1, y0, y1, 0, 0.16, WHITE, S, 'site')                       # coping
    bx(9.2, 14.6, -8.0, -4.6, 0.0, 0.02, POOL_FLOOR, S, 'site')
    for (x0, x1, y0, y1) in ((9.2, 14.6, -8.0, -7.95), (9.2, 14.6, -4.65, -4.6),
                             (9.2, 9.25, -8.0, -4.6), (14.55, 14.6, -8.0, -4.6)):
        bx(x0, x1, y0, y1, 0.02, 0.12, rgb(90, 170, 200), S, 'site')
    bx(9.25, 10.2, -4.95, -4.65, 0.02, 0.07, WHITE, S, 'site')                 # step
    w = bx(9.25, 14.55, -7.95, -4.65, 0.02, 0.1, POOL_WATER, S, 'pool', base=0.55, shiny=0.9)
    POOL_GLOW.append((w, POOL_WATER, POOL_NIGHT))
    for ly in (-6.0, -5.5):                                                    # ladder
        rod(W(14.45, ly, 0.02), W(14.45, ly, 0.75), 0.02, METAL, S, 'site')
        rod(W(14.45, ly, 0.75), W(14.78, ly, 0.75), 0.02, METAL, S, 'site')
    lounger(9.4, 10.1, -10.8, -8.9, 0.12)
    lounger(10.5, 11.2, -10.8, -8.9, 0.12)
    rod(W(12.4, -9.9, 0.12), W(12.4, -9.9, 2.3), 0.03, WHITE, S, 'site')    # umbrella
    put(cone(pos=W(12.4, -9.9, 1.95), axis=vector(0, 0.5, 0), radius=1.4, color=ACCENT), S, 'site')
    vcyl(11.75, -10.3, 0.12, 0.45, 0.2, WHITE, S, 'site')
    bx(9.5, 10.0, -9.7, -9.2, 0.37, 0.39, ACCENT2, S, 'site')                  # towel
    plant(15.4, -10.6, 0.12, 0.4, level=S, red=True)
    plant(8.7, -10.6, 0.12, 0.36, level=S)
    plant(15.4, -3.8, 0.12, 0.34, level=S)

    # ---------------- Mini park & garden
    pts = [(4.0, -5.1), (4.0, -8.3), (2.3, -8.8), (1.2, -10.2), (-0.8, -11.1)]  # stepping stones
    for (pa, pb) in zip(pts[:-1], pts[1:]):
        d = math.hypot(pb[0] - pa[0], pb[1] - pa[1])
        n = max(1, int(d / 0.55))
        for k in range(n):
            t = k / n
            vcyl(pa[0] + (pb[0] - pa[0]) * t, pa[1] + (pb[1] - pa[1]) * t, 0, 0.04, 0.23, PAVE_DARK, S, 'site')
    # fountain
    fx, fy = 4.2, -10.0
    vcyl(fx, fy, 0, 0.3, 1.2, STONE_TRIM, S, 'site')
    rg = ring(pos=W(fx, fy, 0.42), axis=vector(0, 1, 0), radius=1.12, thickness=0.11, color=STONE_TRIM)
    reg(rg, S, 'site')
    fw = cylinder(pos=W(fx, fy, 0.3), axis=vector(0, 0.14, 0), radius=1.08, color=POOL_WATER, opacity=0.7)
    reg(fw, S, 'pool', 0.7)
    POOL_GLOW.append((fw, POOL_WATER, POOL_NIGHT))
    vcyl(fx, fy, 0.42, 0.75, 0.13, STONE_TRIM, S, 'site')
    vcyl(fx, fy, 1.17, 0.12, 0.45, STONE_TRIM, S, 'site')
    sp = sphere(pos=W(fx, fy, 1.42), radius=0.2, color=POOL_WATER, opacity=0.6)
    reg(sp, S, 'pool', 0.6)
    POOL_GLOW.append((sp, POOL_WATER, POOL_NIGHT))
    for k in range(18):                                                        # flower ring
        a = k * 2 * math.pi / 18
        ball(fx + 1.55 * math.cos(a), fy + 1.55 * math.sin(a), 0.16, 0.15, FLOWERS[k % len(FLOWERS)], S, 'site')
    bench(2.4, 2.85, -10.8, -9.2, 'W')
    bench(3.4, 5.0, -12.1, -11.65, 'N')
    # bahay kubo (bamboo and nipa garden hut)
    kx0, kx1, ky0, ky1 = -2.3, 0.7, -14.7, -11.7
    for (px, py) in ((kx0 + 0.1, ky0 + 0.1), (kx1 - 0.1, ky0 + 0.1), (kx0 + 0.1, ky1 - 0.1), (kx1 - 0.1, ky1 - 0.1)):
        vcyl(px, py, 0, 2.45, 0.09, BAMBOO, S, 'site')
    bx(kx0, kx1, ky0, ky1, 0.55, 0.65, BAMBOO, S, 'site')
    for k in range(1, 10):
        bx(kx0 + k * 0.3 - 0.01, kx0 + k * 0.3 + 0.01, ky0, ky1, 0.65, 0.66, rgb(160, 130, 80), S, 'site')
    beam(W(kx0 + 0.1, ky0 + 0.1, 1.0), W(kx1 - 0.1, ky0 + 0.1, 1.0), 0.07, 0.07, BAMBOO, S, 'site')
    beam(W(kx0 + 0.1, ky0 + 0.1, 1.0), W(kx0 + 0.1, ky1 - 0.1, 1.0), 0.07, 0.07, BAMBOO, S, 'site')
    beam(W(kx1 - 0.1, ky0 + 0.1, 1.0), W(kx1 - 0.1, ky1 - 0.1, 1.0), 0.07, 0.07, BAMBOO, S, 'site')
    bx(-1.3, -0.3, -11.7, -11.45, 0, 0.42, BAMBOO, S, 'site')                  # steps
    bx(-1.3, -0.3, -11.45, -11.2, 0, 0.21, BAMBOO, S, 'site')
    bx(kx0 - 0.45, kx1 + 0.45, ky0 - 0.45, ky1 + 0.45, 2.35, 2.47, rgb(120, 92, 54), S, 'site')
    put(pyramid(pos=W((kx0 + kx1) / 2, (ky0 + ky1) / 2, 2.45), axis=vector(0, 1.9, 0),
                size=vector(1.9, 3.9, 3.9), color=THATCH), S, 'site')
    bx(-1.5, -0.1, -13.6, -12.8, 0.65, 0.95, WOOD_MID, S, 'site')               # dulang (low table)
    for cxs in (-1.75, 0.15):
        bx(cxs - 0.2, cxs + 0.2, -13.4, -13.0, 0.65, 0.75, ACCENT, S, 'site')
    # swing set
    for sx in (5.3, 7.5):
        rod(W(sx, -15.0, 0), W(sx, -14.4, 2.3), 0.05, ACCENT2, S, 'site')
        rod(W(sx, -13.8, 0), W(sx, -14.4, 2.3), 0.05, ACCENT2, S, 'site')
    rod(W(5.2, -14.4, 2.3), W(7.6, -14.4, 2.3), 0.06, ACCENT2, S, 'site')
    for sx in (5.9, 6.9):
        for o in (-0.18, 0.18):
            rod(W(sx + o, -14.4, 2.3), W(sx + o, -14.4, 0.52), 0.012, BLACK, S, 'site')
        bx(sx - 0.22, sx + 0.22, -14.55, -14.25, 0.46, 0.52, ACCENT, S, 'site')
    # flower bed along the rear wall, herb boxes, hedges, trees
    bx(-2.8, 7.8, -15.85, -15.3, 0, 0.25, SOIL, S, 'site')
    x = -2.6
    k = 0
    while x < 7.7:
        ball(x, -15.65, 0.42, 0.2, LEAF if k % 2 else LEAF2, S, 'site')
        ball(x + 0.12, -15.45, 0.38, 0.13, FLOWERS[k % len(FLOWERS)], S, 'site')
        x += 0.38
        k += 1
    for (y0, y1) in ((-7.0, -6.0), (-8.6, -7.6)):
        bx(0.3, 2.3, y0, y1, 0, 0.35, WOOD_MID, S, 'site')
        bx(0.4, 2.2, y0 + 0.1, y1 - 0.1, 0.35, 0.38, SOIL, S, 'site')
        for hx in (0.65, 1.05, 1.45, 1.85):
            ball(hx, (y0 + y1) / 2, 0.48, 0.16, LEAF2, S, 'site')
    bx(-2.98, -2.55, -15.9, -5.5, 0, 0.95, LEAF, S, 'site')
    bx(16.55, 16.98, -15.9, -5.5, 0, 0.95, LEAF, S, 'site')
    tree(6.9, -7.4, 4.6, 1.7)                                                  # mango tree
    tree(15.6, -13.6, 5.0, 1.6)
    banana(-1.7, -7.4)
    banana(-1.6, -9.5, 2.3)
    banana(16.1, -12.0)
    for (lx, ly) in ((4.55, -6.5), (3.3, -8.3), (0.8, -9.8), (-1.7, -11.2), (8.5, -11.4),
                     (15.6, -11.4), (7.8, -12.6)):
        garden_lamp(lx, ly)


def street_light(x, y, s):
    """Lamp post on the sidewalk; s = +1 arm reaches toward +y, -1 toward -y."""
    S = 'site'
    ly = y + 1.35 * s
    rod(W(x, y, 0.08), W(x, y, 5.6), 0.08, POLE, S, 'site')
    rod(W(x, y, 5.5), W(x, ly, 5.75), 0.05, POLE, S, 'site')
    bx(x - 0.28, x + 0.28, ly - 0.17, ly + 0.17, 5.62, 5.8, POLE, S, 'site')
    glow_bulb(x, ly, 5.56, 0.15)
    c = cone(pos=W(x, ly, 0.05), axis=vector(0, 5.45, 0), radius=2.6, color=LAMP,
             opacity=0.07, emissive=True)
    reg(c, 'night', 'beam', 0.07)
    light_pool(x, ly, 0.1, 3.0, 0.22)


def person(x, y, z, facing, shirt, pants=rgb(50, 60, 82), skin=SKIN[0], hair=HAIR[0],
           scale=1.0, pose='stand'):
    """A simple human figure; returns its parts (not yet registered).
    facing = direction in radians in the plan (0 = +x, pi/2 = +y toward the street)."""
    s = scale
    f = vector(math.cos(facing), 0, math.sin(facing))
    side = vector(-f.z, 0, f.x)
    up = vector(0, 1, 0)
    base = W(x, y, z)
    parts = []

    def cyl(p0, p1, r, col):
        parts.append(cylinder(pos=p0, axis=p1 - p0, radius=r * s, color=col))

    def sph(p, r, col):
        parts.append(sphere(pos=p, radius=r * s, color=col))

    if pose == 'sit':
        seat = 0.45 * s
        for o in (-0.1, 0.1):
            hip = base + side * (o * s) + up * seat
            knee = hip + f * (0.45 * s)
            cyl(hip, knee, 0.065, pants)
            cyl(knee, knee - up * seat, 0.06, pants)
        top = seat + 0.58 * s
        cyl(base + up * seat, base + up * top, 0.17, shirt)
        for o in (-0.24, 0.24):
            sh = base + side * (o * s) + up * (top - 0.04 * s)
            hand = sh + f * (0.28 * s) - up * (0.38 * s)
            cyl(sh, hand, 0.05, shirt)
            sph(hand, 0.055, skin)
    else:
        hip = 0.82 * s
        for o in (-0.1, 0.1):
            foot = base + side * (o * s)
            cyl(foot, foot + up * hip, 0.065, pants)
            sph(foot + f * (0.04 * s) + up * (0.03 * s), 0.07, BLACK)
        top = 1.42 * s
        cyl(base + up * (hip - 0.05 * s), base + up * top, 0.17, shirt)
        for o in (-0.24, 0.24):
            sh = base + side * (o * s) + up * (top - 0.04 * s)
            hand = base + side * (o * 1.05 * s) + up * (0.82 * s)
            cyl(sh, hand, 0.05, shirt)
            sph(hand, 0.055, skin)
    cyl(base + up * top, base + up * (top + 0.08 * s), 0.05, skin)
    sph(base + up * (top + 0.18 * s), 0.12, skin)
    sph(base + up * (top + 0.23 * s) - f * (0.03 * s), 0.115, hair)
    return parts


def place_person(level, *args, **kw):
    c = compound(person(*args, **kw))
    reg(c, level, 'person')
    return c


def make_car(x, lane_y, dirn, col, speed):
    parts = []

    def b(x0, x1, y0, y1, z0, z1, c):
        parts.append(box(pos=W((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                         size=vector(x1 - x0, z1 - z0, y1 - y0), color=c, shininess=0.7))

    L2 = 2.1
    b(x - L2, x + L2, lane_y - 0.88, lane_y + 0.88, 0.32, 0.95, col)
    c0, c1 = sorted((x - 1.15 * dirn, x + 0.95 * dirn))
    b(c0, c1, lane_y - 0.8, lane_y + 0.8, 0.95, 1.42, rgb(40, 52, 62))
    b(c0 + 0.1, c1 - 0.1, lane_y - 0.78, lane_y + 0.78, 1.4, 1.47, col)
    for wx in (x - 1.35, x + 1.35):
        for wy in (lane_y - 0.8, lane_y + 0.8):
            parts.append(cylinder(pos=W(wx, wy - 0.13, 0.33), axis=vector(0, 0, 0.26),
                                  radius=0.33, color=BLACK))
    body = compound(parts)
    hx, tx = x + (L2 + 0.01) * dirn, x - (L2 + 0.01) * dirn
    lp = []
    for oy in (-0.6, 0.6):
        lp.append(box(pos=W(hx, lane_y + oy, 0.75), size=vector(0.04, 0.12, 0.3), color=rgb(255, 250, 225)))
        lp.append(box(pos=W(tx, lane_y + oy, 0.78), size=vector(0.04, 0.1, 0.3), color=rgb(210, 20, 20)))
    lights = compound(lp)
    CAR_LIGHTS.append(lights)
    bm = cone(pos=W(hx + 9.0 * dirn, lane_y, 0.05), axis=vector(-8.9 * dirn, 0.65, 0), radius=1.8,
              color=rgb(255, 240, 200), opacity=0.12, emissive=True)
    reg(bm, 'night', 'beam', 0.12)
    MOVERS.append(dict(objs=[(o, vector(o.pos)) for o in (body, lights, bm)], x=x, x0=x,
                       speed=speed, dirn=dirn, xmin=-60.0, xmax=74.0, bob=0.0, t=0.0))


def make_walker(x, y, dirn, speed, shirt, level=('site', 'day'), skin=SKIN[1], scale=1.0):
    c = compound(person(x, y, 0.08, 0.0 if dirn > 0 else math.pi, shirt, skin=skin, scale=scale))
    reg(c, level, 'person')
    MOVERS.append(dict(objs=[(c, vector(c.pos))], x=x, x0=x, speed=speed, dirn=dirn,
                       xmin=-45.0, xmax=60.0, bob=0.04, t=x))


def build_street_life():
    for x in (-40, -26, -12, 2, 16, 30, 44, 58):
        street_light(x, 16.45, +1)
    for x in (-33, -19, -5, 9, 23, 37, 51):
        street_light(x, 26.15, -1)
    for (x, lane, d, ci, v) in ((-30, 19.0, 1, 0, 9.0), (10, 19.0, 1, 2, 10.5), (45, 19.0, 1, 4, 8.0),
                                (60, 23.6, -1, 1, 9.5), (20, 23.6, -1, 3, 11.0), (-15, 23.6, -1, 5, 8.5)):
        make_car(x, lane, d, CAR_COLOURS[ci], v)
    make_walker(-20.0, 16.25, 1, 1.3, SHIRTS[1], skin=SKIN[0])
    make_walker(25.0, 16.25, -1, 1.1, SHIRTS[4], skin=SKIN[2])
    make_walker(5.0, 26.35, -1, 1.4, SHIRTS[5], skin=SKIN[3])
    make_walker(-5.0, 26.35, 1, 1.2, SHIRTS[2], level='site', skin=SKIN[1])   # out at night too


def build_people():
    D, N = 'day', 'night'
    # daytime: family outdoors
    place_person(('site', D), 12.2, -6.1, -0.95, 0.0, SHIRTS[0], skin=SKIN[0])            # swimmer
    place_person(('site', D), 13.4, -9.4, 0.12, math.pi / 2, SHIRTS[2], skin=SKIN[2])     # by the pool
    place_person(('site', D), 2.65, -10.0, 0.0, 0.0, SHIRTS[3], skin=SKIN[1], pose='sit')  # bench
    place_person(('site', D), 6.4, -13.1, 0.0, -1.2, SHIRTS[4], skin=SKIN[0], scale=0.62)  # kids
    place_person(('site', D), 5.6, -8.9, 0.0, 2.5, SHIRTS[5], skin=SKIN[2], scale=0.6)
    place_person(('site', D), 1.2, -15.0, 0.0, -math.pi / 2, SHIRTS[3], skin=SKIN[3])     # gardener
    place_person(('gf', D), 11.25, -2.15, 0.05, math.pi / 2, SHIRTS[1], skin=SKIN[1], pose='sit')
    place_person(('sf', D), 6.2, -2.0, F2, -math.pi / 2, SHIRTS[6], skin=SKIN[2])          # terrace
    # night: everyone is home, lights on
    place_person(('gf', N), 10.9, 9.35, F1, -math.pi / 2, SHIRTS[1], skin=SKIN[1], pose='sit')
    place_person(('gf', N), 12.2, 9.35, F1, -math.pi / 2, SHIRTS[0], skin=SKIN[2], pose='sit')
    place_person(('gf', N), 6.4, 0.95, F1, math.pi / 2, SHIRTS[2], skin=SKIN[0])           # kitchen island
    place_person(('sf', N), 2.2, 9.9, F2, -math.pi / 2, SHIRTS[5], skin=SKIN[3], pose='sit')
    place_person(('sf', N), 10.6, 11.45, F2, math.pi / 2, SHIRTS[4], skin=SKIN[0])        # balcony


def update_movers(dt):
    for m in MOVERS:
        m['x'] += m['speed'] * m['dirn'] * dt
        if m['dirn'] > 0 and m['x'] > m['xmax']:
            m['x'] = m['xmin']
        elif m['dirn'] < 0 and m['x'] < m['xmin']:
            m['x'] = m['xmax']
        m['t'] += dt
        dy = m['bob'] * abs(math.sin(m['t'] * 6.0)) if m['bob'] else 0.0
        off = vector(m['x'] - m['x0'], dy, 0)
        for (o, base) in m['objs']:
            o.pos = base + off


# ==========================================================================
# BUILD: ground floor
# ==========================================================================
def build_ground_floor():
    L = 'gf'
    # raised floor platform (plinth) and service-wing base
    bx(-0.15, 14.15, -0.15, 10.15, 0, 0.45, PLINTH, L, 'solid')
    bx(-0.125, 8.625, -3.125, 0.0, 0, 0.3, PLINTH, L, 'solid')
    # entrance steps
    bx(5.45, 8.05, 10.8, 11.2, 0, 0.15, STONE_TRIM, L, 'solid')
    bx(5.45, 8.05, 10.4, 10.8, 0, 0.30, STONE_TRIM, L, 'solid')
    bx(5.45, 8.05, 10.15, 10.4, 0, 0.45, STONE_TRIM, L, 'solid')

    # ---- floors
    floor_area(0, 5, 6.2, 10, 0.45, FLOOR_WOOD, L, T_WOOD)                 # office
    floor_area(5, 8.5, 7.5, 10, 0.45, FLOOR_STONE, L, T_GRANITE)           # foyer
    floor_area(8.5, 14, 0, 10, 0.45, FLOOR_WOOD, L, T_WOOD, tile=2.75)     # sala + dining
    floor_area(0, 8.5, 0, 3.8, 0.45, FLOOR_TILE, L)                        # kitchen
    floor_area(0, 2.6, 3.8, 6.2, 0.45, FLOOR_TILE, L)                      # pantry
    floor_area(2.6, 5, 3.8, 6.2, 0.45, FLOOR_BATH, L)                      # powder room
    floor_area(5, 8.5, 3.8, 7.5, 0.45, FLOOR_STONE, L)                     # hall + stair
    floor_area(0, 8.5, -3, 0, 0.30, FLOOR_SERV, L)                         # service wing

    # ---- exterior stone walls (0.30 m)
    ZT = 3.6
    wall('x', 10.0, -0.15, 14.15, 0.45, ZT, 0.3, STONE, L, 'ext', texture=T_STONE, joints=+1,
         openings=[(1.5, 3.5, 1.0, 2.9), (6.0, 7.5, 0.45, 2.6), (10.25, 12.25, 1.0, 2.9)])
    wall('x', 0.0, -0.15, 14.15, 0.45, ZT, 0.3, STONE, L, 'ext', texture=T_STONE, joints=-1,
         openings=[(2.0, 2.9, 0.45, 2.6), (9.5, 13.0, 0.45, 3.0)])
    wall('y', 0.0, 0.15, 9.85, 0.45, ZT, 0.3, STONE, L, 'ext', texture=T_STONE, joints=-1,
         openings=[(1.0, 2.8, 1.3, 2.6), (4.5, 5.3, 1.9, 2.6), (7.0, 9.2, 1.0, 2.9)])
    wall('y', 14.0, 0.15, 9.85, 0.45, ZT, 0.3, STONE, L, 'ext', texture=T_STONE, joints=+1,
         openings=[(1.0, 4.0, 0.9, 2.9), (6.4, 8.6, 1.0, 2.9)])
    for (cx, cy) in ((0, 0), (14, 0), (0, 10), (14, 10)):                  # quoins
        bx(cx - 0.21, cx + 0.21, cy - 0.21, cy + 0.21, 0.45, ZT, STONE_TRIM, L, 'ext', texture=T_STONE)

    # ---- service wing walls (lime stucco, 0.25 m)
    ZA = 3.75
    wall('y', 0.0, -3.125, -0.15, 0.3, ZA, 0.25, STUCCO, L, 'ext', texture=T_STUCCO,
         openings=[(-2.3, -0.7, 1.4, 2.6)])
    wall('x', -3.0, -0.125, 8.625, 0.3, ZA, 0.25, STUCCO, L, 'ext', texture=T_STUCCO,
         openings=[(1.5, 3.5, 1.4, 2.6), (6.2, 7.1, 0.3, 2.6), (7.4, 8.1, 1.8, 2.5)])
    wall('y', 8.5, -2.875, -0.15, 0.3, ZA, 0.25, STUCCO, L, 'ext', texture=T_STUCCO,
         openings=[(-2.0, -1.0, 1.6, 2.5)])

    # ---- windows and exterior doors
    gf_window('x', 10.0, +1, 1.5, 3.5, 1.0, 2.9)                   # office front
    gf_window('x', 10.0, +1, 10.25, 12.25, 1.0, 2.9)               # sala front
    gf_window('y', 0.0, -1, 1.0, 2.8, 1.3, 2.6, grille=False)      # kitchen
    louver_window('y', 0.0, -1, 4.5, 5.3, 1.9, 2.6)                # pantry
    gf_window('y', 0.0, -1, 7.0, 9.2, 1.0, 2.9)                    # office side
    gf_window('y', 14.0, +1, 1.0, 4.0, 0.9, 2.9, grille=False)     # dining
    gf_window('y', 14.0, +1, 6.4, 8.6, 1.0, 2.9)                   # sala side
    louver_window('y', 0.0, -1, -2.3, -0.7, 1.4, 2.6)              # dirty kitchen
    louver_window('x', -3.0, -1, 1.5, 3.5, 1.4, 2.6)               # dirty kitchen rear
    louver_window('x', -3.0, -1, 7.4, 8.1, 1.8, 2.5)               # laundry
    louver_window('y', 8.5, +1, -2.0, -1.0, 1.6, 2.5)              # laundry side
    # dining sliding doors to the patio
    pane('x', 0.0, 9.5, 13.0, 0.45, 3.0, GLASS, L, 0.32)
    frame('x', 0.0, 9.5, 13.0, 0.45, 3.0, STEEL, L, fw=0.06, dep=0.08,
          mull=[10.375, 11.25, 12.125])
    fbox('x', 0.0, -0.18, 0.08, 9.35, 13.15, 3.0, 3.2, STONE_TRIM, L, 'ext')
    # laundry back door (closed) with wall lamp
    door_leaf(6.2, 7.1, -3.03, -2.97, 0.3, 2.6, L, 'ext', WOOD_MID)
    bx(7.25, 7.4, -3.2, -3.12, 1.95, 2.3, BLACK, L, 'ext')
    lamp_glow(7.32, -3.22, 2.1, 0.06, L)

    # main door: double narra leaves with an arched fanlight
    for (a0, a1) in ((6.0, 6.75), (6.75, 7.5)):
        bx(a0 + 0.005, a1 - 0.005, 9.97, 10.03, 0.45, 2.6, WOOD_MID, L, 'ext')
        for (h0, h1) in ((0.65, 1.2), (1.3, 1.8)):
            bx(a0 + 0.1, a1 - 0.1, 10.03, 10.05, h0, h1, WOOD_DARK, L, 'ext')
    bx(6.68, 6.71, 10.05, 10.09, 1.15, 1.5, BRASS, L, 'ext')
    bx(6.79, 6.82, 10.05, 10.09, 1.15, 1.5, BRASS, L, 'ext')
    rod(W(6.75, 9.83, 2.6), W(6.75, 10.17, 2.6), 0.75, WOOD_MID, L, 'ext')
    bx(5.72, 6.0, 10.12, 10.21, 0.45, 2.6, STONE_TRIM, L, 'ext')
    bx(7.5, 7.78, 10.12, 10.21, 0.45, 2.6, STONE_TRIM, L, 'ext')
    bx(6.6, 6.9, 10.12, 10.23, 3.2, 3.5, STONE_TRIM, L, 'ext')
    for lx in (5.4, 8.1):                                           # door lanterns
        bx(lx - 0.1, lx + 0.1, 10.15, 10.35, 2.0, 2.45, BLACK, L, 'ext')
        lamp_glow(lx, 10.36, 2.22, 0.08, L)
    # planters and pots
    for (p0, p1) in ((1.2, 3.8), (9.95, 12.55)):
        bx(p0, p1, 10.2, 10.7, 0, 0.95, STONE_TRIM, L, 'solid')
        k = p0 + 0.35
        while k < p1 - 0.2:
            ball(k, 10.45, 1.12, 0.3, LEAF if int(k * 3) % 2 else LEAF2, L)
            k += 0.55
        ball(p0 + 0.7, 10.45, 1.45, 0.22, LEAF_RED, L)
        ball(p1 - 0.7, 10.45, 1.45, 0.22, LEAF_RED, L)
    plant(5.2, 10.28, 0.45, 0.34, level=L)
    plant(8.3, 10.28, 0.45, 0.34, level=L)

    # ---- interior partitions
    ZI, TI = 3.6, 0.12
    wall('y', 5.0, 3.8, 10.0, 0.45, ZI, TI, INT_WALL, L, 'int',
         openings=[(4.5, 5.3, 0.45, 2.55), (8.2, 9.1, 0.45, 2.55)])
    wall('x', 6.2, 0.15, 5.0, 0.45, ZI, TI, INT_WALL, L, 'int')
    wall('x', 3.8, 0.15, 5.0, 0.45, ZI, TI, INT_WALL, L, 'int', openings=[(0.8, 1.6, 0.45, 2.55)])
    wall('y', 2.6, 3.8, 6.2, 0.45, ZI, TI, INT_WALL, L, 'int')
    wall('y', 6.1, 3.8, 7.5, 0.45, ZI, TI, INT_WALL, L, 'int')
    wall('x', 3.8, 6.1, 8.5, 0.45, ZI, TI, INT_WALL, L, 'int')
    wall('y', 8.5, 3.8, 9.85, 0.45, ZI, TI, INT_WALL, L, 'int', openings=[(7.8, 9.6, 0.45, 3.1)])
    wall('y', 5.0, -2.875, -0.15, 0.3, ZA, TI, INT_WALL, L, 'int', openings=[(-2.2, -1.2, 0.3, 2.4)])
    # interior doors, shown open
    door_leaf(4.1, 5.0, 9.05, 9.1, 0.45, 2.55, L)       # office
    door_leaf(4.2, 5.0, 5.25, 5.3, 0.45, 2.55, L)       # powder room
    door_leaf(0.8, 0.85, 3.8, 4.6, 0.45, 2.55, L)       # pantry
    door_leaf(1.97, 2.03, -0.9, -0.15, 0.3, 2.55, L)    # kitchen -> dirty kitchen

    # ---- U-shaped stair with floating timber treads
    run = 2.55 / 9
    for i in range(9):                                   # flight A: up from the foyer
        y1 = 7.5 - i * run
        top = 0.45 + (i + 1) * 0.1775
        bx(7.36, 8.44, y1 - run, y1, top - 0.06, top, WOOD_MID, L, 'furn')
    bx(6.16, 8.44, 3.86, 4.95, 2.225 - 0.12, 2.225, WOOD_MID, L, 'furn')     # landing
    for i in range(9):                                   # flight B: up to the caída
        y0 = 4.95 + i * run
        top = 2.225 + (i + 1) * 0.1775
        bx(6.16, 7.24, y0, y0 + run, top - 0.06, top, WOOD_MID, L, 'furn')
    bx(7.25, 7.35, 4.95, 7.5, 0.45, 3.6, INT_WALL, L, 'int')                # spine wall
    rod(W(7.3, 7.5, 1.35), W(7.3, 4.95, 3.05), 0.025, WOOD_DARK, L, 'furn')
    rod(W(7.3, 4.95, 3.05), W(7.3, 7.5, 4.65), 0.025, WOOD_DARK, L, 'furn')

    # ---- ground-floor ceiling beams (vigas) under the timber floor
    for yb in (1.3, 2.9, 8.6):
        bx(0.15, 13.85, yb - 0.07, yb + 0.07, 3.42, 3.6, WOOD_DARK, 'sf', 'solid')

    build_ground_furniture()
    build_patio()


def build_ground_furniture():
    L, z = 'gf', F1
    # ---------------- Office
    rug(0.9, 4.1, 7.0, 9.7, z, L, rgb(196, 176, 150))
    table(1.3, 3.7, 8.75, 9.45, z, 0.75, WOOD_DARK, L)
    bx(2.1, 2.9, 9.17, 9.21, z + 0.82, z + 1.28, BLACK, L, 'furn')          # monitor
    bx(2.45, 2.55, 9.2, 9.3, z + 0.75, z + 0.83, BLACK, L, 'furn')
    bx(2.2, 2.8, 8.85, 9.05, z + 0.75, z + 0.77, rgb(60, 60, 64), L, 'furn')  # keyboard
    vcyl(1.55, 9.2, z + 0.75, 0.35, 0.012, BLACK, L)
    lamp_glow(1.55, 9.12, z + 1.12, 0.07, L)
    chair(2.5, 8.3, z, 'N', L, col=BLACK, seat=LEATHER)
    bookshelf(4.45, 4.85, 6.4, 8.0, z, 2.0, L, along='y')
    sofa(0.45, 1.3, 6.55, 7.4, z, 'W', L, col=ACCENT2)
    vcyl(1.65, 6.95, z, 0.5, 0.025, WOOD_DARK, L)
    vcyl(1.65, 6.95, z + 0.5, 0.03, 0.22, WOOD_DARK, L)
    plant(0.45, 9.6, z, 0.36, level=L)
    # ---------------- Foyer
    bx(5.12, 5.5, 9.2, 9.9, z, z + 0.45, WOOD_DARK, L, 'furn')
    bx(5.14, 5.48, 9.22, 9.88, z + 0.45, z + 0.52, ACCENT, L, 'furn')
    plant(8.15, 9.7, z, 0.34, level=L, red=True)
    bx(5.06, 5.08, 7.9, 8.1, z + 1.2, z + 1.8, BRASS, L, 'furn')             # framed santo niche
    pendant(6.75, 8.75, 3.0, 3.42, L, r=0.18)
    # ---------------- Sala
    rug(9.8, 13.4, 6.6, 8.7, z, L)
    sofa(10.0, 13.2, 8.95, 9.8, z, 'S', L)
    sofa(9.0, 9.8, 7.0, 7.8, z, 'W', L, col=ACCENT)
    sofa(13.0, 13.8, 7.0, 7.8, z, 'E', L, col=ACCENT)
    table(10.8, 12.4, 7.25, 8.0, z, 0.42, WOOD_DARK, L)
    bx(11.0, 11.4, 7.45, 7.75, z + 0.42, z + 0.47, rgb(200, 180, 140), L, 'furn')
    vcyl(11.9, 7.6, z + 0.42, 0.2, 0.06, CLAY, L)
    bx(10.3, 12.9, 5.15, 5.55, z, z + 0.5, WOOD_DARK, L, 'furn')             # TV console
    bx(10.7, 12.5, 5.3, 5.36, z + 0.66, z + 1.66, BLACK, L, 'furn')          # TV
    floor_lamp(13.6, 9.6, z, L)
    plant(9.05, 9.6, z, 0.42, level=L)
    plant(13.6, 5.4, z, 0.36, level=L, red=True)
    pendant(11.25, 7.6, 3.0, 3.42, L, r=0.22)
    # ---------------- Dining
    table(9.9, 12.5, 1.6, 2.7, z, 0.76, WOOD_DARK, L, leg=0.07)
    for cx in (10.4, 11.2, 12.0):
        chair(cx, 1.3, z, 'N', L, col=WOOD_DARK, seat=SOFA)
        chair(cx, 3.0, z, 'S', L, col=WOOD_DARK, seat=SOFA)
    cabinet(13.45, 13.85, 1.3, 3.7, z, 0.85, WOOD_DARK, L)
    vcyl(13.65, 2.5, z + 0.85, 0.35, 0.09, CLAY, L)
    ball(13.65, 2.5, z + 1.3, 0.16, LEAF2, L)
    for px in (10.5, 11.2, 11.9):
        pendant(px, 2.15, 2.65, 3.42, L, r=0.11)
    plant(13.55, 0.45, z, 0.36, level=L)
    # ---------------- Kitchen
    cabinet(0.15, 0.75, 0.15, 3.65, z, 0.88, CABINET, L, top=COUNTER)
    cabinet(0.75, 1.9, 0.15, 0.75, z, 0.88, CABINET, L, top=COUNTER)
    cabinet(3.0, 4.85, 0.15, 0.75, z, 0.88, CABINET, L, top=COUNTER)
    bx(0.25, 0.65, 1.3, 2.05, z + 0.9, z + 0.93, METAL, L, 'furn')          # sink
    rod(W(0.2, 1.68, z + 0.92), W(0.2, 1.68, z + 1.2), 0.015, METAL, L, 'furn')
    bx(3.3, 4.05, 0.2, 0.7, z + 0.92, z + 0.95, BLACK, L, 'furn')            # hob
    for (hx, hy) in ((3.48, 0.33), (3.87, 0.33), (3.48, 0.57), (3.87, 0.57)):
        vcyl(hx, hy, z + 0.95, 0.01, 0.08, rgb(60, 60, 60), L)
    bx(3.25, 4.1, 0.15, 0.6, z + 1.65, z + 2.25, METAL, L, 'furn')           # range hood
    bx(0.15, 0.5, 0.15, 0.95, z + 1.5, z + 2.3, CABINET, L, 'furn')          # upper cabinets
    bx(0.15, 0.5, 2.85, 3.65, z + 1.5, z + 2.3, CABINET, L, 'furn')
    bx(0.75, 1.9, 0.15, 0.5, z + 1.5, z + 2.3, CABINET, L, 'furn')
    bx(4.15, 4.85, 0.15, 0.5, z + 1.5, z + 2.3, CABINET, L, 'furn')
    bx(4.15, 4.85, 2.9, 3.65, z, z + 1.85, METAL, L, 'furn')                 # refrigerator
    bx(4.12, 4.14, 3.0, 3.06, z + 0.9, z + 1.5, BLACK, L, 'furn')
    cabinet(5.6, 7.9, 1.3, 2.2, z, 0.88, CABINET, L)                          # island
    bx(5.5, 8.0, 1.2, 2.3, z + 0.88, z + 0.93, COUNTER, L, 'furn')
    for sx in (6.0, 6.75, 7.5):
        vcyl(sx, 2.6, z, 0.66, 0.03, METAL, L)
        vcyl(sx, 2.6, z + 0.66, 0.06, 0.2, LEATHER, L)
        pendant(sx, 1.75, 2.6, 3.42, L, r=0.11)
    vcyl(6.75, 1.75, z + 0.93, 0.08, 0.18, WHITE, L)
    ball(6.7, 1.72, z + 1.05, 0.06, rgb(230, 170, 40), L)
    ball(6.82, 1.8, z + 1.05, 0.06, rgb(120, 170, 60), L)
    # ---------------- Pantry
    bookshelf(0.15, 0.55, 4.0, 6.0, z, 2.1, L, along='y', palette=[CLAY, WHITE, rgb(200, 180, 120), ACCENT2])
    bookshelf(0.55, 2.45, 5.65, 6.05, z, 2.1, L, along='x', palette=[rgb(220, 200, 150), CLAY, WHITE])
    vcyl(1.9, 4.4, z, 0.6, 0.22, rgb(210, 190, 150), L)                       # rice bin
    # ---------------- Powder room
    toilet(3.3, 5.55, z, 'S', L)
    cabinet(3.0, 3.7, 3.95, 4.4, z, 0.8, WOOD_DARK, L)
    basin(3.05, 3.65, 4.0, 4.35, z + 0.8, L)
    bx(3.05, 3.65, 3.87, 3.89, z + 1.1, z + 1.8, MIRROR, L, 'furn', shiny=0.9)
    pendant(3.8, 5.0, 3.0, 3.42, L, r=0.09)
    # ---------------- Dirty kitchen
    z = FA
    cabinet(0.15, 4.85, -2.85, -2.25, z, 0.86, CONCRETE, L, top=rgb(120, 150, 140))
    bx(1.6, 2.3, -2.8, -2.3, z + 0.9, z + 0.93, METAL, L, 'furn')
    rod(W(1.95, -2.82, z + 0.92), W(1.95, -2.82, z + 1.2), 0.015, METAL, L, 'furn')
    bx(3.4, 4.3, -2.8, -2.3, z + 0.9, z + 1.0, BLACK, L, 'furn')
    vcyl(3.62, -2.55, z + 1.0, 0.18, 0.15, CLAY, L)                           # palayok
    vcyl(4.05, -2.55, z + 1.0, 0.12, 0.17, rgb(60, 60, 60), L)                # kawali
    vcyl(4.55, -1.9, z, 0.6, 0.17, rgb(46, 92, 160), L)                       # LPG tank
    table(3.2, 4.5, -1.6, -0.9, z, 0.8, WOOD_MID, L)
    chair(3.85, -0.65, z, 'S', L)
    s = ellipsoid(pos=W(0.55, -0.55, z + 0.35), size=vector(0.6, 0.7, 0.6), color=CLAY)
    reg(s, L, 'furn')                                                         # banga (water jar)
    bx(4.55, 4.88, -0.8, -0.2, z + 1.4, z + 1.43, WOOD_MID, L, 'furn')
    pendant(2.5, -1.5, 2.9, 3.75, L, r=0.12)
    # ---------------- Laundry
    for (y0, y1) in ((-1.55, -0.9), (-0.85, -0.2)):
        bx(7.7, 8.35, y0, y1, z, z + 0.85, WHITE, L, 'furn')
        r_ = ring(pos=W(7.69, (y0 + y1) / 2, z + 0.45), axis=vector(1, 0, 0), radius=0.18,
                  thickness=0.03, color=METAL)
        reg(r_, L, 'furn')
    cabinet(7.6, 8.35, -2.85, -2.35, z, 0.85, CONCRETE, L)
    basin(7.65, 8.3, -2.8, -2.4, z + 0.85, L)
    bx(5.15, 7.15, -0.45, -0.15, z + 1.5, z + 1.53, WOOD_MID, L, 'furn')
    for k, bxx in enumerate((5.4, 5.7, 6.0, 6.5, 6.8)):
        vcyl(bxx, -0.3, z + 1.53, 0.25, 0.07, [ACCENT2, WHITE, ACCENT, rgb(230, 200, 60), WHITE][k], L)
    vcyl(5.6, -1.6, z, 0.45, 0.25, rgb(190, 160, 110), L)                     # basket
    pendant(6.6, -1.5, 2.9, 3.75, L, r=0.11)


def build_patio():
    L = 'gf'
    for (px, py) in ((8.5, -3.0), (13.8, -3.0), (13.8, -0.2), (8.5, -0.2)):
        bx(px, px + 0.2, py, py + 0.2, 0.05, 2.88, WOOD_DARK, L, 'furn')
    bx(8.5, 8.7, -3.0, 0.0, 2.88, 3.12, WOOD_MID, L, 'furn')
    bx(13.8, 14.0, -3.0, 0.0, 2.88, 3.12, WOOD_MID, L, 'furn')
    for ry in (-0.5, -1.25, -2.0, -2.75):
        bx(8.4, 14.1, ry - 0.06, ry + 0.06, 3.12, 3.3, WOOD_DARK, L, 'furn')
    for (vx, vy) in ((9.4, -1.6), (10.6, -0.8), (11.9, -2.3), (13.2, -1.1), (12.4, -0.4)):
        ball(vx, vy, 3.35, 0.45, LEAF2, L)
    vcyl(11.25, -1.3, 0.05, 0.7, 0.05, STEEL, L)
    vcyl(11.25, -1.3, 0.75, 0.04, 0.6, WHITE, L)
    chair(11.25, -2.15, 0.05, 'N', L, col=STEEL, seat=WHITE)
    chair(11.25, -0.45, 0.05, 'S', L, col=STEEL, seat=WHITE)
    chair(10.4, -1.3, 0.05, 'W', L, col=STEEL, seat=WHITE)
    chair(12.1, -1.3, 0.05, 'E', L, col=STEEL, seat=WHITE)
    plant(13.5, -2.6, 0.05, 0.4, level=L, red=True)
    plant(9.0, -2.6, 0.05, 0.36, level=L)


# ==========================================================================
# BUILD: second floor
# ==========================================================================
def build_second_floor():
    L = 'sf'
    # ---- timber floor structure (with stair opening) and volada
    for (x0, x1, y0, y1) in ((-0.15, 14.15, -0.15, 3.8), (-0.15, 14.15, 7.5, 10.75),
                             (-0.15, 6.1, 3.8, 7.5), (8.5, 14.15, 3.8, 7.5)):
        bx(x0, x1, y0, y1, 3.6, 4.0, WOOD_PLAIN, L, 'solid')
    for x in (0.3, 3.0, 5.2, 8.3, 11.0, 13.7):                           # corbels
        beam(W(x, 10.15, 3.0), W(x, 10.66, 3.62), 0.14, 0.14, WOOD_DARK, L, 'ext')
        bx(x - 0.08, x + 0.08, 10.1, 10.7, 3.45, 3.6, WOOD_DARK, L, 'ext')
    # service-wing roof slab = terrace deck
    bx(-0.125, 8.625, -3.125, 0.0, 3.75, 4.0, STUCCO, L, 'solid')
    floor_area(0, 8.5, -3, 0, 4.0, DECK, L, T_WOOD, tile=2.2)

    # ---- floors
    floor_area(0, 8.5, 7.5, 10.6, 4.0, FLOOR_WOOD, L, T_WOOD, tile=2.2)    # caída
    floor_area(0, 5, 3.8, 7.5, 4.0, FLOOR_WOOD, L, T_WOOD)                 # media
    floor_area(0, 2.6, 0, 3.8, 4.0, FLOOR_WOOD, L, T_WOOD)                 # nook
    floor_area(5, 6.1, 0, 7.5, 4.0, FLOOR_WOOD, L, T_WOOD)                 # hall
    floor_area(8.5, 14, 4.6, 10.6, 4.0, FLOOR_WOOD, L, T_WOOD)             # master bedroom
    floor_area(8.5, 11, 0, 4.6, 4.0, FLOOR_WOOD, L, T_WOOD)                # walk-in closet
    floor_area(6.1, 8.5, 0, 3.8, 4.0, FLOOR_TILE, L)                       # linen
    floor_area(2.6, 5, 0, 3.8, 4.0, FLOOR_BATH, L)                         # common T&B
    floor_area(11, 14, 0, 4.6, 4.0, FLOOR_BATH, L)                         # master T&B

    # ---- exterior timber walls (0.20 m)
    Z0, Z1, T = 4.0, 6.9, 0.2
    wall('x', 10.6, -0.1, 14.1, Z0, Z1, T, WOOD_SIDING, L, 'ext', texture=T_WOOD,
         openings=[(0.3, 8.1, 4.85, 6.45), (8.65, 9.45, 4.85, 6.45),
                   (9.55, 12.95, 4.0, 6.45), (13.05, 13.85, 4.85, 6.45)])
    wall('x', 0.0, -0.1, 14.1, Z0, Z1, T, WOOD_SIDING, L, 'ext', texture=T_WOOD,
         openings=[(0.2, 2.4, 4.0, 6.3), (3.2, 4.4, 5.65, 6.45), (5.05, 6.05, 4.0, 6.3),
                   (6.8, 7.8, 5.65, 6.45), (9.1, 10.4, 4.85, 6.45), (11.6, 13.4, 5.65, 6.45)])
    wall('y', 0.0, 0.1, 10.5, Z0, Z1, T, WOOD_SIDING, L, 'ext', texture=T_WOOD,
         openings=[(0.7, 2.7, 4.85, 6.45), (4.3, 7.3, 4.85, 6.45), (8.1, 10.1, 4.85, 6.45)])
    wall('y', 14.0, 0.1, 10.5, Z0, Z1, T, WOOD_SIDING, L, 'ext', texture=T_WOOD,
         openings=[(1.2, 3.2, 5.65, 6.45), (5.1, 10.1, 4.85, 6.45)])
    # corner posts (haligi) and top band
    for (cx, cy) in ((0, 0), (14, 0), (0, 10.6), (14, 10.6), (8.5, 10.6)):
        bx(cx - 0.14, cx + 0.14, cy - 0.14, cy + 0.14, 3.6, 6.9, WOOD_DARK, L, 'ext')
    bx(-0.12, 14.12, 10.7, 10.75, 6.5, 6.9, WOOD_DARK, L, 'ext')
    bx(-0.12, 14.12, -0.15, -0.1, 6.5, 6.9, WOOD_DARK, L, 'ext')
    bx(-0.15, -0.1, -0.1, 10.7, 6.5, 6.9, WOOD_DARK, L, 'ext')
    bx(14.1, 14.15, -0.1, 10.7, 6.5, 6.9, WOOD_DARK, L, 'ext')

    # ---- windows and doors
    capiz_window('x', 10.6, +1, 0.3, 8.1, 4.85, 6.45, n=8, open_idx=(2, 5))     # caída front
    capiz_window('x', 10.6, +1, 8.65, 9.45, 4.85, 6.45, n=1)
    capiz_window('x', 10.6, +1, 13.05, 13.85, 4.85, 6.45, n=1)
    glass_door('x', 10.6, 9.55, 12.95, 4.0, 6.45, 4, L)                        # balcony doors
    capiz_window('x', 0.0, -1, 3.2, 4.4, 5.65, 6.45, n=1, ventanilla=False)    # common T&B
    capiz_window('x', 0.0, -1, 6.8, 7.8, 5.65, 6.45, n=1, ventanilla=False)    # linen
    capiz_window('x', 0.0, -1, 9.1, 10.4, 4.85, 6.45, n=1)                     # walk-in closet
    capiz_window('x', 0.0, -1, 11.6, 13.4, 5.65, 6.45, n=2, ventanilla=False)  # master T&B
    capiz_window('y', 0.0, -1, 0.7, 2.7, 4.85, 6.45, n=2)                      # nook
    capiz_window('y', 0.0, -1, 4.3, 7.3, 4.85, 6.45, n=3, open_idx=(1,))       # media
    capiz_window('y', 0.0, -1, 8.1, 10.1, 4.85, 6.45, n=2)                     # caída side
    capiz_window('y', 14.0, +1, 1.2, 3.2, 5.65, 6.45, n=2, ventanilla=False)   # master T&B
    capiz_window('y', 14.0, +1, 5.1, 10.1, 4.85, 6.45, n=5, open_idx=(2,))     # master bedroom
    # terrace doors, opened outwards onto the deck
    glass_door('y', 5.08, -1.0, 0.0, 4.0, 6.3, 1, L)                           # hall door
    glass_door('y', 0.23, -1.1, 0.0, 4.0, 6.3, 1, L)                           # nook French doors
    glass_door('y', 2.37, -1.1, 0.0, 4.0, 6.3, 1, L)

    # ---- interior partitions (0.10 m)
    ZI, TI = 6.9, 0.1
    wall('y', 5.0, 0.1, 7.5, Z0, ZI, TI, INT_WALL, L, 'int',
         openings=[(2.7, 3.5, 4.0, 6.1), (5.0, 5.9, 4.0, 6.1)])
    wall('x', 3.8, 0.1, 5.0, Z0, ZI, TI, INT_WALL, L, 'int', openings=[(0.3, 2.3, 4.0, 6.3)])
    wall('y', 2.6, 0.1, 3.8, Z0, ZI, TI, INT_WALL, L, 'int')
    wall('x', 7.5, 0.1, 5.0, Z0, ZI, TI, INT_WALL, L, 'int')
    wall('y', 6.1, 0.1, 3.8, Z0, ZI, TI, INT_WALL, L, 'int', openings=[(1.4, 2.2, 4.0, 6.1)])
    wall('x', 3.8, 6.1, 8.5, Z0, ZI, TI, INT_WALL, L, 'int')
    wall('y', 8.5, 0.1, 10.5, Z0, ZI, TI, INT_WALL, L, 'int', openings=[(8.4, 9.3, 4.0, 6.1)])
    wall('x', 4.6, 8.5, 13.9, Z0, ZI, TI, INT_WALL, L, 'int',
         openings=[(9.2, 10.0, 4.0, 6.1), (13.1, 13.9, 4.0, 6.1)])
    wall('y', 11.0, 0.1, 4.6, Z0, ZI, TI, INT_WALL, L, 'int')
    door_leaf(4.2, 5.0, 3.45, 3.5, 4.0, 6.1, L)          # common T&B
    door_leaf(4.1, 5.0, 5.85, 5.9, 4.0, 6.1, L)          # media room
    door_leaf(6.1, 6.9, 1.4, 1.45, 4.0, 6.1, L)          # linen
    door_leaf(8.5, 9.4, 8.4, 8.45, 4.0, 6.1, L)          # master bedroom
    door_leaf(13.85, 13.9, 3.8, 4.6, 4.0, 6.1, L)        # master T&B
    # railings around the stair opening
    railing(6.1, 3.8, 6.1, 7.5, 4.0, 0.95, L, kind='furn', spacing=0.13)
    railing(7.25, 7.5, 8.5, 7.5, 4.0, 0.95, L, kind='furn', spacing=0.13)

    # ---- balcony
    bx(9.2, 13.3, 10.7, 11.8, 3.75, 4.0, WOOD_DARK, L, 'solid')
    floor_area(9.2, 13.3, 10.7, 11.8, 4.0, DECK, L)
    railing(9.2, 11.8, 13.3, 11.8, 4.0, 1.05, L)
    railing(9.2, 10.75, 9.2, 11.8, 4.0, 1.05, L)
    railing(13.3, 10.75, 13.3, 11.8, 4.0, 1.05, L)
    for bxp in (9.5, 13.0):
        beam(W(bxp, 10.7, 3.15), W(bxp, 11.65, 3.76), 0.14, 0.14, WOOD_DARK, L, 'ext')
    # ---- terrace railing
    railing(0.0, -3.0, 8.5, -3.0, 4.0, 1.05, L, spacing=0.2)
    railing(0.0, -3.0, 0.0, 0.0, 4.0, 1.05, L, spacing=0.2)
    railing(8.5, -3.0, 8.5, 0.0, 4.0, 1.05, L, spacing=0.2)

    build_second_furniture()


def build_second_furniture():
    L, z = 'sf', F2
    # ---------------- Caída (upper lounge)
    rug(0.6, 3.9, 7.9, 10.35, z, L, rgb(190, 150, 120))
    sofa(0.8, 3.6, 9.5, 10.35, z, 'S', L)
    table(1.4, 3.0, 8.35, 9.1, z, 0.42, WOOD_DARK, L)
    sofa(0.45, 1.25, 7.7, 8.5, z, 'N', L, col=ACCENT)
    sofa(3.15, 3.95, 7.7, 8.5, z, 'N', L, col=ACCENT)
    bx(4.6, 7.9, 9.9, 10.4, z, z + 0.42, WOOD_DARK, L, 'furn')               # window bench
    bx(4.65, 7.85, 9.95, 10.35, z + 0.42, z + 0.5, SOFA, L, 'furn')
    vcyl(4.6, 8.7, z, 0.7, 0.06, WOOD_DARK, L)                                # tea table
    vcyl(4.6, 8.7, z + 0.7, 0.04, 0.45, WOOD_DARK, L)
    chair(4.0, 8.7, z, 'W', L)
    chair(5.2, 8.7, z, 'E', L)
    bx(1.55, 2.95, 7.57, 7.95, z, z + 1.9, WOOD_DARK, L, 'furn')             # aparador cabinet
    bx(1.62, 2.88, 7.94, 7.96, z + 0.9, z + 1.8, GLASS, L, 'furn')
    plant(8.1, 10.15, z, 0.34, level=L)
    pendant(3.5, 9.0, 6.25, 6.9, L, r=0.3)                                    # capiz chandelier
    # ---------------- Media room
    rug(0.9, 3.4, 4.3, 7.1, z, L, rgb(170, 160, 150))
    bx(0.15, 0.55, 4.6, 6.8, z, z + 0.5, WOOD_DARK, L, 'furn')
    bx(0.3, 0.36, 4.9, 6.5, z + 0.75, z + 1.65, BLACK, L, 'furn')
    bx(0.2, 0.5, 4.2, 4.5, z, z + 1.0, BLACK, L, 'furn')
    bx(0.2, 0.5, 6.9, 7.2, z, z + 1.0, BLACK, L, 'furn')
    sofa(2.6, 3.5, 4.4, 7.0, z, 'E', L, col=ACCENT2, pillow=SOFA)
    table(1.4, 2.2, 5.1, 6.3, z, 0.4, WOOD_MID, L)
    floor_lamp(4.6, 7.2, z, L)
    # ---------------- Altar & reading nook
    cabinet(2.15, 2.55, 0.6, 2.2, z, 0.9, WOOD_DARK, L)
    vcyl(2.35, 1.4, z + 0.9, 0.35, 0.07, WHITE, L)                            # santo
    ball(2.35, 1.4, z + 1.32, 0.07, WHITE, L)
    for cy in (0.85, 1.95):
        vcyl(2.35, cy, z + 0.9, 0.18, 0.025, WHITE, L)
        lamp_glow(2.35, cy, z + 1.12, 0.03, L)
    bx(2.53, 2.55, 1.37, 1.43, z + 1.4, z + 2.0, WOOD_DARK, L, 'furn')       # cross
    bx(2.53, 2.55, 1.2, 1.6, z + 1.75, z + 1.81, WOOD_DARK, L, 'furn')
    ball(2.35, 1.0, z + 1.0, 0.08, LEAF_RED, L)
    sofa(0.35, 1.15, 2.05, 2.85, z, 'W', L, col=ACCENT)
    bookshelf(0.12, 0.42, 0.3, 1.95, z, 0.8, L, along='y', shelves=2)
    floor_lamp(0.4, 3.35, z, L, h=1.4)
    # ---------------- Common T&B
    toilet(3.03, 0.65, z, 'N', L)
    cabinet(3.75, 4.85, 0.15, 0.6, z, 0.82, WOOD_MID, L)
    basin(3.85, 4.75, 0.2, 0.55, z + 0.82, L)
    bx(3.9, 4.7, 0.11, 0.13, z + 1.0, z + 1.55, MIRROR, L, 'furn', shiny=0.9)
    bx(2.75, 4.15, 2.3, 3.65, z, z + 0.05, WHITE, L, 'furn')
    bx(2.75, 4.15, 2.29, 2.31, z + 0.05, z + 2.0, GLASS, L, 'glass', base=0.3)
    bx(4.14, 4.16, 2.3, 3.65, z + 0.05, z + 2.0, GLASS, L, 'glass', base=0.3)
    vcyl(2.85, 3.2, z + 2.05, 0.03, 0.1, METAL, L)
    pendant(3.8, 1.6, 6.4, 6.9, L, r=0.1)
    # ---------------- Linen & storage
    bookshelf(6.25, 8.35, 0.15, 0.6, z, 2.2, L, along='x', palette=TOWEL_COLOURS)
    bookshelf(7.9, 8.35, 0.65, 3.65, z, 2.2, L, along='y', palette=TOWEL_COLOURS)
    # ---------------- Master bedroom
    rug(9.9, 13.3, 4.7, 7.7, z, L, rgb(205, 180, 150))
    bx(10.5, 12.7, 4.68, 4.78, z, z + 1.3, WOOD_DARK, L, 'furn')             # headboard
    bx(10.6, 12.6, 4.75, 6.95, z, z + 0.35, WOOD_DARK, L, 'furn')            # bed frame
    bx(10.65, 12.55, 4.82, 6.9, z + 0.35, z + 0.6, BEDDING, L, 'furn')       # mattress
    bx(10.63, 12.57, 5.6, 6.93, z + 0.55, z + 0.64, ACCENT, L, 'furn')       # throw
    bx(10.75, 11.55, 4.88, 5.25, z + 0.6, z + 0.76, WHITE, L, 'furn')
    bx(11.65, 12.45, 4.88, 5.25, z + 0.6, z + 0.76, WHITE, L, 'furn')
    for nx in (10.05, 12.65):
        cabinet(nx, nx + 0.45, 4.75, 5.2, z, 0.55, WOOD_DARK, L)
        vcyl(nx + 0.22, 4.97, z + 0.55, 0.3, 0.05, BRASS, L)
        lamp_glow(nx + 0.22, 4.97, z + 0.93, 0.11, L)
    bx(10.8, 12.4, 7.05, 7.4, z, z + 0.45, WOOD_DARK, L, 'furn')             # bench
    table(8.65, 9.1, 6.0, 7.6, z, 0.75, WOOD_DARK, L)                         # vanity desk
    bx(8.56, 8.58, 6.3, 7.3, z + 0.95, z + 1.85, MIRROR, L, 'furn', shiny=0.9)
    vcyl(9.4, 6.8, z, 0.45, 0.2, SOFA, L)
    sofa(12.95, 13.75, 8.1, 8.9, z, 'E', L, col=ACCENT2, pillow=SOFA)
    sofa(12.95, 13.75, 9.25, 10.05, z, 'E', L, col=ACCENT2, pillow=SOFA)
    vcyl(12.6, 9.1, z, 0.5, 0.2, WOOD_DARK, L)
    plant(9.0, 10.2, z, 0.36, level=L)
    vcyl(11.25, 7.6, 6.45, 0.45, 0.02, BLACK, L)                              # ceiling fan
    vcyl(11.25, 7.6, 6.38, 0.1, 0.12, WOOD_DARK, L)
    bx(10.5, 12.0, 7.53, 7.67, 6.4, 6.42, WOOD_DARK, L, 'furn')
    bx(11.18, 11.32, 6.85, 8.35, 6.4, 6.42, WOOD_DARK, L, 'furn')
    lamp_glow(11.25, 7.6, 6.33, 0.1, L)
    # ---------------- Walk-in closet
    for (x0, x1) in ((8.65, 9.2), (10.3, 10.85)):
        cx = (x0 + x1) / 2
        bx(x0, x1, 0.15, 4.45, z, z + 0.35, WOOD_MID, L, 'furn')
        bx(x0, x1, 0.15, 4.45, z + 1.92, z + 1.95, WOOD_MID, L, 'furn')
        bx(x0, x1, 0.15, 4.45, z + 2.3, z + 2.33, WOOD_MID, L, 'furn')
        rod(W(cx, 0.15, z + 1.78), W(cx, 4.45, z + 1.78), 0.015, METAL, L, 'furn')
        yy, i = 0.25, 0
        while yy < 4.3:
            bx(cx - 0.21, cx + 0.21, yy, yy + 0.07, z + 0.95, z + 1.74,
               CLOTH_COLOURS[i % len(CLOTH_COLOURS)], L, 'furn')
            yy += 0.12 if i % 9 != 8 else 0.3
            i += 1
        for k in range(6):
            bx(x0 + 0.05, x1 - 0.05, 0.3 + k * 0.6, 0.55 + k * 0.6, z + 1.95, z + 2.2,
               [WHITE, CLAY, ACCENT2][k % 3], L, 'furn')
    vcyl(9.75, 2.9, z, 0.42, 0.28, ACCENT, L)                                 # ottoman
    pendant(9.75, 2.2, 6.4, 6.9, L, r=0.12)
    # ---------------- Master T&B
    bx(11.6, 13.35, 0.15, 0.95, z, z + 0.55, WHITE, L, 'furn')                # tub
    bx(11.7, 13.25, 0.25, 0.85, z + 0.5, z + 0.56, WATER, L, 'furn')
    cabinet(13.4, 13.85, 1.3, 3.1, z, 0.85, WOOD_DARK, L)
    basin(13.45, 13.8, 1.55, 1.95, z + 0.85, L)
    basin(13.45, 13.8, 2.45, 2.85, z + 0.85, L)
    bx(13.87, 13.89, 1.4, 3.0, z + 1.05, z + 1.85, MIRROR, L, 'furn', shiny=0.9)
    bx(11.15, 12.35, 1.15, 2.45, z, z + 0.05, WHITE, L, 'furn')
    bx(11.15, 12.35, 2.44, 2.46, z + 0.05, z + 2.0, GLASS, L, 'glass', base=0.3)
    bx(12.34, 12.36, 1.15, 2.45, z + 0.05, z + 2.0, GLASS, L, 'glass', base=0.3)
    vcyl(11.25, 1.8, z + 2.05, 0.03, 0.12, METAL, L)
    toilet(11.62, 3.18, z, 'W', L)
    plant(13.55, 4.2, z, 0.28, level=L)
    pendant(12.5, 2.3, 6.4, 6.9, L, r=0.12)
    # ---------------- Roof-deck terrace
    for (p0, p1) in ((0.3, 3.3), (5.2, 8.2)):
        bx(p0, p1, -2.8, -2.4, z, z + 0.45, STONE_TRIM, L, 'furn')
        k = p0 + 0.3
        while k < p1 - 0.1:
            ball(k, -2.6, z + 0.62, 0.26, LEAF if int(k * 4) % 2 else LEAF2, L)
            k += 0.45
    for lx in (3.1, 4.0):                                                     # sun loungers
        bx(lx, lx + 0.7, -2.2, -0.6, z + 0.12, z + 0.3, WOOD_LIGHT, L, 'furn')
        bx(lx + 0.05, lx + 0.65, -1.7, -0.65, z + 0.3, z + 0.36, WHITE, L, 'furn')
        beam(W(lx + 0.35, -1.72, z + 0.3), W(lx + 0.35, -2.15, z + 0.78), 0.62, 0.08, WHITE, L, 'furn')
    vcyl(7.0, -1.4, z, 0.72, 0.04, STEEL, L)
    vcyl(7.0, -1.4, z + 0.72, 0.03, 0.45, WHITE, L)
    chair(7.0, -2.1, z, 'N', L, col=STEEL, seat=WHITE)
    chair(7.0, -0.7, z, 'S', L, col=STEEL, seat=WHITE)
    for k in range(9):                                                        # string lights
        lamp_glow(0.4 + k * 0.95, -3.0, 5.12, 0.045, L)
    # ---------------- Balcony
    chair(10.0, 11.25, z, 'W', L, col=WOOD_DARK, seat=SOFA)
    chair(12.5, 11.25, z, 'E', L, col=WOOD_DARK, seat=SOFA)
    vcyl(11.25, 11.25, z, 0.6, 0.18, WOOD_DARK, L)
    for hx in (9.35, 13.15):
        ball(hx, 11.65, z + 1.12, 0.26, LEAF2, L)
        ball(hx, 11.72, z + 0.85, 0.16, LEAF, L)


# ==========================================================================
# BUILD: roof (clay barrel tiles on a hip roof)
# ==========================================================================
def build_roof():
    R = 'roof'
    EAVE, P, DM = 6.9, 0.38, 6.4

    def rp(x, y, d):
        return W(x, y, EAVE + P * d)

    A, B, C, D = (-0.9, -0.9), (14.9, -0.9), (14.9, 11.9), (-0.9, 11.9)
    R1, R2 = (5.5, 5.5), (8.5, 5.5)

    def plane(pts, col):
        n = norm(cross(pts[1] - pts[0], pts[2] - pts[0]))
        if n.y < 0:
            n = -n
        vs = [vertex(pos=p, color=col, normal=n, opacity=1) for p in pts]
        for v in vs:
            reg(v, R, 'roof', 1.0, mode='vertex')
        obj = quad(vs=vs) if len(vs) == 4 else triangle(vs=vs)
        reg(obj, R, 'roof', 1.0, mode='visonly')

    plane([rp(*D, 0), rp(*C, 0), rp(*R2, DM), rp(*R1, DM)], ROOF_A)     # front
    plane([rp(*A, 0), rp(*R1, DM), rp(*R2, DM), rp(*B, 0)], ROOF_B)     # back
    plane([rp(*A, 0), rp(*D, 0), rp(*R1, DM)], ROOF_C)                  # left
    plane([rp(*B, 0), rp(*R2, DM), rp(*C, 0)], ROOF_D)                  # right

    # barrel tiles running down the slope
    x = -0.75
    while x < 14.8:
        dmax = min(x + 0.9, 14.9 - x, DM)
        if dmax > 0.12:
            for (ye, sgn) in ((11.9, -1), (-0.9, 1)):
                p0 = W(x, ye, EAVE + 0.05)
                rod(p0, p0 + vector(0, P * dmax, sgn * dmax), 0.055, ROOF_LIGHT, R, 'roof')
        x += 0.3
    y = -0.75
    while y < 11.8:
        dmax = min(y + 0.9, 11.9 - y, DM)
        if dmax > 0.12:
            for (xe, sgn) in ((-0.9, 1), (14.9, -1)):
                p0 = W(xe, y, EAVE + 0.05)
                rod(p0, p0 + vector(sgn * dmax, P * dmax, 0), 0.055, ROOF_LIGHT, R, 'roof')
        y += 0.3
    # tile courses
    d = 0.4
    while d < 6.2:
        zc = EAVE + P * d + 0.07
        rod(W(-0.9 + d, 11.9 - d, zc), W(14.9 - d, 11.9 - d, zc), 0.025, ROOF_DARK, R, 'roof')
        rod(W(-0.9 + d, -0.9 + d, zc), W(14.9 - d, -0.9 + d, zc), 0.025, ROOF_DARK, R, 'roof')
        rod(W(-0.9 + d, -0.9 + d, zc), W(-0.9 + d, 11.9 - d, zc), 0.025, ROOF_DARK, R, 'roof')
        rod(W(14.9 - d, -0.9 + d, zc), W(14.9 - d, 11.9 - d, zc), 0.025, ROOF_DARK, R, 'roof')
        d += 0.4
    # hip and ridge caps
    for (p, q) in ((A, R1), (D, R1), (B, R2), (C, R2)):
        rod(rp(*p, 0) + vector(0, 0.06, 0), rp(*q, DM) + vector(0, 0.06, 0), 0.1, ROOF_DARK, R, 'roof')
    rod(rp(*R1, DM) + vector(0, 0.07, 0), rp(*R2, DM) + vector(0, 0.07, 0), 0.12, ROOF_DARK, R, 'roof')
    # fascia boards and soffit
    bx(-0.95, 14.95, 11.85, 11.95, 6.7, 6.95, WOOD_DARK, R, 'roof')
    bx(-0.95, 14.95, -0.95, -0.85, 6.7, 6.95, WOOD_DARK, R, 'roof')
    bx(-0.95, -0.85, -0.95, 11.95, 6.7, 6.95, WOOD_DARK, R, 'roof')
    bx(14.85, 14.95, -0.95, 11.95, 6.7, 6.95, WOOD_DARK, R, 'roof')
    bx(-0.9, 14.9, 10.75, 11.9, 6.84, 6.88, SOFFIT, R, 'roof')
    bx(-0.9, 14.9, -0.9, -0.15, 6.84, 6.88, SOFFIT, R, 'roof')
    bx(-0.9, -0.15, -0.15, 10.75, 6.84, 6.88, SOFFIT, R, 'roof')
    bx(14.15, 14.9, -0.15, 10.75, 6.84, 6.88, SOFFIT, R, 'roof')
    for lx in range(1, 14, 2):                                         # soffit downlights
        lamp_glow(lx, 11.2, 6.82, 0.05, R, kind='roof')


# ==========================================================================
# Labels
# ==========================================================================
def build_labels():
    for r in ROOMS:
        x0, x1, y0, y1 = r['box']
        lab = label(pos=W((x0 + x1) / 2, (y0 + y1) / 2, r['z'] + 1.25), text=r['name'],
                    height=12, box=False, line=False, border=3,
                    color=rgb(40, 32, 26), background=rgb(255, 250, 240), opacity=0.75,
                    visible=False)
        LABELS.append((lab, r['level']))


def finalize():
    """Merge every bucket of small parts into one compound object."""
    for (level, kind), objs in list(BUCKETS.items()):
        if not objs:
            continue
        try:
            c = compound(objs)
            reg(c, level, kind)
        except Exception:
            for o in objs:              # fall back to individual objects
                reg(o, level, kind)
    BUCKETS.clear()


# ==========================================================================
# Fading, floors, camera
# ==========================================================================
def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def smooth(e0, e1, x):
    t = clamp((x - e0) / (e1 - e0))
    return t * t * (3 - 2 * t)


def ease(s):
    s = clamp(s)
    return s * s * s * (s * (s * 6 - 15) + 10)       # smootherstep


def kind_factor(kind, f):
    """How much each kind of object stays visible for see-through level f (1 = solid)."""
    if kind == 'roof':
        return smooth(0.45, 1.0, f)
    if kind == 'ext':
        return 0.16 + 0.84 * smooth(0.0, 0.85, f)
    if kind == 'glass':
        return 0.35 + 0.65 * f
    if kind == 'int':
        return 0.6 + 0.4 * f
    return 1.0


FLOOR_LEVELS = {
    'all': {'gf': 1.0, 'sf': 1.0, 'roof': 1.0, 'site': 1.0},
    'gf':  {'gf': 1.0, 'sf': 0.0, 'roof': 0.0, 'site': 1.0},
    'sf':  {'gf': 1.0, 'sf': 1.0, 'roof': 0.0, 'site': 1.0},
}
LEV = dict(FLOOR_LEVELS['all'], night=0.0, day=1.0)      # current (animated) visibility; 'night' = 0 day .. 1 night
LEV_T = dict(FLOOR_LEVELS['all'], night=0.0, day=1.0)    # targets
STATE = dict(floor='all', auto=True, manual=1.0, labels=True,
             fade=1.0, fade_applied=None, lev_applied=None, last_apply=0.0)


def apply_all(force=False):
    f = STATE['fade']
    for e in REG:
        obj, level, kind, base, mode = e[0], e[1], e[2], e[3], e[4]
        if isinstance(level, tuple):              # e.g. ('gf', 'night'): on the ground floor, at night only
            lv = 1.0
            for lvl in level:
                lv *= LEV.get(lvl, 1.0)
        else:
            lv = LEV.get(level, 1.0)
        if mode == 'window' and base < 0.85:          # lit windows look solid at night
            base = base + (0.85 - base) * LEV['night']
        op = base * kind_factor(kind, f) * lv
        if op > 0.985:
            op = 1.0
        vis = lv > 0.01 and op > 0.012
        if mode != 'vertex' and (force or vis != e[6]):
            obj.visible = vis
            e[6] = vis
        if mode != 'visonly' and (vis or mode == 'vertex'):
            if force or e[5] is None or abs(op - e[5]) > 0.008:
                obj.opacity = op
                e[5] = op
    for lab, level in LABELS:
        show = (STATE['labels'] and STATE['floor'] == level and LEV.get(level, 0) > 0.6)
        if lab.visible != show:
            lab.visible = show
    STATE['fade_applied'] = f
    STATE['lev_applied'] = dict(LEV)


C0 = vector(0, 3.5, 0)
R_ORB, H_ORB, A0 = 26.0, 8.0, 0.62


def orbit_eye(a):
    return C0 + vector(R_ORB * math.sin(a), H_ORB, R_ORB * math.cos(a))


FLOOR_VIEWS = {
    'all': (orbit_eye(A0), C0),
    'gf': (W(19.5, 21.0, 15.0), W(7.0, 4.0, 0.5)),
    'sf': (W(19.5, 21.0, 18.5), W(7.0, 4.0, 4.0)),
}

CAM = {'tw': None}


def view_now():
    fwd = norm(scene.forward)
    dist = scene.range / math.tan(scene.fov / 2)
    tgt = vector(scene.center.x, scene.center.y, scene.center.z)
    return tgt - fwd * dist, tgt


def set_view(eye, tgt):
    d = tgt - eye
    L = mag(d)
    if L < 1e-4:
        return
    scene.center = tgt
    scene.forward = d / L
    scene.range = L * math.tan(scene.fov / 2)


def fly(eye, tgt, dur=3.0):
    e0, t0 = view_now()
    CAM['tw'] = dict(kind='fly', e0=e0, e1=eye, t0=t0, t1=tgt, start=time.perf_counter(),
                     dur=max(0.05, dur), lift=min(3.0, 0.15 * mag(eye - e0)))


def orbit(center, r, h, a0, a1, dur):
    CAM['tw'] = dict(kind='orbit', c=center, r=r, h=h, a0=a0, a1=a1,
                     start=time.perf_counter(), dur=dur)


def update_camera(now):
    tw = CAM['tw']
    if not tw:
        return
    s = clamp((now - tw['start']) / tw['dur'])
    k = ease(s)
    if tw['kind'] == 'fly':
        eye = tw['e0'] + (tw['e1'] - tw['e0']) * k + vector(0, tw['lift'] * math.sin(math.pi * k), 0)
        tgt = tw['t0'] + (tw['t1'] - tw['t0']) * k
    else:
        a = tw['a0'] + (tw['a1'] - tw['a0']) * k
        eye = tw['c'] + vector(tw['r'] * math.sin(a), tw['h'], tw['r'] * math.cos(a))
        tgt = tw['c']
    set_view(eye, tgt)
    if s >= 1.0:
        CAM['tw'] = None


def eye_inside_house(eye):
    return (-7.7 < eye.x < 7.7) and (-8.5 < eye.z < 6.8) and (0.0 < eye.y < 9.5)


def target_fade():
    if not STATE['auto']:
        f = STATE['manual']
    else:
        eye, tgt = view_now()
        D = mag(eye - tgt)
        f = 0.0 if eye_inside_house(eye) else smooth(10.0, 24.0, D)
    if STATE['floor'] != 'all':
        f = min(f, 0.5)            # cut-away floors are always partly see-through
    return f


def update_fade(now, dt):
    ft = target_fade()
    STATE['fade'] += (ft - STATE['fade']) * clamp(dt * 4.0)
    if abs(ft - STATE['fade']) < 0.004:
        STATE['fade'] = ft
    for k in LEV:
        LEV[k] += (LEV_T[k] - LEV[k]) * clamp(dt * 3.2)
        if abs(LEV_T[k] - LEV[k]) < 0.01:
            LEV[k] = LEV_T[k]
    changed = (STATE['fade_applied'] is None or abs(STATE['fade'] - STATE['fade_applied']) > 0.004
               or any(abs(LEV[k] - STATE['lev_applied'][k]) > 0.004 for k in LEV))
    settled = (STATE['fade'] == ft and all(LEV[k] == LEV_T[k] for k in LEV))
    if changed and (now - STATE['last_apply'] > 0.05 or settled):
        apply_all()
        STATE['last_apply'] = now


# --------------------------------------------------------------------------
# Floor switching, room jumps, tour
# --------------------------------------------------------------------------
FLOOR_NAMES = {'all': 'Whole house', 'gf': 'Ground floor', 'sf': 'Second floor'}
BTN = {}


def set_floor(mode, fly_cam=True):
    STATE['floor'] = mode
    LEV_T.update(FLOOR_LEVELS[mode])
    for m, b in BTN.items():
        try:
            b.background = rgb(143, 65, 41) if m == mode else rgb(255, 252, 246)
            b.color = color.white if m == mode else color.black
        except Exception:
            pass
    if fly_cam:
        fly(*FLOOR_VIEWS[mode], dur=2.6)
    apply_all()


def room_view(r):
    x0, x1, y0, y1 = r['box']
    z0 = r['z']
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    span = max(x1 - x0, y1 - y0)
    # always look in from the front-right and from above, like a dollhouse
    dx, dy = 0.42, 0.91
    h = 1.6 + 0.8 * span
    eye = W(cx + dx * h, cy + dy * h, z0 + 3.4 + 0.9 * span)
    tgt = W(cx, cy, z0 + 0.4)
    return eye, tgt


def build_tour():
    T = [
        dict(floor='all', night=False, fly=(orbit_eye(A0), C0), dur=3.0, hold=0.8,
             cap='Welcome: a modern Bahay na Bato, with a stone (bato) ground floor and a timber (bahay) upper floor.'),
        dict(orbit=(C0, R_ORB, H_ORB, A0, A0 + 2 * math.pi), dur=28.0, hold=0.2,
             cap='Exterior walk-around: clay-tile hip roof, capiz windows over ventanillas, volada overhang on corbels.'),
        dict(fly=(W(7.0, 23.0, 1.7), W(7.0, 10.0, 3.4)), dur=4.5, hold=2.5,
             cap='Street view: arched narra door, stone planters and steel-grilled windows.'),
        dict(fly=(W(16.5, 16.5, 5.2), W(11.25, 11.0, 4.9)), dur=3.5, hold=2.0,
             cap='Master-suite balcony with folding glass doors.'),
        dict(fly=(W(-11.0, -15.0, 11.0), W(5.0, -1.0, 3.0)), dur=5.0, hold=2.5,
             cap='Rear: roof-deck terrace over the dirty kitchen and laundry; pergola patio off the dining room.'),
        dict(fly=(W(21.0, -18.5, 9.0), W(11.5, -7.0, 0.3)), dur=4.0, hold=3.0,
             cap='Backyard: mini pool with sun deck, loungers and umbrella.'),
        dict(fly=(W(-9.5, -20.5, 7.5), W(2.5, -11.0, 0.8)), dur=4.5, hold=3.5,
             cap='Mini park and garden: bahay kubo, fountain, stepping stones, swing set and flower beds.'),
        dict(floor='gf', fly=FLOOR_VIEWS['gf'], dur=4.0, hold=2.5,
             cap='Ground floor: the public and working rooms.'),
    ]
    for r in ROOMS:
        if r['level'] == 'gf':
            T.append(dict(fly=room_view(r), dur=3.0, hold=2.4, cap='Ground floor · ' + r['name']))
    T += [
        dict(fly=(W(6.0, 9.6, 2.1), W(12.0, 6.8, 1.3)), dur=3.5, hold=3.0,
             cap='Eye level: from the foyer into the sala.'),
        dict(fly=(W(13.2, 0.7, 2.1), W(3.0, 2.2, 1.2)), dur=3.5, hold=3.0,
             cap='Eye level: dining room looking into the kitchen and breakfast bar.'),
        dict(floor='sf', fly=FLOOR_VIEWS['sf'], dur=4.0, hold=2.5,
             cap='Second floor: the private level. The stair lands in the caída.'),
    ]
    for r in ROOMS:
        if r['level'] == 'sf':
            T.append(dict(fly=room_view(r), dur=3.0, hold=2.4, cap='Second floor · ' + r['name']))
    T += [
        dict(fly=(W(9.3, 10.1, 5.7), W(11.8, 5.6, 4.6)), dur=3.5, hold=3.0,
             cap='Eye level: the master bedroom.'),
        dict(fly=(W(7.9, 8.0, 5.6), W(1.5, 9.6, 4.6)), dur=3.5, hold=3.0,
             cap='Eye level: the caída, the traditional upper lounge.'),
        dict(fly=(W(8.1, -2.7, 5.7), W(1.5, -1.0, 4.4)), dur=3.5, hold=2.5,
             cap='Roof-deck terrace.'),
        dict(floor='all', fly=(W(14.5, 25.0, 3.0), W(7.0, 9.0, 3.8)), dur=5.0, hold=1.0,
             cap='Back outside.'),
        dict(night=True, fly=(W(13.0, 23.5, 2.6), W(7.0, 9.0, 3.8)), dur=3.0, hold=4.0,
             cap='Evening: warm light glows through the capiz windows.'),
        dict(fly=(W(-12.0, 31.0, 4.0), W(8.0, 18.0, 2.0)), dur=4.0, hold=4.0,
             cap='Street lights on, cars passing with headlights.'),
        dict(fly=(W(20.0, -19.0, 8.0), W(8.0, -9.0, 0.5)), dur=5.0, hold=3.5,
             cap='The pool and garden lamps glow at night.'),
        dict(fly=(orbit_eye(A0), C0), dur=4.5, hold=0.3, cap='John Reno Dream House at night.'),
        dict(orbit=(C0, R_ORB, H_ORB, A0, A0 + 2 * math.pi), dur=22.0, hold=1.0,
             cap='John Reno Dream House at night.'),
    ]
    return T


TOUR = []
TOUR_STATE = dict(on=False, i=-1, next=0.0)


def set_caption(text):
    try:
        w_cap.text = ("<div style='font-family:Georgia,serif;font-size:17px;color:#6b2f1c;"
                      "min-height:24px;margin-top:6px'>" + text + "</div>")
    except NameError:
        pass


def start_tour():
    if not TOUR:
        return
    TOUR_STATE.update(on=True, i=-1, next=0.0)
    CAM['tw'] = None
    b_tour.text = '■  Stop tour'


def stop_tour():
    TOUR_STATE['on'] = False
    CAM['tw'] = None
    b_tour.text = '▶  Tour'
    set_caption('')


def toggle_tour():
    if TOUR_STATE['on']:
        stop_tour()
    else:
        start_tour()


def update_tour(now):
    if not TOUR_STATE['on'] or CAM['tw'] is not None or now < TOUR_STATE['next']:
        return
    TOUR_STATE['i'] += 1
    i = TOUR_STATE['i']
    if i >= len(TOUR):
        TOUR_STATE['on'] = False
        b_tour.text = '▶  Tour'
        set_caption('')
        return
    st = TOUR[i]
    if 'floor' in st:
        set_floor(st['floor'], fly_cam=False)
    if 'night' in st:
        set_night(st['night'])
    set_caption(st.get('cap', ''))
    if 'fly' in st:
        fly(st['fly'][0], st['fly'][1], dur=st['dur'])
    else:
        orbit(*st['orbit'], dur=st['dur'])
    TOUR_STATE['next'] = now + st['dur'] + st.get('hold', 2.0)


def reset_view():
    if TOUR_STATE['on']:
        stop_tour()
    set_floor('all', fly_cam=False)
    fly(*FLOOR_VIEWS['all'], dur=2.6)


# --------------------------------------------------------------------------
# Day / night
# --------------------------------------------------------------------------
WARM_GLASS = rgb(255, 204, 122)
WARM_CAPIZ = rgb(255, 222, 160)
NIGHT = dict(applied=None, emissive=False)


def lerp(a, b, t):
    return a + (b - a) * t


def set_night(on):
    LEV_T['night'] = 1.0 if on else 0.0
    LEV_T['day'] = 1.0 - LEV_T['night']
    try:
        b_night.text = '☀  Day' if on else '☾  Night'
    except NameError:
        pass


def toggle_night():
    set_night(LEV_T['night'] < 0.5)


def update_night():
    """Blend sky, sun, interior lights and window glow with the night factor."""
    n = LEV['night']
    if NIGHT['applied'] is not None and abs(n - NIGHT['applied']) < 0.004:
        return
    NIGHT['applied'] = n
    scene.background = lerp(SKY_DAY, SKY_NIGHT, n)
    scene.ambient = lerp(color.gray(0.46), vector(0.12, 0.13, 0.2), n)
    SUN.color = lerp(color.gray(0.78), vector(0.16, 0.19, 0.32), n)      # sun -> moonlight
    FILL.color = lerp(color.gray(0.34), vector(0.04, 0.04, 0.07), n)
    for (lt, full) in NIGHT_LIGHTS:
        lt.color = full * n
    for (pn, base_col, is_capiz) in WINDOWS:
        pn.color = lerp(base_col, WARM_CAPIZ if is_capiz else WARM_GLASS, n)
    glow = n > 0.5
    if glow != NIGHT['emissive']:
        NIGHT['emissive'] = glow
        for (pn, _, _) in WINDOWS:
            pn.emissive = glow
        for t in SIGN:
            t.emissive = glow
        for c in CAR_LIGHTS:
            c.emissive = glow
        for (o, _, _) in POOL_GLOW:
            o.emissive = glow
        for b in GLOW_BULBS:
            b.emissive = glow
    for b in GLOW_BULBS:
        b.color = lerp(color.gray(0.82), rgb(255, 226, 150), n)
    for (o, day_col, night_col) in POOL_GLOW:
        o.color = lerp(day_col, night_col, n)


def build_night_lights():
    warm = vector(1.0, 0.74, 0.45) * 0.12
    for p in (W(11.25, 7.5, 2.9), W(5.5, 2.0, 2.9), W(2.5, 8.0, 2.9),      # sala, kitchen, office
              W(3.5, 9.0, 6.3), W(11.25, 7.6, 6.3), W(6.75, 12.0, 3.0)):  # caida, bedroom, porch
        NIGHT_LIGHTS.append((local_light(pos=p, color=color.black), warm))


def on_key(evt):
    k = (evt.key or '').lower()
    if k == 't':
        toggle_tour()
    elif k == '0':
        set_floor('all')
    elif k == '1':
        set_floor('gf')
    elif k == '2':
        set_floor('sf')
    elif k == 'n':
        toggle_night()
    elif k == 'r':
        reset_view()
    elif k == 'l':
        STATE['labels'] = not STATE['labels']
        apply_all()


def on_mousedown(evt):
    if TOUR_STATE['on']:
        stop_tour()


# ==========================================================================
# User interface: a title and one row of essential buttons
# ==========================================================================
scene.title = (
    "<style>"
    "body{background:#f4efe6;margin:0}"
    ".glowscript{text-align:center;padding-bottom:16px}"
    ".glowscript canvas{border-radius:12px;box-shadow:0 8px 28px rgba(60,40,20,.22)}"
    ".glowscript button{font:600 14px system-ui,-apple-system,'Segoe UI',sans-serif;"
    "padding:9px 18px;margin:12px 4px 0;border:1px solid #d3c4ad;border-radius:999px;"
    "background:#fffcf6;color:#3a2a1e;cursor:pointer}"
    ".glowscript button:hover{border-color:#8f4129}"
    "</style>"
    "<div style='font-family:Georgia,serif;font-size:32px;font-weight:600;color:#3a2a1e;"
    "margin:16px 0 2px'>" + HOUSE_NAME + "</div>"
    "<div style='font:600 12px system-ui,sans-serif;color:#8f7a63;letter-spacing:.18em;"
    "text-transform:uppercase;margin-bottom:12px'>Modern Bahay na Bato</div>")
b_tour = button(text='▶  Tour', bind=lambda b: toggle_tour())
scene.append_to_caption('   ')
BTN['all'] = button(text='Whole house', bind=lambda b: set_floor('all'))
BTN['gf'] = button(text='1st floor', bind=lambda b: set_floor('gf'))
BTN['sf'] = button(text='2nd floor', bind=lambda b: set_floor('sf'))
scene.append_to_caption('   ')
b_night = button(text='☾  Night', bind=lambda b: toggle_night())
button(text='Reset', bind=lambda b: reset_view())
scene.append_to_caption('\n')
w_cap = wtext(text='')
set_caption('Building the house…')

scene.bind('keydown', on_key)
scene.bind('mousedown', on_mousedown)

# ==========================================================================
# Build everything
# ==========================================================================
set_view(*FLOOR_VIEWS['all'])
build_site()
build_backyard()
build_street_life()
build_ground_floor()
build_second_floor()
build_roof()
build_people()
build_labels()
build_night_lights()
finalize()
TOUR = build_tour()
set_floor('all', fly_cam=False)
apply_all(force=True)
update_night()
try:
    scene.waitfor('textures')
except Exception:
    pass
set_caption('')


# ==========================================================================
# Main loop
# ==========================================================================
def main_loop(max_frames=None):
    last = time.perf_counter()
    frames = 0
    while True:
        rate(60)
        now = time.perf_counter()
        dt = min(0.1, now - last)
        last = now
        update_camera(now)
        update_tour(now)
        update_fade(now, dt)
        update_night()
        update_movers(dt)
        frames += 1
        if max_frames is not None and frames >= max_frames:
            return


if __name__ == '__main__':
    main_loop()