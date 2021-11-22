import numpy as np
import matplotlib.pyplot as plt


## Ouverture du fichier texte
txt=open("spherePoints.txt", "r")
lignes=txt.readlines()
txt.close()
ligne=[lignes[i].split(' ') for i in range (len(lignes))]
points=[[float(ligne[i][3]),float(ligne[i][6]),float(ligne[i][8])] for i in range(len(ligne))]
X=[elm[0] for elm in points]
Y=[elm[1] for elm in points]
Z=[elm[2] for elm in points]

## affichage des points
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(X, Y, Z, cmap='Greens');



## fit sphère
def sphereFit(spX,spY,spZ):
    #   Assemble the A matrix
    spX = np.array(spX)
    spY = np.array(spY)
    spZ = np.array(spZ)
    A = np.zeros((len(spX),4))
    A[:,0] = spX*2
    A[:,1] = spY*2
    A[:,2] = spZ*2
    A[:,3] = 1

    #   Assemble the f matrix
    f = np.zeros((len(spX),1))
    f[:,0] = (spX*spX) + (spY*spY) + (spZ*spZ)
    C, residules, rank, singval = np.linalg.lstsq(A,f)

    #   solve for the radius
    t = (C[0]*C[0])+(C[1]*C[1])+(C[2]*C[2])+C[3]
    radius = np.sqrt(t)

    return radius, C[0], C[1], C[2]

[rayon,Xs,Ys,Zs]=sphereFit(X,Y,Z)
print(rayon,Xs,Ys,Zs)


## Affichage des spheres
# definition de la nouvelle sphère
r = rayon
pi = np.pi
cos = np.cos
sin = np.sin
phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
x = r*sin(phi)*cos(theta)+Xs
y = r*sin(phi)*sin(theta)+Ys
z = r*cos(phi)+Zs


fig2= plt.figure()
ax2 = plt.axes(projection='3d')
ax2.scatter3D(X, Y, Z, color='r');
ax2.plot_surface(
    x, y, z,  rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)


