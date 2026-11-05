"""Recognizable furniture assembled from a handful of reusable shapes."""
from . import config as C


def table(b,x,y,z,w=2.2,d=1.1):
    b.box((x,y+0.77,z),(w,0.12,d),'wood',True)
    for dx in (-w/2+0.12,w/2-0.12):
        for dz in (-d/2+0.12,d/2-0.12):
            b.box((x+dx,y+0.36,z+dz),(0.08,0.72,0.08),'charcoal')


def chair(b,x,y,z,back=1):
    b.box((x,y+0.46,z),(0.56,0.12,0.58),'sand',True)
    b.box((x,y+0.77,z+back*0.25),(0.56,0.55,0.08),'wood')
    for dx in (-0.22,0.22):
        for dz in (-0.22,0.22):
            b.box((x+dx,y+0.22,z+dz),(0.055,0.44,0.055),'wood')


def sofa(b,x,y,z,w=3):
    b.box((x,y+0.36,z),(w,0.52,1.05),'green',True)
    b.box((x,y+0.82,z+0.46),(w,0.8,0.23),'green')
    for dx in (-w/2+0.1,w/2-0.1):
        b.box((x+dx,y+0.65,z),(0.22,0.6,1.05),'green')
    for dx in (-w/3,0,w/3):
        b.box((x+dx,y+0.66,z-0.05),(w/3-0.07,0.17,0.8),'sand')
    for dx in (-w/3,w/3):
        b.ellipsoid((x+dx,y+0.96,z+0.23),(0.5,0.5,0.18),'cream')


def plant(b,x,y,z):
    b.box((x,y+0.25,z),(0.42,0.5,0.42),'sand',True)
    for dx,dz in ((0,0),(-0.2,0.1),(0.2,-0.1)):
        b.ellipsoid((x+dx,y+0.85,z+dz),(0.4,0.85,0.32),'leaf')


def bed(b,x,y,z):
    b.box((x,y+0.24,z),(2.25,0.48,2.6),'wood',True)
    b.box((x,y+0.58,z),(2.18,0.25,2.5),'white')
    b.box((x,y+0.74,z+0.4),(2.2,0.08,1.65),'green')
    b.box((x,y+0.65,z-1.3),(2.4,1.3,0.13),'wood')
    for dx in (-0.55,0.55):
        b.ellipsoid((x+dx,y+0.82,z-0.83),(0.85,0.17,0.5),'cream')
    for dx in (-1.65,1.65):
        b.box((x+dx,y+0.3,z-0.8),(0.65,0.6,0.7),'wood',True)
        b.rod((x+dx,y+0.6,z-0.8),(x+dx,y+1.0,z-0.8),0.035,'brass')
        b.ellipsoid((x+dx,y+1.03,z-0.8),(0.36,0.26,0.36),'cream')


def bathroom(b,x,y,z):
    # Vanity, basin, toilet and shower enclosure.
    b.box((x,y+0.43,z),(1.5,0.86,0.6),'wood',True)
    b.box((x,y+0.9,z),(1.6,0.1,0.7),'white')
    b.ellipsoid((x,y+0.95,z),(0.6,0.08,0.38),'stone')
    b.rod((x,y+0.96,z-0.23),(x,y+1.17,z-0.23),0.035)
    b.box((x,y+1.65,z-0.38),(1.4,0.8,0.03),'glass')
    b.ellipsoid((x-0.6,y+0.25,z+1.4),(0.6,0.5,0.8),'white')
    b.ellipsoid((x-0.6,y+0.48,z+1.4),(0.65,0.1,0.82),'cream')
    b.box((x-0.6,y+0.65,z+1.75),(0.6,0.7,0.22),'white',True)
    b.box((x+0.1,y+0.05,z+3),(2.4,0.1,1.6),'stone')
    b.box((x+1.25,y+1,z+3),(0.04,2,1.6),'glass',True,opacity=0.2)
    b.rod((x,y+0.6,z+3.65),(x,y+2.1,z+3.65),0.035)
    b.ellipsoid((x,y+2.1,z+3.5),(0.28,0.05,0.35),'charcoal')


def build(b):
    b.group='ground'
    # West front living, west rear guest bedroom and bath.
    b.box((-7,0.025,3),(7,0.035,5),'sand')
    sofa(b,-7,0,5)
    table(b,-7,0,2.7,2,1)
    b.box((-10.9,0.35,2),(0.6,0.7,3.2),'wood',True)
    b.box((-10.85,1.4,2),(0.08,1.2,2.1),'black')
    chair(b,-4,0,5.2)
    plant(b,-10.7,0,-2.5)
    bed(b,-5.2,0,10)
    b.box((-3.2,1.1,14.9),(1.4,2.2,0.7),'wood',True)
    bathroom(b,-10,0,10.7)
    # Open dining / kitchen zone on east side; route runs along x=4.
    table(b,7,0,0,3.2,1.3)
    for x in (6,7,8):
        chair(b,x,0,-1,-1); chair(b,x,0,1,1)
    for z in (8,10,12,14):
        b.box((11,0.48,z),(1.4,0.96,1.9),'wood',True)
        b.box((11,1,z),(1.5,0.08,2),'cream')
        b.box((11.4,2.25,z),(0.65,0.85,1.85),'ivory')
        b.box((10.99,2.25,z),(0.03,0.035,1.4),'brass')
    b.box((7.5,0.48,10),(2.8,0.96,1.5),'wood',True)
    b.box((7.5,1,10),(3,0.1,1.65),'cream')
    b.ellipsoid((11,1.06,10),(0.8,0.05,0.65),'stone')
    b.rod((11.4,1.04,10),(11.4,1.4,10),0.04)
    b.box((10.9,1.07,13),(1,0.04,1.2),'black')
    for x in (10.65,11.15):
        for z in (12.7,13.3):
            b.ellipsoid((x,1.1,z),(0.3,0.025,0.3),'stone')
    b.box((5,1.1,14.8),(1.2,2.2,0.9),'stone',True)
    b.box((4.7,1.2,14.3),(0.05,0.7,0.06),'charcoal')
    table(b,7,0,17.2,3,1)
    for x in (6,8):
        chair(b,x,0,18.1)
    b.group='upper'; y=C.FLOOR_HEIGHT
    bed(b,-7,y,-1)
    b.box((-10.8,y+1.1,4.5),(0.8,2.2,3.2),'wood',True)
    # Master ensuite in front-west corner of the suite's rear zone.
    b.wall('z',-8,3,7,y,C.FLOOR_HEIGHT,[(5,1.4,0,2.5,False)])
    b.wall('x',3,-12,-8,y,C.FLOOR_HEIGHT,[])
    bathroom(b,-10,y,3.5)
    # Front east room becomes an office/gallery beside the dining void.
    table(b,8,y,4.8,2.8,.85)
    chair(b,8,y,5.65)
    bed(b,8,y,10)
    for z in (5.8,14.8):
        b.box((10,y+1.1,z),(2.7,2.2,0.7),'wood',True)
    sofa(b,-5,y,14.4,3.5)
    table(b,-5,y,12.1)
    b.box((-5,y+1.5,7.2),(2,1.1,0.1),'black')
    bathroom(b,-10,y,10.7)
    for x in (-7.5,-3.5):
        chair(b,x,y,-5.5)
    table(b,-5.5,y,-6,1,0.6)
    # Decorative art and compact plants kept away from the circulation core.
    for level in (0,1):
        b.group='ground' if level==0 else 'upper'; y=level*C.FLOOR_HEIGHT
        for x,z in ((10.7,-2.5),(-3,8.2)):
            plant(b,x,y,z)
        b.box((-7,y+2.1,6.83),(1.8,0.9,0.04),'brass')
        b.box((-7,y+2.1,6.79),(1.6,0.7,0.03),'green')
    enrich(b)


def lamp(b,x,y,z):
    b.box((x,y+.025,z),(.3,.05,.3),'brass')
    b.rod((x,y,z),(x,y+.48,z),.025,'brass')
    b.ellipsoid((x,y+.48,z),(.42,.3,.42),'linen')
    b.ellipsoid((x,y+.35,z),(.18,.08,.18),'cream',emissive=True)


def pendant(b,x,z,ceiling,bottom,r=.35):
    b.rod((x,ceiling,z),(x,bottom,z),.018,'brass')
    b.ellipsoid((x,bottom,z),(r*2,.25,r*2),'brass')
    b.ellipsoid((x,bottom-.1,z),(r*1.7,.06,r*1.7),'cream',emissive=True)


def books(b,x,y,z,n=7):
    for i in range(n):
        b.box((x+i*.1,y+.14,z),(.075,.28+(i%3)*.035,.22),
              ('green','linen','terracotta','wood')[i%4])


def art(b,x,y,z,w=1.8):
    b.box((x,y,z),(w,1.15,.07),'wood')
    b.box((x,y,z-.05),(w-.12,1.03,.03),'linen')
    b.ellipsoid((x-.25,y+.12,z-.08),(.55,.65,.025),'terracotta')
    b.box((x+.3,y-.2,z-.1),(.5,.35,.025),'green')


def enrich(b):
    """Room compositions: fixtures, joinery, fabrics and inhabited details."""
    h=C.FLOOR_HEIGHT
    b.group='ground'
    # Living: layered rug, additional seating, slatted media wall and shelves.
    b.box((-7,.05,2.8),(6.4,.025,4.9),'linen')
    for z in (.7,4.9):
        b.box((-7,.067,z),(6,.012,.065),'wood')
    chair(b,-9.2,0,.2,-1)
    table(b,-4,0,3,.65,.65); lamp(b,-4,.84,3)
    for i in range(17):
        b.box((-11.65,1.7,.1+i*.25),(.08,2.9,.055),'wood')
    for z in (.5,3.6):
        b.box((-11.25,2.3,z),(.65,.08,1.2),'wood')
        plant(b,-11.2,2.35,z)
    books(b,-7.65,.84,2.7,4)
    b.ellipsoid((-6.5,.95,2.7),(.3,.23,.3),'terracotta')
    # Foyer console deliberately outside the central route.
    b.box((-1.65,.85,-2.5),(.45,.12,1.5),'wood',True)
    b.box((-1.87,1.9,-2.5),(.035,1.3,1.1),'brass')
    lamp(b,-1.6,.92,-2.8)
    pendant(b,0,-1.8,3.4,2.8,.55)
    # Dining salon: chandelier suspended through the actual upstairs opening.
    for x,z,drop in ((6,-.5,4.9),(7,0,4.4),(8,.5,5.2),(9,0,4.7),(10,-.5,5.5)):
        pendant(b,x,z,7.1,drop,.32)
    for x in (6,7,8):
        for z in (-.37,.37):
            b.ellipsoid((x,.86,z),(.34,.025,.34),'white')
            b.rod((x+.25,.86,z-.1),(x+.25,.86,z+.1),.012,'brass')
    b.ellipsoid((7,1,0),(.5,.3,.3),'terracotta')
    plant(b,11,0,4.8)
    # Kitchen island stools, pendants, oven, range hood and countertop objects.
    for x in (6.6,7.5,8.4):
        chair(b,x,0,8.65,-1)
        pendant(b,x,10,3.4,2.45,.22)
    b.box((10.23,.54,13),(.06,.58,.9),'black')
    b.box((10.17,.8,13),(.045,.035,.65),'brass')
    b.box((11,2.8,13),(1.4,.25,1.7),'charcoal')
    b.box((11,3.15,13),(.5,.5,.7),'charcoal')
    for z in (8.1,8.4,8.7):
        b.ellipsoid((10.9,1.2,z),(.18,.25,.18),'linen')
    b.box((7.7,1.08,10),(.65,.045,.4),'wood')
    for dx in (-.17,.04,.2):
        b.ellipsoid((7.7+dx,1.17,10),(.18,.16,.18),'terracotta')
    # Repeated trim/curtains, bedroom finishes, ceilings and bath accessories.
    for level in (0,1):
        b.group='ground' if level==0 else 'upper'; y=level*h
        for x in (-7,7):
            for edge in (-2.75,2.75):
                for i in range(5):
                    b.box((x+edge+i*.065,y+1.7,-3.78),(.035,2.8,.16),'linen')
            b.rod((x-3,y+3.2,-3.6),(x+3,y+3.2,-3.6),.025,'brass')
        # Ceiling border stays clear of the dining void on the upper slab.
        for x in (-11.6,-2.4):
            b.box((x,y+3.35,1.4),(.12,.08,10),'wood')
        for z in (-3.4,6.4):
            b.box((-7,y+3.35,z),(9.2,.08,.12),'wood')
        for x in (-10,-4,4,10):
            for z in (5,13.5):
                b.ellipsoid((x,y+3.38,z),(.16,.025,.16),'cream',emissive=True)
        for z in (11.1,14.6):
            b.rod((-11.7,y+1.2,z),(-11.7,y+1.2,z+.65),.025,'brass')
            b.box((-11.64,y+.96,z+.3),(.08,.45,.45),'linen')
        for x in (-10.5,-9.8):
            b.ellipsoid((x,y+1.05,10.75),(.12,.24,.12),'green')
        art(b,-5.3,y+2.1,15.72,2.3)
    # Master suite: upholstered feature wall, bench and reading nook.
    b.group='upper'; y=h
    b.box((-7,y+1.3,-2.65),(4.4,2.6,.12),'linen')
    for i in range(9):
        b.box((-9+i*.5,y+1.3,-2.74),(.035,2.6,.08),'wood')
    b.box((-7,y+.3,1.2),(2,.5,.65),'linen',True)
    chair(b,-10.5,y,.6,-1); lamp(b,-10.5,y,1.5)
    # Guest bedrooms: rugs, foot benches, desks and layered bedding.
    for x,z,group,base in ((-5.2,10,'ground',0),(8,10,'upper',h)):
        b.group=group
        b.box((x,base+.03,z),(4.5,.025,4.5),'linen')
        b.box((x,base+.81,z+.9),(2.2,.04,.5),'terracotta')
        b.box((x,base+.3,z+1.9),(1.8,.45,.5),'sand',True)
    b.group='upper'
    # Home office and gallery, with joinery at the rear wall of the salon.
    b.box((8,h+1.15,6.65),(5.5,2.3,.4),'wood',True)
    for yy in (.4,1.1,1.8):
        b.box((8,h+yy,6.38),(5.4,.06,.55),'sand')
        for xx in (5.8,7.3,9): books(b,xx,h+yy,6.15)
    b.box((8,h+1.18,4.8),(.9,.6,.06),'black')
    b.box((8,h+.89,4.8),(.5,.06,.3),'charcoal')
    lamp(b,9,.84+h,4.8)
    books(b,6.9,h+.84,4.8,5)
    # Family lounge accessories.
    b.box((-5,h+.03,12.6),(5.5,.025,4.9),'linen')
    art(b,-5,h+2.5,7.3,3)
    lamp(b,-3.1,h,14.7)
    # Balcony and terrace read as outdoor rooms.
    plant(b,-8.4,h,-4.8)
    b.group='ground'
    sofa(b,-7,0,17.4,3.5); table(b,-7,0,18.8,2,.8)
    plant(b,-10,0,17.5); plant(b,10.5,0,18)
    for x in (-8,-6,6,8): pendant(b,x,17.5,3.4,2.8,.2)
