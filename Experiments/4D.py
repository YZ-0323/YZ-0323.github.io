import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
X = 18909223
Y = 37203685
Z = 4775807
W = 75807 
cube4D = np.array([
    [-1, -1, -1, -1], [1, -1, -1, -1],
    [-1, 1, -1, -1], [1, 1, -1, -1],
    [-1, -1, 1, -1], [1, -1, 1, -1],
    [-1, 1, 1, -1], [1, 1, 1, -1],
    [-1, -1, -1, 1], [1, -1, -1, 1],
    [-1, 1, -1, 1], [1, 1, -1, 1],
    [-1, -1, 1, 1], [1, -1, 1, 1],
    [-1, 1, 1, 1], [1, 1, 1, 1]
])
edges = [
    (0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
    (2, 6), (3, 7), (4, 5), (4, 6), (5, 7), (6, 7),
    (8, 9), (8, 10), (8, 12), (9, 11), (9, 13), (10, 11),
    (10, 14), (11, 15), (12, 13), (12, 14), (13, 15), (14, 15),
    (0, 8), (1, 9), (2, 10), (3, 11), (4, 12), (5, 13),
    (6, 14), (7, 15)
]
def project_4D_to_3D(points, w_factor):
    projection = []
    for p in points:
        w = 1 / (2 - w_factor * p[3]) 
        projection.append([p[0] * w, p[1] * w, p[2] * w])
    return np.array(projection)
def update(frame):
    ax.clear()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_title("4D Hypercube Projection")
    w_factor = np.sin(frame / 20) * 0.5 + 0.5
    projected = project_4D_to_3D(cube4D, w_factor)
    for edge in edges:
        p1, p2 = projected[edge[0]], projected[edge[1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], 'b')
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ani = animation.FuncAnimation(fig, update, frames=100, interval=50)
plt.show()
