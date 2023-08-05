from bokeh.io import output_notebook, show
from bokeh.palettes import Spectral4
from bokeh.plotting import ColumnDataSource, figure
from bokeh.models import HoverTool
import warnings
from behalearn.visualization.mobile import format_time_to_s


def visualize_custom_data(data, column_names=None, width=None, height=None,
                          display=False, view_movement=False, view_time=False):
    if column_names is None:
        column_names = []
    output_notebook()
    if width is not None and height is not None:
        p = figure(plot_width=width, plot_height=height)
    elif width is None and height is None:
        p = figure()
    else:
        warnings.warn("You have to set both dimensions")
        p = figure()

    if view_movement:
        p, tooltips = visualize_custom_data_view_movement(data,
                                                          column_names, p)
    elif view_time:
        p, tooltips = visualize_custom_data_view_time(data, column_names, p)
    else:
        warnings.warn("You have to choose type of view")
        return

    p.add_tools(HoverTool(tooltips=tooltips))
    p.legend.location = "top_left"
    p.legend.click_policy = "mute"
    p.xaxis.axis_label = 'Time'

    if display:
        show(p)
    else:
        return p


def visualize_custom_data_view_movement(data, column_names, p):
    for column, color in zip(column_names, Spectral4):
        touches_source = ColumnDataSource(data=dict(
            x=data[column[0]].values,
            y=data[column[1]].values,
            time=format_time_to_s(data['time'].values),
        ))
        p.line('x', 'y', source=touches_source, line_width=2, alpha=0.9,
               muted_alpha=0.1, color=color,
               legend=column[0] + ', ' + column[1])

    tooltips = [
        ('X', '@x'),
        ('Y', '@y'),
        ('time', '@time')
    ]

    return p, tooltips


def visualize_custom_data_view_time(data, column_names, p):
    for axis, color in zip(column_names, Spectral4):
        axis_data = data[[axis, 'timeStamp']]
        axis_data_source = ColumnDataSource(data=dict(
            value=axis_data[axis].values,
            time=format_time_to_s(axis_data['timeStamp'].values),
        ))
        p.line('time', 'value', source=axis_data_source, color=color,
               alpha=0.9, muted_alpha=0.1, legend=axis)

    tooltips = [
        ('value', '@value'),
        ('time', '@time')
    ]

    return p, tooltips
