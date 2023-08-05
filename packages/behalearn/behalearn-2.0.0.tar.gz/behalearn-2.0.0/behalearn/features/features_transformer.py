from sklearn.base import TransformerMixin

from behalearn.features import features_for_segment
from behalearn.features import segment_features


class SegmentFeatureCalculator(TransformerMixin):
    """
    Transformer wraps behalearn.features.features_for_segment function.
    See docstring of wrapped function.
    """

    def __init__(self, group_by_columns=None,
                 speed_columns=segment_features._speed_columns,
                 time_columns=segment_features._time_columns,
                 position_columns=segment_features._position_columns):
        self._group_by_columns = group_by_columns
        self._speed_columns = speed_columns
        self._time_columns = time_columns
        self._position_columns = position_columns

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        return features_for_segment(X, group_by_columns=self._group_by_columns,
                                    speed_columns=self._speed_columns,
                                    time_columns=self._time_columns,
                                    position_columns=self._position_columns)
