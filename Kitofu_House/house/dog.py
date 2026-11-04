"""A small procedural Shihpoo and butterfly. No per-frame object creation."""
import math
import vpython as v
from .geometry import color
from .navigation import dog_route


class Dog:
    def __init__(self):
        self.time=0.0
        self.paused=False
        self.parts=[]
        self.legs=[]
        self.tail=[]
        self.pos=v.vector(0,0,0)
        self.heading=v.vector(1,0,0)
        def part(pos,size,mat='white',kind='body'):
            obj=v.ellipsoid(pos=v.vector(*pos),size=v.vector(*size),color=color(mat),shininess=0.05)
            entry=(obj,v.vector(*pos))
            if kind=='leg': self.legs.append(entry)
            elif kind=='tail': self.tail.append(entry)
            else: self.parts.append(entry)
            return obj
        part((0,0.38,0),(0.62,0.39,0.34))
        part((0.29,0.57,0),(0.36,0.36,0.36))
        part((0.44,0.49,0),(0.2,0.17,0.25))
        for side in (-1,1):
            part((0.26,0.51,side*0.18),(0.22,0.33,0.13),'sand')
            part((0.43,0.61,side*0.105),(0.055,0.065,0.052),'black')
            part((0.452,0.627,side*0.11),(0.016,0.017,0.017),'white')
        part((0.535,0.51,0),(0.07,0.055,0.08),'black')
        for x in (-0.22,0.21):
            for z in (-0.13,0.13):
                part((x,0.16,z),(0.14,0.28,0.15),'white','leg')
        # Limited scallops suggest fluff, rather than thousands of strands.
        for x,y,z in ((-.27,.46,0),(-.08,.55,0),(.1,.54,0),(.23,.73,0),
                      (.34,.69,.12),(.34,.69,-.12),(-.13,.37,.17),(-.13,.37,-.17)):
            part((x,y,z),(0.22,0.19,0.19))
        for i in range(6):
            a=i*math.pi/5
            part((-.32-.10*math.sin(a),.49+.23*math.sin(a/2),.08*math.cos(a)),(.17,.17,.17),'white','tail')
        self.butterfly=v.ellipsoid(size=v.vector(.16,.05,.055),color=color('charcoal'))
        self.wings=[v.ellipsoid(size=v.vector(.19,.025,.24),color=color('brass')) for _ in range(2)]
        self.update(0)

    def update(self,dt):
        if not self.paused:
            self.time+=dt
        t=self.time
        x,z=dog_route(t); nx,nz=dog_route(t+0.05)
        self.heading=v.norm(v.vector(nx-x,0,nz-z))
        side=v.vector(-self.heading.z,0,self.heading.x)
        bounce=0.018*(1+math.sin(t*13))
        # Brief smooth hop once per 17 s, still on the bounded route.
        phase=t%17
        hop=.16*math.sin(math.pi*(phase-14)/.7) if 14<phase<14.7 else 0
        self.pos=v.vector(x,bounce+hop,z)
        def world(local):
            return self.pos+self.heading*local.x+v.vector(0,local.y,0)+side*local.z
        for obj,local in self.parts:
            obj.pos=world(local); obj.axis=self.heading*obj.length
        for i,(obj,local) in enumerate(self.legs):
            stride=math.sin(t*13+(0 if i in (0,3) else math.pi))
            obj.pos=world(local+v.vector(.045*stride,.025*max(0,stride),0))
            obj.axis=v.norm(self.heading+v.vector(0,.25*stride,0))*obj.length
        for obj,local in self.tail:
            obj.pos=world(local+v.vector(0,0,.035*math.sin(t*8)))
            obj.axis=self.heading*obj.length
        bx,bz=dog_route(t+1.3)
        self.butterfly.pos=v.vector(bx,1.05+.15*math.sin(t*3),bz)
        self.butterfly.axis=self.heading*self.butterfly.length
        flap=math.sin(t*25)*0.8
        for i,wing in enumerate(self.wings):
            sign=-1 if i==0 else 1
            wing.pos=self.butterfly.pos+side*(sign*.1)+v.vector(0,abs(flap)*.055,0)
            wing.axis=self.heading*wing.length
            wing.up=v.norm(v.vector(0,1,0)+side*(sign*flap))
