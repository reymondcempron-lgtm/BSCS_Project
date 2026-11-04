"""Original simplified silhouettes, no licensed models or manufacturer logos."""
import vpython as v
from .navigation import Obstacle


def wheel(b,x,y,z,r=0.35,width=0.18):
    b.rod((x-width/2,y,z),(x+width/2,y,z),r,'black')
    b.rod((x-width/2-0.01,y,z),(x+width/2+0.01,y,z),r*0.63,'stone')
    b.rod((x-width/2-0.02,y,z),(x+width/2+0.02,y,z),r*0.19,'charcoal')


def motorcycle(b,x,z,adventure=False):
    start=len(b.groups['site'])
    r=0.38 if adventure else 0.31
    for zz in (z-0.78,z+0.78):
        wheel(b,x,r,zz,r)
    b.rod((x,0.45,z+0.7),(x,0.8,z-0.3),0.085)
    b.rod((x,0.45,z-0.78),(x,1.05,z-0.5),0.055,'stone')
    b.ellipsoid((x,0.87,z),(0.5,0.5,0.85),'stone' if adventure else 'white')
    b.box((x,0.91,z+0.45),(0.42,0.15,0.75),'black')
    b.ellipsoid((x,0.62,z-0.25),(0.6,0.75,0.95),'green' if adventure else 'white')
    if not adventure:
        for dx in (-0.305,0.305):
            b.ellipsoid((x+dx,0.68,z-0.3),(0.025,0.38,0.75),'blue')
            b.box((x+dx,0.76,z-0.4),(0.028,0.08,0.55),'red')
    b.box((x,1.22 if adventure else 1.09,z-0.63),(0.42,0.6 if adventure else 0.3,0.05),'glass',opacity=0.45)
    b.rod((x-0.4,1.04,z-0.35),(x+0.4,1.04,z-0.35),0.04)
    for dx in (-0.38,0.38):
        b.rod((x+dx,1.05,z-0.35),(x+dx,1.26,z-0.5),0.02)
        b.ellipsoid((x+dx,1.26,z-0.5),(0.18,0.1,0.08),'charcoal')
    b.rod((x+0.3,0.4,z+0.25),(x+0.3,0.55,z+0.95),0.09,'stone')
    b.box((x,0.92,z-0.91),(0.35,0.11,0.07),'cream')
    b.box((x,0.95,z+0.85),(0.24,0.08,0.06),'red')
    if adventure:
        for dx in (-0.46,0.46):
            b.box((x+dx,0.85,z+0.6),(0.35,0.5,0.65),'stone')
            b.box((x+dx,1.1,z+0.6),(0.37,0.05,0.67),'black')
    b.compound_since(start)
    b.obstacles.append(Obstacle(x,z,1.2,2.3,0,1.5))


def build(b):
    b.group='site'; x,z=-17.3,1.4
    start=len(b.groups['site'])
    b.ellipsoid((x,0.65,z),(2.1,0.65,4.8),'blue')
    b.box((x,0.7,z),(2,0.35,3.8),'blue')
    b.ellipsoid((x,1.08,z+0.15),(1.7,0.75,2.4),'charcoal')
    b.ellipsoid((x,1.23,z+0.2),(1.55,0.5,2.05),'glass')
    b.box((x,1.47,z+0.3),(1.35,0.06,0.8),'blue')
    for dx in (-1,1):
        for dz in (-1.5,1.5):
            wheel(b,x+dx,0.4,z+dz,0.39,0.24)
        b.box((x+dx*0.92,0.77,z-1.97),(0.55,0.12,0.15),'cream')
        b.box((x+dx*0.75,0.78,z+2.08),(0.5,0.1,0.12),'red')
        b.ellipsoid((x+dx*1.12,1.08,z-0.3),(0.25,0.15,0.35),'blue')
    b.box((x,0.5,z-2.18),(1.3,0.18,0.1),'black')
    b.box((x,0.95,z+1.9),(1.8,0.08,0.3),'charcoal')
    b.compound_since(start)
    b.obstacles.append(Obstacle(x,z,2.4,4.8,0,1.6))
    motorcycle(b,-14.3,0,False)
    motorcycle(b,-14.3,3.5,True)
