import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

# Unit-test movement direction without depending on VPython import or browser.
from geometry import look_vector

def test_forward_is_toward_house():
    x,y,z=look_vector(0,0)
    assert (x,z)==(0,-1)

def test_turn_view_right():
    x,y,z=look_vector(math.pi/2,0)
    assert x>.99 and abs(z)<.001

def test_mouse_look_pitch_positive_points_up():
    assert look_vector(0,.5)[1]>0
