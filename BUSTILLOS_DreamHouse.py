from vpython import *
from math import sin, cos, tan, pi, radians, ceil, atan2, asin, exp
from random import random, Random

ALL_OBJ = []


def _track(maker, kind):
    def make(*args, **kw):
        o = maker(*args, **kw)
        ALL_OBJ.append((o, kind))
        return o
    return make


_SIMPLE = globals().get("simple_sphere")
_vp_sphere, _vp_ellipsoid = sphere, ellipsoid


def _far(p, size):
    return (abs(p.x) > 45 or abs(p.z + 5) > 45) and size <= 6


def _sphere(**kw):
    lowpoly = kw.pop("lowpoly", False)
    if _SIMPLE is not None and kw.get("opacity", 1) >= 1 and (
            lowpoly or kw.get("radius", 1.0) <= 0.3 or _far(kw["pos"], 2 * kw.get("radius", 1.0))):
        return _SIMPLE(**kw)
    return _vp_sphere(**kw)


def _ellipsoid(**kw):
    lowpoly = kw.pop("lowpoly", False)
    if "size" in kw:
        L, H, W = kw["size"].x, kw["size"].y, kw["size"].z
    else:
        ax = kw.get("axis")
        L = kw.get("length", mag(ax) if ax is not None else 1.0)
        H, W = kw.get("height", 1.0), kw.get("width", 1.0)
    if _SIMPLE is not None and kw.get("opacity", 1) >= 1 and (
            lowpoly or max(L, H, W) <= 0.35 or _far(kw["pos"], max(L, H, W))):
        args = {k: v for (k, v) in kw.items() if k not in ("axis", "length", "height", "width", "size", "up")}
        if kw.get("axis") is not None:
            args["axis"] = norm(kw["axis"])
        args["size"] = vector(L, H, W)
        if kw.get("up") is not None:
            args["up"] = kw["up"]
        return _SIMPLE(**args)
    return _vp_ellipsoid(**kw)


box = _track(box, "box")
cylinder = _track(cylinder, "cylinder")
sphere = _track(_sphere, "sphere")
ellipsoid = _track(_ellipsoid, "ellipsoid")
cone = _track(cone, "cone")
ring = _track(ring, "ring")
triangle = _track(triangle, "triangle")
pyramid = _track(pyramid, "pyramid")
_vp_compound = compound


GROUPS = []


def as_group(fn, *args, **kw):
    start = len(ALL_OBJ)
    fn(*args, **kw)
    GROUPS.append((start, len(ALL_OBJ)))


def compound(parts, **kw):
    used = set(id(p) for p in parts)
    ALL_OBJ[:] = [(o, k) for (o, k) in ALL_OBJ if id(o) not in used]
    c = _vp_compound(parts, **kw)
    ALL_OBJ.append((c, "compound"))
    return c

HOUSE_NAME = "Dream House"
scene.width = 1200
scene.height = 620
scene.background = vector(0.60, 0.80, 0.97)
scene.ambient = color.gray(0.5)
scene.visible = False
scene.autoscale = False
scene.center, scene.forward, scene.range = vector(-6, 3, -3), vector(-0.35, -0.35, -1), 30

INK = vector(0.04, 0.04, 0.04)
GOLD_BTN = vector(0.97, 0.79, 0.27)

STYLE = ("<style>"
         "@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&display=swap');"
         "html{background:#fff;overflow-x:hidden}"
         "body{font-family:'Josefin Sans','Century Gothic','Futura','Segoe UI',sans-serif;background:#fff;"
         "color:#0b0b0b;max-width:" + str(scene.width) + "px;margin:0 auto !important;padding:0 0 40px;"
         "text-align:left}"
         ".dh-head{background:#0b0b0b;color:#fff;box-shadow:0 0 0 100vmax #0b0b0b;clip-path:inset(0 -100vmax);"
         "padding:20px 0;display:flex;align-items:center;justify-content:space-between;text-align:left}"
         ".dh-logo{font-size:28px;letter-spacing:.42em;font-weight:300;white-space:nowrap}"
         ".dh-logo b{display:inline-block;background:#fff;color:#0b0b0b;padding:4px 8px 0;margin-right:10px;"
         "font-weight:600;letter-spacing:0}"
         ".dh-headr{display:flex;align-items:center;gap:22px}"
         ".dh-pill{background:#fff;color:#0b0b0b;border-radius:999px;padding:8px 16px 6px;font-size:13px;"
         "letter-spacing:.1em}"
         ".dh-small{font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#bbb}"
         ".dh-titlerow{display:flex;justify-content:space-between;align-items:flex-end;margin:40px 0 0;"
         "text-align:left}"
         ".dh-loc{font-size:14px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#555}"
         ".dh-h1{font-size:40px;font-weight:400;line-height:1.15;margin:4px 0 0}"
         ".dh-model{font-size:15px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:#777;"
         "padding-bottom:6px}"
         ".dh-rule{height:2px;background:#0b0b0b;margin:16px 0 18px}"
         ".dh-gap{height:0}"
         ".dh-lab{display:inline-block;width:110px;font-size:10.5px;font-weight:600;letter-spacing:.2em;"
         "text-transform:uppercase;color:#888;vertical-align:middle}"
         "button{font-family:inherit !important;font-size:10px !important;font-weight:600;"
         "letter-spacing:.06em !important;text-transform:uppercase;"
         "width:176px;box-sizing:border-box;white-space:nowrap;overflow:hidden;text-align:center;"
         "margin:3px 5px 3px 0;padding:8px 4px 6px !important;line-height:1.2 !important;"
         "border:1px solid #0b0b0b;border-radius:0;"
         "vertical-align:middle;"
         "background:#fff;color:#0b0b0b;cursor:pointer;transition:background .15s,color .15s}"
         "button:hover{background:#0b0b0b !important;color:#fff !important}"
         ".dh-end{height:1px;background:#e3e1da;margin:14px 0 18px}"
         ".dh-chip{display:table;margin-left:auto !important;margin-right:auto !important;font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;"
         "color:#0b0b0b;border:1px solid #0b0b0b;padding:9px 14px 7px;margin:18px 0 0}"
         ".dh-info{background:#faf9f5;border-left:4px solid #f5c542;padding:14px 18px;font-size:15px;color:#333;"
         "line-height:1.55;margin:14px 0 0;text-align:left}"
         ".dh-info b{font-size:15px;letter-spacing:.12em;text-transform:uppercase;color:#0b0b0b}"
         ".dh-keys{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 22px;white-space:normal !important;"
         "font-size:13.5px;color:#555;margin-top:18px;border-top:1px solid #e3e1da;padding-top:16px}"
         ".dh-keys .dh-kt{flex-basis:100%;text-align:center;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:#777}"
         ".dh-k{white-space:nowrap}"
         "kbd{font-family:inherit;background:#fff;border:1px solid #bbb;border-bottom-width:2px;padding:1px 6px 0;"
         "font-size:12px;margin:0 1px}"
         "</style>")

KEY_FIX = ("<img src='data:,' alt='' style='display:none' onerror=\"if(!window.dhKeys){window.dhKeys=1;"
           "window.addEventListener('keydown',function(e){var k=e.key;"
           "if(k=='ArrowUp'||k=='ArrowDown'||k=='ArrowLeft'||k=='ArrowRight'||k==' '){e.preventDefault();}},"
           "{passive:false});}"
           "if(!window.dhLook){window.dhLook=1;(function hook(){try{var c=window.canvas&&canvas.selected;"
           "if(!c||!c.elements||!c.camera){return setTimeout(hook,400);}var eye=null;"
           "c.elements.mousedown(function(ev){if(ev.which==3&&c.userspin&&!c.userzoom){eye=c.camera.pos;}});"
           "c.elements.mousemove(function(ev){if(eye&&c.userspin&&!c.userzoom){var d=c.camera.axis.mag;"
           "c.center=eye.add(c.__axis.norm().multiply(d));}});"
           "$(document).mouseup(function(){eye=null;});}catch(e){setTimeout(hook,1000);}})();}\">")

TOP = scene.title_anchor
LOGO_NAME = "Bustillos"
LOGO = "<b>" + LOGO_NAME[0] + "</b>" + LOGO_NAME[1:].upper()
scene.title = (
    STYLE + KEY_FIX +
    "<div class='dh-head'><span class='dh-logo'>" + LOGO + "</span>"
    "<span class='dh-headr'><span class='dh-small'>Graphics and Visual Computing</span>"
    "<span class='dh-pill'>3D WALK-THROUGH</span></span></div>"
    "<div class='dh-titlerow'><div><div class='dh-loc'>Modern tropical residence</div>"
    "<div class='dh-h1'>" + HOUSE_NAME + "</div></div>"
    "<div class='dh-model'>Interactive 3D model</div></div>"
    "<div class='dh-rule'></div>"
    "<div id='dh-loading' style='padding:60px 0;font-size:18px;letter-spacing:.2em;text-transform:uppercase;"
    "color:#777'>Building the house&hellip; it appears in a few seconds</div>")


F0 = 0.5
F1 = 4.2
F2 = 7.8

WHITE_WALL = vector(0.93, 0.93, 0.90)
CEILING    = vector(0.97, 0.97, 0.96)
PLINTH     = vector(0.78, 0.78, 0.76)
DARK_STONE = vector(0.21, 0.22, 0.23)
ROOF       = vector(0.16, 0.17, 0.19)
FRAME      = vector(0.12, 0.12, 0.13)
WOOD       = vector(0.55, 0.33, 0.17)
LIVE_EDGE  = vector(0.58, 0.32, 0.14)
SOFFIT     = vector(0.60, 0.38, 0.20)
DECK_WOOD  = vector(0.62, 0.42, 0.26)
TILE_FLOOR = vector(0.86, 0.85, 0.81)
WOOD_FLOOR = vector(0.74, 0.54, 0.34)
BATH_TILE  = vector(0.62, 0.62, 0.60)
GLASS      = vector(0.45, 0.60, 0.68)
RAIL_GLASS = vector(0.75, 0.92, 0.97)
STEEL      = vector(0.74, 0.76, 0.78)
MARBLE     = vector(0.95, 0.95, 0.94)
SOFA       = vector(0.58, 0.36, 0.21)
SOFA_DARK  = vector(0.40, 0.25, 0.16)
SOFA_LEGS  = vector(0.20, 0.13, 0.08)
P_CREAM    = vector(0.94, 0.90, 0.81)
P_SAND     = vector(0.82, 0.70, 0.54)
P_CARAMEL  = vector(0.74, 0.50, 0.30)
P_COCOA    = vector(0.36, 0.23, 0.14)
P_RUST     = vector(0.60, 0.33, 0.19)
YELLOW     = vector(0.95, 0.78, 0.15)
GOLD       = vector(0.95, 0.75, 0.25)
CABINET    = vector(0.42, 0.43, 0.45)
MIRROR     = vector(0.80, 0.87, 0.92)
EPOXY      = vector(0.55, 0.57, 0.60)
DECK_TILE  = vector(0.22, 0.17, 0.12)
GRASS      = vector(0.33, 0.60, 0.25)
HEDGE      = vector(0.18, 0.42, 0.17)
LEAF       = vector(0.20, 0.55, 0.20)
TRUNK      = vector(0.50, 0.40, 0.30)
CONCRETE   = vector(0.70, 0.70, 0.68)
STREET     = vector(0.58, 0.58, 0.56)
PAVER_1    = vector(0.66, 0.67, 0.69)
PAVER_2    = vector(0.45, 0.46, 0.49)
GRAVEL     = vector(0.84, 0.82, 0.78)
POOL_TILE  = vector(0.20, 0.62, 0.90)
WATER      = vector(0.10, 0.58, 0.95)
METAL      = vector(0.80, 0.80, 0.83)
LAMP       = vector(1.00, 0.96, 0.85)
EXT        = vector(0.17, 0.18, 0.20)
FENCE_GRAY = vector(0.36, 0.37, 0.38)
GROUT      = vector(0.74, 0.73, 0.70)
PLANK_LINE = vector(0.60, 0.42, 0.26)
SHEER      = vector(0.96, 0.95, 0.92)
TEAL       = vector(0.15, 0.50, 0.55)

SOLIDS = []
GLASS_PANES = []
CLOUDS = []


def add_solid(x1, x2, y1, y2, z1, z2):
    SOLIDS.append((min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2),
                   min(z1, z2), max(z1, z2)))


def block(x1, x2, y1, y2, z1, z2, col, solid=False, **extra):
    if solid:
        add_solid(x1, x2, y1, y2, z1, z2)
    return box(pos=vector((x1 + x2) / 2, (y1 + y2) / 2, (z1 + z2) / 2),
               size=vector(abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)),
               color=col, **extra)


def wall(run, c, a1, a2, y1, y2, openings=(), t=0.2, col=WHITE_WALL, solid=True, skin=None):
    def part(p1, p2, q1, q2, colr, thick, is_solid, **kw):
        if p2 - p1 < 0.005 or q2 - q1 < 0.005:
            return None
        if run == "x":
            return block(p1, p2, q1, q2, c - thick / 2, c + thick / 2, colr, solid=is_solid, **kw)
        return block(c - thick / 2, c + thick / 2, q1, q2, p1, p2, colr, solid=is_solid, **kw)

    a = a1
    for (o1, o2, b1, b2, kind) in sorted(openings):
        part(a, o1, y1, y2, col, t, solid)
        part(o1, o2, y1, b1, col, t, solid)
        part(o1, o2, b2, y2, col, t, solid)
        a = o2
        f, d = 0.07, t + (0.14 if skin else 0.04)
        if kind in ("win", "glass"):
            pane = part(o1, o2, b1, b2, GLASS, 0.03, True, opacity=0.3, shininess=1)
            if pane:
                GLASS_PANES.append(pane)
            part(o1 - f, o2 + f, b2, b2 + f, FRAME, d, False)
            part(o1 - f, o2 + f, b1 - f, b1, FRAME, d, False)
            n = max(1, round((o2 - o1) / (1.6 if kind == "win" else 1.3)))
            for i in range(n + 1):
                m = o1 + (o2 - o1) * i / n
                part(m - f / 2, m + f / 2, b1, b2, FRAME, d if i in (0, n) else 0.08, False)
        elif kind in ("door", "open"):
            fc = WOOD if kind == "door" else FRAME
            part(o1 - f, o1, b1, b2 + f, fc, d, False)
            part(o2, o2 + f, b1, b2 + f, fc, d, False)
            part(o1, o2, b2, b2 + f, fc, d, False)
    part(a, a2, y1, y2, col, t, solid)
    if skin:
        side, scol = skin
        wall(run, c + side * (t / 2 + 0.02), a1, a2, y1, y2,
             [(o[0], o[1], o[2], o[3], "none") for o in openings], t=0.04, col=scol, solid=False)


def slab(rects, holes, y1, y2, top_col, bottom_col=CEILING):
    fin = min(0.03, (y2 - y1) / 3)
    for (x1, x2, z1, z2) in rects:
        xs = sorted({x1, x2} | {v for h in holes for v in (h[0], h[1]) if x1 < v < x2})
        for xa, xb in zip(xs[:-1], xs[1:]):
            cuts = sorted((max(h[2], z1), min(h[3], z2)) for h in holes
                          if h[0] <= xa + 1e-6 and h[1] >= xb - 1e-6 and h[2] < z2 and h[3] > z1)
            z = z1
            for c1, c2 in cuts + [(z2, z2)]:
                if c1 - z > 0.005:
                    add_solid(xa, xb, y1, y2, z, c1)
                    block(xa, xb, y1, y2 - fin, z, c1, bottom_col)
                    block(xa, xb, y2 - fin, y2, z, c1, top_col)
                z = max(z, c2)


def rail(run, c, a1, a2, y):
    if run == "x":
        block(a1, a2, y, y + 1.05, c - 0.02, c + 0.02, RAIL_GLASS, solid=True, opacity=0.3)
        block(a1, a2, y + 1.05, y + 1.1, c - 0.03, c + 0.03, FRAME)
    else:
        block(c - 0.02, c + 0.02, y, y + 1.05, a1, a2, RAIL_GLASS, solid=True, opacity=0.3)
        block(c - 0.03, c + 0.03, y + 1.05, y + 1.1, a1, a2, FRAME)


def stairs(x_bottom, x_top, z1, z2, y_bottom, y_top, rail_z, n=21, flare=0.0, step_lights=False):
    run = (x_top - x_bottom) / n
    rise = (y_top - y_bottom) / n
    sx = 1 if run > 0 else -1
    open_side = 1 if rail_z >= (z1 + z2) / 2 else -1
    wall_z = z1 if open_side == 1 else z2
    for i in range(n):
        xa, xb = x_bottom + i * run, x_bottom + (i + 1) * run
        top = y_bottom + (i + 1) * rise
        za, zb = z1, z2
        if flare and i < 2:
            grow = flare * (1.0 if i == 0 else 0.5)
            xa -= sx * grow
            if open_side == 1:
                zb += grow
            else:
                za -= grow
        lo, hi = min(xa, xb), max(xa, xb)
        block(lo, hi, y_bottom, top - 0.05, za, zb, vector(0.92, 0.92, 0.89))
        nose = 0.03 * sx
        block(min(xa - nose, xb), max(xa - nose, xb), top - 0.05, top, za - 0.02, zb + 0.02, WOOD)
        add_solid(lo, hi, y_bottom, top, za, zb)
        if step_lights and i % 3 == 1:
            zl = wall_z + 0.012 * open_side
            block((xa + xb) / 2 - 0.08, (xa + xb) / 2 + 0.08, top + 0.18, top + 0.24, zl - 0.012, zl + 0.012,
                  LAMP, emissive=True)
    p1 = vector(x_bottom, y_bottom + rise, rail_z)
    p2 = vector(x_top, y_top, rail_z)
    glass_quad(p1, p2, p2 + vector(0, 0.95, 0), p1 + vector(0, 0.95, 0))
    cylinder(pos=p1 + vector(0, 1.0, 0), axis=p2 - p1, radius=0.04, color=WOOD)
    for p in (p1, p2):
        block(p.x - 0.06, p.x + 0.06, p.y - rise, p.y + 1.05, rail_z - 0.06, rail_z + 0.06, WOOD)
    d = p2 - p1
    box(pos=(p1 + p2) / 2 + vector(0, -0.16, 0), axis=d, up=vector(-d.y, d.x, 0), height=0.24, width=0.06,
        color=WOOD)


def glass_quad(p1, p2, p3, p4, col=RAIL_GLASS, op=0.3):
    for (a, b, c) in ((p1, p2, p3), (p1, p3, p4)):
        n = norm(cross(b - a, c - a))
        triangle(v0=vertex(pos=a, color=col, normal=n, opacity=op),
                 v1=vertex(pos=b, color=col, normal=n, opacity=op),
                 v2=vertex(pos=c, color=col, normal=n, opacity=op))


def tri(p1, p2, p3, col):
    n = norm(cross(p2 - p1, p3 - p1))
    triangle(v0=vertex(pos=p1, color=col, normal=n),
             v1=vertex(pos=p2, color=col, normal=n),
             v2=vertex(pos=p3, color=col, normal=n))
    triangle(v0=vertex(pos=p1, color=col, normal=-n),
             v1=vertex(pos=p3, color=col, normal=-n),
             v2=vertex(pos=p2, color=col, normal=-n))


def gable_end(plane, c, a1, a2, y0, ry, hole=None, col=WHITE_WALL):
    P = (lambda a, y: vector(c, y, a)) if plane == "x" else (lambda a, y: vector(a, y, c))
    am = (a1 + a2) / 2
    if hole is None:
        tri(P(a1, y0), P(a2, y0), P(am, ry), col)
        return
    h1, h2, v1, v2 = hole

    def aL(y):
        return a1 + (y - y0) / (ry - y0) * (am - a1)

    def aR(y):
        return a2 - (y - y0) / (ry - y0) * (a2 - am)

    def quad(p, q, r, s):
        tri(p, q, r, col)
        tri(p, r, s, col)
    quad(P(a1, y0), P(a2, y0), P(aR(v1), v1), P(aL(v1), v1))
    quad(P(aL(v1), v1), P(h1, v1), P(h1, v2), P(aL(v2), v2))
    quad(P(h2, v1), P(aR(v1), v1), P(aR(v2), v2), P(h2, v2))
    tri(P(aL(v2), v2), P(aR(v2), v2), P(am, ry), col)
    wall("z" if plane == "x" else "x", c, h1, h2, v1, v2, [(h1, h2, v1, v2, "win")],
         t=0.1, solid=False)


def gable_roof(x1, x2, z1, z2, wall_top, pitch, ridge="x",
               side_over=1.0, end_over=(0.6, 0.6), windows=(None, None)):
    a = radians(pitch)
    t = 0.22
    if ridge == "x":
        half, mid = (z2 - z1) / 2, (z1 + z2) / 2
        e1, e2 = x1 - end_over[0], x2 + end_over[1]
    else:
        half, mid = (x2 - x1) / 2, (x1 + x2) / 2
        e1, e2 = z1 - end_over[0], z2 + end_over[1]
    ridge_y = wall_top + half * tan(a)
    run = half + side_over
    slope_len = run / cos(a)
    L, emid = e2 - e1, (e1 + e2) / 2
    for s in (1, -1):
        y = ridge_y - (run / 2) * tan(a) + t / 2
        if ridge == "x":
            ax, up = vector(L, 0, 0), vector(0, cos(a), s * sin(a))
            center = vector(emid, y, mid + s * run / 2)
        else:
            ax, up = vector(0, 0, L), vector(s * sin(a), cos(a), 0)
            center = vector(mid + s * run / 2, y, emid)
        box(pos=center, axis=ax, up=up, height=t, width=slope_len, color=ROOF)
        box(pos=center - up * (t / 2 + 0.03), axis=ax, up=up,
            height=0.06, width=slope_len, color=SOFFIT)
    if ridge == "x":
        box(pos=vector(emid, ridge_y + t, mid), size=vector(L, 0.12, 0.4), color=ROOF)
        gable_end("x", x1, z1, z2, wall_top, ridge_y, windows[0])
        gable_end("x", x2, z1, z2, wall_top, ridge_y, windows[1])
    else:
        box(pos=vector(mid, ridge_y + t, emid), size=vector(0.4, 0.12, L), color=ROOF)
        gable_end("z", z1, x1, x2, wall_top, ridge_y, windows[0])
        gable_end("z", z2, x1, x2, wall_top, ridge_y, windows[1])
    return ridge_y


def hip_roof(x1, x2, z1, z2, wall_top, pitch, over=1.0, gable_east=False):
    a = tan(radians(pitch))
    ex1, ez1, ez2 = x1 - over, z1 - over, z2 + over
    ex2 = x2 if gable_east else x2 + over
    ye = wall_top - over * a
    half = (ez2 - ez1) / 2
    zc = (ez1 + ez2) / 2
    yr = ye + half * a
    rx1 = ex1 + half
    rx2 = ex2 if gable_east else ex2 - half
    if rx2 < rx1:
        rx1 = rx2 = (rx1 + rx2) / 2

    def quad(p, q, r, s, col):
        tri(p, q, r, col)
        if mag(r - s) > 1e-6:
            tri(p, r, s, col)

    for lift, col in ((0.0, SOFFIT), (0.2, ROOF)):
        u = vector(0, lift, 0)
        A1, A2 = vector(ex1, ye, ez1) + u, vector(ex2, ye, ez1) + u
        B1, B2 = vector(ex1, ye, ez2) + u, vector(ex2, ye, ez2) + u
        R1, R2 = vector(rx1, yr, zc) + u, vector(rx2, yr, zc) + u
        quad(A1, A2, R2, R1, col)
        quad(B1, B2, R2, R1, col)
        tri(A1, B1, R1, col)
        if not gable_east:
            tri(A2, B2, R2, col)
    if gable_east:
        tri(vector(x2, wall_top, z1), vector(x2, wall_top, z2), vector(x2, yr + 0.2, zc), EXT)
    fy1, fy2 = ye - 0.2, ye + 0.28
    block(ex1, ex2, fy1, fy2, ez1 - 0.06, ez1 + 0.06, ROOF)
    block(ex1, ex2, fy1, fy2, ez2 - 0.06, ez2 + 0.06, ROOF)
    block(ex1 - 0.06, ex1 + 0.06, fy1, fy2, ez1, ez2, ROOF)
    if not gable_east:
        block(ex2 - 0.06, ex2 + 0.06, fy1, fy2, ez1, ez2, ROOF)
    top = vector(0, 0.24, 0)
    corners = [(vector(ex1, ye, ez1), rx1), (vector(ex1, ye, ez2), rx1)]
    if not gable_east:
        corners += [(vector(ex2, ye, ez1), rx2), (vector(ex2, ye, ez2), rx2)]
    for c, rx in corners:
        cylinder(pos=c + top, axis=vector(rx, yr, zc) - c, radius=0.07, color=ROOF)
    if rx2 > rx1:
        cylinder(pos=vector(rx1, yr, zc) + top, axis=vector(rx2 - rx1, 0, 0), radius=0.08, color=ROOF)
    return yr


DIRS = {"+x": (1, 0), "-x": (-1, 0), "+z": (0, 1), "-z": (0, -1)}


def chair(x, z, face, y, col=color.white, legs=WOOD):
    dx, dz = DIRS[face]
    block(x - 0.23, x + 0.23, y + 0.40, y + 0.50, z - 0.23, z + 0.23, col)
    for sx in (-0.18, 0.18):
        for sz in (-0.18, 0.18):
            block(x + sx - 0.025, x + sx + 0.025, y, y + 0.40, z + sz - 0.025, z + sz + 0.025, legs)
    bx, bz = x - dx * 0.21, z - dz * 0.21
    if dx:
        block(bx - 0.04, bx + 0.04, y + 0.5, y + 1.05, z - 0.23, z + 0.23, col)
    else:
        block(x - 0.23, x + 0.23, y + 0.5, y + 1.05, bz - 0.04, bz + 0.04, col)


def soft_pillow(c, wdir, updir, w, h, th, col):
    box(pos=c, axis=wdir * w, up=updir, height=h, width=th * 0.42, color=col)
    ellipsoid(pos=c, axis=wdir * w * 0.97, up=updir, height=h * 0.97, width=th, color=col)


def sofa(x1, x2, z1, z2, y, back, col=SOFA, ends=("arm", "arm"), pillows=(), base=None,
         arm_col=None, legs=SOFA_LEGS):
    along_x = back in ("+z", "-z")
    a1, a2 = (x1, x2) if along_x else (z1, z2)
    lo, hi = (z1, z2) if along_x else (x1, x2)
    D = hi - lo
    sgn = 1 if back[0] == "+" else -1
    front = lo if sgn == 1 else hi
    base = base if base is not None else col * 0.80
    arm_col = arm_col if arm_col is not None else col * 0.92

    def dd(t1, t2):
        u, v = front + sgn * t1, front + sgn * t2
        return min(u, v), max(u, v)

    def part(b1, b2, y1, y2, t1, t2, c):
        d1, d2 = dd(t1, t2)
        if along_x:
            return block(b1, b2, y + y1, y + y2, d1, d2, c)
        return block(d1, d2, y + y1, y + y2, b1, b2, c)

    def P(b, yy, t):
        d = front + sgn * t
        return vector(b, y + yy, d) if along_x else vector(d, y + yy, b)

    def roll(b1, b2, yy, t, r, c):
        cylinder(pos=P(b1, yy, t), axis=P(b2, yy, t) - P(b1, yy, t), radius=r, color=c)

    BT, CT = 0.16, 0.18
    for bb in (a1 + 0.08, a2 - 0.08):
        for t in (0.08, D - 0.08):
            part(bb - 0.035, bb + 0.035, 0, 0.1, t - 0.035, t + 0.035, legs)
    part(a1, a2, 0.1, 0.36, 0, D, base)
    part(a1, a2, 0.36, 0.80, D - BT, D, base)
    aw = min(0.17, (a2 - a1) * 0.16)
    s1, s2 = a1, a2
    for (e, side) in ((ends[0], 0), (ends[1], 1)):
        b1, b2 = (a1, a1 + aw) if side == 0 else (a2 - aw, a2)
        if e == "arm":
            part(b1, b2, 0.1, 0.60, 0, D, arm_col)
            mid = (b1 + b2) / 2
            cylinder(pos=P(mid, 0.60, 0), axis=P(mid, 0.60, D) - P(mid, 0.60, 0), radius=aw / 2,
                     color=arm_col)
        elif e == "back":
            c1, c2 = (a1, a1 + BT) if side == 0 else (a2 - BT, a2)
            part(c1, c2, 0.36, 0.80, 0, D, base)
            k1, k2 = (c2, c2 + CT) if side == 0 else (c1 - CT, c1)
            part(k1, k2, 0.5, 0.86, 0.04, D - BT - CT, col * 1.04)
            mid = (k1 + k2) / 2
            cylinder(pos=P(mid, 0.86, 0.04), axis=P(mid, 0.86, D - BT - CT) - P(mid, 0.86, 0.04),
                     radius=CT / 2, color=col * 1.04)
            aw_e = BT
            b1, b2 = (a1, a1 + aw_e) if side == 0 else (a2 - aw_e, a2)
        if e:
            if side == 0:
                s1 = b2
            else:
                s2 = b1
    n = max(1, int(round((s2 - s1) / 0.9)))
    w = (s2 - s1) / n
    for i in range(n):
        c1, c2 = s1 + i * w + 0.012, s1 + (i + 1) * w - 0.012
        part(c1, c2, 0.36, 0.50, 0.07, D - BT, col * 1.06)
        roll(c1, c2, 0.43, 0.07, 0.07, col * 1.06)
        part(c1, c2, 0.50, 0.86, D - BT - CT, D - BT, col * 1.02)
        roll(c1, c2, 0.86, D - BT - CT / 2, CT / 2, col * 1.02)
    half = (len(pillows) + 1) // 2
    spots = [s1 + 0.32 + 0.5 * i for i in range(half)] + \
            [s2 - 0.32 - 0.5 * i for i in range(len(pillows) - half)]
    for bb, pc in zip(spots, pillows):
        wdir = vector(1, 0, 0) if along_x else vector(0, 0, 1)
        backdir = vector(0, 0, sgn) if along_x else vector(sgn, 0, 0)
        lean = radians(14)
        soft_pillow(P(bb, 0.72, D - BT - CT - 0.1), wdir, norm(vector(0, cos(lean), 0) + backdir * sin(lean)),
                    0.44, 0.42, 0.16, pc)


def armchair(x, z, back, y, col, pillow=None, w=0.9, d=0.88, base=None):
    sofa(x - (w if back[1] == "z" else d) / 2, x + (w if back[1] == "z" else d) / 2,
         z - (d if back[1] == "z" else w) / 2, z + (d if back[1] == "z" else w) / 2, y, back, col,
         ends=("arm", "arm"), pillows=[pillow] if pillow is not None else (), base=base)


def bench_seat(x1, x2, z1, z2, y, wood=WOOD, cushion=vector(0.80, 0.74, 0.66), h=0.46):
    for xx in (x1 + 0.05, x2 - 0.05):
        for zz in (z1 + 0.05, z2 - 0.05):
            block(xx - 0.025, xx + 0.025, y, y + h - 0.1, zz - 0.025, zz + 0.025, wood)
    block(x1, x2, y + h - 0.12, y + h - 0.07, z1, z2, wood)
    block(x1 + 0.01, x2 - 0.01, y + h - 0.07, y + h, z1 + 0.01, z2 - 0.01, cushion)
    if (x2 - x1) > (z2 - z1):
        cylinder(pos=vector(x1 + 0.01, y + h - 0.035, z2 - 0.01), axis=vector(x2 - x1 - 0.02, 0, 0), radius=0.035,
                 color=cushion)
    else:
        cylinder(pos=vector(x2 - 0.01, y + h - 0.035, z1 + 0.01), axis=vector(0, 0, z2 - z1 - 0.02), radius=0.035,
                 color=cushion)


def bed(x1, x2, z1, z2, y, head, frame=CABINET, sheet=color.white, band=None, headboard=None,
        accent=None):
    headboard = headboard if headboard is not None else frame
    accent = accent if accent is not None else (band if band is not None else vector(0.80, 0.74, 0.66))
    WHITE = vector(0.97, 0.97, 0.95)
    along_x = head == "-z"
    a1, a2 = (x1, x2) if along_x else (z1, z2)
    h1, h2 = (z1, z2) if along_x else (x1, x2)

    def part(b1, b2, y1, y2, t1, t2, c):
        if along_x:
            return block(b1, b2, y + y1, y + y2, t1, t2, c)
        return block(t1, t2, y + y1, y + y2, b1, b2, c)

    def P(b, yy, t):
        return vector(b, y + yy, t) if along_x else vector(t, y + yy, b)

    wdir = vector(1, 0, 0) if along_x else vector(0, 0, 1)
    headdir = vector(0, 0, -1) if along_x else vector(-1, 0, 0)

    def lean(deg, flat=False):
        a = radians(deg)
        if flat:
            return norm(headdir * cos(a) + vector(0, sin(a), 0))
        return norm(vector(0, cos(a), 0) + headdir * sin(a))

    W = a2 - a1
    part(a1 + 0.08, a2 - 0.08, 0, 0.12, h1 + 0.08, h2 - 0.08, frame * 0.6)
    part(a1, a2, 0.12, 0.34, h1, h2, frame)
    part(a1 + 0.04, a2 - 0.04, 0.34, 0.56, h1 + 0.04, h2 - 0.04, WHITE)
    d1 = h1 + 0.75
    part(a1 - 0.02, a2 + 0.02, 0.40, 0.62, d1, h2 + 0.02, sheet)
    cylinder(pos=P(a1 - 0.02, 0.60, d1 + 0.06), axis=P(a2 + 0.02, 0.60, d1 + 0.06) - P(a1 - 0.02, 0.60, d1 + 0.06),
             radius=0.06, color=WHITE)
    if band is not None:
        part(a1 - 0.035, a2 + 0.035, 0.30, 0.635, h2 - 0.75, h2 - 0.25, band)
    for k in (0.27, 0.73):
        soft_pillow(P(a1 + W * k, 0.68, h1 + 0.30), wdir, lean(18, flat=True), W * 0.42, 0.46, 0.17, WHITE)
        soft_pillow(P(a1 + W * k, 0.86, h1 + 0.58), wdir, lean(16), W * 0.36, 0.42, 0.15, accent)
    soft_pillow(P(a1 + W / 2, 0.76, h1 + 0.74), wdir, lean(12), W * 0.30, 0.26, 0.13,
                frame if band is None else band)
    part(a1 - 0.08, a2 + 0.08, 0.10, 1.30, h1 - 0.12, h1, headboard * 0.85)
    n = max(4, int(W / 0.22))
    w = (W + 0.12) / n
    for i in range(n):
        b = a1 - 0.06 + (i + 0.5) * w
        cylinder(pos=P(b, 0.36, h1 - 0.03), axis=vector(0, 0.88, 0), radius=w * 0.48, color=headboard)


PORCELAIN = vector(0.97, 0.97, 0.96)
SHOWER_TILE = vector(0.36, 0.35, 0.34)
GROUT = vector(0.25, 0.25, 0.25)


def _frame(face):
    dx, dz = DIRS[face]
    return vector(dx, 0, dz), vector(-dz, 0, dx)


def toilet(x, z, face, y):
    fwd, side = _frame(face)
    c = vector(x, y, z)
    box(pos=c + fwd * 0.02 + vector(0, 0.17, 0), axis=fwd * 0.38, up=vector(0, 1, 0), height=0.34, width=0.27,
        color=PORCELAIN)
    ellipsoid(pos=c + fwd * 0.08 + vector(0, 0.34, 0), axis=fwd * 0.62, height=0.2, width=0.42, color=PORCELAIN)
    ellipsoid(pos=c + fwd * 0.08 + vector(0, 0.44, 0), axis=fwd * 0.58, height=0.045, width=0.4,
              color=vector(0.93, 0.93, 0.92))
    box(pos=c - fwd * 0.26 + vector(0, 0.55, 0), axis=fwd * 0.18, up=vector(0, 1, 0), height=0.44, width=0.4,
        color=PORCELAIN)
    cylinder(pos=c - fwd * 0.26 + vector(0, 0.77, 0), axis=vector(0, 0.008, 0), radius=0.045, color=CHROME)


def faucet_wall(x, y, z, face, col=None):
    col = col if col is not None else CHROME
    fwd, side = _frame(face)
    p = vector(x, y, z)
    cylinder(pos=p, axis=fwd * 0.02, radius=0.03, color=col)
    cylinder(pos=p, axis=fwd * 0.17, radius=0.012, color=col)
    cylinder(pos=p + fwd * 0.17, axis=vector(0, -0.03, 0), radius=0.012, color=col)
    cylinder(pos=p + side * 0.12, axis=fwd * 0.05, radius=0.018, color=col)


def vessel_sink(x, y, z, face=None):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.03, 0), radius=0.16, color=PORCELAIN)
    cylinder(pos=vector(x, y + 0.03, z), axis=vector(0, 0.12, 0), radius=0.22, color=PORCELAIN)
    cylinder(pos=vector(x, y + 0.149, z), axis=vector(0, 0.002, 0), radius=0.195, color=vector(0.90, 0.91, 0.92))
    cylinder(pos=vector(x, y + 0.151, z), axis=vector(0, 0.002, 0), radius=0.03, color=CHROME)
    if face:
        fwd, side = _frame(face)
        faucet_wall(x - fwd.x * 0.28, y + 0.38, z - fwd.z * 0.28, face)


def tub(x1, x2, z1, z2, y, faucet_end=1):
    along_z = (z2 - z1) > (x2 - x1)
    W = (x2 - x1) if along_z else (z2 - z1)
    r = W / 2
    cx, cz = (x1 + x2) / 2, (z1 + z2) / 2
    h = 0.6
    if along_z:
        block(x1, x2, y, y + h, z1 + r, z2 - r, PORCELAIN)
        ends = [vector(cx, y, z1 + r), vector(cx, y, z2 - r)]
        block(x1 + 0.07, x2 - 0.07, y + h - 0.005, y + h + 0.002, z1 + r, z2 - r, vector(0.86, 0.90, 0.93))
    else:
        block(x1 + r, x2 - r, y, y + h, z1, z2, PORCELAIN)
        ends = [vector(x1 + r, y, cz), vector(x2 - r, y, cz)]
        block(x1 + r, x2 - r, y + h - 0.005, y + h + 0.002, z1 + 0.07, z2 - 0.07, vector(0.86, 0.90, 0.93))
    for e in ends:
        cylinder(pos=e, axis=vector(0, h, 0), radius=r, color=PORCELAIN)
        cylinder(pos=e + vector(0, h - 0.005, 0), axis=vector(0, 0.007, 0), radius=r - 0.07,
                 color=vector(0.86, 0.90, 0.93))
    cylinder(pos=vector(cx, y, cz), axis=vector(0, 0.02, 0), radius=r * 0.9, color=vector(0.85, 0.85, 0.84))
    e = ends[1 if faucet_end > 0 else 0]
    out = norm(e - vector(cx, y, cz))
    fp = e + out * (r + 0.18)
    cylinder(pos=fp, axis=vector(0, 1.0, 0), radius=0.02, color=CHROME)
    cylinder(pos=fp + vector(0, 1.0, 0), axis=-out * 0.25, radius=0.015, color=CHROME)
    cylinder(pos=fp + vector(0, 1.0, 0) - out * 0.25, axis=vector(0, -0.06, 0), radius=0.015, color=CHROME)
    cylinder(pos=fp, axis=vector(0, 0.02, 0), radius=0.07, color=CHROME)


def vanity(x1, x2, z1, z2, y, face, sinks=(), col=None, seed=21):
    col = col if col is not None else KWOOD
    block(x1, x2, y + 0.42, y + 0.82, z1, z2, col)
    marble(x1 - 0.01, x2 + 0.01, y + 0.82, y + 0.86, z1 - 0.01, z2 + 0.01, ("top",), seed=seed)
    fwd, side = _frame(face)
    if face in ("+z", "-z"):
        zf = z2 if face == "+z" else z1
        n = max(1, int(round((x2 - x1) / 0.6)))
        for i in range(1, n):
            xg = x1 + i * (x2 - x1) / n
            block(xg - 0.005, xg + 0.005, y + 0.44, y + 0.8, zf - 0.002, zf + 0.002, KGAP)
        for i in range(n):
            xc = x1 + (i + 0.5) * (x2 - x1) / n
            block(xc - 0.12, xc + 0.12, y + 0.74, y + 0.755, zf + fwd.z * 0.002, zf + fwd.z * 0.02, CHROME)
        block(x1 + 0.03, x2 - 0.03, y + 0.41, y + 0.42, z1 + 0.03, z2 - 0.03, LAMP, emissive=True)
        for xs in sinks:
            vessel_sink(xs, y + 0.86, (z1 + z2) / 2 + fwd.z * 0.03, face)
    else:
        xf = x2 if face == "+x" else x1
        n = max(1, int(round((z2 - z1) / 0.6)))
        for i in range(1, n):
            zg = z1 + i * (z2 - z1) / n
            block(xf - 0.002, xf + 0.002, y + 0.44, y + 0.8, zg - 0.005, zg + 0.005, KGAP)
        for i in range(n):
            zc = z1 + (i + 0.5) * (z2 - z1) / n
            block(min(xf, xf + fwd.x * 0.02), max(xf, xf + fwd.x * 0.02), y + 0.74, y + 0.755, zc - 0.12, zc + 0.12,
                  CHROME)
        block(x1 + 0.03, x2 - 0.03, y + 0.41, y + 0.42, z1 + 0.03, z2 - 0.03, LAMP, emissive=True)
        for zs in sinks:
            vessel_sink((x1 + x2) / 2 + fwd.x * 0.03, y + 0.86, zs, face)


def lit_mirror(c, w, h, face, round_=False):
    fwd, side = _frame(face)
    if round_:
        cylinder(pos=c - fwd * 0.03, axis=fwd * 0.01, radius=w / 2 + 0.03, color=LAMP, emissive=True)
        cylinder(pos=c - fwd * 0.02, axis=fwd * 0.02, radius=w / 2, color=MIRROR, shininess=1)
    else:
        box(pos=c - fwd * 0.025, axis=side * (w + 0.05), up=vector(0, 1, 0), height=h + 0.05, width=0.01,
            color=LAMP, emissive=True)
        box(pos=c - fwd * 0.01, axis=side * w, up=vector(0, 1, 0), height=h, width=0.02, color=MIRROR, shininess=1)


def tiled(x1, x2, y1, y2, z1, z2, col=SHOWER_TILE, step=0.6):
    block(x1, x2, y1, y2, z1, z2, col)
    sx, sy, sz = x2 - x1, y2 - y1, z2 - z1
    if sx <= sy and sx <= sz:
        v = y1 + step / 2
        while v < y2:
            block(x1 - 0.002, x2 + 0.002, v - 0.004, v + 0.004, z1, z2, GROUT)
            v += step / 2
        v = z1 + step
        while v < z2:
            block(x1 - 0.002, x2 + 0.002, y1, y2, v - 0.004, v + 0.004, GROUT)
            v += step
    elif sz <= sx and sz <= sy:
        v = y1 + step / 2
        while v < y2:
            block(x1, x2, v - 0.004, v + 0.004, z1 - 0.002, z2 + 0.002, GROUT)
            v += step / 2
        v = x1 + step
        while v < x2:
            block(v - 0.004, v + 0.004, y1, y2, z1 - 0.002, z2 + 0.002, GROUT)
            v += step
    else:
        v = x1 + step
        while v < x2:
            block(v - 0.004, v + 0.004, y2, y2 + 0.002, z1, z2, GROUT)
            v += step
        v = z1 + step
        while v < z2:
            block(x1, x2, y2, y2 + 0.002, v - 0.004, v + 0.004, GROUT)
            v += step


def shower_set(head, mixer, face):
    fwd, side = _frame(face)
    cylinder(pos=head, axis=vector(0, 0.015, 0), radius=0.16, color=CHROME)
    cylinder(pos=head + vector(0, 0.015, 0), axis=vector(0, 0.35, 0), radius=0.012, color=CHROME)
    cylinder(pos=mixer, axis=fwd * 0.02, radius=0.07, color=CHROME)
    cylinder(pos=mixer + fwd * 0.02, axis=fwd * 0.04, radius=0.02, color=CHROME)
    cylinder(pos=mixer + side * 0.25 - vector(0, 0.3, 0), axis=vector(0, 0.9, 0), radius=0.01, color=CHROME)
    cylinder(pos=mixer + side * 0.25 + vector(0, 0.35, 0) + fwd * 0.03, axis=vector(0, -0.2, 0) + fwd * 0.05,
             radius=0.02, color=CHROME)


def towel_bar(p1, p2, towel=vector(0.95, 0.94, 0.90), face="+z"):
    fwd, side = _frame(face)
    cylinder(pos=p1 + fwd * 0.06, axis=p2 - p1, radius=0.012, color=CHROME)
    mid = (p1 + p2) / 2 + fwd * 0.06
    box(pos=mid + vector(0, -0.2, 0), axis=norm(p2 - p1) * mag(p2 - p1) * 0.8, up=vector(0, 1, 0), height=0.42,
        width=0.04, color=towel)


def tp_holder(p, face):
    fwd, side = _frame(face)
    cylinder(pos=p, axis=fwd * 0.04, radius=0.02, color=CHROME)
    cylinder(pos=p + fwd * 0.07 - side * 0.06, axis=side * 0.12, radius=0.055, color=PORCELAIN)


def glass_screen(x1, x2, y1, y2, z1, z2, solid=True):
    block(x1, x2, y1, y2, z1, z2, GLASS, opacity=0.25, solid=solid)
    block(x1 - 0.005, x2 + 0.005, y2 - 0.02, y2, z1 - 0.005, z2 + 0.005, CHROME)


def downlight(x, y, z):
    cylinder(pos=vector(x, y - 0.02, z), axis=vector(0, 0.02, 0), radius=0.07,
             color=LAMP, emissive=True)


def pendant(x, y_ceiling, y_lamp, z, r=0.18, col=LAMP):
    cylinder(pos=vector(x, y_lamp, z), axis=vector(0, y_ceiling - y_lamp, 0), radius=0.008, color=FRAME)
    sphere(pos=vector(x, y_lamp, z), radius=r, color=col, emissive=True)


def spiral_chandelier(x, y_top, z, y_bottom, turns=2.5, n=110):
    CRYSTAL = vector(0.93, 0.96, 1.0)
    cylinder(pos=vector(x, y_top - 0.12, z), axis=vector(0, 0.12, 0), radius=1.0,
             color=vector(0.30, 0.28, 0.25), shininess=1)
    ring(pos=vector(x, y_top - 0.12, z), axis=vector(0, 1, 0), radius=1.0, thickness=0.03, color=GOLD)
    for k in range(14):
        ang = 2 * pi * k / 14
        for rr in (0.45, 0.8):
            cylinder(pos=vector(x + rr * cos(ang + rr), y_top - 0.13, z + rr * sin(ang + rr)),
                     axis=vector(0, 0.01, 0), radius=0.05, color=LAMP, emissive=True)
    ring(pos=vector(x, y_top - 0.02, z), axis=vector(0, 1, 0), radius=1.45, thickness=0.04,
         color=LAMP, emissive=True)
    y0 = y_top - 0.12
    theta_max = 2 * pi * turns
    for k in range(n):
        f = k / (n - 1)
        th = theta_max * f
        r = 0.85 - 0.35 * f
        L = 0.5 + f * (y0 - y_bottom - 0.5)
        top = vector(x + r * cos(th), y0, z + r * sin(th))
        cylinder(pos=top, axis=vector(0, -L, 0), radius=0.004, color=CRYSTAL)
        for b in (0.4, 0.75):
            sphere(pos=top - vector(0, L * b, 0), radius=0.028, color=CRYSTAL, emissive=True)
        ellipsoid(pos=top - vector(0, L + 0.05, 0), size=vector(0.08, 0.17, 0.08),
                  color=LAMP, emissive=True)
        if k % 2 == 0:
            top2 = vector(x + (r - 0.08) * cos(th + 0.12), y0, z + (r - 0.08) * sin(th + 0.12))
            cylinder(pos=top2, axis=vector(0, -(L + 0.15), 0), radius=0.004, color=CRYSTAL)
            ellipsoid(pos=top2 - vector(0, L + 0.2, 0), size=vector(0.07, 0.15, 0.07),
                      color=CRYSTAL, emissive=True)
    for k in range(16):
        ang = 2 * pi * k / 16
        L = 1.2 + 0.8 * ((k * 7) % 16) / 16
        top = vector(x + 0.25 * cos(ang), y0, z + 0.25 * sin(ang))
        cylinder(pos=top, axis=vector(0, -L, 0), radius=0.004, color=CRYSTAL)
        sphere(pos=top - vector(0, L, 0), radius=0.035, color=CRYSTAL, emissive=True)


def crystal_flush(x, y_ceiling, z, r=0.32, h=0.55):
    CR = vector(0.93, 0.96, 1.0)
    yc = y_ceiling - 0.06
    cylinder(pos=vector(x, y_ceiling - 0.004, z), axis=vector(0, 0.003, 0), radius=r * 3.2,
             color=LAMP, emissive=True, opacity=0.18)
    cylinder(pos=vector(x, yc, z), axis=vector(0, 0.06, 0), radius=r, color=CHROME, shininess=1)
    ring(pos=vector(x, yc, z), axis=vector(0, 1, 0), radius=r, thickness=0.012, color=CHROME)
    for k in range(3):
        a = 2 * pi * k / 3
        sphere(pos=vector(x + 0.09 * cos(a), yc - 0.16, z + 0.09 * sin(a)), radius=0.045,
               color=LAMP, emissive=True)
    for (rr, n, L) in [(r * 0.92, 20, h * 0.55), (r * 0.62, 12, h * 0.78), (r * 0.3, 6, h * 0.95)]:
        for k in range(n):
            a = 2 * pi * k / n + rr
            top = vector(x + rr * cos(a), yc, z + rr * sin(a))
            LL = L * (0.9 + 0.1 * sin(5 * a))
            cylinder(pos=top, axis=vector(0, -LL, 0), radius=0.004, color=CR)
            sphere(pos=top - vector(0, LL * 0.5, 0), radius=0.018, color=CR, emissive=True)
            ellipsoid(pos=top - vector(0, LL + 0.04, 0), size=vector(0.03, 0.09, 0.03), color=CR,
                      emissive=True)
    cylinder(pos=vector(x, yc - h - 0.02, z), axis=vector(0, h * 0.3, 0), radius=0.004, color=CR)
    sphere(pos=vector(x, yc - h - 0.06, z), radius=0.05, color=CR, emissive=True)


def ring_chandelier(x, y_ceiling, z, s=0.68):
    BLACK = vector(0.07, 0.07, 0.08)
    BRASS = vector(0.82, 0.60, 0.28)
    CABLE = vector(0.72, 0.72, 0.72)
    LED = vector(1.0, 0.97, 0.90)
    yc = y_ceiling - 0.05
    cylinder(pos=vector(x, yc, z), axis=vector(0, 0.05, 0), radius=0.24 * s, color=BLACK)
    for k in range(6):
        a = 2 * pi * k / 6 + 0.3
        cylinder(pos=vector(x + 0.18 * s * cos(a), yc - 0.02, z + 0.18 * s * sin(a)), axis=vector(0, 0.02, 0),
                 radius=0.012, color=BLACK)
    rings = [(vector(x + 0.05 * s, y_ceiling - 0.95 * s, z - 0.05 * s), 0.62 * s, norm(vector(0.38, 1.0, 0.12)), 0.3),
             (vector(x - 0.05 * s, y_ceiling - 1.20 * s, z + 0.05 * s), 0.80 * s, norm(vector(-0.12, 1.0, -0.30)), 1.3)]
    for (rc, R, n, t0) in rings:
        ring(pos=rc, axis=n, radius=R, thickness=0.024, color=BLACK)
        ring(pos=rc - n * 0.018, axis=n, radius=R - 0.008, thickness=0.018, color=LED, emissive=True)
        u = norm(cross(n, vector(0, 0, 1)))
        v = cross(n, u)
        for k in range(3):
            t = t0 + 2 * pi * k / 3
            p = rc + R * (u * cos(t) + v * sin(t)) + n * 0.024
            top = vector(x + 0.18 * s * cos(t), yc - 0.02, z + 0.18 * s * sin(t))
            cylinder(pos=top, axis=p - top, radius=0.003, color=CABLE)
    for (dx, dz, top, L) in [(0.12, -0.10, 0.85, 0.55), (-0.16, 0.14, 0.62, 0.42)]:
        p = vector(x + dx * s, y_ceiling - top * s, z + dz * s)
        L *= s
        r = 0.045 * s
        cylinder(pos=vector(p.x, yc, p.z), axis=vector(0, p.y - yc, 0), radius=0.003, color=CABLE)
        cylinder(pos=p, axis=vector(0, -L, 0), radius=r, color=BLACK)
        cylinder(pos=p - vector(0, L - 0.16 * s, 0), axis=vector(0, 0.06 * s, 0), radius=r * 1.05, color=BRASS)
        cylinder(pos=p - vector(0, L + 0.08 * s, 0), axis=vector(0, 0.08 * s, 0), radius=r * 0.9, color=LED,
                 emissive=True)


def cube_chandelier(x, y_ceiling, z, yc=10.25):
    OAK = vector(0.82, 0.62, 0.38)
    LED = vector(1.0, 0.88, 0.62)
    CABLE = vector(0.75, 0.75, 0.75)
    C = vector(x, yc, z)

    def bar(p1, p2, col=OAK, t=0.045, lit=False):
        lo = vector(min(p1.x, p2.x) - t / 2, min(p1.y, p2.y) - t / 2, min(p1.z, p2.z) - t / 2)
        hi = vector(max(p1.x, p2.x) + t / 2, max(p1.y, p2.y) + t / 2, max(p1.z, p2.z) + t / 2)
        block(lo.x, hi.x, lo.y, hi.y, lo.z, hi.z, col, emissive=(col is LED))
        if lit:
            if abs(p1.y - p2.y) < 1e-6:
                block(lo.x + 0.01, hi.x - 0.01, lo.y - 0.006, lo.y, lo.z + 0.01, hi.z - 0.01, LED,
                      emissive=True)
            else:
                block(lo.x - 0.006, lo.x, lo.y + 0.02, hi.y - 0.02, lo.z + 0.012, hi.z - 0.012, LED,
                      emissive=True)

    def square(dx, dy, dz, size, plane, lit=()):
        c = C + vector(dx, dy, dz)
        h = size / 2
        if plane == "xy":
            pts = [c + vector(-h, -h, 0), c + vector(h, -h, 0), c + vector(h, h, 0), c + vector(-h, h, 0)]
        elif plane == "zy":
            pts = [c + vector(0, -h, -h), c + vector(0, -h, h), c + vector(0, h, h), c + vector(0, h, -h)]
        else:
            pts = [c + vector(-h, 0, -h), c + vector(h, 0, -h), c + vector(h, 0, h), c + vector(-h, 0, h)]
        for k in range(4):
            bar(pts[k], pts[(k + 1) % 4], lit=k in lit)

    square(0.00, 0.00, -0.32, 0.92, "xy", lit=(2,))
    square(0.14, 0.10, 0.26, 0.76, "xy", lit=(0, 2))
    square(-0.12, -0.14, -0.02, 0.60, "xy")
    square(-0.40, 0.02, 0.04, 0.86, "zy", lit=(2,))
    square(0.36, -0.08, -0.10, 0.70, "zy", lit=(0,))
    square(0.06, 0.16, 0.12, 0.54, "zy")
    square(0.00, -0.46, 0.00, 0.94, "xz", lit=(0, 2))
    square(0.10, 0.44, -0.04, 0.80, "xz")
    square(-0.06, 0.04, 0.02, 0.48, "xz", lit=(1,))
    for (p1, p2) in [(vector(-0.72, 0.30, -0.32), vector(0.30, 0.30, -0.32)),
                     (vector(0.14, 0.02, -0.66), vector(0.14, 0.02, 0.46)),
                     (vector(0.30, -0.62, 0.26), vector(0.30, 0.56, 0.26)),
                     (vector(-0.40, -0.58, -0.22), vector(-0.40, 0.48, -0.22))]:
        bar(C + p1, C + p2, col=LED, t=0.035)
    for (dx, dz) in [(-0.35, -0.3), (0.4, 0.3), (0.05, -0.05)]:
        top = vector(x + dx, yc + 0.48, z + dz)
        cylinder(pos=top, axis=vector(0, y_ceiling - top.y, 0), radius=0.004, color=CABLE)
        cylinder(pos=vector(x + dx, y_ceiling - 0.04, z + dz), axis=vector(0, 0.04, 0), radius=0.05, color=OAK)


MARBLE_W = vector(0.95, 0.945, 0.925)
VEIN_COLS = (vector(0.58, 0.59, 0.61), vector(0.70, 0.64, 0.54), vector(0.76, 0.76, 0.78))
KWOOD = vector(0.36, 0.23, 0.14)
KGAP = vector(0.12, 0.08, 0.05)


def marble(x1, x2, y1, y2, z1, z2, faces=("top",), seed=1, solid=False):
    block(x1, x2, y1, y2, z1, z2, MARBLE_W, solid=solid, shininess=0.9)
    rng = Random(seed)
    e = 0.003
    for f in faces:
        if f == "top":
            U, V, P, nrm = (x1, x2), (z1, z2), (lambda u, v: vector(u, y2 + e, v)), vector(0, 1, 0)
            du, dv = vector(1, 0, 0), vector(0, 0, 1)
        elif f in ("front", "back"):
            zz = z2 + e if f == "front" else z1 - e
            U, V, P, nrm = (x1, x2), (y1, y2), (lambda u, v, zz=zz: vector(u, v, zz)), vector(0, 0, 1 if f == "front" else -1)
            du, dv = vector(1, 0, 0), vector(0, 1, 0)
        else:
            xx = x1 - e if f == "left" else x2 + e
            U, V, P, nrm = (z1, z2), (y1, y2), (lambda u, v, xx=xx: vector(xx, v, u)), vector(-1 if f == "left" else 1, 0, 0)
            du, dv = vector(0, 0, 1), vector(0, 1, 0)
        su, sv = U[1] - U[0], V[1] - V[0]
        if min(su, sv) < 0.12:
            continue
        a0 = rng.uniform(0.25, 0.75) * rng.choice([-1, 1])
        for k in range(1 + int(su * sv * 1.6)):
            u, v = U[0], rng.uniform(V[0], V[1])
            if rng.random() < 0.4:
                u, v = rng.uniform(U[0], U[1]), (V[0] if a0 > 0 else V[1])
            a = a0 + rng.uniform(-0.25, 0.25)
            w = 0.016 if k == 0 else rng.uniform(0.004, 0.011)
            col = VEIN_COLS[0] if k == 0 else rng.choice(VEIN_COLS)
            for seg in range(8):
                a += rng.uniform(-0.35, 0.35) + (a0 - a) * 0.3
                L = rng.uniform(0.16, 0.34)
                cu, cv = cos(a), sin(a)
                t = L
                if cu > 1e-6:
                    t = min(t, (U[1] - u) / cu)
                if cu < -1e-6:
                    t = min(t, (U[0] - u) / cu)
                if cv > 1e-6:
                    t = min(t, (V[1] - v) / cv)
                if cv < -1e-6:
                    t = min(t, (V[0] - v) / cv)
                if t < 0.01:
                    break
                p1, p2 = P(u, v), P(u + cu * t, v + cv * t)
                box(pos=(p1 + p2) / 2, axis=(du * cu + dv * cv) * t, up=nrm, height=0.002, width=w, color=col)
                u, v = u + cu * t, v + cv * t
                w *= rng.uniform(0.85, 1.05)


def cabinet_run_x(x1, x2, y1, y2, z_front, depth, door=0.6, drawers=True, col=KWOOD, handle=STEEL):
    block(x1, x2, y1, y2, z_front - depth, z_front, col)
    n = max(1, int(round((x2 - x1) / door)))
    w = (x2 - x1) / n
    for i in range(1, n):
        xg = x1 + i * w
        block(xg - 0.005, xg + 0.005, y1 + 0.02, y2 - 0.02, z_front, z_front + 0.004, KGAP)
    if drawers:
        block(x1 + 0.01, x2 - 0.01, y2 - 0.22, y2 - 0.21, z_front, z_front + 0.004, KGAP)
    hy = y2 - 0.12 if drawers else (y1 + 0.08 if y1 > 1.5 else y2 - 0.1)
    for i in range(n):
        xc = x1 + (i + 0.5) * w
        block(xc - w * 0.3, xc + w * 0.3, hy - 0.008, hy + 0.008, z_front + 0.004, z_front + 0.025, handle)


def cabinet_run_z(x_front, depth, y1, y2, z1, z2, door=0.6, drawers=True, col=color.white, handle=STEEL):
    block(x_front, x_front + depth, y1, y2, z1, z2, col)
    n = max(1, int(round((z2 - z1) / door)))
    w = (z2 - z1) / n
    gap = vector(0.70, 0.70, 0.70) if col.x > 0.8 else KGAP
    for i in range(1, n):
        zg = z1 + i * w
        block(x_front - 0.004, x_front, y1 + 0.02, y2 - 0.02, zg - 0.005, zg + 0.005, gap)
    if drawers:
        block(x_front - 0.004, x_front, y2 - 0.22, y2 - 0.21, z1 + 0.01, z2 - 0.01, gap)
    hy = y2 - 0.12 if drawers else (y1 + 0.08 if y1 > 1.5 else y2 - 0.1)
    for i in range(n):
        zc = z1 + (i + 0.5) * w
        block(x_front - 0.025, x_front - 0.004, hy - 0.008, hy + 0.008, zc - w * 0.3, zc + w * 0.3, handle)


def faucet(x, y, z, face, col=FRAME):
    d = vector(0, 0, 1) if face == "+z" else vector(-1, 0, 0)
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.04, 0), radius=0.035, color=col)
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.36, 0), radius=0.016, color=col)
    p = vector(x, y + 0.36, z)
    for k in range(6):
        a1, a2 = pi * k / 6, pi * (k + 1) / 6
        q1 = vector(x, y + 0.36, z) + d * (0.11 - 0.11 * cos(a1)) + vector(0, 0.11 * sin(a1), 0)
        q2 = vector(x, y + 0.36, z) + d * (0.11 - 0.11 * cos(a2)) + vector(0, 0.11 * sin(a2), 0)
        cylinder(pos=q1, axis=q2 - q1, radius=0.016, color=col)
        p = q2
    cylinder(pos=p, axis=vector(0, -0.06, 0), radius=0.02, color=col)
    cylinder(pos=vector(x, y + 0.2, z) - d * 0.05, axis=-d * 0.08, radius=0.008, color=col)


def cooktop(x1, x2, y, z1, z2):
    block(x1, x2, y, y + 0.012, z1, z2, vector(0.06, 0.06, 0.07), shininess=1)
    for (fx, fz, r) in [(0.27, 0.3, 0.10), (0.73, 0.3, 0.085), (0.27, 0.72, 0.085), (0.73, 0.72, 0.10)]:
        cx, cz = x1 + (x2 - x1) * fx, z1 + (z2 - z1) * fz
        cylinder(pos=vector(cx, y + 0.012, cz), axis=vector(0, 0.002, 0), radius=r, color=vector(0.30, 0.30, 0.32))
        cylinder(pos=vector(cx, y + 0.013, cz), axis=vector(0, 0.002, 0), radius=r - 0.012, color=vector(0.06, 0.06, 0.07))


def kitchen_sink(x1, x2, y, z1, z2):
    block(x1, x2, y + 0.001, y + 0.004, z1, z2, vector(0.55, 0.57, 0.59), shininess=1)
    block(x1 + 0.03, x2 - 0.03, y + 0.004, y + 0.006, z1 + 0.03, z2 - 0.03, vector(0.30, 0.31, 0.33), shininess=1)


def flower_lamp(p, size=0.11):
    sphere(pos=p, radius=size * 0.28, color=LAMP, emissive=True)
    for k in range(5):
        a = 2 * pi * k / 5
        d = norm(vector(cos(a), 0.8, sin(a)))
        ellipsoid(pos=p + d * size * 0.45, axis=d * size, up=vector(-sin(a), 0, cos(a)),
                  height=size * 0.65, width=size * 0.14, color=vector(0.99, 0.97, 0.92), emissive=True)


def branch_chandelier(x, y_ceiling, z, length=2.6, y_hang=3.1, seed=11):
    BRASS = vector(0.74, 0.56, 0.28)
    rng = Random(seed)
    hub = vector(x, y_hang, z)
    cylinder(pos=vector(x, y_ceiling - 0.05, z), axis=vector(0, 0.05, 0), radius=0.12, color=BRASS)
    cylinder(pos=hub, axis=vector(0, y_ceiling - y_hang, 0), radius=0.014, color=BRASS)
    cylinder(pos=hub + vector(0, -0.05, 0), axis=vector(0, 0.35, 0), radius=0.05, color=BRASS)
    ends = []
    for k in range(8):
        a = (pi / 2 if k % 2 == 0 else -pi / 2) + rng.uniform(-0.7, 0.7)
        L = rng.uniform(0.55, 1.0) * length / 2
        p = hub + vector(0, rng.uniform(-0.02, 0.06), 0)
        seg = L / 4
        for s_ in range(4):
            a += rng.uniform(-0.35, 0.35)
            q = p + vector(cos(a) * seg, rng.uniform(-0.05, 0.07), sin(a) * seg)
            cylinder(pos=p, axis=q - p, radius=0.024 * (1 - s_ * 0.18), color=BRASS)
            if s_ >= 1:
                b = a + rng.choice([-1, 1]) * rng.uniform(0.6, 1.3)
                tl = rng.uniform(0.14, 0.28)
                tip = q + vector(cos(b) * tl, rng.uniform(0.03, 0.12), sin(b) * tl)
                cylinder(pos=q, axis=tip - q, radius=0.009, color=BRASS)
                flower_lamp(tip, rng.uniform(0.09, 0.12))
            p = q
        flower_lamp(p + vector(0, 0.03, 0), 0.12)
        ends.append(p)
    for e in (max(ends, key=lambda v: v.z), min(ends, key=lambda v: v.z)):
        cylinder(pos=e, axis=vector(x, y_ceiling, z) - e, radius=0.003, color=vector(0.2, 0.2, 0.2))


def bar_stool(x, z, y):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.02, 0), radius=0.2, color=FRAME)
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.72, 0), radius=0.025, color=FRAME)
    cylinder(pos=vector(x, y + 0.72, z), axis=vector(0, 0.05, 0), radius=0.2, color=FRAME)


CAR_GLASS = vector(0.10, 0.12, 0.14)
CHROME = vector(0.86, 0.87, 0.89)
TIRE = vector(0.07, 0.07, 0.08)


def panel(p1, p2, w, t, col, xc, **extra):
    d = p2 - p1
    return box(pos=(p1 + p2) / 2 + vector(xc, 0, 0), axis=vector(w, 0, 0),
               up=vector(0, d.z, -d.y), height=t, width=mag(d), color=col, **extra)


def wheel(xc, yc, zc, r, w, rim, spokes=3, rim_r=0.62):
    side = 1 if xc > 0 else -1
    cylinder(pos=vector(xc - w / 2, yc, zc), axis=vector(w, 0, 0), radius=r, color=TIRE)
    xs = xc + side * (w / 2 + 0.005)
    cylinder(pos=vector(xs, yc, zc), axis=vector(side * 0.01, 0, 0), radius=r * rim_r, color=TIRE * 2)
    for k in range(spokes):
        ang = pi * k / spokes
        box(pos=vector(xs + side * 0.012, yc, zc), axis=vector(0, cos(ang), sin(ang)) * r * rim_r * 1.95,
            up=vector(1, 0, 0), height=0.02, width=0.06, color=rim)
    cylinder(pos=vector(xs, yc, zc), axis=vector(side * 0.03, 0, 0), radius=r * 0.15, color=rim)


def body_block(x, w, y1, y2, z1, z2, col, **extra):
    return block(x - w / 2, x + w / 2, y1, y2, z1, z2, col, **extra)


def car_van(x, z, y0=0.15):
    col = vector(0.36, 0.38, 0.40)
    W, L = 1.95, 5.3
    zf, zb = z + L / 2, z - L / 2
    body_block(x, W, y0 + 0.3, y0 + 1.15, zb, zf - 0.25, col)
    body_block(x, W, y0 + 0.25, y0 + 0.85, zf - 0.25, zf, col)
    body_block(x, W - 0.04, y0 + 1.15, y0 + 2.0, zb, zf - 1.45, col)
    body_block(x, W - 0.04, y0 + 1.15, y0 + 1.3, zf - 1.45, zf - 0.6, col)
    panel(vector(0, y0 + 1.3, zf - 0.6), vector(0, y0 + 2.0, zf - 1.45), W - 0.08, 0.05,
          CAR_GLASS, x, shininess=1)
    panel(vector(0, y0 + 1.15, zf - 0.25), vector(0, y0 + 1.3, zf - 0.6), W - 0.04, 0.06, col, x)
    body_block(x, W + 0.02, y0 + 1.25, y0 + 1.85, zb - 0.01, zf - 1.5, CAR_GLASS, shininess=1)
    body_block(x, W + 0.03, y0 + 0.5, y0 + 0.54, zb + 0.3, zf - 0.4, CHROME)
    for i in range(4):
        yy = y0 + 0.62 + i * 0.13
        body_block(x, 1.3 - i * 0.05, yy, yy + 0.05, zf - 0.02, zf + 0.04, CHROME)
    body_block(x, 1.32, y0 + 0.58, y0 + 1.15, zf - 0.03, zf + 0.01, FRAME)
    for s in (-1, 1):
        block(x + s * 0.68, x + s * 0.95, y0 + 1.02, y0 + 1.1, zf - 0.08, zf + 0.02, LAMP, emissive=True)
        block(x + s * 0.92, x + s * 0.97, y0 + 0.9, y0 + 1.6, zb - 0.02, zb + 0.02, color.red)
        block(x + s * 1.0, x + s * 1.12, y0 + 1.45, y0 + 1.6, zf - 1.55, zf - 1.4, CHROME)
        for zz in (z - 1.6, z + 1.55):
            wheel(x + s * 0.85, y0 + 0.36, zz, 0.36, 0.24, CHROME, spokes=6)


def car_suv(x, z, y0=0.15):
    col = vector(0.24, 0.20, 0.19)
    W, L = 1.92, 4.9
    zf, zb = z + L / 2, z - L / 2
    body_block(x, W, y0 + 0.4, y0 + 1.05, zb, zf, col)
    body_block(x, W - 0.06, y0 + 1.05, y0 + 1.12, zf - 1.45, zf - 0.03, col)
    body_block(x, W - 0.06, y0 + 1.05, y0 + 1.75, zb + 0.05, zf - 2.2, col)
    panel(vector(0, y0 + 1.12, zf - 1.45), vector(0, y0 + 1.75, zf - 2.2), W - 0.12, 0.05,
          CAR_GLASS, x, shininess=1)
    body_block(x, W - 0.02, y0 + 1.15, y0 + 1.62, zb + 0.08, zf - 2.25, CAR_GLASS, shininess=1)
    for s in (-1, 1):
        block(x + s * 0.62, x + s * 0.7, y0 + 1.75, y0 + 1.82, zb + 0.3, zf - 2.3, CHROME)
    body_block(x, 1.5, y0 + 0.65, y0 + 1.02, zf - 0.02, zf + 0.02, FRAME)
    body_block(x, 1.86, y0 + 0.86, y0 + 0.9, zf, zf + 0.05, CHROME)
    for s in (-1, 1):
        xe = x + s * 0.86
        block(xe - 0.03, xe + 0.03, y0 + 0.72, y0 + 1.0, zf, zf + 0.04, LAMP, emissive=True)
        block(min(xe, xe - s * 0.25), max(xe, xe - s * 0.25), y0 + 0.97, y0 + 1.0, zf, zf + 0.04,
              LAMP, emissive=True)
        block(min(xe, xe - s * 0.25), max(xe, xe - s * 0.25), y0 + 0.72, y0 + 0.75, zf, zf + 0.04,
              LAMP, emissive=True)
        block(x + s * 0.92, x + s * 0.97, y0 + 0.85, y0 + 1.25, zb - 0.02, zb + 0.02, color.red)
        block(x + s * 0.98, x + s * 1.1, y0 + 1.25, y0 + 1.38, zf - 2.15, zf - 2.0, CHROME)
        block(x + s * 0.9, x + s * 1.08, y0 + 0.28, y0 + 0.33, z - 1.0, z + 1.0, FRAME)
        for zz in (z - 1.45, z + 1.45):
            block(x + s * 0.94, x + s * 1.0, y0 + 0.82, y0 + 0.9, zz - 0.5, zz + 0.5, FRAME)
            wheel(x + s * 0.83, y0 + 0.38, zz, 0.38, 0.26, vector(0.55, 0.56, 0.58), spokes=3)
    body_block(x, 1.3, y0 + 0.3, y0 + 0.4, zf - 0.15, zf + 0.03, CHROME)


def car_pickup(x, z, y0=0.15):
    col = vector(0.04, 0.04, 0.05)
    W, L = 2.0, 5.4
    zf, zb = z + L / 2, z - L / 2
    zc = zb + 2.1
    body_block(x, W, y0 + 0.5, y0 + 0.95, zb, zf, col)
    body_block(x, W, y0 + 0.95, y0 + 1.2, zc, zf - 0.03, col)
    body_block(x, W - 0.06, y0 + 1.2, y0 + 1.27, zf - 1.5, zf - 0.03, col)
    body_block(x, W - 0.08, y0 + 1.2, y0 + 1.9, zc, zf - 2.2, col)
    panel(vector(0, y0 + 1.27, zf - 1.5), vector(0, y0 + 1.9, zf - 2.2), W - 0.14, 0.05,
          CAR_GLASS, x, shininess=1)
    body_block(x, W - 0.04, y0 + 1.3, y0 + 1.78, zc + 0.05, zf - 2.25, CAR_GLASS, shininess=1)
    for s in (-1, 1):
        block(x + s * (W / 2 - 0.08), x + s * W / 2, y0 + 0.95, y0 + 1.3, zb, zc, col)
    body_block(x, W, y0 + 0.95, y0 + 1.3, zb, zb + 0.08, col)
    body_block(x, W - 0.16, y0 + 0.95, y0 + 0.97, zb + 0.08, zc, vector(0.15, 0.15, 0.16))
    body_block(x, 1.6, y0 + 0.78, y0 + 1.18, zf - 0.02, zf + 0.02, vector(0.12, 0.12, 0.13))
    for i in range(4):
        yy = y0 + 0.82 + i * 0.09
        body_block(x, 1.5, yy, yy + 0.03, zf + 0.02, zf + 0.04, vector(0.22, 0.22, 0.23))
    body_block(x, 1.7, y0 + 0.48, y0 + 0.6, zf - 0.1, zf + 0.06, vector(0.7, 0.71, 0.73))
    for s in (-1, 1):
        xe = x + s * 0.88
        block(xe - 0.03, xe + 0.03, y0 + 0.86, y0 + 1.16, zf + 0.0, zf + 0.04, LAMP, emissive=True)
        block(min(xe, xe - s * 0.22), max(xe, xe - s * 0.22), y0 + 1.13, y0 + 1.16, zf, zf + 0.04,
              LAMP, emissive=True)
        block(min(xe, xe - s * 0.22), max(xe, xe - s * 0.22), y0 + 0.86, y0 + 0.89, zf, zf + 0.04,
              LAMP, emissive=True)
        block(x + s * 0.94, x + s * 0.99, y0 + 0.95, y0 + 1.25, zb - 0.02, zb + 0.02, color.red)
        block(x + s * 1.02, x + s * 1.14, y0 + 1.38, y0 + 1.52, zf - 2.15, zf - 2.0, col)
        block(x + s * 0.95, x + s * 1.12, y0 + 0.38, y0 + 0.44, zc - 0.1, zf - 1.6, TIRE)
        for zz in (zb + 1.1, zf - 0.95):
            block(x + s * 0.98, x + s * 1.1, y0 + 0.82, y0 + 1.0, zz - 0.6, zz + 0.6,
                  vector(0.13, 0.13, 0.14))
            wheel(x + s * 0.88, y0 + 0.43, zz, 0.43, 0.32, vector(0.2, 0.2, 0.22), spokes=3, rim_r=0.55)


def car_sport(x, z, y0=0.15):
    col = vector(0.64, 0.65, 0.66)
    W, L = 2.0, 4.97
    zf, zb = z + L / 2, z - L / 2
    body_block(x, W, y0 + 0.25, y0 + 0.82, zb, zf, col, shininess=0.05)
    for z1, z2, top in [(zf - 0.7, zf, 0.86), (zf - 1.4, zf - 0.7, 0.93), (zf - 2.0, zf - 1.4, 0.98)]:
        body_block(x, W - 0.04, y0 + 0.82, y0 + top, z1, z2, col, shininess=0.05)
    panel(vector(0, y0 + 0.86, zf - 0.02), vector(0, y0 + 1.0, zf - 2.0), W - 0.06, 0.08, col, x,
          shininess=0.05)
    body_block(x, W - 0.02, y0 + 0.82, y0 + 0.98, zb + 0.05, zf - 2.0, col, shininess=0.05)
    panel(vector(0, y0 + 1.0, zf - 2.0), vector(0, y0 + 1.45, zf - 2.85), W - 0.2, 0.05,
          CAR_GLASS, x, shininess=1)
    body_block(x, W - 0.2, y0 + 1.4, y0 + 1.47, zb + 1.35, zf - 2.85, CAR_GLASS, shininess=1)
    panel(vector(0, y0 + 1.45, zb + 1.35), vector(0, y0 + 0.98, zb + 0.35), W - 0.2, 0.06,
          CAR_GLASS, x, shininess=1)
    body_block(x, W - 0.18, y0 + 0.98, y0 + 1.4, zb + 1.0, zf - 2.2, CAR_GLASS, shininess=1)
    body_block(x, 1.7, y0 + 0.3, y0 + 0.6, zf - 0.02, zf + 0.02, TIRE)
    body_block(x, 1.84, y0 + 0.22, y0 + 0.3, zb + 0.4, zf - 0.4, TIRE)
    for s in (-1, 1):
        block(min(x + s * 0.45, x + s * 0.95), max(x + s * 0.45, x + s * 0.95), y0 + 0.8, y0 + 0.83,
              zf - 0.05, zf + 0.01, LAMP, emissive=True)
        block(min(x + s * 0.5, x + s * 0.95), max(x + s * 0.5, x + s * 0.95), y0 + 0.72, y0 + 0.76,
              zb - 0.02, zb + 0.01, color.red)
        block(x + s * 0.96, x + s * 1.1, y0 + 1.08, y0 + 1.2, zf - 2.2, zf - 2.05, TIRE)
        for zz in (z - 1.5, z + 1.45):
            block(x + s * 0.95, x + s * 1.02, y0 + 0.72, y0 + 0.8, zz - 0.5, zz + 0.5, TIRE)
            wheel(x + s * 0.87, y0 + 0.39, zz, 0.39, 0.28, vector(0.18, 0.18, 0.2), spokes=5, rim_r=0.72)


def palm(x, z, h=6.5, lean=vector(0.12, 0, 0.08)):
    base = vector(x, 0, z)
    p = base
    for i in range(8):
        f = (i + 1) / 8
        nxt = base + vector(0, h * f, 0) + lean * h * f * f
        cylinder(pos=p, axis=nxt - p, radius=0.22 - 0.09 * f, color=TRUNK)
        p = nxt
    for k in range(9):
        ang = 2 * pi * k / 9
        d = norm(vector(cos(ang), -0.35, sin(ang)))
        ellipsoid(pos=p + d * 1.4, axis=d * 2.8, height=0.08, width=0.7, color=LEAF)
    sphere(pos=p, radius=0.3, color=vector(0.35, 0.30, 0.15))


TREE_BARK = vector(0.36, 0.25, 0.16)
TREE_GREENS = (vector(0.14, 0.32, 0.12), vector(0.20, 0.43, 0.17), vector(0.30, 0.53, 0.21))


def leaf_canopy(c, rx, ry, rz, rng, n, greens=TREE_GREENS):
    ellipsoid(pos=c, size=vector(rx * 1.55, ry * 1.25, rz * 1.55), color=greens[0])
    for i in range(n):
        th = rng.uniform(0, 2 * pi)
        u = rng.uniform(-0.45, 1.0)
        rr = max(0.0, 1 - u * u) ** 0.5
        p = c + vector(rx * rr * cos(th) * rng.uniform(0.65, 1.0), ry * u * 0.8,
                       rz * rr * sin(th) * rng.uniform(0.65, 1.0))
        sz = rng.uniform(0.42, 0.62) * (rx + rz) / 2
        col = greens[2] if u > 0.45 else (greens[1] if u > -0.1 else greens[0])
        yaw = rng.uniform(0, pi)
        ellipsoid(pos=p, axis=vector(cos(yaw), 0, sin(yaw)) * sz * rng.uniform(1.2, 1.6),
                  height=sz * rng.uniform(0.6, 0.8), width=sz * rng.uniform(1.0, 1.4), color=col,
                  lowpoly=True)


def round_tree(x, z, h=3.2, r=1.8, n=16, shadow=True):
    rng = Random(int(x * 73 + z * 131 + 7))
    near = n >= 12
    BARK = vector(0.45, 0.29, 0.18)
    BARK_D = vector(0.31, 0.19, 0.11)
    base = vector(x, 0, z)
    tr = 0.13 * r + 0.1
    lean = vector(rng.uniform(-0.06, 0.06), 0, rng.uniform(-0.06, 0.06)) * h
    if shadow:
        cylinder(pos=base + vector(0, 0.004, 0), axis=vector(0, 0.004, 0), radius=r * 1.25,
                 color=vector(0.20, 0.40, 0.17))
        cylinder(pos=base + vector(0, 0.008, 0), axis=vector(0, 0.004, 0), radius=r * 0.8,
                 color=vector(0.16, 0.34, 0.14))
    for k in range(5 if near else 0):
        a = 2 * pi * k / (5 if near else 3) + rng.uniform(-0.3, 0.3)
        d = vector(cos(a), 0, sin(a))
        start = base + d * tr * 0.4 + vector(0, 0.45, 0)
        tip = base + d * tr * rng.uniform(2.4, 3.2) + vector(0, 0.01, 0)
        cone(pos=start, axis=tip - start, radius=tr * 0.42, color=BARK_D)
    pts = [base + vector(0, h * f, 0) + lean * f * f for f in (0, 0.3, 0.55, 0.8, 1.0)]
    if near:
        for i in range(4):
            cylinder(pos=pts[i], axis=pts[i + 1] - pts[i], radius=tr * (1 - 0.12 * i), color=BARK)
            sphere(pos=pts[i + 1], radius=tr * (1 - 0.12 * i), color=BARK)
    else:
        cylinder(pos=pts[0], axis=pts[4] - pts[0], radius=tr * 0.8, color=BARK)
    if near:
        for k in range(4):
            a = 2 * pi * k / 4 + 0.4
            off = vector(cos(a), 0, sin(a)) * tr * 0.93
            cylinder(pos=pts[0] + off + vector(0, 0.3, 0), axis=(pts[3] - pts[0]) * 0.85,
                     radius=tr * 0.12, color=BARK_D)
    for k in range(3 if near else 0):
        a = 2 * pi * k / 3 + rng.uniform(-0.4, 0.4)
        p0 = pts[0] + (pts[4] - pts[0]) * rng.uniform(0.55, 0.7)
        tip = p0 + vector(cos(a) * r * 0.9, h * 0.35, sin(a) * r * 0.9)
        cylinder(pos=p0, axis=tip - p0, radius=tr * 0.38, color=BARK)
    top = pts[4] + vector(0, r * 0.15, 0)
    R, RY = r * 1.35, r * 0.75
    ellipsoid(pos=top, size=vector(2 * R * 0.82, 2 * RY * 0.85, 2 * R * 0.82), color=vector(0.07, 0.30, 0.13))
    tiers = [(-0.50, 1.00, (0.10, 0.40, 0.18)), (-0.12, 0.92, (0.14, 0.50, 0.22)),
             (0.28, 0.72, (0.21, 0.60, 0.27)), (0.62, 0.42, (0.30, 0.69, 0.31))]
    counts = [11, 10, 8, 5] if near else [4, 4, 3, 1]
    for (fy, fr, cc), cnt in zip(tiers, counts):
        a0 = rng.uniform(0, 2 * pi)
        for j in range(cnt):
            a = a0 + 2 * pi * j / cnt + rng.uniform(-0.2, 0.2)
            radial = vector(cos(a), 0, sin(a))
            p = top + radial * R * fr * rng.uniform(0.78, 0.92) + vector(0, RY * fy + rng.uniform(-0.1, 0.1) * r, 0)
            d = R * rng.uniform(0.50, 0.62) * (1 - 0.12 * (fy + 0.5))
            tilt = radians(rng.uniform(15, 35))
            up = norm(vector(0, cos(tilt), 0) + radial * sin(tilt))
            col = vector(*cc) * rng.uniform(0.93, 1.07)
            ellipsoid(pos=p, axis=radial * d, up=up, height=d * 0.36, width=d, color=col, lowpoly=True)
    for j in range(3 if near else 0):
        a = rng.uniform(0, 2 * pi)
        p = top + vector(cos(a) * R * 0.18, RY * 0.92, sin(a) * R * 0.18)
        d = R * 0.5
        ellipsoid(pos=p, size=vector(d, d * 0.34, d), color=vector(0.34, 0.73, 0.34), lowpoly=True)


def leafy_bush(x, z, r=0.5, y=0.0, col=HEDGE, tight=False):
    rng = Random(int(x * 91 + z * 53 + r * 10))
    c = vector(x, y + r * 0.78, z)
    dark, light = col * 0.72, vector(min(1, col.x * 1.45), min(1, col.y * 1.35), min(1, col.z * 1.4))
    ellipsoid(pos=c, size=vector(2 * r * 0.9, 2 * r * 0.78, 2 * r * 0.9), color=dark, lowpoly=True)
    n = 6 if tight else 5
    for k in range(n):
        a = 2 * pi * k / n + rng.uniform(-0.3, 0.3)
        el = rng.uniform(0.05, 0.75)
        d = vector(cos(a) * cos(el), sin(el) * 0.85, sin(a) * cos(el))
        s = r * (rng.uniform(0.52, 0.6) if tight else rng.uniform(0.52, 0.7))
        off = 0.48 if tight else rng.uniform(0.55, 0.7)
        cc = light if el > 0.5 else col
        ellipsoid(pos=c + d * r * off, size=vector(2 * s, 2 * s * 0.85, 2 * s), color=cc * rng.uniform(0.94, 1.06),
                  lowpoly=True)
    ellipsoid(pos=c + vector(0, r * 0.5, 0), size=vector(r * 1.1, r * 0.8, r * 1.1), color=light, lowpoly=True)


def shrub(x, z, r=0.5, y=0.0):
    leafy_bush(x, z, r, y, HEDGE)


def potted_plant(x, y, z, s=1.0):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.7 * s, 0), radius=0.28 * s,
             color=vector(0.30, 0.30, 0.30))
    for k in range(7):
        ang = 2 * pi * k / 7
        d = norm(vector(0.45 * cos(ang), 1, 0.45 * sin(ang)))
        ellipsoid(pos=vector(x, y + 0.7 * s, z) + d * 0.6 * s, axis=d * 1.2 * s,
                  up=vector(-sin(ang), 0, cos(ang)), height=0.25 * s, width=0.05, color=LEAF,
                  lowpoly=True)


def lounger(x, z, y=0.36):
    block(x, x + 1.9, y, y + 0.14, z - 0.35, z + 0.35, FRAME)
    block(x + 0.3, x + 1.9, y + 0.14, y + 0.26, z - 0.33, z + 0.33, color.white)
    a = radians(35)
    u = vector(-sin(a), cos(a), 0)
    box(pos=vector(x + 0.32, y + 0.26, z) + u * 0.4, axis=vector(0, 0, 0.66), up=u,
        height=0.8, width=0.1, color=color.white)


def rect_minus(rects, holes):
    out = []
    for (x1, x2, z1, z2) in rects:
        xs = sorted({x1, x2} | {v for h in holes for v in (h[0], h[1]) if x1 < v < x2})
        for xa, xb in zip(xs[:-1], xs[1:]):
            cuts = sorted((max(h[2], z1), min(h[3], z2)) for h in holes
                          if h[0] <= xa + 1e-6 and h[1] >= xb - 1e-6 and h[2] < z2 and h[3] > z1)
            z = z1
            for c1, c2 in cuts + [(z2, z2)]:
                if c1 - z > 0.005:
                    out.append((xa, xb, z, c1))
                z = max(z, c2)
    return out


def cloud(x, y, z, s=1.0):
    for dx, dy, dz, r in [(0, 0, 0, 3.0), (2.8, -0.5, 0.6, 2.3), (-2.8, -0.6, -0.4, 2.2), (1.2, 1.1, -0.3, 2.1),
                          (-1.3, 0.9, 0.5, 2.0), (0.2, -0.9, 0.0, 3.4)]:
        CLOUDS.append(ellipsoid(pos=vector(x + dx * s, y + dy * s, z + dz * s),
                                size=vector(2 * r * s, 1.3 * r * s, 1.7 * r * s), color=color.white))


SKY_R = 200
SKY_CENTER = vector(0, 0, -5)
SKY_RINGS = [-8, 0, 6, 14, 26, 42, 62, 90]
SKY_SEG = 20
SKY_STOPS = {
    "Day": [(-10, vector(0.80, 0.88, 0.95)), (0, vector(0.86, 0.92, 0.98)), (15, vector(0.62, 0.79, 0.96)),
            (45, vector(0.42, 0.65, 0.93)), (90, vector(0.27, 0.50, 0.88))],
    "Sunset": [(-10, vector(0.95, 0.62, 0.42)), (0, vector(1.00, 0.72, 0.42)), (12, vector(0.98, 0.55, 0.42)),
               (35, vector(0.68, 0.42, 0.55)), (90, vector(0.22, 0.24, 0.48))],
    "Night": [(-10, vector(0.05, 0.06, 0.12)), (0, vector(0.08, 0.10, 0.20)), (15, vector(0.04, 0.06, 0.15)),
              (45, vector(0.02, 0.03, 0.09)), (90, vector(0.01, 0.015, 0.05))],
}


def sky_color(el, name):
    stops = SKY_STOPS[name]
    if el <= stops[0][0]:
        return stops[0][1]
    for (e1, c1), (e2, c2) in zip(stops[:-1], stops[1:]):
        if e1 <= el <= e2:
            f = (el - e1) / (e2 - e1)
            return c1 + (c2 - c1) * f
    return stops[-1][1]


SKY_VERTS = []
_grid = []
for el in SKY_RINGS:
    row = []
    for j in range(SKY_SEG):
        az = 2 * pi * j / SKY_SEG
        e = radians(el)
        p = SKY_CENTER + vector(SKY_R * cos(e) * cos(az), SKY_R * sin(e), SKY_R * cos(e) * sin(az))
        v = vertex(pos=p, normal=norm(SKY_CENTER - p), color=sky_color(el, "Day"), emissive=True)
        row.append(v)
        SKY_VERTS.append((v, el))
    _grid.append(row)


def _sky_tri(a, b, c):
    n = cross(b.pos - a.pos, c.pos - a.pos)
    if mag(n) < 1e-6:
        return
    if dot(n, SKY_CENTER - a.pos) < 0:
        b, c = c, b
    triangle(v0=a, v1=b, v2=c)


for i in range(len(SKY_RINGS) - 1):
    for j in range(SKY_SEG):
        a, b = _grid[i][j], _grid[i][(j + 1) % SKY_SEG]
        c, d = _grid[i + 1][(j + 1) % SKY_SEG], _grid[i + 1][j]
        _sky_tri(a, b, c)
        _sky_tri(a, c, d)

sun = sphere(pos=vector(45, 50, -90), radius=5, color=vector(1, 0.95, 0.6), emissive=True)
sun_halo = sphere(pos=sun.pos, radius=13, color=vector(1, 0.92, 0.65), opacity=0.18, emissive=True)
for (cx, cy, cz, cs) in [(-35, 30, -75, 1.4), (5, 36, -95, 1.8), (40, 28, -70, 1.2), (-80, 34, -20, 1.6),
                         (85, 32, -10, 1.5), (-60, 40, 60, 1.7), (30, 38, 90, 1.6), (90, 30, 55, 1.2),
                         (-20, 45, 95, 1.3), (-95, 28, -70, 1.3), (65, 44, -60, 1.0), (0, 48, 40, 1.1)]:
    cloud(cx, cy, cz, cs)
CLOUDS[:] = [_vp_compound(CLOUDS)]

cylinder(pos=vector(0, -0.25, -5), axis=vector(0, 0.1, 0), radius=195, color=vector(0.30, 0.48, 0.24))
block(-45, 45, -0.1, 0.0, -45, 12.6, GRASS)
block(-195, 195, -0.1, 0.0, 12.6, 30, STREET)
block(-195, 195, 0.0, 0.08, 11.0, 12.6, CONCRETE, solid=True)
block(-195, 195, 0.0, 0.08, 30.0, 31.6, CONCRETE)
for zc in (12.6, 30.0):
    block(-195, 195, 0.0, 0.12, zc - 0.08, zc + 0.08, vector(0.80, 0.80, 0.78))
for x in range(-190, 190, 8):
    block(x, x + 3, 0.0, 0.02, 20.2, 20.4, color.white)

for k in range(14):
    a = 2 * pi * k / 14 + 0.2
    r = 150 + 15 * sin(3 * k)
    ellipsoid(pos=vector(r * cos(a), -4, r * sin(a) - 5), size=vector(70 + 20 * sin(k), 34 + 12 * cos(2 * k), 55),
              color=vector(0.40, 0.55, 0.50))
for k in range(40):
    a = 2 * pi * k / 40
    r = 92 + 12 * sin(5 * k)
    p = vector(r * cos(a), 0, r * sin(a) - 5)
    if abs(p.x) < 60 and -50 < p.z < 50:
        continue
    round_tree(p.x, p.z, 5.5 + sin(k), 4.4, n=9, shadow=False)

STREET_NIGHT = []


def street_lamp(x, z, facing):
    cylinder(pos=vector(x, 0.08, z), axis=vector(0, 4.2, 0), radius=0.07, color=METAL)
    block(x - 0.05, x + 0.05, 4.2, 4.3, min(z, z + facing * 0.45), max(z, z + facing * 0.45), METAL)
    block(x - 0.15, x + 0.15, 4.1, 4.2, z + facing * 0.35 - 0.1, z + facing * 0.35 + 0.1, LAMP, emissive=True)
    STREET_NIGHT.append(cone(pos=vector(x, 0.09, z + facing * 0.35), axis=vector(0, 4.0, 0), radius=1.7,
                             color=vector(1.0, 0.80, 0.52), opacity=0.06, emissive=True, visible=False))


for x in (-55, -33, -11, 11, 33, 55):
    round_tree(x, 30.9, 3.6, 1.8, shadow=False)
for x in (-44, -22, 0, 22, 44):
    street_lamp(x, 30.6, -1)
street_lamp(-12.4, 12.3, 1)
for (x, z) in [(-34, -16), (-33, 2), (22, -19), (23, 6), (-12, -30), (14, -30)]:
    round_tree(x, z, 3.5, 1.9)

FZ = 11.0
FH = 2.1
for x1, x2 in [(-28, -26.5), (-13.5, 3), (4.6, 18)]:
    block(x1, x2, 0, 0.45, FZ - 0.2, FZ + 0.2, PLINTH, solid=True)
    block(x1, x2, 0.45, FH, FZ - 0.12, FZ + 0.12, FENCE_GRAY, solid=True)
    block(x1, x2, FH, FH + 0.08, FZ - 0.18, FZ + 0.18, PLINTH)
    block(x1 + 0.2, x2 - 0.2, 0.08, 0.82, 11.38, 11.92, HEDGE * 0.8)
    xh = x1 + 0.45
    while xh < x2 - 0.3:
        k = int(xh * 3)
        ellipsoid(pos=vector(xh, 0.82, 11.65), size=vector(0.62, 0.36, 0.66),
                  color=HEDGE * (1.25 if k % 2 else 1.1), lowpoly=True)
        ellipsoid(pos=vector(xh + 0.2, 0.5, 11.93), size=vector(0.5, 0.55, 0.16),
                  color=HEDGE * (1.0 if k % 3 else 1.12), lowpoly=True)
        xh += 0.42


def framed_panel(x1, x2, y1, y2):
    block(x1, x2, y1, y2, FZ + 0.12, FZ + 0.15, vector(0.80, 0.80, 0.78))
    block(x1 + 0.06, x2 - 0.06, y1 + 0.06, y2 - 0.06, FZ + 0.15, FZ + 0.18, WOOD)


framed_panel(-12.8, 2.3, 0.6, 1.95)
framed_panel(12.6, 17.4, 0.6, 1.95)
xs = 5.2
while xs < 12.2:
    block(xs, xs + 0.09, 0.5, FH - 0.05, FZ + 0.12, FZ + 0.2, ROOF)
    xs += 0.15
for i in range(4):
    gx = -26.5 + i * 3.25
    block(gx, gx + 0.25, 0, FH + 0.1, FZ - 0.15, FZ + 0.15, FENCE_GRAY)
    block(gx + 0.25, gx + 3.25, 0.1, FH, FZ - 0.05, FZ + 0.05, WOOD)
    for k in range(1, 6):
        gz = gx + 0.25 + k * 0.5
        block(gz - 0.012, gz + 0.012, 0.1, FH, FZ + 0.05, FZ + 0.06, vector(0.38, 0.22, 0.11))
block(-13.75, -13.5, 0, FH + 0.1, FZ - 0.15, FZ + 0.15, FENCE_GRAY)
add_solid(-26.5, -13.5, 0, FH, FZ - 0.1, FZ + 0.1)
block(4.7, 6.3, 0.1, FH, FZ - 0.35, FZ - 0.25, WOOD)
cylinder(pos=vector(16.8, 0.08, 12.0), axis=vector(0, 4.2, 0), radius=0.07, color=METAL)
block(16.4, 16.85, 4.2, 4.3, 11.95, 12.05, METAL)
block(16.3, 16.6, 4.1, 4.2, 11.9, 12.1, LAMP, emissive=True)

GATE_LAMPS = []
FENCE_NIGHT = []
LANTERN_OFF = vector(0.90, 0.90, 0.87)


def post_lantern(x, y, z, s=0.14):
    block(x - s, x + s, y, y + 0.04, z - s, z + s, FRAME)
    GATE_LAMPS.append(block(x - s + 0.03, x + s - 0.03, y + 0.04, y + 0.34, z - s + 0.03, z + s - 0.03,
                            LANTERN_OFF))
    for dx in (-1, 1):
        for dz in (-1, 1):
            block(x + dx * (s - 0.015) - 0.015, x + dx * (s - 0.015) + 0.015, y + 0.04, y + 0.34,
                  z + dz * (s - 0.015) - 0.015, z + dz * (s - 0.015) + 0.015, FRAME)
    block(x - s - 0.02, x + s + 0.02, y + 0.34, y + 0.4, z - s - 0.02, z + s + 0.02, FRAME)


def wall_sconce(x, y, z):
    block(x - 0.1, x + 0.1, y - 0.2, y + 0.2, z, z + 0.08, FRAME)
    GATE_LAMPS.append(block(x - 0.07, x + 0.07, y - 0.17, y + 0.17, z + 0.08, z + 0.1, LANTERN_OFF))
    for sgn in (1, -1):
        FENCE_NIGHT.append(cone(pos=vector(x, y + sgn * 0.75, z + 0.12), axis=vector(0, -sgn * 0.6, 0),
                                radius=0.32, color=vector(1.0, 0.80, 0.52), opacity=0.08, emissive=True,
                                visible=False))


for i in range(4):
    post_lantern(-26.5 + i * 3.25 + 0.125, FH + 0.1, FZ)
post_lantern(-13.625, FH + 0.1, FZ)
post_lantern(-27.25, FH + 0.08, FZ)
post_lantern(17.7, FH + 0.08, FZ)
for x in (2.75, 4.85):
    wall_sconce(x, 1.35, FZ + 0.12)
for x1, x2 in [(-28, -26.5), (-13.5, 3), (4.6, 18)]:
    FENCE_NIGHT.append(block(x1 + 0.05, x2 - 0.05, FH - 0.07, FH - 0.03, FZ + 0.12, FZ + 0.15, LAMP,
                             emissive=True, visible=False))
FENCE_NIGHT.append(block(-26.5, -13.5, FH - 0.04, FH - 0.0, FZ + 0.05, FZ + 0.08, LAMP, emissive=True,
                         visible=False))
for x in (-24.9, -21.6, -18.4, -15.1, -11.0, -7.0, -3.0, 1.0, 7.0, 10.0, 13.5, 16.5):
    FENCE_NIGHT.append(cone(pos=vector(x, FH, FZ + 0.32), axis=vector(0, -FH + 0.05, 0), radius=0.7,
                            color=vector(1.0, 0.80, 0.52), opacity=0.06, emissive=True, visible=False))


def slats_x(z1, z2, x1, x2, y1, y2, size=0.12, gap=0.04, col=WOOD):
    y = y1
    while y + size <= y2 + 1e-6:
        block(x1, x2, y, y + size, z1, z2, col)
        y += size + gap


for xf in (-28.0, 18.0):
    block(xf - 0.15, xf + 0.15, 0, 2.6, -22, 4, DARK_STONE, solid=True)
    block(xf - 0.15, xf + 0.15, 0, 2.1, 4, FZ, DARK_STONE, solid=True)
    block(xf - 0.2, xf + 0.2, 2.6, 2.66, -22, 4, PLINTH)
for x in range(-27, 19, 3):
    block(x - 0.08, x + 0.08, 0, 2.6, -22.1, -21.9, FRAME)
slats_x(-22.08, -22.0, -28, 18, 0.1, 2.6, 0.16, 0.06, vector(0.56, 0.35, 0.21))
block(-28, 18, 0, 2.62, -22.22, -22.08, vector(0.36, 0.24, 0.15))
block(-28.05, 18.05, 2.62, 2.68, -22.24, -21.96, vector(0.30, 0.20, 0.12))
add_solid(-28, 18, 0, 2.6, -22.22, -21.9)

for i in range(12):
    for j in range(7):
        x, z = -26 + i, 4.5 + j
        block(x, x + 1, 0, 0.03, z, min(z + 1, 10.85), PAVER_1 if (i + j) % 2 == 0 else PAVER_2)
block(-26.5, -13.5, 0.0, 0.085, 11.0, 12.6, PAVER_2)
for k in range(6):
    z = 6.3 + k * 0.75
    block(3.2, 4.4, 0, 0.05, z, z + 0.55, PAVER_2)
block(10.6, 17.8, 0, 0.03, -14, 4, GRAVEL)
z = 3.2
while z > -13.5:
    block(13.2, 14.8, 0.03, 0.07, z - 0.7, z, PAVER_2)
    z -= 1.25
for z in (2.5, -2.0, -6.5, -11.0):
    potted_plant(11.0, 0.03, z, 0.9)

BUILD_START = len(ALL_OBJ)

block(-26, -14, 0, 0.15, -3, 4.5, EPOXY, solid=True)
wall("x", 4.4, -26, -14, 0.15, 3.9,
     [(-25.6, -20.4, 0.15, 3.0, "open"), (-19.6, -14.4, 0.15, 3.0, "open")], col=DARK_STONE)
wall("z", -25.9, -3, 4.5, 0.15, 3.9, [(-0.5, 2.5, 1.6, 3.0, "win")], skin=(-1, EXT))
wall("x", -2.9, -26, -14, 0.15, 3.9, [(-24.5, -21.5, 1.8, 3.2, "win"), (-17.2, -16.2, 0.15, 2.6, "door")],
     skin=(-1, EXT))
block(-14.0, -13.8, 0.15, 3.9, 4.0, 4.5, EXT, solid=True)
add_solid(-26, -14, 3.9, F1, -3, 4.5)
block(-26, -14, 3.9, F1 - 0.03, -3, 4.5, CEILING)
block(-26, -14, F1 - 0.03, F1, -3, 4.5, DECK_TILE)
add_solid(-26.3, -13.8, 3.55, F1, 4.5, 6.2)
block(-26.3, -13.8, 3.55, F1 - 0.03, 4.5, 6.2, color.white)
block(-26.3, -13.8, F1 - 0.03, F1, 4.5, 6.2, DECK_TILE)
block(-26.3, -13.8, 3.53, 3.55, 4.5, 6.1, SOFFIT)
for xl in (-24, -21, -18, -15.5):
    downlight(xl, 3.53, 5.4)
rail("x", 6.16, -26.3, -13.8, F1)
rail("z", -26.26, -3, 6.2, F1)
rail("x", -2.96, -26, -14, F1)
rail("z", -13.84, 4.0, 6.2, F1)

car_van(-24.4, 0.9)
car_suv(-21.6, 1.1)
car_pickup(-18.4, 0.85)
car_sport(-15.6, 1.1)
for x in (-24.4, -21.6, -18.4, -15.6):
    block(x - 0.08, x + 0.08, 3.8, 3.85, -1.5, 3.5, LAMP, emissive=True)
block(-25.75, -22.8, 0.15, 2.4, -2.8, -2.35, CABINET)
for y in (0.8, 1.5, 2.2):
    block(-25.75, -22.8, y, y + 0.03, -2.8, -2.3, METAL)

garage = {"open": False, "angle": 0.0, "doors": []}
GARAGE_DOOR_SOLIDS = []
for x1, x2 in [(-25.6, -20.4), (-19.6, -14.4)]:
    parts = [box(pos=vector((x1 + x2) / 2, 1.575, 4.4), size=vector(x2 - x1, 2.85, 0.08), color=WOOD)]
    y = 0.35
    while y < 3.0:
        parts.append(box(pos=vector((x1 + x2) / 2, y, 4.445), size=vector(x2 - x1, 0.03, 0.01),
                         color=vector(0.35, 0.20, 0.10)))
        y += 0.3
    garage["doors"].append(compound(parts))
    GARAGE_DOOR_SOLIDS.append((x1, x2, 0.15, 3.0, 4.3, 4.5))

block(-14, 10.3, 0, F0, -6.3, 4.3, PLINTH, solid=True)
block(-14.3, -14, 0, F0, -6.3, -3, PLINTH, solid=True)
block(-14, 10, F0, F0 + 0.01, -6, 4, TILE_FLOOR)

wall("x", 3.9, -14, 10, F0, 3.95,
     [(-13, -8, 1.1, 3.5, "win"), (-6.6, 0.6, 0.55, 3.7, "glass"), (3.1, 4.5, F0, 3.5, "door"),
      (4.6, 5.0, 0.55, 3.5, "glass"), (6.6, 9.4, 1.1, 3.5, "win")], skin=(1, EXT))
wall("z", -13.9, -6, 4, F0, 3.95, [(-4.9, -3.9, F0, 2.9, "door"), (1, 2, F0, 2.9, "door")],
     skin=(-1, EXT))
wall("z", 9.9, -6, 4, F0, 3.95, [(-5, -2, 1.6, 3.3, "win"), (0, 3, 1.1, 3.5, "win")], skin=(1, EXT))
wall("x", -5.9, -14, 2, F0, 3.95, [(-9.0, -7.4, 1.6, 3.4, "win"), (-3.6, -1.6, 2.5, 3.6, "win")],
     skin=(-1, EXT))
wall("x", -5.9, 2, 10, F0, 3.95, [(3, 5.5, F0, 3.0, "door")])

T = 0.12
wall("z", -7, -1, 4, F0, 3.95, [(-0.8, 1.0, F0, 2.9, "open"), (1.2, 3.8, 0.6, 3.8, "glass")], t=T)
wall("x", -1, -14, -6, F0, 3.95, [(-11, -8.6, F0, 2.9, "open")], t=T)
wall("z", -6, -6, -1, F0, 3.95, [(-3.2, -1.6, F0, 2.9, "open")], t=T)
wall("z", 2, -1, 4, F0, 3.95, [(0.8, 2.6, F0, 3.0, "open")], t=T)
wall("z", 6, -1, 4, F0, 3.95, [(0.2, 1.2, F0, 2.9, "door")], t=T)
wall("x", -1, 6, 10, F0, 3.95, [], t=T)
wall("z", 6, -6, -1, F0, 3.95, [(-3.2, -2.3, F0, 2.9, "door")], t=T)

block(1.0, 1.8, F0, 3.95, 4.04, 4.34, DARK_STONE)
block(5.3, 6.0, F0, 3.95, 4.04, 4.34, DARK_STONE)
xs = 2.0
while xs + 0.09 <= 2.95:
    block(xs, xs + 0.09, F0, 3.9, 4.04, 4.19, WOOD)
    xs += 0.14
block(2.2, 5.6, 0, F0, 4.0, 5.0, color.white, solid=True)
block(2.2, 5.6, 0, 0.333, 5.0, 5.5, color.white, solid=True)
block(2.2, 5.6, 0, 0.167, 5.5, 6.0, color.white, solid=True)
potted_plant(2.55, F0, 4.6, 1.2)
potted_plant(5.25, F0, 4.6, 1.2)
block(4.42, 4.5, F0, 3.5, 2.4, 3.8, WOOD, solid=True)
block(4.36, 4.42, 1.6, 2.4, 2.6, 2.66, METAL)
block(2, 10, 3.9, 3.95, 4.0, 5.4, SOFFIT)

block(-5.8, 0.2, F0 + 0.01, F0 + 0.02, 0.2, 3.3, vector(0.88, 0.86, 0.82))
sofa(-5.6, -0.2, 2.6, 3.4, F0, "+z", ends=("back", "arm"),
     pillows=[P_CREAM, P_COCOA, P_SAND, P_CREAM])
sofa(-5.6, -4.7, 0.6, 2.6, F0, "-x", ends=("arm", None), pillows=[P_SAND])
for cx, cz, r, h in [(-3.3, 1.55, 0.55, 0.4), (-2.2, 1.75, 0.4, 0.32)]:
    cylinder(pos=vector(cx, F0, cz), axis=vector(0, h - 0.04, 0), radius=r * 0.6, color=FRAME)
    cylinder(pos=vector(cx, F0 + h - 0.04, cz), axis=vector(0, 0.04, 0), radius=r, color=MARBLE)
armchair(0.65, 1.05, "+x", F0, vector(0.72, 0.52, 0.34), P_CREAM)
cylinder(pos=vector(1.4, F0, 3.4), axis=vector(0, 1.5, 0), radius=0.02, color=FRAME)
cylinder(pos=vector(1.4, 1.95, 3.4), axis=vector(0, 0.35, 0), radius=0.22, color=FRAME)
wall("z", 1.91, -1, 4, F0, 3.95, [(0.8, 2.6, F0, 3.0, "none")], t=0.06, col=WOOD, solid=False)
block(-7, 2, 7.25, 7.3, -1, 4, CEILING)
block(-6, 1, 7.17, 7.25, -0.2, 3.2, WOOD)
block(-4.6, -0.4, 7.12, 7.17, 0.6, 2.4, CEILING)
as_group(spiral_chandelier, -2.5, 7.12, 1.5, y_bottom=2.9)
for x in (-6.4, 1.4):
    for z in (-0.5, 1.5, 3.5):
        downlight(x, 7.25, z)

block(-11.3, -9.7, 1.22, 1.3, 0.1, 3.1, LIVE_EDGE)
for zz in (0.4, 2.8):
    block(-10.9, -10.1, F0, 1.22, zz - 0.08, zz + 0.08, vector(0.35, 0.22, 0.12))
for zz in (0.5, 1.2, 2.0, 2.7):
    chair(-11.65, zz, "+x", F0)
    chair(-9.35, zz, "-x", F0)
chair(-10.5, -0.35, "+z", F0)
chair(-10.5, 3.45, "-z", F0)
as_group(branch_chandelier, -10.5, 3.95, 1.6)

add_solid(-13.85, -7.15, 0, 1.43, -5.8, -5.17)
block(-13.8, -7.2, F0, F0 + 0.1, -5.75, -5.3, FRAME)
cabinet_run_x(-13.8, -11.8, F0 + 0.1, 1.38, -5.22, 0.58)
cabinet_run_x(-10.8, -7.2, F0 + 0.1, 1.38, -5.22, 0.58)
block(-11.8, -10.8, F0 + 0.1, 1.38, -5.8, -5.21, STEEL, shininess=1)
block(-11.66, -10.94, 0.72, 1.12, -5.21, -5.205, vector(0.08, 0.08, 0.09), shininess=1)
block(-11.66, -10.94, 1.2, 1.22, -5.205, -5.17, STEEL)
block(-11.75, -10.85, 0.66, 0.67, -5.21, -5.205, vector(0.4, 0.4, 0.42))
marble(-13.85, -7.15, 1.38, 1.43, -5.8, -5.17, ("top",), seed=3)
marble(-13.8, -7.2, 1.43, 2.25, -5.8, -5.775, ("front",), seed=4)
kitchen_sink(-8.6, -7.8, 1.43, -5.7, -5.32)
faucet(-8.2, 1.43, -5.72, "+z")
cooktop(-11.8, -10.8, 1.43, -5.7, -5.27)
block(-11.9, -10.7, 2.5, 2.75, -5.8, -5.15, STEEL, shininess=1)
block(-11.5, -11.1, 2.75, 3.95, -5.8, -5.5, STEEL, shininess=1)
block(-11.75, -10.85, 2.495, 2.5, -5.7, -5.3, LAMP, emissive=True)
block(-13.8, -12.2, 2.25, 3.6, -5.8, -5.45, KWOOD)
block(-13.72, -12.28, 2.33, 3.52, -5.462, -5.455, vector(0.85, 0.80, 0.70))
for ys in (2.75, 3.15):
    block(-13.72, -12.28, ys, ys + 0.02, -5.78, -5.47, KWOOD * 1.25)
    for xc in (-13.5, -13.25, -13.0, -12.75, -12.5):
        cylinder(pos=vector(xc, ys + 0.02, -5.62), axis=vector(0, 0.12, 0), radius=0.05, color=color.white)
block(-13.7, -12.3, 2.33, 3.52, -5.45, -5.43, GLASS, opacity=0.5)
cabinet_run_x(-10.6, -7.2, 2.25, 3.6, -5.45, 0.35, drawers=False)
for (x1, x2) in [(-13.75, -12.25), (-10.55, -7.25)]:
    block(x1, x2, 2.235, 2.25, -5.75, -5.5, LAMP, emissive=True)
block(-11.9, -10.7, 2.25, 2.5, -5.8, -5.775, MARBLE_W)
block(-7.0, -6.15, F0, 2.6, -5.8, -5.0, STEEL, shininess=1)
block(-6.581, -6.569, F0 + 0.05, 2.55, -5.0, -4.996, vector(0.3, 0.3, 0.32))
for xh in (-6.64, -6.51):
    block(xh - 0.012, xh + 0.012, 1.2, 2.2, -4.996, -4.95, vector(0.62, 0.63, 0.65))
add_solid(-12.1, -8.5, 0, 1.43, -3.8, -2.6)
marble(-12.1, -8.5, 1.37, 1.43, -3.8, -2.6, ("top",), seed=5)
marble(-12.1, -12.04, F0, 1.37, -3.8, -2.6, ("left",), seed=6)
marble(-8.56, -8.5, F0, 1.37, -3.8, -2.6, ("right",), seed=7)
block(-12.04, -8.56, F0, F0 + 0.1, -3.62, -2.85, FRAME)
block(-12.04, -8.56, F0 + 0.1, 1.37, -3.7, -2.75, KWOOD)
for i in range(1, 5):
    xg = -12.04 + i * (3.48 / 5)
    block(xg - 0.005, xg + 0.005, F0 + 0.12, 1.35, -3.704, -3.7, KGAP)
for i in range(5):
    xc = -12.04 + (i + 0.5) * (3.48 / 5)
    block(xc - 0.2, xc + 0.2, 1.24, 1.256, -3.725, -3.704, STEEL)
for x in (-12.5, -10.3, -8.0):
    downlight(x, 3.95, -3.2)

stairs(0.1, -5.6, -5.8, -4.15, F0, F1, rail_z=-4.15, flare=0.4, step_lights=True)
block(-5.6, 0.1, 1.0, 1.03, -5.8, -5.78, LAMP, emissive=True)
potted_plant(1.4, F0, -5.3, 1.1)

block(5.55, 5.92, F0, 1.35, 2.0, 3.5, WOOD)
block(5.92, 5.94, 1.6, 2.8, 2.2, 3.3, MIRROR, shininess=1)
as_group(ring_chandelier, 4.0, 3.9, 1.5)

bed(7.0, 9.0, -0.8, 1.3, F0, "-z", WOOD, color.white, vector(0.16, 0.22, 0.36),
    headboard=vector(0.70, 0.62, 0.52), accent=vector(0.86, 0.80, 0.70))
block(6.9, 9.1, F0, 1.25, 3.2, 3.75, WOOD)
chair(8.0, 2.8, "+z", F0, FRAME, FRAME)
as_group(crystal_flush, 8.0, 3.95, 1.5, 0.28, 0.45)

tiled(6.1, 9.8, F0 + 0.005, F0 + 0.02, -5.8, -1.06, vector(0.82, 0.80, 0.76))
marble(6.6, 9.4, F0, 3.9, -1.08, -1.06, ("back",), seed=31)
vanity(7.0, 8.9, -1.6, -1.08, F0, "-z", sinks=[7.95])
lit_mirror(vector(7.95, F0 + 1.75, -1.11), 1.0, 1.1, "-z")
toilet(6.75, -5.42, "+z", F0)
tp_holder(vector(6.06, F0 + 0.7, -4.95), "+x")
tiled(9.76, 9.8, F0, 1.55, -5.8, -4.2)
tiled(8.6, 9.8, F0, 3.9, -5.8, -5.76)
tiled(8.6, 9.8, F0 + 0.02, F0 + 0.035, -5.8, -4.2, vector(0.42, 0.41, 0.40), step=0.3)
glass_screen(8.58, 8.62, F0, F0 + 2.1, -5.8, -4.2)
glass_screen(9.2, 9.8, F0, F0 + 2.1, -4.22, -4.18)
shower_set(vector(9.2, 3.55, -5.0), vector(9.78, F0 + 1.1, -5.3), "-x")
block(8.9, 9.5, F0 + 1.1, F0 + 1.4, -5.76, -5.7, vector(0.16, 0.16, 0.16))
for (bx, bc) in [(9.05, vector(0.9, 0.88, 0.82)), (9.2, vector(0.3, 0.32, 0.3))]:
    cylinder(pos=vector(bx, F0 + 1.1, -5.73), axis=vector(0, 0.2, 0), radius=0.03, color=bc)
block(8.7, 9.7, F0 + 0.036, F0 + 0.04, -5.72, -5.68, CHROME)
block(8.65, 9.25, F0 + 0.02, F0 + 0.035, -4.1, -3.6, vector(0.92, 0.90, 0.86))
towel_bar(vector(9.8, F0 + 1.0, -3.7), vector(9.8, F0 + 1.0, -2.9), face="-x")
for (dx, dz) in [(7.9, -3.4), (7.9, -1.9)]:
    downlight(dx, 3.95, dz)
yb = 1.62
while yb < 3.3:
    block(9.72, 9.78, yb, yb + 0.06, -5, -2, WOOD)
    yb += 0.1

block(1.7, 10.3, 0, F0, -14.3, -6, PLINTH, solid=True)
block(2, 10, F0, F0 + 0.01, -14, -6, TILE_FLOOR)
wall("x", -13.9, 2, 10, F0, 3.95,
     [(2.6, 4.0, 0.55, 3.4, "glass"), (4.2, 7.8, F0, 3.4, "open"), (8.0, 9.4, 0.55, 3.4, "glass")])
wall("z", 2.1, -14, -6.6, F0, 3.95, [(-10, -7.2, 1.1, 3.4, "win")])
block(2.0, 2.2, F0, 3.95, -6.6, -6, WHITE_WALL, solid=True)
wall("z", 9.9, -14, -6.6, F0, 3.95, [(-12.5, -10.5, 2.0, 3.4, "win")])
block(9.8, 10.0, F0, 3.95, -6.6, -6, WHITE_WALL, solid=True)
block(2.2, 2.65, F0, 1.0, -13.4, -10.6, CABINET)
block(2.2, 2.28, 1.4, 2.5, -12.9, -11.1, FRAME)
block(2.2, 2.6, F0, 3.4, -13.8, -13.4, CABINET)
block(2.2, 2.6, F0, 3.4, -10.6, -10.2, CABINET)
sofa(4.6, 5.6, -13.4, -10.4, F0, "+x", SOFA_DARK, ends=("back", "arm"),
     pillows=[P_CARAMEL, P_CREAM, P_SAND])
sofa(3.4, 4.6, -13.6, -12.8, F0, "-z", SOFA_DARK, ends=("arm", None))
block(3.2, 4.1, F0, 0.9, -12.4, -11.2, MARBLE)
add_solid(9.15, 9.8, 0, 1.44, -13.8, -7.6)
block(9.26, 9.8, F0, F0 + 0.1, -13.8, -7.6, FRAME)
cabinet_run_z(9.2, 0.6, F0 + 0.1, 1.38, -13.8, -7.6)
marble(9.15, 9.8, 1.38, 1.44, -13.8, -7.6, ("top",), seed=8)
marble(9.77, 9.8, 1.44, 2.4, -13.8, -7.6, ("left",), seed=9)
kitchen_sink(9.3, 9.7, 1.44, -9.25, -8.45)
faucet(9.72, 1.44, -8.85, "-x")
cooktop(9.25, 9.72, 1.44, -12.45, -11.55)
block(9.3, 9.8, 2.45, 2.62, -12.55, -11.45, STEEL, shininess=1)
block(9.56, 9.8, 2.62, 3.95, -12.2, -11.8, STEEL, shininess=1)
block(9.35, 9.75, 2.445, 2.45, -12.4, -11.6, LAMP, emissive=True)
block(9.0, 9.8, F0, 2.7, -7.5, -6.1, STEEL, shininess=1)
block(8.996, 9.0, F0 + 0.05, 2.65, -6.806, -6.794, vector(0.3, 0.3, 0.32))
for zh in (-6.87, -6.73):
    block(8.95, 8.996, 1.2, 2.2, zh - 0.012, zh + 0.012, vector(0.62, 0.63, 0.65))
cabinet_run_z(9.45, 0.35, 2.4, 3.4, -9.8, -7.6, drawers=False)
block(9.47, 9.75, 2.385, 2.4, -9.75, -7.65, LAMP, emissive=True)
add_solid(6.7, 8.7, 0, 1.42, -10.1, -7.7)
marble(6.7, 8.7, 1.35, 1.42, -10.1, -7.7, ("top",), seed=10)
marble(6.7, 8.7, F0, 1.35, -10.1, -10.04, ("back",), seed=11)
marble(6.7, 8.7, F0, 1.35, -7.76, -7.7, ("front",), seed=12)
block(6.8, 8.6, F0, 1.35, -10.04, -7.76, KWOOD)
for zz in (-9.5, -8.9, -8.3):
    bar_stool(6.3, zz, F0)
for zz in (-9.5, -8.3):
    pendant(7.7, 3.95, 3.2, zz, 0.15)

VOID = (-7, 2, -1, 4)
STAIR_HOLE = (-5.6, 0.1, -5.8, -4.15)
slab([(-14, 10, -6, 4), (-3, 10, -6.5, -6), (2, 10, 4, 5.4)], [VOID, STAIR_HOLE],
     3.95, F1, WOOD_FLOOR)

wall("x", 3.9, -14, -3, F1, 7.4, [(-10.5, -7.6, 4.7, 7.0, "win"), (-6.6, -3.2, 4.4, 7.2, "glass")],
     skin=(1, EXT))
wall("z", -13.9, -6, 4, F1, 7.4,
     [(-5.2, -3.2, 5.6, 6.9, "win"), (0.4, 1.6, F1, 6.6, "open"), (1.7, 2.9, 4.25, 6.6, "glass")],
     skin=(-1, EXT))
wall("x", -5.9, -14, -3, F1, 7.4, [(-9.2, -6.4, 4.8, 7.0, "win")], skin=(-1, EXT))
wall("x", 3.9, -3, 2, F1, F2, [(-2.4, 1.4, 4.5, 7.4, "glass")], skin=(1, EXT))
wall("z", 2.0, -6.5, 5.4, F1, F2, [(-4.05, -3.05, F1, 6.6, "door")])
wall("x", 5.3, 2, 10, F1, F2, [(2.6, 9.4, 4.6, 7.4, "win")], skin=(1, EXT))
wall("z", 9.9, -6.5, 5.4, F1, F2, [(-4.6, -2.4, 5.6, 7.0, "win"), (1.5, 4.5, 4.8, 7.0, "win")],
     skin=(1, EXT))
wall("x", -6.4, -3, 10, F1, F2, [(-2.4, 0.4, 4.8, 7.0, "win"), (0.65, 1.65, F1, 6.6, "door")], skin=(-1, EXT))
block(-3.1, -2.9, F1, F2, -6.5, -6, EXT, solid=True)
block(-14, -3, 7.4, 7.5, -6, 4, CEILING)
block(-3.02, -2.98, 7.4, 7.6, -6, 4, CEILING)
block(1.84, 1.9, F1, F2, 4.0, 5.4, EXT)

for (a1, a2, b1, b2) in [(2.3, 9.7, 7.4, 7.7), (2.3, 9.7, 4.3, 4.6), (2.3, 2.6, 4.3, 7.7), (9.4, 9.7, 4.3, 7.7)]:
    block(a1, a2, b1, b2, 5.44, 6.0, color.white)
for (a1, a2, b1, b2) in [(1.2, 4.8, 7.0, 7.3), (1.2, 4.8, 4.5, 4.8), (1.2, 1.5, 4.5, 7.3), (4.5, 4.8, 4.5, 7.3)]:
    block(10.04, 10.6, b1, b2, a1, a2, color.white)
block(1.9, 10.3, 3.7, 4.25, 5.4, 5.7, color.white)
block(10.04, 10.3, 3.7, 4.25, -6.5, 5.7, color.white)
block(-14.0, -3.0, 3.95, 4.6, 4.04, 4.1, WOOD)
block(-13.8, -10.9, 4.75, 7.2, 4.04, 4.1, WOOD)
for gx in [-13.8 + 0.3 * k for k in range(1, 10)]:
    block(gx - 0.01, gx + 0.01, 4.75, 7.2, 4.1, 4.11, vector(0.38, 0.22, 0.11))
block(-14.0, -7.0, 3.62, 3.95, 4.04, 4.1, WOOD)

wall("x", -1, -14, -7, F1, 7.4, [(-9.6, -8.6, F1, 6.6, "door")], t=T)
wall("z", -7, -1, 4, F1, 7.4, [], t=T)
wall("z", -10, -6, -1, F1, 7.4, [(-2.9, -2.0, F1, 6.6, "door")], t=T)
wall("x", 0.5, 2, 10, F1, 7.6, [(3, 4, F1, 6.6, "door")], t=T)
wall("z", 5.5, -6.5, 0.5, F1, 7.6, [(-2.5, -1.6, F1, 6.6, "door")], t=T)
rail("x", -1.0, -7, 2, F1)
rail("x", -4.15, -5.6, 0.1, F1)
rail("z", 0.1, -5.8, -4.15, F1)
for x in (-9, -5, -1):
    downlight(x, 7.4, -3.6)

bed(-13.0, -11.0, -0.8, 1.3, F1, "-z", vector(0.78, 0.78, 0.80), color.white, vector(0.10, 0.15, 0.36),
    headboard=vector(0.84, 0.84, 0.86), accent=vector(0.60, 0.62, 0.66))
block(-13.6, -11.0, F1, 4.65, 3.35, 3.8, CABINET)
block(-13.6, -11.0, 4.65, 6.6, 3.7, 3.8, vector(0.32, 0.33, 0.35))
block(-12.9, -11.7, 5.0, 5.75, 3.64, 3.7, FRAME)
block(-11.0, -10.6, F1, 6.6, 3.3, 3.8, CABINET)
block(-10.6, -10.1, F1, 4.7, -0.9, -0.5, CABINET)
as_group(crystal_flush, -10.5, 7.4, 1.5)

tiled(-13.8, -10.06, F1 + 0.005, F1 + 0.02, -5.8, -1.06, vector(0.82, 0.80, 0.76))
marble(-13.8, -11.3, F1, 7.4, -5.8, -5.78, ("front",), seed=33)
vanity(-13.6, -11.6, -5.78, -5.25, F1, "+z", sinks=[-12.6])
lit_mirror(vector(-12.6, F1 + 1.75, -5.75), 0.9, 0.9, "+z", round_=True)
tiled(-13.84, -13.8, F1, 7.4, -2.4, -1.06)
tiled(-13.8, -12.4, F1, 7.4, -1.1, -1.06)
tiled(-13.8, -12.4, F1 + 0.02, F1 + 0.035, -2.4, -1.06, vector(0.42, 0.41, 0.40), step=0.3)
glass_screen(-12.42, -12.38, F1, F1 + 2.1, -2.4, -1.06)
glass_screen(-13.8, -13.35, F1, F1 + 2.1, -2.42, -2.38)
shower_set(vector(-13.1, 7.0, -1.7), vector(-13.78, F1 + 1.1, -1.75), "+x")
block(-12.95, -12.35, F1 + 0.02, F1 + 0.035, -2.95, -2.5, vector(0.92, 0.90, 0.86))
toilet(-10.45, -4.6, "-x", F1)
tp_holder(vector(-10.95, F1 + 0.7, -5.78), "+z")

block(4.0, 8.2, F1, 6.9, 0.56, 0.66, vector(0.3, 0.31, 0.33))
bed(5.0, 7.2, 0.76, 2.9, F1, "-z", vector(0.25, 0.26, 0.28), color.white, vector(0.55, 0.36, 0.22),
    headboard=vector(0.36, 0.37, 0.40), accent=vector(0.80, 0.70, 0.56))
for x in (4.4, 7.8):
    block(x - 0.3, x + 0.3, F1, 4.75, 0.7, 1.15, CABINET)
block(5.2, 7.0, F1, 4.65, 3.0, 3.45, CABINET)
for x1 in (2.5, 8.85):
    block(x1, x1 + 0.6, F1 + 0.05, 7.5, 5.05, 5.15, vector(0.45, 0.45, 0.47))
for (a1, a2, b1, b2) in [(2.2, 9.8, 0.7, 0.9), (2.2, 9.8, 4.95, 5.15), (2.2, 2.4, 0.7, 5.15), (9.6, 9.8, 0.7, 5.15)]:
    block(a1, a2, 7.45, 7.6, b1, b2, WOOD)
for x in (3.5, 8.5):
    downlight(x, 7.6, 3)
as_group(crystal_flush, 6.0, 7.6, 3.1, 0.36, 0.6)

block(2.1, 2.7, F1, 7.2, -3.2, 0.35, MIRROR, shininess=1)
block(2.2, 5.4, F1, 7.2, -6.3, -5.7, MIRROR, shininess=1)
for zz in (-2.6, -2.0, -1.4, -0.8, -0.2):
    block(2.69, 2.72, F1, 7.2, zz - 0.01, zz + 0.01, FRAME)
block(3.2, 4.4, F1, 5.1, -2.6, -1.2, CABINET)
pendant(3.8, 7.6, 6.8, -1.9, 0.25, color.white)

tiled(5.56, 9.8, F1 + 0.005, F1 + 0.02, -6.3, 0.44, vector(0.84, 0.82, 0.78))
marble(5.56, 5.58, F1, 7.6, -6.2, -3.4, ("right",), seed=35)
vanity(5.6, 6.15, -6.1, -3.6, F1, "+x", sinks=[-5.35, -4.35])
for zm in (-5.35, -4.35):
    lit_mirror(vector(5.62, F1 + 1.75, zm), 0.8, 1.0, "+x")
tub(8.4, 9.4, -1.9, -0.1, F1, faucet_end=-1)
pendant(8.9, 7.6, 6.6, -1.0, 0.14)
tiled(9.76, 9.8, F1, 7.2, -6.3, -5.1)
tiled(8.2, 9.8, F1, 7.2, -6.34, -6.3)
tiled(8.2, 9.8, F1 + 0.02, F1 + 0.035, -6.3, -5.1, vector(0.42, 0.41, 0.40), step=0.3)
glass_screen(8.18, 8.22, F1, F1 + 2.2, -6.3, -5.95)
glass_screen(8.2, 9.8, F1, F1 + 2.2, -5.12, -5.08)
shower_set(vector(9.0, 7.1, -5.7), vector(9.78, F1 + 1.1, -5.7), "-x")
block(9.74, 9.8, F1 + 1.0, F1 + 1.3, -6.2, -5.9, vector(0.16, 0.16, 0.16))
toilet(7.3, -5.95, "+z", F1)
tp_holder(vector(7.75, F1 + 0.7, -6.28), "+z")
towel_bar(vector(9.8, F1 + 1.1, -3.5), vector(9.8, F1 + 1.1, -2.7), face="-x")
downlight(7.5, 7.6, -2.5)
downlight(7.0, 7.6, -5.0)

potted_plant(-9.4, F1, -5.4, 1.0)
bench_seat(-8.45, -7.2, -1.5, -1.12, F1, WOOD, vector(0.80, 0.74, 0.66))

LOFT_HOLE = (-3, 2, -2.7, -1.1)
slab([(-3, 2, -6.5, 4), (2, 10, -6.5, 5.4)], [LOFT_HOLE], 7.6, F2, WOOD_FLOOR)
stairs(-3.4, 2.0, -2.7, -1.1, F1, F2, rail_z=-2.7)
wall("x", -3.75, -0.25, 7.25, F2, 9.0, [], t=T)
wall("x", 2.65, -0.25, 7.25, F2, 9.0, [], t=T)
wall("z", -0.25, -3.75, 2.65, F2, 9.0, [(-2.7, -1.1, F2, 9.0, "none")], t=T)
wall("z", 7.25, -3.75, 2.65, F2, 9.0, [], t=T)
rail("x", -2.7, -0.25, 2, F2)
rail("x", -1.1, -0.25, 2, F2)

ART_COLORS = [(vector(0.85, 0.55, 0.30), vector(0.20, 0.30, 0.45)),
              (vector(0.90, 0.88, 0.82), vector(0.75, 0.62, 0.40)),
              (vector(0.25, 0.40, 0.42), vector(0.92, 0.80, 0.55)),
              (vector(0.60, 0.25, 0.22), vector(0.95, 0.93, 0.88))]


def art(face, plane, a1, a2, y1, y2, style=0):
    s = 1 if face[0] == "+" else -1
    c1, c2 = ART_COLORS[style % len(ART_COLORS)]
    mid = y1 + (y2 - y1) * 0.45

    def flat(p1, p2, q1, q2, d1, d2, col):
        if face[1] == "z":
            block(p1, p2, q1, q2, plane + s * d1, plane + s * d2, col)
        else:
            block(plane + s * d1, plane + s * d2, q1, q2, p1, p2, col)
    flat(a1, a2, y1, y2, 0, 0.03, FRAME)
    flat(a1 + 0.05, a2 - 0.05, y1 + 0.05, y2 - 0.05, 0.03, 0.04, c1)
    flat(a1 + 0.05, a2 - 0.05, y1 + 0.05, mid, 0.04, 0.045, c2)
    am = (a1 + a2) / 2
    flat(am - 0.1, am + 0.25, mid - 0.15, y2 - 0.2, 0.045, 0.05, c2 * 0.7)


def table_lamp(x, y, z):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.35, 0), radius=0.03, color=FRAME)
    cylinder(pos=vector(x, y + 0.35, z), axis=vector(0, 0.25, 0), radius=0.16, color=LAMP, emissive=True)


def floor_lamp(x, y, z):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.02, 0), radius=0.18, color=FRAME)
    cylinder(pos=vector(x, y, z), axis=vector(0, 1.45, 0), radius=0.02, color=FRAME)
    cylinder(pos=vector(x, y + 1.45, z), axis=vector(0, 0.3, 0), radius=0.22, color=LAMP, emissive=True)


def big_plant(x, y, z, h=1.6):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.5, 0), radius=0.25, color=vector(0.85, 0.83, 0.78))
    cylinder(pos=vector(x, y + 0.5, z), axis=vector(0, h - 0.6, 0), radius=0.03, color=TRUNK)
    for dx, dy, dz, r in [(0, 0, 0, 0.32), (0.22, -0.25, 0.1, 0.26), (-0.2, -0.3, -0.12, 0.26),
                          (0.05, 0.25, -0.18, 0.22), (-0.12, -0.55, 0.18, 0.22)]:
        sphere(pos=vector(x + dx, y + h + dy, z + dz), radius=r, color=LEAF)


def curtain(run, c, a1, a2, y1, y2):
    if run == "x":
        block(a1, a2, y1, y2, c - 0.025, c + 0.025, SHEER, opacity=0.85)
    else:
        block(c - 0.025, c + 0.025, y1, y2, a1, a2, SHEER, opacity=0.85)


def cushion(x1, x2, y, z1, z2, col, h=0.38):
    block(x1, x2, y, y + h, z1, z2, col)


def rug(x1, x2, z1, z2, y, col):
    block(x1, x2, y + 0.005, y + 0.018, z1, z2, col)


def cove(x1, x2, z1, z2, y):
    for (a1, a2, b1, b2) in [(x1, x2, z1, z1 + 0.04), (x1, x2, z2 - 0.04, z2),
                             (x1, x1 + 0.04, z1, z2), (x2 - 0.04, x2, z1, z2)]:
        block(a1, a2, y - 0.02, y, b1, b2, LAMP, emissive=True)


v = -14.0
while v <= 10.01:
    block(v - 0.006, v + 0.006, F0 + 0.01, F0 + 0.014, -6, 4, GROUT)
    v += 1.2
v = -6.0
while v <= 4.01:
    block(-14, 10, F0 + 0.01, F0 + 0.014, v - 0.006, v + 0.006, GROUT)
    v += 1.2
for (x1, x2, z1, z2, y) in [(2.1, 9.8, 0.6, 5.3, F1), (-13.8, -7.1, -0.9, 3.8, F1), (-0.2, 7.2, -3.7, 2.6, F2)]:
    v = x1 + 0.22
    while v < x2:
        block(v - 0.006, v + 0.006, y, y + 0.004, z1, z2, PLANK_LINE)
        v += 0.22

cylinder(pos=vector(-6.3, F0, 3.1), axis=vector(0, 0.55, 0), radius=0.25, color=WOOD)
table_lamp(-6.3, F0 + 0.55, 3.1)
curtain("x", 3.72, -6.95, -6.45, F0, 7.2)
curtain("x", 3.72, 1.35, 1.85, F0, 7.2)
big_plant(1.45, F0, -0.5, 1.8)
zg = -0.9
while zg < 3.95:
    if not (0.8 < zg < 2.6):
        block(1.87, 1.88, F0, 3.95, zg, zg + 0.02, vector(0.38, 0.22, 0.11))
    zg += 0.3
cove(-6, 1, -0.2, 3.2, 7.17)
cove(-4.6, -0.4, 0.6, 2.4, 7.12)
art("+x", -6.94, 0.0, 2.6, 5.0, 6.6, 0)

block(-10.75, -10.25, 1.3, 1.305, 0.3, 2.9, vector(0.85, 0.80, 0.70))
cylinder(pos=vector(-10.5, 1.305, 1.6), axis=vector(0, 0.3, 0), radius=0.08, color=color.white)
for dx, dz, cc in [(0, 0, color.white), (0.08, 0.05, YELLOW), (-0.07, -0.05, color.white)]:
    sphere(pos=vector(-10.5 + dx, 1.68, 1.6 + dz), radius=0.08, color=cc)
block(-13.78, -13.3, F0, 1.3, -0.7, 0.8, WOOD)
table_lamp(-13.55, 1.3, -0.35)
art("+x", -13.8, -0.55, 0.65, 1.9, 3.0, 1)
big_plant(-13.4, F0, 3.4, 1.5)

for x in (-11.4, -10.3, -9.2):
    bar_stool(x, -2.2, F0)
    cylinder(pos=vector(x, 2.97, -3.2), axis=vector(0, 0.98, 0), radius=0.006, color=FRAME)
    cone(pos=vector(x, 2.75, -3.2), axis=vector(0, 0.24, 0), radius=0.17, color=vector(0.08, 0.08, 0.09))
    ring(pos=vector(x, 2.75, -3.2), axis=vector(0, 1, 0), radius=0.17, thickness=0.008, color=GOLD)
    cylinder(pos=vector(x, 2.745, -3.2), axis=vector(0, 0.005, 0), radius=0.155, color=LAMP, emissive=True)
cylinder(pos=vector(-9.4, 1.43, -3.2), axis=vector(0, 0.08, 0), radius=0.22, color=color.white)
for dx, dz, cc in [(0, 0, vector(0.9, 0.5, 0.1)), (0.1, 0.06, vector(0.8, 0.1, 0.1)),
                   (-0.09, 0.05, vector(0.95, 0.85, 0.2)), (0.02, -0.1, vector(0.3, 0.6, 0.2))]:
    sphere(pos=vector(-9.4 + dx, 1.56, -3.2 + dz), radius=0.06, color=cc)

art("+x", -5.94, -4.0, -3.3, 1.5, 2.6, 2)
block(2.06, 5.94, 3.9, 3.95, -1, 4, WOOD)
for (x, z) in [(3, 0.3), (5, 0.3), (3, 3), (5, 3)]:
    downlight(x, 3.9, z)
block(2.08, 2.5, F0, 0.95, -0.8, 0.6, WOOD)
big_plant(3.0, F0, 3.35, 1.5)

for x in (6.55, 9.45):
    block(x - 0.28, x + 0.28, F0, 1.05, -0.88, -0.38, WOOD)
    table_lamp(x, 1.05, -0.63)
art("+z", -0.94, 7.4, 8.6, 2.0, 2.9, 3)
rug(6.6, 9.4, 1.4, 3.0, F0, vector(0.80, 0.76, 0.68))
curtain("z", 9.72, -0.6, -0.05, 1.0, 3.7)
curtain("z", 9.72, 3.05, 3.6, 1.0, 3.7)

potted_plant(9.3, F0, -1.6, 0.6)
cylinder(pos=vector(6.12, 1.7, -4.4), axis=vector(0.06, 0, 0), radius=0.15, color=METAL)

rug(2.9, 5.5, -13.3, -10.5, F0, vector(0.78, 0.75, 0.70))
floor_lamp(5.4, F0, -10.0)
big_plant(2.6, F0, -6.6, 1.7)
art("-z", -6.0, 6.2, 8.0, 1.8, 2.8, 0)

rug(-13.3, -10.7, 1.0, 3.0, F1, vector(0.78, 0.80, 0.82))
block(-13.75, -13.1, F1, 4.7, -0.9, -0.4, CABINET)
table_lamp(-13.42, 4.7, -0.65)
table_lamp(-10.35, 4.7, -0.7)
art("+z", -0.94, -12.8, -11.2, 5.6, 6.5, 2)
curtain("x", 3.72, -10.95, -10.5, F1, 7.3)
curtain("x", 3.72, -7.6, -7.15, F1, 7.3)
armchair(-8.0, 2.0, "+x", F1, vector(0.80, 0.75, 0.68), vector(0.16, 0.22, 0.38))

block(-12.0, -11.4, 5.4, 5.43, -1.06, -1.1, METAL)
block(-11.95, -11.45, 4.8, 5.4, -1.08, -1.12, color.white)
potted_plant(-10.5, F1, -1.5, 0.6)

rug(4.4, 7.8, 1.8, 4.3, F1, vector(0.85, 0.83, 0.78))
table_lamp(4.4, 4.75, 0.92)
table_lamp(7.8, 4.75, 0.92)
armchair(9.0, 3.9, "+x", F1, vector(0.80, 0.75, 0.68), P_CARAMEL)
floor_lamp(9.5, F1, 3.1)
art("+x", 2.1, 1.5, 3.8, 5.2, 6.4, 1)
cove(2.4, 9.6, 0.9, 4.95, 7.45)

cylinder(pos=vector(3.8, F1, -1.9), axis=vector(0, 0.01, 0), radius=0.9, color=vector(0.9, 0.88, 0.84))
potted_plant(6.3, F1, 0.0, 0.7)
block(5.62, 5.68, 5.3, 5.33, -3.3, -2.8, METAL)
block(5.64, 5.7, 4.7, 5.3, -3.25, -2.85, color.white)
rug(7.0, 7.8, -1.6, -0.4, F1, color.white)

rug(-9.5, -5.9, -4.0, -3.0, F1, vector(0.70, 0.66, 0.58))
art("+x", -9.94, -5.6, -4.7, 5.2, 6.4, 3)
art("-z", -1.06, -8.4, -7.25, 5.3, 6.25, 3)

LOFT_FABRIC = vector(0.66, 0.50, 0.36)
LEATHER = vector(0.55, 0.34, 0.20)
DARK_WOOD = vector(0.30, 0.19, 0.11)
for (x1, x2, z1, z2) in [(-0.25, 7.3, -3.86, -3.64), (-0.25, 7.3, 2.54, 2.76), (7.14, 7.36, -3.75, 2.65),
                         (-0.36, -0.14, -3.75, -2.7), (-0.36, -0.14, -1.1, 2.65)]:
    block(x1, x2, 9.0, 9.05, z1, z2, WOOD)
for (x1, x2, z1, z2) in [(-0.19, 7.19, -3.69, -3.66), (-0.19, 7.19, 2.56, 2.59), (7.16, 7.19, -3.69, 2.59)]:
    block(x1, x2, 8.95, 8.99, z1, z2, LAMP, emissive=True)
xs_ = 3.2
while xs_ < 6.8:
    block(xs_, xs_ + 0.07, F2, 9.0, -3.69, -3.64, DARK_WOOD)
    xs_ += 0.12
block(3.6, 6.4, 8.05, 8.4, -3.64, -3.28, vector(0.18, 0.18, 0.19))
block(3.6, 6.4, 8.02, 8.05, -3.6, -3.32, LAMP, emissive=True)
block(4.15, 5.85, 8.45, 9.4, -3.62, -3.56, FRAME)
block(4.2, 5.8, 8.5, 9.35, -3.56, -3.555, vector(0.08, 0.10, 0.14), shininess=1)
rug(2.7, 6.95, -2.95, 1.4, F2, vector(0.55, 0.50, 0.45))
rug(2.9, 6.75, -2.75, 1.2, F2 + 0.006, vector(0.86, 0.82, 0.74))
sofa(3.0, 6.3, 0.35, 1.25, F2, "+z", LOFT_FABRIC, ends=("arm", None), pillows=[P_CREAM, P_RUST, P_SAND])
sofa(6.3, 7.1, -1.7, 1.25, F2, "+x", LOFT_FABRIC, ends=("arm", "back"), pillows=[P_RUST, P_CREAM])
block(3.2, 3.95, F2 + 0.5, F2 + 0.53, 0.4, 1.0, vector(0.80, 0.50, 0.35))
cylinder(pos=vector(4.7, F2, -1.0), axis=vector(0, 0.34, 0), radius=0.5, color=DARK_WOOD)
cylinder(pos=vector(4.7, F2 + 0.34, -1.0), axis=vector(0, 0.04, 0), radius=0.56, color=WOOD)
block(4.3, 4.65, F2 + 0.38, F2 + 0.43, -1.25, -1.0, vector(0.2, 0.3, 0.45))
block(4.32, 4.62, F2 + 0.43, F2 + 0.47, -1.22, -1.02, vector(0.85, 0.82, 0.75))
potted_plant(5.0, F2 + 0.38, -0.85, 0.35)
POUF = vector(0.55, 0.34, 0.20)
cylinder(pos=vector(6.05, F2, -2.45), axis=vector(0, 0.34, 0), radius=0.32, color=POUF)
ellipsoid(pos=vector(6.05, F2 + 0.34, -2.45), size=vector(0.64, 0.12, 0.64), color=POUF * 1.06)
ring(pos=vector(6.05, F2 + 0.2, -2.45), axis=vector(0, 1, 0), radius=0.322, thickness=0.008, color=POUF * 0.7)
block(5.83, 6.27, F2 + 0.38, F2 + 0.44, -2.6, -2.3, vector(0.90, 0.86, 0.78))
VASE = vector(0.88, 0.84, 0.76)
cylinder(pos=vector(6.8, F2, -3.15), axis=vector(0, 0.1, 0), radius=0.15, color=VASE)
ellipsoid(pos=vector(6.8, F2 + 0.35, -3.15), size=vector(0.38, 0.56, 0.38), color=VASE)
cylinder(pos=vector(6.8, F2 + 0.55, -3.15), axis=vector(0, 0.22, 0), radius=0.08, color=VASE)
ring(pos=vector(6.8, F2 + 0.77, -3.15), axis=vector(0, 1, 0), radius=0.08, thickness=0.012, color=VASE * 0.95)
for k in range(8):
    a = 2 * pi * k / 8 + 0.3
    d = norm(vector(0.45 * cos(a), 1, 0.45 * sin(a)))
    p0 = vector(6.8, F2 + 0.74, -3.15)
    L = 0.55 + 0.12 * ((k * 5) % 3)
    tip = p0 + d * L
    cylinder(pos=p0, axis=tip - p0, radius=0.006, color=vector(0.70, 0.60, 0.44))
    ellipsoid(pos=tip + d * 0.18, axis=d * 0.44, height=0.16, width=0.16, color=vector(0.93, 0.86, 0.72),
              lowpoly=True)
as_group(cube_chandelier, 4.7, 11.0, -0.95)
armchair(0.9, 1.37, "+z", F2, LEATHER, P_CREAM)
floor_lamp(0.18, F2, 2.25)
cylinder(pos=vector(1.75, F2, 1.5), axis=vector(0, 0.5, 0), radius=0.2, color=DARK_WOOD)
table_lamp(1.75, F2 + 0.5, 1.5)
block(-0.15, 2.6, F2, F2 + 0.95, 2.2, 2.59, WOOD)
BOOKS = [vector(0.55, 0.15, 0.12), vector(0.15, 0.30, 0.45), vector(0.85, 0.80, 0.70),
         vector(0.25, 0.40, 0.25), vector(0.75, 0.55, 0.20), vector(0.20, 0.20, 0.22)]
for shelf_y in (F2 + 0.08, F2 + 0.52):
    block(-0.12, 2.57, shelf_y - 0.03, shelf_y, 2.17, 2.2, DARK_WOOD)
    bx = -0.05
    k = 0
    while bx < 2.45:
        w_ = 0.05 + 0.03 * (k % 3)
        h_ = 0.26 + 0.06 * ((k * 7) % 4)
        if k % 9 != 8:
            block(bx, bx + w_, shelf_y, shelf_y + h_, 2.23, 2.5, BOOKS[k % len(BOOKS)])
        bx += w_ + 0.01
        k += 1
potted_plant(2.3, F2 + 0.95, 2.4, 0.4)
big_plant(6.75, F2, 2.15, 1.2)
art("+z", -3.69, 0.3, 1.5, 8.2, 8.85, 2)
SKYLIGHTS = []
SLOPE = radians(32)
for xc in (2.8, 5.2):
    zc = 1.7
    yc = 7.425 + tan(SLOPE) * (6.0 - zc) - 0.05
    n_up = vector(0, cos(SLOPE), sin(SLOPE))
    box(pos=vector(xc, yc, zc) + n_up * 0.015, axis=vector(1.32, 0, 0), up=n_up, height=0.02, width=1.12,
        color=FRAME)
    SKYLIGHTS.append(box(pos=vector(xc, yc, zc), axis=vector(1.2, 0, 0), up=n_up, height=0.02, width=1.0,
                         color=vector(0.78, 0.90, 1.0), emissive=True))

OAK = vector(0.86, 0.74, 0.58)
STUDIO_WHITE = vector(0.96, 0.93, 0.88)
CREAMY = vector(0.93, 0.89, 0.81)
STRAP = vector(0.22, 0.22, 0.23)
WARM_GLOW = vector(1.0, 0.90, 0.72)
block(-21.3, -13.95, 0, F0, -8.95, -3.0, PLINTH, solid=True)
block(-21.1, -14.05, F0, F0 + 0.01, -8.7, -3.04, OAK)
xp = -21.1
while xp < -14.05:
    block(xp - 0.004, xp + 0.004, F0 + 0.01, F0 + 0.013, -8.7, -3.04, vector(0.72, 0.60, 0.45))
    xp += 0.2
wall("z", -21.1, -8.8, -3.0, F0, 3.95, [(-8.4, -3.4, 0.6, 3.5, "glass")], col=STUDIO_WHITE, skin=(-1, EXT))
wall("x", -8.7, -21.2, -13.9, F0, 3.95, [(-20.7, -18.6, 0.6, 3.5, "glass"), (-18.3, -16.3, F0, 3.3, "open"),
                                         (-16.0, -14.4, 0.6, 3.5, "glass")], col=STUDIO_WHITE, skin=(-1, EXT))
wall("z", -13.9, -8.8, -5.95, F0, 3.95, [], col=STUDIO_WHITE, skin=(1, EXT))
block(-14.07, -14.045, F0, 3.9, -5.95, -4.9, STUDIO_WHITE)
block(-14.07, -14.045, F0, 3.9, -3.9, -3.08, STUDIO_WHITE)
block(-14.07, -14.045, 2.9, 3.9, -4.9, -3.9, STUDIO_WHITE)
for (x1, x2) in [(-21.0, -17.27), (-16.13, -14.07)]:
    block(x1, x2, F0, 3.9, -3.075, -3.05, STUDIO_WHITE)
block(-17.27, -16.13, 2.67, 3.9, -3.075, -3.05, STUDIO_WHITE)
block(-21.0, -14.07, 3.84, 3.95, -8.6, -3.05, CEILING)
block(-21.0, -14.07, F0, F0 + 0.1, -3.1, -3.08, vector(0.90, 0.86, 0.80))
block(-21.06, -21.0, F0, F0 + 0.1, -8.6, -3.08, vector(0.90, 0.86, 0.80))


def arch_mirror(xc, w=0.9, y0=F0 + 0.25, h=1.95, zw=-3.08):
    r = w / 2
    block(xc - r - 0.06, xc + r + 0.06, y0 - 0.06, y0 + h, zw - 0.012, zw, WARM_GLOW, emissive=True)
    cylinder(pos=vector(xc, y0 + h, zw - 0.012), axis=vector(0, 0, 0.012), radius=r + 0.06, color=WARM_GLOW,
             emissive=True)
    block(xc - r, xc + r, y0, y0 + h, zw - 0.03, zw - 0.012, MIRROR, shininess=1)
    cylinder(pos=vector(xc, y0 + h, zw - 0.03), axis=vector(0, 0, 0.018), radius=r, color=MIRROR, shininess=1)


for xc in (-20.35, -19.2, -18.05, -15.6, -14.7):
    arch_mirror(xc, 0.82 if xc > -16 else 0.9)
for (cx, cz) in [(-17.62, -4.85), (-17.62, -7.6)]:
    cylinder(pos=vector(cx, F0, cz), axis=vector(0, 3.34, 0), radius=0.19, color=STUDIO_WHITE)
    cylinder(pos=vector(cx, F0, cz), axis=vector(0, 0.08, 0), radius=0.21, color=vector(0.90, 0.86, 0.80))
    add_solid(cx - 0.19, cx + 0.19, F0, 3.84, cz - 0.19, cz + 0.19)
for zt in (-4.4, -6.9):
    block(-20.8, -14.3, 3.79, 3.84, zt - 0.02, zt + 0.02, FRAME)
    xs = -20.4
    while xs < -14.4:
        cylinder(pos=vector(xs, 3.79, zt), axis=vector(0, -0.06, 0), radius=0.012, color=FRAME)
        cylinder(pos=vector(xs, 3.73, zt), axis=vector(0.04, -0.11, 0.04 if zt > -5 else -0.04), radius=0.045,
                 color=color.white)
        cylinder(pos=vector(xs + 0.04, 3.62, zt + (0.04 if zt > -5 else -0.04)), axis=vector(0.004, -0.006, 0),
                 radius=0.035, color=LAMP, emissive=True)
        xs += 1.1
for zc in (-3.6, -8.25):
    block(-21.0, -14.1, 3.82, 3.84, zc - 0.02, zc + 0.02, WARM_GLOW, emissive=True)


def reformer(x1, x2, z, y, frame=OAK, pad=CREAMY, tower=False):
    w = 0.33
    for xx in (x1 + 0.05, x2 - 0.05):
        for zz in (z - w + 0.05, z + w - 0.05):
            block(xx - 0.04, xx + 0.04, y, y + 0.2, zz - 0.04, zz + 0.04, frame * 0.92)
    block(x1, x2, y + 0.2, y + 0.33, z - w, z - w + 0.07, frame)
    block(x1, x2, y + 0.2, y + 0.33, z + w - 0.07, z + w, frame)
    block(x1, x1 + 0.09, y + 0.2, y + 0.33, z - w, z + w, frame)
    block(x2 - 0.09, x2, y + 0.2, y + 0.33, z - w, z + w, frame)
    block(x1 + 0.35, x1 + 1.05, y + 0.33, y + 0.4, z - 0.27, z + 0.27, frame * 0.95)
    block(x1 + 0.36, x1 + 1.04, y + 0.4, y + 0.45, z - 0.26, z + 0.26, pad)
    block(x1 + 0.12, x1 + 0.35, y + 0.33, y + 0.42, z - 0.2, z + 0.2, pad)
    for zz in (-0.15, 0.15):
        block(x1 + 0.96, x1 + 1.04, y + 0.45, y + 0.6, z + zz - 0.05, z + zz + 0.05, pad)
    for k in range(4):
        zz = z - 0.15 + 0.1 * k
        cylinder(pos=vector(x1 + 1.05, y + 0.28, zz), axis=vector(x2 - 0.4 - x1 - 1.05, 0, 0), radius=0.011,
                 color=CHROME)
    xf = x2 - 0.3
    for zz in (z - 0.3, z + 0.3):
        cylinder(pos=vector(xf, y + 0.33, zz), axis=vector(0, 0.34, 0), radius=0.018, color=CHROME)
    cylinder(pos=vector(xf, y + 0.67, z - 0.32), axis=vector(0, 0, 0.64), radius=0.03, color=STRAP)
    for zz in (z - 0.3, z + 0.3):
        cylinder(pos=vector(x1 + 0.04, y + 0.33, zz), axis=vector(0, 0.55, 0), radius=0.02, color=CHROME)
        cylinder(pos=vector(x1 + 0.04, y + 0.88, zz - 0.03), axis=vector(0, 0, 0.06), radius=0.04, color=STRAP)
        cylinder(pos=vector(x1 + 0.04, y + 0.88, zz), axis=vector(0.75, -0.4, 0), radius=0.007, color=STRAP)
    if tower:
        for zz in (z - w + 0.03, z + w - 0.03):
            block(x1 - 0.06, x1 + 0.02, y + 0.2, y + 2.0, zz - 0.03, zz + 0.03, frame)
        block(x1 - 0.06, x1 + 0.02, y + 1.95, y + 2.03, z - w, z + w, frame)
        cylinder(pos=vector(x1 + 0.02, y + 1.15, z - w + 0.03), axis=vector(0, 0, 2 * w - 0.06), radius=0.02,
                 color=CHROME)
        for zz in (z - 0.12, z + 0.12):
            cylinder(pos=vector(x1 + 0.03, y + 1.95, zz), axis=vector(0, -0.55, 0), radius=0.012, color=CHROME)
            cylinder(pos=vector(x1 + 0.03, y + 1.4, zz), axis=vector(0.1, -0.08, 0), radius=0.02, color=STRAP)


def cadillac(cx, cz, y, L=2.2, W=0.78):
    BLACK_PAD = vector(0.12, 0.12, 0.13)
    SILVER = vector(0.78, 0.79, 0.80)
    FUZZY = vector(0.94, 0.93, 0.90)
    x1, x2, z1, z2 = cx - L / 2, cx + L / 2, cz - W / 2, cz + W / 2
    top = y + 0.66
    for xx in (x1 + 0.06, x2 - 0.06):
        for zz in (z1 + 0.06, z2 - 0.06):
            block(xx - 0.04, xx + 0.04, y + 0.05, top - 0.08, zz - 0.04, zz + 0.04, FRAME)
            cylinder(pos=vector(xx, y + 0.035, zz - 0.02), axis=vector(0, 0, 0.04), radius=0.035, color=FRAME)
    for zz in (z1, z2 - 0.05):
        block(x1, x2, top - 0.14, top - 0.06, zz, zz + 0.05, SILVER)
    block(x1, x1 + 0.05, top - 0.14, top - 0.06, z1, z2, SILVER)
    block(x2 - 0.05, x2, top - 0.14, top - 0.06, z1, z2, SILVER)
    for (a, b) in [(x1 + 0.02, x1 + 0.62), (x1 + 0.64, x1 + 1.42), (x1 + 1.44, x2 - 0.02)]:
        block(a, b, top - 0.06, top, z1 + 0.02, z2 - 0.02, BLACK_PAD)
    block(x1 + 1.0, x1 + 1.07, top - 0.13, top + 0.004, z1 - 0.005, z2 + 0.005, vector(0.05, 0.05, 0.05))
    cylinder(pos=vector(x1 + 0.3, y + 0.28, cz), axis=vector(L - 0.6, 0, 0), radius=0.025, color=OAK)
    block(x1 + 0.02, x1 + 0.1, top, top + 0.45, z1 + 0.06, z2 - 0.06, BLACK_PAD)
    for zz in (cz - 0.16, cz + 0.16):
        block(x2 - 0.32, x2 - 0.2, top, top + 0.18, zz - 0.06, zz + 0.06, BLACK_PAD)
    H = y + 2.15
    posts = [(x1, z1), (x1, z2), (x2, z1), (x2, z2)]
    for (px, pz) in posts:
        cylinder(pos=vector(px, top - 0.14, pz), axis=vector(0, H - top + 0.14, 0), radius=0.025, color=CHROME)
        for yc in (y + 1.0, y + 1.45, y + 1.9):
            cylinder(pos=vector(px, yc, pz), axis=vector(0, 0.08, 0), radius=0.034, color=FRAME)
    for pz in (z1, z2):
        cylinder(pos=vector(x1, H, pz), axis=vector(L, 0, 0), radius=0.022, color=CHROME)
    for px in (x1, x2):
        cylinder(pos=vector(px, H, z1), axis=vector(0, 0, W), radius=0.022, color=CHROME)
    cylinder(pos=vector(x1, H - 0.12, cz + 0.1), axis=vector(L, 0, 0), radius=0.02, color=CHROME)
    cylinder(pos=vector(cx + 0.4, H, z1), axis=vector(0, 0, W), radius=0.02, color=CHROME)
    cylinder(pos=vector(x2, y + 1.35, z1), axis=vector(0, 0, W), radius=0.022, color=CHROME)
    cylinder(pos=vector(x2 - 0.02, y + 1.35, cz - 0.22), axis=vector(0, 0, 0.44), radius=0.03, color=BLACK_PAD)
    cylinder(pos=vector(x1, y + 1.05, z1), axis=vector(0, 0, W), radius=0.02, color=OAK)
    for zz in (z1 + 0.18, z2 - 0.18):
        cylinder(pos=vector(x2 - 0.03, H, zz), axis=vector(0, -0.55, 0), radius=0.012, color=CHROME)
        cylinder(pos=vector(x2 - 0.03, H - 0.55, zz), axis=vector(0, -0.18, 0), radius=0.025, color=BLACK_PAD)
        cylinder(pos=vector(x1 + 0.03, H, zz), axis=vector(0, -0.6, 0), radius=0.012, color=CHROME)
        box(pos=vector(x1 + 0.05, H - 0.8, zz), axis=vector(0.06, 0, 0), up=vector(0, 1, 0), height=0.36, width=0.1,
            color=FUZZY)
    cylinder(pos=vector(cx + 0.35, H - 0.12, cz + 0.1), axis=vector(0, -0.75, 0), radius=0.01, color=CHROME)
    block(cx + 0.2, cx + 0.5, H - 0.9, H - 0.87, cz - 0.05, cz + 0.25, OAK)
    for zz in (cz - 0.05, cz + 0.25):
        cylinder(pos=vector(cx + 0.35, H - 0.87, zz), axis=vector(0, -0.15, 0), radius=0.012, color=BLACK_PAD)


def yoga_mat(x1, x2, zc, y, col, blocks=True):
    block(x1, x2, y + 0.002, y + 0.008, zc - 0.31, zc + 0.31, col)
    if blocks:
        for k in range(2):
            block(x2 - 0.42 + k * 0.24, x2 - 0.2 + k * 0.24, y + 0.008, y + 0.11, zc + 0.36, zc + 0.5,
                  vector(0.80, 0.66, 0.46))
        block(x1 + 0.1, x1 + 0.12, y + 0.008, y + 0.012, zc - 0.25, zc + 0.25, vector(0.35, 0.33, 0.30))


for zr in (-4.3, -5.6):
    reformer(-20.6, -18.1, zr, F0)
cadillac(-19.4, -7.35, F0)
for zc, mc in [(-5.95, vector(0.66, 0.73, 0.64)), (-6.85, vector(0.86, 0.78, 0.64)),
               (-7.75, vector(0.80, 0.60, 0.50))]:
    yoga_mat(-16.95, -15.15, zc, F0, mc)
block(-14.45, -14.1, F0, F0 + 1.6, -5.6, -4.95, OAK)
for k, ys in enumerate((F0 + 0.02, F0 + 0.55, F0 + 1.1)):
    block(-14.45, -14.1, ys, ys + 0.025, -5.6, -4.95, OAK * 0.92)
    for j in range(3):
        cylinder(pos=vector(-14.42, ys + 0.12, -5.55 + j * 0.2), axis=vector(0.28, 0, 0), radius=0.09,
                 color=[CREAMY, vector(0.80, 0.74, 0.66), color.white][(k + j) % 3])
sphere(pos=vector(-14.45, F0 + 0.3, -8.2), radius=0.3, color=CREAMY)
big_plant(-20.65, F0, -3.5, 1.5)

slab([(0.4, 10, -14, -6.5)], [], 3.95, F1, WOOD_FLOOR)
wall("z", 0.5, -14, -6.5, F1, 7.4, [], skin=(-1, EXT))
wall("x", -13.9, 0.4, 10, F1, 7.4, [(1.0, 4.0, 4.8, 7.0, "glass"), (5.4, 9.4, 4.8, 7.0, "glass")],
     skin=(-1, EXT))
wall("z", 9.9, -14, -6.5, F1, 7.4, [(-12.6, -9.0, 5.2, 7.0, "win")], skin=(1, EXT))
wall("x", -7.6, 0.5, 4.6, F1, 7.4, [(0.8, 1.8, F1, 6.6, "door")], t=T)
wall("z", 2.4, -7.6, -6.55, F1, 7.4, [(-7.45, -6.6, F1, 6.6, "door")], t=T)
wall("z", 4.6, -14, -7.6, F1, 7.4, [], t=T)
for (x1, x2) in [(0.6, 0.65), (1.65, 9.8)]:
    block(x1, x2, F1, 7.4, -6.585, -6.55, WHITE_WALL)
block(0.65, 1.65, 6.6, 7.4, -6.585, -6.55, WHITE_WALL)
block(0.4, 10.0, 3.7, 3.95, -14.05, -13.75, color.white)
block(0.25, 0.55, 3.7, 3.95, -14.05, -6.5, color.white)

P = F1
rug(1.1, 4.1, -12.3, -9.1, P, vector(0.56, 0.52, 0.47))
rug(1.25, 3.95, -12.15, -9.25, P + 0.004, vector(0.72, 0.68, 0.62))
block(0.62, 0.98, P, 7.3, -13.5, -7.9, KWOOD)
for zv in (-11.65, -9.8):
    block(0.62, 1.0, P, 7.3, zv - 0.02, zv + 0.02, KWOOD * 1.15)
BOOK_COLS = [vector(0.55, 0.15, 0.12), vector(0.15, 0.30, 0.45), vector(0.86, 0.82, 0.72),
             vector(0.25, 0.40, 0.25), vector(0.75, 0.55, 0.20), vector(0.20, 0.20, 0.22),
             vector(0.62, 0.48, 0.36), vector(0.90, 0.88, 0.84)]
brng = Random(5)
for ys in [P + 0.08, P + 0.6, P + 1.12, P + 1.64, P + 2.16, P + 2.68]:
    block(0.62, 1.0, ys - 0.025, ys, -13.5, -7.9, KWOOD * 1.15)
    for (za, zb_) in [(-13.45, -11.7), (-11.6, -9.85), (-9.75, -7.95)]:
        zb = za + 0.02
        style = brng.randint(0, 3)
        while zb < zb_ - 0.08:
            if style == 0 and zb > za + 0.6:
                if brng.random() < 0.5:
                    cylinder(pos=vector(0.82, ys, zb + 0.1), axis=vector(0, 0.24, 0), radius=0.07, color=VASE)
                else:
                    potted_plant(0.82, ys, zb + 0.1, 0.22)
                zb += 0.32
                style = 1
                continue
            if style == 2 and zb > za + 0.5:
                for kk in range(4):
                    block(0.68, 0.96, ys + kk * 0.045, ys + kk * 0.045 + 0.04, zb, zb + 0.24,
                          BOOK_COLS[brng.randint(0, 7)])
                zb += 0.3
                style = 1
                continue
            bw = brng.uniform(0.03, 0.06)
            bh = brng.uniform(0.22, 0.34)
            block(0.68, 0.96, ys, ys + bh, zb, zb + bw, BOOK_COLS[brng.randint(0, 7)])
            zb += bw + 0.003
block(1.5, 3.7, P + 0.72, P + 0.77, -10.75, -9.85, KWOOD)
block(1.5, 1.58, P, P + 0.72, -10.75, -9.85, KWOOD)
block(2.95, 3.7, P, P + 0.72, -10.75, -9.85, KWOOD * 0.92)
for yd in (P + 0.25, P + 0.5):
    block(2.97, 3.68, yd, yd + 0.01, -10.77, -10.75, KGAP)
    block(3.2, 3.45, yd + 0.1, yd + 0.115, -10.79, -10.77, STEEL)
block(1.58, 2.95, P + 0.3, P + 0.72, -9.9, -9.85, KWOOD)
block(1.75, 3.05, P + 0.77, P + 0.775, -10.65, -10.25, vector(0.20, 0.18, 0.17))
for (mx, mw) in [(2.05, 0.6), (2.72, 0.6)]:
    block(mx - mw / 2, mx + mw / 2, P + 0.95, P + 1.31, -10.1, -10.07, FRAME)
    block(mx - mw / 2 + 0.015, mx + mw / 2 - 0.015, P + 0.965, P + 1.295, -10.11, -10.1, vector(0.16, 0.30, 0.46),
          emissive=True)
    cylinder(pos=vector(mx, P + 0.775, -10.02), axis=vector(0, 0.2, 0), radius=0.018, color=FRAME)
    block(mx - 0.1, mx + 0.1, P + 0.775, P + 0.785, -10.1, -9.95, FRAME)
block(2.12, 2.6, P + 0.775, P + 0.79, -10.5, -10.35, vector(0.85, 0.85, 0.86))
block(2.7, 2.78, P + 0.775, P + 0.79, -10.48, -10.38, vector(0.85, 0.85, 0.86))
block(1.62, 1.95, P + 0.775, P + 0.79, -10.6, -10.35, vector(0.60, 0.61, 0.63))
box(pos=vector(1.785, P + 0.89, -10.33), axis=vector(0.33, 0, 0), up=vector(0, 0.97, 0.25), height=0.22, width=0.008,
    color=vector(0.60, 0.61, 0.63))
table_lamp(3.5, P + 0.77, -10.05)
cylinder(pos=vector(3.25, P + 0.77, -10.55), axis=vector(0, 0.1, 0), radius=0.04, color=color.white)
cylinder(pos=vector(3.05, P + 0.77, -10.15), axis=vector(0, 0.12, 0), radius=0.035, color=FRAME)
potted_plant(1.7, P + 0.77, -10.0, 0.25)
for k in range(5):
    a = 2 * pi * k / 5
    cylinder(pos=vector(2.35, P + 0.06, -11.2), axis=vector(0.3 * cos(a), 0, 0.3 * sin(a)), radius=0.02, color=FRAME)
    sphere(pos=vector(2.35 + 0.3 * cos(a), P + 0.035, -11.2 + 0.3 * sin(a)), radius=0.035, color=FRAME)
cylinder(pos=vector(2.35, P + 0.06, -11.2), axis=vector(0, 0.36, 0), radius=0.028, color=CHROME)
block(2.07, 2.63, P + 0.42, P + 0.5, -11.45, -10.92, FRAME)
block(2.08, 2.62, P + 0.5, P + 0.57, -11.45, -10.95, LEATHER)
cylinder(pos=vector(2.08, P + 0.535, -10.95), axis=vector(0.54, 0, 0), radius=0.035, color=LEATHER)
box(pos=vector(2.35, P + 0.92, -11.53), axis=vector(0.52, 0, 0), up=vector(0, 0.97, -0.24), height=0.72, width=0.08,
    color=LEATHER)
box(pos=vector(2.35, P + 1.38, -11.63), axis=vector(0.34, 0, 0), up=vector(0, 0.97, -0.24), height=0.2, width=0.08,
    color=LEATHER)
for xa in (2.03, 2.67):
    block(xa - 0.02, xa + 0.02, P + 0.5, P + 0.72, -11.3, -11.25, FRAME)
    block(xa - 0.04, xa + 0.04, P + 0.72, P + 0.75, -11.4, -11.0, FRAME)
block(4.15, 4.52, P + 0.08, P + 0.68, -13.4, -11.2, KWOOD)
for xx in (4.2, 4.47):
    for zz in (-13.35, -11.25):
        block(xx - 0.02, xx + 0.02, P, P + 0.08, zz - 0.02, zz + 0.02, FRAME)
for zg in (-12.67, -11.93):
    block(4.146, 4.15, P + 0.12, P + 0.64, zg - 0.005, zg + 0.005, KGAP)
art("-x", 4.54, -13.1, -11.5, P + 1.2, P + 2.3, 1)
cylinder(pos=vector(4.3, P + 0.68, -12.9), axis=vector(0, 0.26, 0), radius=0.07, color=VASE)
for k in range(3):
    block(4.2, 4.46, P + 0.68 + k * 0.04, P + 0.71 + k * 0.04, -11.9, -11.55, BOOK_COLS[k + 2])
cylinder(pos=vector(3.4, 6.45, -7.665), axis=vector(0, 0, -0.03), radius=0.17, color=FRAME)
cylinder(pos=vector(3.4, 6.45, -7.695), axis=vector(0, 0, -0.005), radius=0.15, color=color.white)
for (dx, dy) in [(0, 0.1), (0.07, 0)]:
    block(3.4 - 0.008 + min(0, dx), 3.4 + 0.008 + max(0, dx), 6.45 - 0.008, 6.45 + dy + 0.008, -7.71, -7.7, FRAME)
armchair(3.95, -8.55, "+x", P, LEATHER, P_CREAM)
cylinder(pos=vector(3.1, P, -8.45), axis=vector(0, 0.5, 0), radius=0.03, color=FRAME)
cylinder(pos=vector(3.1, P + 0.5, -8.45), axis=vector(0, 0.03, 0), radius=0.25, color=KWOOD)
floor_lamp(4.35, P, -7.95)
big_plant(1.25, P, -13.4, 1.4)
curtain("x", -13.72, 0.75, 1.0, P + 0.1, 7.2)
curtain("x", -13.72, 4.0, 4.3, P + 0.1, 7.2)
pendant(2.6, 7.4, 6.5, -10.3, 0.12)
for (dx, dz) in [(1.5, -8.5), (3.5, -12.8), (1.5, -12.8)]:
    downlight(dx, 7.4, dz)

cylinder(pos=vector(7.3, P + 0.005, -11.25), axis=vector(0, 0.012, 0), radius=1.7, color=vector(0.60, 0.36, 0.26))
GLOSS = vector(0.05, 0.05, 0.06)
for (lx, lz) in [(6.45, -10.65), (6.45, -11.85), (8.0, -11.25)]:
    cylinder(pos=vector(lx, P, lz), axis=vector(0, 0.62, 0), radius=0.05, color=GLOSS)
    cylinder(pos=vector(lx, P, lz), axis=vector(0, 0.05, 0), radius=0.06, color=vector(0.8, 0.65, 0.3))
block(6.3, 7.5, P + 0.6, P + 0.95, -12.0, -10.5, GLOSS, shininess=1)
cylinder(pos=vector(7.5, P + 0.6, -11.25), axis=vector(0, 0.35, 0), radius=0.75, color=GLOSS, shininess=1)
block(5.95, 6.3, P + 0.62, P + 0.72, -11.95, -10.55, GLOSS)
block(5.97, 6.28, P + 0.72, P + 0.75, -11.9, -10.6, vector(0.97, 0.96, 0.92))
for k in range(36):
    if k % 7 in (2, 6):
        continue
    zk = -11.88 + k * (1.26 / 36) + 0.017
    block(6.12, 6.28, P + 0.75, P + 0.78, zk - 0.006, zk + 0.006, GLOSS)
block(6.28, 6.32, P + 0.75, P + 0.92, -11.95, -10.55, GLOSS)
block(6.42, 6.46, P + 0.95, P + 1.25, -11.55, -10.95, GLOSS)
block(6.4, 6.42, P + 1.0, P + 1.22, -11.45, -11.05, vector(0.95, 0.94, 0.9))
la = radians(35)
lid_c = vector(7.25, P + 0.95 + 0.75 * sin(la), -12.0 + 0.75 * cos(la))
box(pos=lid_c, axis=vector(1.9, 0, 0), up=vector(0, cos(la), -sin(la)), height=0.025, width=1.5, color=GLOSS)
cylinder(pos=vector(7.6, P + 0.95, -12.0 + 1.25 * cos(la)), axis=vector(0, 1.25 * sin(la), 0), radius=0.012,
         color=GLOSS)
bench_seat(5.4, 5.85, -11.6, -10.9, P, GLOSS, vector(0.15, 0.12, 0.12), h=0.5)


def studio_mic(base, top, aim, condenser=True):
    cylinder(pos=base, axis=vector(0, 0.02, 0), radius=0.16, color=FRAME)
    cylinder(pos=base, axis=top - base, radius=0.012, color=FRAME)
    d = norm(aim - top)
    tip = top + d * 0.55
    cylinder(pos=top, axis=tip - top, radius=0.009, color=FRAME)
    cylinder(pos=top - d * 0.2, axis=d * 0.2, radius=0.03, color=FRAME)
    if condenser:
        ring(pos=tip, axis=vector(0, 1, 0), radius=0.06, thickness=0.006, color=CHROME)
        cylinder(pos=tip + vector(0, -0.09, 0), axis=vector(0, 0.2, 0), radius=0.032, color=vector(0.75, 0.68, 0.45))
        sphere(pos=tip + vector(0, 0.115, 0), radius=0.033, color=vector(0.35, 0.35, 0.37))
        pf = tip + d * 0.16 + vector(0, 0.08, 0)
        ring(pos=pf, axis=d, radius=0.09, thickness=0.006, color=FRAME)
        cylinder(pos=pf, axis=d * 0.002, radius=0.085, color=vector(0.1, 0.1, 0.1), opacity=1)
    else:
        cylinder(pos=tip, axis=d * 0.12, radius=0.018, color=FRAME)
        sphere(pos=tip + d * 0.15, radius=0.03, color=vector(0.6, 0.6, 0.62))


studio_mic(vector(5.5, P, -9.2), vector(5.5, P + 1.55, -9.2), vector(6.2, P + 1.5, -8.5))
studio_mic(vector(5.0, P, -12.5), vector(5.0, P + 1.25, -12.5), vector(6.6, P + 0.9, -11.5))
studio_mic(vector(6.0, P, -7.6), vector(6.0, P + 1.45, -7.6), vector(6.0, P + 1.4, -8.4), condenser=False)
studio_mic(vector(9.6, P, -9.3), vector(9.6, P + 1.4, -9.3), vector(8.7, P + 1.0, -8.3))
DRUM = vector(0.55, 0.12, 0.12)
cylinder(pos=vector(8.7, P + 0.3, -8.1), axis=vector(-0.42, 0, 0), radius=0.28, color=DRUM)
cylinder(pos=vector(8.28, P + 0.3, -8.1), axis=vector(-0.01, 0, 0), radius=0.27, color=color.white)
for (tx, tz, tr, ty, th) in [(8.55, -7.92, 0.13, 0.72, 0.12), (8.55, -8.28, 0.13, 0.72, 0.12),
                             (8.95, -8.5, 0.18, 0.58, 0.14), (8.95, -7.55, 0.2, 0.25, 0.38)]:
    cylinder(pos=vector(tx, P + ty, tz), axis=vector(0, th, 0), radius=tr, color=DRUM)
    cylinder(pos=vector(tx, P + ty + th, tz), axis=vector(0, 0.005, 0), radius=tr - 0.01, color=color.white)
    for sgn in (-1, 1):
        cylinder(pos=vector(tx, P + ty + (th if sgn > 0 else 0), tz), axis=vector(0, 0.008 * sgn, 0),
                 radius=tr + 0.008, color=CHROME)
for (cx, cz, cy, cr) in [(9.05, -8.85, 0.9, 0.18), (8.35, -8.65, 1.25, 0.24), (8.4, -7.45, 1.15, 0.27)]:
    cylinder(pos=vector(cx, P, cz), axis=vector(0, cy, 0), radius=0.012, color=CHROME)
    cylinder(pos=vector(cx, P + cy, cz), axis=vector(0, 0.006, 0), radius=cr, color=vector(0.85, 0.68, 0.30))
cylinder(pos=vector(9.4, P, -8.1), axis=vector(0, 0.48, 0), radius=0.03, color=CHROME)
cylinder(pos=vector(9.4, P + 0.48, -8.1), axis=vector(0, 0.08, 0), radius=0.18, color=FRAME)
zs = -8.9
while zs < -6.7:
    block(9.72, 9.78, P + 0.3, 7.0, zs, zs + 0.06, KWOOD)
    zs += 0.11


def guitar(x, yc, z_wall, body, neck=vector(0.30, 0.18, 0.10)):
    zf = z_wall - 0.07
    ellipsoid(pos=vector(x, yc - 0.17, zf), size=vector(0.40, 0.44, 0.1), color=body)
    ellipsoid(pos=vector(x, yc + 0.12, zf), size=vector(0.31, 0.32, 0.1), color=body)
    cylinder(pos=vector(x, yc - 0.05, zf - 0.051), axis=vector(0, 0, -0.002), radius=0.055, color=vector(0.05, 0.04, 0.03))
    block(x - 0.05, x + 0.05, yc - 0.33, yc - 0.3, zf - 0.055, zf - 0.045, vector(0.2, 0.12, 0.06))
    block(x - 0.025, x + 0.025, yc + 0.22, yc + 0.68, zf - 0.03, zf + 0.01, neck)
    block(x - 0.045, x + 0.045, yc + 0.68, yc + 0.85, zf - 0.03, zf + 0.01, neck * 0.8)
    for sx in (-0.012, -0.004, 0.004, 0.012):
        block(x + sx - 0.0012, x + sx + 0.0012, yc - 0.31, yc + 0.68, zf - 0.058, zf - 0.055, CHROME)
    block(x - 0.03, x + 0.03, yc + 0.85, yc + 0.9, z_wall - 0.05, z_wall, FRAME)


for (gx, gc) in [(6.6, vector(0.80, 0.56, 0.32)), (7.5, vector(0.40, 0.18, 0.08)), (8.4, vector(0.10, 0.10, 0.11))]:
    guitar(gx, P + 1.45, -6.585, gc)
for i, zp in enumerate([-13.2, -12.45, -11.7, -10.95, -10.2, -9.45, -8.7]):
    for j, yp in enumerate([P + 1.0, P + 1.75]):
        pc = [vector(0.30, 0.27, 0.25), vector(0.55, 0.35, 0.22), vector(0.82, 0.78, 0.70)][(i + j) % 3]
        block(4.66, 4.72, yp, yp + 0.65, zp, zp + 0.68, pc)
for (cx, cz) in [(6.4, -10.0), (8.2, -10.0), (7.3, -12.2)]:
    block(cx - 0.6, cx + 0.6, 6.88, 6.93, cz - 0.6, cz + 0.6, vector(0.86, 0.82, 0.76))
    for sx in (-0.5, 0.5):
        cylinder(pos=vector(cx + sx, 6.93, cz), axis=vector(0, 0.45, 0), radius=0.003, color=FRAME)


def big_speaker(x, z, face_z=1):
    zf = z + 0.19 * face_z
    block(x - 0.2, x + 0.2, P, P + 0.04, z - 0.22, z + 0.22, vector(0.25, 0.25, 0.27))
    block(x - 0.18, x + 0.18, P + 0.04, P + 1.25, z - 0.19, z + 0.19, FRAME)
    for (yy, rr) in [(P + 0.35, 0.13), (P + 0.72, 0.13)]:
        cylinder(pos=vector(x, yy, zf), axis=vector(0, 0, 0.012 * face_z), radius=rr + 0.012, color=CHROME)
        cylinder(pos=vector(x, yy, zf + 0.012 * face_z), axis=vector(0, 0, 0.004 * face_z), radius=rr,
                 color=vector(0.08, 0.08, 0.09))
        sphere(pos=vector(x, yy, zf + 0.01 * face_z), radius=0.04, color=vector(0.2, 0.2, 0.22))
    block(x - 0.12, x + 0.12, P + 0.98, P + 1.14, zf, zf + 0.012 * face_z, vector(0.22, 0.22, 0.24))
    block(x - 0.04, x + 0.04, P + 1.04, P + 1.08, zf + 0.012 * face_z, zf + 0.016 * face_z, CHROME)


big_speaker(5.4, -13.5)
big_speaker(9.45, -13.5)
block(5.05, 5.55, P, P + 0.95, -7.05, -6.62, FRAME)
for (yy, rr) in [(P + 0.28, 0.17), (P + 0.66, 0.17)]:
    ring(pos=vector(5.3, yy, -7.06), axis=vector(0, 0, 1), radius=rr, thickness=0.012, color=vector(0.55, 0.85, 1.0),
         emissive=True)
    cylinder(pos=vector(5.3, yy, -7.06), axis=vector(0, 0, 0.004), radius=rr - 0.015, color=vector(0.1, 0.1, 0.11))
block(5.15, 5.45, P + 0.86, P + 0.92, -7.07, -7.05, vector(0.3, 0.3, 0.32))
block(9.15, 9.78, P + 0.72, P + 0.77, -12.4, -9.8, KWOOD)
for zz in (-12.35, -9.85):
    block(9.18, 9.75, P, P + 0.72, zz - 0.03, zz + 0.03, KWOOD)
block(9.25, 9.6, P + 0.77, P + 0.81, -11.7, -10.5, FRAME)
block(9.3, 9.42, P + 0.81, P + 0.815, -11.65, -10.55, vector(0.95, 0.95, 0.92))
block(9.5, 9.75, P + 0.77, P + 0.79, -12.2, -11.85, vector(0.60, 0.61, 0.63))
box(pos=vector(9.72, P + 0.9, -12.02), axis=vector(0, 0, 0.35), up=vector(0.25, 0.97, 0), height=0.22,
    width=0.008, color=vector(0.60, 0.61, 0.63))
block(9.5, 9.7, P + 0.77, P + 0.83, -10.3, -10.0, vector(0.75, 0.15, 0.12))
for zz in (-12.25, -9.95):
    block(9.45, 9.75, P + 0.77, P + 1.15, zz - 0.12, zz + 0.12, FRAME)
    cylinder(pos=vector(9.45, P + 0.88, zz), axis=vector(-0.01, 0, 0), radius=0.08, color=vector(0.25, 0.25, 0.27))
    cylinder(pos=vector(9.45, P + 1.06, zz), axis=vector(-0.01, 0, 0), radius=0.035, color=CHROME)
ring(pos=vector(9.55, P + 0.95, -11.0), axis=vector(1, 0, 0), radius=0.09, thickness=0.012, color=FRAME)
for (dx, dz) in [(5.6, -8.0), (8.4, -10.0), (6.4, -12.6), (8.6, -12.6)]:
    downlight(dx, 7.4, dz)
block(4.75, 9.75, 7.05, 7.08, -6.68, -6.62, LAMP, emissive=True)

for (dx, dz) in [(4.0, -9.0), (4.0, -12.6), (7.4, -12.6)]:
    downlight(dx, 3.95, dz)

ROOF_START = len(ALL_OBJ)

hip_roof(-14, -3, -6, 4, 7.4, 20, over=1.0, gable_east=True)
B_PITCH, B_OVER = 32, 0.6
hip_roof(-3, 10, -6.5, 5.4, F2, B_PITCH, over=B_OVER)
ky = F2 + (2.0 - B_OVER) * tan(radians(B_PITCH))
kx = -3 - B_OVER + 2.0
tri(vector(-3, F2, 4.0), vector(2, F2, 4.0), vector(2, ky, 4.0), EXT)
tri(vector(-3, F2, 4.0), vector(2, ky, 4.0), vector(kx, ky, 4.0), EXT)
tri(vector(1.9, F2, 4.0), vector(1.9, F2, 5.4), vector(1.9, ky, 4.0), EXT)
block(0.6, 9.8, 7.36, 7.4, -13.8, -6.6, CEILING)
block(0.3, 10.1, 7.4, 7.6, -14.15, -6.5, ROOF)
for (x1, x2, z1, z2) in [(0.22, 10.18, -14.22, -14.1), (0.22, 0.34, -14.22, -6.5), (10.06, 10.18, -14.22, -6.5)]:
    block(x1, x2, 7.3, 7.68, z1, z2, ROOF)
block(-21.35, -13.85, 3.95, 4.12, -8.95, -2.95, ROOF)
for (x1, x2, z1, z2) in [(-21.42, -13.8, -9.02, -8.9), (-21.42, -21.3, -9.02, -2.95), (-13.95, -13.8, -9.02, -5.95)]:
    block(x1, x2, 3.85, 4.16, z1, z2, ROOF)

ROOF_END = len(ALL_OBJ)

MULCH      = vector(0.30, 0.20, 0.13)
STONE_EDGE = vector(0.86, 0.85, 0.81)
GRASS_2    = vector(0.37, 0.65, 0.28)
PINK       = vector(0.88, 0.22, 0.58)
ORANGE     = vector(0.97, 0.50, 0.18)
CREAM      = vector(0.98, 0.92, 0.70)
PURPLE     = vector(0.65, 0.35, 0.85)
FERN       = vector(0.18, 0.45, 0.20)


def garden_bed(x1, x2, z1, z2):
    block(x1, x2, 0.0, 0.06, z1, z2, MULCH)
    for (a1, a2, b1, b2) in [(x1, x2, z1, z1 + 0.1), (x1, x2, z2 - 0.1, z2),
                             (x1, x1 + 0.1, z1, z2), (x2 - 0.1, x2, z1, z2)]:
        block(a1, a2, 0.0, 0.13, b1, b2, STONE_EDGE)


def flower_bush(x, z, r=0.45, fcol=PINK, n=10, y=0.0):
    leafy_bush(x, z, r, y, vector(0.20, 0.48, 0.20))
    rng = Random(int(x * 37 + z * 71 + 5))
    c = vector(x, y + r * 0.78, z)
    for k in range(7):
        ang = 2 * pi * k / 7 + rng.uniform(-0.3, 0.3)
        el = rng.uniform(0.15, 1.1)
        d = vector(cos(ang) * cos(el), sin(el), sin(ang) * cos(el))
        sphere(pos=c + d * r * 0.98, radius=r * 0.13, color=fcol * rng.uniform(0.92, 1.0), lowpoly=True)


def grass_clump(x, z, h=0.9, col=vector(0.45, 0.62, 0.25), y=0.0):
    for k in range(4):
        ang = 2 * pi * k / 4 + 0.4
        d = norm(vector(0.4 * cos(ang), 1, 0.4 * sin(ang)))
        ellipsoid(pos=vector(x, y, z) + d * h / 2, axis=d * h, up=vector(-sin(ang), 0, cos(ang)),
                  height=0.16, width=0.03, color=col, lowpoly=True)


def topiary(x, z, r=0.4, y=0.0):
    leafy_bush(x, z, r, y, vector(0.16, 0.40, 0.17), tight=True)


def bollard(x, z, y=0.0):
    cylinder(pos=vector(x, y, z), axis=vector(0, 0.6, 0), radius=0.07, color=FRAME)
    cylinder(pos=vector(x, y + 0.6, z), axis=vector(0, 0.08, 0), radius=0.075, color=LAMP, emissive=True)
    cylinder(pos=vector(x, y + 0.68, z), axis=vector(0, 0.03, 0), radius=0.1, color=FRAME)


def flowering_tree(x, z, h=3.0, flower=color.white):
    rng = Random(int(x * 59 + z * 97 + 3))
    base = vector(x, 0, z)
    cone(pos=base, axis=vector(0, 0.35, 0), radius=0.24, color=TREE_BARK)
    cylinder(pos=base, axis=vector(0, h * 0.55, 0), radius=0.14, color=TREE_BARK)
    fork = base + vector(0, h * 0.55, 0)
    for k in range(4):
        ang = 2 * pi * k / 4 + 0.3 + rng.uniform(-0.3, 0.3)
        tip = fork + vector(0.9 * cos(ang), h * rng.uniform(0.32, 0.45), 0.9 * sin(ang))
        cylinder(pos=fork, axis=tip - fork, radius=0.08, color=TREE_BARK)
        leaf_canopy(tip + vector(0, 0.12, 0), 0.55, 0.38, 0.55, rng, 5)
        for j in range(5):
            a2 = 2 * pi * j / 5 + k
            sphere(pos=tip + vector(0.38 * cos(a2), 0.42, 0.38 * sin(a2)), radius=0.09, color=flower)


def garden_bench(x, z, face):
    dx, dz = DIRS[face]
    if dx == 0:
        block(x - 0.8, x + 0.8, 0.42, 0.48, z - 0.25, z + 0.25, WOOD)
        for sx in (-0.7, 0.7):
            block(x + sx - 0.05, x + sx + 0.05, 0, 0.42, z - 0.22, z + 0.22, FRAME)
        bz = z - dz * 0.24
        block(x - 0.8, x + 0.8, 0.48, 0.92, bz - 0.03, bz + 0.03, WOOD)
    else:
        block(x - 0.25, x + 0.25, 0.42, 0.48, z - 0.8, z + 0.8, WOOD)
        for sz in (-0.7, 0.7):
            block(x - 0.22, x + 0.22, 0, 0.42, z + sz - 0.05, z + sz + 0.05, FRAME)
        bx = x - dx * 0.24
        block(bx - 0.03, bx + 0.03, 0.48, 0.92, z - 0.8, z + 0.8, WOOD)


v = -13.9
k = 0
while v < 17.8:
    if k % 2 == 0:
        block(v, min(v + 1.5, 17.8), 0.0, 0.004, 4.3, 10.8, GRASS_2)
    v += 1.5
    k += 1
v = -20.3
k = 0
while v < -3.0:
    if k % 2 == 0:
        block(-27.7, -4.0, 0.0, 0.004, v, min(v + 1.5, -3.0), GRASS_2)
    v += 1.5
    k += 1

palm(-3.8, 8.2, 7.0)
palm(0.2, 7.6, 6.2, lean=vector(-0.1, 0, 0.1))
palm(8.0, 8.4, 7.4)
garden_bed(-13.8, 0.95, 4.4, 5.6)
xg = -13.2
i = 0
while xg < 0.6:
    if i % 3 == 0:
        topiary(xg, 5.0, 0.38, 0.06)
    elif i % 3 == 1:
        flower_bush(xg, 5.0, 0.32, [PINK, color.white, CREAM][(i // 3) % 3], 8, 0.06)
    else:
        grass_clump(xg, 5.0, 0.8, y=0.06)
    xg += 0.75
    i += 1
garden_bed(6.1, 9.95, 5.8, 6.9)
for xg, kind in [(6.5, 0), (7.3, 1), (8.1, 2), (8.9, 1), (9.6, 0)]:
    if kind == 0:
        topiary(xg, 6.35, 0.35, 0.06)
    elif kind == 1:
        flower_bush(xg, 6.35, 0.33, ORANGE, 8, 0.06)
    else:
        grass_clump(xg, 6.35, 0.9, y=0.06)
garden_bed(-5.0, 1.4, 6.8, 9.1)
for (xg, zg, kind) in [(-4.5, 7.2, 1), (-3.0, 7.0, 2), (-1.6, 7.4, 1), (-0.6, 8.6, 2), (0.9, 8.5, 1),
                       (-2.4, 8.7, 0), (-4.5, 8.7, 2), (1.0, 7.2, 0)]:
    if kind == 0:
        topiary(xg, zg, 0.3, 0.06)
    elif kind == 1:
        flower_bush(xg, zg, 0.3, [PINK, PURPLE][int(xg) % 2], 8, 0.06)
    else:
        grass_clump(xg, zg, 0.7, FERN, 0.06)
garden_bed(6.8, 9.3, 7.5, 9.3)
for (xg, zg) in [(7.2, 7.9), (8.8, 8.9), (7.3, 8.9)]:
    grass_clump(xg, zg, 0.7, FERN, 0.06)
flower_bush(8.8, 7.9, 0.3, color.white, 8, 0.06)
garden_bed(-13.3, 2.8, 9.7, 10.8)
garden_bed(6.5, 17.6, 9.7, 10.8)
for xg in [-12.8 + 1.2 * n for n in range(13)] + [7.0 + 1.2 * n for n in range(9)]:
    n = int(round(xg * 10)) % 3
    if n == 0:
        grass_clump(xg, 10.25, 1.2, y=0.06)
    elif n == 1:
        flower_bush(xg, 10.25, 0.4, PINK, 10, 0.06)
    else:
        topiary(xg, 10.25, 0.38, 0.06)
for zg in (6.6, 8.2, 9.6):
    bollard(2.95, zg)
    bollard(4.65, zg)
for zg in (5.6, 7.6, 9.6):
    bollard(-13.75, zg)

garden_bed(16.9, 17.8, -13.8, 9.5)
zg = -13.3
i = 0
while zg < 9.2:
    if i % 2 == 0:
        grass_clump(17.35, zg, 1.6, vector(0.35, 0.58, 0.22), 0.06)
    else:
        flower_bush(17.35, zg, 0.38, [PINK, ORANGE, color.white][i % 3], 9, 0.06)
    zg += 1.1
    i += 1

garden_bench(-19.0, -10.6, "-z")
garden_bench(-21.5, -12.0, "+x")
garden_bed(-27.7, -13.3, -21.8, -20.3)
xg = -27.0
i = 0
while xg < -17.5:
    m = i % 4
    if m == 0:
        flower_bush(xg, -21.05, 0.45, [PINK, ORANGE, PURPLE, CREAM][(i // 4) % 4], 10, 0.06)
    elif m == 1:
        grass_clump(xg, -21.05, 1.3, y=0.06)
    elif m == 2:
        topiary(xg, -21.05, 0.42, 0.06)
    else:
        grass_clump(xg, -21.05, 0.9, FERN, 0.06)
    xg += 1.05
    i += 1
garden_bed(-27.7, -26.6, -20.2, -3.5)
zg = -19.6
while zg < -3.8:
    flower_bush(-27.15, zg, 0.45, PINK, 10, 0.06)
    zg += 1.3
garden_bed(-25.8, -21.4, -4.3, -3.06)
for xg in [-25.3 + 0.9 * n for n in range(4)]:
    if int(round((xg + 30) / 0.9)) % 2:
        topiary(xg, -3.7, 0.33, 0.06)
    else:
        flower_bush(xg, -3.7, 0.3, color.white, 8, 0.06)
garden_bed(-13.8, -6.3, -7.3, -6.1)
for i, xg in enumerate((-13.3, -12.3, -11.3, -10.3, -9.3, -8.3, -7.3)):
    if i % 2 == 0:
        topiary(xg, -6.7, 0.3, 0.06)
    else:
        grass_clump(xg, -6.7, 0.7, FERN, 0.06)

round_tree(-24.5, -18.0, 3.4, 1.9)
flowering_tree(-19.5, -16.0, 3.0, color.white)
flowering_tree(-22.2, -14.6, 2.8, CREAM)
flowering_tree(-23.5, -7.6, 2.8, vector(0.98, 0.65, 0.75))


def cypress(x, z, h=4.5):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 0.5, 0), radius=0.08, color=TRUNK)
    ellipsoid(pos=vector(x, 0.4 + h / 2, z), size=vector(0.85, h, 0.85), color=vector(0.12, 0.33, 0.15))
    ellipsoid(pos=vector(x, 0.4 + h * 0.62, z), size=vector(0.6, h * 0.7, 0.6), color=vector(0.15, 0.38, 0.17))


for xg in (-16.8, -15.6, -14.4):
    cypress(xg, -21.0, 4.8)
for (xg, zg) in [(-13.9, -17.0), (-14.0, -16.0), (-13.8, -15.0)]:
    grass_clump(xg, zg, 1.5, vector(0.45, 0.62, 0.25))
flower_bush(-14.6, -16.4, 0.45, PURPLE, 8)

garden_bed(13.6, 17.8, -21.8, -14.2)
palm(15.5, -19.0, 6.0, lean=vector(-0.1, 0, 0.05))
palm(16.6, -15.6, 5.0, lean=vector(-0.05, 0, -0.08))
cypress(17.2, -21.1, 4.6)
cypress(14.3, -21.1, 4.2)
for (xg, zg) in [(14.2, -17.2), (13.9, -15.0), (17.2, -17.6)]:
    grass_clump(xg, zg, 1.1, FERN, 0.06)
for (xg, zg, fc) in [(14.6, -20.0, ORANGE), (16.4, -20.4, PINK), (14.0, -18.6, ORANGE), (15.4, -15.0, CREAM)]:
    flower_bush(xg, zg, 0.4, fc, 10, 0.06)

for xg in (-26.0, -21.0, -11.0, -3.0, 6.0):
    for dx, dy, dz in [(0, 0, 0), (0.45, -0.25, 0.1), (-0.4, -0.3, 0.2)]:
        flower_bush(xg + dx, -21.8 + dz, 0.38, PINK, 6, 2.25 + dy)

TERRACE_START = len(ALL_OBJ)

OUT_FRAME = vector(0.20, 0.20, 0.21)
OUT_CUSH = vector(0.90, 0.87, 0.80)
OUT_SOFA = vector(0.70, 0.55, 0.40)
TEAK = vector(0.46, 0.30, 0.17)
TEAL = vector(0.15, 0.50, 0.55)
TY = F1 + 0.015

zp = -3.0
while zp < 6.19:
    xa, xb = (-26.3, -13.8) if zp >= 4.5 else (-26.0, -14.0)
    block(xa, xb, F1, TY, zp + 0.012, min(zp + 0.15, 6.2), DECK_WOOD)
    zp += 0.16


def outdoor_sofa(x1, x2, z1, z2, y, back, ends=("arm", "arm"), pillows=()):
    sofa(x1, x2, z1, z2, y, back, OUT_SOFA, ends=ends, pillows=pillows, base=TEAK, arm_col=TEAK,
         legs=TEAK * 0.8)


RATTAN = vector(0.72, 0.54, 0.33)
EGG_CUSHION = vector(0.95, 0.92, 0.85)
JUTE = vector(0.78, 0.66, 0.48)


def egg_chair(x, zc, y, pillow=vector(0.70, 0.45, 0.50)):
    c = vector(x, y + 1.0, zc)
    sb = vector(x, y, zc - 0.68)
    cylinder(pos=sb, axis=vector(0, 0.04, 0), radius=0.36, color=FRAME)
    cylinder(pos=sb, axis=vector(0, 2.0, 0), radius=0.035, color=FRAME)
    p = sb + vector(0, 2.0, 0)
    for k in range(6):
        a = (pi / 2) * (k + 1) / 6
        q = sb + vector(0, 2.0 + 0.3 * sin(a), 0.68 * (1 - cos(a)))
        cylinder(pos=p, axis=q - p, radius=0.035, color=FRAME)
        p = q
    top = vector(x, y + 1.66, zc - 0.05)
    cylinder(pos=top, axis=p - top, radius=0.01, color=vector(0.35, 0.35, 0.36))
    RX, RY, RZ = 0.5, 0.66, 0.46

    def pt(th, ph):
        return c + vector(RX * cos(ph) * sin(th), RY * sin(ph), -RZ * cos(ph) * cos(th))

    def strip(points, r, col):
        for p1, p2 in zip(points[:-1], points[1:]):
            cylinder(pos=p1, axis=p2 - p1, radius=r, color=col)

    side = radians(105)
    lip = radians(-38)
    for k in range(15):
        th = -side + 2 * side * k / 14
        strip([pt(th, radians(-88 + 176 * j / 9)) for j in range(10)], 0.014, RATTAN * (0.92 if k % 2 else 1.0))
    for k in range(9):
        th = side + (2 * pi - 2 * side) * (k + 0.5) / 9
        strip([pt(th, radians(-88 + (-38 + 88) * j / 4)) for j in range(5)], 0.014, RATTAN)
    for ph_d in (-70, -55, -38, -15, 10, 35, 58):
        ph = radians(ph_d)
        if ph_d <= -38:
            ths = [2 * pi * j / 24 for j in range(25)]
        else:
            ths = [-side + 2 * side * j / 16 for j in range(17)]
        strip([pt(th, ph) for th in ths], 0.01, RATTAN * 0.8)
    rim = ([pt(-side, radians(-38 + 128 * j / 10)) for j in range(11)] +
           [pt(side, radians(90 - 128 * j / 10)) for j in range(1, 11)] +
           [pt(side + (2 * pi - 2 * side) * j / 10, lip) for j in range(1, 11)])
    strip(rim, 0.03, RATTAN * 0.95)
    ellipsoid(pos=c + vector(0, 0.05, -0.2), size=vector(0.8, 1.02, 0.4), color=EGG_CUSHION)
    ellipsoid(pos=c + vector(0, -0.33, 0.02), size=vector(0.82, 0.24, 0.72), color=EGG_CUSHION)
    soft_pillow(c + vector(0, -0.02, 0.05), vector(1, 0, 0), norm(vector(0, 0.95, -0.3)), 0.44, 0.42, 0.15, pillow)


def rattan_table(x, z, y, r=0.32, h=0.46):
    cylinder(pos=vector(x, y, z), axis=vector(0, h, 0), radius=r, color=RATTAN)
    for f in (0.15, 0.5, 0.85):
        ring(pos=vector(x, y + h * f, z), axis=vector(0, 1, 0), radius=r, thickness=0.012, color=RATTAN * 0.78)
    cylinder(pos=vector(x, y + h, z), axis=vector(0, 0.03, 0), radius=r + 0.02, color=RATTAN * 0.92)


def string_lights(p, q, sag=0.3, n=12):
    prev = p
    for i in range(1, n + 1):
        f = i / n
        pt = p + (q - p) * f - vector(0, sag * 4 * f * (1 - f), 0)
        cylinder(pos=prev, axis=pt - prev, radius=0.006, color=FRAME)
        sphere(pos=pt - vector(0, 0.06, 0), radius=0.045, color=LAMP, emissive=True)
        prev = pt


def planter(x1, x2, z1, z2, y, h=0.55):
    block(x1, x2, y, y + h, z1, z2, vector(0.28, 0.29, 0.30))
    block(x1 + 0.05, x2 - 0.05, y + h - 0.02, y + h + 0.01, z1 + 0.05, z2 - 0.05, MULCH)
    xg = x1 + 0.35
    i = 0
    while xg < x2 - 0.2:
        if i % 2 == 0:
            grass_clump(xg, (z1 + z2) / 2, 0.9, y=y + h)
        else:
            flower_bush(xg, (z1 + z2) / 2, 0.22, [PINK, color.white][(i // 2) % 2], 7, y + h)
        xg += 0.55
        i += 1


def lantern(x, z, y, h=0.5):
    block(x - 0.13, x + 0.13, y, y + h, z - 0.13, z + 0.13, OUT_FRAME, opacity=0.6)
    cylinder(pos=vector(x, y + 0.05, z), axis=vector(0, h * 0.5, 0), radius=0.06, color=LAMP, emissive=True)


for px in (-25.7, -20.3):
    for pz in (1.9, 5.9):
        block(px - 0.08, px + 0.08, TY, TY + 2.6, pz - 0.08, pz + 0.08, OUT_FRAME)
for pz in (1.9, 5.9):
    block(-25.85, -20.15, TY + 2.6, TY + 2.78, pz - 0.1, pz + 0.1, OUT_FRAME)
xs = -25.7
while xs <= -20.29:
    block(xs - 0.04, xs + 0.04, TY + 2.78, TY + 2.86, 1.7, 6.1, OUT_FRAME)
    xs += 0.36
for xs in (-25.2, -24.0, -22.8, -21.6, -20.6):
    string_lights(vector(xs, TY + 2.55, 1.9), vector(xs, TY + 2.55, 5.9))

rug(-25.3, -21.2, 2.3, 5.5, TY, vector(0.62, 0.55, 0.45))
rug(-25.1, -21.4, 2.5, 5.3, TY + 0.006, vector(0.85, 0.80, 0.70))
outdoor_sofa(-25.5, -21.6, 5.0, 5.85, TY, "+z", ends=("back", "arm"), pillows=[P_CREAM, P_COCOA, P_SAND, P_CREAM])
outdoor_sofa(-25.6, -24.75, 2.5, 5.0, TY, "-x", ends=("arm", None), pillows=[P_COCOA, P_CREAM])
outdoor_sofa(-21.9, -21.05, 2.6, 3.45, TY, "+x")
outdoor_sofa(-21.9, -21.05, 3.85, 4.7, TY, "+x")
block(-24.0, -22.5, TY, TY + 0.38, 3.2, 4.3, WOOD)
block(-23.9, -22.6, TY + 0.38, TY + 0.41, 3.3, 4.2, vector(0.66, 0.45, 0.26))
lantern(-23.6, 3.6, TY + 0.41, 0.3)
cylinder(pos=vector(-22.9, TY + 0.41, 3.9), axis=vector(0, 0.12, 0), radius=0.12, color=color.white)
grass_clump(-22.9, 3.9, 0.35, FERN, TY + 0.53)
lantern(-25.45, 2.15, TY)
lantern(-20.7, 5.55, TY)

cylinder(pos=vector(-23.6, TY, -1.0), axis=vector(0, 0.72, 0), radius=0.06, color=OUT_FRAME)
cylinder(pos=vector(-23.6, TY + 0.72, -1.0), axis=vector(0, 0.04, 0), radius=0.6, color=color.white)
for (cx, cz, face) in [(-23.6, -1.8, "+z"), (-23.6, -0.2, "-z"), (-24.4, -1.0, "+x"), (-22.8, -1.0, "-x")]:
    chair(cx, cz, face, TY, OUT_CUSH, OUT_FRAME)
cylinder(pos=vector(-23.6, TY + 0.76, -1.0), axis=vector(0, 1.7, 0), radius=0.03, color=OUT_FRAME)
cone(pos=vector(-23.6, TY + 2.25, -1.0), axis=vector(0, 0.55, 0), radius=1.6, color=vector(0.92, 0.88, 0.78))
sphere(pos=vector(-23.6, TY + 2.82, -1.0), radius=0.06, color=OUT_FRAME)
cylinder(pos=vector(-23.6, TY + 0.76, -1.0), axis=vector(0, 0.2, 0), radius=0.07, color=color.white)
for dx in (-0.3, 0.3):
    cylinder(pos=vector(-23.6 + dx, TY + 0.76, -1.0), axis=vector(0, 0.02, 0), radius=0.13,
             color=color.white)

for (ex, pc) in [(-18.75, vector(0.70, 0.45, 0.50)), (-16.05, vector(0.62, 0.50, 0.40))]:
    cylinder(pos=vector(ex, TY + 0.003, 4.75), axis=vector(0, 0.008, 0), radius=0.95, color=JUTE)
    ring(pos=vector(ex, TY + 0.01, 4.75), axis=vector(0, 1, 0), radius=0.95, thickness=0.02, color=JUTE * 0.85)
    egg_chair(ex, 4.75, TY, pc)
rattan_table(-17.4, 4.95, TY)
lantern(-17.4, 4.95, TY + 0.49, 0.3)
block(-17.62, -17.42, TY + 0.49, TY + 0.53, 4.75, 4.95, vector(0.85, 0.80, 0.72))
for (px, pz) in [(-19.85, 5.5), (-15.0, 5.5)]:
    cylinder(pos=vector(px, TY, pz), axis=vector(0, 0.55, 0), radius=0.26, color=vector(0.86, 0.82, 0.76))
    potted_plant(px, TY + 0.4, pz, 1.1)

planter(-25.9, -21.2, -2.9, -2.45, TY)
planter(-20.4, -17.4, -2.9, -2.45, TY)
planter(-16.9, -14.3, -2.9, -2.45, TY)
planter(-25.95, -25.5, -1.6, 1.4, TY)
big_plant(-14.5, TY, 5.7, 1.5)
big_plant(-14.5, TY, -0.4, 1.3)
potted_plant(-14.5, TY, 2.4, 1.0)
block(-14.25, -14.06, 6.0, 6.35, 1.0, 1.25, OUT_FRAME)
block(-14.24, -14.1, 6.05, 6.3, 1.03, 1.22, LAMP, emissive=True)


TERRACE_END = len(ALL_OBJ)

D = 0.5
WL = 0.45
PAVER = vector(0.88, 0.87, 0.84)
PAVER_LINE = vector(0.74, 0.73, 0.70)
POOL_DARK = vector(0.05, 0.28, 0.48)
WATER2 = vector(0.08, 0.45, 0.75)
STONE_WALL = vector(0.80, 0.79, 0.76)
PURE_WHITE = vector(0.97, 0.97, 0.95)

W1 = (-5.0, 9.4, -20.2, -15.2)
W2 = (-12.0, -5.0, -20.2, -11.2)
SPA = (9.4, 12.6, -20.0, -16.6)
PIT = (-11.0, -6.6, -18.4, -14.0)
PATH_A = (-9.6, -8.2, -14.0, -11.2)
PATH_B = (1.0, 2.6, -20.2, -15.2)

for (x1, x2, z1, z2) in rect_minus([(-13.0, 13.5, -21.6, -14.0), (-13.0, 1.7, -14.0, -8.0)], [W1, W2, SPA]):
    add_solid(x1, x2, 0, D, z1, z2)
    block(x1, x2, 0, D - 0.02, z1, z2, vector(0.80, 0.79, 0.76))
    block(x1, x2, D - 0.02, D, z1, z2, PAVER)
    v = ceil(x1)
    while v < x2:
        block(v - 0.008, v + 0.008, D, D + 0.003, z1, z2, PAVER_LINE)
        v += 1.0
    v = ceil(z1)
    while v < z2:
        block(x1, x2, D, D + 0.003, v - 0.008, v + 0.008, PAVER_LINE)
        v += 1.0

POOL_WATERS = []
for (x1, x2, z1, z2) in rect_minus([W1, W2], [PIT]):
    block(x1, x2, 0, 0.05, z1, z2, POOL_DARK)
    POOL_WATERS.append(block(x1, x2, 0.05, WL, z1, z2, WATER2, opacity=0.6, shininess=1))
for (x1, x2, z1, z2) in [(-12.3, 9.7, -20.5, -20.2), (-5.3, 9.7, -15.2, -14.9), (-5.0, -4.7, -15.2, -10.9),
                         (-12.3, -4.7, -11.2, -10.9), (-12.3, -12.0, -20.5, -10.9), (9.4, 9.7, -20.5, -14.9)]:
    block(x1, x2, D, D + 0.025, z1, z2, PURE_WHITE)
for (x1, x2, z1, z2) in [(-12.0, 9.4, -20.2, -20.16), (-5.0, 9.4, -15.24, -15.2), (-5.04, -5.0, -15.2, -11.2),
                         (-12.0, -5.0, -11.24, -11.2), (-12.0, -11.96, -20.2, -11.2)]:
    block(x1, x2, 0.05, D, z1, z2, POOL_DARK * 1.3)
for xl in (-10.0, -6.0, -2.0, 3.5, 7.0):
    cylinder(pos=vector(xl, 0.25, -20.16), axis=vector(0, 0, 0.01), radius=0.09, color=LAMP, emissive=True)
for (x1, x2, z1, z2) in rect_minus([W1, W2], [PATH_A, PATH_B, PIT]):
    add_solid(x1, x2, 0, 1.2, z1, z2)

for (x1, x2, z1, z2) in [(-9.6, -8.2, -12.45, -11.55), (-9.6, -8.2, -13.65, -12.8),
                         (1.0, 2.6, -16.75, -15.55), (1.0, 2.6, -18.3, -17.1), (1.0, 2.6, -19.85, -18.65)]:
    block(x1, x2, 0, D + 0.02, z1, z2, PURE_WHITE, solid=True)
for (x1, x2, z1, z2) in [(-9.6, -8.2, -11.55, -11.2), (-9.6, -8.2, -12.8, -12.45), (-9.6, -8.2, -14.0, -13.65),
                         (1.0, 2.6, -15.55, -15.2), (1.0, 2.6, -17.1, -16.75), (1.0, 2.6, -18.65, -18.3),
                         (1.0, 2.6, -20.2, -19.85)]:
    add_solid(x1, x2, 0, D + 0.02, z1, z2)

PT = 0.55
for (x1, x2, z1, z2) in [(-11.0, -6.6, -18.4, -18.2), (-11.0, -10.8, -18.2, -14.0), (-6.8, -6.6, -18.2, -14.0),
                         (-11.0, -9.6, -14.2, -14.0), (-8.2, -6.6, -14.2, -14.0)]:
    block(x1, x2, 0, PT, z1, z2, PURE_WHITE, solid=True)
block(-9.6, -8.2, 0, D + 0.02, -14.2, -14.0, PURE_WHITE, solid=True)
block(-9.6, -8.2, 0, 0.27, -14.6, -14.2, PURE_WHITE, solid=True)
block(-10.8, -6.8, 0, 0.02, -18.2, -14.2, vector(0.72, 0.72, 0.70), solid=True)
SEAT = OUT_SOFA
for (x1, x2, z1, z2) in [(-10.8, -10.1, -17.5, -14.9), (-10.8, -6.8, -18.2, -17.5), (-7.5, -6.8, -17.5, -14.9)]:
    block(x1, x2, 0.02, 0.38, z1, z2, PURE_WHITE)
    block(x1 + 0.03, x2 - 0.03, 0.38, 0.5, z1 + 0.03, z2 - 0.03, SEAT)
for (x1, x2, z1, z2) in [(-10.8, -10.6, -18.2, -14.9), (-10.8, -6.8, -18.2, -18.0), (-7.0, -6.8, -18.2, -14.9)]:
    block(x1, x2, 0.5, 0.88, z1, z2, SEAT)
for (x1, x2, z1, z2, cc) in [(-10.6, -10.42, -17.9, -17.5, P_COCOA),
                             (-10.2, -9.8, -17.98, -17.8, P_CREAM),
                             (-7.6, -7.2, -17.98, -17.8, P_COCOA),
                             (-6.98, -6.8, -16.0, -15.6, P_CREAM),
                             (-10.6, -10.42, -15.6, -15.2, P_COCOA)]:
    block(x1, x2, 0.5, 0.84, z1, z2, cc)
block(-10.1, -7.5, 0.02, 0.03, -17.5, -14.9, vector(0.85, 0.82, 0.75))
FP = vector(-8.8, 0.02, -16.2)
cylinder(pos=FP, axis=vector(0, 0.38, 0), radius=0.6, color=vector(0.75, 0.74, 0.72))
ring(pos=FP + vector(0, 0.385, 0), axis=vector(0, 1, 0), radius=0.55, thickness=0.05,
     color=vector(0.62, 0.62, 0.6))
cylinder(pos=FP + vector(0, 0.38, 0), axis=vector(0, 0.02, 0), radius=0.5, color=vector(0.08, 0.08, 0.1))
for k in range(20):
    ang = k * 2.4
    rr = 0.1 + 0.32 * ((k * 7) % 10) / 10
    sphere(pos=FP + vector(rr * cos(ang), 0.415, rr * sin(ang)), radius=0.045,
           color=vector(0.10, 0.20, 0.34), shininess=1)
FLAMES = []
for k in range(7):
    ang = 2 * pi * k / 7
    rr = 0.0 if k == 0 else 0.22
    fx, fz = FP.x + rr * cos(ang), FP.z + rr * sin(ang)
    h0 = 0.62 if k == 0 else 0.4
    for layer, (col_f, rf, hf, op) in enumerate([(vector(1.0, 0.30, 0.05), 0.13, 1.0, 0.7),
                                                 (vector(1.0, 0.56, 0.10), 0.09, 0.82, 0.85),
                                                 (vector(1.0, 0.88, 0.45), 0.05, 0.55, 1.0)]):
        fl = cone(pos=vector(fx, 0.41, fz), axis=vector(0, h0 * hf, 0), radius=rf * (1.3 if k == 0 else 1.0),
                  color=col_f, emissive=True)
        FLAMES.append((fl, h0 * hf, k * 1.37 + layer * 0.5))
EMBERS = []
for k in range(10):
    ang = 2 * pi * k / 10 + 0.3
    EMBERS.append(sphere(pos=FP + vector(0.34 * cos(ang), 0.43, 0.34 * sin(ang)), radius=0.035,
                         color=vector(1.0, 0.4, 0.1), emissive=True))
SPARKS = []
for k in range(10):
    s = sphere(pos=FP + vector(0, 0.5 + 0.17 * k, 0), radius=0.015, color=vector(1.0, 0.75, 0.3),
               emissive=True)
    SPARKS.append([s, 0.5 + 0.17 * k, 0.6 + 0.07 * (k % 4), k * 0.9])
FIRE_GLOW = sphere(pos=FP + vector(0, 0.75, 0), radius=0.8, color=vector(1.0, 0.5, 0.15),
                   opacity=0.08, emissive=True)

block(5.6, 9.4, 0.05, 0.33, -20.2, -17.6, vector(0.55, 0.75, 0.85))


def ledge_lounger(x, z_back, y=0.33):
    a = radians(32)
    u = vector(0, cos(a), -sin(a))
    block(x - 0.33, x + 0.33, y, y + 0.16, z_back + 0.5, z_back + 1.55, PURE_WHITE)
    box(pos=vector(x, y + 0.08, z_back + 0.5) + u * 0.3 + vector(0, 0, -0.17), axis=vector(0.66, 0, 0),
        up=u, height=0.7, width=0.08, color=PURE_WHITE)
    b = radians(25)
    u2 = vector(0, cos(b), sin(b))
    box(pos=vector(x, y + 0.02, z_back + 1.72), axis=vector(0.66, 0, 0), up=u2,
        height=0.4, width=0.07, color=PURE_WHITE)


ledge_lounger(6.6, -20.1)
ledge_lounger(8.3, -20.1)

SY = 1.1
for (x1, x2, z1, z2) in [(9.4, 12.6, -20.0, -19.75), (9.4, 12.6, -16.85, -16.6),
                         (9.4, 9.65, -19.75, -16.85), (12.35, 12.6, -19.75, -16.85)]:
    block(x1, x2, 0, SY, z1, z2, STONE_WALL, solid=True)
block(9.65, 12.35, 0, 0.55, -19.75, -16.85, POOL_DARK)
spa_water = block(9.65, 12.35, 0.55, 1.0, -19.75, -16.85, WATER2, opacity=0.6, shininess=1)
POOL_WATERS.append(spa_water)
add_solid(9.65, 12.35, 0, 1.2, -19.75, -16.85)
block(9.3, 9.45, 1.0, 1.04, -19.2, -17.4, METAL)
POOL_WATERS.append(block(9.33, 9.37, WL, 1.0, -19.2, -17.4, WATER2, opacity=0.45))
for zl in (-19.0, -17.6):
    cylinder(pos=vector(11.0, 0.8, zl + 0.0), axis=vector(0, 0.01, 0), radius=0.08, color=LAMP, emissive=True)

wall("z", -12.75, -20.6, -11.7, D, 3.1, [(-17.6, -14.6, 1.2, 2.5, "none")], t=0.4, col=STONE_WALL)
PB_WALL = vector(0.86, 0.82, 0.74)
block(-17.7, -12.95, 0, D, -14.5, -10.3, PLINTH, solid=True)
tiled(-17.5, -12.95, D, D + 0.012, -14.3, -10.5, vector(0.78, 0.74, 0.66), step=0.5)
wall("x", -10.4, -17.6, -12.95, D, 3.1, [(-14.2, -13.2, 2.1, 2.8, "win")], col=PB_WALL)
wall("z", -17.6, -14.4, -10.4, D, 3.1, [], col=PB_WALL)
wall("x", -14.4, -17.6, -12.95, D, 3.1, [(-16.2, -14.6, 2.2, 2.8, "win")], col=PB_WALL)
block(-17.5, -12.95, 3.05, 3.1, -14.3, -10.5, CEILING)
block(-18.0, -12.4, 3.1, 3.26, -14.8, -10.0, vector(0.36, 0.25, 0.16))
block(-18.02, -12.38, 3.26, 3.3, -14.82, -9.98, ROOF)
xs = -17.5
while xs < -13.1:
    block(xs, xs + 0.06, D + 0.1, 3.0, -10.3, -10.26, vector(0.50, 0.34, 0.20))
    xs += 0.13
block(-13.95, -12.97, D, D + 2.1, -11.72, -11.68, vector(0.50, 0.34, 0.20))
block(-12.98, -12.92, D, D + 2.2, -10.5, -10.3, PB_WALL)
block(-12.98, -12.55, D + 2.2, 3.1, -11.7, -10.3, PB_WALL)
tiled(-17.5, -17.46, D, 3.0, -14.3, -12.9)
tiled(-17.5, -16.1, D, 3.0, -14.3, -14.26)
tiled(-17.5, -16.1, D + 0.012, D + 0.027, -14.3, -12.9, vector(0.42, 0.41, 0.40), step=0.3)
glass_screen(-16.12, -16.08, D, D + 2.1, -14.3, -13.5)
glass_screen(-17.5, -16.1, D, D + 2.1, -12.92, -12.88)
shower_set(vector(-16.8, 2.7, -13.6), vector(-17.48, D + 1.1, -13.6), "+x")
toilet(-17.15, -11.6, "+x", D)
tp_holder(vector(-16.6, D + 0.7, -10.52), "-z")
vanity(-16.0, -14.4, -11.05, -10.5, D, "-z", sinks=[-15.2])
lit_mirror(vector(-15.2, D + 1.75, -10.53), 0.8, 0.8, "-z", round_=True)
bench_seat(-15.8, -14.0, -14.25, -13.85, D, vector(0.50, 0.34, 0.20), vector(0.93, 0.90, 0.84))
for k, tc in enumerate([color.white, vector(0.35, 0.55, 0.70), color.white, vector(0.35, 0.55, 0.70)]):
    cylinder(pos=vector(-15.6 + k * 0.4, D + 0.55, -14.2), axis=vector(0, 0, 0.3), radius=0.08, color=tc)
for xh in (-15.3, -14.6):
    cylinder(pos=vector(xh, D + 1.7, -14.3), axis=vector(0, 0, 0.06), radius=0.015, color=CHROME)
    box(pos=vector(xh, D + 1.25, -14.22), axis=vector(0.32, 0, 0), up=vector(0, 1, 0), height=0.9, width=0.08,
        color=color.white)
potted_plant(-13.4, D, -14.0, 0.7)
downlight(-15.2, 3.05, -12.3)
downlight(-16.8, 3.05, -13.6)


block(-12.97, -12.53, 3.1, 3.15, -20.62, -10.78, PAVER)
yl = 0.75
while yl < 3.05:
    for (z1, z2) in ([(-20.6, -17.6), (-14.6, -10.8)] if 1.2 < yl < 2.5 else [(-20.6, -10.8)]):
        block(-12.56, -12.54, yl, yl + 0.015, z1, z2, vector(0.66, 0.65, 0.62))
    yl += 0.22

for px in (-12.3, -4.4):
    for pz in (-20.9, -10.6):
        block(px - 0.09, px + 0.09, D, 3.5, pz - 0.09, pz + 0.09, PURE_WHITE, solid=True)
    block(px - 0.1, px + 0.1, 3.5, 3.75, -21.0, -10.5, PURE_WHITE)
for pz in (-20.9, -10.6):
    block(-12.4, -4.3, 3.5, 3.75, pz - 0.1, pz + 0.1, PURE_WHITE)
zl = -20.75
while zl < -10.7:
    a = radians(40)
    box(pos=vector(-8.35, 3.65, zl), axis=vector(7.9, 0, 0), up=vector(0, cos(a), sin(a)),
        height=0.18, width=0.025, color=PURE_WHITE)
    zl += 0.22

FLOAT_C = vector(-1.6, WL + 0.02, -17.7)
floaty = ring(pos=FLOAT_C, axis=vector(0, 1, 0), radius=0.45, thickness=0.13, color=vector(1.0, 0.45, 0.25))

outdoor_sofa(-3.6, -0.6, -9.6, -8.8, D, "+z", pillows=[P_COCOA, P_CREAM, P_SAND])
outdoor_sofa(-4.2, -3.4, -12.4, -10.0, D, "-x")
block(-2.9, -1.3, D, D + 0.38, -11.6, -10.6, WOOD)
lantern(-2.1, -11.1, D + 0.38, 0.3)
big_plant(13.0, D, -14.6, 1.5)
big_plant(-4.6, D, -8.5, 1.4)
potted_plant(12.9, D, -21.1, 1.1)


scene.lights = []
SUN_MAIN = distant_light(direction=vector(0.22, 0.44, 0.88), color=color.gray(0.8))
SUN_FILL = distant_light(direction=vector(-0.88, -0.22, -0.44), color=color.gray(0.3))
NIGHT_LIGHTS = [
    (local_light(pos=vector(-2.5, 5.0, 1.5), color=color.black), vector(0.42, 0.33, 0.21)),
    (local_light(pos=vector(5.0, 6.8, -1.0), color=color.black), vector(0.30, 0.23, 0.15)),
    (local_light(pos=vector(-0.5, 1.0, -17.5), color=color.black), vector(0.06, 0.22, 0.30)),
    (local_light(pos=vector(-23.0, 6.6, 3.5), color=color.black), vector(0.30, 0.22, 0.13)),
    (local_light(pos=vector(3.8, 2.5, 7.5), color=color.black), vector(0.30, 0.21, 0.11)),
]
moon = sphere(pos=vector(-55, 48, -100), radius=4, color=vector(0.95, 0.95, 0.88), emissive=True, visible=False)
STARS = []
for i in range(100):
    az = radians((i * 137.508) % 360)
    el = radians(10 + (i * 53) % 75)
    STARS.append(sphere(pos=vector(160 * cos(el) * cos(az), 160 * sin(el), 160 * cos(el) * sin(az)),
                        radius=0.25 + 0.2 * (i % 3), color=color.white, emissive=True))
STARS = [_vp_compound(STARS)]
STARS[0].emissive = True
STARS[0].visible = False

NIGHT_ONLY = []
BEAM = vector(1.0, 0.80, 0.52)


def uplight(x, z, h, spread, y0=0.06, strength=0.07):
    NIGHT_ONLY.append(cylinder(pos=vector(x, y0, z), axis=vector(0, 0.08, 0), radius=0.08,
                               color=LAMP, emissive=True, visible=False))
    NIGHT_ONLY.append(cone(pos=vector(x, y0 + h, z), axis=vector(0, -h, 0), radius=spread,
                           color=BEAM, opacity=strength, emissive=True, visible=False))


for x in (-12.6, -9.2, -5.6, -1.2, 6.7, 9.4):
    uplight(x, 4.5, 3.6, 0.55)
for (x, z, h) in [(-3.8, 8.2, 6.0), (0.2, 7.6, 5.4), (8.0, 8.4, 6.2), (15.5, -19.0, 5.2), (16.6, -15.6, 4.4)]:
    uplight(x + 0.5, z + 0.5, h, 1.1, strength=0.05)
for (x, z) in [(-14.4, -21.0), (-15.6, -21.0), (-16.8, -21.0), (14.3, -21.1), (17.2, -21.1)]:
    uplight(x, z + 0.6, 4.4, 0.6, strength=0.05)
NIGHT_ONLY.append(cone(pos=vector(16.45, 0.09, 12.0), axis=vector(0, 4.0, 0), radius=1.7,
                       color=BEAM, opacity=0.06, emissive=True, visible=False))
NIGHT_ONLY.extend(FENCE_NIGHT)
NIGHT_ONLY.extend(STREET_NIGHT)
NIGHT_ONLY[:] = [_vp_compound(NIGHT_ONLY)]

LIGHTING = {
    "Day": dict(sky=vector(0.60, 0.80, 0.97), amb=color.gray(0.5), main=color.gray(0.8),
                main_dir=vector(0.22, 0.44, 0.88), fill=color.gray(0.3), cloud=color.white,
                sun=vector(1, 0.95, 0.6), sun_pos=vector(45, 50, -90), night=False),
    "Sunset": dict(sky=vector(0.95, 0.62, 0.45), amb=vector(0.42, 0.33, 0.30), main=vector(0.95, 0.65, 0.42),
                   main_dir=vector(0.8, 0.3, 0.5), fill=vector(0.25, 0.20, 0.30),
                   cloud=vector(1.0, 0.78, 0.68), sun=vector(1, 0.55, 0.25), sun_pos=vector(70, 9, -95),
                   night=False),
    "Night": dict(sky=vector(0.03, 0.04, 0.10), amb=vector(0.17, 0.155, 0.15), main=vector(0.16, 0.19, 0.28),
                  main_dir=vector(-0.35, 0.75, 0.55), fill=vector(0.04, 0.035, 0.03),
                  cloud=vector(0.14, 0.16, 0.22), sun=vector(1, 0.95, 0.6), sun_pos=vector(45, 50, -90),
                  night=True),
}
view_state = {"light": "Day", "cut": "Whole house", "view": "Exterior overview"}
WATER_NOW = [WATER2]
LIGHT_BTNS = {}
CUT_BTNS = {}


def highlight(buttons, active):
    for name, b in buttons.items():
        b.background = vector(0.04, 0.04, 0.04) if name == active else color.white
        b.color = color.white if name == active else vector(0.04, 0.04, 0.04)


def set_lighting(name):
    L = LIGHTING[name]
    view_state["light"] = name
    scene.background = sky_color(0, name)
    for v, el in SKY_VERTS:
        v.color = sky_color(el, name)
    scene.ambient = L["amb"]
    SUN_MAIN.color = L["main"]
    SUN_MAIN.direction = L["main_dir"]
    SUN_FILL.color = L["fill"]
    for c in CLOUDS:
        c.color = L["cloud"]
    sun.visible = not L["night"]
    sun.color = L["sun"]
    sun.pos = L["sun_pos"]
    sun_halo.visible = not L["night"]
    sun_halo.pos = L["sun_pos"]
    sun_halo.color = L["sun"]
    moon.visible = L["night"]
    for s in STARS:
        s.visible = L["night"]
    for o in NIGHT_ONLY:
        o.visible = L["night"]
    for lt, col in NIGHT_LIGHTS:
        lt.color = col if L["night"] else color.black
    for g in GLASS_PANES:
        g.color = vector(0.95, 0.78, 0.50) if L["night"] else GLASS
        g.opacity = 0.38 if L["night"] else 0.3
        g.emissive = L["night"]
    for lamp in GATE_LAMPS:
        lit = name != "Day"
        lamp.color = LAMP if lit else LANTERN_OFF
        lamp.emissive = lit
    for sk in SKYLIGHTS:
        sk.color = {"Day": vector(0.78, 0.90, 1.0), "Sunset": vector(1.0, 0.72, 0.52),
                    "Night": vector(0.05, 0.07, 0.15)}[name]
        sk.emissive = name != "Night"
    WATER_NOW[0] = vector(0.10, 0.62, 0.95) if L["night"] else WATER2
    for w in POOL_WATERS:
        w.emissive = L["night"]
    highlight(LIGHT_BTNS, name)
    update_status()


def _bottom(o, kind):
    try:
        if kind == "triangle":
            return min(o.v0.pos.y, o.v1.pos.y, o.v2.pos.y)
        if kind in ("cylinder", "cone"):
            return min(o.pos.y, o.pos.y + o.axis.y)
        if kind == "sphere":
            return o.pos.y - o.radius
        if kind == "ring":
            return o.pos.y - o.thickness
        return o.pos.y - o.size.y / 2
    except Exception:
        return 0.0


GROUP_BOTTOM = {}
for (g0, g1) in GROUPS:
    gb = min(_bottom(*ALL_OBJ[i]) for i in range(g0, g1))
    for i in range(g0, g1):
        GROUP_BOTTOM[i] = gb
HOUSE_PARTS = []
for i in range(BUILD_START, ROOF_END):
    o, k = ALL_OBJ[i]
    HOUSE_PARTS.append((o, GROUP_BOTTOM.get(i, _bottom(o, k)), ROOF_START <= i, False))
TERRACE_PARTS = [o for (o, k) in ALL_OBJ[TERRACE_START:TERRACE_END]]


def _changing_objects():
    skip = {"ALL_OBJ", "HOUSE_PARTS", "TERRACE_PARTS", "GROUPS", "GROUP_BOTTOM"}
    ids = set()

    def walk(v, depth):
        if isinstance(v, (list, tuple, set)) and depth < 4:
            for item in v:
                walk(item, depth + 1)
        elif isinstance(v, dict) and depth < 4:
            for item in v.values():
                walk(item, depth + 1)
        else:
            ids.add(id(v))
    for name, v in list(globals().items()):
        if name in skip or name.startswith("__"):
            continue
        if isinstance(v, list) and len(v) > 1500:
            continue
        walk(v, 0)
    return ids


MERGE_KINDS = {"box": 24, "pyramid": 18, "cylinder": 130, "cone": 70, "sphere": 900, "ellipsoid": 900,
               "ring": 1500}


def merge_still_objects():
    changing = _changing_objects()
    in_house = {id(o): (b, roof) for (o, b, roof, _) in HOUSE_PARTS}
    in_terrace = set(id(o) for o in TERRACE_PARTS)
    buckets, keep_house, keep_terrace = {}, [], []
    for (o, k) in ALL_OBJ:
        if id(o) in in_house:
            b, roof = in_house[id(o)]
            group = "top" if (roof or b >= 7.1) else ("mid" if b >= 3.88 else "low")
        elif id(o) in in_terrace:
            group = "terrace"
        else:
            group = "outside"
        still = (k in MERGE_KINDS and id(o) not in changing and getattr(o, "visible", True)
                 and getattr(o, "opacity", 1) >= 1)
        if not still:
            if group == "terrace":
                keep_terrace.append(o)
            elif group != "outside":
                keep_house.append((o,) + in_house[id(o)] + (False,))
            continue
        buckets.setdefault((group, bool(getattr(o, "emissive", False))), []).append((o, k))
    bottoms = {"top": (8.0, True), "mid": (5.0, False), "low": (0.0, False)}
    new_house, new_terrace = list(keep_house), list(keep_terrace)
    for (group, glow), items in buckets.items():
        chunks, cur, n = [], [], 0
        for (o, k) in items:
            if n + MERGE_KINDS[k] > 250000 and cur:
                chunks.append(cur)
                cur, n = [], 0
            cur.append(o)
            n += MERGE_KINDS[k]
        if cur:
            chunks.append(cur)
        for parts in chunks:
            if len(parts) < 2:
                c = parts[0]
            else:
                c = _vp_compound(parts)
                c.emissive = glow
            if group == "terrace":
                new_terrace.append(c)
            elif group != "outside":
                new_house.append((c,) + bottoms[group] + (False,))
    HOUSE_PARTS[:] = new_house
    TERRACE_PARTS[:] = new_terrace


merge_still_objects()
CUTS = {"Whole house": None, "Roof off": 7.1, "Ground floor only": 3.88}


def set_cut(name):
    cut = CUTS[name]
    view_state["cut"] = name
    for o, b, is_roof, is_chand in HOUSE_PARTS:
        o.visible = cut is None or (not is_roof and b < cut)
    for o in TERRACE_PARTS:
        o.visible = name != "Ground floor only"
    highlight(CUT_BTNS, name)
    update_status()


EYE = 1.6
RADIUS = 0.25
STEP_UP = 0.5
SPEED = 2.5
TURN = 1.8
TOUR_SPEED = 1.8

cam = {"mode": "orbit", "spin": False}
player = {"x": 0.0, "z": 0.0, "feet": 0.0, "head": 0.0, "pitch": 0.0}
pressed = set()
nudge = {"move": 0.0, "turn": 0.0}
MOVE_KEYS = {"w", "a", "s", "d", "up", "down", "left", "right"}


fast = {"shift": False, "toggle": False}


SHIFTED_ARROWS = {"&": "up", "(": "down", "%": "left", '"': "right"}


def key_name(evt):
    k = str(evt.key)
    if k in SHIFTED_ARROWS:
        fast["shift"] = True
        return SHIFTED_ARROWS[k]
    k = k.lower()
    if "+" in k and len(k) > 1:
        parts = k.split("+")
        if "shift" in parts[:-1]:
            fast["shift"] = True
        k = parts[-1]
    return k


def key_down(evt):
    k = key_name(evt)
    if k == "shift" or getattr(evt, "shift", False):
        fast["shift"] = True
        update_status()
    if k == "q":
        if "q" not in pressed:
            pressed.add("q")
            toggle_fast(None)
        return
    if k == "shift":
        return
    pressed.add(k)
    if k in MOVE_KEYS and cam["mode"] == "orbit":
        ensure_walk()


def key_up(evt):
    k = key_name(evt)
    if k == "shift" or getattr(evt, "shift", None) is False:
        if fast["shift"]:
            fast["shift"] = False
            update_status()
    pressed.discard(k)


def toggle_fast(b):
    fast["toggle"] = not fast["toggle"]
    try:
        fast_btn.text = "Fast walk: on" if fast["toggle"] else "Fast walk: off"
        fast_btn.background = vector(0.04, 0.04, 0.04) if fast["toggle"] else color.white
        fast_btn.color = color.white if fast["toggle"] else vector(0.04, 0.04, 0.04)
    except NameError:
        pass
    update_status()


scene.bind("keydown", key_down)
scene.bind("keyup", key_up)


def active_solids():
    if garage["angle"] < 0.3:
        return SOLIDS + GARAGE_DOOR_SOLIDS
    return SOLIDS


def is_blocked(x, z, feet):
    for (x1, x2, y1, y2, z1, z2) in active_solids():
        if (x1 - RADIUS < x < x2 + RADIUS and z1 - RADIUS < z < z2 + RADIUS
                and y1 < feet + 1.75 and y2 > feet + STEP_UP):
            return True
    return False


def ground_height(x, z, feet):
    best = 0.0
    for (x1, x2, y1, y2, z1, z2) in SOLIDS:
        if x1 <= x <= x2 and z1 <= z <= z2 and best < y2 <= feet + STEP_UP:
            best = y2
    return best


def put_camera(eye, d):
    scene.camera.pos = eye
    scene.camera.axis = norm(d) * 3
    walk_cam["dir"] = norm(scene.forward)
    walk_cam["eye"] = eye + vector(0, 0, 0)


walk_cam = {"dir": None, "eye": None}


def set_walk_look():
    scene.userspin = True
    scene.userzoom = False
    try:
        scene.userpan = False
    except Exception:
        pass


def set_userspin(on):
    scene.userspin = on
    scene.userzoom = on
    try:
        scene.userpan = on
    except Exception:
        pass


def floor_name(y):
    return "Loft" if y > 6 else "Second floor" if y > 2.5 else "Ground floor"


def update_status():
    running = fast["shift"] or fast["toggle"]
    status.text = ("<span class='dh-chip'>" + view_state["view"] + " &middot; " + view_state["cut"]
                   + " &middot; " + view_state["light"] + (" &middot; Fast walk" if running else "") + "</span>")


def show_info(title, text):
    info.text = "<div class='dh-info'><b>" + title + "</b><br>" + text + "</div>"


ORBIT_VIEWS = {
    "Exterior overview": (vector(-6, 3, -3), vector(-0.35, -0.35, -1), 30),
    "Garden & pool": (vector(-2, 1, -15.5), vector(-0.35, -0.55, 1), 17),
    "Bird's-eye": (vector(-5, 0, -5), vector(0, -1, -0.05), 32),
}


def set_view(center, forward, rng):
    cam["mode"] = "orbit"
    set_userspin(True)
    scene.fov = pi / 3
    scene.center = center
    scene.forward = forward
    scene.range = rng


def go_orbit(name, smooth=True):
    center, fwd, rng = ORBIT_VIEWS[name]
    tour["on"] = False
    pressed.clear()
    view_state["view"] = name
    update_status()
    if not smooth:
        set_view(center, fwd, rng)
        return
    scene.fov = pi / 3
    eye = center - norm(fwd) * rng / tan(pi / 6)
    fly_to(eye, center, 1.8, after=lambda: set_view(center, fwd, rng))


fly = {"on": False}


def fly_to(eye, look, dur=1.6, after=None, dolly=False):
    d1 = norm(look - eye)
    if dolly:
        p0, d0 = eye - d1 * 0.9 + vector(0, 0.1, 0), d1
    else:
        p0, d0 = scene.camera.pos + vector(0, 0, 0), norm(scene.camera.axis)
    fly.update(on=True, t=0.0, dur=dur, p0=p0, p1=eye, d0=d0, d1=d1, after=after)
    cam["mode"] = "fly"
    set_userspin(False)
    put_camera(p0, d0)


def update_fly(dt):
    fly["t"] += dt / fly["dur"]
    f = min(1.0, fly["t"])
    e = 0.5 - 0.5 * cos(pi * f)
    eye = fly["p0"] + (fly["p1"] - fly["p0"]) * e
    d = fly["d0"] + (fly["d1"] - fly["d0"]) * e
    put_camera(eye, d if mag(d) > 1e-3 else fly["d1"])
    if f >= 1.0:
        fly["on"] = False
        cam["mode"] = "orbit"
        if fly["after"]:
            fly["after"]()


def enter_walk(eye, look):
    d = norm(look - eye)
    cam["mode"] = "walk"
    tour["on"] = False
    set_walk_look()
    scene.fov = radians(70)
    player.update(x=eye.x, z=eye.z, head=atan2(d.z, d.x), pitch=max(-1.2, min(1.2, asin(d.y))))
    player["feet"] = ground_height(eye.x, eye.z, eye.y - EYE + 0.05)
    place_camera()


def place_camera():
    p = player
    look = vector(cos(p["pitch"]) * cos(p["head"]), sin(p["pitch"]), cos(p["pitch"]) * sin(p["head"]))
    eye = vector(p["x"], p["feet"] + EYE, p["z"])
    if (walk_cam["eye"] is not None and walk_cam["dir"] is not None and mag(eye - walk_cam["eye"]) < 1e-4
            and mag(norm(look) - walk_cam["dir"]) < 1e-4):
        return
    put_camera(eye, look)


def adopt_mouse_look():
    if walk_cam["dir"] is None:
        return
    f = norm(scene.forward)
    if mag(f - walk_cam["dir"]) > 1e-3:
        player["head"] = atan2(f.z, f.x)
        player["pitch"] = max(-1.2, min(1.2, asin(max(-1.0, min(1.0, f.y)))))
        walk_cam["dir"] = f


def update_walk(dt):
    p = player
    adopt_mouse_look()
    run = 2.4 if (fast["shift"] or fast["toggle"]) else 1.0
    turn = 0.0
    if "left" in pressed:
        turn -= 1
    if "right" in pressed:
        turn += 1
    if nudge["turn"] != 0:
        s = 1 if nudge["turn"] > 0 else -1
        turn += s
        nudge["turn"] -= s * min(abs(nudge["turn"]), TURN * dt)
    p["head"] += turn * TURN * dt
    if "r" in pressed:
        p["pitch"] = min(1.2, p["pitch"] + TURN * dt * 0.6)
    if "f" in pressed:
        p["pitch"] = max(-1.2, p["pitch"] - TURN * dt * 0.6)
    fwd = vector(cos(p["head"]), 0, sin(p["head"]))
    side = vector(-sin(p["head"]), 0, cos(p["head"]))
    move = vector(0, 0, 0)
    if "w" in pressed or "up" in pressed:
        move = move + fwd
    if "s" in pressed or "down" in pressed:
        move = move - fwd
    if "d" in pressed:
        move = move + side
    if "a" in pressed:
        move = move - side
    if nudge["move"] != 0:
        s = 1 if nudge["move"] > 0 else -1
        move = move + fwd * s
        nudge["move"] -= s * min(abs(nudge["move"]), SPEED * dt)
    if mag(move) > 0:
        move = norm(move) * SPEED * run * dt
        nx = p["x"] + move.x
        if not is_blocked(nx, p["z"], p["feet"]):
            p["x"] = nx
        nz = p["z"] + move.z
        if not is_blocked(p["x"], nz, p["feet"]):
            p["z"] = nz
    target = ground_height(p["x"], p["z"], p["feet"])
    p["feet"] += (target - p["feet"]) * min(1.0, dt * 12)
    place_camera()
    where = "Walking &middot; " + floor_name(p["feet"] + 0.1)
    if view_state["view"] != where:
        view_state["view"] = where
        update_status()


SPACES = {
    "Exterior": (None, "Exterior overview",
                 "Dark charcoal walls, hip roofs, white frames and warm wood."),
    "Living room": (vector(0.8, 2.1, 1.9), vector(-5.5, 2.4, 1.6),
                    "Double-height room with tall glass, sheer curtains and a wood feature wall."),
    "Chandelier": (vector(-0.6, 2.0, 0.2), vector(-2.5, 5.6, 1.5),
                   "A spiral cascade of 110 crystal strands under a glowing ceiling disc."),
    "Dining & kitchen": (vector(-7.6, 2.1, -0.4), vector(-11.0, 1.4, -1.5),
                         "Live-edge table for ten, and a white marble kitchen behind it."),
    "Master suite": (vector(6.0, 5.8, 4.4), vector(6.1, 4.8, 1.0),
                     "Bedroom with tray ceiling, walk-in closet and spa bathroom."),
    "Bedroom 2": (vector(-8.0, 5.8, 3.0), vector(-12.5, 5.0, 0.5),
                  "TV wall, glass door to the roof terrace and its own bathroom."),
    "Loft": (vector(1.2, 9.4, -0.3), vector(5.5, 8.7, -1.6),
             "Cozy lounge with a sectional, a wooden geometric chandelier, wood slat TV wall and skylights."),
    "Garage": (vector(-20.0, 1.75, -2.4), vector(-20.0, 1.0, 3.0),
               "Four cars: a luxury van, an SUV, a pickup and a sport SUV."),
    "Pool & fire lounge": (vector(-3.0, 2.1, -13.0), vector(-8.8, 0.6, -16.2),
                           "Resort pool with stepping stones, spa waterfall and a dry sunken fire lounge."),
    "Roof terrace": (vector(-14.6, 5.8, 1.0), vector(-23.0, 4.7, 3.5),
                     "Pergola with string lights, lounge, dining set and sun loungers."),
    "Pilates studio": (vector(-15.0, 2.1, -4.4), vector(-19.5, 1.2, -6.5),
                       "Bright cream studio with arched mirrors, two reformers, a Cadillac trapeze table and yoga mats."),
    "Music room": (vector(5.6, 5.8, -7.4), vector(8.0, 5.0, -11.5),
                   "Grand piano, drum kit, guitars on the wall and a vinyl corner."),
    "Office": (vector(1.3, 5.8, -8.3), vector(2.6, 5.0, -12.0),
               "Walnut desk, floor-to-ceiling bookcase and a leather executive chair."),
    "Guest bathroom": (vector(6.6, 2.1, -2.75), vector(9.2, 1.3, -4.6),
                       "Bathroom for visitors: marble wall, floating vanity, walk-in rain shower."),
    "Pool bathroom": (vector(-13.6, 2.1, -11.1), vector(-16.8, 1.2, -13.4),
                      "Cabana by the pool deck with a rain shower, toilet, vanity, towels and robes."),
    "Garden": (None, "Garden & pool",
               "Flower beds, palms, frangipani trees and cypress trees."),
}


def go_space(name):
    eye, look, text = SPACES[name]
    tour["on"] = False
    pressed.clear()
    show_info(name, text)
    if eye is None:
        go_orbit(look)
        return
    view_state["view"] = name
    update_status()
    fly_to(eye, look, 1.0, after=lambda: enter_walk(eye, look), dolly=True)


def S(eye, look, title=None, text="", pause=0.0, cut=False):
    return dict(eye=vector(*eye), look=vector(*look), title=title, text=text, pause=pause, cut=cut)


TOUR = [
    S((3.8, 1.68, 17.5), (1, 4.5, 0), "Welcome", "A modern tropical home with a 4-car garage, a resort pool "
      "and three levels. Sit back, the tour walks you through.", 4, True),
    S((3.8, 1.68, 10.0), (3.8, 2.5, 0)),
    S((3.8, 2.1, 6.4), (3.8, 2.4, 0)),
    S((3.8, 2.1, 2.6), (4.0, 2.75, -0.5), "Foyer", "A black double-ring LED chandelier under the wood ceiling, tall plants and the main door.", 2.5),
    S((3.0, 2.1, 1.7), (-3, 2.8, 1.7)),
    S((0.8, 2.1, 1.7), (-6, 2.4, 2.0), "Living room",
      "Double-height space with tall glass, sheer curtains and a wood feature wall.", 3),
    S((-0.6, 2.0, 0.2), (-2.5, 5.6, 1.5), "Spiral crystal chandelier",
      "110 crystal strands spiral down from a glowing ceiling disc.", 4),
    S((-6.0, 2.1, 0.1), (-10.5, 1.6, 1.6)),
    S((-8.8, 2.1, -0.3), (-10.5, 1.4, 1.6), "Dining room", "A live-edge table for ten under a brass branch chandelier with flower lights.", 3),
    S((-9.6, 2.1, -2.0), (-10.5, 1.5, -5.5), "Kitchen", "White veined marble counters, a waterfall marble island, walnut cabinets and a stainless range hood.", 3),
    S((-12.8, 2.1, -4.4), (-17, 1.6, -6)),
    S((-15.2, 2.1, -4.4), (-19.5, 1.2, -6.4), "Pilates studio",
      "A bright cream studio: backlit arched mirrors, two reformers, a Cadillac trapeze table and yoga mats.", 3),
    S((-12.8, 2.1, -4.4), (-7, 2.1, -2.4)),
    S((-7.2, 2.1, -2.4), (-3, 2.0, -2.4)),
    S((-4.0, 2.1, -2.4), (1, 2.0, -3.5)),
    S((1.3, 2.1, -3.6), (5, 2.1, -2.75)),
    S((5.0, 2.1, -2.75), (8, 1.8, -2.75)),
    S((6.7, 2.1, -2.75), (9.2, 1.3, -4.6), "Guest bathroom",
      "A bathroom for visitors: marble wall, floating walnut vanity and a walk-in rain shower.", 2.5),
    S((5.0, 2.1, -2.75), (1.3, 2.1, -3.6)),
    S((1.3, 2.1, -3.6), (1.0, 2.0, -5.2)),
    S((1.0, 2.1, -5.2), (-5, 4.6, -5.2), "Main staircase", "Wood steps with a glass railing lead upstairs.", 2),
    S((0.1, 2.1, -5.2), (-5, 4.6, -5.2)),
    S((-5.6, 5.8, -5.2), (-8, 5.8, -5.2)),
    S((-7.4, 5.8, -5.2), (-7, 5.8, -3)),
    S((-6.0, 5.8, -3.4), (-2.5, 4.8, 1.5), "Balcony", "Look down over the living room and the chandelier.", 4),
    S((0.8, 5.8, -3.9), (3, 5.8, -3.9)),
    S((3.0, 5.8, -3.9), (2.6, 5.6, -1.0), "Walk-in closet", "Mirrored wardrobes and a center island.", 2.5),
    S((3.5, 5.8, -0.6), (3.5, 5.8, 3)),
    S((3.5, 5.8, 3.6), (6.1, 4.8, 1.2), "Master bedroom",
      "Upholstered headboard wall and a tray ceiling with cove lights.", 3),
    S((3.5, 5.8, -0.6), (4.5, 5.6, -2.0)),
    S((4.5, 5.8, -2.0), (8, 5.8, -2.0)),
    S((6.8, 5.8, -2.0), (9.1, 4.9, -0.8), "Master bath", "Freestanding tub, glass shower and a double vanity.", 3),
    S((4.5, 5.8, -2.0), (3, 5.8, -3.9)),
    S((3.0, 5.8, -3.9), (0, 5.8, -3.9)),
    S((1.2, 5.8, -3.9), (1.2, 5.8, -7)),
    S((1.2, 5.8, -7.0), (1.4, 5.5, -10)),
    S((1.3, 5.8, -8.3), (2.6, 5.0, -12.0), "Office",
      "A walnut desk facing the door, a floor-to-ceiling bookcase and big windows over the pool.", 3),
    S((1.3, 5.8, -7.0), (4, 5.8, -7.0)),
    S((3.6, 5.8, -7.05), (6, 5.6, -9)),
    S((5.6, 5.8, -7.4), (8.0, 5.0, -11.5), "Music room",
      "A black grand piano, a drum kit, guitars on the wall and a vinyl corner with tall speakers.", 3.5),
    S((3.6, 5.8, -7.05), (1.2, 5.8, -7.0)),
    S((1.2, 5.8, -7.0), (1.2, 5.8, -4)),
    S((1.2, 5.8, -3.9), (-4, 5.8, -3.9)),
    S((0.8, 5.8, -3.9), (-4, 5.8, -3.9)),
    S((-4.2, 5.8, -3.9), (-4.2, 5.8, -1.8)),
    S((-4.2, 5.8, -1.8), (2, 7.0, -1.8)),
    S((-3.4, 5.8, -1.8), (2, 8.5, -1.8)),
    S((2.0, 9.4, -1.8), (5, 9.2, -1.8)),
    S((2.8, 9.4, -0.4), (5.2, 8.8, -3.2), "Loft",
      "Cozy lounge with a sectional, a wooden geometric chandelier, wood slat TV wall and skylights.", 3.5),
    S((6.0, 2.1, -7.6), (6.0, 1.6, -14), "Family room", "Lounge and a second kitchen that open to the pool.", 3, True),
    S((6.0, 2.1, -13.2), (6.0, 1.5, -17)),
    S((6.0, 2.1, -14.6), (-8.8, 0.6, -16.2), "Resort pool",
      "Stepping stones, a tanning ledge, a spa waterfall and a louvered pergola.", 3),
    S((-4.55, 2.1, -14.2), (-8.8, 0.8, -11)),
    S((-4.55, 2.1, -10.95), (-8.9, 1.2, -10.95)),
    S((-8.9, 2.1, -10.95), (-8.9, 1.0, -14)),
    S((-8.9, 2.12, -11.9), (-8.9, 1.0, -15)),
    S((-8.9, 2.12, -13.2), (-8.8, 0.6, -16.2)),
    S((-8.9, 1.62, -14.9), (-8.8, 0.6, -16.2)),
    S((-8.9, 1.55, -15.0), (-8.8, 0.55, -16.2), "Sunken fire lounge",
      "A dry lounge below the water line, with a built-in sofa and a fire pit.", 4),
    S((-13.6, 2.1, -11.1), (-16.8, 1.2, -13.4), "Pool bathroom",
      "A cabana right by the pool deck: rain shower, toilet, vanity, towels and robes.", 3, True),
    S((-14.6, 5.8, 1.0), (-23, 4.7, 3.5), "Roof terrace",
      "Pergola with string lights, lounge, dining set and sun loungers.", 3, True),
    S((-20.0, 1.75, -2.4), (-20, 1.0, 3), "Garage", "Room for four: van, SUV, pickup and sport SUV.", 3, True),
]
tour = {"on": False, "paused": False, "i": 0, "hold": 0.0, "eye": vector(0, 0, 0), "cam": vector(0, 0, 0),
        "dir": vector(0, 0, -1)}


def turn_toward(d, target, k):
    v = d + (target - d) * k
    return norm(v) if mag(v) > 1e-6 else target


def tour_arrive(i):
    s = TOUR[i]
    tour["i"] = i
    tour["hold"] = s["pause"]
    tour["moved"] = 0.0
    if s["title"]:
        show_info(s["title"], s["text"])
        view_state["view"] = "Tour: " + s["title"]
        update_status()


def tour_jump(i):
    s = TOUR[i]
    tour["moved"] = 0.0
    tour["eye"] = s["eye"]
    tour["cam"] = s["eye"]
    tour["dir"] = norm(s["look"] - s["eye"])
    tour_arrive(i)
    put_camera(tour["cam"], tour["dir"])


def tour_start(b=None):
    pressed.clear()
    tour.update(on=True, paused=False)
    pause_btn.text = "Pause"
    cam["mode"] = "tour"
    set_userspin(False)
    scene.fov = radians(70)
    tour_jump(0)


def tour_pause(b):
    if not tour["on"]:
        return
    tour["paused"] = not tour["paused"]
    b.text = "Resume" if tour["paused"] else "Pause"


def tour_next(b):
    if not tour["on"]:
        return
    for j in range(tour["i"] + 1, len(TOUR)):
        if TOUR[j]["title"]:
            tour_jump(j)
            return


def tour_prev(b):
    if not tour["on"]:
        return
    titled = [j for j in range(len(TOUR)) if TOUR[j]["title"] and j < tour["i"]]
    if titled:
        tour_jump(titled[-1])


def tour_stop(b=None):
    if tour["on"]:
        tour["on"] = False
        enter_walk(tour["cam"], tour["cam"] + tour["dir"])


def update_tour(dt):
    if tour["paused"]:
        return
    i = tour["i"]
    s = TOUR[i]
    ease_pos = 1 - exp(-dt * 6)
    ease_dir = 1 - exp(-dt * 2.4)
    if tour["hold"] > 0:
        tour["hold"] -= dt
        tour["cam"] = tour["cam"] + (tour["eye"] - tour["cam"]) * ease_pos
        tour["dir"] = turn_toward(tour["dir"], norm(s["look"] - tour["cam"]), ease_dir)
        put_camera(tour["cam"], tour["dir"])
        return
    if i + 1 >= len(TOUR):
        tour["on"] = False
        show_info("Tour complete", "Pick a space above, walk with the arrow keys, or try Night.")
        go_orbit("Exterior overview")
        return
    nxt = TOUR[i + 1]
    if nxt["cut"]:
        tour_jump(i + 1)
        return
    d = nxt["eye"] - tour["eye"]
    moved = tour.get("moved", 0.0)
    start = (moved + 0.15) / 1.0 if s["pause"] > 0 else 1.0
    end = (mag(d) + 0.1) / 1.2 if nxt["pause"] > 0 else 1.0
    speed = TOUR_SPEED * max(0.3, min(1.0, start, end))
    step = speed * dt
    tour["moved"] = moved + step
    if mag(d) <= step:
        tour["eye"] = nxt["eye"]
        tour_arrive(i + 1)
    else:
        tour["eye"] = tour["eye"] + norm(d) * step
    tour["cam"] = tour["cam"] + (tour["eye"] - tour["cam"]) * ease_pos
    tour["dir"] = turn_toward(tour["dir"], norm(nxt["look"] - tour["cam"]), ease_dir)
    put_camera(tour["cam"], tour["dir"])


def ensure_walk():
    if cam["mode"] == "walk":
        return
    if tour["on"]:
        tour_stop()
    else:
        enter_walk(vector(3.8, 1.68, 15.5), vector(3.8, 1.8, 0))


def dp_forward(b):
    ensure_walk()
    nudge["move"] += 1.0


def dp_back(b):
    ensure_walk()
    nudge["move"] -= 1.0


def dp_left(b):
    ensure_walk()
    nudge["turn"] -= pi / 8


def dp_right(b):
    ensure_walk()
    nudge["turn"] += pi / 8


def zoom_in(b):
    if cam["mode"] == "orbit":
        scene.range = scene.range * 0.8
    else:
        dp_forward(b)


def zoom_out(b):
    if cam["mode"] == "orbit":
        scene.range = scene.range * 1.25
    else:
        dp_back(b)


def toggle_spin(b):
    if cam["mode"] != "orbit":
        go_orbit("Exterior overview")
    cam["spin"] = not cam["spin"]
    b.text = "Stop rotating" if cam["spin"] else "Auto-rotate"


def toggle_garage(b):
    garage["open"] = not garage["open"]
    b.text = "Close garage" if garage["open"] else "Open garage"


def lab(text=""):
    scene.append_to_title("<span class='dh-lab'>" + (text or "&nbsp;") + "</span>")


def row_break():
    scene.append_to_title("<div class='dh-gap'></div>")


lab("Tour")
button(text="Start guided tour", bind=tour_start, background=GOLD_BTN, color=INK, pos=TOP)
pause_btn = button(text="Pause", bind=tour_pause, pos=TOP)
button(text="Back", bind=tour_prev, pos=TOP)
button(text="Next", bind=tour_next, pos=TOP)
button(text="Stop & walk", bind=tour_stop, pos=TOP)
row_break()

ROOM_ROWS = [["Exterior", "Living room", "Chandelier", "Dining & kitchen", "Master suite", "Bedroom 2"],
             ["Loft", "Music room", "Office", "Pilates studio", "Garage"],
             ["Garden", "Pool & fire lounge", "Pool bathroom", "Roof terrace", "Guest bathroom"]]
lab("Spaces")
for name in ROOM_ROWS[0]:
    button(text=name, bind=lambda b, n=name: go_space(n), pos=TOP)
row_break()
lab()
for name in ROOM_ROWS[1]:
    button(text=name, bind=lambda b, n=name: go_space(n), pos=TOP)
row_break()
lab()
for name in ROOM_ROWS[2]:
    button(text=name, bind=lambda b, n=name: go_space(n), pos=TOP)
row_break()

lab("View")
for name in CUTS:
    CUT_BTNS[name] = button(text=name, bind=lambda b, n=name: set_cut(n), pos=TOP)
for name in LIGHTING:
    LIGHT_BTNS[name] = button(text=name, bind=lambda b, n=name: set_lighting(n), pos=TOP)
row_break()

lab("Camera")
button(text="Zoom in", bind=zoom_in, pos=TOP)
button(text="Zoom out", bind=zoom_out, pos=TOP)
button(text="Reset view", bind=lambda b: go_orbit("Exterior overview"), pos=TOP)
button(text="Bird's-eye", bind=lambda b: go_orbit("Bird's-eye"), pos=TOP)
spin_btn = button(text="Auto-rotate", bind=toggle_spin, pos=TOP)
row_break()

lab("Walk")
button(text="Turn left", bind=dp_left, pos=TOP)
button(text="Forward", bind=dp_forward, pos=TOP)
button(text="Back", bind=dp_back, pos=TOP)
button(text="Turn right", bind=dp_right, pos=TOP)
fast_btn = button(text="Fast walk: off", bind=toggle_fast, pos=TOP)
button(text="Open garage", bind=toggle_garage, pos=TOP)
scene.append_to_title("<div class='dh-end'></div>")

scene.caption = ""
status = wtext(text="")
info = wtext(text="")
scene.append_to_caption(
    "<div class='dh-keys'><span class='dh-kt'>Keyboard &middot; click the 3D view first</span>"
    "<span class='dh-k'><kbd>W</kbd><kbd>S</kbd> or <kbd>\u2191</kbd><kbd>\u2193</kbd> walk</span>"
    "<span class='dh-k'><kbd>\u2190</kbd><kbd>\u2192</kbd> turn</span>"
    "<span class='dh-k'><kbd>A</kbd><kbd>D</kbd> step sideways</span>"
    "<span class='dh-k'><kbd>R</kbd><kbd>F</kbd> look up / down</span>"
    "<span class='dh-k'>hold <kbd>Shift</kbd> run</span>"
    "<span class='dh-k'><kbd>Q</kbd> fast walk on / off</span>"
    "<span class='dh-k'>right-drag to look around (inside too), scroll to zoom outside</span></div>")

set_lighting("Day")
set_cut("Whole house")
go_orbit("Exterior overview", smooth=False)
show_info("Welcome", "Press <b>Start guided tour</b> for a walk-through, or pick a space above.")
scene.append_to_title("<img src='data:,' alt='' style='display:none' "
                      "onerror=\"var e=document.getElementById('dh-loading');if(e){e.remove();}\">")
scene.visible = True


anim = {"fire": True}


def animate(t, dt, frame):
    if frame % 4 == 0:
        for i, w in enumerate(POOL_WATERS):
            w.color = WATER_NOW[0] + vector(0.04, 0.05, 0.0) * sin(2 * t + i)
    if frame % 30 == 0:
        anim["fire"] = mag(scene.camera.pos - FP) < 30
    if frame % 2 == 0:
        floaty.pos = FLOAT_C + vector(1.8 * cos(0.3 * t), 0.02 * sin(2 * t), 0.8 * sin(0.3 * t))
    if frame % 2 == 0 and anim["fire"]:
        for fl, h, ph in FLAMES:
            hh = h * (0.72 + 0.22 * sin(8.0 * t + ph) + 0.12 * sin(13.0 * t + 2.1 * ph))
            fl.axis = vector(0.05 * sin(5 * t + ph), hh, 0.05 * cos(4 * t + 1.7 * ph))
        for sp in SPARKS:
            sp[1] += sp[2] * dt * 2
            if sp[1] > 2.3:
                sp[1] = 0.5
                sp[3] = random() * 6.28
            sp[0].pos = vector(FP.x + 0.15 * sin(sp[3] + sp[1] * 3), sp[1], FP.z + 0.15 * cos(sp[3] + sp[1] * 2))
    if frame % 6 == 0 and anim["fire"]:
        for k, e in enumerate(EMBERS):
            e.color = vector(1.0, 0.3 + 0.1 * (1 + sin(3 * t + k)), 0.06)
        FIRE_GLOW.opacity = (0.16 if view_state["light"] == "Night" else 0.08) + 0.03 * sin(9 * t)
    target = pi / 2 if garage["open"] else 0.0
    if abs(target - garage["angle"]) > 1e-4:
        step = max(-0.025, min(0.025, target - garage["angle"]))
        for d in garage["doors"]:
            d.rotate(angle=step, axis=vector(1, 0, 0), origin=vector(d.pos.x, 3.0, 4.4))
        garage["angle"] += step


t = 0
dt = 1 / 60
frame = 0
while True:
    rate(60)
    t += dt
    frame += 1
    animate(t, dt, frame)
    if cam["mode"] == "fly":
        update_fly(dt)
    elif cam["mode"] == "tour":
        if pressed & MOVE_KEYS:
            tour_stop()
        elif tour["on"]:
            update_tour(dt)
    elif cam["mode"] == "walk":
        update_walk(dt)
    elif cam["mode"] == "orbit" and cam["spin"]:
        scene.forward = scene.forward.rotate(angle=0.002, axis=vector(0, 1, 0))
