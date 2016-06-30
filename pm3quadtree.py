from xdcel import *
from pmquadtree import *
import pickle

def split_by_edges_pm3(edges, pmq):
    subedges = []
    for e in edges:
        if is_intersect(pmq.extent, e):
            subedges.append(e)
        elif pmq.extent.contains(e.fr) and\
        pmq.extent.contains(e.to):
            subedges.append(e)
    if not pmq.is_leaf():
        for i in range(4):
            split_by_edges_pm3(subedges, pmq.quads[i])
        return
    if len(subedges) == 0:
        pmq.type = WHITE
        return
    else:
        pmq.type = BLACK
        for e in subedges:
            pmq.edges.append(e)
        return

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

    pm3q = PMQuadTreeNode(extent.getcenter(), extent)
    split_by_points(XD.vertices, pm3q)
    split_by_edges_pm3(XD.edges, pm3q)
    print search_pmquadtree(pm3q, 1, 1)

if __name__ == '__main__':
    test()
