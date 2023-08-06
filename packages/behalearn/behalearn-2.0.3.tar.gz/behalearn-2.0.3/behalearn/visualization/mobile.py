from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource, figure
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot
import numpy as np
import warnings
from behalearn.visualization.utils import max_min_range, min_max_range


def label_touches(data):
    gesture = 0
    for index, row in data.iterrows():
        data.loc[index, 'gesture'] = gesture
        if row.eventType == 'TOUCH_END' or row.eventType == 'TOUCH_CANCEL':
            gesture += 1

    return data


class _MobilePlot:

    def __init__(self, data_touch, data_acc, data_gyro, touch_width=None,
                 touch_height=None, discrete=False,
                 resolution_width=None, resolution_height=None,
                 highlight=False, acc_width=None, acc_height=None,
                 gyro_width=None, gyro_height=None):
        self.data_touch = data_touch.copy()
        self.data_acc = data_acc.copy()
        self.data_gyro = data_gyro.copy()
        self.data_touch['time'] = self._format_time_to_s(
            self.data_touch['time'])
        self.data_acc['time'] = self._format_time_to_s(
            self.data_acc['time'])
        self.data_gyro['time'] = self._format_time_to_s(
            self.data_gyro['time'])

        self.touch_width = touch_width
        self.touch_height = touch_height
        self.acc_width = acc_width
        self.acc_height = acc_height
        self.gyro_width = gyro_width
        self.gyro_height = gyro_height
        self.discrete = discrete
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.highlight = highlight

        self.touch_move_data = self.data_touch[(self.data_touch['eventType']
                                                == 'TOUCH_MOVE')]
        self.touch_start_data = self.data_touch[(self.data_touch['eventType']
                                                 == 'TOUCH_START')]

        self.touch_end_data = self.data_touch[(self.data_touch['eventType']
                                               == 'TOUCH_END')
                                              | (self.data_touch['eventType']
                                                 == 'TOUCH_CANCEL')]
        self.finger_keys = self.data_touch.id.unique()
        self.settings_dict = self._create_settings()
        self._init()

    def _init(self):
        output_notebook()
        self.touch_figure = self._create_touch_figure()
        self.acc_figure = self._create_acc_figure()
        self.gyro_figure = self._create_gyro_figure()

        self._set_resolution()
        self.data_touch.groupby(['gesture', 'id']).apply(
            self._add_background_line_touch)
        self._add_background_line_acc()
        self._add_background_line_gyro()

        if 'segment' in self.touch_move_data:
            self.touch_move_data.groupby(['segment', 'gesture', 'id']).apply(
                self._visualize_data_movement)
        else:
            self.touch_move_data.groupby(['gesture', 'id']).apply(
                self._visualize_data_movement)

        self.touch_start_data.groupby('id').apply(self._visualize_data_events,
                                                  True)
        self.touch_end_data.groupby('id').apply(self._visualize_data_events,
                                                False)

        self._set_widgets(self.touch_figure, 'touch')
        self._set_widgets(self.acc_figure, 'acc')
        self._set_widgets(self.gyro_figure, 'gyro')

        self.grid = gridplot(
            [[self.touch_figure], [self.acc_figure, self.gyro_figure]],
            toolbar_location='right')

    def _create_touch_figure(self):
        if None not in (self.touch_width, self.touch_height):
            return figure(plot_width=self.touch_width,
                          plot_height=self.touch_height)

        warnings.warn("You have to set both dimensions")
        return figure()

    def _create_acc_figure(self):
        if None not in (self.acc_width, self.acc_height):
            return figure(plot_width=self.acc_width,
                          plot_height=self.acc_height)

        warnings.warn("You have to set both dimensions")
        return figure()

    def _create_gyro_figure(self):
        if None not in (self.gyro_width, self.gyro_height):
            return figure(plot_width=self.gyro_width,
                          plot_height=self.gyro_height)

        warnings.warn("You have to set both dimensions")
        return figure()

    def _set_resolution(self):
        data = self.data_touch
        resolution_width = self.resolution_width
        resolution_height = self.resolution_height

        if None not in (resolution_width, resolution_height):
            self.touch_figure.y_range = Range1d(resolution_height, 0)
            self.touch_figure.x_range = Range1d(0, resolution_width)
        else:
            warnings.warn("You have to set both dimensions (resolution)")
            self.touch_figure.y_range = max_min_range(
                data['positionY'],
                offset=50)
            self.touch_figure.x_range = min_max_range(
                data['positionX'],
                offset=50)

    def _create_settings(self):
        settings_dict = {
            "touch": {},
            "acc": {},
            "gyro": {}
        }
        for key, color in zip(self.finger_keys, Spectral4):
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

    @staticmethod
    def _format_time_to_s(values):
        return list(map(lambda x: round((x / 1000), 3), values))

    def _add_touch_line(self):
        if self.highlight:
            self.touch_figure.line('touch_x', 'touch_y',
                                   source=self.movement_datasource,
                                   line_width=2, alpha=0.5, muted_alpha=0.1,
                                   legend=self.settings_dict['touch']
                                   [self.finger_id]['key'],
                                   color=self.settings_dict['touch']
                                   [self.finger_id]['color'],
                                   muted_color=self.settings_dict['touch']
                                   [self.finger_id]['color'],
                                   hover_line_color="firebrick", hover_alpha=1)
        else:
            self.touch_figure.line('touch_x', 'touch_y',
                                   source=self.movement_datasource,
                                   line_width=2, alpha=0.9, muted_alpha=0.1,
                                   legend=self.settings_dict['touch']
                                   [self.finger_id]['key'],
                                   color=self.settings_dict['touch']
                                   [self.finger_id]['color'],
                                   muted_color=self.settings_dict['touch']
                                   [self.finger_id]['color'])

    def _add_touch_circle(self):
        if self.highlight:
            self.touch_figure.circle('touch_x', 'touch_y',
                                     source=self.movement_datasource,
                                     line_width=2, alpha=0.5, muted_alpha=0.1,
                                     legend=self.settings_dict['touch']
                                     [self.finger_id]['key'],
                                     color=self.settings_dict['touch']
                                     [self.finger_id]['color'],
                                     muted_color=self.settings_dict['touch']
                                     [self.finger_id]['color'],
                                     hover_line_color="firebrick",
                                     hover_alpha=1)
        else:
            self.touch_figure.circle('touch_x', 'touch_y',
                                     source=self.movement_datasource,
                                     line_width=2, alpha=0.9, muted_alpha=0.1,
                                     legend=self.settings_dict['touch']
                                     [self.finger_id]['key'],
                                     color=self.settings_dict['touch']
                                     [self.finger_id]['color'],
                                     muted_color=self.settings_dict['touch']
                                     [self.finger_id]['color'])

    def _add_acc_line(self):
        for axis in ['X', 'Y', 'Z']:
            if self.highlight:
                self.acc_figure.line('time', 'acc_' + axis,
                                     source=self.movement_datasource,
                                     color=self.settings_dict['acc'][axis]
                                     ['color'],
                                     alpha=0.9, muted_alpha=0.1,
                                     legend=self.settings_dict['acc'][axis]
                                     ['key'],
                                     muted_color=self.settings_dict['acc']
                                     [axis]['color'],
                                     hover_line_color="firebrick",
                                     hover_alpha=1)
            else:
                self.acc_figure.line('time', 'acc_' + axis,
                                     source=self.movement_datasource,
                                     color=self.settings_dict['acc'][axis]
                                     ['color'],
                                     alpha=0.9, muted_alpha=0.1,
                                     legend=self.settings_dict['acc'][axis]
                                     ['key'],
                                     muted_color=self.settings_dict['acc']
                                     [axis]['color'])

    def _add_gyro_line(self):
        for axis in ['alpha', 'beta', 'gamma']:
            if self.highlight:
                self.gyro_figure.line('time', 'gyro_' + axis,
                                      source=self.movement_datasource,
                                      color=self.settings_dict['gyro'][axis]
                                      ['color'], alpha=0.5, muted_alpha=0.1,
                                      legend=self.settings_dict['gyro'][axis]
                                      ['key'],
                                      muted_color=self.settings_dict['gyro']
                                      [axis]['color'],
                                      hover_line_color="firebrick",
                                      hover_alpha=1)
            else:
                self.gyro_figure.line('time', 'gyro_' + axis,
                                      source=self.movement_datasource,
                                      color=self.settings_dict['gyro'][axis]
                                      ['color'], alpha=0.9, muted_alpha=0.1,
                                      legend=self.settings_dict['gyro'][axis]
                                      ['key'],
                                      muted_color=self.settings_dict['gyro']
                                      [axis]['color'])

    def _add_background_line_touch(self, data):
        data_source = ColumnDataSource(data=dict(
            touch_x=data['positionX'].values,
            touch_y=data['positionY'].values,
            eventType=data['eventType'].values,
            fingerId=data['id'].values,
            force=data['force'].values,
            time=data['time'].values,
        ))
        self.touch_figure.line('touch_x', 'touch_y', source=data_source,
                               line_width=2, alpha=0.4,
                               color=self.settings_dict['touch'][data.name[-1]]
                               ['color'])

    def _add_background_line_acc(self):
        for axis in ['X', 'Y', 'Z']:
            data_source = ColumnDataSource(data={
                "time_acc": self.data_acc['time'].values,
                "acc_" + axis: self.data_acc['payload_acc' + axis].values,
            })
            self.acc_figure.line('time_acc', "acc_" + axis, source=data_source,
                                 color=self.settings_dict['acc'][axis]
                                 ['color'], alpha=0.4)

    def _add_background_line_gyro(self):
        for axis in ['alpha', 'beta', 'gamma']:
            data_source = ColumnDataSource(data={
                "time_gyro": self.data_gyro['time'].values,
                "gyro_" + axis: self.data_gyro['payload_' + axis].values,
            })
            self.gyro_figure.line('time_gyro', "gyro_" + axis,
                                  source=data_source,
                                  color=self.settings_dict['gyro'][axis]
                                  ['color'], alpha=0.4)

    @staticmethod
    def _set_widgets(figure, figure_type):
        tooltips = []
        if figure_type == 'acc':
            tooltips = [
                ('acc_X', '@acc_X'),
                ('acc_Y', '@acc_Y'),
                ('acc_Z', '@acc_Z'),
                ('time', '@time_acc')
            ]
            figure.xaxis.axis_label = 'Time'
            figure.title.text = "Accelerometer data"
        if figure_type == 'gyro':
            tooltips = [
                ('gyro_alpha', '@gyro_alpha'),
                ('gyro_beta', '@gyro_beta'),
                ('gyro_gamma', '@gyro_gamma'),
                ('time', '@time_gyro')
            ]
            figure.xaxis.axis_label = 'Time'
            figure.title.text = "Gyroscope data"
        if figure_type == 'touch':
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

    def _even_datasets(self):
        level = max(
            [self.data_touch_part.shape[0], self.data_acc_part.shape[0],
             self.data_gyro_part.shape[0]])
        for i in range(level - self.data_touch_part.shape[0]):
            self.data_touch_part = self.data_touch_part.append(
                {'positionX': np.nan, 'positionY': np.nan},
                ignore_index=True)
        for i in range(level - self.data_acc_part.shape[0]):
            self.data_acc_part = self.data_acc_part.append(
                {'payload_accX': np.nan, 'payload_accY': np.nan,
                 'payload_accZ': np.nan}, ignore_index=True)
        for i in range(level - self.data_gyro_part.shape[0]):
            self.data_gyro_part = self.data_gyro_part.append(
                {'payload_alpha': np.nan, 'payload_beta': np.nan,
                 'payload_gamma': np.nan}, ignore_index=True)

    def _get_movement_datasource(self):
        self.movement_datasource = ColumnDataSource(data=dict(
            gyro_alpha=self.data_gyro_part['payload_alpha'].values,
            gyro_beta=self.data_gyro_part['payload_beta'].values,
            gyro_gamma=self.data_gyro_part['payload_gamma'].values,
            time=self.data_touch_part['time'].values,
            touch_x=self.data_touch_part['positionX'].values,
            touch_y=self.data_touch_part['positionY'].values,
            eventType=self.data_touch_part['eventType'].values,
            fingerId=self.data_touch_part['id'].values,
            force=self.data_touch_part['force'].values,
            acc_X=self.data_acc_part['payload_accX'].values,
            acc_Y=self.data_acc_part['payload_accY'].values,
            acc_Z=self.data_acc_part['payload_accZ'].values,
            time_acc=self.data_acc_part['time'].values,
            time_gyro=self.data_gyro_part['time'].values
        ))

    def _visualize_data_movement(self, data_touch):
        self.data_touch_part = data_touch
        self.finger_id = data_touch.name[-1]
        self.data_acc_part = self.data_acc[
            (self.data_acc['time'] >= self.data_touch['time'].min())
            & (self.data_acc['time'] <= self.data_touch['time'].max())]
        self.data_gyro_part = self.data_gyro[(self.data_gyro['time'] >=
                                              self.data_touch['time'].min())
                                             & (self.data_gyro['time'] <=
                                                self.data_touch['time'].max())]
        self._even_datasets()
        self._get_movement_datasource()

        if self.discrete:
            self._add_touch_circle()
        else:
            self._add_touch_line()

        self._add_acc_line()
        self._add_gyro_line()

    def _get_events_datasource(self, data):
        self.events_datasource = ColumnDataSource(data=dict(
            time=data['time'].values,
            touch_x=data['positionX'].values,
            touch_y=data['positionY'].values,
            eventType=data['eventType'].values,
            fingerId=data['id'].values,
            force=data['force'].values,
        ))
        self.finger_id = data.name

    def _visualize_touch_events(self, start):
        fill_color = self.settings_dict['touch'][self.finger_id]['color']
        if not start:
            fill_color = 'white'
        self.touch_figure.circle('touch_x', 'touch_y',
                                 source=self.events_datasource,
                                 alpha=0.9, muted_alpha=0.1, size=8,
                                 legend=self.settings_dict['touch']
                                 [self.finger_id]['key'],
                                 color=self.settings_dict['touch']
                                 [self.finger_id]['color'],
                                 muted_color=self.settings_dict['touch']
                                 [self.finger_id]['color'],
                                 fill_color=fill_color)

    def _visualize_data_events(self, data, start):
        self._get_events_datasource(data)
        self._visualize_touch_events(start)

    def show(self):
        show(self.grid)


def visualize_mobile_data(data_touch, data_acc, data_gyro, touch_width=None,
                          touch_height=None, discrete=False,
                          resolution_width=None, resolution_height=None,
                          highlight=False, acc_width=None, acc_height=None,
                          gyro_width=None, gyro_height=None):
    """
    Function that returns MobilePlot class which contains Bokeh figure with
    provided DataFrames and parameters

    :param data_touch: Pandas DataFrame with user touches, data have to have
                        the same columns as Fastar/Logger-Web logs and flatten
                         with flat_touches function from Fastar/ML-Module
    :param data_acc: Pandas DataFrame with accelerometer data, data have to
                        have the same columns as Fastar/Logger-Web logs
    :param data_gyro: Pandas DataFrame with gyroscope data, data have to
                        have the same columns as Fastar/Logger-Web logs
    :param touch_width: Integer number to set width of touch figure (optional)
    :param touch_height: Integer number to set height of touch figure
                            (optional)
    :param discrete: Boolean to set touch figure discrete (default=False)
    :param resolution_width: Integer number to set touch figure width axis
                                resolution (optional)
    :param resolution_height: Integer number to set touch figure height axis
                                resolution (optional)
    :param highlight: Boolean to set figures highlighting, touch DF has to have
                        segment column with set labeled segments to highlight
                        (default=False)
    :param acc_width: Integer number to set width of accelerometer figure
                        (optional)
    :param acc_height: Integer number to set height of accelerometer figure
                        (optional)
    :param gyro_width: Integer number to set width of gyroscope figure
                        (optional)
    :param gyro_height: Integer number to set height of gyroscope figure
                        (optional)
    :return: MobilePlot class which contains Bokeh figure with
                provided DataFrames and parameters
    """
    return _MobilePlot(data_touch, data_acc, data_gyro,
                       touch_width=touch_width, touch_height=touch_height,
                       resolution_width=resolution_width,
                       resolution_height=resolution_height,
                       discrete=discrete, highlight=highlight,
                       acc_width=acc_width, acc_height=acc_height,
                       gyro_width=gyro_width, gyro_height=gyro_height)
