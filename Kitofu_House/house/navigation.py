"""Pure Python collision and route logic, testable without a browser."""
from dataclasses import dataclass
from math import cos, sin
from . import config as C


@dataclass(frozen=True)
class Obstacle:
    x: float
    z: float
    width: float
    depth: float
    bottom: float
    top: float

    def blocks(self, x, z, floor, radius=0.22):
        return (self.bottom < floor + 1.8 and self.top > floor + 0.12
                and abs(x-self.x) < self.width/2+radius
                and abs(z-self.z) < self.depth/2+radius)


def floor_at(x, z, old_floor):
    # Straight stair: 1.8 m wide, rises toward the rear through a slab void.
    if 0.45 <= x <= 2.65 and 5 <= z <= 12.2:
        return C.FLOOR_HEIGHT * min(1, max(0, (z-5)/7.2))
    if old_floor > C.FLOOR_HEIGHT-0.15:
        if 5 < x < 11.7 and -3.7 < z < 2.2:
            return None  # actual double-height dining salon, guarded gallery edges
        inside = -12 < x < 12 and C.HOUSE_FRONT < z < C.HOUSE_REAR
        balcony = -9 < x < -2.2 and C.HOUSE_FRONT-3 < z < C.HOUSE_FRONT
        return C.FLOOR_HEIGHT if inside or balcony else None
    if old_floor > 0.15:
        return None  # do not step sideways off the stair
    return 0.0


def can_walk(x, z, old_floor, obstacles):
    if not (-C.LOT_WIDTH/2+0.5 < x < C.LOT_WIDTH/2-0.5 and
            -C.LOT_DEPTH/2+0.5 < z < C.LOT_DEPTH/2-0.5):
        return None
    floor = floor_at(x, z, old_floor)
    if floor is None or abs(floor-old_floor)>0.16 or any(o.blocks(x, z, floor) for o in obstacles):
        return None
    return floor


def dog_route(t):
    a = t*C.DOG_SPEED
    return (C.DOG_CENTER[0]+C.DOG_RADII[0]*cos(a),
            C.DOG_CENTER[1]+C.DOG_RADII[1]*sin(a))


# All internal door centres meet this connected circulation spine.
# Nodes contain feet positions; camera eye height is added by the controller.
NODES = {
    'gate': (0, 0, -31), 'front': (0, 0, -8),
    'garage_path': (-16, 0, -8), 'garage': (-16, 0, -3),
    'foyer': (0, 0, -1), 'living_door': (-2, 0, 1), 'living': (-5, 0, 1),
    'hall': (0, 0, 3.5), 'dining_door': (2, 0, 3.5), 'dining': (4, 0, 3.5),
    'stair_base': (1.5, 0, 4.6), 'stair_top': (1.5, C.FLOOR_HEIGHT, 12.6),
    'landing': (0, C.FLOOR_HEIGHT, 12.6), 'upper_hall': (-0.7, C.FLOOR_HEIGHT, 1),
    'master': (-4.4, C.FLOOR_HEIGHT, 1), 'balcony_door': (-4.4, C.FLOOR_HEIGHT, -3),
    'balcony': (-5, C.FLOOR_HEIGHT, -5.1),
    'gallery_door': (2, C.FLOOR_HEIGHT, 3.5),
    'gallery': (4, C.FLOOR_HEIGHT, 3.5),
    'office': (7, C.FLOOR_HEIGHT, 3.5),
    'rear_hall': (-0.7, 0, 13.5), 'terrace': (0, 0, 18),
    'pool': (0, 0, 20), 'bbq_path': (-13, 0, 20), 'bbq': (-13, 0, 23),
    'lawn': (0, 0, -17),
}
EDGES = [('gate','front'), ('front','garage_path'), ('garage_path','garage'),
         ('front','foyer'), ('foyer','living_door'), ('living_door','living'),
         ('foyer','hall'), ('hall','dining_door'), ('dining_door','dining'),
         ('hall','stair_base'), ('stair_base','stair_top'), ('stair_top','landing'),
         ('landing','upper_hall'), ('upper_hall','master'), ('master','balcony_door'),
         ('balcony_door','balcony'), ('upper_hall','gallery_door'),
         ('gallery_door','gallery'), ('gallery','office'),
         ('hall','rear_hall'), ('rear_hall','terrace'),
         ('terrace','pool'), ('pool','bbq_path'), ('bbq_path','bbq'), ('front','lawn')]
STOPS = [('Front entrance','front'), ('Garage','garage'), ('Entrance foyer','foyer'),
         ('Living room','living'), ('Dining & kitchen','dining'), ('Upstairs landing','landing'),
         ('Master suite','master'), ('Shaded balcony','balcony'),
         ('Gallery & home office','office'), ('Rear terrace','terrace'),
         ('Backyard pool','pool'), ('BBQ pavilion','bbq'), ('Dog lawn','lawn')]
LOOKS = {'front':(0,3,3), 'garage':(-18,1,1), 'foyer':(-5,1.6,1),
         'living':(-9,1,3), 'dining':(8,4.4,0), 'landing':(-6,5,12),
         'office':(8,4.5,0),
         'master':(-8,4.8,-1), 'balcony':(0,1,-20), 'terrace':(3,1,25),
         'pool':(3,0,25), 'bbq':(-16,1,28), 'lawn':(3,0.7,-19)}


def route(start, end):
    queue = [(start, [])]
    seen = set()
    while queue:
        node, path = queue.pop(0)
        if node == end:
            return path
        if node in seen:
            continue
        seen.add(node)
        for a, b in EDGES:
            if a == node:
                queue.append((b, path+[b]))
            elif b == node:
                queue.append((a, path+[a]))
    raise ValueError(f'No connected route from {start} to {end}')
