"""Street -> lawn -> house -> pool; boundary palms and a separate pavilion."""
import math
import vpython as v
from . import config as C
from .geometry import color
from .interiors import table, chair, sofa
from .navigation import Obstacle

WATER_SURFACE=None


def animate(t):
    if WATER_SURFACE is not None:
        WATER_SURFACE.color=color((.16+.015*math.sin(t),.59+.025*math.sin(t*.7),.65))


def palm(b,x,z):
    start=len(b.groups[b.group])
    b.rod((x,0,z),(x+0.25,5.6,z),0.18,'wood')
    n=5 if C.DETAIL=='low' else 8
    for i in range(n):
        a=i*2*math.pi/n
        leaf=b.ellipsoid((x+math.cos(a)*1.2,5.5,z+math.sin(a)*1.2),(3.4,0.18,0.65),'leaf')
        leaf.axis=v.norm(v.vector(math.cos(a),-0.2,math.sin(a)))*leaf.length
    b.compound_since(start)
    b.obstacles.append(Obstacle(x,z,0.5,0.5,0,5.5))


def build(b):
    global WATER_SURFACE
    b.group='site'; W,D=C.LOT_WIDTH,C.LOT_DEPTH
    # Split the terrain around the pool, leaving a genuine 1.5 m basin opening.
    px,pz,pw,pd=C.POOL
    left,right=px-pw/2,px+pw/2
    near,far=pz-pd/2,pz+pd/2
    for x1,x2,z1,z2 in ((-W/2,left,-D/2,D/2),(right,W/2,-D/2,D/2),
                        (left,right,-D/2,near),(left,right,far,D/2)):
        b.box(((x1+x2)/2,-1.5,(z1+z2)/2),(x2-x1,2.9,z2-z1),'grass')
    b.box((0,-0.17,-D/2-4),(W+12,0.2,8),'charcoal')
    for x in range(-24,25,6):
        b.box((x,-0.058,-D/2-4),(3,0.01,0.12),'cream')
    b.box((0,-0.05,-D/2-0.7),(W,0.14,1.4),'sand')
    # Perimeter: open pedestrian and driveway passages at the street.
    for x in (-W/2,W/2):
        b.box((x,1.1,0),(0.25,2.2,D),'ivory',True)
    b.box((0,1.1,D/2),(W,2.2,0.25),'ivory',True)
    for a,c in ((-W/2,-19.5),(-12.5,-1.5),(1.5,W/2)):
        b.box(((a+c)/2,0.65,-D/2),(c-a,1.3,0.3),'stone',True)
        count=max(1,int((c-a)/0.45))
        start=len(b.groups['site'])
        for i in range(count):
            b.box((a+(i+0.5)*(c-a)/count,1.65,-D/2),(0.09,0.7,0.09),'wood')
        b.compound_since(start)
    # Gates visibly slid aside / swung open, so both passages are usable.
    b.box((-9,1.1,-34.7),(6.5,1.8,0.08),'charcoal',True)
    b.box((1.55,1.0,-33.9),(0.09,1.9,2),'wood',True)
    b.box((-16,-0.03,-18),(7,0.08,34),'stone')
    b.box((0,0.015,-20),(2.7,0.06,30),'sand')
    b.box((0,0.01,-7),(34,0.06,2),'sand')
    # West/east paths extend to the rear, preserving the central front lawn.
    for x in (-20,14):
        b.box((x,0.01,9),(1.6,0.06,38),'sand')
    b.box((-6,0.01,20),(27,0.06,1.8),'sand')
    # Pool surround with a real inset basin; terrain pieces are not used as water.
    x,z,w,d=C.POOL
    for side in (-1,1):
        b.box((x+side*(w/2+.75),0,z),(1.5,0.12,d+3),'sand')
        b.box((x,0,z+side*(d/2+.75)),(w,0.12,1.5),'sand')
    b.box((x,-1.45,z),(w,0.12,d),'blue')
    for px in (x-w/2,x+w/2):
        b.box((px,-0.62,z),(0.22,1.7,d),'cream')
    for pz in (z-d/2,z+d/2):
        b.box((x,-0.62,pz),(w,1.7,0.22),'cream')
    WATER_SURFACE=b.box((x,0.08,z),(w-0.3,0.035,d-0.3),'water',opacity=0.57)
    b.obstacles.append(Obstacle(x,z,w+0.5,d+0.5,-1,1))
    for i in range(3):
        b.box((x-w/2+0.4+i*0.38,-0.1-i*0.3,z-1.6),(0.42,0.18,1.8),'cream')
    for zz in (z-0.6,z+0.1):
        b.rod((x+w/2+0.4,0.1,zz),(x+w/2+0.4,1.15,zz),0.04)
        b.rod((x+w/2+0.4,1.15,zz),(x+w/2-0.4,1.15,zz),0.04)
        b.rod((x+w/2-0.4,1.15,zz),(x+w/2-0.4,0.2,zz),0.04)
    for lx in (-1,3,7):
        b.box((lx,0.28,30.5),(1.1,0.32,2.4),'wood',True)
        b.box((lx,0.49,30.4),(0.95,0.14,2),'cream')
        pillow=b.box((lx,0.68,31.3),(0.95,0.3,0.7),'sand')
    x,z,w,d=C.PAVILION
    b.box((x,0.02,z),(w,0.14,d),'wood')
    for px in (x-w/2+0.2,x+w/2-0.2):
        for pz in (z-d/2+0.2,z+d/2-0.2):
            b.box((px,1.65,pz),(0.2,3.3,0.2),'wood',True)
    b.box((x,3.4,z),(w+0.7,0.25,d+0.7),'charcoal')
    b.box((x,3.23,z),(w+0.3,0.08,d+0.3),'wood')
    b.box((x-3,0.5,z+1),(1.4,1,4),'stone',True)
    b.box((x-3,1.05,z+1),(1.6,0.12,4.2),'cream')
    b.box((x-3,1.17,z),(1.2,0.16,1.4),'black')
    for i in range(7):
        b.rod((x-3.5,1.28,z-0.55+i*0.17),(x-2.5,1.28,z-0.55+i*0.17),0.018,'stone')
    b.ellipsoid((x-3,1.13,z+2),(0.9,0.04,0.65),'stone')
    b.rod((x-3.45,1.1,z+2),(x-3.45,1.45,z+2),0.035)
    table(b,x+0.5,0,z,2.5,1.1)
    for xx in (x-0.3,x+1.3):
        chair(b,xx,0,z-1,-1); chair(b,xx,0,z+1)
    sofa(b,x+0.6,0,z+2.8,3.5)
    for xx in (x-2,x+2):
        b.ellipsoid((xx,3.03,z),(0.28,0.12,0.28),'cream',emissive=True)
    lights=[v.local_light(pos=v.vector(x,2.8,z),color=v.vector(0.25,0.18,0.09),visible=False)]
    for x,z in C.TREE_POSITIONS:
        palm(b,x,z)
    for x in (-20.6,20.6):
        for z in range(-28,32,5 if C.DETAIL=='low' else 3):
            b.ellipsoid((x,0.45,z),(1.2,0.9,1.8),'leaf')
    # A brass address plaque beside the front pedestrian gate.
    b.box((4,1.35,-35.2),(3.8,0.6,0.08),'green')
    b.keep(v.text(text=C.TITLE, pos=v.vector(2.4,1.2,-35.26), height=0.22,
                  depth=0.015, color=color('cream'), align='left', axis=v.vector(1,0,0)))
    # Planting beds frame the lawn without entering the dog's safe loop.
    for bx,bz,length in ((17,-21,12),(17,10,14),(-10,-30,8),(15,29,7)):
        b.box((bx,.13,bz),(2.5,.3,length),'travertine',True)
        b.box((bx,.3,bz),(2.25,.08,length-.2),'wood')
        for i in range(int(length)):
            zz=bz-length/2+.5+i
            b.ellipsoid((bx,.65,zz),(1.4,.9,1.1),'leaf')
            for dx in (-.6,.6):
                b.ellipsoid((bx+dx,.5,zz),(.5,.45,.5),'green')
            if i%2==0: b.ellipsoid((bx,.98,zz),(.3,.2,.3),'cream')
    for zz in range(-31,-8,2):
        b.box((0,.049,zz),(2.6,.014,.06),'wood')
    for xx,zz in ((2,-30),(2,-9),(12,19),(-18,22),(11,31)):
        b.box((xx,.3,zz),(.18,.6,.18),'charcoal',True)
        b.box((xx,.57,zz),(.2,.14,.2),'cream',emissive=True)
        lights.append(v.local_light(pos=v.vector(xx,.8,zz),color=v.vector(.12,.085,.045),visible=False))
    b.rod((5,.1,32),(5,2.8,32),.045,'wood')
    b.ellipsoid((5,2.8,32),(4,.35,3.5),'linen')
    for xx in (-1,3,7):
        for i in range(2): b.box((xx,.61+i*.045,30),(.7,.04,.4),'white')
    for zz in range(23,30): b.box((-13,3.15,zz),(8.7,.1,.08),'wood')
    for xx in (-15,-13,-11):
        b.rod((xx,3.1,26),(xx,2.5,26),.015,'brass')
        b.ellipsoid((xx,2.48,26),(.45,.25,.45),'linen')
    for xx,yy,zz in ((-7,2.8,2),(8,5.7,0),(7.5,2.7,10),(-7,6.5,-1),(0,2.8,-2)):
        lights.append(v.local_light(pos=v.vector(xx,yy,zz),color=v.vector(.18,.13,.075),visible=False))
    return lights
