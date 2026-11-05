"""Single camera owner: overview, routed tour, collision walking or pet follow."""
import math
import vpython as v
from . import config as C
from .navigation import NODES, STOPS, LOOKS, route, can_walk


# eye, room-centred orbit pivot, automatic cutaway
ROOM_VIEWS = {
    'Living Room': ((-3.4,2.5,-2),(-7,1.1,2.8),'Ground floor'),
    'Dining Salon': ((4.2,2.6,4.2),(7,1.4,0),'Ground floor'),
    'Kitchen': ((4.3,2.4,6.2),(9,1.2,11),'Ground floor'),
    'Guest Bedroom': ((-3,2.2,14),(-5.2,1,10),'Ground floor'),
    'Guest Bathroom': ((-8.6,2.1,11.8),(-10,1,13),'Ground floor'),
    'Master Suite': ((-3.5,6.2,2),(-7,4.7,-.7),'Roof off'),
    'Master Bathroom': ((-8.6,5.7,4.6),(-10,4.6,5.5),'Roof off'),
    'Bedroom 2': ((4.2,6.1,13.4),(8,4.6,10),'Roof off'),
    'Family Lounge': ((-2.8,6.2,9.5),(-5,4.7,13),'Roof off'),
    'Shared Bathroom': ((-8.6,5.7,11.8),(-10,4.6,13),'Roof off'),
    'Home Office': ((4,6.3,3.4),(8,4.9,5),'Roof off'),
    'Balcony': ((-3,6.7,-8.8),(-5.6,4.4,-5.5),'Roof off'),
    'Rear Terrace': ((-3,3.2,21),(-6,1,17.5),'Full exterior'),
    'Pool & Garden': ((15,9,33),(3,.5,25),'Full exterior'),
    'BBQ Pavilion': ((-7,4.2,21),(-13,1,26),'Full exterior'),
    'Garage': ((-24,5,-9),(-16,1,1),'Full exterior'),
}


class Cameras:
    def __init__(self,scene,obstacles,dog):
        self.scene,self.obstacles,self.dog=scene,obstacles,dog
        self.mode='Overview'; self.location='Front overview'
        self.keys=set(); self.node='front'; self.stop=0
        self.queue=[]; self.target_node=None; self.pause=False; self.dwell=0
        self.yaw=0; self.pitch=0; self.floor=0; self.status=None
        self.orbit_transition=None
        self.cutaway=None
        self.scene.bind('keydown',self.keydown)
        self.scene.bind('keyup',self.keyup)
        self.overview('front',immediate=True)

    def keydown(self,event):
        key=event.key.lower()
        if key=='escape':
            self.explore()
        elif self.mode=='Walk':
            self.keys.add(key)

    def keyup(self,event):
        self.keys.discard(event.key.lower())

    def change(self,mode):
        if self.mode=='Room view' and mode!='Room view' and self.cutaway:
            self.cutaway('Full exterior')
        self.keys.clear(); self.mode=mode
        self.queue=[]; self.target_node=None; self.orbit_transition=None
        self.scene.userspin=mode in ('Overview','Room view')
        self.scene.userzoom=mode in ('Overview','Room view')
        self.scene.userpan=mode in ('Overview','Room view')
        self.pause=False; self.dwell=0
        self.report()

    def report(self):
        if self.status:
            text=f'  {self.location}  |  {self.mode}'
            if self.mode=='Tour' and self.pause: text+=' (paused)'
            if self.status.text!=text: self.status.text=text

    def eye(self,node):
        x,y,z=NODES[node]
        return v.vector(x,y+C.EYE_HEIGHT,z)

    def point(self,pos,look):
        self.scene.camera.pos=pos
        self.scene.camera.axis=look-pos

    def room(self,name):
        eye,pivot,cut=ROOM_VIEWS[name]
        self.change('Room view')
        if self.cutaway: self.cutaway(cut)
        self.scene.fov=math.radians(70)
        self.scene.up=v.vector(0,1,0)
        self.point(v.vector(*eye),v.vector(*pivot))
        self.scene.center=v.vector(*pivot)
        self.location=name+' · drag to rotate · wheel to zoom'
        self.report()

    def overview(self,which='front',immediate=False):
        self.change('Overview')
        self.scene.fov=math.pi/3
        self.scene.up=v.vector(0,1,0)
        views={'front':((30,16,-38),(0,3,1)),
               'estate':((48,32,-57),(0,1,-1)),
               'backyard':((36,27,46),(0,1,20)),
               'upstairs':((25,24,-22),(0,4,5)),
               'garage':((-29,12,-18),(-16,1,1))}
        pos,look=views[which]; pos=v.vector(*pos); look=v.vector(*look)
        self.location=which.title()+' overview'
        if immediate: self.point(pos,look)
        else:
            # Overview transfer rises above all structures before crossing the lot.
            self.orbit_transition=[v.vector(self.scene.camera.pos.x,26,self.scene.camera.pos.z),
                                   v.vector(pos.x,26,pos.z),pos]
            self.overview_look=look
        self.report()

    def explore(self):
        # Explicit entry placement avoids inheriting an aerial camera as a walker.
        self.change('Walk'); self.node='front'; self.floor=0
        self.yaw=0; self.pitch=0; self.location='Front path — walk'
        self.point(self.eye('front'),self.eye('front')+v.vector(0,0,1))
        self.report()

    def floor_transfer(self,up):
        self.change('Walk')
        self.node='landing' if up else 'hall'
        self.floor=C.FLOOR_HEIGHT if up else 0
        self.yaw=math.pi if up else 0; self.pitch=0
        self.location='Upstairs landing' if up else 'Ground floor hall'
        pos=self.eye(self.node)
        self.point(pos,pos+v.vector(0,0,-1 if up else 1)); self.report()

    def begin(self,index=0):
        self.change('Tour'); self.stop=index; self.node='front'
        # A named tour entry is an explicit reset, then all travel uses door routes.
        self.point(self.eye('front'),v.vector(*LOOKS['front']))
        self.travel(index)

    def travel(self,index):
        index=max(0,min(len(STOPS)-1,index)); self.stop=index
        destination=STOPS[index][1]
        # Mid-segment changes first return along the current clear segment.
        self.queue=([self.node] if self.target_node else [])+route(self.node,destination)
        self.target_node=None; self.dwell=0; self.pause=False
        self.location=f'{index+1:02d} / {len(STOPS)} · {STOPS[index][0]}'
        self.report()

    def next(self,delta):
        if self.mode!='Tour': self.begin((self.stop+delta)%len(STOPS))
        else: self.travel((self.stop+delta)%len(STOPS))

    def follow(self):
        self.change('Follow dog'); self.location='Front lawn'; self.report()

    def update(self,dt):
        if self.mode=='Room view':
            return  # native mouse interaction owns the camera until another action
        if self.mode=='Overview':
            if self.orbit_transition:
                target=self.orbit_transition[0]
                pos=self.scene.camera.pos; diff=target-pos
                pos=target if v.mag(diff)<dt*C.OVERVIEW_SPEED else pos+v.norm(diff)*dt*C.OVERVIEW_SPEED
                self.point(pos,self.overview_look)
                if v.mag(diff)<dt*C.OVERVIEW_SPEED: self.orbit_transition.pop(0)
            return
        if self.mode=='Follow dog':
            side=v.vector(-self.dog.heading.z,0,self.dog.heading.x)
            pos=self.dog.pos+self.dog.heading*.8+side*2.3+v.vector(0,1.05,0)
            self.point(pos,self.dog.pos+v.vector(0,.4,0)); return
        if self.mode=='Walk':
            # keysdown is the supported snapshot; event state is never a second owner.
            pressed={k.lower() for k in v.keysdown()}
            self.keys.intersection_update(pressed)
            self.yaw+=((('right' in self.keys)-('left' in self.keys))*C.TURN_SPEED*dt)
            self.pitch=max(-.8,min(.8,self.pitch+(('up' in self.keys)-('down' in self.keys))*dt))
            forward=v.vector(-math.sin(self.yaw),0,math.cos(self.yaw))
            right=v.vector(-forward.z,0,forward.x)
            direction=forward*(('w' in self.keys)-('s' in self.keys))+right*(('d' in self.keys)-('a' in self.keys))
            if v.mag(direction)>0:
                delta=v.norm(direction)*C.WALK_SPEED*dt
                # Axis-separated resolution slides along walls; <=0.15 m per step.
                for shift in (v.vector(delta.x,0,0),v.vector(0,0,delta.z)):
                    p=self.scene.camera.pos+shift
                    floor=can_walk(p.x,p.z,self.floor,self.obstacles)
                    if floor is not None:
                        self.floor=floor; self.scene.camera.pos=v.vector(p.x,floor+C.EYE_HEIGHT,p.z)
            self.scene.camera.axis=forward*math.cos(self.pitch)+v.vector(0,math.sin(self.pitch),0)
            self.location=f'Walking · {"upstairs" if self.floor>3.5 else "stairs" if self.floor>.1 else "ground"}'
            self.report(); return
        if self.mode=='Tour' and not self.pause:
            if self.target_node is None and self.queue:
                self.target_node=self.queue.pop(0)
            if self.target_node is not None:
                target=self.eye(self.target_node); pos=self.scene.camera.pos
                diff=target-pos; distance=v.mag(diff)
                if distance<=dt*C.TOUR_SPEED:
                    self.scene.camera.pos=target; self.node=self.target_node; self.target_node=None
                else:
                    self.scene.camera.pos=pos+v.norm(diff)*dt*C.TOUR_SPEED
                if distance>.01:
                    desired=v.norm(diff)
                    axis=v.norm(self.scene.camera.axis)
                    blended=axis+(desired-axis)*min(1,dt*5)
                    if v.mag(blended)>.01: self.scene.camera.axis=v.norm(blended)
            else:
                look=v.vector(*LOOKS.get(self.node,(0,1,0)))-self.scene.camera.pos
                axis=v.norm(self.scene.camera.axis); desired=v.norm(look)
                self.scene.camera.axis=axis+(desired-axis)*min(1,dt*3)
                self.dwell+=dt
                if self.dwell>C.TOUR_DWELL:
                    if self.stop==len(STOPS)-1:
                        self.pause=True; self.report()
                    else: self.travel(self.stop+1)
