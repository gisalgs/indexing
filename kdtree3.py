"""
k-D trees. Part 3.

Nearest neighbor search using k-D trees

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from kdtree1 import *

INF = float('inf')
maxdist = INF

def update_neighbors(p0, p, neighbors, n):
    d = p0.distance(p)
    for i, x in enumerate(neighbors):
        if i == n:
            return neighbors[n-1][1]
        if d < x[1]:
            neighbors.insert(i, [p0, d])
            if len(neighbors) < n:
                return INF
            return neighbors[n-1][1]
    neighbors.append([p0, d])
    return INF

def nnquery(t, p, n, found, depth=0):
    global maxdist
    if t is None:
        return
    if t.left == None and t.right == None:
        maxdist = update_neighbors(t.point, p, found, n)
        return
    axis = depth % len(p)
    if p[axis] < t.point[axis]:
        nearer_tree, farther_tree = t.left, t.right
    else:
        nearer_tree, farther_tree = t.right, t.left
    nnquery(nearer_tree, p, n, found, depth+1)
    maxdist = update_neighbors(t.point, p, found, n)
    if (t.point.distance(p)) < maxdist:
        nnquery(farther_tree, p, n, found, depth+1)
    return

def kdtree_nearest_neighbor_query(t, p, n=1):
    nearest_neighbors = []
    nnquery(t, p, n, nearest_neighbors)
    return nearest_neighbors[:n]

if __name__ == '__main__':
    data1 = [ (2,2), (0,5), (8,0), (9,8), (7,14),
              (13,12), (14,13) ]
    points = [Point(d[0], d[1]) for d in data1]
    p = Point(5,5)
    t1 = kdtree(points)
    n = 3
    nearests = []
    nnquery(t1, p, n, nearests)
    print [x[0] for x in nearests[:n]]
    print [x[1] for x in nearests[:n]]
    print sorted([p.distance(x) for x in points])[:n]
