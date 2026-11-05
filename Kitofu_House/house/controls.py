"""Supported VPython widgets only: no JavaScript injection or DOM dependencies."""
import vpython as v
from . import config as C
from .geometry import color
from .cameras import ROOM_VIEWS


def build(scene,camera,builder,dog,local_lights,sun,fill):
    scene.append_to_caption('<br><b>YOUR PRIVATE VISIT</b> &nbsp; Architecture, interiors and gardens.<br><br>')
    def button(text,action,primary=False):
        return v.button(text=text,bind=lambda _:action(),color=color('cream' if primary else 'charcoal'),
                        background=color('green' if primary else 'linen'))
    button('Start House Tour',lambda:camera.begin(),True)
    button('Explore Freely',camera.explore,True)
    def pause_tour():
        if camera.mode=='Tour':
            camera.pause=not camera.pause; camera.keys.clear(); camera.report()
            pause_button.text='Resume Tour' if camera.pause else 'Pause Tour'
    pause_button=button('Pause Tour',pause_tour)
    button('Previous',lambda:camera.next(-1))
    button('Next',lambda:camera.next(1))
    button('Exit tour',lambda:camera.overview())
    scene.append_to_caption('<br><br><b>SPACES</b> &nbsp; Click a room, then right-drag to rotate and scroll to zoom.<br>')
    for index,name in enumerate(ROOM_VIEWS):
        button(name,lambda name=name:camera.room(name))
        if (index+1)%4==0: scene.append_to_caption('<br>')
    scene.append_to_caption('<br><b>EXPLORE</b> &nbsp; ')
    button('Upstairs',lambda:camera.floor_transfer(True))
    button('Downstairs',lambda:camera.floor_transfer(False))
    button('Follow Kitofu',camera.follow)
    scene.append_to_caption('<br><br><b>PRESENTATION</b> &nbsp; ')
    view=v.menu(choices=['Entrance portrait','Entire estate','Backyard retreat','Garage'],bind=lambda _:None)
    button('Show View',lambda:camera.overview(['front','estate','backyard','garage'][view.index]))
    button('Reset View',lambda:camera.overview('front',True))
    def lighting(widget):
        evening=widget.selected=='Evening'
        scene.background=color((.19,.24,.28) if evening else (.78,.86,.87))
        scene.ambient=color((.27,.26,.23) if evening else (.48,.48,.44))
        sun.color=color((.5,.35,.22) if evening else (.75,.72,.64))
        fill.color=color((.16,.21,.3) if evening else (.25,.3,.33))
        for light in local_lights: light.visible=evening
    v.menu(choices=['Day','Evening'],bind=lighting)
    scene.append_to_caption('  Cutaway  ')
    cuts=v.menu(choices=['Full exterior','Roof off','Ground floor'],bind=lambda w:builder.cutaway(w.selected))
    def apply_cutaway(mode):
        builder.cutaway(mode); cuts.selected=mode
    camera.cutaway=apply_cutaway
    dog_button=None
    def pause_dog():
        dog.paused=not dog.paused
        dog_button.text='Resume Kitofu' if dog.paused else 'Pause Kitofu'
    dog_button=button('Pause Kitofu',pause_dog)
    scene.append_to_caption('<br><br><b>NOW EXPLORING</b> &nbsp; ')
    camera.status=v.wtext(text=''); camera.report()
    scene.append_to_caption('\n<b>Walk:</b> click scene, WASD move · arrow keys turn/look · Esc returns to walking entrance. '
                            '<b>Orbit:</b> right-drag or Ctrl-drag · wheel zoom · Shift-drag pan.\n'
                            'Upstairs / Downstairs are explicit floor transfers; the central staircase is also walkable. '
                            'Click Reset view to leave dog-follow or recover your view.\n')
