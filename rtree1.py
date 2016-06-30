"""
R-tree, part 1

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from extent import *

class Entry():
    def __init__(self, extent=None, child=None,
                 parent=None, node=None):
        self.MBR = extent
        self.child = child     # a child node
        self.node = node       # node containing this entry
    def __repr__(self):
        return str(self.MBR)

class RTreeNode():
    def __init__(self, M, parent=None):
        self.entries = []
        self.M = M
        self.parent = parent   # an entry in the parent node
        self.extent = None
    def __getitem__(self, i):
        if i>=self.M or i>=len(self.entries):
            return None
        return self.entries[i]
    def __repr__(self):
        return str(self.extent)
    def is_leaf(self):
        for e in self.entries:
            if e.child is not None:
                return False
        return True
    def is_root(self):
        return self.parent is None
    def update(self):
        if not len(self.entries):
            return
        if self.entries[0] is not None:
            self.extent = self.entries[0].MBR
        for e in self.entries[1:]:
            self.extent = union_extent(self.extent, e.MBR)
    def update_up(self):
        self.update()
        if self.is_root():
            return
        self.parent.MBR = self.extent
        self.parent.node.update_up()
    def get_all_leaves(self, depth=0):
        if not self.is_leaf():
            for e in self.entries:
                e.child.get_all_leaves(depth+1)
        else:
            print depth, "-", self, self.entries
            return

def union_extent(e1, e2):
    xmin = min(e1.xmin, e2.xmin)
    xmax = max(e1.xmax, e2.xmax)
    ymin = min(e1.ymin, e2.ymin)
    ymax = max(e1.ymax, e2.ymax)
    return Extent(xmin, xmax, ymin, ymax)
