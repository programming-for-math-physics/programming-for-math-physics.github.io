class BoundingBox:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
    def union(self, bb):
        x0 = min(self.x0, bb.x0)
        y0 = min(self.y0, bb.y0)
        x1 = max(self.x1, bb.x1)
        y1 = max(self.y1, bb.y1)
        return BoundingBox(x0, y0, x1, y1)

class closed_shape:
    def __init__(self, **kw):
        self.set(stroke="black", fill="none")
        self.set(**kw)
    def set(self, **kw):
        self.__dict__.update(kw)
        return self
    def to_svg(self):
        attrs = [ ('%s="%s"' % (k.replace("_", "-"),v)) for k,v in self.__dict__.items() ]
        return "<%s %s />" % (self.__class__.__name__, " ".join(attrs))
        
class circle(closed_shape):
    def __init__(self, c, r, **kw):
        super().__init__(**kw)
        self.cx, self.cy = c
        self.r = r
    def bounding_box(self):
        cx = self.cx
        cy = self.cy
        r = self.r
        return BoundingBox(cx - r, cy - r, cx + r, cy + r)

class rect(closed_shape):
    def __init__(self, xy, width, height, **kw):
        super().__init__(**kw)
        self.x,self.y = xy
        self.width = width
        self.height = height
    def bounding_box(self):
        return BoundingBox(self.x, self.y, 
                           self.x + self.width, self.y + self.height)

class line(closed_shape):
    def __init__(self, xy1, xy2, **kw):
        super().__init__(**kw)
        self.x1,self.y1 = xy1
        self.x2,self.y2 = xy2
    def bounding_box(self):
        return BoundingBox(self.x1, self.y1, self.x2, self.y2)

class SVGCanvas:
    def __init__(self):
        self.shapes = []
    def add(self, shape):
        self.shapes.append(shape)
    def bounding_box(self):
        bb = self.shapes[0].bounding_box()
        for shape in self.shapes[1:]:
            bb = bb.union(shape.bounding_box())
        return bb
    def draw(self, filename):
        bb = self.bounding_box()
        w = bb.x1 - bb.x0
        h = bb.y1 - bb.y0
        wp = open(filename, "w")
        wp.write("""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<svg 
    xmlns="http://www.w3.org/2000/svg"
    width="%d"
    height="%d"
    viewBox="%d %d %d %d"
>
""" % (w, h, bb.x0, bb.y0, w, h))
        for shape in self.shapes:
            wp.write("""%s\n""" % shape.to_svg())
        wp.write("""</svg>\n""")
        wp.close()

def main():
    c = SVGCanvas()
    m = 10
    n = 5
    r = 5
    s = 50
    for i in range(m):
        c.add(line((i * s, 0), (i * s, (n - 1) * s)))
    for j in range(n):
        if j == 0 or j == n - 1:
            c.add(line((- 2 * s, j * s), ((m + 1) * s, j * s), stroke_width=3))
        else:
            c.add(line((0, j * s), ((m - 1) * s, j * s)))
    for i in range(m):
        for j in range(n):
            if i == 0 or i == m - 1 or j == 0 or j == n - 1:
                c.add(rect((i * s - r, j * s - r), width=2 * r, height=2 * r, fill="black"))
            else:
                c.add(circle((i * s, j * s), r, fill="black"))
    c.draw("a.svg")

main()

        
