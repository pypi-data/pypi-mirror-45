from bokeh.io import output_notebook, show
from bokeh.palettes import Spectral4
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool
import warnings
from behalearn.visualization.utils import format_time_to_s


def visualize_custom_data(data, view_mode, x_columns=None, y_columns=None,
                          width=None, height=None, display=False):
    """
    Function for visualizing custom columns from dataframe on mobile devices.
    :param data: Pandas DataFrame with user data, data should be logged with
    Fastar/Logger-Web
    :param view_mode: There are 2 possible modes to view - both_axes /
    time_axis.
    both_axes - columns from list x_columns are displayed on x-axis and
    columns from list y_columns are displayed on y-axis, parameters
    x_columns and y_columns should not be None
    time_axis - on x-axis is always time column and columns from list
    y_columns are displayed on y-axis, parameter y_columns should not be None
    :param x_columns: list of columns to display on x-axis
    :param y_columns: list of columns to display on y-axis
    :param width: Integer number to set width of figure (optional)
    :param height: Integer number to set height of figure (optional)
    :param display: Displays Bokeh figure, default False
    :return: Bokeh figure with provided DataFrames and parameters
    """
    output_notebook()
    if width is not None and height is not None:
        p = figure(plot_width=width, plot_height=height)
    elif width is None and height is None:
        p = figure()
    else:
        warnings.warn("You have to set both dimensions")
        p = figure()

    if view_mode is None:
        warnings.warn("You have to choose view_mode - both_axes /"
                      " time_axis")

    if view_mode not in ['both_axes', 'time_axis']:
        warnings.warn("Choose between 2 modes - both_axes / time_axis")

    if view_mode == 'both_axes' and len(x_columns) != len(y_columns):
        warnings.warn("There have to be same amount of x and y columns")

    if view_mode == 'both_axes':
        p = visualize_custom_data_both_axes(data, x_columns,
                                            y_columns, p)
    if view_mode == 'time_axis':
        p = visualize_custom_data_time_axis(data, y_columns, p)

    if view_mode in ['both_axes', 'time_axis']:
        tooltips = [
            ('X', '@x'),
            ('Y', '@y'),
            ('time', '@time')
        ]
        p.add_tools(HoverTool(tooltips=tooltips))
        p.legend.location = "top_left"
        p.legend.click_policy = "mute"

    if display:
        show(p)

    return p


def visualize_custom_data_both_axes(data, x_columns, y_columns, p):
    for x_column, y_column, color in zip(x_columns, y_columns, Spectral4):
        touches_source = ColumnDataSource(data=dict(
            x=data[x_column].values,
            y=data[y_column].values,
            time=format_time_to_s(data['time'].values),
        ))
        p.line('x', 'y', source=touches_source, line_width=2, alpha=0.9,
               muted_alpha=0.1, color=color,
               legend=x_column + ', ' + y_column)

    return p


def visualize_custom_data_time_axis(data, y_columns, p):
    for y_column, color in zip(y_columns, Spectral4):
        data_source = ColumnDataSource(data=dict(
            x=data['time'].values,
            y=data[y_column].values,
            time=format_time_to_s(data['time'].values),
        ))
        p.line('x', 'y', source=data_source, color=color,
               alpha=0.9, muted_alpha=0.1, legend=y_column)

    return p
