from prkdtree1 import *

# range search for points within a radius of r around p
def range_query(t, p, r):
    def rquery(t, p, r, found, depth=0):
        if t is None:
            return
        w = t.xyrange[0][1] - t.xyrange[0][0]
        h = t.xyrange[1][1] - t.xyrange[1][0]
        if prkdcompare(t, Point(p.x-r-w, p.y-r-h),
                       depth)[1] > 0:
            rquery(t.right, p, r, found, depth+1)
            return
        if prkdcompare(t, Point(p.x+r+w, p.y+r+h),
                       depth)[1] < 0:
            rquery(t.left, p, r, found, depth+1)
            return
        if t.point is not None:
            if p.distance(t.point) <= r:
                found.append(t.point)
        rquery(t.left, p, r, found, depth+1)
        rquery(t.right, p, r, found, depth+1)
        return
    found = []
    if t is not None:
        rquery(t, p, r, found)
    return found

if __name__ == '__main__':
    import sys
    sys.path.append('../')
    from geom.point import *
    data1 = [ (2,2), (0,5), (8,0), (9,8), (7,14),
              (13,12), (14,13) ]
    points = [Point(d[0], d[1]) for d in data1]
    px = [p.x for p in points]
    py = [p.y for p in points]
    xmin = min(px)
    xmax = max(px)
    ymin = min(py)
    ymax = max(py)
    xylim = [ [xmin, xmax], [ymin, ymax] ]
    t = prkdtree(points, xylim)
    p = Point(5,5)
    print range_query(t, p, 5)
