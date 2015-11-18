def range_query(t, p, r):
    def rquery(t, p, r, found):
        if t is None:
            return
        if p.x-r > t.point.x :
            rquery(t.ne, p, r, found)  # right points only
            rquery(t.se, p, r, found)
            return
        if p.y-r > t.point.y: 
            rquery(t.ne, p, r, found)  # above points only
            rquery(t.nw, p, r, found)
            return
        if p.x+r < t.point.x: 
            rquery(t.nw, p, r, found)  # left points only
            rquery(t.sw, p, r, found)
            return
        if p.y+r < t.point.y: 
            rquery(t.se, p, r, found)  # below points only
            rquery(t.sw, p, r, found)
            return
        if p.distance(t.point) <= r:
            found.append(t.point)
        rquery(t.nw, p, r, found)
        rquery(t.ne, p, r, found)
        rquery(t.se, p, r, found)
        rquery(t.sw, p, r, found)
        return
    found = []
    if t is not None:
        rquery(t, p, r, found)
    return found
