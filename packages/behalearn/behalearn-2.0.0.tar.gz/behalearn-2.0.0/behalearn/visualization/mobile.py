from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource, figure
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot
import numpy as np
import warnings


def format_time_to_s(values):
    return list(map(lambda x: str(x / 1000) + ' s', values))


def label_touches(data):
    gesture = 0
    for index, row in data.iterrows():
        data.loc[index, 'gesture'] = gesture
        if row.eventType == 'TOUCH_END' or row.eventType == 'TOUCH_CANCEL':
            gesture += 1

    return data


def visualize_touch_movement(p, data_source, finger_id, highlight, discrete,
                             settings_dict):
    if discrete is False:
        if highlight:
            p.line('touch_x', 'touch_y', source=data_source,
                   line_width=2, alpha=0.5, muted_alpha=0.1,
                   legend=settings_dict['touch'][finger_id]['key'],
                   color=settings_dict['touch'][finger_id]['color'],
                   muted_color=settings_dict['touch'][finger_id]['color'],
                   hover_line_color="firebrick", hover_alpha=1)
        else:
            p.line('touch_x', 'touch_y', source=data_source,
                   line_width=2, alpha=0.9, muted_alpha=0.1,
                   legend=settings_dict['touch'][finger_id]['key'],
                   color=settings_dict['touch'][finger_id]['color'],
                   muted_color=settings_dict['touch'][finger_id]['color'])
    else:
        p.circle('touch_x', 'touch_y', source=data_source,
                 line_width=2, alpha=0.9, muted_alpha=0.1,
                 legend=settings_dict['touch'][finger_id]['key'],
                 color=settings_dict['touch'][finger_id]['color'],
                 muted_color=settings_dict['touch'][finger_id]['color'])
    return p


def visualize_touch_events(p, data_source, finger_id, start, settings_dict):
    fill_color = settings_dict['touch'][finger_id]['color']
    if not start:
        fill_color = 'white'
    p.circle('touch_x', 'touch_y', source=data_source,
             alpha=0.9, muted_alpha=0.1, size=8,
             legend=settings_dict['touch'][finger_id]['key'],
             color=settings_dict['touch'][finger_id]['color'],
             muted_color=settings_dict['touch'][finger_id]['color'],
             fill_color=fill_color)
    return p


def visualize_acc_data(p, data_source, highlight, settings_dict):
    for axis in ['X', 'Y', 'Z']:
        if highlight:
            p.line('time', 'acc_' + axis, source=data_source,
                   color=settings_dict['acc'][axis]['color'], alpha=0.9,
                   muted_alpha=0.1,
                   legend=settings_dict['acc'][axis]['key'],
                   muted_color=settings_dict['acc'][axis]['color'],
                   hover_line_color="firebrick", hover_alpha=1)
        else:
            p.line('time', 'acc_' + axis, source=data_source,
                   color=settings_dict['acc'][axis]['color'], alpha=0.9,
                   muted_alpha=0.1,
                   legend=settings_dict['acc'][axis]['key'],
                   muted_color=settings_dict['acc'][axis]['color'])
    return p


def visualize_gyro_data(p, data_source, highlight, settings_dict):
    for axis in ['alpha', 'beta', 'gamma']:
        if highlight:
            p.line('time', 'gyro_' + axis, source=data_source,
                   color=settings_dict['gyro'][axis]['color'], alpha=0.5,
                   muted_alpha=0.1,
                   legend=settings_dict['gyro'][axis]['color'],
                   muted_color=settings_dict['gyro'][axis]['color'],
                   hover_line_color="firebrick", hover_alpha=1)
        else:
            p.line('time', 'gyro_' + axis, source=data_source,
                   color=settings_dict['gyro'][axis]['color'], alpha=0.9,
                   muted_alpha=0.1,
                   legend=settings_dict['gyro'][axis]['color'],
                   muted_color=settings_dict['gyro'][axis]['color'])
    return p


def visualize_touch_acc_gyro_data(data_touch, data_acc, data_gyro,
                                  highlight=False, **kwargs):
    def prepare_figure(width, height):
        if width is not None and height is not None:
            p = figure(plot_width=width, plot_height=height)
        elif width is None and height is None:
            p = figure()
        else:
            warnings.warn("You have to set both dimensions")
            p = figure()
        return p

    def set_resolution(touch_figure, data_touch, resolution_width,
                       resolution_height):
        if resolution_width is not None and resolution_height is not None:
            touch_figure.y_range = Range1d(resolution_height, 0)
            touch_figure.x_range = Range1d(0, resolution_width)
        elif resolution_width is None and resolution_height is None:
            touch_figure.y_range = Range1d(data_touch['positionY'].max() + 50,
                                           data_touch['positionY'].min() - 50)
            touch_figure.x_range = Range1d(data_touch['positionX'].min() - 50,
                                           data_touch['positionX'].max() + 50)
        else:
            warnings.warn("You have to set both dimensions")
            touch_figure.y_range = Range1d(data_touch['positionY'].max() + 50,
                                           data_touch['positionY'].min() - 50)
            touch_figure.x_range = Range1d(data_touch['positionX'].min() - 50,
                                           data_touch['positionX'].max() + 50)
        return touch_figure

    def set_widgets(figure, figure_type):
        if figure_type in ['acc', 'gyro']:
            tooltips = [
                ('value', '@value'),
                ('time', '@time')
            ]
            figure.xaxis.axis_label = 'Time'
            if figure_type == 'acc':
                figure.title.text = "Accelerometer data"
            else:
                figure.title.text = "Gyroscope data"
        else:
            tooltips = [
                ('X', '@touch_x'),
                ('Y', '@touch_y'),
                ('eventType', '@eventType'),
                ('time', '@time'),
                ('fingerId', '@fingerId'),
                ('force', '@force')
            ]
            figure.title.text = "Touch data"
            figure.xaxis.axis_label = 'X'
            figure.yaxis.axis_label = 'Y'
        figure.legend.location = "top_left"
        figure.legend.click_policy = "mute"
        figure.add_tools(HoverTool(tooltips=tooltips))
        return figure

    def prepare_settings(finger_keys):
        settings_dict = {
            "touch": {},
            "acc": {},
            "gyro": {}
        }
        for key, color in zip(finger_keys, Spectral4):
            settings_dict['touch'][key] = {
                "key": 'id_' + str(key),
                "color": color
            }
        for key, color in zip(['X', 'Y', 'Z'], Spectral4):
            settings_dict['acc'][key] = {
                "key": str(key),
                "color": color
            }
        for key, color in zip(['alpha', 'beta', 'gamma'], Spectral4):
            settings_dict['gyro'][key] = {
                "key": str(key),
                "color": color
            }
        return settings_dict

    def background_line_touch(data_touch, touch_figure):
        data_source = ColumnDataSource(data=dict(
            touch_x=data_touch['position_x'].values,
            touch_y=data_touch['position_y'].values,
            eventType=data_touch['eventType'].values,
            fingerId=data_touch['id'].values,
            force=data_touch['force'].values,
        ))
        touch_figure.line('touch_x', 'touch_y', source=data_source,
                          line_width=2, alpha=0.4,
                          color='#C0C0C0')

    def background_line_acc(data_acc, acc_figure):
        for axis in ['X', 'Y', 'Z']:
            data_source = ColumnDataSource(data=dict(
                time=data_acc['time'].values,
                value=data_acc['payload_acc' + axis].values,
            ))
            acc_figure.line('time', 'value', source=data_source,
                            color='#C0C0C0', alpha=0.4)

    def background_line_gyro(data_gyro, gyro_figure):
        for axis in ['alpha', 'beta', 'gamma']:
            data_source = ColumnDataSource(data=dict(
                time=data_gyro['time'].values,
                value=data_gyro['payload_' + axis].values,
            ))
            gyro_figure.line('time', 'value', source=data_source,
                             color='#C0C0C0', alpha=0.4, )

    def visualize_data_movement(data_touch, data_acc, data_gyro, touch_figure,
                                acc_figure, gyro_figure, highlight, discrete,
                                settings_dict):
        finger_id = data_touch.name[2]
        data_acc = data_acc[(data_acc['time'] >= data_touch['time'].min()) & (
                data_acc['time'] <= data_touch['time'].max())]
        data_gyro = data_gyro[
            (data_gyro['time'] >= data_touch['time'].min()) & (
                    data_gyro['time'] <= data_touch['time'].max())]

        level = max(
            [data_touch.shape[0], data_acc.shape[0], data_gyro.shape[0]])
        for i in range(level - data_touch.shape[0]):
            data_touch = data_touch.append(
                {'position_x': np.nan, 'position_y': np.nan},
                ignore_index=True)
        for i in range(level - data_acc.shape[0]):
            data_acc = data_acc.append(
                {'payload_accX': np.nan, 'payload_accY': np.nan,
                 'payload_accZ': np.nan}, ignore_index=True)
        for i in range(level - data_gyro.shape[0]):
            data_gyro = data_gyro.append(
                {'payload_alpha': np.nan, 'payload_brta': np.nan,
                 'payload_gamma': np.nan}, ignore_index=True)
        data_source = ColumnDataSource(data=dict(
            gyro_alpha=data_gyro['payload_alpha'].values,
            gyro_beta=data_gyro['payload_beta'].values,
            gyro_gamma=data_gyro['payload_gamma'].values,
            time=data_touch['time'].values,
            touch_x=data_touch['position_x'].values,
            touch_y=data_touch['position_y'].values,
            eventType=data_touch['eventType'].values,
            fingerId=data_touch['id'].values,
            force=data_touch['force'].values,
            acc_X=data_acc['payload_accX'].values,
            acc_Y=data_acc['payload_accY'].values,
            acc_Z=data_acc['payload_accZ'].values
        ))
        touch_figure = visualize_touch_movement(touch_figure, data_source,
                                                finger_id, highlight, discrete,
                                                settings_dict)
        acc_figure = visualize_acc_data(acc_figure, data_source, highlight,
                                        settings_dict)
        gyro_figure = visualize_acc_data(gyro_figure, data_source, highlight,
                                         settings_dict)

    def visualize_data_events(data_touch, touch_figure, start, settings_dict):
        data_source = ColumnDataSource(data=dict(
            time=data_touch['time'].values,
            touch_x=data_touch['position_x'].values,
            touch_y=data_touch['position_y'].values,
            eventType=data_touch['eventType'].values,
            fingerId=data_touch['id'].values,
            force=data_touch['force'].values,
        ))
        touch_figure = visualize_touch_events(touch_figure, data_source,
                                              data_touch.name, start,
                                              settings_dict)

    output_notebook()
    finger_keys = data_touch.id.unique()
    settings_dict = prepare_settings(finger_keys)

    touch_figure = prepare_figure(kwargs.get('touch_width', None),
                                  kwargs.get('touch_height', None))
    touch_figure = set_resolution(touch_figure, data_touch,
                                  kwargs.get('touch_resolution_width', None),
                                  kwargs.get('touch_resolution_height', None))

    acc_figure = prepare_figure(kwargs.get('acc_width', None),
                                kwargs.get('acc_height', None))

    gyro_figure = prepare_figure(kwargs.get('gyro_width', None),
                                 kwargs.get('gyro_height', None))

    data_touch_movement = data_touch[data_touch['eventType'] == 'TOUCH_MOVE']
    data_touch.groupby(['gesture', 'id']).apply(background_line_touch,
                                                touch_figure)
    background_line_acc(data_acc, acc_figure)
    background_line_gyro(data_gyro, gyro_figure)

    if 'segment' in data_touch_movement:
        if highlight:
            data_touch_movement.groupby(['segment', 'gesture', 'id']).apply(
                visualize_data_movement, data_acc, data_gyro,
                touch_figure, acc_figure, gyro_figure,
                True, kwargs.get('touch_discrete', False), settings_dict)
        else:
            data_touch_movement.groupby(['segment', 'gesture', 'id']).apply(
                visualize_data_movement, data_acc, data_gyro,
                touch_figure, acc_figure, gyro_figure,
                False, kwargs.get('touch_discrete', False), settings_dict)
    else:
        data_touch_movement.groupby(['gesture', 'id']).apply(
            visualize_data_movement, data_acc, data_gyro,
            touch_figure, acc_figure, gyro_figure,
            False, kwargs.get('touch_discrete', False), settings_dict)

    data_touch_start = data_touch[data_touch['eventType'] == 'TOUCH_START']
    data_touch_start.groupby('id').apply(visualize_data_events, touch_figure,
                                         True, settings_dict)

    data_touch_end = data_touch[(data_touch['eventType'] == 'TOUCH_END') | (
            data_touch['eventType'] == 'TOUCH_CANCEL')]
    data_touch_end.groupby('id').apply(visualize_data_events, touch_figure,
                                       False, settings_dict)

    touch_figure = set_widgets(touch_figure, 'touch')
    acc_figure = set_widgets(acc_figure, 'acc')
    gyro_figure = set_widgets(gyro_figure, 'gyro')

    grid = gridplot([[touch_figure], [acc_figure, gyro_figure]],
                    toolbar_location='right')
    show(grid)
