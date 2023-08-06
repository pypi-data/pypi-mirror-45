from sklearn.base import TransformerMixin

from behalearn.preprocessing.segment import split
from behalearn.preprocessing.segment import split_segment
from behalearn.preprocessing import speed_features
from behalearn.preprocessing import angular_velocity
from behalearn.preprocessing.segment import split_segment_custom


class SegmentSplitter(TransformerMixin):
    """
    Transformer wraps behalearn.preprocessing.segment.split function.
    See docstring of wrapped function.
    """

    def __init__(self, res_col_name, by, criteria):
        self._column_name = res_col_name
        self._group_by = by
        self._criteria = criteria

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        X = X.copy()
        X.sort_values(by=self._group_by, inplace=True)

        segment_res = []
        for name, data in X.groupby(self._group_by):
            segment_num = split(data, self._criteria)
            segment_res.extend([f'{name}-{i}' for i in segment_num])

        X[self._column_name] = segment_res
        return X


class PercentualSegmentSplitter(TransformerMixin):
    """
    Transformer wraps behalearn.preprocessing.segment.split_segment function.
    See docstring of wrapped function.
    """

    def __init__(self, seg_col_name, res_col_name, s_counts):
        self._seg_col_name = seg_col_name
        self._res_col_name = res_col_name
        self._s_counts = s_counts

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        X[self._res_col_name] = split_segment(X[self._seg_col_name].values,
                                              self._s_counts)
        return X


class SpeedFeaturesCalculator(TransformerMixin):
    """
    Transformer wraps behalearn.preprocessing.speed_features function.
    See docstring of wrapped function.
    """

    def __init__(self, by,
                 prefix, columns, combinations=3):
        self._group_by = by
        self._prefix = prefix
        self._columns = columns
        self._combinations = combinations

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        return X.groupby(self._group_by) \
            .apply(self._speed_features)

    def _speed_features(self, X):
        return speed_features(X, self._prefix, self._columns,
                              self._combinations)


class AngularVelocityCalculator(TransformerMixin):
    """
    Transformer wraps behalearn.preprocessing.angular_velocity function.
    See docstring of wrapped function.
    """

    def __init__(self, by, prefix, columns):
        self._group_by = by
        self._prefix = prefix
        self._columns = columns

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        return X.groupby(self._group_by) \
            .apply(self._angular_velocity)

    def _angular_velocity(self, X):
        return angular_velocity(X, self._prefix, self._columns)


class CustomSegmentSplitter(TransformerMixin):
    """
    Transformer wraps behalearn.preprocessing.segment.split_segment_custom
    function. See docstring of wrapped function.
    """

    def __init__(self, res_col_name, begin_criteria,
                 end_criteria, time_reserve=0):
        self._column_name = res_col_name
        self._begin_criteria = begin_criteria
        self._end_criteria = end_criteria
        self._time_reserve = time_reserve

    def fit(self, X, y=None, **fit_params):
        return self

    def transform(self, X, **transform_params):
        X[self._column_name] = split_segment_custom(X,
                                                    self._begin_criteria,
                                                    self._end_criteria,
                                                    self._time_reserve)
        return X
