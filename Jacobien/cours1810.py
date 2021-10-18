import numpy as np


def direct(theta1, theta2, theta3, l1=1, l2=2, l3=3):
    xp = (l2 * np.cos(theta2) + l3 * np.cos(theta3)) * np.cos(theta1)
    yp = (l2 * np.cos(theta2) + l3 * np.cos(theta3)) * np.sin(theta1)
    zp = (l2 * np.sin(theta2) + l3 * np.sin(theta3) + l1)
    return np.array([[xp], [yp], [zp]])


def Jacob(theta1, theta2, theta3, l1=1, l2=2, l3=3):
    M = np.zeros((3, 3))
    M[0, 0] = -np.sin(theta1) * (l2 * np.cos(theta2) + l3 * np.cos(theta2 + theta3))
    M[0, 1] = -np.cos(theta1) * (l2 * np.sin(theta2) + l3 * np.sin(theta2 + theta3))
    M[0, 2] = -np.cos(theta1) * l3 * np.sin(theta2 + theta3)
    M[1, 0] = np.cos(theta1) * (l2 * np.cos(theta2) + l3 * np.cos(theta2 + theta3))
    M[1, 1] = -np.sin(theta1) * (l2 * np.sin(theta2) + l3 * np.sin(theta2 + theta3))
    M[1, 2] = -np.sin(theta1) * l3 * np.sin(theta2 + theta3)
    M[1, 2] = l2 * np.cos(theta2) + l3 * np.cos(theta2 + theta3)
    M[2, 2] = l3 * np.cos(theta2 + theta3)
    return (M)


def Newton(x, y, z, l1, l2, l3, mxIter):
    theta = [1, 1, 1]
    iter = 0
    while iter < mxIter:

        J = Jacob(theta[0], theta[1], theta[2], l1, l2, l3)
        A = np.linalg.inv(J)
        B = np.array([[x], [y], [z]]) - direct(theta[0], theta[1], theta[2], l1, l2, l3)
        theta = theta + np.transpose(np.dot(A, B))[0]
        iter += 1
        print('erreur =',B)

    print( "La solution finale de theta est :",theta)

    return (theta)

Newton(0.5, 0.1, 0.6, 0.5, 0.5, 0.5, 5)
