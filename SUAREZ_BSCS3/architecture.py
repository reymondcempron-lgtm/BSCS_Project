"""SUAREZ home exterior, rooms and furnishings (all genuine VPython objects)."""
from math import pi, atan
from vpython import vec, sphere, ring, cylinder, cone, box, curve, vertex, triangle
from objects import (cube, column, beam, lamp, glass_panel, window_front,
    window_side, plant_pot, physical_sign, PLASTER, IVORY, LIMESTONE,
    CONCRETE, CHARCOAL, GRAPHITE, WALNUT, OAK, LILAC, MAUVE, ROSE,
    DUSTY_PINK, LINEN, GREEN, GLASS, GOLD, WATER)


def wall_x(a,b,z,*,y0=.42,y1=4.45,color=PLASTER):
    return cube((a+b)/2,(y0+y1)/2,z,b-a,y1-y0,.22,color,
                surface='stucco',shine=.19)


def wall_z(x,a,b,*,y0=.42,y1=4.45,color=PLASTER):
    return cube(x,(y0+y1)/2,(a+b)/2,.22,y1-y0,b-a,color,
                surface='stucco',shine=.19)


def window_gap_x(a,b,z, low=1.14,high=3.43):
    wall_x(a,b,z,y0=.42,y1=low)
    wall_x(a,b,z,y0=high,y1=4.45)
    window_front(a+.06,b-.06,z+.12,bottom=low,top=high)


def window_gap_z(x,a,b,low=1.12,high=3.45):
    wall_z(x,a,b,y0=.42,y1=low)
    wall_z(x,a,b,y0=high,y1=4.45)
    window_side(x+(.12 if x>0 else -.12),a+.06,b-.06,low,high)


def door_frame(x,z,w=1.8,back=False):
    # Dark timber jamb with open doorway.
    for xx in (x-w/2,x+w/2):
        cube(xx,2.02,z,.10,3.22,.20,WALNUT,surface='wood')
    cube(x,3.62,z,w,.13,.22,WALNUT,surface='wood')
    # Side-swing open door leaf outside of walking path.
    leaf=cube(x+w/2+.42,1.99,z+(-.20 if back else .23),
              .91,2.98,.075,WALNUT,surface='wood')
    leaf.rotate(angle=.56 if back else -.55,axis=vec(0,1,0),origin=leaf.pos)
    sphere(pos=leaf.pos+vec(.24,0,.07),radius=.065,color=GOLD)


def front_shell():
    roof=[]
    # Thick foundations, tiled entry path and real textured warm timber flooring.
    cube(0,.14,0,22.65,.44,16.65,LIMESTONE,surface='granite')
    cube(0,.405,0,21.76,.088,15.78,IVORY,surface='wood',shine=.21)
    # Flooring zones in approximately natural materials.
    cube(-6.65,.465,3.25,8.25,.018,8.7,vec(.84,.66,.78),surface='wood')
    cube(-6.70,.465,-4.5,8.0,.018,6.5,vec(.91,.76,.85),surface='wood')
    cube(0,.466,-4.4,5.3,.016,6.6,vec(.94,.87,.96),surface='marble')
    cube(6.8,.466,3.35,8.0,.018,8.7,vec(.90,.80,.91),surface='granite')
    cube(6.85,.465,-4.5,8.0,.018,6.5,vec(.89,.72,.84),surface='wood')

    # Front elevation: real openings (not painted window rectangles).
    wall_x(-11,-9.45,8)
    window_gap_x(-9.45,-4.25,8)
    wall_x(-4.25,-1.32,8)
    wall_x(1.32,4.25,8)
    window_gap_x(4.25,9.45,8)
    wall_x(9.45,11,8)
    wall_x(-1.32,1.32,8,y0=3.62,y1=4.45)
    door_frame(0,8,2.55)

    # Rear facade: direct opening to the observatory, plus picture windows.
    wall_x(-11,-8.55,-8)
    wall_x(-6.60,4.45,-8)
    window_gap_x(4.45,9.22,-8,1.15,3.43)
    wall_x(9.22,11,-8)
    wall_x(-8.55,-6.60,-8,y0=3.58,y1=4.45)
    door_frame(-7.55,-8,1.90,back=True)

    # Side facade banding and actual window apertures.
    for x in (-11,11):
        wall_z(x,-8,-5.5)
        window_gap_z(x,-5.5,-2.45)
        wall_z(x,-2.45,1.20)
        window_gap_z(x,1.20,5.75)
        wall_z(x,5.75,8)
        cube(x,4.33,0,.31,.20,16.4,GRAPHITE)
    cube(0,4.36,8.1,22.4,.17,.39,GRAPHITE)
    cube(0,4.36,-8.1,22.4,.17,.39,GRAPHITE)

    # Interior room walls. Door-sized gaps are kept clear for exploration.
    for a,b in [(-10.87,-4.85),(-3.32,-1.50),(.02,4.03),(5.66,10.87)]:
        wall_x(a,b,-1.16,y0=.48,y1=4.23,color=vec(.91,.81,.95))
    for a,b in [(-4.85,-3.32),(-1.50,.02),(4.03,5.66)]:
        wall_x(a,b,-1.16,y0=3.56,y1=4.23,color=vec(.91,.81,.95))
    wall_z(-2.73,-7.88,-1.19,color=vec(.88,.78,.93))
    wall_z(2.73,-7.88,-1.19,color=vec(.88,.78,.93))
    # Bedroom wall with mauve accent behind headboard.
    cube(-6.65,2.31,-7.75,7.9,3.58,.045,
         vec(.61,.40,.79),surface='stucco',shine=.10)
    # Guest-study back has deep warm timber paneling.
    cube(6.85,2.26,-7.76,7.9,3.46,.045,
         vec(.74,.50,.70),surface='wood',shine=.21)

    # REDESIGNED ROOF — shallow double-pitched contemporary purple gable.
    # Two rotated VPython boxes form actual sloping roof planes, rather
    # than a huge flat slab. The fascia and ridge are separate details.
    for side in (-1,1):
        slope = -side*.135
        pane=cube(side*5.98,5.35,0,12.10,.26,18.45,CHARCOAL,
                  surface='metal',shine=.39)
        pane.rotate(angle=slope,axis=vec(0,0,1),origin=pane.pos)
        roof.append(pane)
        fascia=cube(side*5.92,5.15,9.27,12.15,.18,.13,ROSE,shine=.45)
        fascia.rotate(angle=slope,axis=vec(0,0,1),origin=fascia.pos)
        roof.append(fascia)
        cube(side*11.71,4.53,0,.18,.28,18.83,MAUVE)
    roof.append(cube(0,6.15,0,.33,.20,18.75,DUSTY_PINK,shine=.42))
    # Gable infill in lilac render. Both faces are visible from outdoors.
    for z, direction in ((8.03,1),(-8.03,-1)):
        points=[vec(-11.15,4.44,z),vec(11.15,4.44,z),vec(0,6.10,z)]
        if direction<0: points.reverse()
        triangle(vs=[vertex(pos=p,color=PLASTER) for p in points])
        cube(0,4.41,z,22.3,.12,.17,ROSE)

    # Bold architectural feature panels frame the main entrance, giving
    # the front facade a distinct purple / pink luxury-home identity.
    for side in (-1,1):
        cube(side*3.16,2.43,8.18,.53,3.64,.20,MAUVE,shine=.23)
        cube(side*3.57,2.45,8.25,.105,3.60,.14,GOLD,shine=.67)
    cube(0,3.84,8.22,2.90,.18,.15,ROSE)
    for x in (-10.68,10.68):
        cube(x,2.44,8.18,.30,3.95,.16,DUSTY_PINK,shine=.22)
    # Pink floor trim reads clearly through the wide panoramic windows.
    cube(0,.62,7.93,22.2,.16,.14,ROSE)

    # Open covered entry porch and steps at the front.
    cube(0,.32,9.44,6.3,.22,2.78,DUSTY_PINK,surface='granite')
    cube(0,.21,11.18,5.6,.21,.65,LIMESTONE,surface='granite')
    cube(0,.115,11.78,5.1,.19,.65,LIMESTONE,surface='granite')
    for xx in (-2.82,2.82):
        column(xx,.43,10.72,.115,3.95,MAUVE)
        cube(xx,4.3,10.72,.38,.11,.38,OAK,surface='wood')
    cube(0,4.49,10.36,6.5,.19,4.65,MAUVE,surface='wood')
    cube(0,4.65,10.36,6.70,.11,4.85,DUSTY_PINK,surface='metal')
    lamp(0,4.30,9.8,.70)
    for x in (-2.15,2.15):
        plant_pot(x,9.58,size=.95)
    return roof


def sofa(x,z):
    # 2.8m tufted couch with cushioned back, arms, metal feet and toss pillows.
    for sx in (x-1.3,x+1.3):
        for sz in (z-.64,z+.60):
            column(sx,.49,sz,.056,.24,GRAPHITE)
    cube(x,.83,z,3.30,.54,1.66,LINEN,shine=.15)
    cube(x,1.25,z-.72,3.31,.88,.29,LILAC,shine=.14)
    for sx in (x-1.55,x+1.55):
        cube(sx,1.13,z,.24,.65,1.74,LILAC,shine=.14)
    for sx in (x-.91,x+.08,x+.98):
        cube(sx,1.10,z+.25,.94,.13,1.02,LINEN,shine=.12)
    for sx, tint in ((x-.93,LILAC),(x+1.04,DUSTY_PINK)):
        cube(sx,1.44,z-.38,.51,.42,.18,tint,shine=.10)


def wooden_table(x,y,z,sx,sz):
    cube(x,y,z,sx,.16,sz,WALNUT,surface='wood')
    for dx in (-sx*.41,sx*.41):
        for dz in (-sz*.36,sz*.36):
            column(x+dx,.48,z+dz,.056,y-.56,GRAPHITE)


def chair(x,z,angle=0):
    # Chair faces down the negative z direction, rotate around its center.
    group=[]
    group.append(cube(x,.91,z,.76,.16,.73,OAK,surface='wood'))
    group.append(cube(x,1.38,z-.30,.76,.88,.13,
                      vec(.65,.47,.40),surface='wood'))
    for dx in (-.29,.29):
        for dz in (-.28,.28):
            group.append(column(x+dx,.48,z+dz,.046,.46,GRAPHITE))
    if angle:
        for obj in group:
            obj.rotate(angle=angle,axis=vec(0,1,0),origin=vec(x,0,z))


def pendant(x,z,y=3.75):
    column(x,y,z,.018,.45,GRAPHITE)
    cone(pos=vec(x,y-.05,z),axis=vec(0,-.36,0),radius=.34,
         color=GRAPHITE,shininess=.25)
    lamp(x,y-.39,z,.7)


def furniture():
    # LIVING ROOM (front left)
    cube(-6.45,.48,3.8,6.8,.018,4.5,DUSTY_PINK,shine=.08)
    sofa(-6.9,5.13)
    wooden_table(-6.85,.92,2.84,2.25,1.15)
    cube(-6.84,1.01,2.8,.70,.025,.44,IVORY,surface='marble')
    cube(-6.85,1.05,2.95,.35,.08,.25,ROSE)
    # TV screen on the far wall and credenza.
    cube(-6.75,2.08,-.88,3.6,1.88,.09,CHARCOAL,shine=.77)
    cube(-6.75,2.10,-.81,3.25,1.54,.011,vec(.12,.18,.21),shine=.85)
    cube(-6.75,.85,-.81,4.35,.52,.52,WALNUT,surface='wood')
    for x in (-8.60,-4.86):
        plant_pot(x,1.25,size=1.15)
    column(-10.0,.48,6.78,.045,2.12,GRAPHITE)
    cone(pos=vec(-10,2.60,6.78),axis=vec(0,.52,0),radius=.30,color=LINEN)
    lamp(-10,2.65,6.78,.65)
    # Neutral wall art, narrow frames and picture slats.
    cube(-10.7,2.37,3.15,.08,1.55,2.25,GRAPHITE)
    cube(-10.63,2.37,3.15,.06,1.36,2.03,vec(.76,.65,.61))
    for z in (2.75,3.16,3.57):
        cube(-10.58,2.35,z,.02,.72,.12,LILAC)

    # KITCHEN (front right) - cabinets, overhead cabinets, backsplash and appliances.
    cube(9.85,1.01,2.40,1.55,1.10,6.4,vec(.58,.52,.50),surface='wood')
    cube(9.85,1.61,2.40,1.85,.11,6.5,vec(.73,.72,.69),surface='marble')
    cube(7.05,1.01,.18,5.6,1.10,1.36,vec(.58,.52,.50),surface='wood')
    cube(7.05,1.61,.18,5.78,.12,1.55,IVORY,surface='marble')
    cube(7.1,2.17,-.70,5.5,1.07,.06,vec(.78,.77,.74),surface='marble')
    for x in (5.02,6.26,7.5,8.74):
        cube(x,3.12,.09,1.14,.91,.66,vec(.77,.72,.68),surface='wood')
        cube(x,2.99,.48,.13,.035,.05,GOLD)
    cube(9.84,2.90,3.9,1.41,1.02,1.72,vec(.70,.67,.64),surface='metal')
    # Oven front + four burners.
    cube(7.85,1.02,.91,1.44,.82,.07,CHARCOAL)
    cube(7.85,1.01,.96,1.17,.57,.035,DARK_GREY:=vec(.22,.25,.26),opacity=.65)
    for x in (7.42,8.31):
        for z in (-.15,.30):
            ring(pos=vec(x,1.692,z),axis=vec(0,1,0),
                 radius=.17,thickness=.021,color=GRAPHITE)
    # Sink & tap.
    cube(5.55,1.70,.16,.96,.018,.63,vec(.44,.48,.49),shine=.85)
    column(5.38,1.71,-.17,.055,.34,GRAPHITE)
    beam((5.38,2.05,-.17),(5.59,2.05,-.17),.041,GRAPHITE)
    # Fridge and kitchen island with two stools.
    cube(10.0,1.86,6.73,1.39,2.75,1.32,
         vec(.61,.64,.64),surface='metal',shine=.70)
    cube(10.0,2.30,7.41,.90,.045,.08,GRAPHITE)
    cube(5.64,1.03,4.55,2.65,1.14,1.33,
         vec(.68,.63,.61),surface='wood')
    cube(5.64,1.66,4.55,2.96,.12,1.53,IVORY,surface='marble')
    for xx in (5.10,6.19):
        column(xx,.47,5.67,.09,.70,GRAPHITE)
        cube(xx,1.13,5.67,.49,.13,.52,WALNUT,surface='wood')
    pendant(5.64,4.35)
    pendant(8.33,4.35)

    # DINING (center front), with upholstered chairs and table place settings.
    wooden_table(.0,1.18,3.8,2.72,1.56)
    for z in (2.55,5.12):
        for x in (-.8,.8):
            chair(x,z,0 if z>3.8 else pi)
    for xx in (-.75,.75):
        cylinder(pos=vec(xx,1.27,3.8),axis=vec(0,.018,0),
                 radius=.25,color=IVORY)
    cylinder(pos=vec(0,1.29,3.8),axis=vec(0,.36,0),
             radius=.09,color=vec(.59,.69,.59),opacity=.6)
    sphere(pos=vec(0,1.75,3.8),radius=.15,color=DUSTY_PINK)
    pendant(0,3.8)
    cube(.30,.53,6.7,2.65,.024,.73,vec(.66,.61,.58))

    # BEDROOM (rear left): correctly proportioned king-size bed and nightstands.
    cube(-6.9,.49,-4.85,5.3,.019,4.45,DUSTY_PINK)
    cube(-6.76,.70,-5.35,3.20,.38,4.34,WALNUT,surface='wood')
    cube(-6.76,1.03,-5.38,3.04,.28,4.18,LINEN,shine=.10)
    cube(-6.76,1.21,-5.70,3.04,.18,3.38,
         LILAC,shine=.10)
    cube(-6.76,1.65,-7.50,3.52,1.28,.17,MAUVE,shine=.16)
    for x in (-7.50,-6.03):
        cube(x,1.31,-3.63,1.17,.23,.69,IVORY)
    for x in (-9.15,-4.35):
        cube(x,.83,-6.50,.68,.64,.70,OAK,surface='wood')
        column(x,1.16,-6.5,.04,.27,GOLD)
        sphere(pos=vec(x,1.49,-6.5),radius=.19,color=IVORY,emissive=True)
        lamp(x,1.62,-6.5,.45)
    cube(-10.48,2.05,-3.45,.38,3.10,2.47,WALNUT,surface='wood')
    cube(-10.22,2.07,-3.47,.06,2.77,1.02,vec(.73,.72,.68),opacity=.25)
    cube(-3.05,1.24,-4.5,.18,1.22,2.0,vec(.70,.67,.66))
    plant_pot(-9.75,-2.15,size=.85)

    # BATHROOM (rear center): terrazzo floor, shower, freestanding bath and mirror.
    cube(-.02,.480,-4.43,5.12,.016,6.50,IVORY,surface='stones')
    cube(-.81,.75,-6.18,2.66,.54,1.20,IVORY,shine=.87)
    cube(-.81,1.02,-6.18,2.32,.10,.87,vec(.67,.78,.79),opacity=.52)
    for xx in (-1.84,.23):
        column(xx,.49,-6.62,.075,.22,GRAPHITE)
    glass_panel(1.69,1.74,-5.92,.075,2.50,2.90)
    beam((1.61,3.32,-6.94),(1.61,3.32,-5.32),.028,GRAPHITE)
    cylinder(pos=vec(1.25,2.75,-6.85),axis=vec(0,-.20,0),
             radius=.27,color=GRAPHITE)
    cube(-1.88,1.11,-2.45,.98,.30,.72,
         vec(.66,.61,.58),surface='wood')
    cube(-1.88,1.35,-2.45,1.08,.12,.81,IVORY,surface='marble')
    cylinder(pos=vec(-1.88,1.44,-2.48),axis=vec(0,.13,0),
             radius=.25,color=IVORY)
    cube(-1.88,2.60,-1.39,.96,1.55,.055,
         vec(.60,.68,.71),opacity=.51,shine=.94)
    cube(.97,.80,-2.25,.62,.60,.80,IVORY)
    cube(.97,1.12,-2.55,.85,.14,.28,IVORY)
    cylinder(pos=vec(.97,1.18,-2.25),axis=vec(0,.08,0),
             radius=.24,color=IVORY)

    # STUDY / GUEST SUITE (rear right): walnut desk, laptop, shelf, chaise.
    wooden_table(6.65,1.18,-5.76,2.95,1.0)
    cube(6.7,1.70,-6.10,1.00,.70,.065,GRAPHITE)
    cube(6.70,1.70,-6.06,.88,.54,.012,
         vec(.21,.30,.38),emissive=True)
    cube(6.7,1.27,-5.25,.85,.025,.54,GRAPHITE)
    cube(6.55,.80,-4.22,.90,.58,.82,MAUVE)
    cube(6.55,1.25,-4.59,.9,.76,.16,MAUVE)
    for y in (1.32,2.28,3.17):
        cube(10.08,y,-4.35,1.10,.11,4.80,WALNUT,surface='wood')
    for z in (-6.4,-5.2,-3.9,-2.6):
        cube(10.08,1.72,z,.71,.74,.19,LILAC if z<-4 else IVORY)
    cube(4.34,.73,-4.70,1.95,.43,3.9,
         DUSTY_PINK,shine=.18)
    cube(4.24,1.17,-6.27,1.87,.88,.36,MAUVE)
    plant_pot(9.71,-1.95)

    # Warm ceiling downlights in rooms (subtle, non-emissive ceiling panels).
    for x,z in [(-7,4),(-4.4,2.0),(7,3),(-6.9,-4.3),(0,-4),(7,-4.4)]:
        cube(x,4.39,z,.46,.035,.46,GRAPHITE)
        lamp(x,4.26,z,.45)
