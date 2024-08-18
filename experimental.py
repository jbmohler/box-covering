import math
import itertools
import random

def nzrandom():
    while True:
        z = random.random()
        if z > 0:
            return z

def random_sphere(n):
    center = [nzrandom() for _ in range(n)]
    max_radius = min([min([c-0., 1.-c]) for c in center])
    assert max_radius > 0
    return center, nzrandom()*max_radius


def distance(p1, p2):
    return math.sqrt(sum([(a-b)**2 for a, b in zip(p1, p2)]))

def cube_grid_points(p, center, r):
    range_limits = [(math.ceil((c-r)*p), math.floor((c+r)*p)) for c in center]
    range_coords = [list(range(l, u+1)) for l, u in range_limits]

    yield from itertools.product(*range_coords)

def filter_grid_points(p, center, r):
    resolution = 1./p
    for v in cube_grid_points(p, center, r):
        # print(v)
        if distance(center, [g * resolution for g in v])<= r:
            yield v

def process(n, p):
    assert n >= 1
    assert p >= 2

    covered = set()
    count = 0

    precision = math.ceil(math.log10(p)) + 2
    rnd = lambda v: f"{v:.{precision}f}"
    resolution = 1./p

    while len(covered) < (p-1)**n:
        center, radius = random_sphere(n)

        sphere_coverage = list(filter_grid_points(p, center, radius))

        t1 = len(covered)
        covered |= set(sphere_coverage)
        t2 = len(covered)

        # print(f"placed sphere ({', '.join(rnd(c) for c in center)}) with radius {rnd(radius)} -- covered {len(sphere_coverage)}; added {t2-t1}")

        count += 1

    return count

if __name__ == '__main__':
    import sys
    import statistics

    n, p = int(sys.argv[1]), int(sys.argv[2])

    for p in range(2, 50):
        print(f"cover {(p-1)**n} points in the unit {n}-cube")

        xx = [process(n, p) for index in range(1000)]
        print(statistics.mean(xx))
