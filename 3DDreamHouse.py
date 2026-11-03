"""Interactive VPython model of a modern tropical two-storey luxury home."""

from math import cos, pi, radians, sin

from vpython import *


scene = canvas(
    title="Modern Tropical Residence",
    width=1280,
    height=800,
    background=vector(0.68, 0.81, 0.93),
    center=vector(0, 3.2, 1.5),
    range=22,
)
scene.autoscale = False
scene.ambient = vector(0.62, 0.64, 0.68)
scene.lights = []
distant_light(direction=vector(-0.8, -1.1, -0.5), color=vector(1, 0.91, 0.78))
distant_light(direction=vector(0.7, -0.8, 0.55), color=vector(0.72, 0.82, 1))
scene.userspin = True
scene.userzoom = True
camera_target = vector(0, 3.2, 1.5)
orbit = {
    "yaw": radians(39.9),
    "elevation": radians(19.7),
    "distance": 38.1,
}
scene.caption = (
    "\nArrow keys: orbit 360°  |  Home: reset view"
    "  |  Drag: orbit  |  Scroll: zoom  |  Shift-drag: pan\n"
)

WHITE = vector(0.88, 0.89, 0.86)
WALL_WHITE = vector(0.82, 0.84, 0.82)
WOOD = vector(0.43, 0.25, 0.13)
WOOD_LIGHT = vector(0.58, 0.36, 0.2)
WOOD_DARK = vector(0.27, 0.16, 0.1)
CHARCOAL = vector(0.075, 0.09, 0.1)
GLASS = vector(0.22, 0.43, 0.53)
CONCRETE = vector(0.66, 0.67, 0.64)
GRASS = vector(0.25, 0.39, 0.2)
LEAF = vector(0.16, 0.34, 0.16)
FLOWER = vector(0.87, 0.34, 0.48)
SOIL = vector(0.25, 0.17, 0.11)


def block(position, size, tint, opacity=1):
    """Create a rectangular architectural or landscape element."""
    return box(pos=position, size=size, color=tint, opacity=opacity)


def add_window(position, width, height, face="front", panes=2):
    """Build a blue-tinted glazed unit with a slim dark aluminum frame."""
    x, y, z = position.x, position.y, position.z
    frame = 0.075
    depth = 0.1
    if face == "front":
        glass_z = z + 0.025
        frame_z = z + 0.085
        block(vector(x, y, glass_z), vector(width - 2 * frame, height - 2 * frame, 0.045), GLASS, 0.58)
        block(vector(x, y - height / 2 + frame / 2, frame_z), vector(width, frame, depth), CHARCOAL)
        block(vector(x, y + height / 2 - frame / 2, frame_z), vector(width, frame, depth), CHARCOAL)
        for side in (-1, 1):
            block(
                vector(x + side * (width / 2 - frame / 2), y, frame_z),
                vector(frame, height, depth),
                CHARCOAL,
            )
        for pane in range(1, panes):
            mullion_x = x - width / 2 + width * pane / panes
            block(vector(mullion_x, y, frame_z + 0.01), vector(0.045, height - 0.08, 0.035), CHARCOAL)
        block(
            vector(x + width * 0.2, y + height * 0.06, z + 0.07),
            vector(0.025, height * 0.62, 0.012),
            vector(0.72, 0.83, 0.87),
            0.34,
        )
    else:
        facing = 1 if face == "right" else -1
        glass_x = x + facing * 0.025
        frame_x = x + facing * 0.085
        block(vector(glass_x, y, z), vector(0.045, height - 2 * frame, width - 2 * frame), GLASS, 0.58)
        block(vector(frame_x, y - height / 2 + frame / 2, z), vector(depth, frame, width), CHARCOAL)
        block(vector(frame_x, y + height / 2 - frame / 2, z), vector(depth, frame, width), CHARCOAL)
        for side in (-1, 1):
            block(
                vector(frame_x, y, z + side * (width / 2 - frame / 2)),
                vector(depth, height, frame),
                CHARCOAL,
            )
        block(vector(frame_x, y, z), vector(depth, height, 0.045), CHARCOAL)


def build_windows():
    """Place the floor-to-ceiling glazing, entry door, and upper windows."""
    # Ground-floor living-room glazing.
    add_window(vector(-4.25, 1.95, 5.08), 2.45, 2.65, panes=2)
    add_window(vector(1.7, 1.98, 5.08), 4.3, 2.7, panes=3)

    # Timber entrance door with a narrow glazed sidelight.
    block(vector(-1.75, 1.79, 5.16), vector(1.35, 2.5, 0.12), WOOD)
    for slat_x in (-2.23, -2.04, -1.85, -1.66, -1.47, -1.28):
        block(vector(slat_x, 1.79, 5.23), vector(0.025, 2.35, 0.012), WOOD_LIGHT)
    add_window(vector(-0.72, 1.98, 5.08), 0.42, 2.55, panes=1)
    cylinder(pos=vector(-1.28, 1.78, 5.29), axis=vector(0, 0.24, 0), radius=0.025, color=vector(0.72, 0.68, 0.52))

    # Upper-floor sliding doors open onto the balcony.
    add_window(vector(-0.05, 5.05, 5.08), 4.65, 2.45, panes=3)
    # Rectangular windows on the upper side elevations.
    add_window(vector(6.08, 5.12, -1.25), 1.7, 1.65, face="right", panes=1)
    add_window(vector(-6.08, 5.12, -1.2), 1.7, 1.65, face="left", panes=1)


def build_house():
    """Build the two-storey shell, floors, white facade, and wood feature wall."""
    # Raised foundation and story slabs.
    block(vector(0, 0.53, 0), vector(12.7, 0.32, 10.8), CONCRETE)
    block(vector(0, 3.68, 0), vector(12.25, 0.28, 10.45), WALL_WHITE)

    # Ground-floor rear and side walls.
    block(vector(0, 2.12, -5.08), vector(12, 3.0, 0.22), WALL_WHITE)
    for x in (-5.92, 5.92):
        block(vector(x, 2.12, 0), vector(0.22, 3.0, 10), WALL_WHITE)

    # White front columns and continuous lintel leave the main glazing exposed.
    for x in (-5.75, -2.95, -0.98, 4.02, 5.75):
        block(vector(x, 2.12, 5.08), vector(0.28, 3.0, 0.3), WHITE)
    block(vector(0, 3.48, 5.08), vector(12, 0.28, 0.3), WHITE)
    block(vector(0, 0.78, 5.08), vector(12, 0.32, 0.3), WHITE)

    # Upper-floor side and rear walls.
    block(vector(0, 5.13, -5.08), vector(12, 2.62, 0.22), WALL_WHITE)
    for x in (-5.92, 5.92):
        block(vector(x, 5.13, 0), vector(0.22, 2.62, 10), WALL_WHITE)

    # White front end panels frame the natural timber feature wall.
    block(vector(-4.82, 5.13, 5.08), vector(2.15, 2.62, 0.24), WHITE)
    block(vector(4.82, 5.13, 5.08), vector(2.15, 2.62, 0.24), WHITE)
    # Timber panels flank the upper sliding doors, with a matching header.
    for x in (-3.35, 3.25):
        block(vector(x, 5.15, 5.23), vector(1.0, 2.45, 0.12), WOOD)
        for slat in range(1, 8):
            slat_x = x - 0.5 + slat * (1.0 / 8)
            block(vector(slat_x, 5.15, 5.31), vector(0.035, 2.35, 0.025), WOOD_LIGHT)
    block(vector(0, 6.35, 5.22), vector(5.65, 0.22, 0.14), WOOD)

    # Subtle timber fins add depth to the upper side elevations.
    for z in range(-3, 4):
        block(vector(6.055, 5.12, z), vector(0.12, 2.25, 0.055), WOOD_LIGHT)

    build_windows()
    build_roof()


def build_roof():
    """Create broad flat roof overhangs and a raised timber roof screen."""
    block(vector(0, 6.62, 0), vector(13.5, 0.36, 11.8), CHARCOAL)
    block(vector(0, 6.83, 0), vector(13.65, 0.08, 11.95), WHITE)

    # Raised, open timber screen feature on the roof; it is not another floor.
    for x in (-4.2, 4.2):
        block(vector(x, 7.42, -0.4), vector(0.16, 1.05, 5.6), WOOD_DARK)
    block(vector(0, 7.94, -0.4), vector(8.55, 0.16, 5.75), WOOD)
    for x in range(-38, 39, 3):
        block(vector(x / 10, 7.42, 2.45), vector(0.045, 0.95, 0.06), WOOD_LIGHT)


def build_balcony():
    """Build the front balcony with metal railing and a small outdoor dining set."""
    block(vector(0, 3.9, 6.25), vector(6.5, 0.24, 2.65), CONCRETE)
    # Front balustrade: round metal top/bottom rails and evenly spaced posts.
    cylinder(pos=vector(0, 5.0, 7.55), axis=vector(6.25, 0, 0), radius=0.055, color=CHARCOAL)
    cylinder(pos=vector(0, 4.08, 7.55), axis=vector(6.25, 0, 0), radius=0.045, color=CHARCOAL)
    for index in range(19):
        x = -3.0 + index * (6.0 / 18)
        cylinder(pos=vector(x, 4.08, 7.55), axis=vector(0, 0.92, 0), radius=0.025, color=CHARCOAL)
    # Short return rails at both balcony sides.
    for x in (-3.05, 3.05):
        cylinder(pos=vector(x, 4.08, 6.25), axis=vector(0, 0.92, 0), radius=0.035, color=CHARCOAL)
        cylinder(pos=vector(x, 5.0, 6.25), axis=vector(0, 0, 1.3), radius=0.045, color=CHARCOAL)

    # Minimal table and four chairs, all kept within the balcony footprint.
    block(vector(0, 4.55, 6.25), vector(1.25, 0.09, 0.8), WOOD_LIGHT)
    for x in (-0.48, 0.48):
        for z in (5.96, 6.54):
            cylinder(pos=vector(x, 4.15, z), axis=vector(0, 0.4, 0), radius=0.035, color=CHARCOAL)
    for x in (-1.05, 1.05):
        for z in (5.95, 6.55):
            block(vector(x, 4.32, z), vector(0.48, 0.08, 0.42), WOOD)
            for leg_x in (-0.18, 0.18):
                for leg_z in (-0.14, 0.14):
                    cylinder(
                        pos=vector(x + leg_x, 4.08, z + leg_z),
                        axis=vector(0, 0.24, 0),
                        radius=0.018,
                        color=CHARCOAL,
                    )


def build_carport():
    """Add the right-side covered parking bay and its white support columns."""
    block(vector(9.25, 3.35, 0.2), vector(7.3, 0.28, 10.5), WHITE)
    for x in (6.3, 12.2):
        for z in (-4.45, 4.8):
            block(vector(x, 1.82, z), vector(0.28, 3.05, 0.28), WHITE)
    block(vector(9.25, 0.47, 0.2), vector(7.4, 0.12, 10.7), CONCRETE)


def build_pool():
    """Create a raised rectangular pool with pale coping and decorative stones."""
    pool_x, pool_z = -8.0, 10.0
    block(vector(pool_x, 0.48, pool_z), vector(5.6, 0.42, 7.4), WHITE)
    block(vector(pool_x, 0.63, pool_z), vector(5.1, 0.16, 6.9), vector(0.13, 0.4, 0.55), 0.82)
    block(vector(pool_x, 0.73, pool_z), vector(5.3, 0.08, 7.1), vector(0.3, 0.62, 0.72), 0.5)
    for x, z, radius in (
        (-10.9, 6.2, 0.42),
        (-10.8, 13.9, 0.5),
        (-5.1, 6.6, 0.36),
        (-5.0, 13.6, 0.46),
        (-8.2, 14.0, 0.34),
        (-8.9, 6.0, 0.3),
    ):
        sphere(pos=vector(x, 0.58, z), radius=radius, color=vector(0.43, 0.45, 0.41))


def build_palm(x, z, scale=1):
    """Create a tropical palm with a textured-looking trunk and tapered fronds."""
    trunk_height = 4.2 * scale
    cylinder(
        pos=vector(x, 0.45, z),
        axis=vector(-0.16 * scale, trunk_height, 0),
        radius=0.19 * scale,
        color=WOOD,
    )
    crown = vector(x - 0.16 * scale, 0.45 + trunk_height, z)
    for index in range(9):
        angle = radians(index * 40)
        direction = vector(cos(angle), -0.28 + 0.035 * (index % 3), sin(angle))
        ellipsoid(
            pos=crown + direction * (1.1 * scale),
            size=vector(0.24 * scale, 0.12 * scale, 2.5 * scale),
            axis=direction,
            color=LEAF if index % 2 else vector(0.22, 0.4, 0.2),
        )


def build_plant(x, z, scale=1, flowering=False):
    """Add a small cluster of rounded foliage and optional pink blossoms."""
    cylinder(
        pos=vector(x, 0.4, z),
        axis=vector(0, 0.12, 0),
        radius=0.46 * scale,
        color=SOIL,
    )
    for dx, dz, size in ((-0.25, 0, 0.62), (0.22, -0.12, 0.68), (0.02, 0.25, 0.58), (-0.1, -0.22, 0.48)):
        sphere(
            pos=vector(x + dx * scale, 0.78 * scale, z + dz * scale),
            radius=size * 0.55 * scale,
            color=LEAF,
        )
    if flowering:
        for dx, dz in ((-0.28, 0.03), (0.2, -0.14), (0.04, 0.28), (0.18, 0.12), (-0.08, -0.22)):
            sphere(
                pos=vector(x + dx * scale, 1.08 * scale, z + dz * scale),
                radius=0.085 * scale,
                color=FLOWER,
            )


def build_garden():
    """Lay out the lawn, field, paths, driveway, trees, and ornamental plants."""
    # The broad field and the raised, rectangular landscaped property.
    block(vector(0, -0.22, 2), vector(240, 0.25, 240), vector(0.34, 0.48, 0.25))
    block(vector(0, 0.12, 3.5), vector(28, 0.42, 34), CONCRETE)
    block(vector(0, 0.36, 3.5), vector(27.4, 0.08, 33.4), GRASS)

    # Light concrete driveway runs from the front gate to the carport.
    block(vector(8.6, 0.43, 12.0), vector(5.0, 0.08, 16.0), vector(0.72, 0.72, 0.68))
    for z in range(6, 20, 2):
        block(vector(8.6, 0.48, z), vector(4.8, 0.015, 0.025), vector(0.62, 0.64, 0.62))

    # Front stepping-stone path leading to the entry.
    for index in range(6):
        block(
            vector(-1.8, 0.48, 8.5 + index * 1.35),
            vector(2.0, 0.12, 0.92),
            vector(0.79, 0.79, 0.74),
        )

    build_pool()
    for x, z, scale in (
        (-12, 4, 1.0),
        (-11.6, 16, 0.9),
        (-5.1, 16.0, 0.82),
        (5.7, 11.8, 0.82),
        (12.2, 11.0, 0.95),
        (4.7, 17.0, 0.75),
    ):
        build_plant(x, z, scale, flowering=True)
    build_palm(-11.8, 3.4, 1.0)
    build_palm(12.0, 5.6, 0.9)

    # Low ornamental grasses near the path and garden bed.
    for x, z in ((-5.0, 7.2), (4.8, 7.4), (6.1, 15.0), (11.4, 16.3)):
        for index in range(7):
            angle = radians(index * (360 / 7))
            cone(
                pos=vector(x, 0.48, z),
                axis=vector(0.24 * cos(angle), 0.65, 0.24 * sin(angle)),
                radius=0.09,
                color=vector(0.32, 0.46, 0.23),
            )


def build_fence():
    """Enclose the property with timber slats, masonry posts, and a sliding gate."""
    fence_y = 1.15
    fence_z = 20.0
    gate_left, gate_right = 6.0, 11.2
    post_positions = (-13, -7, -1, 5.8, 11.4, 13)
    for x in post_positions:
        block(vector(x, 1.05, fence_z), vector(0.34, 2.1, 0.38), WHITE)

    def slat_section(start, end):
        count = int((end - start) / 0.34)
        for index in range(count):
            x = start + 0.18 + index * 0.34
            block(vector(x, fence_y, fence_z), vector(0.23, 1.55, 0.16), WOOD)
        block(vector((start + end) / 2, 0.43, fence_z), vector(end - start, 0.12, 0.2), WOOD_DARK)
        block(vector((start + end) / 2, 1.82, fence_z), vector(end - start, 0.12, 0.2), WOOD_DARK)

    slat_section(-13, gate_left)
    slat_section(gate_right, 13)
    # Sliding timber gate across the central entrance opening.
    gate_center = (gate_left + gate_right) / 2
    block(vector(gate_center, 1.08, 19.72), vector(4.85, 1.65, 0.16), WOOD_DARK)
    for index in range(17):
        x = gate_center - 2.3 + index * 0.29
        block(vector(x, 1.08, 19.61), vector(0.16, 1.53, 0.11), WOOD_LIGHT)

    # Side fence lines continue toward the back corners.
    for x in (-13, 13):
        for index in range(47):
            z = -13 + index * 0.7
            block(vector(x, fence_y, z), vector(0.16, 1.55, 0.22), WOOD)
        block(vector(x, 0.43, 3.0), vector(0.2, 0.12, 33), WOOD_DARK)
        block(vector(x, 1.82, 3.0), vector(0.2, 0.12, 33), WOOD_DARK)


def build_stairs():
    """Add broad, low-profile exterior steps at the main entrance."""
    for index in range(4):
        block(
            vector(-1.75, 0.56 - index * 0.07, 5.72 + index * 0.58),
            vector(2.0, 0.18, 0.82),
            CONCRETE,
        )


def update_camera():
    """Position the camera using its orbit angles around the house."""
    horizontal_distance = orbit["distance"] * cos(orbit["elevation"])
    scene.camera.pos = camera_target + vector(
        horizontal_distance * sin(orbit["yaw"]),
        orbit["distance"] * sin(orbit["elevation"]),
        horizontal_distance * cos(orbit["yaw"]),
    )
    scene.camera.axis = camera_target - scene.camera.pos
    scene.camera.up = vector(0, 1, 0)


def on_keydown(event):
    """Orbit the camera with arrow keys and restore its initial view with Home."""
    key = event.key.lower().replace("arrow", "")
    orbit_step = radians(8)
    elevation_step = radians(5)

    if key == "left":
        orbit["yaw"] = (orbit["yaw"] - orbit_step) % (2 * pi)
    elif key == "right":
        orbit["yaw"] = (orbit["yaw"] + orbit_step) % (2 * pi)
    elif key == "up":
        orbit["elevation"] = min(radians(80), orbit["elevation"] + elevation_step)
    elif key == "down":
        orbit["elevation"] = max(radians(5), orbit["elevation"] - elevation_step)
    elif key == "home":
        orbit.update(yaw=radians(39.9), elevation=radians(19.7), distance=38.1)
    else:
        return

    update_camera()


def build_scene():
    """Assemble all architectural and landscape components."""
    # Soft cloud shapes and a subtle contact shadow, without a rooftop sun prop.
    for position, size in (
        (vector(-15, 14, -32), vector(8, 1.3, 1.2)),
        (vector(-11, 14.3, -32), vector(5, 1.5, 1.2)),
        (vector(12, 13, -35), vector(7, 1.2, 1.1)),
        (vector(16, 13.4, -35), vector(5, 1.4, 1.1)),
    ):
        ellipsoid(pos=position, size=size, color=WHITE, opacity=0.38)
    ellipsoid(
        pos=vector(0, 0.42, 0),
        size=vector(15, 0.04, 12),
        color=vector(0.22, 0.24, 0.22),
        opacity=0.18,
    )

    build_garden()
    build_house()
    build_balcony()
    build_carport()
    build_stairs()
    build_fence()


build_scene()
scene.bind("keydown", on_keydown)
update_camera()

while True:
    rate(60)
