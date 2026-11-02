from vpython import *

scene = canvas(
    title='3D Dream House with Multiple Chickens and Chicks',
    width=1000, 
    height=700, 
    center=vector(0, 2, 0), 
    background=color.cyan
)

cam_angle = 0
cam_distance = 35

def update_camera():
    global cam_angle, cam_distance
    x = cam_distance * sin(cam_angle)
    z = cam_distance * cos(cam_angle)
    scene.camera.pos = vector(x, 12, z)
    scene.camera.axis = vector(0, 2, 0) - scene.camera.pos

update_camera()

def handle_keydown(evt):
    global cam_angle
    k = evt.key
    if k == 'left' or k == 'a':
        cam_angle += 0.1
    elif k == 'right' or k == 'd':
        cam_angle -= 0.1
    update_camera()

scene.bind('keydown', handle_keydown)

ground = box(pos=vector(0, -0.5, 0), size=vector(50, 1, 50), color=vector(0.3, 0.7, 0.3))
pathway = box(pos=vector(0, 0.01, 7), size=vector(3.5, 0.02, 12), color=vector(0.6, 0.6, 0.6))

walls = box(pos=vector(0, 2.5, 0), size=vector(9, 5, 7), color=color.white)
roof = cone(pos=vector(0, 5.2, 0), axis=vector(0, 3.2, 0), radius=6, color=vector(0.8, 0.2, 0.1))

door = box(pos=vector(0, 1.5, 3.55), size=vector(1.8, 3, 0.1), color=vector(0.4, 0.2, 0.1))
doorknob = sphere(pos=vector(0.6, 1.5, 3.62), radius=0.1, color=color.yellow)

win_left = box(pos=vector(-2.8, 3, 3.55), size=vector(1.6, 1.6, 0.1), color=color.cyan)
win_right = box(pos=vector(2.8, 3, 3.55), size=vector(1.6, 1.6, 0.1), color=color.cyan)
win_frame_l = box(pos=vector(-2.8, 3, 3.58), size=vector(1.7, 0.1, 0.05), color=color.black)
win_frame_r = box(pos=vector(2.8, 3, 3.58), size=vector(1.7, 0.1, 0.05), color=color.black)

chimney = box(pos=vector(2.8, 5.8, -1), size=vector(1.2, 3.5, 1.2), color=vector(0.5, 0.2, 0.1))

def make_tree(x, z):
    cylinder(pos=vector(x, 0, z), axis=vector(0, 3.5, 0), radius=0.5, color=vector(0.4, 0.25, 0.1))
    cone(pos=vector(x, 3.0, z), axis=vector(0, 3, 0), radius=2.2, color=vector(0.1, 0.5, 0.15))
    cone(pos=vector(x, 4.8, z), axis=vector(0, 2.8, 0), radius=1.6, color=vector(0.15, 0.6, 0.15))

tree_positions = [
    (-13, 9), (9, 5), (12, -1), (8, -6),
    (11, 10), (-6, 11), (7, 11), (-12, -7), (10, -5)
]
for pos in tree_positions:
    make_tree(pos[0], pos[1])

box(pos=vector(-7, 1, 11), size=vector(11, 0.1, 0.2), color=vector(0.5, 0.3, 0.1))
box(pos=vector(-7, 0.5, 11), size=vector(11, 0.1, 0.2), color=vector(0.5, 0.3, 0.1))

box(pos=vector(7, 1, 11), size=vector(11, 0.1, 0.2), color=vector(0.5, 0.3, 0.1))
box(pos=vector(7, 0.5, 11), size=vector(11, 0.1, 0.2), color=vector(0.5, 0.3, 0.1))

for x in range(-12, -1):
    box(pos=vector(x, 0.8, 11), size=vector(0.2, 1.6, 0.1), color=vector(0.6, 0.4, 0.2))
for x in range(2, 13):
    box(pos=vector(x, 0.8, 11), size=vector(0.2, 1.6, 0.1), color=vector(0.6, 0.4, 0.2))

gate_post_l = box(pos=vector(-1.6, 1.2, 11), size=vector(0.4, 2.4, 0.4), color=color.gray(0.3))
gate_post_r = box(pos=vector(1.6, 1.2, 11), size=vector(0.4, 2.4, 0.4), color=color.gray(0.3))

gate_left = box(pos=vector(-0.75, 1, 11), size=vector(1.3, 1.8, 0.08), color=color.black)
gate_right = box(pos=vector(0.75, 1, 11), size=vector(1.3, 1.8, 0.08), color=color.black)

car_body = box(pos=vector(-8, 0.8, 2), size=vector(4, 1.2, 2.2), color=color.blue)
car_top = box(pos=vector(-8, 1.7, 2), size=vector(2.2, 1.0, 2.0), color=color.blue)
wheel_fl = cylinder(pos=vector(-6.8, 0.4, 3.1), axis=vector(0, 0, -0.3), radius=0.4, color=color.black)
wheel_fr = cylinder(pos=vector(-9.2, 0.4, 3.1), axis=vector(0, 0, -0.3), radius=0.4, color=color.black)
wheel_bl = cylinder(pos=vector(-6.8, 0.4, 0.9), axis=vector(0, 0, -0.3), radius=0.4, color=color.black)
wheel_br = cylinder(pos=vector(-9.2, 0.4, 0.9), axis=vector(0, 0, -0.3), radius=0.4, color=color.black)

class WalkingFamily:
    def __init__(self, start_x, start_z, speed, direction):
        self.mother_body = sphere(pos=vector(start_x, 0.25, start_z), size=vector(0.7, 0.5, 0.5), color=color.white)
        self.mother_head = sphere(pos=vector(start_x + 0.25, 0.55, start_z), radius=0.2, color=color.white)
        self.mother_beak = cone(pos=vector(start_x + 0.42, 0.55, start_z), axis=vector(0.15, 0, 0), radius=0.08, color=color.orange)
        self.mother_comb = box(pos=vector(start_x + 0.25, 0.75, start_z), size=vector(0.08, 0.12, 0.04), color=color.red)

        self.chicks = []
        for i in range(3):
            cx = start_x - (0.5 * (i + 1))
            cz = start_z
            c_body = sphere(pos=vector(cx, 0.15, cz), radius=0.18, color=color.yellow)
            c_head = sphere(pos=vector(cx + 0.08, 0.32, cz), radius=0.1, color=color.yellow)
            self.chicks.append([c_body, c_head])

        self.speed = speed
        self.direction = direction

    def move(self):
        mother_parts = [self.mother_body, self.mother_head, self.mother_beak, self.mother_comb]
        for p in mother_parts:
            p.pos.z += self.speed * self.direction

        for i, chick in enumerate(self.chicks):
            offset = 0.5 * (i + 1)
            target_z = self.mother_body.pos.z - (offset * self.direction)
            for part in chick:
                part.pos.z += (target_z - part.pos.z) * 0.1
                part.pos.x = self.mother_body.pos.x - offset if self.direction > 0 else self.mother_body.pos.x + offset

        if self.mother_body.pos.z > 15 or self.mother_body.pos.z > 16:
            self.direction = -1
        elif self.mother_body.pos.z < 12:
            self.direction = 1

chicken_families = [
    WalkingFamily(-2.5, 13.0, 0.02, 1),
    WalkingFamily(2.5, 14.2, 0.025, -1),
    WalkingFamily(0.0, 13.5, 0.015, 1)
]

sun = sphere(pos=vector(-16, 16, -12), radius=3, color=color.yellow, emissive=True)

scene.append_to_caption("\n\n**Controls:**\n- Use **Left / Right Arrow keys** (or **A / D**) to rotate the camera around the house.\n- Multiple mother chickens and yellow chicks are walking outside the gate!")

while True:
    rate(30)
    for fam in chicken_families:
        fam.move()
