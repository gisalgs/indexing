from prkdtree1 import *
from kdtree3 import * # use update_neighbors and INF

prmaxdist = INF

def prkdtree_nnquery(t, p, n, found, depth=0):
    global prmaxdist
    if t is None:
        return
    if t.is_leaf() and t.point is not None:               #*@\label{prkdtree3:diff1}
        prmaxdist = update_neighbors(t.point, p, found, n)
        return
    axis,dir = prkdcompare(t, p, depth)
    if dir<0:
        nearer_tree, farther_tree = t.left, t.right
    else:
        nearer_tree, farther_tree = t.right, t.left
    prkdtree_nnquery(nearer_tree, p, n, found, depth+1)
    #prmaxdist = update_neighbors(t.point, p, found, n)     #*@\label{prkdtree3:diff2}
    if (t.center-p[axis]) < prmaxdist:
        prkdtree_nnquery(farther_tree, p, n, found, depth+1)
    return

def nearest_neighbor_query(t, p, n=1):
    nearest_neighbors = []
    prkdtree_nnquery(t, p, n, nearest_neighbors)
    return nearest_neighbors[:n]

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
    n = 3
    p = Point(5,5)
    nearests = nearest_neighbor_query(t, p, n)
    print [x[0] for x in nearests[:n]]
    print [x[1] for x in nearests[:n]]
    print sorted([p.distance(x) for x in points])[:n]
