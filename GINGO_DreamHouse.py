from vpython import *
import math

SKY_BLUE        = vec(0.40, 0.70, 0.95)
WALL_CREAM      = vec(0.95, 0.90, 0.82)
WALL_TAUPE      = vec(0.60, 0.52, 0.44)
SIDING_DARK     = vec(0.50, 0.42, 0.35)
COLUMN_TAUPE    = vec(0.55, 0.47, 0.40)
ACCENT_BROWN    = vec(0.40, 0.30, 0.22)
ROOF_TILE_DARK  = vec(0.24, 0.11, 0.09)
ROOF_TILE_MID   = vec(0.29, 0.14, 0.11)
ROOF_TILE_LIGHT = vec(0.35, 0.18, 0.14)
ROOF_RIDGE      = vec(0.17, 0.08, 0.06)
TRIM_WHITE      = vec(0.95, 0.95, 0.93)
WOOD_DARK       = vec(0.30, 0.15, 0.08)
GLASS_DARK      = vec(0.15, 0.25, 0.35)
METAL_DARK      = vec(0.18, 0.18, 0.20)
GRASS_GREEN     = vec(0.35, 0.65, 0.30)
CONCRETE_PAD    = vec(0.75, 0.75, 0.75)
STORE_INTERIOR  = vec(0.88, 0.82, 0.70)
STORE_FLOOR     = vec(0.78, 0.74, 0.68)

FOUNDATION_H = 0.40
SLAB_BOTTOM  = 3.80
GF_TOP       = 4.25
UF_TOP       = 7.10
STORE_TOP    = 4.70
WING_TOP     = 6.00
Z_HOUSE      = 3.00
Z_STORE      = 4.00
Z_SLAB       = 5.40
Z_COL        = 4.80

ANCHORS = {
    "store_sign_zone": (-7.6, -2.4, 3.2, 4.7, Z_STORE),
    "store_opening":   (-7.1, -2.9, 0.45, 3.2, Z_STORE),
    "carport_bay":     (4.8, 8.15, -2.0, 5.4, 0.12, 3.8),
    "balcony_rail":    (1.5, 9.2, 4.25, Z_SLAB),
    "fence_line_z":    9.0,
    "patio_left":      vec(-11.5, 0.0, 6.0),
}

scene = canvas(
    title="<b>JONNA GINGO | Dream House</b>",
    width=1280, height=720,
    background=SKY_BLUE
)
scene.autoscale = False

def add_box(pos, size, color):
    return box(pos=pos, size=size, color=color)

def add_span(x0, x1, y0, y1, z0, z1, color):
    return add_box(vec((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2),
                   vec(x1 - x0, y1 - y0, z1 - z0), color)

def add_cylinder(p0, p1, radius, color):
    return cylinder(pos=p0, axis=p1 - p0, radius=radius, color=color)

def add_face(points, color, inside):
    pts = []
    for p in points:
        if not pts or mag(p - pts[-1]) > 1e-6:
            pts.append(p)
    if len(pts) > 1 and mag(pts[0] - pts[-1]) < 1e-6:
        pts.pop()
    n = norm(cross(pts[1] - pts[0], pts[2] - pts[0]))
    c = vec(0, 0, 0)
    for p in pts:
        c = c + p
    c = c / len(pts)
    if dot(n, c - inside) < 0:
        n = -n
    verts = [vertex(pos=p, normal=n, color=color) for p in pts]
    if len(verts) == 3:
        triangle(v0=verts[0], v1=verts[1], v2=verts[2])
    else:
        quad(v0=verts[0], v1=verts[1], v2=verts[2], v3=verts[3])
    return n

def make_hip_roof(center, width, depth, height):
    cx, cy, cz = center.x, center.y, center.z
    x0, x1 = cx - width / 2, cx + width / 2
    z0, z1 = cz - depth / 2, cz + depth / 2
    top = cy + height

    inset = min(width, depth) / 2
    rx = width / 2 - inset
    rz = depth / 2 - inset

    A = vec(x0, cy, z0); B = vec(x1, cy, z0); C = vec(x1, cy, z1); D = vec(x0, cy, z1)
    Ra = vec(cx - rx, top, cz - rz); Rb = vec(cx + rx, top, cz - rz)
    Rc = vec(cx + rx, top, cz + rz); Rd = vec(cx - rx, top, cz + rz)
    inside = vec(cx, cy, cz)

    faces = [(D, C, Rd, Rc),
             (C, B, Rc, Rb),
             (B, A, Rb, Ra),
             (A, D, Ra, Rd)]

    for e0, e1, r0, r1 in faces:
        n = add_face([e0, e1, r1, r0], ROOF_TILE_DARK, inside)
        slope_len = mag((r0 + r1) / 2 - (e0 + e1) / 2)
        rows = max(3, int(slope_len / 0.34))
        for i in range(0, rows + 1):
            t = i / float(rows + 1)
            a = e0 + (r0 - e0) * t + n * 0.04
            b = e1 + (r1 - e1) * t + n * 0.04
            if mag(b - a) < 0.5:
                continue
            col = ROOF_TILE_LIGHT if i % 2 == 0 else ROOF_TILE_MID
            add_cylinder(a, b, 0.07, col)

    for corner, ridge_pt in ((A, Ra), (B, Rb), (C, Rc), (D, Rd)):
        add_cylinder(corner, ridge_pt, 0.09, ROOF_RIDGE)
    if mag(Rc - Ra) > 0.05:
        add_cylinder(Ra, Rc, 0.12, ROOF_RIDGE)

    fy0, fy1 = cy - 0.25, cy
    add_span(x0, x1, fy0, fy1, z1 - 0.12, z1, TRIM_WHITE)
    add_span(x0, x1, fy0, fy1, z0, z0 + 0.12, TRIM_WHITE)
    add_span(x0, x0 + 0.12, fy0, fy1, z0, z1, TRIM_WHITE)
    add_span(x1 - 0.12, x1, fy0, fy1, z0, z1, TRIM_WHITE)
    add_span(x0, x1, fy0, fy0 + 0.06, z0, z1, ACCENT_BROWN)

def make_window(cx, cy, z, w, h):
    d = 0.14
    add_span(cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, z, z + d, TRIM_WHITE)
    g = 0.12
    add_span(cx - w / 2 + g, cx + w / 2 - g, cy - h / 2 + g, cy + h / 2 - g,
             z + d - 0.02, z + d + 0.02, GLASS_DARK)
    add_span(cx - 0.04, cx + 0.04, cy - h / 2 + g, cy + h / 2 - g,
             z + d, z + d + 0.05, TRIM_WHITE)
    add_span(cx - w / 2 - 0.1, cx + w / 2 + 0.1, cy - h / 2 - 0.1, cy - h / 2,
             z, z + d + 0.15, TRIM_WHITE)

def make_door(cx, w, h, y0, z):
    add_span(cx - w / 2, cx + w / 2, y0, y0 + h, z, z + 0.10, WOOD_DARK)
    t = 0.12
    add_span(cx - w / 2 - t, cx - w / 2, y0, y0 + h + t, z, z + 0.12, TRIM_WHITE)
    add_span(cx + w / 2, cx + w / 2 + t, y0, y0 + h + t, z, z + 0.12, TRIM_WHITE)
    add_span(cx - w / 2 - t, cx + w / 2 + t, y0 + h, y0 + h + t, z, z + 0.12, TRIM_WHITE)
    for gx in (-0.3, 0.0, 0.3):
        add_span(cx + gx - 0.02, cx + gx + 0.02, y0 + 0.2, y0 + h - 0.2,
                 z + 0.10, z + 0.12, ACCENT_BROWN)
    add_span(cx + w / 2 - 0.2, cx + w / 2 - 0.12, y0 + 1.0, y0 + 1.5,
             z + 0.10, z + 0.16, METAL_DARK)

def add_siding(x0, x1, y0, y1, z, step=0.38):
    y = y0
    while y < y1 - 0.02:
        add_span(x0, x1, y, y + 0.05, z, z + 0.04, SIDING_DARK)
        y += step

def make_column(cx, cz, y0, y1, w=0.9, base=True):
    add_span(cx - w / 2, cx + w / 2, y0, y1, cz - w / 2, cz + w / 2, COLUMN_TAUPE)
    cw = w + 0.25
    add_span(cx - cw / 2, cx + cw / 2, y1 - 0.32, y1, cz - cw / 2, cz + cw / 2, TRIM_WHITE)
    nw = w + 0.12
    add_span(cx - nw / 2, cx + nw / 2, y1 - 0.40, y1 - 0.32, cz - nw / 2, cz + nw / 2, TRIM_WHITE)
    if base:
        add_span(cx - nw / 2, cx + nw / 2, y0, y0 + 0.35, cz - nw / 2, cz + nw / 2, CONCRETE_PAD)

def create_environment():
    add_span(-14, 14, -0.5, 0.0, -8, 13, GRASS_GREEN)

def create_foundation():
    f = FOUNDATION_H
    add_span(-7.7, -2.3, 0, f, -0.7, 4.1, CONCRETE_PAD)
    add_span(-6.5, -0.3, 0, f, -4.1, -0.5, CONCRETE_PAD)
    add_span(-2.5, 4.9, 0, f, -1.3, 3.1, CONCRETE_PAD)
    add_span(4.8, 9.2, 0, 0.12, -2.0, 5.4, CONCRETE_PAD)

    add_span(-1.0, 0.9, 0, 0.20, 3.1, 3.9, CONCRETE_PAD)
    add_span(-0.8, 0.7, 0.20, f, 3.1, 3.5, CONCRETE_PAD)

def create_store_shell():
    f, t = FOUNDATION_H, 0.30
    add_span(-7.6, -7.6 + t, f, STORE_TOP, -0.6, Z_STORE, WALL_CREAM)
    add_span(-2.4 - t, -2.4, f, STORE_TOP, -0.6, Z_STORE, WALL_CREAM)
    add_span(-7.6, -2.4, f, STORE_TOP, -0.6, -0.6 + t, STORE_INTERIOR)
    add_span(-7.6, -7.1, f, STORE_TOP, Z_STORE - t, Z_STORE, WALL_CREAM)
    add_span(-2.9, -2.4, f, STORE_TOP, Z_STORE - t, Z_STORE, WALL_CREAM)
    add_span(-7.6, -2.4, 3.2, STORE_TOP, Z_STORE - t, Z_STORE, WALL_CREAM)
    add_span(-7.3, -2.7, f, f + 0.05, -0.3, Z_STORE, STORE_FLOOR)
    add_span(-7.3, -2.7, 3.2, 3.35, -0.3, Z_STORE - t, STORE_INTERIOR)

    add_span(-7.1, -2.9, 3.08, 3.2, Z_STORE - 0.05, Z_STORE + 0.05, TRIM_WHITE)
    add_span(-7.1, -7.0, f, 3.08, Z_STORE - 0.05, Z_STORE + 0.05, TRIM_WHITE)
    add_span(-3.0, -2.9, f, 3.08, Z_STORE - 0.05, Z_STORE + 0.05, TRIM_WHITE)

def create_main_structure():
    f = FOUNDATION_H

    add_span(-2.4, 4.8, f, GF_TOP, -1.2, Z_HOUSE, WALL_CREAM)
    add_span(-2.35, 4.75, 0.45, 4.20, Z_HOUSE, Z_HOUSE + 0.06, WALL_TAUPE)
    add_siding(-2.35, 4.75, 0.60, 4.10, Z_HOUSE + 0.06)

    add_span(-6.4, -0.4, f, WING_TOP, -4.0, -0.6, WALL_CREAM)

    add_span(1.5, 5.2, GF_TOP, UF_TOP, -1.2, Z_HOUSE, WALL_CREAM)
    add_span(1.55, 5.15, GF_TOP + 0.05, 6.80, Z_HOUSE, Z_HOUSE + 0.06, WALL_TAUPE)
    add_siding(1.55, 5.15, 4.45, 6.75, Z_HOUSE + 0.06)
    add_span(-0.4, 1.5, GF_TOP, UF_TOP, -1.2, 2.4, WALL_CREAM)

    create_carport_and_balcony()

def create_carport_and_balcony():
    add_span(0.4, 9.2, SLAB_BOTTOM, GF_TOP, Z_HOUSE, Z_SLAB, TRIM_WHITE)
    add_span(4.8, 9.2, SLAB_BOTTOM, GF_TOP, -2.0, Z_HOUSE, TRIM_WHITE)

    add_span(4.8, 9.2, 0.12, SLAB_BOTTOM, -2.0, -1.7, WALL_TAUPE)
    add_span(4.8, 5.1, 0.12, SLAB_BOTTOM, -2.0, -1.2, WALL_TAUPE)

    make_column(1.05, Z_COL, 0.0, SLAB_BOTTOM)
    make_column(8.6, Z_COL, 0.12, SLAB_BOTTOM)
    make_column(8.6, 0.9, 0.12, SLAB_BOTTOM, w=0.7)

    add_span(1.05, 8.6, 3.30, SLAB_BOTTOM, Z_COL - 0.25, Z_COL + 0.25, COLUMN_TAUPE)

    make_column(1.05, Z_COL, GF_TOP, UF_TOP, base=False)
    make_column(6.45, Z_COL, GF_TOP, UF_TOP, base=False)

def create_roofs():
    make_hip_roof(vec(-5.0, STORE_TOP + 0.25, 2.0), 7.2, 5.6, 1.35)

    make_hip_roof(vec(-1.0, GF_TOP + 0.25, 2.8), 2.8, 2.2, 0.7)

    make_hip_roof(vec(-3.4, WING_TOP + 0.25, -2.3), 7.2, 5.4, 1.3)

    make_hip_roof(vec(4.1, UF_TOP + 0.25, 1.6), 9.4, 8.0, 1.8)

def create_doors_and_windows():
    make_door(-0.05, 1.2, 2.8, FOUNDATION_H, Z_HOUSE + 0.06)
    make_window(-1.55, 2.35, Z_HOUSE + 0.06, 1.3, 1.65)
    make_window(3.00, 2.35, Z_HOUSE + 0.06, 1.8, 1.65)
    make_window(3.35, 5.55, Z_HOUSE + 0.06, 2.4, 2.0)

FENCE_POST     = vec(0.80, 0.76, 0.70)
FENCE_WALL     = vec(0.92, 0.88, 0.80)
FENCE_METAL    = vec(0.14, 0.14, 0.16)
LIGHT_GLOW     = vec(1.00, 0.93, 0.62)
WOOD_MED       = vec(0.62, 0.40, 0.20)
WOOD_LIGHT     = vec(0.78, 0.55, 0.32)
SIGN_RED       = vec(0.85, 0.05, 0.07)
SIGN_FRAME     = vec(0.78, 0.78, 0.78)
SIGN_TEXT      = vec(0.08, 0.08, 0.08)
SIDEWALK_COL   = vec(0.80, 0.80, 0.78)
WALK_TILE      = vec(0.86, 0.85, 0.82)
TILE_LINE      = vec(0.66, 0.66, 0.64)
DRIVE_CONCRETE = vec(0.72, 0.72, 0.72)
LEAF_GREEN     = vec(0.18, 0.47, 0.20)
LEAF_LIGHT     = vec(0.32, 0.64, 0.28)
TRUNK_BROWN    = vec(0.38, 0.28, 0.20)
FURNITURE      = vec(0.17, 0.15, 0.14)
TABLE_BROWN    = vec(0.30, 0.20, 0.14)
UMBRELLA_BEIGE = vec(0.90, 0.84, 0.70)
CAR_SILVER     = vec(0.84, 0.85, 0.88)
CAR_BUMPER     = vec(0.70, 0.71, 0.74)
CAR_GLASS      = vec(0.10, 0.14, 0.18)
CAR_DARK       = vec(0.12, 0.12, 0.14)
CAR_TIRE       = vec(0.07, 0.07, 0.08)
CAR_CHROME     = vec(0.92, 0.92, 0.94)
CAR_LIGHT      = vec(0.97, 0.97, 0.90)
CAR_TAIL       = vec(0.75, 0.08, 0.08)

PRODUCT_COLORS = [vec(0.86, 0.15, 0.12), vec(0.95, 0.78, 0.10), vec(0.95, 0.50, 0.10),
                  vec(0.20, 0.62, 0.30), vec(0.15, 0.45, 0.82), vec(0.90, 0.35, 0.60),
                  vec(0.55, 0.30, 0.70), vec(0.92, 0.92, 0.88)]
BOTTLE_COLORS  = [vec(0.35, 0.15, 0.10), vec(0.95, 0.55, 0.10), vec(0.25, 0.65, 0.30),
                  vec(0.20, 0.45, 0.85), vec(0.90, 0.85, 0.20)]

FENCE_Z = 9.0
SIDEWALK_Z0, SIDEWALK_Z1 = 9.4, 12.4
SIDEWALK_X = 14.0
FENCE_X_LEFT, FENCE_X_RIGHT, FENCE_Z_BACK = -12.1, 13.5, -7.0
STORE_OPEN_X0, STORE_OPEN_X1 = -7.1, -2.9
DOOR_CX = -0.05
PED_GATE_X0, PED_GATE_X1 = DOOR_CX - 0.5, DOOR_CX + 0.5
VEH_GATE_X0, VEH_GATE_X1 = 4.6, 9.4
DRIVE_X0, DRIVE_X1 = 4.8, 9.2
CAR_CX, CAR_CZ = 6.5, 1.9
DINING_CX, DINING_CZ = -9.9, 5.8

FRONT_POST_X = [-12.1, -7.9, -2.4,
                PED_GATE_X0 - 0.4, PED_GATE_X1 + 0.4,
                VEH_GATE_X0 - 0.4, VEH_GATE_X1 + 0.4,
                13.5]
FRONT_OPENING_AFTER = {1, 3, 5}
SIDE_POST_Z = [9.0, 5.0, 1.0, -3.0, -7.0]

WALK_FENCE_RIGHT_X = FRONT_POST_X[2]
WALK_FENCE_LEFT_X = FRONT_POST_X[1]
WALK_FENCE_END_Z = 4.5
DINING_GATE_Z0, DINING_GATE_Z1 = 7.3, 8.6
BACK_POST_X = [FENCE_X_LEFT + (FENCE_X_RIGHT - FENCE_X_LEFT) * i / 6.0 for i in range(7)]

def add_span_axis(axis, a0, a1, y0, y1, c0, c1, color):
    if axis == "x":
        return add_span(a0, a1, y0, y1, c0, c1, color)
    return add_span(c0, c1, y0, y1, a0, a1, color)

def add_text(txt, pos, height, color):
    try:
        t = text(text=txt, pos=pos, align="center", height=height, depth=0.02, color=color)
    except Exception:
        t = label(pos=pos, text=txt, height=int(height * 28), color=color, box=False, opacity=0)
    return t

def make_wall_lamp(x, y, z):
    add_span(x - 0.14, x + 0.14, y - 0.26, y + 0.26, z, z + 0.07, METAL_DARK)
    add_span(x - 0.08, x + 0.08, y - 0.19, y + 0.19, z + 0.07, z + 0.09, LIGHT_GLOW)

def make_paved_path(x0, x1, z0, z1, top, base_col, line_col, tile):
    add_span(x0, x1, -0.05, top, z0, z1, base_col)
    z = z0 + tile
    while z < z1 - 0.05:
        add_span(x0, x1, top, top + 0.01, z, z + 0.04, line_col)
        z += tile
    x = x0 + tile
    while x < x1 - 0.05:
        add_span(x, x + 0.04, top, top + 0.01, z0, z1, line_col)
        x += tile

def make_shrub(x, z, r=0.45, y=0.0):
    ellipsoid(pos=vec(x, y + r * 0.75, z), length=2.3 * r, height=1.5 * r,
              width=2.0 * r, color=LEAF_GREEN)
    ellipsoid(pos=vec(x + 0.2 * r, y + 1.15 * r, z - 0.1 * r), length=1.2 * r,
              height=0.9 * r, width=1.1 * r, color=LEAF_LIGHT)

def make_planter(x, z, w=0.55, h=0.5):
    add_span(x - w / 2, x + w / 2, 0, h, z - w / 2, z + w / 2, FENCE_WALL)
    make_shrub(x, z, r=0.3, y=h)

def make_palm(x, z, h=3.4):
    add_cylinder(vec(x, 0, z), vec(x, h, z), 0.12, TRUNK_BROWN)
    for k in range(8):
        a = k * math.pi / 4
        d = norm(vec(math.cos(a) * 0.9, 0.15, math.sin(a) * 0.9))
        ellipsoid(pos=vec(x, h, z) + d * 0.85, axis=d, length=1.8, height=0.12,
                  width=0.45, color=LEAF_GREEN if k % 2 == 0 else LEAF_LIGHT)

def make_fence_post(cx, z=FENCE_Z, lamp=True):
    add_span(cx - 0.4, cx + 0.4, 0, 2.8, z - 0.4, z + 0.4, FENCE_POST)
    add_span(cx - 0.48, cx + 0.48, 2.8, 2.92, z - 0.48, z + 0.48, TRIM_WHITE)
    if lamp:
        make_wall_lamp(cx, 1.85, z + 0.4)

def make_fence_run(axis, a0, a1, c):
    add_span_axis(axis, a0, a1, 0, 0.9, c - 0.2, c + 0.2, FENCE_WALL)
    add_span_axis(axis, a0, a1, 0.9, 0.98, c - 0.26, c + 0.26, TRIM_WHITE)
    top = 2.45
    add_span_axis(axis, a0, a0 + 0.08, 0.98, top, c - 0.05, c + 0.05, FENCE_METAL)
    add_span_axis(axis, a1 - 0.08, a1, 0.98, top, c - 0.05, c + 0.05, FENCE_METAL)
    for yb in (1.25, 1.65, 2.05):
        add_span_axis(axis, a0, a1, yb - 0.04, yb + 0.04, c - 0.05, c + 0.05, FENCE_METAL)
    add_span_axis(axis, a0, a1, top - 0.08, top, c - 0.06, c + 0.06, FENCE_METAL)

def make_fence_section(x0, x1, z=FENCE_Z):
    make_fence_run("x", x0, x1, z)

def make_gate_panel(axis, a0, a1, c, y0, y1, bars):
    t, s = 0.05, 0.10
    add_span_axis(axis, a0, a0 + s, y0, y1, c - t, c + t, FENCE_METAL)
    add_span_axis(axis, a1 - s, a1, y0, y1, c - t, c + t, FENCE_METAL)
    add_span_axis(axis, a0, a1, y0, y0 + s, c - t, c + t, FENCE_METAL)
    add_span_axis(axis, a0, a1, y1 - s, y1, c - t, c + t, FENCE_METAL)
    gap = (y1 - y0 - 2 * s) / (bars + 1)
    for i in range(1, bars + 1):
        yb = y0 + s + gap * i
        add_span_axis(axis, a0, a1, yb - 0.045, yb + 0.045, c - t, c + t, FENCE_METAL)

def make_gate_hardware(x0, x1, z, hinge_side="left"):
    hx = x0 if hinge_side == "left" else x1 - 0.12
    lx = x1 - 0.3 if hinge_side == "left" else x0 + 0.18
    for hy in (0.6, 2.0):
        add_span(hx, hx + 0.12, hy - 0.1, hy + 0.1, z + 0.05, z + 0.13, CAR_BUMPER)
    add_span(lx, lx + 0.12, 1.25, 1.45, z + 0.05, z + 0.12, CAR_BUMPER)

def make_railing_run(axis, a0, a1, c, y0, y1):
    length = a1 - a0
    n = max(1, int(round(length / 1.4)))
    for i in range(n + 1):
        a = a0 + length * i / n
        add_span_axis(axis, a - 0.04, a + 0.04, y0, y1, c - 0.05, c + 0.05, FENCE_METAL)
    for k in (1, 2, 3):
        yb = y0 + (y1 - y0) * k / 4.4
        add_span_axis(axis, a0, a1, yb - 0.035, yb + 0.035, c - 0.03, c + 0.03, FENCE_METAL)
    add_span_axis(axis, a0 - 0.04, a1 + 0.04, y1 - 0.07, y1, c - 0.06, c + 0.06, FENCE_METAL)

def make_chair(cx, cz, facing):
    hw = 0.3
    add_span(cx - hw, cx + hw, 0.55, 0.62, cz - hw, cz + hw, FURNITURE)
    bz = cz - facing * (hw - 0.03)
    for lx in (-hw + 0.03, hw - 0.03):
        add_span(cx + lx - 0.03, cx + lx + 0.03, 0, 0.55,
                 cz + facing * (hw - 0.03) - 0.03, cz + facing * (hw - 0.03) + 0.03, FURNITURE)
        add_span(cx + lx - 0.03, cx + lx + 0.03, 0, 1.25, bz - 0.03, bz + 0.03, FURNITURE)
    for yb in (0.85, 1.08):
        add_span(cx - hw + 0.03, cx + hw - 0.03, yb, yb + 0.12, bz - 0.02, bz + 0.02, FURNITURE)

def make_umbrella(x, z, radius=2.05, rim_y=3.15, apex_y=3.7):
    add_cylinder(vec(x, 0, z), vec(x, 0.1, z), 0.32, FURNITURE)
    add_cylinder(vec(x, 0, z), vec(x, apex_y + 0.08, z), 0.05, FURNITURE)
    apex = vec(x, apex_y, z)
    rim = [vec(x + radius * math.cos(k * math.pi / 4 + math.pi / 8), rim_y,
               z + radius * math.sin(k * math.pi / 4 + math.pi / 8)) for k in range(8)]
    light, under = vec(0.95, 0.90, 0.78), vec(0.76, 0.70, 0.58)
    drop = vec(0, 0.03, 0)
    for k in range(8):
        a, b = rim[k], rim[(k + 1) % 8]
        add_face([apex, a, b], UMBRELLA_BEIGE if k % 2 == 0 else light, vec(x, rim_y - 0.5, z))
        add_face([apex - drop, a - drop, b - drop], under, vec(x, apex_y + 1.0, z))
        add_cylinder(a, b, 0.03, vec(0.80, 0.74, 0.60))
        add_cylinder(apex - vec(0, 0.07, 0), a - vec(0, 0.06, 0), 0.025, TABLE_BROWN)
    sphere(pos=apex + vec(0, 0.06, 0), radius=0.07, color=TABLE_BROWN)

def stock_shelf_row(kind, x0, x1, y, z):
    n = 9
    step = (x1 - x0) / n
    for i in range(n):
        x = x0 + step * (i + 0.5)
        col = PRODUCT_COLORS[(i * 3 + len(kind)) % len(PRODUCT_COLORS)]
        if kind == "cans":
            cylinder(pos=vec(x, y, z), axis=vec(0, 0.24, 0), radius=0.09, color=col)
        elif kind == "household":
            if i % 2 == 0:
                cylinder(pos=vec(x, y, z), axis=vec(0, 0.42, 0), radius=0.10, color=col)
            else:
                add_box(vec(x, y + 0.17, z), vec(0.26, 0.34, 0.2), col)
        elif kind == "noodles":
            add_box(vec(x, y + 0.15, z), vec(0.26, 0.30, 0.18), col)
        elif kind == "biscuits":
            add_box(vec(x, y + 0.18, z), vec(0.28, 0.36, 0.12), col)
        else:
            add_box(vec(x, y + 0.21, z), vec(0.26, 0.42, 0.07), col)

def make_refrigerator(x0, x1, y0, y1, z0, z1):
    t = 0.06
    add_span(x0, x1, y0, y1, z0, z0 + t, vec(0.90, 0.92, 0.95))
    add_span(x0, x0 + t, y0, y1, z0, z1, FENCE_METAL)
    add_span(x1 - t, x1, y0, y1, z0, z1, FENCE_METAL)
    add_span(x0, x1, y1 - 0.2, y1, z0, z1, FENCE_METAL)
    add_span(x0, x1, y0, y0 + 0.1, z0, z1, FENCE_METAL)
    add_span(x0 + 0.1, x1 - 0.1, y1 - 0.16, y1 - 0.06, z1, z1 + 0.02, SIGN_RED)
    for k in range(4):
        lvl = y0 + 0.1 + k * 0.48
        if k > 0:
            add_span(x0 + t, x1 - t, lvl - 0.03, lvl, z0 + t, z1 - 0.05, vec(0.75, 0.78, 0.80))
        for i in range(5):
            bx = x0 + t + (x1 - x0 - 2 * t) * (i + 0.5) / 5
            col = BOTTLE_COLORS[(i + k * 2) % len(BOTTLE_COLORS)]
            cylinder(pos=vec(bx, lvl, z1 - 0.25), axis=vec(0, 0.38, 0),
                     radius=0.065, color=col)
    box(pos=vec((x0 + x1) / 2, (y0 + 0.1 + y1 - 0.2) / 2, z1),
        size=vec(x1 - x0 - 2 * t, y1 - y0 - 0.3, 0.03),
        color=vec(0.70, 0.85, 0.95), opacity=0.28)
    add_span(x1 - 0.17, x1 - 0.13, 1.2, 2.0, z1, z1 + 0.06, CAR_CHROME)

def make_suv(cx, cz, floor=0.12):
    wy = floor + 0.45
    for sx in (-1, 1):
        for zz in (cz + 1.9, cz - 1.9):
            xc = cx + sx * 1.1
            cylinder(pos=vec(xc - 0.2, wy, zz), axis=vec(0.4, 0, 0), radius=0.45, color=CAR_TIRE)
            xh = xc + (0.17 if sx > 0 else -0.22)
            cylinder(pos=vec(xh, wy, zz), axis=vec(0.05, 0, 0), radius=0.24, color=CAR_BUMPER)
    add_span(cx - 1.15, cx + 1.15, floor + 0.35, floor + 1.43, cz - 3.0, cz + 3.0, CAR_SILVER)
    add_span(cx - 1.05, cx + 1.05, floor + 1.43, floor + 2.13, cz - 2.6, cz + 0.5, CAR_SILVER)
    add_span(cx - 1.08, cx + 1.08, floor + 2.13, floor + 2.21, cz - 2.7, cz + 0.45, CAR_SILVER)
    yb, yt = floor + 1.43, floor + 2.13
    inside = vec(cx, floor + 1.3, cz)
    add_face([vec(cx - 1.0, yb, cz + 1.1), vec(cx + 1.0, yb, cz + 1.1),
              vec(cx + 1.0, yt, cz + 0.5), vec(cx - 1.0, yt, cz + 0.5)], CAR_GLASS, inside)
    for sx in (-1, 1):
        xs = cx + sx * 1.05
        add_face([vec(xs, yb, cz + 1.1), vec(xs, yb, cz + 0.5), vec(xs, yt, cz + 0.5)], CAR_SILVER, inside)
        x0w, x1w = (xs, xs + 0.03) if sx > 0 else (xs - 0.03, xs)
        for za, zb in ((cz - 0.8, cz + 0.45), (cz - 2.15, cz - 0.9), (cz - 2.5, cz - 2.25)):
            add_span(x0w, x1w, floor + 1.55, floor + 2.05, za, zb, CAR_GLASS)
        xm = cx + sx * 1.27
        add_box(vec(xm, floor + 1.63, cz + 0.55), vec(0.18, 0.14, 0.26), CAR_DARK)
        xd = cx + sx * 1.16
        for zl in (cz + 0.5, cz - 0.95, cz - 2.3):
            add_box(vec(xd, floor + 0.95, zl), vec(0.03, 0.9, 0.03), vec(0.38, 0.39, 0.43))
        for zh in (cz - 0.1, cz - 1.35):
            add_box(vec(xd, floor + 1.2, zh), vec(0.05, 0.05, 0.28), CAR_DARK)
        add_span(cx + sx * 0.85 - 0.3, cx + sx * 0.85 + 0.3, floor + 1.08, floor + 1.36,
                 cz + 3.0, cz + 3.04, CAR_LIGHT)
        add_span(cx + sx * 0.9 - 0.2, cx + sx * 0.9 + 0.2, floor + 1.13, floor + 1.43,
                 cz - 3.04, cz - 3.0, CAR_TAIL)
    add_span(cx - 0.5, cx + 0.5, floor + 0.98, floor + 1.33, cz + 3.0, cz + 3.04, CAR_DARK)
    for gy in (floor + 1.08, floor + 1.21):
        add_span(cx - 0.5, cx + 0.5, gy, gy + 0.04, cz + 3.04, cz + 3.06, CAR_CHROME)
    add_span(cx - 1.18, cx + 1.18, floor + 0.35, floor + 0.8, cz + 2.95, cz + 3.12, CAR_BUMPER)
    add_span(cx - 0.7, cx + 0.7, floor + 0.46, floor + 0.63, cz + 3.12, cz + 3.14, CAR_DARK)
    add_span(cx - 1.18, cx + 1.18, floor + 0.35, floor + 0.8, cz - 3.12, cz - 2.95, CAR_BUMPER)
    add_span(cx - 0.95, cx + 0.95, floor + 1.55, floor + 2.05, cz - 2.64, cz - 2.6, CAR_GLASS)

def create_street_and_paths():
    add_span(-SIDEWALK_X, SIDEWALK_X, -0.1, 0.10, SIDEWALK_Z0, SIDEWALK_Z1, SIDEWALK_COL)
    x = -SIDEWALK_X + 3.0
    while x < SIDEWALK_X - 0.1:
        add_span(x, x + 0.05, 0.10, 0.11, SIDEWALK_Z0, SIDEWALK_Z1, TILE_LINE)
        x += 3.0

    make_paved_path(STORE_OPEN_X0, STORE_OPEN_X1, 5.5, SIDEWALK_Z0, 0.05, WALK_TILE, TILE_LINE, 1.05)

    make_paved_path(PED_GATE_X0 + 0.05, PED_GATE_X1 - 0.05, 3.9, SIDEWALK_Z0, 0.05, WALK_TILE, TILE_LINE, 1.0)

    make_paved_path(DRIVE_X0, DRIVE_X1, 5.4, SIDEWALK_Z1, 0.12, DRIVE_CONCRETE, vec(0.58, 0.58, 0.58), 1.15)

    make_paved_path(-11.5, -8.3, 3.9, 7.7, 0.04, vec(0.80, 0.78, 0.74), TILE_LINE, 1.05)

def create_store_sign():
    x0, x1, y0, y1 = -7.5, -2.5, 3.3, 4.55
    zf = Z_STORE
    add_span(x0 - 0.06, x1 + 0.06, y0 - 0.06, y1 + 0.06, zf, zf + 0.05, SIGN_FRAME)
    add_span(x0, x1, y0, y1, zf + 0.05, zf + 0.08, TRIM_WHITE)
    add_span(x0, -6.3, y0, y1, zf + 0.08, zf + 0.09, SIGN_RED)
    tilt = math.radians(20)
    for sx in (-6.5, -6.2):
        box(pos=vec(sx, (y0 + y1) / 2, zf + 0.095), axis=vec(math.sin(tilt), math.cos(tilt), 0),
            length=(y1 - y0) / math.cos(tilt), height=0.10, width=0.01, color=TRIM_WHITE)
    add_text("JONNA", vec(-4.35, 4.05, zf + 0.1), 0.7, SIGN_TEXT)
    add_text("Convenience Store", vec(-4.35, 3.55, zf + 0.1), 0.3, SIGN_TEXT)

def create_store_interior():
    sx0, sx1, zb0, zb1 = -6.9, -3.7, -0.3, 0.25
    add_span(sx0, sx1, 0.45, 2.93, zb0, zb0 + 0.05, WOOD_MED)
    add_span(sx0 - 0.05, sx0, 0.45, 2.93, zb0, zb1, WOOD_MED)
    add_span(sx1, sx1 + 0.05, 0.45, 2.93, zb0, zb1, WOOD_MED)
    add_span(sx0, sx1, 2.88, 2.93, zb0, zb1, WOOD_MED)
    kinds = ["household", "cans", "noodles", "biscuits", "snacks"]
    for k, kind in enumerate(kinds):
        yb = 0.5 + k * 0.48
        add_span(sx0, sx1, yb - 0.05, yb, zb0, zb1, WOOD_LIGHT)
        stock_shelf_row(kind, sx0 + 0.1, sx1 - 0.1, yb, 0.0)

    add_span(-6.9, -4.3, 0.45, 1.45, 1.6, 2.4, WOOD_MED)
    add_span(-6.95, -4.25, 1.45, 1.52, 1.55, 2.45, WOOD_LIGHT)
    for gx in (-6.5, -5.9, -5.3, -4.7):
        add_span(gx, gx + 0.04, 0.6, 1.35, 2.4, 2.42, vec(0.45, 0.28, 0.14))
    add_span(-5.2, -4.7, 1.52, 1.82, 1.8, 2.2, FENCE_METAL)
    for i, px in enumerate((-6.5, -6.2, -5.9)):
        cylinder(pos=vec(px, 1.52, 2.0), axis=vec(0, 0.22, 0), radius=0.1,
                 color=PRODUCT_COLORS[i])

    make_refrigerator(-4.0, -3.0, 0.45, 2.65, 2.0, 3.0)

def create_store_entrance():
    for top, zf in ((0.13, 5.5), (0.27, 5.0), (0.40, 4.5)):
        add_span(STORE_OPEN_X0, STORE_OPEN_X1, 0, top, 4.1, zf, CONCRETE_PAD)
    make_planter(-8.6, 3.5)
    make_planter(-1.5, 4.9)

def create_suv_in_carport():
    make_suv(CAR_CX, CAR_CZ)

def create_fence_and_gates():
    for cx in FRONT_POST_X:
        make_fence_post(cx, FENCE_Z)
    for i in range(len(FRONT_POST_X) - 1):
        if i in FRONT_OPENING_AFTER:
            continue
        make_fence_run("x", FRONT_POST_X[i] + 0.4, FRONT_POST_X[i + 1] - 0.4, FENCE_Z)

    for zp in SIDE_POST_Z[1:]:
        make_fence_post(FENCE_X_LEFT, zp, lamp=False)
        make_fence_post(FENCE_X_RIGHT, zp, lamp=False)
    for za, zb in zip(SIDE_POST_Z[:-1], SIDE_POST_Z[1:]):
        make_fence_run("z", zb + 0.4, za - 0.4, FENCE_X_LEFT)
        make_fence_run("z", zb + 0.4, za - 0.4, FENCE_X_RIGHT)

    for bx in BACK_POST_X[1:-1]:
        make_fence_post(bx, FENCE_Z_BACK, lamp=False)
    for xa, xb in zip(BACK_POST_X[:-1], BACK_POST_X[1:]):
        make_fence_run("x", xa + 0.4, xb - 0.4, FENCE_Z_BACK)

    make_gate_panel("x", PED_GATE_X0, PED_GATE_X1, FENCE_Z, 0.25, 2.45, 5)
    make_gate_hardware(PED_GATE_X0, PED_GATE_X1, FENCE_Z, "left")

    mid = (VEH_GATE_X0 + VEH_GATE_X1) / 2
    make_gate_panel("x", VEH_GATE_X0, mid, FENCE_Z, 0.25, 2.45, 7)
    make_gate_panel("x", mid, VEH_GATE_X1, FENCE_Z, 0.25, 2.45, 7)
    make_gate_hardware(VEH_GATE_X0, mid, FENCE_Z, "right")
    make_gate_hardware(mid, VEH_GATE_X1, FENCE_Z, "left")

def create_walkway_side_fences():
    xr = WALK_FENCE_RIGHT_X
    zs = [FENCE_Z, 6.7, WALK_FENCE_END_Z]
    for zp in zs[1:]:
        make_fence_post(xr, zp, lamp=False)
    for za, zb in zip(zs[:-1], zs[1:]):
        make_fence_run("z", zb + 0.4, za - 0.4, xr)

    xl = WALK_FENCE_LEFT_X
    gate_post_z = DINING_GATE_Z0 - 0.4
    make_fence_post(xl, gate_post_z, lamp=False)
    make_fence_post(xl, WALK_FENCE_END_Z, lamp=False)
    make_fence_run("z", WALK_FENCE_END_Z + 0.4, gate_post_z - 0.4, xl)

    make_gate_panel("x", xl - 1.3, xl, DINING_GATE_Z1 - 0.05, 0.25, 2.45, 5)
    for hy in (0.6, 2.0):
        add_span(xl - 0.12, xl, hy - 0.1, hy + 0.1, DINING_GATE_Z1 - 0.15, DINING_GATE_Z1 + 0.05, CAR_BUMPER)
    add_span(xl - 0.1, xl + 0.1, 1.25, 1.45, DINING_GATE_Z0, DINING_GATE_Z0 + 0.06, CAR_BUMPER)

    make_paved_path(-8.3, STORE_OPEN_X0, DINING_GATE_Z0, DINING_GATE_Z1 - 0.1, 0.05, WALK_TILE, TILE_LINE, 0.6)

def create_balcony_railings():
    y0, y1 = GF_TOP, GF_TOP + 1.2
    make_railing_run("x", 0.5, 9.1, Z_SLAB - 0.1, y0, y1)
    make_railing_run("z", -1.9, Z_SLAB - 0.1, 9.1, y0, y1)
    make_railing_run("x", 5.2, 9.1, -1.9, y0, y1)
    make_railing_run("z", Z_HOUSE + 0.05, Z_SLAB - 0.1, 0.5, y0, y1)

    add_cylinder(vec(5.6, y0, 4.75), vec(5.6, y0 + 0.55, 4.75), 0.28, WALL_CREAM)
    make_shrub(5.6, 4.75, r=0.35, y=y0 + 0.55)

def create_dining_area():
    cx, cz = DINING_CX, DINING_CZ
    add_span(cx - 1.1, cx + 1.1, 0.92, 1.0, cz - 0.6, cz + 0.6, TABLE_BROWN)
    for lx in (-1.0, 1.0):
        for lz in (-0.5, 0.5):
            add_span(cx + lx - 0.04, cx + lx + 0.04, 0, 0.92, cz + lz - 0.04, cz + lz + 0.04, TABLE_BROWN)
    add_span(cx - 1.0, cx + 1.0, 0.8, 0.92, cz - 0.5 - 0.02, cz - 0.5 + 0.02, TABLE_BROWN)
    add_span(cx - 1.0, cx + 1.0, 0.8, 0.92, cz + 0.5 - 0.02, cz + 0.5 + 0.02, TABLE_BROWN)
    add_span(cx - 1.0 - 0.02, cx - 1.0 + 0.02, 0.8, 0.92, cz - 0.5, cz + 0.5, TABLE_BROWN)
    add_span(cx + 1.0 - 0.02, cx + 1.0 + 0.02, 0.8, 0.92, cz - 0.5, cz + 0.5, TABLE_BROWN)
    for dx in (-0.6, 0.6):
        make_chair(cx + dx, cz - 1.05, +1)
        make_chair(cx + dx, cz + 1.05, -1)
    make_umbrella(cx, cz)

def create_landscaping():
    for x, z, r in [(-11.2, 8.1, 0.45), (-1.7, 8.2, 0.35), (1.9, 8.2, 0.42),
                    (3.2, 8.2, 0.42), (10.2, 5.4, 0.55), (11.9, 7.4, 0.50), (12.7, 7.4, 0.42),
                    (12.8, 3.0, 0.55)]:
        make_shrub(x, z, r)
    make_palm(-10.9, 2.0, 3.8)
    make_palm(-9.4, 0.2, 3.2)

def create_exterior_lights():
    make_wall_lamp(-7.35, 2.3, Z_STORE)
    make_wall_lamp(-2.65, 2.3, Z_STORE)
    add_span(-6.2, -3.8, 3.15, 3.2, 0.8, 1.0, LIGHT_GLOW)

def setup_lighting():
    scene.lights = []
    scene.ambient = vec(0.45, 0.45, 0.48)
    distant_light(direction=vec(0.4, -0.7, -0.5), color=vec(0.85, 0.83, 0.80))
    distant_light(direction=vec(-0.4, -0.3, 0.6), color=vec(0.25, 0.25, 0.30))

HOME_CENTER = vec(0.3, 4.6, 0.3)
HOME_POS    = vec(0.3, 5.6, 30.8)
HOME_FOV    = 0.7

MIN_DIST  = 12.0
MAX_DIST  = 48.0
MAX_ELEV  = math.radians(50)
MIN_CAM_Y = 1.0

def reset_view(btn=None):
    scene.up = vec(0, 1, 0)
    scene.fov = HOME_FOV
    scene.center = HOME_CENTER
    scene.camera.pos = HOME_POS
    scene.camera.axis = HOME_CENTER - HOME_POS

def setup_camera():
    scene.userspin = True
    scene.userzoom = True
    scene.userpan = False
    reset_view()

def setup_camera_controls():
    scene.append_to_caption("\n")
    button(text="Reset View", bind=reset_view)
    scene.append_to_caption("   Rotate: right-drag  |  Zoom: mouse wheel  |  Reset View: front view\n")

def enforce_view_limits():
    off = scene.camera.pos - HOME_CENTER
    d = mag(off)
    if d < 1e-6:
        reset_view()
        return
    horiz = math.sqrt(off.x * off.x + off.z * off.z)
    elev = math.atan2(off.y, horiz)

    new_d = min(max(d, MIN_DIST), MAX_DIST)
    sin_min = max(-1.0, min(1.0, (MIN_CAM_Y - HOME_CENTER.y) / new_d))
    new_elev = min(max(elev, math.asin(sin_min)), MAX_ELEV)

    drifted = mag(scene.center - HOME_CENTER) > 1e-3
    if not drifted and abs(new_d - d) < 1e-3 and abs(new_elev - elev) < 1e-4:
        return

    if horiz < 1e-6:
        hx, hz = 0.0, 1.0
    else:
        hx, hz = off.x / horiz, off.z / horiz
    new_off = vec(hx * math.cos(new_elev) * new_d,
                  math.sin(new_elev) * new_d,
                  hz * math.cos(new_elev) * new_d)
    scene.center = HOME_CENTER
    scene.camera.pos = HOME_CENTER + new_off
    scene.camera.axis = HOME_CENTER - scene.camera.pos

def main():
    create_environment()
    create_foundation()
    create_store_shell()
    create_main_structure()
    create_roofs()
    create_doors_and_windows()

    create_street_and_paths()
    create_store_sign()
    create_store_interior()
    create_store_entrance()
    create_suv_in_carport()
    create_fence_and_gates()
    create_walkway_side_fences()
    create_balcony_railings()
    create_dining_area()
    create_landscaping()
    create_exterior_lights()
    setup_lighting()
    setup_camera()
    setup_camera_controls()

    print("Loaded successfully.")

    while True:
        rate(30)
        enforce_view_limits()

if __name__ == "__main__":
    main()
