"""Landscaping, pool, outdoor lounge and the attached observatory tower."""
from math import cos, sin, pi
from random import Random
from vpython import vec, sphere, ring, cylinder, cone, curve, distant_light
from geometry import (TOWER_X, TOWER_Z, STAIR_RADIUS, STAIR_TURNS,
                      DECK_Y, stair)
from objects import (cube, column, beam, lamp, glass_panel, shrub, tree,
    flower, plant_pot, physical_sign, PLASTER, IVORY, LIMESTONE,
    CONCRETE, CHARCOAL, GRAPHITE, WALNUT, OAK, LILAC, MAUVE, ROSE,
    DUSTY_PINK, LINEN, GREEN, GLASS, GOLD, WATER)

rng = Random(2026)


def world_ground():
    # Broad green site and muted rolling garden edges.
    cube(0,-.36,0,74,.66,63,vec(.33,.50,.35),surface='gravel',shine=.08)
    cube(0,-.004,0,66,.07,54,vec(.33,.45,.30),shine=.06)
    # Public road, gate strip and footpath: fewer identical geometric shapes.
    cube(0,-.08,28.0,74,.08,6.2,vec(.36,.37,.38),surface='granite')
    cube(0,-.015,25.0,74,.10,.32,LIMESTONE,surface='granite')
    cube(0,.02,20.1,4.28,.12,15.3,
         vec(.77,.65,.82),surface='stones',shine=.11)
    for i in range(15):
        z=12.9+i*.90
        cube(0,.097,z,3.72,.055,.73,
             vec(.87+.025*(i%2),.73,.89),surface='granite')
    # Outdoor edging to soften hard-cornered modeling.
    for x in (-2.21,2.21):
        cube(x,.12,19.7,.12,.19,15.65,LIMESTONE,surface='granite')

    # Fence: concrete pillars + black slim vertical metal rails.
    for x in (-34,-28,-22,-16,-10,-4,4,10,16,22,28,34):
        cube(x,.99,27.25,.51,2.0,.52,LIMESTONE,surface='granite')
        cube(x,1.99,27.25,.66,.18,.67,GRAPHITE)
    for side in (-1,1):
        a,b=(-34,-4.0) if side<0 else (4.0,34)
        cube((a+b)/2,1.75,27.25,b-a,.06,.11,GRAPHITE)
        cube((a+b)/2,.73,27.25,b-a,.06,.11,GRAPHITE)
        x=a+.42
        while x<b:
            cube(x,1.22,27.25,.056,1.78,.09,GRAPHITE)
            x+=.47
    # A pair of front gates are swung back to allow walking through.
    for x0,sign in ((-2.02,-1),(2.02,1)):
        for d in (.37,1.11,1.85):
            column(x0+sign*d,.15,27.05,.038,1.74,GRAPHITE)
        cube(x0+sign*1.13,1.04,27.05,2.1,.054,.09,GRAPHITE)

    # Planting strips planted in irregular natural clusters.
    for side in (-1,1):
        cx=side*6.65
        cube(cx,.07,17.42,7.05,.14,11.0,
             vec(.30,.27,.23),surface='gravel',shine=.07)
        for j in range(15):
            x=cx+rng.uniform(-3.05,3.05)
            z=rng.uniform(12.4,22.0)
            hue=[ROSE,DUSTY_PINK,LILAC,IVORY,
                 MAUVE][j%5]
            flower(x,z,hue,size=rng.uniform(.8,1.35))
        for j in range(11):
            x=cx+rng.uniform(-3.1,3.1)
            z=rng.uniform(12.8,22.0)
            shrub(x,z,scale=rng.uniform(.48,.83))
    # Border hedges, ornamental garden trees, natural cast-shadow approximations.
    for x,z,s,b in [(-29,-16,1.23,False),(-31,8,1.15,True),
                     (-19,23,1.09,False),(30,17,1.17,True),
                     (29,-17,1.20,False),(7,-24,1.12,True),
                     (-25,-23,1.13,False)]:
        cylinder(pos=vec(x,-.005,z),axis=vec(0,.018,0),
                 radius=2.1*s,color=vec(.18,.29,.17),opacity=.18)
        tree(x,z,s,bloom=b)
    for x in (-17,-14.6,14,17,20,23,26):
        shrub(x,13.0,1.01)
    for z in (-23,-19,-15,-11):
        shrub(-22,z,.95)

    # Rose-and-lavender borders follow both sides of the front path.
    # Individual stems, leaves and petals make these read as a garden,
    # rather than a few isolated geometric balls.
    for side in (-1, 1):
        for j in range(14):
            z=12.65+j*.57
            x=side*(2.82 + .20*(j%3))
            tint=(ROSE, LILAC, DUSTY_PINK, MAUVE)[j%4]
            flower(x,z,tint,size=1.25 if j%3==0 else .98)
        for j in range(7):
            flower(side*(3.75+.31*(j%2)),13.0+j*1.15,
                   (ROSE,LILAC)[j%2],size=1.35)

    # Garden path to rear stargazing tower, visible beside the house.
    for i in range(6):
        z=-8.9-i*1.40
        cube(-7.55,.075,z,2.62,.12,1.19,
             vec(.85,.73,.89),surface='stones')
    # Path lights, understated and warm.
    for x in (-2.45,2.45):
        for z in (14.1,19.4,24.2):
            column(x,.08,z,.050,.56,CHARCOAL)
            cube(x,.68,z,.22,.18,.22,IVORY,emissive=True)
            lamp(x,.66,z,.25)


def pool_and_gazebo():
    # Pool 14 m x 12 m area on the right, with stone perimeter and turquoise water.
    cx,cz=21.0,-2.43
    cube(cx,.12,cz,17.25,.34,13.30,
         vec(.90,.75,.87),surface='stones',shine=.13)
    cube(cx,.30,cz,14.28,.12,10.52,vec(.40,.32,.66),surface='stones')
    cube(cx,.38,cz,13.47,.042,9.7,WATER,opacity=.85,shine=.98)
    for x in (14.08,27.92):
        cube(x,.43,cz,.40,.18,10.72,IVORY,surface='marble')
    for z in (-7.69,2.84):
        cube(cx,.43,z,14.2,.18,.35,IVORY,surface='marble')
    for x in (14.27,27.73):
        cube(x,.49,cz,.11,.06,10.65,ROSE,shine=.57)
    for z in (-7.64,2.80):
        cube(cx,.49,z,14.0,.06,.10,LILAC,shine=.57)
        # Underwater bands add depth rather than a flat blue rectangle.
    for x in (16.6,19.9,23.3,26.4):
        cube(x,.384,cz,.025,.01,9.10,
             vec(.94,.76,.96),opacity=.20,shine=.91)
    for z in (-5.6,-2.6,.45):
        cube(cx,.391,z,12.6,.012,.019,
             vec(.97,.87,.95),opacity=.16,shine=.92)
    # Rim / entry stair.
    for j in range(3):
        cube(15.9+j*.47,.44-j*.025,1.79,1.1,.065,1.0,
             vec(.86,.72,.88),surface='marble')
    # Pool ladder.
    for x in (26.35,27.14):
        beam((x,.48,1.75),(x,1.18,1.75),.035,GRAPHITE)
        beam((x,1.18,1.75),(x,1.18,1.05),.035,GRAPHITE)
    for y in (.53,.82):
        beam((26.35,y,1.60),(27.14,y,1.60),.030,GRAPHITE)
    # Two loungers with cushion, legs and pastel towels.
    for x in (17.7,21.9):
        cube(x,.50,5.36,2.45,.11,1.0,WALNUT,surface='wood')
        cube(x,.68,5.37,2.37,.17,.95,LINEN)
        back=cube(x-.89,.83,5.35,.96,.13,.95,IVORY)
        back.rotate(angle=-.48,axis=vec(0,0,1),origin=back.pos)
        for xx in (x-1.01,x+1.02):
            for z in (5.03,5.70):
                column(xx,.23,z,.045,.29,GRAPHITE)
    for x in (17.7,21.9):
        cube(x,.784,5.3,.55,.025,.85,LILAC if x<20 else DUSTY_PINK)
    cube(24.87,.63,5.11,.85,.06,.88,WALNUT,surface='wood')
    column(24.87,.22,5.11,.047,.41,GRAPHITE)

    # Pergola / gazebo behind the pool: slatted roof and an outdoor lounge.
    gx,gz=22.5,-13.9
    cube(gx,.12,gz,10.35,.27,7.40,LIMESTONE,surface='stones')
    for x in (18.12,26.88):
        for z in (-16.87,-10.92):
            column(x,.27,z,.14,3.28,GRAPHITE)
            cube(x,3.56,z,.35,.12,.35,GRAPHITE)
    for z in (-16.96,-10.85):
        cube(gx,3.58,z,9.50,.16,.24,WALNUT,surface='wood')
    for i in range(11):
        x=18.12+i*.87
        cube(x,3.72,gz,.18,.17,7.06,WALNUT,surface='wood')
    cube(21.0,.63,-14.9,4.2,.63,1.5,
         DUSTY_PINK,shine=.13)
    cube(21.0,1.06,-15.50,4.21,.72,.33,MAUVE)
    cube(21.0,.94,-13.62,2.48,.15,1.03,WALNUT,surface='wood')
    for x in (20.01,21.97):
        for z in (-13.95,-13.35):
            column(x,.26,z,.047,.63,GRAPHITE)
    for x in (18.5,26.4):
        plant_pot(x,-16.2,size=1.1)
    lamp(gx,3.34,gz,.65)


def observatory():
    """Connected three-storey-height tower; real staircase geometry and deck."""
    cx,cz=TOWER_X,TOWER_Z
    # Enclosed passage with warm plaster side walls and a roof.
    cube(cx,.18,-9.26,3.48,.28,3.30,LIMESTONE,surface='granite')
    for x in (cx-1.62,cx+1.62):
        cube(x,2.27,-9.28,.16,3.72,3.14,PLASTER,surface='stucco')
        cube(x,2.46,-9.30,.07,1.38,1.20,GLASS,opacity=.16)
    cube(cx,4.31,-9.28,3.52,.23,3.36,WALNUT,surface='wood')
    cube(cx,4.52,-9.30,3.60,.15,3.52,GRAPHITE,surface='metal')

    # Tall square steel frame with very light tinted glazing.
    cube(cx,.16,cz,5.50,.40,5.55,CONCRETE,surface='granite')
    for x in (cx-2.48,cx+2.48):
        for z in (cz-2.48,cz+2.48):
            column(x,.39,z,.115,12.78,GRAPHITE)
            cube(x,13.08,z,.34,.18,.34,CHARCOAL)
    # 1st floor/landing/tower glazing: front bottom is open at staircase entrance.
    for y in (3.95,7.84,12.42):
        cube(cx,y,cz+2.48,4.97,.12,.20,GRAPHITE)
        cube(cx,y,cz-2.48,4.97,.12,.20,GRAPHITE)
        for x in (cx-2.48,cx+2.48):
            cube(x,y,cz,.20,.12,4.97,GRAPHITE)
    for zz in (cz-2.47,cz+2.47):
        for xx in (cx-1.24,cx+1.24):
            for y in (5.9,9.8):
                glass_panel(xx,y,zz,2.28,3.53,.055,purple=True)
    for xx in (cx-2.48,cx+2.48):
        for zz in (cz-1.27,cz+1.27):
            for y in (5.88,9.82):
                glass_panel(xx,y,zz,.055,3.48,2.27,purple=True)
    # Ground front doorway physically open so it does not block walking.
    for x in (cx-2.48,cx+2.48):
        cube(x,2.24,cz+2.48,.20,3.61,.14,GRAPHITE)
    glass_panel(cx,2.25,cz-2.47,4.5,3.54,.05,purple=True)

    # Central spindle, 54 actual individual steps and helical silver handrail.
    column(cx,.40,cz,.11,10.4,GRAPHITE)
    t_count=54
    railpoints=[]
    for i in range(t_count+1):
        t=i/t_count
        x,y,z=stair(t)
        ang=pi/2+t*STAIR_TURNS*2*pi
        tread=cube(x,y,z,1.26,.13,.54,
                   OAK,surface='wood',shine=.21)
        tread.rotate(angle=-ang,axis=vec(0,1,0),origin=tread.pos)
        if i%3==0:
            ox,oz=cos(ang)*.36,sin(ang)*.36
            beam((x+ox,y,z+oz),(x+ox,y+.94,z+oz),.035,GRAPHITE)
        railpoints.append(vec(cx+(STAIR_RADIUS+.42)*cos(ang),
                              y+1.00,cz+(STAIR_RADIUS+.42)*sin(ang)))
    curve(pos=railpoints,radius=.039,color=LILAC)

    # Open viewing deck with modern timber floor and transparent perimeter.
    cube(cx,DECK_Y-.13,cz,4.74,.31,4.72,WALNUT,surface='wood')
    for x in (cx-2.35,cx+2.35):
        for z in (cz-2.35,cz+2.35):
            column(x,DECK_Y,z,.042,1.08,GRAPHITE)
    for x in (cx-2.35,cx+2.35):
        glass_panel(x,DECK_Y+.56,cz,.055,1.03,4.48,purple=True)
    for z in (cz-2.35,cz+2.35):
        glass_panel(cx,DECK_Y+.56,z,4.49,1.03,.055,purple=True)
        cube(cx,DECK_Y+1.11,z,4.72,.058,.075,GRAPHITE)
    for x in (cx-2.35,cx+2.35):
        cube(x,DECK_Y+1.11,cz,.075,.055,4.70,GRAPHITE)
    # Observatory roof with overhang (raised, not enclosed hemispherical dome).
    cube(cx,13.44,cz,5.70,.16,5.70,WALNUT,surface='wood')
    cube(cx,13.61,cz,5.91,.18,5.92,CHARCOAL,surface='metal')
    for x in (cx-2.36,cx+2.36):
        for z in (cz-2.36,cz+2.36):
            column(x,DECK_Y,z,.10,3.00,GRAPHITE)

    # Brass telescope that can actually be walked around.
    tx,tz=cx+.34,cz-.30
    column(tx,DECK_Y,tz,.095,1.28,GRAPHITE)
    sphere(pos=vec(tx,DECK_Y+1.29,tz),radius=.22,color=GOLD)
    # Smooth brass tube aiming toward the distant garden, skewed upward.
    tube=beam((tx-.62,DECK_Y+1.07,tz+.34),
              (tx+.85,DECK_Y+1.90,tz-1.01),.19,GOLD)
    ring(pos=vec(tx+.85,DECK_Y+1.90,tz-1.01),
         axis=vec(1,.56,-.9),radius=.23,thickness=.07,color=CHARCOAL)
    # Bench for stargazing.
    cube(cx-1.45,DECK_Y+.63,cz-1.30,1.25,.14,.55,OAK,surface='wood')
    for x in (cx-1.95,cx-.95):
        column(x,DECK_Y,cz-1.3,.046,.62,GRAPHITE)
    lamp(cx,13.28,cz,.65)
