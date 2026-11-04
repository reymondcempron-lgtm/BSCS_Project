"""Small, reusable architectural objects made using VPython primitives."""
from math import cos, pi, sin
from random import Random
from vpython import (box, cylinder, sphere, cone, ring, curve, vec, color,
                     textures, local_light, text)

# SUAREZ color story: lavender house + plum roof + blush-pink accents.
# VPython colors are RGB triples between 0 and 1.
IVORY = vec(.97, .91, .98)          # bright pink-white details
PLASTER = vec(.75, .62, .89)        # visibly LAVENDER exterior
LIMESTONE = vec(.83, .71, .85)      # lilac stone paths
CONCRETE = vec(.75, .63, .80)       # violet stone foundation
CHARCOAL = vec(.30, .16, .43)       # eggplant/plum roof
GRAPHITE = vec(.39, .23, .55)       # dark-violet frames and railings
WALNUT = vec(.56, .38, .53)         # purple-brown stained wood
OAK = vec(.81, .59, .72)            # blush stained timber
LILAC = vec(.81, .65, .96)          # pastel purple upholstery
MAUVE = vec(.56, .30, .75)          # rich violet feature walls
ROSE = vec(.97, .43, .68)           # saturated rose garden
DUSTY_PINK = vec(.96, .69, .83)     # blush pink accents
LINEN = vec(.97, .83, .91)          # pink-cream fabric
GREEN = vec(.25, .46, .26)
LEAF = vec(.32, .53, .30)
GLASS = vec(.70, .57, .88)          # lilac-blue glass
GOLD = vec(.95, .75, .44)           # champagne gold
WATER = vec(.50, .54, .90)          # sapphire-lilac pool
DARK_GLASS = vec(.38, .30, .59)

rng = Random(84)


def cube(x, y, z, sx, sy, sz, tint, *, surface=None, opacity=1,
         shine=.32, emissive=False):
    kw = dict(pos=vec(x, y, z), size=vec(sx, sy, sz), color=tint,
              opacity=opacity, shininess=shine, emissive=emissive)
    if surface:
        # Never replace unknown materials with granite: that made the old
        # build look like every object was cut from the same gray rock.
        material = getattr(textures, surface, None)
        if material is not None:
            kw['texture'] = material
    return box(**kw)


def column(x, y0, z, radius, height, tint, *, facets=12):
    return cylinder(pos=vec(x, y0, z), axis=vec(0, height, 0),
                    radius=radius, color=tint, shininess=.32)


def beam(a, b, radius, tint):
    va, vb = vec(*a), vec(*b)
    return cylinder(pos=va, axis=vb-va, radius=radius, color=tint)


def lamp(x, y, z, warmth=1.0):
    # VPython's lights do not produce physically traced cast shadows.
    sphere(pos=vec(x, y, z), radius=.12,
           color=vec(1.0, .75, .47), emissive=True)
    return local_light(pos=vec(x, y, z),
                       color=vec(.22, .16, .11)*warmth)


def glass_panel(x, y, z, sx, sy, sz, *, purple=False):
    tint = vec(.55, .37, .72) if purple else DARK_GLASS
    p = cube(x, y, z, sx, sy, sz, tint, opacity=.27, shine=.96)
    # A narrow light-toned highlight makes glazing less like a pastel solid.
    if sx > sz:
        cube(x-sx*.31, y, z+.022, .045, sy*.90, .016,
             vec(.91, .94, .95), opacity=.25, shine=.98)
    return p


def window_front(x0, x1, z=8.04, bottom=1.12, top=3.51):
    """A realistic dark-aluminium framed two-pane front window."""
    mid = (x0+x1)/2
    w = x1-x0
    glass_panel(mid, (bottom+top)/2, z, w-.12, top-bottom-.12, .08)
    for x in (x0, mid, x1):
        cube(x, (bottom+top)/2, z+.12, .075, top-bottom+.17, .14,
             CHARCOAL, shine=.68)
    for y in (bottom, top, bottom+.06*(top-bottom)):
        cube(mid, y, z+.13, w+.10, .075, .17, CHARCOAL, shine=.68)
    cube(mid, bottom-.09, z+.19, w+.32, .07, .35, LIMESTONE, surface='granite')


def window_side(x, z0, z1, bottom=1.08, top=3.42):
    w = z1-z0
    glass_panel(x, (bottom+top)/2, (z0+z1)/2, .07, top-bottom-.1, w-.12)
    for z in (z0, (z0+z1)/2, z1):
        cube(x+(.10 if x>0 else -.10), (bottom+top)/2, z,
             .13, top-bottom+.13, .07, CHARCOAL)
    for y in (bottom, top):
        cube(x, y, (z0+z1)/2, .17, .075, w+.12, CHARCOAL)


def shrub(x, z, scale=1.0):
    column(x, .18, z, .12*scale, .38*scale, WALNUT)
    for dx, dz, sz in ((0,0,1),(-.24,.12,.75),(.22,-.13,.78)):
        sphere(pos=vec(x+dx*scale,.75*scale,z+dz*scale),
               radius=.42*scale*sz, color=vec(.22,.35+.12*rng.random(),.21),
               shininess=.12)


def tree(x, z, size=1.0, bloom=False):
    h=3.9*size
    column(x,.13,z,.21*size,h,WALNUT)
    for i in range(5):
        a=i*2*pi/5 + .31
        ox=.98*cos(a)*size
        oz=.98*sin(a)*size
        sphere(pos=vec(x+ox,h+.48*size,z+oz),radius=1.30*size,
               color=vec(.23+.03*rng.random(), .37+.11*rng.random(), .22),
               shininess=.10)
    sphere(pos=vec(x,h+1.16*size,z),radius=1.48*size,
           color=vec(.26,.42,.26),shininess=.10)
    if bloom:
        for i in range(15):
            a=2*pi*i/15
            sphere(pos=vec(x+cos(a)*1.35*size,h+.6*size+((i%3)-1)*.35,
                           z+sin(a)*1.1*size), radius=.11*size,
                   color=ROSE if i%3 else vec(.93,.73,.79))


def flower(x, z, hue=ROSE, size=1.0):
    height=.30*size
    column(x,.14,z,.021*size,height,GREEN)
    sphere(pos=vec(x,.16+height,z),radius=.07*size,color=GOLD)
    for i in range(5):
        a=i*2*pi/5
        sphere(pos=vec(x+.105*cos(a)*size,.16+height,z+.105*sin(a)*size),
               radius=.085*size,color=hue)


def plant_pot(x,z,y=.46,size=1.0):
    column(x,y,z,.26*size,.50*size,vec(.48,.37,.32))
    for i in range(6):
        a=i*pi/3
        sphere(pos=vec(x+cos(a)*.19*size,y+.74*size,z+sin(a)*.19*size),
               radius=.23*size,color=vec(.22,.39,.25))


def physical_sign(words, x, y, z, size=.40):
    """Flat wall-mounted letters (not floating UI labels)."""
    try:
        return text(text=words, pos=vec(x,y,z), align='center',
                    height=size, depth=.018, color=CHARCOAL,
                    emissive=False)
    except Exception:
        # Text may fail on old font/browser configurations; model still works.
        return None
