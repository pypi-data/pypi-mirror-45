from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource, figure
from behalearn.visualization.utils import add_background_image
import warnings


def format_time_to_s(values):
    return list(map(lambda x: str(x / 1000) + ' s', values))


def visualize_mouse_data(data, width=None, height=None, resolution_width=None,
                         resolution_height=None, discrete=False,
                         highlight=False, img_url=None, img_start_x=None,
                         img_start_y=None):
    def add_line(data, p, highlight):
        line_data_source = ColumnDataSource(data=dict(
            x=data['payload_positionX'].values,
            y=data['payload_positionY'].values,
            eventType=data['eventType'].values,
            time=format_time_to_s(data['time'].values)
        ))
        if highlight:
            p.line('x', 'y', source=line_data_source, line_width=2,
                   hover_line_color="firebrick", alpha=0.5, hover_alpha=1)
        else:
            p.line('x', 'y', source=line_data_source, line_width=2, alpha=0.9)

    def add_circle(data, p, highlight):
        circle_data_source = ColumnDataSource(data=dict(
            x=data['payload_positionX'].values,
            y=data['payload_positionY'].values,
            eventType=data['eventType'].values,
            time=format_time_to_s(data['time'].values)
        ))
        if highlight:
            p.circle('x', 'y', source=circle_data_source, size=5,
                     hover_line_color="firebrick", alpha=0.5, hover_alpha=1)
        else:
            p.circle('x', 'y', source=circle_data_source, size=5)

    def add_background_line(data, p):
        line_data_source = ColumnDataSource(data=dict(
            x=data['payload_positionX'].values,
            y=data['payload_positionY'].values,
            eventType=data['eventType'].values,
            time=format_time_to_s(data['time'].values)
        ))
        p.line('x', 'y', source=line_data_source, line_width=2, alpha=0.4,
               color="#C0C0C0")

    output_notebook()
    if width is not None and height is not None:
        p = figure(plot_width=width, plot_height=height)
    elif width is None and height is None:
        p = figure()
    else:
        warnings.warn("You have to set both dimensions")
        p = figure()

    if resolution_width is not None and resolution_height is not None:
        p.y_range = Range1d(resolution_height, 0)
        p.x_range = Range1d(0, resolution_width)
    elif resolution_width is None and resolution_height is None:
        p.y_range = Range1d(data['payload_positionY'].max() + 50,
                            data['payload_positionY'].min() - 50)
        p.x_range = Range1d(data['payload_positionX'].min() - 50,
                            data['payload_positionX'].max() + 50)
    else:
        warnings.warn("You have to set both dimensions")
        p.y_range = Range1d(data['payload_positionY'].max() + 50,
                            data['payload_positionY'].min() - 50)
        p.x_range = Range1d(data['payload_positionX'].min() - 50,
                            data['payload_positionX'].max() + 50)

    add_background_line(data, p)

    mouse_move_data = data[(data['eventType'] == 'MOUSE_MOVE')]

    if discrete is False:
        if highlight:
            if 'segment' in mouse_move_data:
                mouse_move_data.groupby('segment').apply(add_line, p, True)
            else:
                add_line(mouse_move_data, p, True)
        else:
            add_line(mouse_move_data, p, False)
    else:
        if highlight:
            if 'segment' in mouse_move_data:
                mouse_move_data.groupby('segment').apply(add_circle, p, True)
            else:
                add_circle(mouse_move_data, p, True)
        else:
            add_circle(mouse_move_data, p, False)

    mouse_up_down_data = data[(data['eventType'] == 'MOUSE_UP') | (
            data['eventType'] == 'MOUSE_DOWN')]
    events_source = ColumnDataSource(data=dict(
        x=mouse_up_down_data['payload_positionX'].values,
        y=mouse_up_down_data['payload_positionY'].values,
        eventType=mouse_up_down_data['eventType'].values,
        time=format_time_to_s(mouse_up_down_data['time'].values)
    ))
    p.circle('x', 'y', source=events_source, size=8, color="red", alpha=0.5)

    tooltips = [
        ('X', '@x'),
        ('Y', '@y'),
        ('eventType', '@eventType'),
        ('time', '@time')
    ]
    p.add_tools(HoverTool(tooltips=tooltips))

    if img_url is not None:
        if img_start_x is not None and img_start_y is not None:
            x = img_start_x
            y = img_start_y
        else:
            x = data['positionX'].min()
            y = data['positionY'].min()
        w = data['positionX'].max() - data['positionX'].min()
        h = (data['positionY'].max() - data['positionY'].min()) * 0.92
        add_background_image(p, img_url, x, y, w, h)

    show(p)
