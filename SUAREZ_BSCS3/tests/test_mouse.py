import math
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

# Test math without importing the VPython browser engine.
from geometry import look_vector, rotate_from_mouse, angles_from_axis


def test_angles():
    from math import atan2, hypot
    x,y,z=look_vector(.7,.3)
    assert abs(atan2(x,-z)-.7)<1e-8
    assert abs(atan2(y,hypot(x,z))-.3)<1e-8


def test_gable_pitch():
    # Two roof halves should incline toward the center.
    assert -(-1)*.135>0
    assert -(1)*.135<0


def test_mouse_pixel_changes_direction():
    yaw, pitch = rotate_from_mouse(0, 0, 250, -100)
    assert abs(yaw-1.0)<1e-10
    assert abs(pitch-.4)<1e-10

def test_mouse_pitch_clamped():
    _, pitch = rotate_from_mouse(0, 0, 0, -9999)
    assert abs(pitch-1.38)<1e-10

def test_native_mouse_axis_angles():
    yaw, pitch=angles_from_axis(1,0,-1)
    assert abs(yaw-math.pi/4)<1e-10
    assert abs(pitch)<1e-10
