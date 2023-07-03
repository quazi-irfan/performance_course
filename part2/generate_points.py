def generate_hd_points_and_distances(n, seed, output_json, output_hd):
    import random, json, statistics
    from math import sin, cos, asin, sqrt
    import haversine

    random.seed(seed)
    v = int(statistics.NormalDist(0, 25).samples(1)[0])

    clustered = True
    dict_data = {'pairs': []}
    hd_data = []

    ci = [
            [[-180, 180], [-90, 90]],
            [[-150, 30], [30, 60]],
            [[30, 150], [30, 60]],
            [[-150, 30], [-60, 30]],
            [[30, 150], [-60, 30]]
    ]

    # https://journeynorth.org/tm/LongitudeIntro.html
    for i in range(n):

        index = 0 if not clustered else random.randint(1, 4)

        lon1, lat1 = random.uniform(ci[index][0][0]-v, ci[index][0][1]+v), random.uniform(ci[index][1][0]-v, ci[index][1][1]+v)
        lon2, lat2 = random.uniform(ci[index][0][0]-v, ci[index][0][1]+v), random.uniform(ci[index][1][0]-v, ci[index][1][1]+v)
        # lon1, lat1 = random.randint(-180, 180), random.randint(-90, 90)
        # lon2, lat2 = random.randint(-180, 180), random.randint(-90, 90)

        dict_data['pairs'].append(
            {'x0': lon1,
             'y0': lat1,
             'x1': lon2,
             'y1': lat2}
        )

        distance = haversine.haversine_distance(lon1, lat1, lon2, lat2)
        # c = 0.01745329251994329577
        # dLat = (lat2 - lat1) * c
        # dLon = (lon2 - lon1) * c
        # lat1, lat2 = lat1 * c, lat2 * c
        #
        # a = (sin(dLat/2.0) ** 2) + cos(lat1) * cos(lat2) * (sin(dLon/2.0) ** 2)
        # d = (2 * asin(sqrt(a))) * 6372.8
        hd_data.append(distance)

    hd_data.append(statistics.mean(hd_data))

    with open(output_json, 'w') as o1:
        print(json.dumps(dict_data), file=o1)

    with open(output_hd, 'w') as o2:
        print(*hd_data, sep='\n', file=o2)


import time
generate_hd_points_and_distances(100_000, int(time.time()), 'json_points', 'distances')


