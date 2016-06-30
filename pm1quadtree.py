from pmquadtree import *

def split_by_edges_pm1(edges, pmq):
    subedges = []
    for e in edges:
        if is_intersect(pmq.extent, e):
            subedges.append(e)
        elif pmq.extent.contains(e.fr) and\
        pmq.extent.contains(e.to):
            subedges.append(e)
    if len(subedges) == 0:
        pmq.type = WHITE
        return
    if pmq.vertex is not None:
        is_same_source = True
        for e in subedges:
            if not e.is_endpoint(pmq.vertex):
                is_same_source = False
        if is_same_source:
            for e in subedges:
                pmq.edges.append(e)
            pmq.type = BLACK
            return
    else: # pmq does not contain a vertex
        if len(subedges) == 1:
            pmq.type = BLACK
            pmq.edges.append(subedges[0])
            return
    if pmq.extent.is_minimal():
        for e in subedges:
            pmq.edges.append(e)
        pmq.type = BLACK
        return
    if pmq.is_leaf():  # now we split this if necessary:
        xmin = pmq.extent.xmin
        xmax = pmq.extent.xmax
        ymin = pmq.extent.ymin
        ymax = pmq.extent.ymax
        xmid = xmin + (xmax-xmin)/2.0
        ymid = ymin + (ymax-ymin)/2.0
        exts = [ Extent(xmin, xmid, ymid, ymax), # nw
                 Extent(xmid, xmax, ymid, ymax), # ne
                 Extent(xmid, xmax, ymin, ymid), # se
                 Extent(xmin, xmid, ymin, ymid)  # sw
             ]
        pmq.quads = [ PMQuadTreeNode(exts[i].getcenter(),
                                     exts[i])
                      for i in range(4) ]
    if pmq.vertex:
        for q in pmq.quads:
            if q.extent.contains(pmq.vertex):
                q.vertex = pmq.vertex
        pmq.vertex = None
    for i in range(4):
        split_by_edges_pm1(subedges, pmq.quads[i])

