from __future__ import division
import numpy as np

#This is an scikit-learn style Naive Bayes classifier for multivariate Bernoulli models based on Python.
#This classifier class is mainly consists of three utility functions: fit(), predict_log_proba(), predict(), and one helper function: _binarize_X().
#To apply this classfier, we need to fit the data first, and then call the predict_log_proba() to predict the probability of each entry in a transcation.

#Instructions:
# import nb_manual as nb
# model = nb.BernoulliNB()
# model.fit(X,Y)
# predict_prob = model.predict_log_proba(X_test)


class BernoulliNB(object):
    #
    #
    def __init__(self, alpha=0.8):
        """Init the naive bayes classifier Object.

        Args:
            self: The object.
            alpha: Smoothing parameter.

        Returns:
            Default setting BNB object.

        """
        self.alpha = alpha
        self.binarize = 0
        self.class_log_prior_ = None
        self.feature_prob_ = None


    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y.

        Args:
            self: The object.
            X: Training vector, {array-like, sparse matrix}.
            y: Target values, array-like.

        Returns:
            The BNB object that has been passed in.

        """
        X = self._binarize_X(X)
        count_sample = X.shape[0]
        separated = [[x for x, t in zip(X, y) if t == c] for c in np.unique(y)]
        self.class_log_prior_ = [np.log(len(i) / count_sample) for i in separated]
        count = np.array([np.array(i).sum(axis=0) for i in separated]) + self.alpha
        smoothing = 2 * self.alpha
        n_doc = np.array([len(i) + smoothing for i in separated])
        self.feature_prob_ = count / n_doc[np.newaxis].T
        return self

    #
    def predict_log_proba(self, X):
        """Calculate log-probability estimates for the test vector X.

        Args:
            self: The object.
            X: Test vector, array-like.

        Returns:
            Returns the log-probability of the samples for each class in the model.

        """
        X = self._binarize_X(X)
        return [(np.log(self.feature_prob_) * x + \
                 np.log(1 - self.feature_prob_) * np.abs(x - 1)
                ).sum(axis=1) + self.class_log_prior_ for x in X]

    def predict(self, X):
        """Perform classification on an array of test vectors X.

        Args:
            self: The object.
            X: Test vector, array-like.

        Returns:
            Predicted target values for X.

        """
        X = self._binarize_X(X)
        return np.argmax(self.predict_log_proba(X), axis=1)

    def _binarize_X(self, X):
        """Helper function: Binarize the data from X with specified threshold.

        Args:
            self: The object.
            X: Input vector.

        Returns:
            Binarized values.

        """
        return np.where(X > self.binarize, 1, 0) if self.binarize != None else X
