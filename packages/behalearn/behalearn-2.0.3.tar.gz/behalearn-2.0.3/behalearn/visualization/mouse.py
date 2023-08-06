from bokeh.io import output_notebook, show
from bokeh.models import HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import ColumnDataSource, figure
from behalearn.visualization.utils import add_background_image
from behalearn.visualization.utils import max_min_diff
from behalearn.visualization.utils import max_min_range, min_max_range
from behalearn.visualization.utils import format_time_to_s
import warnings


class _MousePlot:

    def __init__(self, data, view_mode,
                 width=None, height=None,
                 discrete=False,
                 resolution_width=None, resolution_height=None,
                 highlight=False, x_columns=None, y_columns=None):
        self.data = data
        self.view_mode = view_mode

        self.width = width
        self.height = height
        self.discrete = discrete
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.highlight = highlight

        self.mouse_move_data = data[(data['eventType'] == 'MOUSE_MOVE')]
        self.mouse_up_down_data = data[(data['eventType'] == 'MOUSE_UP')
                                       | (data['eventType'] == 'MOUSE_DOWN')]
        self.x_columns = x_columns
        self.y_columns = y_columns

        self._init()

    def add_background_img(self, img_url, img_start_x=None, img_start_y=None):
        if img_url is None:
            raise RuntimeError("img is none")

        if None not in (img_start_x, img_start_y):
            x = img_start_x
            y = img_start_y
        else:
            x = self.data['payload_positionX'].min()
            y = self.data['payload_positionY'].min()

        w = max_min_diff(self.data['payload_positionX'])
        h = max_min_diff(self.data['payload_positionY']) * 0.92
        add_background_image(self.p, img_url, x, y, w, h)
        return self

    def show(self):
        show(self.p)

    def _init(self):
        output_notebook()
        self.p = self._create_figure()

        if self.view_mode is None:
            warnings.warn("You have to choose view_mode - both_axes /"
                          " time_axis")

        if self.view_mode not in ['both_axes', 'time_axis']:
            warnings.warn("Choose between 2 modes - both_axes / time_axis")

        if self.x_columns is None and self.y_columns is None and \
                self.view_mode == 'both_axes':
            self.x_columns = ['payload_positionX']
            self.y_columns = ['payload_positionY']

        if self.x_columns is None and self.view_mode == 'time_axis':
            self.x_columns = ['time'] * len(self.y_columns)

        if len(self.x_columns) != len(self.y_columns):
            warnings.warn("There have to be same amount of x and y columns")

        for x_column, y_column in zip(self.x_columns, self.y_columns):
            self.x_column = x_column
            self.y_column = y_column
            self._set_resolution()
            self._add_background_line()

            if self.discrete:
                self._handle_discrete()
            else:
                self._handle_joint()

            self._add_generic_params()

    def _get_datasource(self, data):
        return ColumnDataSource(data=dict(
            x=data[self.x_column].values,
            y=data[self.y_column].values,
            eventType=data['eventType'].values,
            time=format_time_to_s(data['time'].values),
        ))

    def _handle_discrete(self):
        if self.highlight and 'segment' in self.mouse_move_data:
            self.mouse_move_data.groupby('segment').apply(self._add_circle)
        elif not self.highlight:
            self._add_circle(self.mouse_move_data)

    def _handle_joint(self):
        if self.highlight and 'segment' in self.mouse_move_data:
            self.mouse_move_data.groupby('segment').apply(self._add_line)
        elif not self.highlight:
            self._add_line(self.mouse_move_data)

    def _create_figure(self):
        if None not in (self.width, self.height):
            return figure(plot_width=self.width, plot_height=self.height)

        warnings.warn("You have to set both dimensions")
        return figure()

    def _set_resolution(self):
        data = self.data
        resolution_width = self.resolution_width
        resolution_height = self.resolution_height

        if None not in (resolution_width, resolution_height):
            self.p.y_range = Range1d(resolution_height, 0)
            self.p.x_range = Range1d(0, resolution_width)
        else:
            warnings.warn("You have to set both dimensions (resolution)")
            self.p.y_range = max_min_range(data[self.y_column], offset=50)
            self.p.x_range = min_max_range(data[self.x_column], offset=50)

    def _add_generic_params(self):
        self.p.circle('x', 'y',
                      source=self._get_datasource(self.mouse_up_down_data),
                      size=8, color="red", alpha=0.5)

        tooltips = [
            ('X', '@x'),
            ('Y', '@y'),
            ('eventType', '@eventType'),
            ('time', '@time')
        ]

        self.p.add_tools(HoverTool(tooltips=tooltips))
        self.p.y_range = Range1d(self.data[self.x_column].max(),
                                 self.data[self.y_column].min())

    def _add_line(self, data):
        line_data_source = self._get_datasource(data)

        if self.highlight:
            self.p.line('x', 'y', source=line_data_source, line_width=2,
                        hover_line_color="firebrick",
                        alpha=0.5, hover_alpha=1)
        else:
            self.p.line('x', 'y', source=line_data_source, line_width=2,
                        alpha=0.9)

    def _add_circle(self, data):
        circle_data_source = self._get_datasource(data)

        if self.highlight:
            self.p.circle('x', 'y', source=circle_data_source, size=5,
                          hover_line_color="firebrick",
                          alpha=0.5, hover_alpha=1)
        else:
            self.p.circle('x', 'y', source=circle_data_source, size=5)

    def _add_background_line(self):
        datasource = self._get_datasource(self.data)

        self.p.line('x', 'y', source=datasource, line_width=2,
                    alpha=0.4, color="#C0C0C0")


def visualize_mouse_data(data, view_mode, width=None, height=None,
                         resolution_width=None, resolution_height=None,
                         discrete=False, highlight=False,
                         x_columns=None, y_columns=None):
    """

    :param data: Pandas DataFrame with user touches, data have to have
                    the same columns as Fastar/Logger-Web
    :param view_mode: There are 2 possible modes to view - both_axes /
                        time_axis.
                        both_axes - columns from list x_columns are displayed
                                     on x-axis and columns from list
                                     y_columns are displayed on y-axis,
                                     parameters x_columns and y_columns should
                                     not be None
                        time_axis - on x-axis is always time column and columns
                                    from list y_columns are displayed
                                    on y-axis, parameter y_columns should
                                    not be None
    :param width: Integer number to set width of figure (optional)
    :param height: Integer number to set height of figure (optional)
    :param resolution_width: Integer number to set figure width axis
                                resolution (optional)
    :param resolution_height: Integer number to set figure height axis
                                resolution (optional)
    :param discrete: Boolean to set touch figure discrete (default=False)
    :param highlight: Boolean to set figures highlighting, touch DF has to have
                        segment column with set labeled segments to highlight
                        (default=False)
    :param x_columns: list of columns to display on x-axis
    :param y_columns: list of columns to display on y-axis
    :return: MousePlot class which contains Bokeh figure with
                provided DataFrames and parameters
    """
    return _MousePlot(data, view_mode,
                      width=width, height=height,
                      resolution_width=resolution_width,
                      resolution_height=resolution_height,
                      discrete=discrete, highlight=highlight,
                      x_columns=x_columns, y_columns=y_columns)
