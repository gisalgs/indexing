"""
Point k-D trees. Part 1.

History
    October 13, 2017
        Python 3
        query_kdtree returns None, None when tree is empty

    December 4, 2016
        Function kdtree() now does not stop with duplicated points.

    November 2, 2016
        Added function depth

    October 31, 2016
        Function query_kdtree: now returns None if the point is found and is_find_only is False.
        This will explicitly exclude duplicated points from being inserted into the tree.

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

class kDTreeNode():
    """
    Node for point k-D trees.
    """
    def __init__(self, point, left, right):
        self.point = point
        self.left = left
        self.right = right
    def __repr__(self):
        return str(self.point)

def kdcompare(r, p, depth):
    """
    Returns the branch of searching on a k-d tree
    Input
       r: root
       p: point
       depth : starting depth of search
    Output
       A value of -1 (left branch), or 1 (right)
    """
    k = len(p)
    dim = depth%k
    if p[dim] <= r.point[dim]:
        return -1
    else:
        return 1

def kdtree(points):
    """
    Creates a point k-D tree using a predefined order of points
    """
    root = kDTreeNode(point=points[0], left=None, right=None)
    for p in points[1:]:
        node = kDTreeNode(point=p, left=None, right=None)
        p0, lr = query_kdtree(root, p, 0, False)
        if p0 is None and lr is None:   # skip if duplicated
            continue
        if lr<0:
            p0.left = node
        else:
            p0.right = node
    return root

def kdtree2(points, depth = 0):
    """
    Creates a point k-d tree using the median point to split the data
    """
    if len(points)==0:
        return
    k = len(points[0])
    axis = depth % k
    points.sort(key=lambda p: p[axis])
    pivot = len(points)//2
    return kDTreeNode(point=points[pivot],
                      left=kdtree2(points[:pivot], depth+1),
                      right=kdtree2(points[pivot+1:], depth+1))

def query_kdtree(t, p, depth=0, is_find_only=True):
    """
    Input
      t:            a node of a point k-D tree
      p:            target point to be found in the tree
      depth:        the depth of node t (default 0)
      is_find_only: True to find if p exists, or False to find the parent node of p

    Output
      t:            the node that contains p or None (is_find_only is True)
                    the node that should be the parent node of p (is_find_only is False)
      lr:           None (is_find_only is True)
                    -1 -- indicating p be the left child node of t (is_find_only is False)
                    1  -- indicating p be the right child node of t (is_find_only is False)
    """
    if t is None:
        return None, None
    if t.point == p:
        if is_find_only:
            return t, None
        else:
            return None, None
    lr = kdcompare(t, p, depth)
    if lr<0:
        child = t.left
    else:
        child = t.right
    if is_find_only==False and child is None:
        return t, lr
    return query_kdtree(child, p, depth+1, is_find_only)

def depth(t):
    """
    Returns the depth of the tree
    """
    if t == None:
        return -1
    return max(depth(t.left)+1, depth(t.right)+1)


if __name__ == '__main__':
    import sys
    sys.path.append('../geom')
    from point import *

    data1 = [ (2,2), (0,5), (8,0), (9,8),
              (7,14), (13,12), (14,13) ]
    points = [Point(d[0], d[1]) for d in data1]
    p = points[0]
    t1 = kdtree(points)
    t2 = kdtree2(points)

    print([ query_kdtree(t1, p)[0] for p in points ])
    print([ query_kdtree(t2, p)[0] for p in points ])
    print('Depth of t1:', depth(t1))
    print('Depth of t2:', depth(t2))
