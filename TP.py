import matplotlib.pyplot as plt
import numpy as np

## Ouverture du fichier texte
txt = open("spherePoints.txt", "r")
lignes = txt.readlines()
txt.close()
ligne = [lignes[i].split(' ') for i in range(len(lignes))]
points = [[float(ligne[i][3]), float(ligne[i][6]), float(ligne[i][8])] for i in range(len(ligne))]
X = [elm[0] for elm in points]
Y = [elm[1] for elm in points]
Z = [elm[2] for elm in points]

## affichage des points
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X, Y, Z, cmap='Greens');


## fit sphère
def sphereFit(spX, spY, spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX), 4))
    A[:, 0] = spX * 2
    A[:, 1] = spY * 2
    A[:, 2] = spZ * 2
    A[:, 3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX), 1))
    f[:, 0] = (spX * spX) + (spY * spY) + (spZ * spZ)
    C, residules, rank, singval = np.linalg.lstsq(A, f)

    #   solve for the radius
    t = (C[0] * C[0]) + (C[1] * C[1]) + (C[2] * C[2]) + C[3]
    radius = np.sqrt(t)

    return radius, C[0], C[1], C[2]


[rayon, Xs, Ys, Zs] = sphereFit(X, Y, Z)
print(rayon, Xs, Ys, Zs)

## Affichage des spheres
# definition de la nouvelle sphère
r = rayon
pi = np.pi
cos = np.cos
sin = np.sin
phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0 * pi:100j]
x = r * sin(phi) * cos(theta) + Xs
y = r * sin(phi) * sin(theta) + Ys
z = r * cos(phi) + Zs

fig2 = plt.figure()
ax2 = plt.axes(projection='3d')
ax2.scatter3D(X, Y, Z, color='r');
ax2.plot_surface(
    x, y, z, rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)

## definition du repere à partir des 3 points
P1 = np.array([1056.877, 602.023, -167.401])
P2 = np.array([1048.896, 701.938, -167.892])
P3 = np.array([1156.740, 609.933, -167.633])
Xr = [P1[0], P2[0], P3[0]]
Yr = [P1[1], P2[1], P3[1]]
Zr = [P1[2], P2[2], P3[2]]

fig3 = plt.figure()
ax3 = plt.axes(projection='3d')
ax3.scatter3D(Xr, Yr, Zr, color='r');

# origine = P1
Vx = (P2 - P1)/np.linalg.norm(P2 - P1)
Vy = (P3 - P1)/np.linalg.norm(P3 - P1)
print(np.arccos(np.dot(Vx, Vy)) / np.pi * 180)

Vz=np.cross(Vx,Vy)

M=np.transpose([Vx,Vy,Vz])
print(M)

T=np.zeros((4,4))
T[3,3]=1
T[0:3,0:3]=M
T[0:3,3]=np.transpose(P1)

print('la matrice de translation est :',T)