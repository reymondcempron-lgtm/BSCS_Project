import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geometry import intersects,slide,stair,look_vector,stair_entrance,within_deck,DECK_Y


def test_main_front_entry_open():
    assert not intersects(0,8)
    assert intersects(4,8)


def test_doors_and_rooms():
    assert not intersects(-4.04,-1.14)  # bedroom door
    assert not intersects(-.7,-1.14)   # bathroom door
    assert not intersects(4.8,-1.14)   # study door
    assert not intersects(-7.55,-8.01) # tower connector opening
    assert intersects(-6,-1.14)


def test_glazed_windows_still_solid_for_walkers():
    assert intersects(-7.2,8)
    assert intersects(11,3.1)


def test_collision_slide():
    x,z=slide(4.0,8.52,0.0,-.18)
    assert z==8.52
    assert x==4.0


def test_pool_and_property_bounds():
    assert intersects(19,-3)
    assert intersects(37,25)
    assert not intersects(0,22)


def test_spiral_stair_ends_at_deck():
    p0,p1=stair(0),stair(1)
    assert math.isclose(p0[0],p1[0],abs_tol=1e-6)
    assert math.isclose(p0[2],p1[2],abs_tol=1e-6)
    assert math.isclose(p1[1],DECK_Y,abs_tol=1e-6)
    assert stair_entrance(p0[0],p0[2])
    assert within_deck(p1[0],p1[2])


def test_camera_vectors():
    assert look_vector(0,0)==(0,0,-1)
    assert math.isclose(look_vector(math.pi/2,0)[0],1)
