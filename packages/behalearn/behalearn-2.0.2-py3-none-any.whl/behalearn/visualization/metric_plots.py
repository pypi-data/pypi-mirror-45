from bokeh.io import output_notebook, show
from bokeh.plotting import figure, ColumnDataSource
import numpy as np
from bokeh.models import HoverTool
from behalearn.metrics import fmr_score, fnmr_score, true_positive_rate


def trapezoid_diagonal_intersection(A, B, C, D):
    """
    Calculates coordinates of point which is intersection of trapezoid
    diagonal. Trapezoid bases are lines BC and AD.

    :param A: point A (tuple) of trapezoid
    :param B: point B (tuple) of trapezoid
    :param C: point C (tuple) of trapezoid
    :param D: point D (tuple) of trapezoid
    :return: threshold, EER value; coordinates of diagonal intersection
    """
    A_x, A_y = A
    _, B_y = B
    C_x, C_y = C
    _, D_y = D
    bc = abs(A_y - B_y)
    ad = abs(C_y - D_y)
    bd = np.sqrt(((C_y - A_y) ** 2) + ((C_x - A_x) ** 2))

    ratio = bc / ad

    x = bd / (ratio + 1)

    dx = (x / bd) * abs(C_x - A_x)
    dy = (x / bd) * abs(C_y - A_y)

    return C_x + dx, C_y - dy


def calc_err(thresholds, fmrs, fnmrs):
    """
    Calculates EER and threshold value where it appears.

    :param thresholds: array of thresholds
    :param fmrs: array of FAR errors corresponding to threshold
    :param fnmrs: array of FRR errors corresponding to threshold
    :return: threshold, eer
    """
    for i in range(len(fmrs)):
        if fmrs[i] == fnmrs[i]:
            return thresholds[i], fmrs[i]
        if fnmrs[i] > fmrs[i]:
            return trapezoid_diagonal_intersection(
                (thresholds[i], fmrs[i]),
                (thresholds[i], fnmrs[i]),
                (thresholds[i-1], fmrs[i-1]),
                (thresholds[i-1], fnmrs[i-1])
            )


def plot_far_frr_eer(data, thresholds):
    """
    Plots FAR, FRR and EER for each user dataframe was trained for

    :param data: DataFrame containing columns: user_train, proba1 & y_test
    :param thresholds: array of thresholds
    :return:
    """
    tested_users = data.user_train.unique()

    for t_user in tested_users:
        fmrs = []
        fnmrs = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            fmrs.append(fmr_score(t_user_data.y_test, y_pred_thr))
            fnmrs.append(fnmr_score(t_user_data.y_test, y_pred_thr))
        eer_thr, eer = calc_err(thresholds, fmrs, fnmrs)

        output_notebook()

        plt = figure(
            tools="pan,box_zoom,reset,save",
            x_axis_label='threshold', y_axis_label='error'
        )

        curve_data_source = ColumnDataSource(data=dict(
            threshold=thresholds,
            fmr=fmrs,
            fnmr=fnmrs,
        ))

        eer_data_source = ColumnDataSource(data=dict(
            eer_thr=[eer_thr],
            eer=[eer]
        ))

        hover = HoverTool(names=['fmr', 'fnmr'], tooltips=[
            ('threshold', '@threshold'),
            ('fmr', '@fmr{0.00%}'),
            ('fnmr', '@fnmr{0.00%}')
        ])

        hover_eer = HoverTool(names=['eer'], tooltips=[
            ('threshold', '@eer_thr'),
            ('errors', '@eer{0.00%}')
        ])

        plt.add_tools(hover)
        plt.add_tools(hover_eer)

        plt.line('threshold', 'fmr', name='fmr', line_color='red',
                 legend='FMR', source=curve_data_source)
        plt.line('threshold', 'fnmr', name='fnmr', line_color='blue',
                 legend='FNMR', source=curve_data_source)
        plt.circle('eer_thr', 'eer', name='eer', fill_color='green', size=10,
                   legend='EER', source=eer_data_source)

    show(plt)


def plot_det_curve(data, thresholds, scale_log=False):
    """
        Plots DET curve with EER point for each user dataframe was trained for

        :param data: DataFrame containing columns: user_train, proba1 & y_test
        :param thresholds: array of thresholds
        :return:
        """
    tested_users = data.user_train.unique()

    for t_user in tested_users:
        fmrs = []
        fnmrs = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            fmrs.append(fmr_score(t_user_data.y_test, y_pred_thr))
            fnmrs.append(fnmr_score(t_user_data.y_test, y_pred_thr))
        eer_thr, eer = calc_err(thresholds, fmrs, fnmrs)

        output_notebook()

        if (scale_log):
            plt = figure(
                tools="pan,box_zoom,reset,save", x_axis_type="log",
                y_axis_type="log",
                x_axis_label='false match rate',
                y_axis_label='false non-match rate'
            )
        else:
            plt = figure(
                tools="pan,box_zoom,reset,save",
                x_axis_label='false match rate',
                y_axis_label='false non-match rate'
            )
            plt.line([0, 1], [0, 1], line_dash=[1, 5], line_color='gray')

        curve_data_source = ColumnDataSource(data=dict(
            threshold=thresholds,
            fmr=fmrs,
            fnmr=fnmrs,
        ))

        eer_data_source = ColumnDataSource(data=dict(
            eer_thr=[eer_thr],
            eer=[eer]
        ))

        hover = HoverTool(names=['fmr'], tooltips=[
            ('threshold', '@threshold'),
            ('fmr', '@fmr{0.00%}'),
            ('fnmr', '@fnmr{0.00%}')
        ])

        hover_eer = HoverTool(names=['eer'], tooltips=[
            ('threshold', '@eer_thr'),
            ('errors', '@eer{0.00%}')
        ])

        plt.add_tools(hover)
        plt.add_tools(hover_eer)

        plt.line('fmr', 'fnmr', name='fmr', line_color='red', legend='DET',
                 source=curve_data_source)
        plt.circle('eer', 'eer', name='eer', fill_color='green', size=10,
                   legend='EER', source=eer_data_source)

    show(plt)


def plot_roc_curve(data, thresholds):
    """
    Plots ROC curve for each user dataframe was trained for

    :param data: DataFrame containing columns: user_train, proba1 & y_test
    :param thresholds: array of thresholds
    :return:
    """

    tested_users = data.user_train.unique()

    for t_user in tested_users:
        true_positive_rates = []
        false_match_rates = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            true_positive_rates.append(true_positive_rate(t_user_data.y_test,
                                                          y_pred_thr))
            false_match_rates.append(fmr_score(t_user_data.y_test, y_pred_thr))

        # plt.plot(false_match_rates, true_positive_rates, 'b-')
        output_notebook()

        plt = figure(
            tools="pan,box_zoom,reset,save",
            x_axis_label='false match rate', y_axis_label='true positive rate'
        )

        curve_data_source = ColumnDataSource(data=dict(
            threshold=thresholds,
            fmr=false_match_rates,
            tpr=true_positive_rates
        ))

        hover = HoverTool(tooltips=[
            ('threshold', '@threshold'),
            ('fmr', '@fmr{0.00%}'),
            ('tpr', '@tpr{0.00%}')
        ])

        plt.add_tools(hover)

        plt.line('fmr', 'tpr', line_color='blue', legend='ROC',
                 source=curve_data_source)

    show(plt)
