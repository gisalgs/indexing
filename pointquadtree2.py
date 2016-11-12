"""
Point quadtree. Part 2.

Circular range query

History
  November 23, 2015
  Add more conditions to further speed up search.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

def range_query(t, p, r):
    def rquery(t, p, r, found):
        if t is None:
            return
        x, y = t.point.x, t.point.y
        xmin, xmax = p.x-r, p.x+r
        ymin, ymax = p.y-r, p.y+r
        if x<xmin and y<ymin:
            rquery(t.ne, p, r, found)
            return
        elif x<xmin and y>ymax:
            rquery(t.se, p, r, found)
            return
        elif x>xmax and y>ymax:
            rquery(t.sw, p, r, found)
            return
        elif x>xmax and y<ymin:
            rquery(t.nw, p, r, found)
            return
        else:
            if x < xmin:
                rquery(t.ne, p, r, found)  # right points only
                rquery(t.se, p, r, found)
                return
            if y < ymin:
                rquery(t.ne, p, r, found)  # above points only
                rquery(t.nw, p, r, found)
                return
            if x > xmax:
                rquery(t.nw, p, r, found)  # left points only
                rquery(t.sw, p, r, found)
                return
            if y > ymax:
                rquery(t.se, p, r, found)  # below points only
                rquery(t.sw, p, r, found)
                return
        if p.distance(t.point) <= r:
            found.append(t.point)
        rquery(t.nw, p, r, found)
        rquery(t.ne, p, r, found)
        rquery(t.se, p, r, found)
        rquery(t.sw, p, r, found)
        return
    found = []
    if t is not None:
        rquery(t, p, r, found)
    return found

def test():
    count = 0
    data = [ [i, j] for i in range(100) for j in range(100) ]
    points = [Point(d[0], d[1]) for d in data]
    q = pointquadtree(points)
    time1 = time.time()
    found = range_query(q, Point(50, 50), 2)
    time2 = time.time()
    print count
    print found
    print time2-time1

if __name__ == "__main__":
    import sys
    sys.path.append('../geom')
    from point import *
    from pointquadtree1 import *
    import time
    test()
