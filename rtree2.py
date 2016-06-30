"""
R-tree, part 2

Contact:
Ningchuan Xiao
The Ohio State University
Columbus, OH
"""

__author__ = "Ningchuan Xiao <ncxiao@gmail.com>"

from math import ceil
from rtree1 import *

# e is an extent
def insert(node, e, child=None):
    for ent in node.entries:             # already in tree
        if ent.MBR == e:
            return True
    entry = Entry(extent=e, child=child) # create a new entry
    if len(node.entries) < node.M:       # there is room
        entry.node = node
        if entry.child is not None:
            entry.child.parent = entry
        node.entries.append(entry)
        node.update_up()
        return True
    M = node.M                           # overflowing node needs to be split
    m = ceil(float(M)/2)
    L1 = RTreeNode(M)
    L2 = RTreeNode(M)
    maxi, maxj = -1, -1
    maxdist = 0.0
    tmpentries = [ent for ent in node.entries]
    tmpentries.append(entry)
    M1 = len(tmpentries)
    # get the farthest apart MBRs as seeds
    for i in range(M1):
        for j in range(i+1, M1):
            d = tmpentries[i].MBR.distance(tmpentries[j].MBR)
            if d>maxdist:
                maxdist = d
                maxi = i
                maxj = j
    e1 = tmpentries[maxi]
    e2 = tmpentries[maxj]
    allexts = []              # holds the rest of the MBRs
    for ext in tmpentries:
        if ext is not e1 and ext is not e2:
            allexts.append(ext)
    L1.entries.append(e1)
    L2.entries.append(e2)
    L1.update()
    L2.update()
    while len(allexts):
        numremained = len(allexts)
        gotonode = None
        if len(L1.entries) == m-numremained:
            gotonode = L1
        elif len(L2.entries) == m-numremained:
            gotonode = L2
        if gotonode is not None:
            while len(allexts): 
                ext = allexts.pop()
                gotonode.entries.append(ext)
        else:
            minarea = union_extent(L1.extent,L2.extent).area()
            minext = -1
            gotonode = None
            for i in range(len(allexts)):
                tmpext1  = union_extent(L1.extent,
                                        allexts[i].MBR)
                tmparea1 = tmpext1.area() - L1.extent.area()
                tmpext2  = union_extent(L2.extent,
                                        allexts[i].MBR)
                tmparea2 = tmpext2.area() - L2.extent.area()
                if min(tmparea1, tmparea2) > minarea:
                    continue
                minext  = i
                if tmparea1 < tmparea2:
                    if tmparea1 < minarea:
                        tmpgotonode = L1
                        minarea = tmparea1
                elif tmparea2 < tmparea1:
                    if tmparea2 < minarea:
                        tmpgotonode = L2
                        minarea = tmparea2
                else: 
                    minarea = tmparea1
                    if L1.extent.area() < L2.extent.area():
                        tmpgotonode = L1
                    elif L2.extent.area() < L1.extent.area():
                        tmpgotonode = L2
                    else:
                        if len(L1.entries) < len(L2.entries):
                            tmpgotonode = L1
                        else:
                            tmpgotonode = L2
            if minext <> -1 and tmpgotonode is not None:
                ext = allexts.pop(minext)
                gotonode = tmpgotonode
            gotonode.entries.append(ext)
        gotonode.update()
        for ent in L1.entries:
            ent.node = L1
            if ent.child is not None:
                ent.child.parent = ent
        for ent in L2.entries:
            ent.node = L2
            if ent.child is not None:
                ent.child.parent = ent
    split(node, L1, L2)
    L1.update_up()
    L2.update_up()
    return True
    
def split(node, L1, L2):
    entry1 = Entry(L1.extent)
    entry2 = Entry(L2.extent)
    if node.is_root():
        node.entries = [] 
        entry1.node = node
        entry2.node = node
        entry1.child = L1
        entry2.child = L2
        node.entries.append(entry1)
        node.entries.append(entry2)
        L1.parent = entry1
        L2.parent = entry2
        return 
    else: 
        entry1.node = L1
        L1.parent = node.parent
        L1.parent.child = L1
        del node
        insert(L1.parent.node, L2.extent, L2)
        return 

def search_rtree_extent(node, e):
    if node.is_leaf():
        return node
    best_entry = None
    intersect_area = -1
    for ent in node.entries:
        tmp_area = ent.MBR.intersect(e)
        if tmp_area > intersect_area:
            intersect_area = tmp_area
            best_entry = ent
    return search_rtree_extent(best_entry.child, e)
        
