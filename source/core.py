import numpy as np
import scipy.spatial
import math
import itertools

import matplotlib.pyplot as plt


def are_points_far_enough(a, b):
    result = pow(abs(a[1] - b[1]), 2) + pow(abs(a[0] - b[0]), 2)
    if result < 0.06:
        return False
    else:
        return True


def create_new_middle_point(a, b):
    x = abs(a[1] + b[1]) / 2
    y = abs(a[0] + b[0]) / 2
    point = [x, y]
    return point


def filter_far_points_in_triangulation(tess, points):
    "buggy, two vertices might share more than one face, so duplicate points"
    remove = []
    add = []

    for face in tess.simplices:
        for verticeA, verticeB in itertools.combinations(face, 2):
            if are_points_far_enough(tess.points[verticeA], tess.points[verticeB]):
                remove.append(verticeA)
                remove.append(verticeB)
                add.append(create_new_middle_point(tess.points[verticeA], tess.points[verticeB]))

    print("Total points to be removed(might be duplicates): ", len(remove))
    print("Total points to be added: ", len(add))
    points = np.delete(points, remove, axis=0)
    points = np.append(points, add, axis=0)
    return points


# First create the x and y coordinates of the points.
n_angles = 20
n_radii = 10
min_radius = 0.15
radii = np.linspace(min_radius, 0.95, n_radii)
angles = np.linspace(0, 2 * math.pi, n_angles, endpoint=False)
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
angles[:, 1::2] += math.pi / n_angles
x = (radii * np.cos(angles)).flatten()
y = (radii * np.sin(angles)).flatten()

# Create the Delaunay tessalation using scipy.spatial
points = np.vstack([x, y]).T

print("Total initial points: ", len(points))

tess = scipy.spatial.Delaunay(points)
# Plotting
plt.triplot(x, y, tess.simplices.copy())
plt.plot(x, y, 'o')
plt.show()

remove = []
add = []

result = filter_far_points_in_triangulation(tess, points)
print("Total final points: ", len(result))

tess = scipy.spatial.Delaunay(points)
