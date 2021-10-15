# cette version resout le probleme dans le cadre d'un probleme plan pour les deuw axes

import numpy as np
from math import *
import matplotlib.pyplot as plt



np.set_printoptions(suppress=True)


def matriceR(a, b, g):
    # a = radians(a)
    # b = radians(b)
    # g = radians(g)

    x = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    y = np.array([[np.cos(b), 0, np.sin(b)], [0, 1, 0], [-np.sin(b), 0, np.cos(b)]])
    z = np.array([[np.cos(g), -np.sin(g), 0], [np.sin(g), np.cos(g), 0], [0, 0, 1]])

    return x @ y @ z


def matriceT(x, y, z, a, b, g):
    T = np.concatenate((matriceR(a, b, g), np.array([[x, y, z]]).T), axis=1)
    return np.concatenate((T, np.array([[0, 0, 0, 1]])), axis=0)


def DirectKinematics(l1, l2, l3, t1, t2, t3):
    T01 = matriceT(0, 0, 0, 0, 0, t1)
    T12 = matriceT(0, 0, l1, np.pi / 2, 0, t2)
    T23 = matriceT(l2, 0, 0, 0, 0, t3)
    T34 = matriceT(l3, 0, 0, 0, 0, 0)

    T04 = T01 @ T12 @ T23 @ T34

    P = np.array([[0, 0, 0, 1]]).T
    P1 = np.round(T01 @ P, 3)
    P2 = np.round(T01 @ T12 @ P, 3)
    P3 = np.round(T01 @ T12 @ T23 @ P, 3)
    P4 = np.round(T04 @ P, 3)
    X = [0, P1[0, 0], P2[0, 0], P3[0, 0], P4[0, 0]]
    Y = [0, P1[1, 0], P2[1, 0], P3[1, 0], P4[1, 0]]
    Z = [0, P1[2, 0], P2[2, 0], P3[2, 0], P4[2, 0]]

    return [X[4], Y[4], Z[4]], X, Y, Z


def inverseKinematics(l1, l2, l3, x, y, z):
    # x, y et z sont les coordonnées du point P.
    r = [[], [], [], []]

    # On commence par le calcul des theta1
    if y == 0 and x != 0:
        r[0].append(0)
        r[1].append(0)
        r[2].append(np.pi)
        r[3].append(np.pi)
    elif x == 0 and y != 0:
        r[0].append(np.pi / 2)
        r[1].append(np.pi / 2)
        r[2].append(np.pi / 2 + np.pi)
        r[3].append(np.pi / 2 + np.pi)
    else:
        r[0].append(np.arctan2(y, x))
        r[1].append(np.arctan2(y, x))
        r[2].append(np.arctan2(y, x) + pi)
        r[3].append(np.arctan2(y, x) + pi)

    # On va ensuite calculer les theta2
    for i in range(len(r)):
        if i == 0 or i == 2:
            eps = 1
        else:
            eps = -1
        d = (x ** 2 + y ** 2 + (z - l1) ** 2 - l2 ** 2 - l3 ** 2) / (2 * l2 * l3)
        t3 = np.arctan2(eps * np.sqrt(1 - d ** 2), d)
        t2 = np.arctan2(z - l1, np.sqrt(x ** 2 + y ** 2)) - np.arctan2(l3 * np.sin(t3), l2 + l3 * np.cos(t3))
        if i > 1:
            r[i].append(t2 + (r[1][1] - r[0][1]) + (np.pi - 2 * r[1][1]))
        else:
            r[i].append(t2)
        r[i].append(t3)

    return r


## Données du robot

t1 = np.radians(30)
t2 = np.radians(40)
t3 = np.radians(50)
l1 = 100
l2 = 400
l3 = 300

P, X, Y, Z = DirectKinematics(l1, l2, l3, t1, t2, t3)
print(P)
thetas = inverseKinematics(l1, l2, l3, P[0], P[1], P[2])

thetas.append([t1, t2, t3])

PointsP = []
ax = plt.figure(1)
ax = plt.axes(projection='3d')
ax.set_xlim3d(0, 700)
ax.set_ylim3d(0, 700)
ax.set_zlim3d(0, 700)

j = 0

for i in thetas:
    P, X, Y, Z = DirectKinematics(l1, l2, l3, i[0], i[1], i[2])
    PointsP.append(P)
    if i == [t1, t2, t3]:
        ax.scatter3D(X, Y, Z, c='yellow')
        plt.plot(X, Y, Z, c='yellow', label=j)
    else:
        ax.scatter3D(X, Y, Z)
        plt.plot(X, Y, Z, label=j)
    j += 1

plt.legend()

for i in range(len(thetas)):
    for j in range(len(thetas[i])):
        thetas[i][j] = round(degrees(thetas[i][j]), 1)

print(thetas[:4])
