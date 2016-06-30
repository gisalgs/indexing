"""
Example of using R-tree

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from rtree1 import *
from rtree2 import *

MBRs = [ [10,17,3,7],   # R14
         [12,16,4,6],   # R12
         [7,9,0,5],     # R10
         [1,8,1,4],     # R11
         [1,2,6,11],    # R8
         [15,18,0,2],   # R13
         [0,3,3,12],    # R9
         [13,15,14,18], # R16
         [10,18,12,15], # R15
         [14,17,9,16] ] # R17

M = 3
root = RTreeNode(M, None)

extents = [Extent(mbr[0], mbr[1], mbr[2], mbr[3])
           for mbr in MBRs]
for e in extents:
    n = search_rtree_extent(root, e)
    insert(n, e)

root.get_all_leaves()
