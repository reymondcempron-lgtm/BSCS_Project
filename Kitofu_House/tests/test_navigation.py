"""Focused site, wall-opening, stair and tour-route regression checks."""
import math
import unittest
from house import config as C
from house.navigation import Obstacle, dog_route, floor_at, can_walk, NODES, EDGES, STOPS, route


class NavigationTests(unittest.TestCase):
    def test_backyard_order_and_clearances(self):
        px,pz,pw,pd=C.POOL
        gx,gz,gw,gd=C.PAVILION
        self.assertGreater(pz-pd/2,C.HOUSE_REAR+3.4)
        self.assertGreater(gz-gd/2,C.HOUSE_REAR+3.4)
        self.assertLess(gx+gw/2,px-pw/2)
        self.assertLess(pz+pd/2,C.LOT_DEPTH/2)

    def test_entire_dog_loop_and_butterfly_are_safe(self):
        lo,hi,front,rear=C.LAWN
        for i in range(2000):
            for t in (i*.1,i*.1+1.3):
                x,z=dog_route(t)
                self.assertTrue(lo+.6<x<hi-.6 and front+.6<z<rear-.6)
                self.assertGreater(x,-12.5)
                self.assertLess(z,C.HOUSE_FRONT-2)

    def test_stair_is_continuous_and_no_sideways_fall(self):
        floor=0
        for i in range(721):
            floor=floor_at(1.5,5+i*.01,floor)
            self.assertAlmostEqual(floor,C.FLOOR_HEIGHT*i/720,places=5)
        self.assertEqual(floor_at(1.5,12.4,floor),C.FLOOR_HEIGHT)
        self.assertIsNone(floor_at(5,8,1.5))
        self.assertIsNone(floor_at(13,8,C.FLOOR_HEIGHT))
        self.assertIsNone(can_walk(1.5,8,C.FLOOR_HEIGHT,[]))
        self.assertIsNone(can_walk(1.5,8,0,[]))

    def test_wall_and_furniture_collisions(self):
        wall=Obstacle(0,0,.24,5,0,3.6)
        self.assertIsNone(can_walk(.2,0,0,[wall]))
        self.assertEqual(can_walk(.5,0,0,[wall]),0)
        self.assertEqual(can_walk(.2,0,3.6,[wall]),3.6)

    def test_dining_void_has_no_upstairs_floor(self):
        self.assertIsNone(floor_at(8,0,C.FLOOR_HEIGHT))
        self.assertIsNone(can_walk(8,0,C.FLOOR_HEIGHT,[]))
        self.assertEqual(floor_at(8,0,0),0)
        self.assertEqual(floor_at(4,0,C.FLOOR_HEIGHT),C.FLOOR_HEIGHT)
        self.assertEqual(floor_at(8,4,C.FLOOR_HEIGHT),C.FLOOR_HEIGHT)

    def test_every_tour_destination_is_connected(self):
        for _,a in STOPS:
            for _,b in STOPS:
                for node in route(a,b): self.assertIn(node,NODES)

    def test_routes_clear_actual_house_walls_and_furniture(self):
        # Use the real wall splitting algorithm, recording boxes without a canvas.
        from house.geometry import Builder
        from house import architecture, interiors, vehicles
        class Recorder(Builder):
            def box(self,pos,size,material='ivory',solid=False,**kw):
                if solid:
                    x,y,z=pos; w,h,d=size
                    self.obstacles.append(Obstacle(x,z,w,d,y-h/2,y+h/2))
            def rod(self,*a,**kw): pass
            def ellipsoid(self,*a,**kw): pass
        b=Recorder(); architecture.build(b); interiors.build(b); vehicles.build(b)
        for a,c in EDGES:
            p,q=NODES[a],NODES[c]
            for i in range(101):
                t=i/100
                x,y,z=(p[j]+(q[j]-p[j])*t for j in range(3))
                hits=[o for o in b.obstacles if o.blocks(x,z,y)]
                self.assertFalse(hits,f'{a} -> {c}, t={t}: {hits}')


if __name__=='__main__': unittest.main()
