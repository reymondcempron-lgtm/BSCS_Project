"""Two floors, real door/window openings, open stairwell and tropical shell."""
from . import config as C
import vpython as v


def build(b):
    f,r,w,h = C.HOUSE_FRONT,C.HOUSE_REAR,C.HOUSE_WIDTH/2,C.FLOOR_HEIGHT
    for level in range(2):
        base = level*h
        b.group = 'ground' if level == 0 else 'upper'
        if level == 0:
            b.box((0,-C.SLAB/2,(f+r)/2),(2*w,C.SLAB,r-f),'sand')
        else:
            # Slab intentionally split around the stairs at x=.45..2.65,z=5..12.2.
            b.box((-5.775,base-C.SLAB/2,6),(12.45,C.SLAB,20),'sand')
            # Dining salon void: x=5..11.7, z=-3.7..2.2. Gallery on two edges.
            b.box((3.825,base-C.SLAB/2,6),(2.35,C.SLAB,20),'sand')
            b.box((8.35,base-C.SLAB/2,9.1),(6.7,C.SLAB,13.8),'sand')
            b.box((8.35,base-C.SLAB/2,-3.85),(6.7,C.SLAB,0.3),'sand')
            b.box((11.85,base-C.SLAB/2,6),(0.3,C.SLAB,20),'sand')
            b.box((1.55,base-C.SLAB/2,0.5),(2.2,C.SLAB,9),'sand')
            b.box((1.55,base-C.SLAB/2,14.1),(2.2,C.SLAB,3.8),'sand')
        front_open = [(-7,6,0.75,2.2,True),(0,2.8,0,2.8,False),(7,6,0.75,2.2,True)]
        if level:
            front_open = [(-5,2.2,0,2.8,False),(0,2,0.8,2.1,True),(7,6,0.75,2.2,True)]
        b.wall('x',f,-w,w,base,h,front_open)
        b.wall('x',r,-w,w,base,h,[(-7,6,0.75,2.2,True),(0,2.8,0,2.8,False) if level==0 else (0,2,0.8,2.1,True),(7,6,0.75,2.2,True)])
        for x in (-w,w):
            b.wall('z',x,f,r,base,h,[(0,4,0.8,2.1,True),(7,4,0.8,2.1,True),(13,3,0.8,2.1,True)])
        # A 4 m circulation core joins every room. Right rear core widens for stairs.
        b.wall('z',-2,f,r,base,h,[(1,2.2,0,2.7,False),(12.5,2.2,0,2.7,False)])
        b.wall('z',2,f,4.7,base,h,[(3.5,1.8,0,2.7,False)])
        b.wall('z',3,4.7,r,base,h,[(12.5,2.2,0,2.7,False)])
        b.wall('x',7,-w,-2,base,h,[])
        if level:
            b.wall('x',7,3,w,base,h,[])
        # Bathroom reached through each west bedroom; a real internal doorway.
        b.wall('z',-8,10,r,base,h,[(12.5,1.4,0,2.5,False)])
        b.wall('x',10,-w,-8,base,h,[])
        # Skirting/soffit facade bands.
        b.box((0,base+h-0.12,f-0.18),(24.6,0.22,0.5),'stone')
    b.group = 'ground'
    # Stair treads double as a continuous collision ramp in navigation.py.
    for i in range(24):
        rise = (i+1)*h/24
        b.box((1.55,rise/2,5+(i+0.5)*0.3),(2.1,rise,0.3),'wood')
    for x in (0.48,2.62):
        b.rod((x,0.9,5),(x,h+0.9,12.2),0.045)
        for i in range(0,25,3):
            z=5+i*0.3; y=i*h/24
            b.rod((x,y,z),(x,y+0.9,z),0.025)
    # Terrace and generous shaded upstairs balcony.
    b.box((0,-0.08,r+1.7),(24,0.16,3.4),'wood')
    b.group = 'upper'
    b.box((-5.6,h-0.12,f-1.5),(7,0.24,3),'wood')
    for x in (-9.05,-2.15):
        b.box((x,h+0.55,f-1.5),(0.09,1.1,3),'charcoal',True)
    b.box((-5.6,h+0.55,f-3),(7,1.1,0.07),'glass',True,opacity=0.3)
    b.rod((-9.1,h+1.1,f-3),(-2.1,h+1.1,f-3),0.045)
    # Guard the upper void, leaving the rear landing open.
    for x in (0.45,2.65):
        b.box((x,h+0.5,8.6),(0.08,1,7.2),'charcoal',True)
    # Gallery balustrades prevent walking into the actual double-height void.
    for x,z,sz in ((5,-.75,(.08,1.1,5.9)),(8.35,2.2,(6.7,1.1,.08))):
        b.box((x,h+.55,z),sz,'glass',True,opacity=.25)
        b.box((x,h+1.1,z),(sz[0],.07,sz[2]),'charcoal')
    b.group = 'roof'
    # Two pitched wings: a stepped silhouette, deep eaves and timber soffits.
    import math
    for cx,width,top in ((-6.4,14.4,8.9),(6.4,14.4,9.4)):
        pitch=math.radians(13); half=width/2
        for side in (-1,1):
            for offset,thick,mat in ((0,.22,'roof'),(-.16,.08,'wood')):
                b.box((cx+side*half/2,top-half/2*math.tan(pitch)+offset,6),
                      (half/math.cos(pitch),thick,23.5),mat,
                      axis=v.vector(math.cos(pitch),-side*math.sin(pitch),0))
        b.box((cx,top+.1,6),(.25,.15,23.6),'roof')
        # Stepped narrow infill panels close both gable ends beneath the slopes.
        for i in range(36):
            xx=cx-half+(i+.5)*width/36
            if abs(xx)>w-.2:
                continue
            wall_top=top-abs(xx-cx)*math.tan(pitch)-.22
            if wall_top>2*h:
                for zz in (f,r):
                    b.box((xx,(wall_top+2*h)/2,zz),(width/36+.01,wall_top-2*h,.22),'ivory')
    b.box((0,7.35,-5.7),(5.2,.25,4.4),'ivory')
    # No rooftop room: only solar hardware above the second floor.
    for x in (-9.5,9.5):
        top=8.9 if x<0 else 9.4
        y=top-abs(x-(-6.4 if x<0 else 6.4))*math.tan(pitch)+.18
        ax=v.vector(math.cos(pitch),(.225 if x<0 else -.225),0)
        for z in (7,11,15):
            b.box((x,y,z),(3.7,.08,3.2),'blue',axis=ax)
            for dz in (-1.05,0,1.05):
                b.box((x,y+.05,z+dz),(3.7,.015,.025),'charcoal',axis=ax)
    b.group = 'ground'
    # Stone entrance pier and timber screening; leave entrance completely clear.
    b.box((3.1,1.8,f-0.35),(1.2,3.6,0.55),'stone')
    for i in range(6 if C.DETAIL=='low' else 12):
        b.box((-11+i*0.23,1.8,f-0.4),(0.09,3.4,0.16),'wood')
    for x in (-10,10):
        b.box((x,1.8,r+2.9),(0.24,3.6,0.24),'stone',True)
    b.box((0,3.5,r+1.5),(25,0.18,3.5),'wood')
    # Covered side garage, accessible from its open street-facing end.
    x,z,gw,gd=C.GARAGE
    b.group='site'
    b.box((x,-0.06,z),(gw,0.12,gd),'stone')
    b.box((x,3.3,z),(gw+0.6,0.24,gd+0.5),'ivory')
    for px in (x-gw/2,x+gw/2):
        for pz in (z-gd/2,z+gd/2):
            b.box((px,1.6,pz),(0.22,3.2,0.22),'charcoal',True)
    # Entrance portal, recessed glazing surrounds and timber balcony screens.
    b.group='ground'
    for px in (-2.1,2.1):
        b.box((px,1.85,f-1.5),(.42,3.7,.5),'travertine',True)
    b.box((0,3.8,f-1.5),(4.65,.28,3.5),'ivory')
    b.box((0,3.62,f-1.5),(4.2,.08,3.1),'wood')
    for level in range(2):
        b.group='ground' if level==0 else 'upper'
        for px in (-7,7):
            b.box((px,level*h+3.1,f-.45),(6.5,.13,1.05),'ivory')
        for px in (-11.55,11.55):
            b.box((px,level*h+1.8,f-.35),(.45,3.6,.7),'travertine')
    b.group='upper'
    for i in range(11):
        b.box((-9.3+i*.18,h+1.5,-6.8),(.07,2.9,.18),'wood')
    b.box((-5.6,h-.35,-5.5),(7.4,.22,3.4),'ivory')
    b.group='site'
    for i in range(14):
        b.box((x,3.12,z-gd/2+i*gd/14),(gw,.08,.075),'wood')
