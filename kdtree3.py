"""
k-D trees. Part 3.

Nearest neighbor search using point k-D trees

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

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
    if abs(t.point[axis]-p[axis]) < maxdist: # must check the far side
        nnquery(farther_tree, p, n, found, depth+1)
    return

def kdtree_nearest_neighbor_query(t, p, n=1):
    nearest_neighbors = []
    nnquery(t, p, n, nearest_neighbors)
    return nearest_neighbors[:n]
