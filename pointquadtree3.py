"""
Point quadtree. Part 3.

Nearest neighbor query

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

INF = float('inf')
pqmaxdist = INF

import sys
sys.path.append('..')
from indexing.kdtree3 import *

# returns the quad of t where p is located
# 0-NW, 1-NE, 2-SE, 3-SW
def pqcompare(t, p):
    if p.x<t.point.x and p.y<t.point.y:
        return 3 # sw
    elif p.x<t.point.x and p.y>=t.point.y:
        return 0
    elif p.x>=t.point.x and p.y<t.point.y:
        return 2
    else:
        return 1

def pq_nnquery(t, p, n, found):
    global pqmaxdist
    if t is None:
        return
    if t.is_leaf():
        pqmaxdist = update_neighbors(t.point, p, found, n)
        return
    quad_index = pqcompare(t, p)
    quads = [t.nw, t.ne, t.se, t.sw]
    pq_nnquery(quads[quad_index], p, n, found)
    pqmaxdist = update_neighbors(t.point, p, found, n)
    # check if the circle of pqmaxdist overlap with other quads
    for i in range(4):
        if i != quad_index:
            if abs(t.point.x-p.x) < pqmaxdist or abs(t.point.y-p.y) < pqmaxdist:
                pq_nnquery(quads[i], p, n, found)
    return

def pq_nearest_neighbor_query(t, p, n=1):
    nearest_neighbors = []
    pq_nnquery(t, p, n, nearest_neighbors)
    return nearest_neighbors[:n]
