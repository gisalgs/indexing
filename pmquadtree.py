# Used by all PM quadtrees
import sys
sys.path.append('../geom')
from point import *
from linesegment import Segment
from intersection import test_intersect
from extent import *

BLACK = 2 # nodes with point or line
WHITE = 1 # nodes with no point or line intersecing
GREY  = 0 # intermediate nodes

class PMQuadTreeNode():
    def __init__(self, point, extent,
                 nw=None, ne=None, se=None, sw=None):
        self.point = point # center
        self.extent = extent
        self.quads = [nw, ne, se, sw]
        self.vertex = None
        self.edges = []
        self.type = GREY
    def __repr__(self):
        return str(self.point)
    def __getitem__(self, i):
        if i<4: return self.quads[i]
        return None
    def is_leaf(self):
        return sum([ q is None for q in self.quads])==4

def split_by_points(points, pmq):
    if len(points) == 1:
        pmq.vertex = points[0]
        pmq.type = BLACK
        return
    if len(points) ==0:
        pmq.type = WHITE
        return
    xmin = pmq.extent.xmin
    xmax = pmq.extent.xmax
    ymin = pmq.extent.ymin
    ymax = pmq.extent.ymax
    xmid = xmin + (xmax-xmin)/2.0
    ymid = ymin + (ymax-ymin)/2.0
    exts = [ Extent(xmin, xmid, ymid, ymax), # nw
             Extent(xmid, xmax, ymid, ymax), # ne
             Extent(xmid, xmax, ymin, ymid), # se
             Extent(xmin, xmid, ymin, ymid)  # sw
    ]
    pmq.quads = [PMQuadTreeNode(exts[i].getcenter(),exts[i])
                 for i in range(4)] 
    subpoints = [[], [], [], []]     # four empty points lists
    for p in points:
        for i in range(4):
            if exts[i].contains(p):
                subpoints[i].append(p)
    for i in range(4):
        split_by_points(subpoints[i], pmq.quads[i])

def search_pmquadtree(pmq, x, y):
    if pmq.type is not GREY:
        return pmq
    for q in pmq.quads:
        if q.extent.contains(Point(x, y)):
            return search_pmquadtree(q, x, y)
    return None

def is_intersect(extent, edge):
    if not extent.touches(edge.extent()):
        return False
    # four corners clockwise
    p1 = Point(extent.xmin, extent.ymin)
    p2 = Point(extent.xmin, extent.ymax)
    p3 = Point(extent.xmax, extent.ymax)
    p4 = Point(extent.xmax, extent.ymin)
    segs = [ Segment(0, p1, p2), Segment(1, p2, p3),
             Segment(2, p3, p4), Segment(3, p4, p1) ]
    s0 = Segment(4, edge.fr, edge.to)
    for s in segs:
        if test_intersect(s, s0):
            return True
    return False
