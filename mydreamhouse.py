
from vpython import *


scene = canvas(
    title="",
    width=1100,
    height=750,
    background=vector(0.55, 0.70, 0.82)
)

scene.center = vector(0, 4, 0)
scene.camera.pos = vector(0, 9, -27)
scene.camera.axis = vector(0, -3, 27)
scene.range = 16


white = vector(0.92, 0.92, 0.88)
gray = vector(0.48, 0.52, 0.56)
black = vector(0.08, 0.09, 0.12)
glass = vector(0.38, 0.61, 0.72)
wood = vector(0.30, 0.16, 0.08)
gold = vector(1, 0.72, 0.32)
green = vector(0.10, 0.32, 0.12)


box(pos=vector(0,-0.3,0),
    size=vector(35,0.5,35),
    color=vector(0.20,0.32,0.16))


box(pos=vector(0,-0.02,-13),
    size=vector(35,0.12,5),
    color=vector(0.16,0.18,0.23))


box(pos=vector(4,0.03,-8),
    size=vector(8,0.12,5),
    color=vector(0.65,0.65,0.62))



box(pos=vector(0,1.9,0),
    size=vector(12,3.8,8),
    color=white)


for x in [-5.8,5.8]:
    box(pos=vector(x,1.9,-4.08),
        size=vector(0.3,3.7,0.15),
        color=gray)


box(pos=vector(-2.8,1.5,-4.12),
    size=vector(2.4,3,0.18),
    color=wood)

for x in [-3.35,-2.25]:
    box(pos=vector(x,1.5,-4.23),
        size=vector(0.85,2.65,0.04),
        color=glass,
        opacity=0.65)


box(pos=vector(-2.8,1.5,-4.27),
    size=vector(0.08,2.7,0.06),
    color=black)


for x in [-2.9,-2.65]:
    sphere(pos=vector(x,1.5,-4.32),
           radius=0.06,color=gold)


box(pos=vector(3,1.9,-4.12),
    size=vector(4,2.5,0.15),
    color=black)

box(pos=vector(3,1.9,-4.22),
    size=vector(3.75,2.25,0.04),
    color=glass,opacity=0.45)

for x in [1.7,3,4.3]:
    box(pos=vector(x,1.9,-4.26),
        size=vector(0.07,2.25,0.05),
        color=black)

box(pos=vector(3,1.9,-4.26),
    size=vector(3.75,0.07,0.05),
    color=black)



box(pos=vector(0,5.5,0),
    size=vector(12,3.4,8),
    color=white)


box(pos=vector(-3,5.45,-4.1),
    size=vector(2.8,2.7,0.14),
    color=black)

box(pos=vector(-3,5.45,-4.2),
    size=vector(2.55,2.45,0.04),
    color=glass,opacity=0.55)


box(pos=vector(3,5.45,-4.1),
    size=vector(2.8,2.7,0.14),
    color=black)

box(pos=vector(3,5.45,-4.2),
    size=vector(2.55,2.45,0.04),
    color=glass,opacity=0.55)


for x in [-3,3]:
    box(pos=vector(x,5.45,-4.26),
        size=vector(0.07,2.45,0.04),
        color=black)



black = vector(0.04, 0.04, 0.05)


box(
    pos=vector(0, 3.85, -5.1),
    size=vector(12.8, 0.3, 2.5),
    color=gray
)

for y in [4.15, 4.42, 4.69, 4.96]:
    box(
        pos=vector(0, y, -6.3),
        size=vector(12.2, 0.07, 0.07),
        color=black
    )


for x in range(-6, 7):
    box(
        pos=vector(x, 4.55, -6.3),
        size=vector(0.07, 1.1, 0.07),
        color=black
    )


for y in [4.15, 4.42, 4.69, 4.96]:
    box(
        pos=vector(-6.3, y, -5.1),
        size=vector(0.07, 0.07, 2.4),
        color=black
    )


for y in [4.15, 4.42, 4.69, 4.96]:
    box(
        pos=vector(6.3, y, -5.1),
        size=vector(0.07, 0.07, 2.4),
        color=black
    )


for z in [-6.2, -5.6, -5.0, -4.4, -3.9]:
    box(
        pos=vector(-6.3, 4.55, z),
        size=vector(0.07, 1.1, 0.07),
        color=black
    )


for z in [-6.2, -5.6, -5.0, -4.4, -3.9]:
    box(
        pos=vector(6.3, 4.55, z),
        size=vector(0.07, 1.1, 0.07),
        color=black
    )



def roof_triangle(a,b,c):
    triangle(
        v0=vertex(pos=vector(*a),color=black),
        v1=vertex(pos=vector(*b),color=black),
        v2=vertex(pos=vector(*c),color=black)
    )


ridge_left = (-3.5,8.5,0)
ridge_right = (3.5,8.5,0)

front_left = (-7,7,-5)
front_right = (7,7,-5)
back_left = (-7,7,5)
back_right = (7,7,5)


roof_triangle(ridge_left,ridge_right,front_left)
roof_triangle(ridge_right,front_right,front_left)


roof_triangle(ridge_left,ridge_right,back_left)
roof_triangle(ridge_right,back_right,back_left)


roof_triangle(ridge_left,front_left,back_left)


roof_triangle(ridge_right,front_right,back_right)


cylinder(pos=vector(-3.5,8.5,0),
         axis=vector(7,0,0),
         radius=0.09,color=black)



for x in [-5,-0.2,5]:
    box(pos=vector(x,2.3,-4.2),
        size=vector(0.3,0.55,0.12),
        color=gold)

    sphere(pos=vector(x,2.3,-4.3),
           radius=0.15,
           color=gold,
           emissive=True)



def plant(x,z):
    cylinder(pos=vector(x,0,z),
             axis=vector(0,0.8,0),
             radius=0.08,
             color=wood)

    for y in [0.9,1.25,1.5]:
        cone(pos=vector(x,y,z),
             axis=vector(0,0.8,0),
             radius=0.55-(y-0.9)*0.35,
             color=green)

for x in [-8,-6.5,-5.5,5.5,7,8]:
    plant(x,-5)


for x in [-7,-5.5,5.5,7]:
    sphere(pos=vector(x,0.35,-6),
           radius=0.4,
           color=green)



silver = vector(0.68, 0.72, 0.78)
dark = vector(0.025, 0.03, 0.04)
black = vector(0.01, 0.01, 0.01)
glass = vector(0.08, 0.15, 0.20)
chrome = vector(0.8, 0.82, 0.85)
red = vector(0.8, 0.02, 0.02)
white = vector(1, 1, 1)


cx = 4.0
cz = -8.0


silver = vector(0.65, 0.68, 0.72)
dark = vector(0.08, 0.09, 0.10)
chrome = vector(0.75, 0.78, 0.82)
glass = vector(0.08, 0.18, 0.23)
white = vector(1, 1, 1)
black = vector(0.02, 0.02, 0.02)
red = vector(0.8, 0.02, 0.02)


truck_parts = []


def P(x, y, z):
    return vector(cx + x, y, cz + z)


def TB(pos, size, color, **kwargs):
    obj = box(pos=pos, size=size, color=color, **kwargs)
    truck_parts.append(obj)
    return obj

def TC(pos, axis, radius, color):
    obj = cylinder(
        pos=pos,
        axis=axis,
        radius=radius,
        color=color
    )
    truck_parts.append(obj)
    return obj

def TS(pos, radius, color, **kwargs):
    obj = sphere(
        pos=pos,
        radius=radius,
        color=color,
        **kwargs
    )
    truck_parts.append(obj)
    return obj



TB(P(0, 0.85, 0),
   vector(2.35, 0.65, 4.9), silver)

# Lower chassis
TB(P(0, 0.48, 0),
   vector(2.15, 0.22, 4.65), dark)



TB(P(0, 1.12, -1.75),
   vector(2.3, 0.35, 1.25), silver)


TB(P(0, 0.65, -2.52),
   vector(2.45, 0.28, 0.22), chrome)

TB(P(0, 0.49, -2.62),
   vector(2.35, 0.13, 0.12), dark)


TB(P(0, 0.91, -2.54),
   vector(1.12, 0.42, 0.08), dark)

for y in [0.80, 0.90, 1.00]:
    TB(P(0, y, -2.60),
       vector(0.95, 0.025, 0.025), chrome)


TS(P(0, 0.94, -2.64), 0.11, chrome)



for x in [-0.87, 0.87]:

    TB(P(x, 1.08, -2.55),
       vector(0.48, 0.25, 0.08), dark)

    TB(P(x, 1.10, -2.61),
       vector(0.38, 0.08, 0.035),
       white, emissive=True)



TB(P(0, 1.65, -0.35),
   vector(2.18, 1.35, 2.05), silver)


TB(P(0, 2.34, -0.35),
   vector(2.20, 0.16, 2.05), silver)


TB(P(0, 1.83, -1.39),
   vector(1.92, 0.85, 0.055),
   glass, opacity=0.8)


TB(P(0, 1.82, 0.68),
   vector(1.75, 0.75, 0.055),
   glass, opacity=0.8)


for x in [-1.105, 1.105]:

    TB(P(x, 1.92, -0.35),
       vector(0.045, 0.70, 1.65),
       glass, opacity=0.8)


TB(P(0, 1.02, 1.50),
   vector(2.15, 0.12, 1.65), dark)


TB(P(-1.05, 1.40, 1.50),
   vector(0.13, 0.65, 1.75), silver)


TB(P(1.05, 1.40, 1.50),
   vector(0.13, 0.65, 1.75), silver)


TB(P(0, 1.38, 2.37),
   vector(2.15, 0.65, 0.13), silver)


TB(P(0, 1.10, 1.50),
   vector(1.85, 0.06, 1.40),
   vector(0.12, 0.13, 0.14))



for x in [-1.18, 1.18]:

    for z in [-1.45, 1.60]:

        
        TC(P(x - 0.13, 0.55, z),
           vector(0.26, 0, 0), 0.48, black)

        
        TC(P(x - 0.145, 0.55, z),
           vector(0.29, 0, 0), 0.29, chrome)


        TC(P(x - 0.16, 0.55, z),
           vector(0.32, 0, 0), 0.12, dark)

    
        TC(P(x - 0.17, 0.55, z),
           vector(0.34, 0, 0), 0.055, chrome)



for x in [-1.25, 1.25]:

    TB(P(x, 1.92, -1.20),
       vector(0.30, 0.17, 0.30), dark)




for x in [-1.20, 1.20]:

    TB(P(x, 0.43, -0.10),
       vector(0.15, 0.12, 1.35), dark)



for x in [-0.92, 0.92]:

    TB(P(x, 1.35, 2.45),
       vector(0.22, 0.43, 0.08), red)



for x in [-0.95, 0.95]:

    TS(P(x, 0.65, -2.63),
       0.09, white, emissive=True)


truck = compound(truck_parts)



truck.rotate(
    angle=pi/2,
    axis=vector(0, 1, 0),
    origin=truck.pos
)


truck.pos += vector(0.8, 0, 0)



wall_color = vector(0.78, 0.78, 0.75)
stone_color = vector(0.22, 0.23, 0.24)
gate_color = vector(0.035, 0.04, 0.05)
light_color = vector(1, 0.72, 0.30)


fence_height = 2.5
fence_thickness = 0.35


box(
    pos=vector(-11.5, 1.25, 0.5),
    size=vector(fence_thickness, fence_height, 22),
    color=wall_color
)


box(
    pos=vector(11.5, 1.25, 0.5),
    size=vector(fence_thickness, fence_height, 22),
    color=wall_color
)


box(
    pos=vector(0, 1.25, 11.5),
    size=vector(23, fence_height, fence_thickness),
    color=wall_color
)


box(
    pos=vector(-8.5, 1.25, -10.5),
    size=vector(6, fence_height, fence_thickness),
    color=wall_color
)


box(
    pos=vector(8.5, 1.25, -10.5),
    size=vector(6, fence_height, fence_thickness),
    color=wall_color
)


for x in [-9, 9]:
    box(
        pos=vector(x, 1.15, -10.72),
        size=vector(2.2, 1.5, 0.08),
        color=stone_color
    )


post_positions = [-11.5, -5.5, 5.5, 11.5]

for x in post_positions:
    box(
        pos=vector(x, 1.5, -10.5),
        size=vector(0.65, 3, 0.65),
        color=gray
    )

    
    box(
        pos=vector(x, 3.05, -10.5),
        size=vector(0.85, 0.18, 0.85),
        color=wall_color
    )


box(
    pos=vector(-2.65, 1.25, -10.5),
    size=vector(5.25, 2.1, 0.16),
    color=gate_color
)


box(
    pos=vector(2.65, 1.25, -10.5),
    size=vector(5.25, 2.1, 0.16),
    color=gate_color
)


for y in [0.4, 0.7, 1.0, 1.3, 1.6, 1.9, 2.2]:
    
    box(
        pos=vector(-2.65, y, -10.62),
        size=vector(5.1, 0.055, 0.06),
        color=black
    )

    box(
        pos=vector(2.65, y, -10.62),
        size=vector(5.1, 0.055, 0.06),
        color=black
    )


for x in [-5.2, 0, 5.2]:
    box(
        pos=vector(x, 1.25, -10.65),
        size=vector(0.12, 2.1, 0.08),
        color=gray
    )


for x in [-0.18, 0.18]:
    box(
        pos=vector(x, 1.25, -10.75),
        size=vector(0.07, 0.4, 0.08),
        color=light_color
    )


for x in [-11.5, -9, -7, -5.5,
           5.5, 7, 9, 11.5]:

    box(
        pos=vector(x, 1.65, -10.75),
        size=vector(0.18, 0.55, 0.12),
        color=light_color
    )

    sphere(
        pos=vector(x, 1.65, -10.85),
        radius=0.12,
        color=light_color,
        emissive=True
    )


for x in [-5.5, 5.5]:
    box(
        pos=vector(x, 3.25, -10.5),
        size=vector(0.35, 0.12, 0.35),
        color=light_color,
        emissive=True
    )



for x in [-8.5, 8.5]:
    box(
        pos=vector(x, 2.55, -10.5),
        size=vector(6.1, 0.12, 0.5),
        color=gray
    )


for x in [-11.5, 11.5]:
    box(
        pos=vector(x, 2.55, 0.5),
        size=vector(0.5, 0.12, 22.2),
        color=gray
    )


box(
    pos=vector(0, 2.55, 11.5),
    size=vector(23.2, 0.12, 0.5),
    color=gray
)


for x in [-2,0,2]:
    box(pos=vector(x,0.08,-8),
        size=vector(1.4,0.12,1),
        color=white)


while True:
    rate(30)
