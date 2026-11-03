from vpython import *
from math import sin, cos, pi

scene = canvas(title="MY DREAM HOUSE", width=1200, height=760,
               background=vector(0.78, 0.88, 0.98))
scene.autoscale = False
scene.center = vector(0, 3.7, -0.2)
scene.range = 29
scene.forward = vector(-1.05, -0.78, -1.25)

ivory = vector(0.91, 0.89, 0.82)
sand = vector(0.70, 0.63, 0.51)
stone = vector(0.49, 0.50, 0.49)
charcoal = vector(0.105, 0.13, 0.15)
wood = vector(0.42, 0.24, 0.12)
wood_light = vector(0.61, 0.39, 0.21)
glass = vector(0.23, 0.61, 0.76)
grass = vector(0.22, 0.43, 0.22)
leaf = vector(0.10, 0.31, 0.15)
leaf_light = vector(0.23, 0.48, 0.23)
paver = vector(0.72, 0.70, 0.63)
water = vector(0.07, 0.49, 0.70)
gold = vector(0.85, 0.66, 0.32)
warm = vector(1.0, 0.76, 0.40)
cushion = vector(0.87, 0.84, 0.76)
cream = ivory

lights = []
animated_gate_parts = []
animated_door_parts = []
ripple_rings = []
gate_is_open = False
gate_busy = False
gate_progress = 0.0
gate_travel = 5.4
door_is_open = False
door_busy = False
door_progress = 0.0
animations_running = True
lights_on = True

def V(p):
    return vector(*p)

def bx(pos, size, color, opacity=1.0):
    return box(pos=V(pos), size=V(size), color=color, opacity=opacity)

def cy(pos, axis, radius, color, **kwargs):
    return cylinder(pos=V(pos), axis=V(axis), radius=radius,
                    color=color, **kwargs)

def sp(pos, radius, color, **kwargs):
    return sphere(pos=V(pos), radius=radius, color=color, **kwargs)

def cone_obj(pos, axis, radius, color):
    return cone(pos=V(pos), axis=V(axis), radius=radius, color=color)

def add_light(pos, scale=1.0):
    housing = bx(pos, (0.20*scale, 0.38*scale, 0.12*scale), charcoal)
    bulb = sp((pos[0], pos[1]-0.02*scale, pos[2]-0.075*scale),
              0.075*scale, warm, emissive=True)
    lights.append(bulb)
    return housing, bulb

def build_palm(x, z, height=5.4):

    cy((x, 0.03, z), (0, height*0.82, 0), 0.19, wood)
    sp((x, height*0.81, z), 0.27, wood_light)
    crown_y = height*0.82

    for i in range(8):
        a = 2*pi*i/8
        dx, dz = cos(a), sin(a)
        end = vector(x + dx*1.65, crown_y-0.62, z + dz*1.65)
        start = vector(x, crown_y, z)
        stem = cylinder(pos=start, axis=end-start, radius=0.045,
                        color=leaf_light)

        for t in (0.28, 0.43, 0.58, 0.72, 0.84):
            p = start + (end-start)*t
            side = vector(-dz, 0, dx)
            length = 0.48*(1-t*0.55)
            for sign in (-1, 1):
                tip = p + side*sign*length + vector(dx*0.10, -0.12, dz*0.10)
                cylinder(pos=p, axis=tip-p, radius=0.018,
                         color=leaf if i%2 else leaf_light)

        frond_group = [stem]

        palm_fronds.append((stem, start, end, a))

def build_bird_of_paradise(x, z, height=1.15):
    cy((x, 0.04, z), (0, 0.22, 0), 0.16, sand)
    for i in range(6):
        a = i*2*pi/6
        end = vector(x+0.48*cos(a), height, z+0.48*sin(a))
        cylinder(pos=vector(x, 0.18, z), axis=end-vector(x, 0.18, z),
                 radius=0.035, color=leaf_light)

        blade = cone(pos=end-vector(0,0.12,0), axis=vector(0,0.48,0),
                     radius=0.17, color=leaf if i%2 else leaf_light)

def build_shrub(x, z, radius=0.42):
    for dx, dz, r in [(0,0,1),(.25,.1,.72),(-.22,.12,.70),(.08,-.23,.68)]:
        sp((x+dx, 0.35, z+dz), radius*r, leaf if int((x+z)*10)%2 else leaf_light)

def build_planter(x, z, sx=1.0, sz=1.0):
    bx((x,0.24,z),(sx,0.48,sz),stone)
    bx((x,0.50,z),(sx+0.08,0.08,sz+0.08),sand)
    build_bird_of_paradise(x,z,0.95)

def build_ground():
    bx((0,-0.34,0),(44,0.68,36),grass)

    bx((0,0.02,-17.55),(44,0.14,1.0),paver)
    bx((0,0.04,-16.78),(44,0.10,0.30),stone)

    bx((0,0.035,-9.0),(7.5,0.13,14.6),stone)

    for x in (-3.88,3.88):
        bx((x,0.12,-9.0),(0.16,0.06,14.7),charcoal)

    for z in (-15.4,-13.3,-11.2,-9.1,-7.0,-4.9,-2.8):
        bx((0,0.105,z),(7.45,0.018,0.035),sand)

    for z in (-3.5,-2.5,-1.5):
        bx((0,0.145,z),(2.35,0.12,0.62),ivory)

    bx((0,0.10,-1.45),(4.2,0.12,1.5),paver)

def build_window_front(x, y, width, height, z):
    """Centered front window with a timber perimeter and inset glazing.

    (x, y) is the single center reference for the entire window.
    All frame and glass coordinates are calculated from that center,
    so the glass stays inside the frame rather than crossing it.
    """
    frame_t = 0.065
    frame_depth = 0.060
    glass_depth = 0.028
    mullion_t = 0.035

    frame_z = z - 0.035
    glass_z = frame_z + frame_depth * 0.50 + glass_depth * 0.50 + 0.008

    clear_w = max(0.10, width - 2 * frame_t)
    clear_h = max(0.10, height - 2 * frame_t)

    pane_w = max(0.05, (clear_w - mullion_t) / 2)
    pane_offset = mullion_t / 2 + pane_w / 2
    bx((x - pane_offset, y, glass_z),
       (pane_w, clear_h, glass_depth), glass, 0.62)
    bx((x + pane_offset, y, glass_z),
       (pane_w, clear_h, glass_depth), glass, 0.62)

    side_h = height - 2 * frame_t
    for xx in (x - width/2 + frame_t/2,
               x + width/2 - frame_t/2):
        bx((xx, y, frame_z), (frame_t, side_h, frame_depth), wood)

    for yy in (y - height/2 + frame_t/2,
               y + height/2 - frame_t/2):
        bx((x, yy, frame_z), (width, frame_t, frame_depth), wood)

    bx((x, y, frame_z - 0.003),
       (mullion_t, clear_h, frame_depth + 0.006), wood_light)

def build_house():

    bx((0,1.68,3),(12,3.36,10),ivory)

    bx((5.30,1.72,-2.075),(1.40,3.30,0.13),sand)

    bx((0,5.18,3.55),(10.1,3.62,8.25),ivory)

    bx((-4.35,5.16,-0.67),(1.25,3.48,0.16),stone)

    bx((0,3.43,3),(12.65,0.26,10.65),charcoal)
    bx((0,3.59,3),(12.30,0.10,10.30),sand)
    bx((0,7.03,3.55),(10.65,0.32,8.85),charcoal)
    bx((0,7.22,3.55),(10.25,0.10,8.48),stone)

    bx((0,3.26,-2.37),(12.8,0.15,0.22),wood)
    bx((0,3.17,-2.39),(12.8,0.06,0.25),charcoal)

    bx((0,6.82,-0.77),(10.8,0.15,0.34),wood)

    bx((-5.18,1.78,-2.105),(1.35,3.05,0.16),wood)
    for x in (-5.68,-5.43,-5.18,-4.93,-4.68):
        bx((x,1.82,-2.205),(0.055,2.90,0.055),wood_light)

    bx((0,2.79,-2.56),(2.82,0.12,1.13),wood_light)

    bx((0, 1.20, -2.12), (1.38, 2.38, 0.06), charcoal)
    door_panel = bx((0,1.20,-2.19),(1.40,2.40,0.13),wood)
    gold_lines = []
    for x in (-0.45,-0.15,0.15,0.45):
        gold_lines.append(bx((x,1.20,-2.27),(0.035,2.25,0.025),gold))
    door_handle = sp((0.48,1.23,-2.31),0.065,gold)
    door_hinge_x, door_hinge_z = -0.70, -2.19
    for obj, is_box in [(door_panel, True)] + [(g, True) for g in gold_lines] + [(door_handle, False)]:
        orig_p = vector(obj.pos)
        orig_sx = obj.size.x if is_box else 0.0
        animated_door_parts.append((obj, is_box, orig_p, orig_sx, orig_p.x - door_hinge_x, orig_p.z - door_hinge_z))
    for x in (-0.94,0.94):
        bx((x,1.35,-2.20),(0.35,2.05,0.08),glass,0.50)

    build_window_front(-3.15,1.86,2.05,2.28,-2.16)
    build_window_front(3.12,1.86,2.05,2.28,-2.16)

    door_x, door_y, door_z = 0.25, 5.18, -0.72
    door_w, door_h = 3.35, 2.42
    bx((door_x,door_y,door_z),(door_w,door_h,0.075),glass,0.50)
    frame_z = door_z-0.065
    for xx in (door_x-door_w/2, door_x, door_x+door_w/2):
        bx((xx,door_y,frame_z),(0.075,door_h+0.12,0.10),charcoal)
    for yy in (door_y-door_h/2,door_y+door_h/2):
        bx((door_x,yy,frame_z),(door_w+0.12,0.075,0.10),charcoal)
    bx((door_x+0.06,door_y,frame_z-0.015),(0.035,door_h-0.12,0.035),stone)
    for xx in (door_x-0.10,door_x+0.18):
        bx((xx,door_y-0.02,frame_z-0.04),(0.035,0.22,0.025),gold)

    upper_win_y = 5.98
    upper_win_w, upper_win_h = 1.55, 1.50
    window_door_spacing = 2.85
    left_window_x = door_x - window_door_spacing
    right_window_x = door_x + window_door_spacing
    window_front_z = -0.72
    build_window_front(left_window_x, upper_win_y,
                       upper_win_w, upper_win_h, window_front_z)
    build_window_front(right_window_x, upper_win_y,
                       upper_win_w, upper_win_h, window_front_z)

    wood_screen_center_x = -4.35
    bx((wood_screen_center_x,5.15,-0.73),(0.82,2.78,0.13),wood)
    for x in (wood_screen_center_x-0.30, wood_screen_center_x-0.10,
              wood_screen_center_x+0.10, wood_screen_center_x+0.30):
        bx((x,5.15,-0.82),(0.045,2.60,0.045),wood_light)

    bx((0.25,3.78,-1.35),(7.9,0.22,2.25),sand)
    bx((0.25,3.91,-1.35),(7.75,0.06,2.13),stone)

    rail_y, rail_h, front_z = 4.415, 1.05, -2.49
    balcony_left, balcony_right = -3.60, 4.10
    span = balcony_right-balcony_left
    bx(((balcony_left+balcony_right)/2,rail_y,front_z),
       (span,rail_h,0.075),glass,0.34)
    bx(((balcony_left+balcony_right)/2,rail_y+rail_h/2,front_z),
       (span+0.10,0.085,0.10),charcoal)
    bx(((balcony_left+balcony_right)/2,rail_y-rail_h/2,front_z),
       (span+0.10,0.075,0.10),charcoal)
    for i in range(9):
        x=balcony_left+i*span/8
        bx((x,rail_y,front_z),(0.065,rail_h,0.075),charcoal)

    side_z_front, side_z_back = front_z, -0.28
    side_len = abs(side_z_back-side_z_front)
    for x in (balcony_left, balcony_right):
        bx((x,rail_y,(side_z_front+side_z_back)/2),
           (0.075,rail_h,side_len),glass,0.34)
        bx((x,rail_y+rail_h/2,(side_z_front+side_z_back)/2),
           (0.10,0.085,side_len+0.06),charcoal)
        bx((x,rail_y-rail_h/2,(side_z_front+side_z_back)/2),
           (0.10,0.075,side_len+0.06),charcoal)
        for zpost in (side_z_front,side_z_back):
            bx((x,rail_y,zpost),(0.075,rail_h,0.075),charcoal)

    for x in (-2.8,2.8):
        bx((x,4.04,-1.65),(0.72,0.22,0.46),sand)
        build_shrub(x,-1.65,0.20)

    for z in (0.2,3.0,5.7):
        bx((6.012,1.90,z),(0.024,1.38,1.48),glass,0.58)

        for zz in (z-0.77,z+0.77):
            bx((6.026,1.90,zz),(0.028,1.48,0.045),charcoal)
        for y in (1.205,2.595):
            bx((6.026,y,z),(0.028,0.045,1.54),charcoal)

    for z in (1.4,4.7):
        bx((5.045,5.18,z),(0.018,1.52,1.38),glass,0.55)
        for zz in (z-0.72,z+0.72):
            bx((5.054,5.18,zz),(0.020,1.58,0.045),charcoal)
        for y in (4.405,5.955):
            bx((5.054,y,z),(0.020,0.045,1.48),charcoal)

    for x in (-1.45,1.45):
        add_light((x,2.16,-2.28),0.85)
    add_light((5.30,2.3,-2.26),0.8)

    bx((0,0.18,-2.55),(3.2,0.20,1.0),stone)
    bx((0,0.10,-3.20),(3.8,0.12,0.50),paver)

    for x in (-4.0,4.0):
        bx((x,7.39,5.8),(1.6,0.30,0.65),sand)
        build_shrub(x,5.8,0.26)

def build_fence():

    h=1.72

    bx((-14.5,0.77,-16),(11.0,1.54,0.18),charcoal)
    bx((14.5,0.77,-16),(11.0,1.54,0.18),charcoal)
    for x in list(range(-19,-9))+list(range(10,20)):
        for y in (0.36,0.72,1.08,1.44):
            bx((x,y,-16.08),(0.90,0.075,0.10),stone)

    bx((0,h/2,16),(40,h,0.18),charcoal)
    for x in range(-19,20):
        for y in (0.38,0.76,1.14,1.52):
            bx((x,y,16.08),(0.88,0.075,0.10),stone)

    for x in (-20,20):
        bx((x,h/2,0),(0.18,h,32),charcoal)
        for z in range(-15,16):
            for y in (0.38,0.76,1.14,1.52):
                bx((x+(-0.08 if x<0 else 0.08),y,z),(0.10,0.075,0.88),stone)

    for x in (-20,-14,-9,9,14,20):
        bx((x,0.96,-16),(0.52,1.92,0.52),sand)
        bx((x,1.96,-16),(0.68,0.12,0.68),charcoal)
        add_light((x,2.18,-16),0.72)
    for x in (-20,-10,0,10,20):
        bx((x,0.96,16),(0.48,1.92,0.48),sand)
        bx((x,1.96,16),(0.62,0.12,0.62),charcoal)
    for z in range(-12,17,4):
        for x in (-20,20):
            bx((x,0.96,z),(0.46,1.92,0.46),sand)

    bx((-6.8,1.20,-16.16),(1.25,0.52,0.10),charcoal)
    for dx in (-0.20,0,0.20):
        bx((-6.8+dx,1.20,-16.23),(0.055,0.25,0.025),gold)

def build_gate_panel(center_x, width=4.0):
    panel_parts = []

    panel_parts.append(bx((center_x,0.92,-16.25),(width,1.68,0.16),charcoal))
    panel_parts.append(bx((center_x,0.18,-16.34),(width,0.10,0.08),wood_light))
    panel_parts.append(bx((center_x,1.66,-16.34),(width,0.10,0.08),wood_light))
    for x in (center_x-width/2,center_x+width/2):
        panel_parts.append(bx((x,0.92,-16.34),(0.10,1.58,0.10),charcoal))

    for i in range(13):
        x=center_x-width/2+0.22+i*(width-0.44)/12
        panel_parts.append(bx((x,0.92,-16.405),(0.055,1.42,0.055),sand))

    for x in (center_x-width*0.34,center_x+width*0.34):
        panel_parts.append(cylinder(pos=vector(x,0.12,-16.29),
            axis=vector(0,0.12,0),radius=0.105,color=charcoal))
        panel_parts.append(cylinder(pos=vector(x,0.12,-16.425),
            axis=vector(0,0.02,0),radius=0.045,color=gold))
    panel_parts.append(bx((center_x,0.12,-16.30),(width,0.08,0.12),stone))
    homes_z = [obj.pos.z for obj in panel_parts]
    homes_x = [obj.pos.x for obj in panel_parts]
    animated_gate_parts.append((panel_parts, homes_z, homes_x, center_x))
    return panel_parts

def build_gate():

    build_gate_panel(-2.0)
    build_gate_panel(2.0)

    bx((0,0.045,-16.29),(8.55,0.07,0.15),charcoal)
    bx((0,0.09,-16.38),(8.55,0.035,0.045),gold)

    for x in (-8.95,8.95):
        bx((x,0.38,-16.26),(0.50,0.70,0.52),charcoal)
        bx((x,0.76,-16.26),(0.58,0.08,0.60),stone)

    for x in (-4.12,4.12):
        bx((x,0.88,-16.03),(0.12,1.76,0.16),charcoal)

    for x in (-6.5, 6.5):
        bx((x, 0.92, -16.0), (5.0, 1.78, 0.16), charcoal)

        for i in range(16):
            sx = x - 2.35 + i * (4.70 / 15)
            bx((sx, 0.92, -16.095), (0.055, 1.50, 0.045), sand)

        bx((x, 1.82, -16.0), (5.0, 0.10, 0.18), charcoal)
        bx((x, 0.08, -16.0), (5.0, 0.10, 0.18), charcoal)

def build_pool():

    bx((11,0.015,5),(12.6,0.15,10.4),paver)

    bx((11,0.12,5),(9.65,0.24,7.55),charcoal)
    bx((11,0.23,5),(9.22,0.08,7.12),glass)

    water_surface=bx((11,0.285,5),(8.90,0.055,6.80),water)

    for x in (6.18,15.82):
        bx((x,0.30,5),(0.22,0.20,7.65),ivory)
    for z in (1.17,8.83):
        bx((11,0.30,z),(9.75,0.20,0.22),ivory)

    for i in range(3):
        bx((11,0.35+i*0.025,1.78+i*0.42),(2.3,0.10,0.38),
           vector(0.38+0.08*i,0.68+0.04*i,0.76))

    for x in (5.5,7.0,8.5,10.0,11.5,13.0,14.5,16.0):
        bx((x,0.105,5),(0.025,0.012,9.7),sand)

    for z in (3.0,7.0):
        bulb=sp((6.78,0.31,z),0.18,vector(0.55,0.90,1.0),
                emissive=True)
        lights.append(bulb)

    for i in range(5):
        ring=sphere(pos=vector(9.2+i*0.70,0.33,4.1+(i%2)*1.5),
                    radius=0.22, color=vector(0.45,0.85,0.96),
                    opacity=0.48)
        ripple_rings.append((ring, i*1.23))

    for z in (2.35,4.55,6.75):
        bx((17.15,0.30,z),(1.18,0.16,1.85),ivory)
        bx((17.15,0.43,z-0.42),(1.05,0.10,0.62),cushion)
        bx((17.15,0.55,z-0.72),(1.05,0.10,0.48),ivory)
        for x in (16.75,17.55):
            cy((x,0.12,z),(0,0.18,0),0.035,charcoal)

    cy((18.25,0.18,4.4),(0,0.28,0),0.30,wood_light)
    cy((18.25,0.47,4.4),(0,0.045,0),0.31,charcoal)
    cy((18.32,0.50,4.4),(0,0.16,0),0.045,gold)

    cy((18.5,0,7.2),(0,2.55,0),0.055,charcoal)
    cone_obj((18.5,2.52,7.2),(0,0.26,0),1.35,ivory)

    build_planter(5.0,1.5,0.95,0.95)
    build_planter(5.0,8.5,0.95,0.95)
    cy((15.7,0,9.0),(0,2.1,0),0.055,charcoal)
    cy((15.7,2.1,9.0),(0.48,0,0),0.055,charcoal)
    sp((16.12,2.1,9.0),0.11,stone)

def build_lounge():

    bx((-10,0.035,5),(8.7,0.15,8.7),paver)

    bx((-10,0.125,5),(5.9,0.055,4.5),wood)
    bx((-10,0.16,5),(5.65,0.035,4.25),cushion)
    for z in (3.2,4.1,5.0,5.9,6.8):
        bx((-10,0.183,z),(5.5,0.012,0.025),sand)

    for x in (-13.7,-6.3):
        for z in (1.3,8.7):
            bx((x,2.05,z),(0.22,4.1,0.22),wood)
            bx((x,4.13,z),(0.34,0.12,0.34),wood_light)
    for z in (1.3,8.7):
        bx((-10,4.10,z),(7.55,0.24,0.24),wood)

    for x in (-13.45,-12.55,-11.65,-10.75,-9.85,-8.95,-8.05,-7.15,-6.55):
        bx((x,4.18,5),(0.16,0.16,7.45),wood_light)

    bx((-10,4.31,5),(7.28,0.075,7.18),glass,0.22)

    for x in (-13.72,-6.28):
        bx((x,4.34,5),(0.12,0.10,7.55),wood)
    for z in (1.22,8.78):
        bx((-10,4.34,z),(7.55,0.10,0.12),wood)

    for x in (-12.55,-11.05,-9.55,-8.05,-6.85):
        bx((x,4.355,5),(0.025,0.018,7.08),stone)

    for x in (-11.7,-8.3):
        cy((x,4.08,4.2),(0,-0.42,0),0.018,charcoal)
        bulb=sp((x,3.60,4.2),0.11,warm,emissive=True)
        lights.append(bulb)

    bx((-10,0.55,2.65),(4.0,0.52,1.05),ivory)
    bx((-10,0.98,3.05),(4.0,0.72,0.20),wood)
    for x in (-11.82,-10.92,-10.02,-9.12,-8.22):
        bx((x,0.86,2.70),(0.78,0.18,0.78),cushion)
        bx((x,1.18,3.05),(0.74,0.48,0.16),cushion)
    for x in (-12.0,-8.0):
        bx((x,0.83,2.65),(0.22,0.76,1.12),wood)

    bx((-10,0.65,4.70),(2.0,0.14,1.05),wood_light)
    for x in (-10.75,-9.25):
        for z in (4.35,5.05):
            bx((x,0.34,z),(0.075,0.55,0.075),charcoal)
    cy((-10,0.75,4.65),(0,0.08,0),0.18,stone)
    sp((-9.55,0.79,4.7),0.10,gold)

    for x in (-12.2,-7.8):
        bx((x,0.48,6.75),(1.25,0.22,1.42),wood)
        bx((x,0.63,6.72),(1.10,0.12,1.23),cushion)
        bx((x,0.89,7.23),(1.12,0.48,0.16),cushion)
        for dx in (-0.50,0.50):
            bx((x+dx,0.40,6.75),(0.06,0.45,1.25),charcoal)

    build_planter(-13.45,5.0,0.90,0.90)
    build_planter(-6.55,5.0,0.90,0.90)

    cy((-7.1,0.18,7.15),(0,0.40,0),0.25,wood_light)
    cy((-7.1,0.60,7.15),(0,0.05,0),0.27,charcoal)

def build_landscape():

    for x,z,h in [(-17.4,11.5,6.0),(-17.4,3.5,5.2),(-17.4,-10.0,5.4),
                  (17.8,12.0,6.1),(17.8,-10.0,5.2),(-12.0,12.5,4.8)]:
        build_palm(x,z,h)

    for x in (-15.8,-13.6,-11.4,11.4,13.6,15.8):
        bx((x,0.06,-12.3),(1.65,0.12,1.75),sand)
        build_bird_of_paradise(x,-12.3,0.92)
        build_shrub(x+0.52,-12.0,0.28)

    for x in (-18.5,18.5):
        for z in (-7,-3,1,5,9):
            build_shrub(x,z,0.36)

    for x,z in [(-15,7),(-14,8),(-13,7),(14,10),(15,9),(16,10)]:
        build_shrub(x,z,0.27)

    for z in (-14.2,-11.4,-8.6,-5.8,-3.0):
        for x in (-4.35,4.35):
            cy((x,0,z),(0,0.70,0),0.07,charcoal)
            bulb=sp((x,0.76,z),0.12,warm,emissive=True)
            lights.append(bulb)

    for x,z in [(-16,5),(-15.5,5.4),(16,11),(15.5,11.4)]:
        sp((x,0.18,z),0.30,stone)

palm_fronds=[]

build_ground()
build_house()
build_fence()
build_gate()
build_pool()
build_lounge()
build_landscape()

distant_light(direction=vector(-1,-1,-0.5), color=vector(0.92,0.90,0.84))
distant_light(direction=vector(1,-0.45,1), color=vector(0.55,0.62,0.72))
scene.center=vector(0,3.7,0)
scene.range=29
scene.forward=vector(-1.05,-0.78,-1.25)

def set_gate_open(want_open):
    """Two-leaf sliding gate: tuck inward, then slide sideways behind infill."""
    global gate_is_open, gate_busy, gate_progress
    if gate_busy:
        return
    if door_is_open:
        set_door_open(False)
        return
    gate_busy = True
    target = 1.0 if want_open else 0.0
    direction = 1 if target > gate_progress else -1

    steps = 56
    while abs(gate_progress - target) > 0.001:
        rate(60)
        gate_progress += direction / steps
        gate_progress = max(0.0, min(1.0, gate_progress))
        p = gate_progress
        tuck = 0.52 * min(p / 0.18, 1.0)
        slide_ratio = max(0.0, min((p - 0.18) / 0.82, 1.0))
        slide = gate_travel * slide_ratio

        for parts, home_zs, home_xs, center_x in animated_gate_parts:
            side = -1 if center_x < 0 else 1
            for obj, home_z, home_x in zip(parts, home_zs, home_xs):
                obj.pos.x = home_x + side * slide
                obj.pos.z = home_z + tuck

        if abs(gate_progress - target) < 1.0 / steps:
            gate_progress = target

    p = gate_progress
    tuck = 0.52 * min(p / 0.18, 1.0)
    slide = gate_travel * max(0.0, min((p - 0.18) / 0.82, 1.0))
    for parts, home_zs, home_xs, center_x in animated_gate_parts:
        side = -1 if center_x < 0 else 1
        for obj, home_z, home_x in zip(parts, home_zs, home_xs):
            obj.pos.x = home_x + side * slide
            obj.pos.z = home_z + tuck

    gate_is_open = (target == 1.0)
    gate_busy = False
    gate_button.text = "Close gate" if gate_is_open else "Open gate"

def toggle_gate(btn):
    set_gate_open(not gate_is_open)

def update_door_pose(p):
    """Front door swing pose: rotates outward onto the covered front porch."""
    door_hinge_x, door_hinge_z = -0.70, -2.19
    max_angle = 1.35
    theta = p * max_angle
    cos_t = cos(theta)
    sin_t = sin(theta)
    for obj, is_box, orig_p, orig_sx, dx0, dz0 in animated_door_parts:
        dx = dx0 * cos_t + dz0 * sin_t
        dz = -dx0 * sin_t + dz0 * cos_t
        obj.pos.x = door_hinge_x + dx
        obj.pos.y = orig_p.y
        obj.pos.z = door_hinge_z + dz
        if is_box:
            obj.axis = vector(orig_sx * cos_t, 0, -orig_sx * sin_t)

def set_door_open(want_open):
    """Front door smooth swing animation."""
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
        update_door_pose(door_progress)
        if abs(door_progress - target) < 1.0 / steps:
            door_progress = target

    door_progress = target
    update_door_pose(door_progress)
    door_is_open = (target == 1.0)
    door_busy = False
    door_button.text = "Close door" if door_is_open else "Open door"

def toggle_door(btn):
    set_door_open(not door_is_open)

def toggle_lights(btn):
    global lights_on
    lights_on=not lights_on
    for bulb in lights:
        bulb.visible=lights_on
    btn.text="Lights: ON" if lights_on else "Lights: OFF"

def toggle_animations(btn):
    global animations_running
    animations_running=not animations_running
    btn.text="Pause motion" if animations_running else "Resume motion"

def reset_scene(btn):

    if gate_busy or door_busy:
        return
    if door_is_open:
        set_door_open(False)
    if gate_is_open:
        set_gate_open(False)
    for bulb in lights:
        bulb.visible=lights_on
    for ring, phase in ripple_rings:
        ring.visible=True
    print("Scene reset: gate closed; display settings retained.")

scene.append_to_caption("\n\n")
gate_button=button(text="Open gate", bind=toggle_gate)
scene.append_to_caption("   ")
door_button=button(text="Open door", bind=toggle_door)
scene.append_to_caption("   ")
light_button=button(text="Lights: ON", bind=toggle_lights)
scene.append_to_caption("   ")
motion_button=button(text="Pause motion", bind=toggle_animations)
scene.append_to_caption("   ")
button(text="Reset", bind=reset_scene)
scene.append_to_caption("\nDrag: rotate | Wheel: zoom | Right-drag: pan\n")

time_phase=0.0
while True:
    rate(40)
    if not animations_running:
        continue
    time_phase += 0.045

    for ring, phase in ripple_rings:
        pulse=0.75+0.25*sin(time_phase*1.25+phase)
        ring.radius=0.16+0.07*pulse
        ring.opacity=0.28+0.20*(0.5+0.5*sin(time_phase+phase))
        ring.pos.y=0.335+0.018*sin(time_phase+phase)

    if lights_on:
        glow=0.72+0.28*(0.5+0.5*sin(time_phase*1.4))
        for bulb in lights:
            bulb.color=vector(1.0,0.73*glow,0.36*glow)