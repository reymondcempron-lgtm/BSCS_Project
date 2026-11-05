"""Camera ownership and time-based tour progression without a graphical canvas."""
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import vpython as v
from house.cameras import Cameras, ROOM_VIEWS
from house.navigation import STOPS


class CameraTests(unittest.TestCase):
    def setUp(self):
        self.scene=SimpleNamespace(camera=SimpleNamespace(pos=v.vector(0,0,0),axis=v.vector(0,0,1)),
                                   bind=lambda *args:None)
        self.dog=SimpleNamespace(pos=v.vector(0,0,-19),heading=v.vector(1,0,0))
        self.camera=Cameras(self.scene,[],self.dog)

    def test_all_mode_transitions_clear_input_and_routes(self):
        c=self.camera
        for action in (c.begin,c.explore,c.follow,lambda:c.floor_transfer(True),c.overview,
                       lambda:c.room('Master Suite')):
            c.keys.add('w'); c.queue=['old']; c.target_node='old'
            action()
            self.assertEqual(c.keys,set())
            self.assertNotIn('old',c.queue)
            self.assertNotEqual(c.target_node,'old')

    def test_tour_visits_every_stop_and_finishes_paused(self):
        c=self.camera; c.begin(); visited=set()
        for _ in range(20000):
            c.update(.025)
            if c.dwell>0: visited.add(c.stop)
            if c.pause: break
        self.assertEqual(visited,set(range(len(STOPS))))
        self.assertTrue(c.pause)
        self.assertEqual(c.node,'lawn')

    def test_pause_and_mid_segment_retarget(self):
        c=self.camera; c.begin(1); c.update(.05)
        c.pause=True; old=v.vector(self.scene.camera.pos)
        c.update(.05); self.assertEqual(old,self.scene.camera.pos)
        c.travel(3)
        self.assertEqual(c.queue[0],'front')
        self.assertFalse(c.pause)

    def test_walk_speed_is_frame_rate_independent(self):
        def move(dt):
            c=self.camera; c.explore(); c.keys.add('w')
            with patch('vpython.keysdown',return_value=['w']):
                for _ in range(round(1/dt)): c.update(dt)
            return v.vector(self.scene.camera.pos)
        a,b=move(.025),move(.05)
        self.assertLess(v.mag(a-b),1e-9)
        self.assertAlmostEqual(a.z,-5)

    def test_follow_exit_stops_camera_overwrites(self):
        c=self.camera; c.follow(); c.update(.025)
        c.overview(immediate=True); position=v.vector(self.scene.camera.pos)
        self.dog.pos=v.vector(4,0,-20); c.update(.025)
        self.assertEqual(position,self.scene.camera.pos)

    def test_room_buttons_release_camera_and_set_room_pivot(self):
        c=self.camera; applied=[]; c.cutaway=applied.append
        for name,(eye,pivot,cut) in ROOM_VIEWS.items():
            c.begin(); c.update(.05); c.room(name)
            self.assertEqual(c.mode,'Room view')
            self.assertTrue(self.scene.userspin and self.scene.userzoom and self.scene.userpan)
            self.assertEqual(self.scene.camera.pos,v.vector(*eye))
            self.assertEqual(self.scene.center,v.vector(*pivot))
            self.assertEqual(applied[-1],cut)
            # Simulate a native mouse orbit; updates must preserve the user's view.
            pos=v.vector(2,6,3); axis=v.vector(-1,-.4,2)
            self.scene.camera.pos=pos; self.scene.camera.axis=axis
            for _ in range(10): c.update(.05)
            self.assertEqual(self.scene.camera.pos,pos)
            self.assertEqual(self.scene.camera.axis,axis)

    def test_leaving_room_restores_exterior_and_camera_owner(self):
        c=self.camera; applied=[]; c.cutaway=applied.append
        for action in (c.begin,c.explore,c.follow,c.overview):
            c.room('Master Suite'); action()
            self.assertEqual(applied[-1],'Full exterior')
            self.assertNotEqual(c.mode,'Room view')

    def test_every_space_button_opens_its_own_room(self):
        from house import controls
        buttons=[]
        scene=self.scene; scene.append_to_caption=lambda _:None
        def button(**kw):
            obj=SimpleNamespace(**kw); buttons.append(obj); return obj
        def menu(**kw):
            return SimpleNamespace(**kw,selected=kw['choices'][0],index=0)
        builder=SimpleNamespace(cutaway=lambda _:None)
        with patch('vpython.button',side_effect=button), patch('vpython.menu',side_effect=menu), \
             patch('vpython.wtext',return_value=SimpleNamespace(text='')):
            controls.build(scene,self.camera,builder,self.dog,[],None,None)
        for name in ROOM_VIEWS:
            widget=next(b for b in buttons if b.text==name)
            widget.bind(widget)
            self.assertTrue(self.camera.location.startswith(name+' ·'))


if __name__=='__main__': unittest.main()
