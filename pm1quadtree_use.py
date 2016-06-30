import pickle
from pm1quadtree import *
from xdcel import *

import sys
sys.path.append('../contrib')
from dcel import *

D = pickle.load(open('../data/mydcel.pickle'))
XD = Xdcel(D)

X = [v.x for v in D.vertices]
Y = [v.y for v in D.vertices]
xmin,xmax,ymin,ymax = min(X)-1, max(X)+1, min(Y)-1, max(Y)+1
maxmax = max(xmax,ymax)
xmax=ymax=maxmax
extent = Extent(xmin, xmax, ymin, ymax)

pmq = PMQuadTreeNode(extent.getcenter(), extent)
split_by_points(XD.vertices, pmq)
split_by_edges_pm1(XD.edges, pmq)
print search_pmquadtree(pmq, 1, 1)
print search_pmquadtree(pmq, 1, 2)
print search_pmquadtree(pmq, 6, 5)
