def rename_columns(data, **kwargs):
    """
    Function renames chosen DataFrame columns to given names. Edited DataFrame
    needs to contain columns with names 'username', 'x', 'y' and 'time'

    :param data: Dataframe
    :param kwargs: Any number of arguments in style:
                oldColumnName = 'newColumnName', where oldColumnName
                is current name of column and newColumnName is name it should
                be renamed to.
                newColumnName should be one of the following: 'x', 'y',
                'z', 'time', 'username'
    :return: returns DataFrame with renamed columns; raises ValueError if not
            all required columns were specified
    """

    required_columns = {'username', 'x', 'y', 'time'}
    new_data = data.rename(columns=kwargs)
    if required_columns.issubset(set(new_data.columns)):
        return new_data
    else:
        raise ValueError('Missing some of the required columns')


def interpolate_custom_event(prev_event, next_event, custom_event_time):
    """
    Interpolates time of custom event to plane coordinates according to
    previous and following event
    :param prev_event: previous event with coordinates defined by tuple
    of coordinates which last element is time_stamp
    :param next_event: following event with coordinates defined by tuple
    of coordinates which last element is time_stamp
    :param custom_event_time: time of cutom event
    :return: tuple of coordinates
    """

    coord_prev, time_prev = prev_event[:-1], prev_event[-1]
    coord_next, time_next = next_event[:-1], next_event[-1]

    ratio = (custom_event_time - time_prev) / (time_next - time_prev)

    result = []
    for prev_coord, next_coord in zip(coord_prev, coord_next):
        result.append(prev_coord + (next_coord - prev_coord) * ratio)

    return tuple(result)
