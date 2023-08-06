def abs_max(series):
    return series[series.abs().idxmax()]


def abs_min(series):
    return series[series.abs().idxmin()]


def lower_quartile(series):
    return series.quantile(.25)


def upper_quartile(series):
    return series.quantile(.75)


def inter_quartile_range(series):
    return series.quantile(.75) - series.quantile(.25)


def duration(series):
    return series.values[-1] - series.values[0]


def start_of_series(series):
    return series.values[0]


def end_of_series(series):
    return series.values[-1]


_speed_functions = tuple(['mean', abs_min, abs_max, 'median', lower_quartile,
                          upper_quartile, inter_quartile_range])
_time_functions = tuple([duration])
_position_functions = tuple([start_of_series, end_of_series])

_speed_columns = tuple(['velocity_x', 'velocity_y', 'velocity_xy',
                        'acceleration_x', 'acceleration_y',
                        'acceleration_xy',
                        'jerk_x', 'jerk_y', 'jerk_xy',
                        'angular_velocity_xy'])

_time_columns = tuple(['time'])
_position_columns = tuple(['x', 'y'])


def features_for_segment(data, group_by_columns=None,
                         speed_columns=_speed_columns,
                         time_columns=_time_columns,
                         position_columns=_position_columns):
    """
    Function to compute basic features from given pandas DataFrame.

    :param data: pandas DataFrame with specified columns
    :param group_by_columns: list of strings with column names to use in
                            groupby
    :param speed_columns: List of columns which contains speed features
    :param position_columns: List of columns which contains position data
    :param time_columns: List of columns which contains time data
    :return: DataFrame containing computed features from data
    """

    if group_by_columns is None:
        group_by_columns = ['username', 'segment']

    columns = {*speed_columns, *position_columns, *time_columns}
    if not columns.issubset(data.columns):
        return None

    features_df = (data.groupby(group_by_columns)
                   .agg({**{key: _speed_functions for key in speed_columns},
                         **{key: _time_functions for key in time_columns},
                         **{key: _position_functions for key in
                            position_columns}}))
    features_df.columns = ["_".join(y) for y in features_df.columns.ravel()]
    features_df.reset_index(inplace=True)

    return features_df
