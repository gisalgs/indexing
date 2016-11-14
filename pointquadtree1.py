"""
Point quadtree. Part 1.

History:

  November 12, 2016

    The search_pqtree function now returns None if the point is found and
    is_find_only is set to False so that points will not be duplicated
    in the tree.

  November 19, 2015

      changed the two conditions in search_pqtree to:
         if p.x>=q.point.x
      and
         if p.y>=q.point.y

      This forces the consistency in how the four quads are determined in
      functions search_pqtree and insert_pqtree
      (Thanks to Hui Kong for examining the code!)

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

class PQuadTreeNode():
    def __init__(self,point,nw=None,ne=None,se=None,sw=None):
        self.point = point
        self.nw = nw
        self.ne = ne
        self.se = se
        self.sw = sw
    def __repr__(self):
        return str(self.point)
    def is_leaf(self):
        return self.nw==None and self.ne==None and \
            self.se==None and self.sw==None

def search_pqtree(q, p, is_find_only=True):
    if q is None:
        return
    if q.point == p:
        if is_find_only:
            return q
        else:
            return
    dx,dy = 0,0
    if p.x >= q.point.x:
        dx = 1
    if p.y >= q.point.y:
        dy = 1
    qnum = dx+dy*2
    child = [q.sw, q.se, q.nw, q.ne][qnum]
    if child is None and not is_find_only:
        return q
    return search_pqtree(child, p, is_find_only)

def insert_pqtree(q, p):
    n = search_pqtree(q, p, False)
    node = PQuadTreeNode(point=p)
    if p.x < n.point.x and p.y < n.point.y:
        n.sw = node
    elif p.x < n.point.x and p.y >= n.point.y:
        n.nw = node
    elif p.x >= n.point.x and p.y < n.point.y:
        n.se = node
    else:
        n.ne = node

def pointquadtree(data):
    root = PQuadTreeNode(point = data[0])
    for p in data[1:]:
        insert_pqtree(root, p)
    return root
