from vpython import *

scene.title = "Elegant Dream House - 3D VPython"
scene.width = 1200
scene.height = 750
scene.background = vector(0.45, 0.75, 0.98)
scene.center = vector(0, 4, 0)
scene.camera.pos = vector(25, 16, 34)
scene.camera.axis = vector(-25, -10, -34)
scene.autoscale = False
scene.range = 24

white = vector(0.95, 0.93, 0.87)
cream = vector(0.83, 0.74, 0.61)
dark = vector(0.12, 0.13, 0.17)
roof_color = vector(0.08, 0.10, 0.16)
glass = vector(0.25, 0.65, 0.82)
gold = vector(0.85, 0.65, 0.25)
wood = vector(0.32, 0.17, 0.09)
grass = vector(0.12, 0.42, 0.13)
metal = vector(0.12, 0.13, 0.16)

box(
    pos=vector(0, -0.35, 0),
    size=vector(48, 0.6, 48),
    color=grass
)

box(
    pos=vector(0, -0.02, 12),
    size=vector(19, 0.12, 12),
    color=vector(0.48, 0.46, 0.43)
)

for z in range(8, 17, 2):
    box(
        pos=vector(0, 0.08, z),
        size=vector(2.2, 0.12, 1.5),
        color=white
    )

box(
    pos=vector(13, 0.15, 3),
    size=vector(8, 0.35, 10),
    color=white
)

box(
    pos=vector(13, 0.35, 3),
    size=vector(7.5, 0.08, 9.5),
    color=vector(0.05, 0.55, 0.9),
    opacity=0.85
)

for i in range(4):
    box(
        pos=vector(9.3 + i * 0.3, 0.2 + i * 0.08, 6),
        size=vector(1, 0.12, 2),
        color=white
    )

box(
    pos=vector(0, 0.25, 0),
    size=vector(20, 0.5, 14),
    color=cream
)

box(
    pos=vector(0, 1.9, 0),
    size=vector(18, 3.2, 12),
    color=white
)

box(
    pos=vector(0, 3.45, 6.08),
    size=vector(18, 0.25, 0.2),
    color=cream
)

box(
    pos=vector(-5.5, 1.65, 6.13),
    size=vector(6, 2.6, 0.12),
    color=dark
)

box(
    pos=vector(-5.5, 3.05, 6.25),
    size=vector(6.4, 0.18, 0.25),
    color=wood
)

for x in [-8.65, -2.35]:
    box(
        pos=vector(x, 1.7, 6.25),
        size=vector(0.18, 2.7, 0.25),
        color=cream
    )

for y in [0.65, 1.05, 1.45, 1.85, 2.25, 2.65]:
    box(
        pos=vector(-5.5, y, 6.23),
        size=vector(5.9, 0.035, 0.04),
        color=vector(0.3, 0.3, 0.3)
    )

def make_window(x, y, width, height, z):

    box(
        pos=vector(x, y, z),
        size=vector(width, height, 0.12),
        color=glass,
        opacity=0.65
    )

    for side in [-1, 1]:
        box(
            pos=vector(x + side * width / 2, y, z + 0.1),
            size=vector(0.12, height + 0.15, 0.12),
            color=dark
        )

    box(
        pos=vector(x, y + height / 2, z + 0.1),
        size=vector(width + 0.12, 0.12, 0.12),
        color=dark
    )

    box(
        pos=vector(x, y - height / 2, z + 0.1),
        size=vector(width + 0.12, 0.12, 0.12),
        color=dark
    )

    box(
        pos=vector(x, y, z + 0.16),
        size=vector(0.07, height, 0.08),
        color=dark
    )

make_window(2.8, 1.9, 2.8, 2.2, 6.2)
make_window(7, 1.9, 2.4, 2.2, 6.2)

box(
    pos=vector(-0.4, 1.55, 6.3),
    size=vector(1.7, 2.7, 0.2),
    color=wood
)

box(
    pos=vector(-0.4, 1.55, 6.43),
    size=vector(1.35, 2.3, 0.04),
    color=vector(0.4, 0.23, 0.12)
)

sphere(
    pos=vector(0.2, 1.6, 6.52),
    radius=0.09,
    color=gold
)

for x in [-1.7, 1]:
    box(
        pos=vector(x, 1.8, 6.35),
        size=vector(0.25, 3.4, 0.3),
        color=white
    )

box(
    pos=vector(-0.35, 3.65, 6.5),
    size=vector(4.2, 0.3, 1.2),
    color=cream
)

box(
    pos=vector(0, 5.1, 0),
    size=vector(18, 3.1, 12),
    color=cream
)

make_window(-6.3, 5.1, 3.2, 2.2, 6.12)
make_window(6.3, 5.1, 3.2, 2.2, 6.12)

box(
    pos=vector(0, 5.25, 6.15),
    size=vector(3.5, 2.5, 0.12),
    color=glass,
    opacity=0.55
)

for x in [-1.8, 1.8]:
    box(
        pos=vector(x, 5.25, 6.3),
        size=vector(0.14, 2.8, 0.15),
        color=dark
    )

box(
    pos=vector(0, 3.9, 6.3),
    size=vector(3.7, 0.15, 0.15),
    color=dark
)

arch_points = []

for i in range(31):
    angle = pi * i / 30

    arch_points.append(
        vector(
            1.8 * cos(angle),
            6.35 + 1.1 * sin(angle),
            6.3
        )
    )

curve(
    pos=arch_points,
    radius=0.09,
    color=dark
)

for x in [-0.9, 0, 0.9]:
    box(
        pos=vector(x, 5.25, 6.38),
        size=vector(0.07, 2.5, 0.08),
        color=dark
    )

box(
    pos=vector(0, 5.5, 6.38),
    size=vector(3.4, 0.07, 0.08),
    color=dark
)

box(
    pos=vector(0, 3.65, 7.4),
    size=vector(14, 0.25, 2.3),
    color=white
)

for x in range(-7, 8):
    cylinder(
        pos=vector(x, 3.8, 8.5),
        axis=vector(0, 1, 0),
        radius=0.045,
        color=metal
    )

for y in [3.9, 4.8]:
    cylinder(
        pos=vector(-7, y, 8.5),
        axis=vector(14, 0, 0),
        radius=0.055,
        color=metal
    )

for x in [-7, 7]:
    for z in [7, 8]:
        cylinder(
            pos=vector(x, 3.8, z),
            axis=vector(0, 1, 0),
            radius=0.045,
            color=metal
        )

def roof_triangle(p1, p2, p3):
    triangle(
        vs=[
            vertex(pos=p1, color=roof_color),
            vertex(pos=p2, color=roof_color),
            vertex(pos=p3, color=roof_color)
        ]
    )

front_left = vector(-9, 6.85, 6.5)
front_right = vector(9, 6.85, 6.5)
back_left = vector(-9, 6.85, -6.5)
back_right = vector(9, 6.85, -6.5)

ridge_left = vector(-4.5, 9.2, 0)
ridge_right = vector(4.5, 9.2, 0)

roof_triangle(front_left, front_right, ridge_left)
roof_triangle(front_right, ridge_right, ridge_left)

roof_triangle(back_left, ridge_left, ridge_right)
roof_triangle(back_right, ridge_right, ridge_left)

roof_triangle(front_left, ridge_left, back_left)

roof_triangle(front_right, back_right, ridge_right)

box(
    pos=vector(0, 6.85, 6.55),
    size=vector(19, 0.22, 0.3),
    color=dark
)

def make_car(x, z, car_color):

    box(
        pos=vector(x, 0.65, z),
        size=vector(2.2, 0.65, 4),
        color=car_color
    )

    box(
        pos=vector(x, 1.12, z - 0.2),
        size=vector(1.7, 0.65, 2.2),
        color=car_color
    )

    box(
        pos=vector(x, 1.3, z + 0.85),
        size=vector(1.5, 0.42, 0.08),
        color=glass,
        opacity=0.7
    )

    box(
        pos=vector(x, 1.3, z - 1.3),
        size=vector(1.5, 0.42, 0.08),
        color=glass,
        opacity=0.7
    )

    for wx in [-1.05, 1.05]:
        for wz in [-1.3, 1.3]:
            cylinder(
                pos=vector(x + wx, 0.45, z + wz),
                axis=vector(0.18, 0, 0),
                radius=0.38,
                color=dark
            )

    for wx in [-0.7, 0.7]:
        box(
            pos=vector(x + wx, 0.75, z + 2.03),
            size=vector(0.4, 0.18, 0.08),
            color=color.yellow,
            emissive=True
        )

make_car(-6.5, 10.5, vector(0.85, 0.85, 0.88))
make_car(-3.5, 10.5, vector(0.08, 0.08, 0.10))

for x in [-10, 10]:

    box(
        pos=vector(x, 1.5, 17),
        size=vector(0.9, 3, 0.9),
        color=cream
    )

    box(
        pos=vector(x, 3.1, 17),
        size=vector(1.2, 0.25, 1.2),
        color=white
    )

    box(
        pos=vector(x, 3.35, 17),
        size=vector(0.4, 0.25, 0.4),
        color=gold,
        emissive=True
    )

for x in [-11.2, 11.2]:
    box(
        pos=vector(x, 0.9, 17),
        size=vector(1.8, 1.8, 0.6),
        color=white
    )

for x in [-9, 9]:
    box(
        pos=vector(x, 1.3, 16.55),
        size=vector(0.18, 2.4, 0.15),
        color=metal
    )

for x in range(-8, 9):
    box(
        pos=vector(x, 1.3, 16.55),
        size=vector(0.07, 2.2, 0.12),
        color=metal
    )

for y in [0.3, 1.3, 2.4]:
    box(
        pos=vector(0, y, 16.55),
        size=vector(18, 0.12, 0.15),
        color=metal
    )

for x in range(-8, 9, 2):
    sphere(
        pos=vector(x, 2.55, 16.55),
        radius=0.09,
        color=gold
    )

box(
    pos=vector(0, 1.3, 16.4),
    size=vector(0.12, 2.4, 0.2),
    color=gold
)

cylinder(
    pos=vector(0, 0.2, -11),
    axis=vector(0, 0.35, 0),
    radius=2,
    color=white
)

cylinder(
    pos=vector(0, 0.45, -11),
    axis=vector(0, 0.08, 0),
    radius=1.7,
    color=glass,
    opacity=0.75
)

cylinder(
    pos=vector(0, 0.5, -11),
    axis=vector(0, 1.2, 0),
    radius=0.25,
    color=white
)

sphere(
    pos=vector(0, 1.8, -11),
    radius=0.35,
    color=glass
)

def make_tree(x, z, height):

    cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, height, 0),
        radius=0.25,
        color=wood
    )

    for side in [-1, 1]:
        cylinder(
            pos=vector(x, height * 0.55, z),
            axis=vector(side * 0.7, 0.8, 0),
            radius=0.12,
            color=wood
        )

    sphere(
        pos=vector(x, height + 0.6, z),
        radius=1.1,
        color=vector(0.08, 0.35, 0.08)
    )

    sphere(
        pos=vector(x - 0.7, height + 0.3, z),
        radius=0.8,
        color=vector(0.12, 0.45, 0.12)
    )

    sphere(
        pos=vector(x + 0.7, height + 0.3, z),
        radius=0.8,
        color=vector(0.12, 0.42, 0.1)
    )

make_tree(-14, -5, 3.5)
make_tree(15, -7, 3.5)
make_tree(-15, 9, 3)
make_tree(15, 10, 3)

flower_colors = [
    color.red,
    color.yellow,
    vector(1, 0.3, 0.6),
    color.white
]

for x in range(-9, 10, 2):
    for z in [11, 12]:

        sphere(
            pos=vector(x, 0.3, z),
            radius=0.18,
            color=flower_colors[(x + 10) % 4]
        )

        cylinder(
            pos=vector(x, 0, z),
            axis=vector(0, 0.3, 0),
            radius=0.035,
            color=grass
        )

for x, z in [
    (-10, 5), (-11, 2), (-10, -3),
    (10, 5), (11, 0), (10, -4),
    (-8, 15), (8, 15)
]:
    sphere(
        pos=vector(x, 0.6, z),
        radius=0.7,
        color=vector(0.08, 0.35, 0.08)
    )

for x in [-8, -3, 3, 8]:

    cylinder(
        pos=vector(x, 0, 9),
        axis=vector(0, 1.8, 0),
        radius=0.07,
        color=dark
    )

    sphere(
        pos=vector(x, 1.9, 9),
        radius=0.18,
        color=gold,
        emissive=True
    )

sun = sphere(
    pos=vector(-17, 16, -5),
    radius=1.6,
    color=vector(1, 0.85, 0.1),
    emissive=True
)

for angle in range(0, 360, 45):

    a = angle * pi / 180

    cylinder(
        pos=vector(
            -17 + 2.1 * cos(a),
            16 + 2.1 * sin(a),
            -5
        ),
        axis=vector(
            0.55 * cos(a),
            0.55 * sin(a),
            0
        ),
        radius=0.07,
        color=color.yellow,
        emissive=True
    )

def make_cloud(x, y, z, scale):

    cloud_color = vector(1, 1, 1)

    ellipsoid(
        pos=vector(x, y, z),
        size=vector(3.0 * scale, 1.2 * scale, 1.2 * scale),
        color=cloud_color
    )

    ellipsoid(
        pos=vector(x - 1.1 * scale, y + 0.2 * scale, z),
        size=vector(2.1 * scale, 1.4 * scale, 1.2 * scale),
        color=cloud_color
    )

    ellipsoid(
        pos=vector(x + 1.1 * scale, y + 0.3 * scale, z),
        size=vector(2.2 * scale, 1.4 * scale, 1.2 * scale),
        color=cloud_color
    )

    ellipsoid(
        pos=vector(x, y + 0.65 * scale, z),
        size=vector(2.0 * scale, 1.3 * scale, 1.1 * scale),
        color=cloud_color
    )

make_cloud(-20, 14, -3, 1.5)
make_cloud(-8, 18, -10, 1.2)
make_cloud(7, 16, -9, 1.4)
make_cloud(20, 17, -2, 1.5)
make_cloud(14, 13, -15, 1.0)

scene.center = vector(0, 5, 0)
scene.camera.pos = vector(25, 16, 34)
scene.camera.axis = scene.center - scene.camera.pos

print("Elegant Dream House successfully created!")
print("Features: Gate, Swimming Pool, Fountain, Cars, Sun and Clouds.")
print("Keep this terminal open while viewing the 3D house.")

while True:
    rate(30)