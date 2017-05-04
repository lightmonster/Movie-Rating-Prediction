import numpy as np
from scipy.optimize import fmin_bfgs


def mn_gradient(X, Y, W, sigma2, weighted):

    n_samples, n_features = X.shape
    _n, n_len = Y.shape


    Yhat = np.dot(X, W)
    Yhat -= Yhat.min(axis=1)[:, np.newaxis]
    Yhat = np.exp(-Yhat)
    # l1-normalize
    Yhat /= Yhat.sum(axis=1)[:, np.newaxis]

    #if weighted:
    nll = np.sum(np.log((1. + 1e-15) * Yhat) * Y)
    Yhat *= Y.sum(axis=1)[:, np.newaxis]
    Yhat -= Y


    grad = np.dot(X.T, Yhat)

    if sigma2 is not None:
        nll -= np.sum(W * W) / (2. * sigma2)
        nll -= n_features * n_len * np.log(sigma2) / 2.
        grad -= W / float(sigma2)

    nll /= -float(n_samples)
    grad /= -float(n_samples)

    return nll, grad


class FGComp(object):
    def __init__(self, X, Y, ss, weighted):
        self.X = X
        self.Y = Y
        self.ss = ss
        self.weighted = weighted

        self.nll_ = None
        self.grad_ = None

    def _compute_func_grad(self, w):


        W = w.reshape((self.X.shape[1], self.Y.shape[1]))
        self.nll_, self.grad_ = mn_gradient(
            self.X, self.Y, W, self.ss, self.weighted)

    def compute_fun(self, w):
        if self.nll_ is None:
            temp = w.reshape((self.X.shape[1], self.Y.shape[1]))
            self.nll_, self.grad_ = mn_gradient(self.X, self.Y, temp, self.ss, self.weighted)
        nll = self.nll_
        self.nll_ = None  # to mark for recomputing 
        return nll

    def compute_grad(self, w):
        if self.grad_ is None:
            temp = w.reshape((self.X.shape[1], self.Y.shape[1]))
            self.nll_, self.grad_ = mn_gradient(self.X, self.Y, temp, self.ss, self.weighted)
        grad = self.grad_.ravel()  
        self.grad_ = None  
        return grad


class MLR(object):

    def __init__(self, ss=0.4, weighted=True):
        self.ss = ss
        self.weighted = weighted
        self.coeff = None
        self.nll_ = None
        self.grad_ = None

    def fit(self, X, y):
        n_samples, n_features = X.shape


        if y.ndim == 1:
            self.classes = np.unique(y)
            n_len = len(self.classes)
            Y = np.zeros((n_samples, n_len), dtype=np.float64)
            for i, cls in enumerate(self.classes):
                Y[y == cls, i] = 1
        else:
            _n, n_len = Y.shape
            self.classes = np.arange(n_len)
            Y = y

        # initialize the weight matrix
        np.random.seed(1314)
        w0 = np.random.random((n_features * n_len, ))

        fgcomp = FGComp(X, Y, self.ss, self.weighted)

        results = fmin_bfgs(fgcomp.compute_fun, w0, fprime=fgcomp.compute_grad, full_output=True)
        self.coeff = results[0].reshape((n_features, n_len))

        return self


    def predict_proba(self, X):
        Yhat = np.dot(X, self.coeff)
        Yhat -= Yhat.min(axis=1)[:, np.newaxis]
        Yhat = np.exp(-Yhat)
        
        Yhat /= Yhat.sum(axis=1)[:, np.newaxis]
        return Yhat