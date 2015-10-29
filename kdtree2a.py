"""
k-D trees, Part 2a.

Rectangle range query of point k-D trees

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from kdtree1 import *

def range_query_orthogonal(t, rect, found, depth=0):
    """
    Orthogonal (rectangular) range search for points

    Input
      t: node of a point k-D tree
      rect: 2D list defining a rectangle as [ [xmin, xmax], [ymin, ymax] ]
      found: a list to hold points found, declared outside

    Output
      This function does not return any values. However, all the points 
      found during the query process will be appended to list found.
    """
    if t is None:
        return
    k = len(t.point)
    axis = depth%k
    if t.point[axis] < rect[axis][0]:
        range_query_orthogonal(t.right, rect, found, depth+1) 
        return
    if t.point[axis] > rect[axis][1]:
        range_query_orthogonal(t.left, rect, found, depth+1) 
        return
    x, y = t.point.x, t.point.y
    if not (rect[0][0]>x or rect[0][1]<x or
            rect[1][0]>y or rect[1][1]<y):
        found.append(t.point)
    range_query_orthogonal(t.left, rect, found, depth+1)
    range_query_orthogonal(t.right, rect, found, depth+1)
    return

def test():
    data1 = [ (2,2), (0,5), (8,0), (9,8), (7,14),
              (13,12), (14,13) ]
    points = [Point(d[0], d[1]) for d in data1]
    t1 = kdtree(points)
    rect = [ [1, 9], [2, 9] ]
    found = []
    range_query_orthogonal(t1, rect, found)
    print found

if __name__ == '__main__':
    test()
