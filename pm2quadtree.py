from xdcel import *
from pmquadtree import *
import pickle

def split_by_edges_pm2(edges, pmq):
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
    elif len(subedges) == 1:
        pmq.type = BLACK
        pmq.edges.append(subedges[0])
        return
    else:
        p1,p2 = subedges[0].fr, subedges[0].to
        common_vertex = None
        if subedges[1].is_endpoint(p1):
            common_vertex = p1
        elif subedges[1].is_endpoint(p2):
            common_vertex = p2
        if common_vertex is not None:
            for e in subedges[2:]:
                if not e.is_endpoint(common_vertex):
                    common_vertex = None
                    break
        if common_vertex is not None:
            for e in subedges:
                pmq.edges.append(e)
            pmq.type = BLACK
            return
    if pmq.extent.is_minimal():
        for e in subedges:
            pmq.edges.append(e)
        pmq.type = BLACK
        return
    if pmq.is_leaf():
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
        split_by_edges_pm2(subedges, pmq.quads[i])

def test():
    D = pickle.load(open('../data/mydcel.pickle'))
    XD = Xdcel(D)

    X = [v.x for v in D.vertices]
    Y = [v.y for v in D.vertices]
    xmin,xmax,ymin,ymax = min(X)-1, max(X)+1,\
                          min(Y)-1, max(Y)+1
    maxmax = max(xmax,ymax)
    xmax=ymax=maxmax
    extent = Extent(xmin, xmax, ymin, ymax)

    pm2q = PMQuadTreeNode(extent.getcenter(), extent)
    split_by_points(XD.vertices, pm2q)
    split_by_edges_pm2(XD.edges, pm2q)
    print search_pmquadtree(pm2q, 10, 10)

if __name__ == '__main__':
    test()
    
