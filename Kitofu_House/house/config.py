"""Edit this file first. Units: metres; Y up, -Z street, +Z backyard."""
TITLE = 'KITOFU HOUSE'
DETAIL = 'standard'  # 'low' reduces foliage and decorative slats
FPS = 40
VIEW_WIDTH, VIEW_HEIGHT = 1100, 640
TOUR_SPEED, TOUR_DWELL = 3.5, 5.0
OVERVIEW_SPEED = 22.0
LOT_WIDTH, LOT_DEPTH = 44.0, 70.0
HOUSE_WIDTH, HOUSE_DEPTH = 24.0, 20.0
HOUSE_FRONT = -4.0
HOUSE_REAR = HOUSE_FRONT + HOUSE_DEPTH
FLOOR_HEIGHT = 3.6
SLAB = 0.24
EYE_HEIGHT = 1.65
WALK_SPEED = 3.0
TURN_SPEED = 1.35
POOL = (3.0, 25.0, 13.0, 6.0)  # x, z, width, depth
PAVILION = (-13.0, 26.0, 9.0, 8.0)
GARAGE = (-16.0, 1.0, 7.0, 10.0)
LAWN = (-9.0, 12.0, -28.0, -10.0)  # safe pet region
DOG_CENTER = (2.0, -19.0)
DOG_RADII = (7.0, 5.0)
DOG_SPEED = 0.23
TREE_POSITIONS = [(-20, z) for z in (-28, -17, 15, 29)] + [(20, z) for z in (-26, -14, 1, 15, 29)] + [(-7, 33), (8, 33)]
PALETTE = {
    'ivory': (0.88, 0.85, 0.76), 'cream': (0.97, 0.94, 0.85),
    'stone': (0.39, 0.43, 0.42), 'wood': (0.48, 0.29, 0.14),
    'charcoal': (0.11, 0.15, 0.15), 'green': (0.12, 0.28, 0.21),
    'grass': (0.37, 0.49, 0.27), 'leaf': (0.17, 0.36, 0.20),
    'sand': (0.73, 0.65, 0.48), 'brass': (0.66, 0.51, 0.26),
    'water': (0.18, 0.64, 0.70), 'glass': (0.62, 0.79, 0.80),
    'white': (0.96, 0.95, 0.90), 'blue': (0.08, 0.28, 0.68),
    'red': (0.78, 0.12, 0.10), 'black': (0.04, 0.05, 0.05),
    'linen': (0.83, 0.78, 0.66), 'terracotta': (0.64, 0.30, 0.20),
    'roof': (0.17, 0.20, 0.20), 'travertine': (0.78, 0.73, 0.62),
}
