from bisect import *

class PRKDTreeNode():
    def __init__(self, xyrange, center, point, left, right):
        self.xyrange = xyrange # ranges of xy
        self.center = center   # center coordinate
        self.point = point     # point
        self.left = left       # left child subtree
        self.right = right     # right child subtree
    def is_leaf(self):
        return (self.left == None and self.right == None)
    def __repr__(self):
        return str(self.center)

# r-root node of a subtree, p-point, depth-current depth
def prkdcompare(r, p, depth):
    k = len(p)
    dim = depth%k
    if p[dim] <= r.center:
        return dim,-1      # left
    else:
        return dim,1       # right

def prkdtree(points, xylim, center=None, depth=0):
    if len(points)==1:
        return PRKDTreeNode(xyrange=xylim,
                            center=center,
                            point=points[0],
                            left=None,
                            right=None)
    if len(points)==0:
        return PRKDTreeNode(xyrange=xylim,
                            center=center,
                            point=None,
                            left=None,
                            right=None)
    k = len(points[0])
    axis = depth % k
    pmid = (xylim[axis][1]+xylim[axis][0])/2.0
    points.sort(key=lambda points:points[axis])
    P = [p[axis] for p in points]
    pivot = bisect(P, pmid) # includes all <=
    xmin,xmax=xylim[0][0], xylim[0][1]
    ymin,ymax=xylim[1][0], xylim[1][1]
    rangel = [ [xmin, xmax], [ymin, ymax] ]
    rangel[axis][1] = pmid
    ranger = [ [xmin, xmax], [ymin, ymax] ]
    ranger[axis][0] = pmid
    axis2 = (depth+1) % k
    pmidl = (rangel[axis2][0]+rangel[axis2][1])/2.0
    pmidr = (ranger[axis2][0]+ranger[axis2][1])/2.0
    return PRKDTreeNode(xyrange = xylim,
                        center = pmid,
                        point = None,
                        left=prkdtree(points[:pivot],
                                      rangel,pmidl,depth+1),
                        right=prkdtree(points[pivot:],
                                       ranger,pmidr,depth+1))

# query if point p is in t
def query_prkdtree(t, p, depth=0):
    if t is None:
        return
    if t.point == p:
        return p
    if t.is_leaf():
        return
    if prkdcompare(t, p, depth)[1] < 0:
        next = t.left
    else:
        next = t.right
    p0 = query_prkdtree(next, p, depth+1)
    if p0 is not None:
        return p0
    return

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
    print [query_prkdtree(t, p) for p in points]
