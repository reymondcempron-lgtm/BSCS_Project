"""Eye-level VPython walk camera: only arrow keys + mouse.

Mouse rotation uses pixel movement when available, and VPython's 3D
mouse coordinates as a fallback. Native VPython right-drag / Ctrl-drag
rotation remains enabled as an independent fallback.
"""
from math import sin, cos, atan2, hypot, pi
from time import perf_counter
from vpython import vec, keysdown
from geometry import (EYE_HEIGHT, DECK_Y, stair, stair_entrance,
                      within_deck, slide, look_vector,
                      rotate_from_mouse, angles_from_axis)

MOVE_SPEED = 5.0
MOUSE_SENSITIVITY = 0.0040
PITCH_LIMIT = 1.38


def movement(keys, yaw):
    k = {str(key).lower() for key in keys}
    f = int(bool(k & {'up', 'arrowup'})) - int(bool(k & {'down','arrowdown'}))
    s = int(bool(k & {'right','arrowright'})) - int(bool(k & {'left','arrowleft'}))
    dx = sin(yaw)*f + cos(yaw)*s
    dz = -cos(yaw)*f + sin(yaw)*s
    d = hypot(dx,dz)
    return (dx/d, dz/d, f) if d else (0.,0.,f)


class FirstPerson:
    def __init__(self, scene):
        self.scene = scene
        self.x, self.z = 0., 23.6
        self.y = EYE_HEIGHT
        self.yaw = 0.
        self.pitch = -0.025
        self.last_mouse = None
        self.last_world = None
        self.dragging = False
        self.mouse_detected = False
        self.down = set()
        self.mode = 'ground'
        self.stair_t = 0.
        self.last_frame = perf_counter()
        scene.bind('mousemove', self.mousemove)
        scene.bind('mousedown', self.mousedown)
        scene.bind('mouseup', self.mouseup)
        scene.bind('mouseenter', self.reset_mouse)
        scene.bind('keydown', self.keydown)
        scene.bind('keyup', self.keyup)
        self.apply_camera()

    def reset_mouse(self, event=None):
        self.last_mouse = None
        self.last_world = None

    def mousedown(self, event=None):
        self.dragging = True
        self.reset_mouse()

    def mouseup(self, event=None):
        self.dragging = False
        self.reset_mouse()

    def keydown(self, event):
        key = str(getattr(event, 'key', '')).lower()
        if key:
            self.down.add(key)

    def keyup(self, event):
        key = str(getattr(event, 'key', '')).lower()
        self.down.discard(key)

    @staticmethod
    def mouse_coords(event):
        # Depending on browser and VPython version, mousemove events may
        # contain pixel or only projected 3D coordinates.
        try:
            return float(event.pageX), float(event.pageY)
        except (AttributeError, TypeError, ValueError):
            return None

    @staticmethod
    def world_coords(event):
        try:
            p = event.pos
            return float(p.x),float(p.y),float(p.z)
        except (AttributeError, TypeError, ValueError):
            return None

    def mousemove(self,event):
        xy = self.mouse_coords(event)
        if xy is not None:
            if self.last_mouse is not None:
                dx,dy = xy[0]-self.last_mouse[0], xy[1]-self.last_mouse[1]
                if abs(dx) < 300 and abs(dy)<300:
                    self.yaw,self.pitch=rotate_from_mouse(self.yaw,self.pitch,dx,dy)
                    self.apply_camera()
            self.last_mouse=xy
            self.last_world=None
        else:
            # Unconditionally fallback rather than silently disabling look.
            world=self.world_coords(event)
            if world is not None and self.last_world is not None:
                # Approximate screen-right and screen-up directions in the
                # current camera plane; world position is less reliable than
                # pageX/pageY but still provides rotation on older versions.
                delta=[world[i]-self.last_world[i] for i in range(3)]
                right=(cos(self.yaw),0.,sin(self.yaw))
                dx=sum(delta[i]*right[i] for i in range(3))
                dy=delta[1]
                if abs(dx)<12 and abs(dy)<12:
                    self.yaw,self.pitch=rotate_from_mouse(self.yaw,self.pitch,dx,-dy,
                                                     sensitivity=.045)
                    self.apply_camera()
            self.last_world=world
            self.last_mouse=None
        self.mouse_detected=True

    def apply_camera(self):
        a=look_vector(self.yaw,self.pitch)
        self.scene.camera.pos=vec(self.x,self.y,self.z)
        self.scene.camera.axis=vec(*a)*9.5

    def capture_native_mouse_rotation(self):
        """Honor built-in right-drag camera rotation instead of undoing it.

        With scene.userspin=True, VPython changes the camera direction when
        right-dragging. Read that direction before re-anchoring eye position.
        """
        camera=self.scene.camera
        try:
            a=camera.axis
            ax,ay,az=float(a.x),float(a.y),float(a.z)
            d=hypot(hypot(ax,az),ay)
            if d<=1e-5:
                return
            unit=(ax/d,ay/d,az/d)
            expected=look_vector(self.yaw,self.pitch)
            dot=sum(unit[i]*expected[i] for i in range(3))
            if dot<.9999:
                self.yaw,self.pitch=angles_from_axis(*unit)
                self.pitch=max(-PITCH_LIMIT,min(PITCH_LIMIT,self.pitch))
        except (AttributeError, TypeError, ValueError):
            pass

    def step(self):
        now=perf_counter()
        dt=min(.045,max(.005,now-self.last_frame))
        self.last_frame=now
        self.capture_native_mouse_rotation()
        # Combine event-based keyboard tracking and keysdown polling.
        # Both methods cover browsers that use different focus behavior.
        k=set(self.down) | {str(key).lower() for key in keysdown()}
        dx,dz,forward=movement(k,self.yaw)

        if self.mode=='stairs':
            if forward:
                self.stair_t=max(0.,min(1.,self.stair_t+forward*dt*.11))
            self.x,y_step,self.z=stair(self.stair_t)
            self.y=y_step+1.57
            if self.stair_t>=1.0:
                self.mode='deck'
                self.y=DECK_Y+1.72
            elif self.stair_t<=0 and forward<0:
                self.mode='ground'
                self.y=EYE_HEIGHT
            self.apply_camera()
            return

        if self.mode=='ground' and forward>0 and stair_entrance(self.x,self.z):
            self.mode='stairs'
            self.stair_t=0.0
            self.x,y_step,self.z=stair(0.)
            self.y=y_step+1.57
            self.apply_camera()
            return
        if self.mode=='deck' and forward<0 and stair_entrance(self.x,self.z):
            self.mode='stairs'
            self.stair_t=1.0
            self.apply_camera()
            return

        if dx or dz:
            amt=MOVE_SPEED*dt
            nx,nz=self.x+dx*amt,self.z+dz*amt
            if self.mode=='deck':
                if within_deck(nx,self.z): self.x=nx
                if within_deck(self.x,nz): self.z=nz
                self.y=DECK_Y+1.72
            else:
                self.x,self.z=slide(self.x,self.z,dx*amt,dz*amt)
                self.y=EYE_HEIGHT
        self.apply_camera()
