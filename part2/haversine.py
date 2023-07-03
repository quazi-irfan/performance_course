def haversine_distance(lon1, lat1, lon2, lat2):
    from math import sin, cos, asin, sqrt

    c = 0.01745329251994329577
    dLat = (lat2 - lat1) * c
    dLon = (lon2 - lon1) * c
    lat1, lat2 = lat1 * c, lat2 * c

    a = (sin(dLat / 2.0) ** 2) + cos(lat1) * cos(lat2) * (sin(dLon / 2.0) ** 2)
    d = (2 * asin(sqrt(a))) * 6372.8

    return d