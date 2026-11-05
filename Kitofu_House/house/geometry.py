"""Small reusable shapes; collisions and cutaway groups share the geometry."""
import vpython as v
from .config import PALETTE
from .navigation import Obstacle


def color(name):
    return v.vector(*PALETTE[name]) if isinstance(name, str) else v.vector(*name)


class Builder:
    def __init__(self):
        self.groups = {'ground': [], 'upper': [], 'roof': [], 'site': []}
        self.group = 'site'
        self.obstacles = []
        self.count = 0

    def keep(self, obj):
        self.groups[self.group].append(obj)
        self.count += 1
        return obj

    def box(self, pos, size, material='ivory', solid=False, **kw):
        if 'axis' in kw:
            kw['axis']=v.norm(kw['axis'])*size[0]
        obj = self.keep(v.box(pos=v.vector(*pos), size=v.vector(*size), color=color(material), shininess=0.15, **kw))
        if solid:
            x,y,z = pos
            w,h,d = size
            self.obstacles.append(Obstacle(x,z,w,d,y-h/2,y+h/2))
        return obj

    def ellipsoid(self, pos, size, material='leaf', **kw):
        return self.keep(v.ellipsoid(pos=v.vector(*pos), size=v.vector(*size), color=color(material), **kw))

    def rod(self, a, b, radius=0.04, material='charcoal'):
        start, end = v.vector(*a), v.vector(*b)
        return self.keep(v.cylinder(pos=start, axis=end-start, radius=radius, color=color(material)))

    def wall(self, axis, fixed, start, end, base, height, openings=(), material='ivory'):
        """Openings: (centre along wall, width, sill, opening height, glazed)."""
        def piece(a,b,low,h,mat=material,solid=True,**kw):
            if b-a < 0.001 or h < 0.001:
                return
            pos = ((a+b)/2,base+low+h/2,fixed) if axis == 'x' else (fixed,base+low+h/2,(a+b)/2)
            size = (b-a,h,0.24) if axis == 'x' else (0.24,h,b-a)
            return self.box(pos,size,mat,solid,**kw)
        cursor = start
        for centre,width,sill,h,glazed in sorted(openings):
            a,b = centre-width/2,centre+width/2
            piece(cursor,a,0,height)
            piece(a,b,0,sill)
            piece(a,b,sill+h,height-sill-h)
            # Window frames stand around a genuine hole, not on a solid wall.
            if glazed:
                piece(a,b,sill,h,'glass',True,opacity=0.24)
                for edge in (a,b):
                    piece(edge-0.045,edge+0.045,sill,h,'charcoal')
                for level in (sill,sill+h):
                    piece(a,b,level,0.075,'charcoal')
                piece(centre-0.035,centre+0.035,sill,h,'charcoal')
            cursor = b
        piece(cursor,end,0,height)

    def compound_since(self, start):
        objects = self.groups[self.group][start:]
        if objects:
            comp = v.compound(objects)
            self.groups[self.group][start:] = [comp]
            return comp

    def cutaway(self, mode):
        for obj in self.groups['roof']:
            obj.visible = mode == 'Full exterior'
        for obj in self.groups['upper']:
            obj.visible = mode != 'Ground floor'
