import numpy as np

def regression (X, y): # return b_list, mean of err_list
    n = len(X)
    # (1) X'y Matrix
    Xt = np.transpose (X)
    X_y = np.dot (Xt, y)
    # (2) X'X Matrix
    Xt_X = np.dot (Xt, X)
    # (6) Inverse Matrix
    inv_Xt_X = np.linalg.inv(Xt_X)
    b_list = np.dot(inv_Xt_X, X_y)
    err_list = []
    for i in range(n):
        err_list.append(y[i] - np.dot (b_list,X[i]))
    return [b_list, np.mean(err_list)]

X = np.array([[4,5,4], [4,5,3], [4,9,8], [5,8,7], [5,5,9], [8,10,8], [9,7,13], [5,14,14], [14,6,12], [9,9,9]])
y = np.array([5,4,9,3,5,5,8,5,5,12])

print regression (X,y)
