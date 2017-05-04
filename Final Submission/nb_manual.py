from __future__ import division
import numpy as np


# Instruction:
# import nb_manual as nb
# model = nb.BernoulliNB()
# model.fit(X,Y)
# predict_prob = model.predict_log_proba(X_test)


class BernoulliNB(object):
    def __init__(self, alpha=0.8):
        self.alpha = alpha
        self.binarize = 0.6
        self.class_log_prior_ = None
        self.feature_prob_ = None

    def fit(self, X, y):
        X = self._binarize_X(X)
        count_sample = X.shape[0]
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
        count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
        smoothing = 2 * self.alpha
        n_doc = np.array([len(i) + smoothing for i in separated])
        self.feature_prob_ = count / n_doc[np.newaxis].T
        return self

    def predict_log_proba(self, X):
        X = self._binarize_X(X)
        return [(np.log(self.feature_prob_) * x + np.log(1 - self.feature_prob_) * np.abs(x - 1)
                 ).sum(axis=1) + self.class_log_prior_ for x in X]

    def predict(self, X):
        X = self._binarize_X(X)
        return np.argmax(self.predict_log_proba(X), axis=1)

    def _binarize_X(self, X):
        return np.where(X > self.binarize, 1, 0) if self.binarize is not None else X
