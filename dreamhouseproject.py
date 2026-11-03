
from vpython import *

# ==========================================
# MY MODERN LUXURY 3D DREAM HOUSE
# ==========================================

scene.title = "MY MODERN LUXURY DREAM HOUSE"
scene.width = 1100
scene.height = 750
scene.background = vector(0.53, 0.81, 0.96)
scene.center = vector(0, 4, 0)
scene.range = 24
scene.forward = vector(-1, -0.55, -1)

# ==========================================
# COLORS
# ==========================================

white = vector(0.95, 0.94, 0.90)
brown = vector(0.40, 0.23, 0.13)
dark_brown = vector(0.20, 0.11, 0.07)
wood = vector(0.62, 0.38, 0.20)
glass = vector(0.25, 0.70, 0.85)
green = vector(0.12, 0.45, 0.16)
gray = vector(0.45, 0.45, 0.45)

# ==========================================
# 1. GROUND AND DRIVEWAY
# ==========================================

box(
    pos=vector(0, -0.3, 0),
    size=vector(40, 0.5, 40),
    color=green
)

box(
    pos=vector(8, -0.02, -7),
    size=vector(12, 0.1, 8),
    color=gray
)

# ==========================================
# 2. FIRST FLOOR
# ==========================================

# Floor
box(
    pos=vector(0, 0.12, 0),
    size=vector(10, 0.24, 6),
    color=white
)

# Back wall
box(
    pos=vector(0, 2.5, 2.85),
    size=vector(10, 5, 0.3),
    color=white
)

# Side walls
for x in [-4.85, 4.85]:
    box(
        pos=vector(x, 2.5, 0),
        size=vector(0.3, 5, 6),
        color=white
    )

# Front pillars
for x in [-4.7, -1.1, 1.1, 4.7]:
    box(
        pos=vector(x, 2.5, -2.85),
        size=vector(0.3, 5, 0.3),
        color=white
    )

# ==========================================
# 3. FIRST FLOOR WINDOWS
# ==========================================

for x in [-2.9, 2.9]:

    box(
        pos=vector(x, 3, -2.85),
        size=vector(3.1, 2.2, 0.12),
        color=glass
    )

    # Vertical window frame
    box(
        pos=vector(x, 3, -2.95),
        size=vector(0.09, 2.2, 0.08),
        color=white
    )

    # Horizontal window frame
    box(
        pos=vector(x, 3, -2.95),
        size=vector(3.1, 0.09, 0.08),
        color=white
    )

# ==========================================
# 4. FRONT DOOR
# ==========================================

box(
    pos=vector(0, 1.4, -3.0),
    size=vector(1.6, 2.8, 0.2),
    color=dark_brown
)

box(
    pos=vector(0, 1.4, -3.12),
    size=vector(1.1, 2.3, 0.05),
    color=wood
)

# Door handle
sphere(
    pos=vector(0.55, 1.4, -3.2),
    radius=0.09,
    color=color.yellow
)

# Front steps
for i in range(3):
    box(
        pos=vector(0, 0.15 + i * 0.2, -3.5 - i * 0.4),
        size=vector(2.4, 0.2, 0.8),
        color=gray
    )

# ==========================================
# 5. SECOND FLOOR
# ==========================================

# Second floor
box(
    pos=vector(0, 5.15, 0),
    size=vector(10, 0.3, 6),
    color=white
)

# Back wall
box(
    pos=vector(0, 6.6, 2.85),
    size=vector(10, 2.8, 0.3),
    color=white
)

# Side walls
for x in [-4.85, 4.85]:
    box(
        pos=vector(x, 6.6, 0),
        size=vector(0.3, 2.8, 6),
        color=white
    )

# Upper floor windows
for x in [-3, 0, 3]:

    box(
        pos=vector(x, 6.7, 2.65),
        size=vector(1.6, 1.5, 0.12),
        color=glass
    )

# ==========================================
# 6. THIRD FLOOR
# ==========================================

# Third floor slab
box(
    pos=vector(0, 8.15, 0),
    size=vector(10, 0.3, 6),
    color=white
)

# Back wall
box(
    pos=vector(0, 9.6, 2.85),
    size=vector(10, 2.8, 0.3),
    color=white
)

# Side walls
for x in [-4.85, 4.85]:
    box(
        pos=vector(x, 9.6, 0),
        size=vector(0.3, 2.8, 6),
        color=white
    )

# Third-floor windows
for x in [-3, 0, 3]:
    box(
        pos=vector(x, 9.7, 2.65),
        size=vector(1.6, 1.5, 0.12),
        color=glass
    )

# ==========================================
# 7. BEDROOM FURNITURE
# ==========================================

# BEDROOM 1 - LEFT SIDE

# Bed frame
box(
    pos=vector(-2.5, 5.55, 0),
    size=vector(2.2, 0.3, 2.7),
    color=wood
)

# Mattress
box(
    pos=vector(-2.5, 5.75, 0),
    size=vector(2.1, 0.15, 2.5),
    color=white
)

# Blanket
box(
    pos=vector(-2.5, 5.85, 0.6),
    size=vector(2.05, 0.1, 1.3),
    color=vector(0.55, 0.30, 0.20)
)

# Pillows
for x in [-3, -2]:
    box(
        pos=vector(x, 5.88, -0.8),
        size=vector(0.8, 0.12, 0.5),
        color=vector(0.65, 0.75, 0.95)
    )

# Nightstand
box(
    pos=vector(-4, 5.65, -0.5),
    size=vector(0.65, 0.7, 0.7),
    color=wood
)

# BEDROOM 2 - RIGHT SIDE

# Bed frame
box(
    pos=vector(2.4, 5.55, 0),
    size=vector(2.1, 0.3, 2.7),
    color=wood
)

# Mattress
box(
    pos=vector(2.4, 5.75, 0),
    size=vector(2.0, 0.15, 2.5),
    color=white
)

# Blanket
box(
    pos=vector(2.4, 5.85, 0.6),
    size=vector(1.95, 0.1, 1.3),
    color=vector(0.55, 0.30, 0.20)
)

# Pillows
for x in [1.9, 2.9]:
    box(
        pos=vector(x, 5.88, -0.8),
        size=vector(0.8, 0.12, 0.5),
        color=vector(0.65, 0.75, 0.95)
    )

# Nightstand
box(
    pos=vector(3.9, 5.65, -0.5),
    size=vector(0.65, 0.7, 0.7),
    color=wood
)

# Wardrobe
box(
    pos=vector(0, 6.3, 2.3),
    size=vector(2.2, 1.4, 0.8),
    color=wood
)

# Wardrobe doors
for x in [-0.55, 0.55]:
    box(
        pos=vector(x, 6.3, 1.88),
        size=vector(0.9, 1.3, 0.05),
        color=brown
    )

# ==========================================
# 8. BALCONY
# ==========================================

box(
    pos=vector(0, 5.15, -3.6),
    size=vector(10, 0.2, 1.3),
    color=wood
)

# Balcony railing
for x in range(-4, 5):
    cylinder(
        pos=vector(x, 5.25, -4.2),
        axis=vector(0, 0.9, 0),
        radius=0.035,
        color=gray
    )

box(
    pos=vector(0, 6.15, -4.2),
    size=vector(9, 0.08, 0.08),
    color=gray
)

# ==========================================
# 9. FLAT BROWN ROOF
# ==========================================

box(
    pos=vector(0, 11.15, 0),
    size=vector(10.5, 0.3, 6.5),
    color=brown
)

# ==========================================
# 10. GARAGE
# ==========================================

# Garage floor
box(
    pos=vector(8, 0.15, 0),
    size=vector(5.8, 0.3, 6),
    color=white
)

# Back wall
box(
    pos=vector(8, 2.1, 2.85),
    size=vector(5.8, 4, 0.3),
    color=white
)

# Side walls
for x in [5.2, 10.8]:
    box(
        pos=vector(x, 2.1, 0),
        size=vector(0.3, 4, 6),
        color=white
    )

# Garage roof
box(
    pos=vector(8, 4.2, 0),
    size=vector(6.2, 0.3, 6.5),
    color=brown
)

# Garage entrance frame
for x in [5.5, 10.5]:
    box(
        pos=vector(x, 2, -2.9),
        size=vector(0.3, 4, 0.3),
        color=white
    )

# ==========================================
# 11. CAR INSIDE GARAGE
# ==========================================

# Car body
box(
    pos=vector(8, 0.85, 0),
    size=vector(2.2, 0.7, 4),
    color=vector(0.75, 0.78, 0.83)
)

# Car cabin
box(
    pos=vector(8, 1.4, 0),
    size=vector(1.8, 0.8, 2.2),
    color=glass
)

# Car wheels
for x in [6.8, 9.2]:
    for z in [-1.3, 1.3]:
        cylinder(
            pos=vector(x, 0.45, z),
            axis=vector(0.2, 0, 0),
            radius=0.35,
            color=color.black
        )

# ==========================================
# 12. SWIMMING POOL
# ==========================================

# Pool water
box(
    pos=vector(-8, 0.02, -6),
    size=vector(7, 0.08, 5),
    color=vector(0.05, 0.55, 0.95)
)

# Pool borders
for x in [-11.65, -4.35]:
    box(
        pos=vector(x, 0.12, -6),
        size=vector(0.3, 0.2, 5.5),
        color=white
    )

for z in [-8.65, -3.35]:
    box(
        pos=vector(-8, 0.12, z),
        size=vector(7.5, 0.2, 0.3),
        color=white
    )

# Poolside lounge chairs
for x in [-10, -7]:
    box(
        pos=vector(x, 0.35, -2.2),
        size=vector(1.1, 0.15, 1.0),
        color=wood
    )

# ==========================================
# 13. GARDEN PATHWAY
# ==========================================

for i in range(8):
    box(
        pos=vector(0, 0.04, -4.5 - i * 0.85),
        size=vector(1.4, 0.08, 0.6),
        color=vector(0.8, 0.76, 0.68)
    )

# ==========================================
# 14. REALISTIC 3D GARDEN TREES
# ==========================================

def make_tree(x, z, height=6):

    s = height / 6

    trunk_color = vector(0.35, 0.18, 0.08)

    # TREE TRUNK
    cylinder(
        pos=vector(x, 0, z),
        axis=vector(0, height * 0.55, 0),
        radius=0.28 * s,
        color=trunk_color
    )

    # TREE BRANCHES
    branches = [
        (vector(-0.8, 1.5, 0), vector(-0.9, 1.2, 0.2)),
        (vector(0.8, 1.8, 0), vector(0.9, 1.1, -0.2)),
        (vector(0, 2.2, 0.5), vector(0.2, 1.1, 0.8)),
        (vector(0, 2.5, -0.5), vector(-0.2, 1.0, -0.8))
    ]

    for start, direction in branches:
        cylinder(
            pos=vector(x, 0, z) + start * s,
            axis=direction * s,
            radius=0.12 * s,
            color=trunk_color
        )

    # BOTTOM LEAF LAYER
    cone(
        pos=vector(x, height * 0.30, z),
        axis=vector(0, height * 0.45, 0),
        radius=1.6 * s,
        color=vector(0.08, 0.38, 0.12)
    )

    # MIDDLE LEAF LAYER
    cone(
        pos=vector(x, height * 0.48, z),
        axis=vector(0, height * 0.40, 0),
        radius=1.3 * s,
        color=vector(0.12, 0.50, 0.15)
    )

    # TOP LEAF LAYER
    cone(
        pos=vector(x, height * 0.65, z),
        axis=vector(0, height * 0.35, 0),
        radius=0.95 * s,
        color=vector(0.18, 0.58, 0.20)
    )


# ORIGINAL GARDEN TREES
make_tree(-14, -2, 6)
make_tree(-14, 5, 5)
make_tree(-13, -10, 6)

make_tree(14, -2, 6)
make_tree(14, 5, 5)
make_tree(13, -10, 6)

# ==========================================
# 15. TREES BESIDE THE ENTRANCE
# ==========================================

# LEFT TREE
make_tree(-5.5, -10.5, 3.5)

# RIGHT TREE
make_tree(6.5, -10.5, 3.5)

# ==========================================
# 16. FLOWERS
# ==========================================

for x in [-5, -4, 4, 5, 11, 12]:
    for z in [-3, 1, 4]:

        cylinder(
            pos=vector(x, 0, z),
            axis=vector(0, 0.4, 0),
            radius=0.04,
            color=color.green
        )

        sphere(
            pos=vector(x, 0.5, z),
            radius=0.17,
            color=vector(1, 0.25, 0.55)
        )

# ==========================================
# 17. FENCE - OPEN ENTRANCE
# ==========================================

# Left fence
for x in range(-16, -4, 2):
    box(
        pos=vector(x, 0.8, -12.5),
        size=vector(1.8, 1.6, 0.18),
        color=dark_brown
    )

# Right fence
for x in range(6, 17, 2):
    box(
        pos=vector(x, 0.8, -12.5),
        size=vector(1.8, 1.6, 0.18),
        color=dark_brown
    )

# Horizontal fence rails
for y in [0.4, 1.1]:

    box(
        pos=vector(-10, y, -12.6),
        size=vector(10, 0.12, 0.2),
        color=wood
    )

    box(
        pos=vector(11, y, -12.6),
        size=vector(10, 0.12, 0.2),
        color=wood
    )

# Side fences
for x in [-16, 16]:
    box(
        pos=vector(x, 0.8, 0),
        size=vector(0.18, 1.6, 25),
        color=dark_brown
    )

# NO FRONT GATE
# NO GATE PANELS
# NO GATE PILLARS
# OPEN ENTRANCE TO THE FRONT DOOR

# ==========================================
# 18. SUN
# ==========================================

sphere(
    pos=vector(12, 13, 0),
    radius=1.2,
    color=color.yellow,
    emissive=True
)

# ==========================================
# 19. FINISH
# ==========================================

print("====================================")
print("MY MODERN LUXURY DREAM HOUSE")
print("====================================")
print("Three-story house: READY")
print("Flat brown roof: READY")
print("Swimming pool: READY")
print("Garage and car: READY")
print("Garden and flowers: READY")
print("Garden trees: READY")
print("Two entrance trees: READY")
print("Bedroom furniture: READY")
print("Open front entrance: READY")
print("Fence: READY")
print("====================================")

# KEEP THE 3D SCENE RUNNING
while True:
    rate(60)