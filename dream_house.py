"""Furnished tropical home. Run with Python and the vpython package."""
from math import sin, cos, pi
from random import Random
from vpython import (canvas, vector as V, box, cylinder, sphere, ellipsoid,
                     cone, curve, label, distant_light, local_light,
                     menu, button, checkbox, rate)

scene = canvas(title='TROPICAL HOUSE | A home among the palms\n', width=1200,
               height=760, background=V(.58, .78, .94))
scene.autoscale = False
scene.ambient = V(.48, .48, .46)
scene.lights = []
distant_light(direction=V(-1, 2, 1), color=V(.85, .79, .65))
distant_light(direction=V(1, 1, -1), color=V(.3, .36, .43))
CREAM, CLAY, WOOD = V(.91, .87, .76), V(.64, .36, .28), V(.39, .23, .12)
BLACK, GLASS, WHITE = V(.055, .065, .065), V(.19, .34, .38), V(.95, .94, .87)
GREEN, STONE = V(.25, .43, .12), V(.63, .63, .57)
groups = {k: [] for k in ('site', 'ground', 'upper', 'shell0', 'shell1', 'roof')}
group = 'site'
room_labels, lamps, gate_parts = [], [], []
rng = Random(12)


def keep(obj):
    groups[group].append(obj)
    return obj


def block(x, y, z, sx, sy, sz, col=CREAM, **kwargs):
    return keep(box(pos=V(x, y, z), size=V(sx, sy, sz), color=col, **kwargs))


def rod(a, b, radius=.035, col=BLACK):
    return keep(cylinder(pos=V(*a), axis=V(*b)-V(*a), radius=radius, color=col))


def ball(x, y, z, radius, col):
    return keep(sphere(pos=V(x, y, z), radius=radius, color=col))


def room(text, x, y, z, floor):
    obj = label(pos=V(x, y, z), text=text, height=12, box=False,
                color=V(.12, .18, .15), opacity=0, visible=False)
    room_labels.append((obj, floor))


def table(x, y, z, w=1.6, d=.9, h=.76, col=WOOD):
    block(x, y+h, z, w, .09, d, col)
    for dx in (-w/2+.1, w/2-.1):
        for dz in (-d/2+.1, d/2-.1):
            block(x+dx, y+h/2, z+dz, .065, h, .065, BLACK)


def chair(x, y, z, facing=1):
    block(x, y+.46, z, .48, .12, .5, V(.65, .63, .48))
    block(x, y+.79, z+.22*facing, .48, .62, .07, WOOD)
    for dx in (-.18, .18):
        for dz in (-.18, .18):
            block(x+dx, y+.23, z+dz, .045, .46, .045, BLACK)


def plant(x, y, z, scale=1):
    keep(cone(pos=V(x, y+.35*scale, z), axis=V(0, -.35*scale, 0),
              radius=.24*scale, color=CLAY))
    for i in range(7):
        a = i*2*pi/7
        leaf = keep(ellipsoid(pos=V(x+.19*scale*cos(a), y+.65*scale,
                                   z+.19*scale*sin(a)),
                              size=V(.16*scale, .8*scale, .12*scale), color=GREEN))
        leaf.rotate(angle=.55, axis=V(sin(a), 0, -cos(a)))


def window(x, y, z, w, h):
    block(x, y, z, w, h, .055, GLASS, opacity=.45)
    for dx in (-w/2, w/2):
        block(x+dx, y, z+.04, .065, h+.08, .09, BLACK)
    for dy in (-h/2, h/2):
        block(x, y+dy, z+.04, w+.08, .065, .09, BLACK)
    for i in range(1, 4):
        block(x-w/2+w*i/4, y, z+.04, .045, h, .08, BLACK)


def lamp(x, y, z):
    block(x, y, z, .18, .09, .18, V(1, .83, .46), emissive=True)


# Lot: front faces positive Z; two floors at Y=.25 and Y=3.55.
block(0, -.18, 0, 23, .3, 22, V(.31, .47, .17))
block(0, -.09, 9, 25, .12, 3.2, V(.43, .45, .45))
block(0, .01, 7, 24, .18, 1.1, STONE)
for x in range(-12, 13, 2):
    block(x, .105, 7, .025, .012, 1.1, V(.38, .39, .36))
block(1.8, .04, 3.8, 3.4, .15, 5.4, STONE)
for z in (2, 3, 4, 5, 6):
    block(1.8, .12, z, 3.4, .015, .03, V(.45, .45, .41))
block(-7.5, 1.65, -.6, .2, 3.3, 13, V(.51, .52, .49))

# Foundation and ground-floor furnishing.
group = 'ground'
block(0, .12, -1.5, 10, .25, 9, STONE)
block(0, .26, -1.5, 9.7, .04, 8.7, V(.81, .77, .66))
for x in range(-4, 5):
    block(x, .286, -1.5, .012, .005, 8.7, V(.69, .65, .56))
room('LIVING', 2.3, .4, 1, 0)
block(2.5, .3, .4, 3.7, .025, 2.8, V(.64, .61, .48))
# Sofa and chaise, cushions, coffee table, media console and television.
block(2.7, .62, -.65, 2.8, .6, .9, V(.75, .72, .61))
block(2.7, 1.08, -1.02, 2.8, .75, .2, V(.69, .66, .55))
for x in (1.4, 4):
    block(x, .88, -.62, .22, .6, 1.05, V(.69, .66, .55))
for x in (1.85, 2.7, 3.55):
    block(x, .96, -.55, .77, .15, .65, V(.85, .81, .69))
    block(x, 1.23, -.82, .42, .38, .16, CLAY)
block(3.55, .63, .25, .95, .58, 1.05, V(.75, .72, .61))
table(2.15, .3, .65, 1.25, .68, .4)
block(2.1, .76, .65, .37, .04, .26, CREAM)
table(2.4, .28, 2.48, 2.6, .38, .45)
block(2.4, 1.28, 2.55, 1.75, 1, .08, BLACK)
block(2.4, 1.28, 2.495, 1.62, .88, .015, V(.17, .28, .31))
plant(4.35, .28, 1.6)
# Dining room.
room('DINING', -2.6, .4, -.6, 0)
table(-2.6, .28, -1.25, 2.1, 1.1)
for x in (-3.3, -2.6, -1.9):
    chair(x, .28, -.28, 1)
    chair(x, .28, -2.22, -1)
    for z in (-.95, -1.55):
        keep(cylinder(pos=V(x, 1.1, z), axis=V(0, .018, 0), radius=.16, color=WHITE))
plant(-2.6, 1.1, -1.25, .45)
# Fitted kitchen with cabinets, hob, oven, sink, refrigerator and island.
room('KITCHEN', -2.7, .4, -4.3, 0)
for x in (-4.2, -3.3, -2.4, -1.5):
    block(x, .75, -5.35, .86, .94, .68, WOOD)
    block(x, 1.25, -5.32, .9, .09, .78, WHITE)
    block(x, 2.25, -5.6, .86, .75, .36, CREAM)
    rod((x-.18, .95, -4.99), (x+.18, .95, -4.99), .025)
block(-4.2, 1.31, -5.3, .68, .03, .5, BLACK)
for x in (-4.38, -4.03):
    for z in (-5.15, -5.45):
        keep(cylinder(pos=V(x, 1.34, z), axis=V(0, .015, 0), radius=.115, color=STONE))
block(-4.2, .75, -4.99, .68, .5, .03, BLACK)
block(-2.4, 1.31, -5.3, .62, .025, .45, STONE)
block(-2.4, 1.33, -5.3, .48, .015, .33, GLASS)
rod((-2.4, 1.3, -5.55), (-2.4, 1.68, -5.55), .025, STONE)
rod((-2.4, 1.68, -5.55), (-2.4, 1.68, -5.3), .025, STONE)
block(-.55, 1.35, -5.35, .8, 2.15, .75, STONE)
block(-.55, 1.72, -4.96, .77, .025, .025, BLACK)
rod((-.28, .75, -4.94), (-.28, 1.45, -4.94), .025)
block(-2.6, .78, -3.55, 1.9, 1, .75, WOOD)
block(-2.6, 1.32, -3.55, 2.05, .08, .9, WHITE)


def bathroom(x, y, z, floor):
    room('BATH', x, y+.15, z, floor)
    block(x, y, z, 2.2, .04, 2.1, V(.63, .72, .7))
    block(x-.65, y+.42, z-.55, .65, .8, .5, WOOD)
    keep(ellipsoid(pos=V(x-.65, y+.87, z-.55), size=V(.64, .15, .45), color=WHITE))
    block(x-.65, y+1.5, z-.91, .65, .85, .025, V(.64, .82, .86))
    rod((x-.65, y+.85, z-.8), (x-.65, y+1.08, z-.8), .025, STONE)
    block(x+.63, y+.47, z-.65, .48, .9, .2, WHITE)
    keep(ellipsoid(pos=V(x+.63, y+.37, z-.27), size=V(.52, .45, .7), color=WHITE))
    block(x-.55, y+.05, z+.55, .9, .12, .85, WHITE)
    block(x-.04, y+1.05, z+.55, .025, 2, .9, GLASS, opacity=.25)
    rod((x-.9, y+.25, z+.8), (x-.9, y+1.95, z+.8), .025, STONE)
    rod((x-.9, y+1.95, z+.8), (x-.6, y+1.95, z+.8), .035, STONE)


bathroom(3.65, .3, -4.7, 0)
# Laundry and stair flight; floor opening above the flight.
block(1.65, .75, -5.35, .75, .92, .7, WHITE)
keep(cylinder(pos=V(1.65, .75, -4.98), axis=V(0, 0, .04), radius=.27, color=BLACK))
for i in range(16):
    h = (i+1)*3.25/16
    z = 1.85-i*.29
    block(-.55, .28+h/2, z, 1.05, h, .29, WOOD)
    rod((.02, .28+h, z), (.02, 1.14+h, z), .018)
rod((.02, 1.34, 1.85), (.02, 4.39, -2.5), .035)

# Upper floor with an open stairwell.
group = 'upper'
block(-2.95, 3.5, -1.5, 4.1, .18, 9, CREAM)
block(2.4, 3.5, -1.5, 5.2, .18, 9, CREAM)
block(-.55, 3.5, -4.4, 1.1, .18, 3.2, CREAM)
block(-.55, 3.5, 2.7, 1.1, .18, .6, CREAM)


def bedroom(x, z, name, accent):
    y = 3.61
    room(name, x, y+.1, z+1.2, 1)
    block(x, y+.02, z, 3.1, .025, 3.2, V(.67, .63, .51))
    block(x, y+.28, z, 1.85, .45, 2.2, WOOD)
    block(x, y+.58, z, 1.8, .3, 2.1, WHITE)
    block(x, y+.76, z+.37, 1.83, .08, 1.35, accent)
    block(x, y+.72, z-1.05, 1.95, 1.2, .12, WOOD)
    for dx in (-.46, .46):
        block(x+dx, y+.81, z-.72, .68, .16, .43, CREAM)
    for dx in (-1.3, 1.3):
        table(x+dx, y, z-.7, .52, .5, .52)
        rod((x+dx, y+.6, z-.7), (x+dx, y+.95, z-.7), .025)
        keep(cone(pos=V(x+dx, y+.87, z-.7), axis=V(0, .3, 0), radius=.2, color=CREAM))
    block(x, y+1.15, z-2.05, 2.6, 2.3, .55, WOOD)
    for dx in (-.85, 0, .85):
        block(x+dx, y+1.15, z-1.76, .025, 2.2, .025, BLACK)
        rod((x+dx+.25, y+1, z-1.74), (x+dx+.25, y+1.35, z-1.74), .02)


bedroom(-2.85, .35, 'BEDROOM 2', V(.36, .5, .52))
bedroom(2.6, .35, 'PRIMARY BEDROOM', V(.63, .38, .27))
bathroom(3.65, 3.61, -4.7, 1)
room('STUDY', -2.9, 3.7, -4.4, 1)
table(-3, 3.61, -5.3, 2.5, .7)
chair(-3, 3.61, -4.55)
block(-3, 4.7, -5.35, .85, .55, .055, BLACK)
block(-3, 4.41, -5.12, .65, .025, .22, BLACK)
for shelf_y in (4, 4.65, 5.3, 5.95):
    block(-4.6, shelf_y, -4.7, .42, .07, 1.6, WOOD)
    for j in range(6):
        block(-4.6, shelf_y+.23, -5.3+j*.22, .32, .4, .13,
              (CLAY, CREAM, GREEN)[j % 3])
plant(-1.6, 3.61, -5.3)

# Shell walls and partitions are independently hidden for the cutaways.
for level in (0, 1):
    group = 'shell0' if level == 0 else 'shell1'
    base = .28+level*3.3
    for x in (-4.9, 4.9):
        block(x, base+1.5, -1.5, .18, 3, 9, CREAM)
    block(0, base+1.5, -5.9, 9.8, 3, .18, CREAM)
    # Rear bathroom enclosure with doorway; bedroom divider has landing access.
    block(2.35, base+1.45, -4.7, .12, 2.9, 2.4, CREAM)
    block(4.2, base+1.45, -3.5, 1.4, 2.9, .12, CREAM)
    block(2.65, base+1.45, -3.5, .6, 2.9, .12, CREAM)
    if level:
        for x in (-1.05, .7):
            block(x, base+1.45, .1, .12, 2.9, 5.4, CREAM)
        block(-2.95, base+1.45, -2.6, 2.2, 2.9, .12, CREAM)
        # Terracotta siding surrounds the left window.
        block(-2.5, 4.05, 3, 4.8, 1, .16, CLAY)
        block(-2.5, 6.18, 3, 4.8, .95, .16, CLAY)
        for x in (-4.4, -.65):
            block(x, 5.17, 3, 1, 1.3, .16, CLAY)
        window(-2.55, 5.17, 3.02, 2.8, 1.25)
        for y in (3.7, 3.95, 4.2, 4.45, 5.85, 6.1, 6.35):
            block(-2.5, y, 3.095, 4.7, .012, .015, WOOD)
        block(.4, 5.1, 3.15, .7, 3.1, .3, CREAM)
        block(2.8, 4.08, 3.25, 4.1, 1.05, .2, CLAY)
        block(2.8, 6.3, 3.25, 4.1, .4, .2, CREAM)
        window(2.8, 5.35, 3.27, 4.05, 1.55)
        # Curtains behind glazing.
        for x in (1, 1.18, 4.35, 4.53):
            block(x, 5.35, 3.05, .16, 1.5, .06, V(.68, .60, .46))
    else:
        for x in (-4.65, -.1, 4.65):
            block(x, 1.85, 2.9, .35, 3.15, .4, CREAM)
        window(2.35, 1.65, 2.8, 4.2, 2.65)
        block(-2.4, 1.65, 1.9, 4.1, 2.65, .12, WOOD)
        window(-2.9, 1.7, 2, 1.6, 1.7)
        block(-1.15, 1.5, 2, .95, 2.4, .12, WOOD)
        ball(-.82, 1.45, 2.09, .045, STONE)
    block(0, base+3.05, 3, 10.5, .2, 1.1, CREAM)

group = 'roof'
# Clerestory screen and two gently sloping roof planes.
block(2.1, 6.94, -.9, 5.7, .15, 8.9, CREAM)
for i in range(13):
    y = 6.7+i*.085
    block(2.1, y, 3.15, 5.6, .044, .08, BLACK)
    block(-.7, y, -.9, .08, .044, 8.1, BLACK)
for x in (-.7, .7, 2.1, 3.5, 4.9):
    block(x, 7.22, 3.15, .055, 1.15, .07, BLACK)
for x, y, width in ((-2.8, 7.03, 5.3), (2.1, 7.96, 6.6)):
    slab = block(x, y, -1, width, .22, 10.5, CREAM)
    slab.rotate(angle=-.035, axis=V(1, 0, 0))
    soffit = block(x, y-.14, -1, width-.15, .045, 10.3, WOOD)
    soffit.rotate(angle=-.035, axis=V(1, 0, 0))
    for lx in (x-width*.3, x+width*.3):
        lamp(lx, y-.17, 3.4)

group = 'shell0'
for x in (-4.4, -3.7, -3, -2.3, -1.6, -.9):
    block(x, 3.3, 3.3, .12, .18, 1.4, WOOD)
group = 'ground'
chair(-3.8, .28, 2.8)
chair(-2.4, .28, 2.8)
table(-3.1, .28, 3.1, .6, .6, .48)
for x in (-4.5, 4.5):
    plant(x, .28, 3.3, 1.3)
for x in (-3, 1, 4):
    lamp(x, 3.25, 2.85)
    lamps.append(local_light(pos=V(x, 2.95, 1.5), color=V(.16, .12, .06)))

# Fence and animated sliding gate.
group = 'site'
for x in (-7.2, -3.3, .1, 3.7, 7.2):
    block(x, 1.1, 5.8, .38, 2.2, .42, CREAM)
    block(x, 1.8, 6.03, .12, .2, .07, BLACK)
    lamp(x, 1.7, 6.09)


def fence(a, b, sliding=False):
    start = len(groups['site'])
    for y in (.35, 1.85):
        block((a+b)/2, y, 5.8, b-a, .065, .065, BLACK)
    count = int((b-a)/.17)
    for i in range(count+1):
        x = a+(b-a)*i/count
        rod((x, .3, 5.8), (x, 2, 5.8), .018)
        rod((x-.06, 1.97, 5.8), (x, 2.08, 5.8), .012)
        rod((x, 2.08, 5.8), (x+.06, 1.97, 5.8), .012)
    if sliding:
        gate_parts.extend((obj, V(obj.pos.x, obj.pos.y, obj.pos.z))
                          for obj in groups['site'][start:])


fence(-7, -3.5)
fence(-3.1, -.1)
fence(.3, 3.5, True)
fence(3.9, 7)
for x in (-6.6, -5.7, -4.8, -3.9, 4.4, 5.3, 6.2, 7.1):
    plant(x, .05, 6.15, .8)
for x in (-6.7, 6.6):
    for z in (-5, -3.4, -1.8, -.2, 1.4, 3):
        for j in range(3):
            ball(x+rng.uniform(-.3, .3), .7+rng.uniform(0, .4), z+j*.25,
                 .48, V(.23+rng.random()*.12, .39+rng.random()*.15, .08))


def palm(x, z, height):
    rod((x, 0, z), (x+.4, height, z), .16, V(.43, .35, .21))
    top = V(x+.4, height, z)
    for i in range(10):
        a = i*2*pi/10
        pts = [top+V(cos(a)*t*3, sin(t*pi)*1.2-t*.8, sin(a)*t*3)
               for t in (0, .2, .4, .6, .8, 1)]
        keep(curve(pos=pts, radius=.035, color=GREEN))
        for j in range(1, 6):
            t = j/6
            p = top+V(cos(a)*t*3, sin(t*pi)*1.2-t*.8, sin(a)*t*3)
            for side in (-1, 1):
                tip = p+V(-sin(a)*side*.65, -.25, cos(a)*side*.65)
                rod((p.x, p.y, p.z), (tip.x, tip.y, tip.z), .04*(1-t)+.012, GREEN)
    for dx in (-.15, .15):
        ball(x+.4+dx, height-.12, z, .17, WOOD)


palm(7.5, -.5, 7)
palm(-6.5, -4, 8)
palm(7.2, -6.5, 6)

view = 'Exterior'
show_labels = False
gate_open, gate_offset = False, 0.0


def refresh():
    visible = {'site', 'ground', 'upper', 'shell0', 'shell1', 'roof'}
    if view == 'Ground floor':
        visible = {'site', 'ground'}
    elif view == 'Upper floor':
        visible = {'site', 'ground', 'upper'}
    for name, objects in groups.items():
        for obj in objects:
            obj.visible = name in visible
    for obj, floor in room_labels:
        obj.visible = show_labels and ((floor == 0 and view == 'Ground floor') or
                                      (floor == 1 and view == 'Upper floor'))


def change_view(evt):
    global view
    view = evt.selected
    refresh()
    if view == 'Exterior':
        scene.center, scene.forward, scene.range = V(0, 3, 0), V(-.22, -.15, -1), 11
    else:
        scene.center = V(0, 1 if view == 'Ground floor' else 4, -1.5)
        scene.forward, scene.range = V(-.12, -1, -.65), 7.8


def toggle_labels(evt):
    global show_labels
    show_labels = evt.checked
    refresh()


def toggle_gate(evt):
    global gate_open
    gate_open = not gate_open
    evt.text = 'Close gate' if gate_open else 'Open gate'


def night(evt):
    scene.background = V(.035, .055, .10) if evt.checked else V(.58, .78, .94)
    scene.ambient = V(.22, .23, .28) if evt.checked else V(.48, .48, .46)
    for light in lamps:
        light.color = V(.8, .55, .28) if evt.checked else V(.16, .12, .06)


scene.append_to_caption('\nVIEW  ')
menu(choices=['Exterior', 'Ground floor', 'Upper floor'], bind=change_view)
scene.append_to_caption('    ')
button(text='Open gate', bind=toggle_gate)
scene.append_to_caption('    ')
checkbox(text='Night lighting', bind=night)
scene.append_to_caption('    ')
checkbox(text='Room labels', bind=toggle_labels)
scene.append_to_caption('\n\nRight-drag: orbit  |  Scroll: zoom  |  Shift-drag: pan\n'
                        'Select a floor to remove the roof and walls and explore the furniture.\n')
scene.center, scene.forward, scene.range = V(0, 3, 0), V(-.22, -.15, -1), 11
while True:
    rate(30)
    target = 3.35 if gate_open else 0
    if abs(target-gate_offset) > .005:
        gate_offset += max(-.055, min(.055, target-gate_offset))
        for obj, original in gate_parts:
            obj.pos = original+V(gate_offset, 0, 0)
