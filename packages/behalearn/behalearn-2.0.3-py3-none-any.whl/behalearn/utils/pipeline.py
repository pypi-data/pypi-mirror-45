def pipeline(X, steps, settings=None):
    """
    Sequentially apply list of transforms to given input

    :param X: data which you want to transform
    :param steps: List of (name, transform) tuples, where name is string and
            transform is function
    :param settings: setting for each step in dict, where key is in format
            name__param. E.g.: {'name__param': 123}
    :return: output from last transformer
    """

    if settings is None:
        settings = {}

    res = [X]
    for name, func in steps:
        res = func(*res, **step_settings(name, settings))

    return res


def step_settings(step_name, settings):
    step_name_prefix = f'{step_name}__'
    result = {}

    for key, value in settings.items():
        if key.startswith(step_name_prefix):
            param_name = key.replace(step_name_prefix, '', 1)
            result[param_name] = value

    return result
