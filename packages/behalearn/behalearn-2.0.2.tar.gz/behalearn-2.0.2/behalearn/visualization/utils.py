from bokeh.models import Range1d
from pandas import Series


def format_time_to_s(values):
    return list(map(lambda x: str(x / 1000) + ' s', values))


def add_background_image(p, image_url, x, y, w, h):
    p.image_url(url=image_url, x=x, y=y, w=w, h=h, global_alpha=0.35)


def max_min_diff(series: Series):
    return series.max() - series.min()


def max_min_range(series: Series, offset=0) -> Range1d:
    return Range1d(series.max() + offset, series.min() - offset)


def min_max_range(series: Series, offset=0) -> Range1d:
    return Range1d(series.min() - offset, series.max() + offset)
