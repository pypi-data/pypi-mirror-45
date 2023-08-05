import numpy as np
from sklearn.base import ClassifierMixin


class VotingSegmentClassifier(ClassifierMixin):

    def __init__(self, estimator, **kwargs):
        self._estimator = estimator(**kwargs)

    def fit(self, X, y, **fit_params):
        self._estimator.fit(X, y)
        return self

    def predict_proba(self, X, **predict_params):
        predictions = self._estimator.predict(X)
        return np.bincount(predictions) / predictions.shape[0]

    def predict(self, X, **predict_params):
        pred_proba = self.predict_proba(X, **predict_params)
        return np.argmax(pred_proba)
