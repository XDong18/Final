import numpy as np 


def computeP(pts_3d, pts_2d):
    pts_num = len(pts_3d)
    matrix = np.zeros((2 * pts_num, 12))
    X = pts_3d[:, 0]
    Y = pts_3d[:, 1]
    Z = pts_3d[:, 2]
    u = pts_2d[:, 0]
    v = pts_2d[:, 1]
    matrix[::2, 0] = X
    matrix[::2, 1] = Y
    matrix[::2, 2] = Z
    matrix[::2, 3] = np.ones(pts_num)
    matrix[1::2, 4] = X
    matrix[1::2, 5] = Y
    matrix[1::2, 6] = Z
    matrix[1::2, 7] = np.ones(pts_num)
    temp_8 = np.zeros(2 * pts_num)
    temp_8[::2] = - X * u
    temp_8[1::2] = - X * v
    matrix[:, 8] = temp_8
    temp_9 = np.zeros(2 * pts_num)
    temp_9[::2] = - Y * u
    temp_9[1::2] = - Y * v
    matrix[:, 9] = temp_9    
    temp_10 = np.zeros(2 * pts_num)
    temp_10[::2] = - Z * u
    temp_10[1::2] = - Z * v
    matrix[:, 10] = temp_10
    matrix[::2, 11] = - u
    matrix[1::2, 11] = - v

    AtA = np.dot(matrix.T, matrix)
    eigvalue, eigvector = np.linalg.eig(AtA)
    min_eig = np.argmin(eigvalue)
    flatten_P = eigvector[:, min_eig]
    P = flatten_P.reshape(3, 4)
    return P





    
    





