"""SUAREZ Lavender & Rose Dream House. Run: python main.py.

True VPython geometry: boxes, spheres, cylinders, cones, curves, triangles.
Controls: arrow keys to walk, mouse to look; right-drag / Ctrl-drag
uses VPython's native camera rotation as an alternative.
"""
from math import pi
from vpython import canvas, vec, rate, distant_light
from architecture import front_shell, furniture
from grounds import world_ground, pool_and_gazebo, observatory
from navigation import FirstPerson


def main():
    scene=canvas(
        title='<b>SUAREZ DREAM HOUSE</b> | Lavender & Rose',
        width=1160, height=690,
        background=vec(.77,.77,.94),
        center=vec(0,2,0), forward=vec(0,0,-1),
    )
    scene.caption=(
        '<b>Explore:</b> Arrow keys = walk &nbsp; | &nbsp; '
        'Move mouse = look around &nbsp; | &nbsp; '
        'Right-drag or Ctrl-drag = alternative rotation. '
        'Click inside the 3D view first.\n'
    )
    scene.autoscale=False
    # Native rotation is left ON on purpose: if the browser does not pass
    # pageX/pageY for mousemove, right-drag still changes the view.
    scene.userspin=True
    scene.userzoom=False
    scene.userpan=False
    scene.fov=pi/2.6
    scene.lights=[]
    scene.ambient=vec(.49,.46,.56)
    distant_light(direction=vec(.46,.84,.32),color=vec(.80,.73,.72))
    distant_light(direction=vec(-.64,.23,-.38),color=vec(.25,.22,.36))

    world_ground()
    front_shell()
    furniture()
    pool_and_gazebo()
    observatory()

    player=FirstPerson(scene)
    while True:
        rate(55)
        player.step()


if __name__=='__main__':
    main()
