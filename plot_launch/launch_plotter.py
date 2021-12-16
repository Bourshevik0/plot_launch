#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines codes needed to plot using matplotlib and numpy.
"""

# Import built-in modules
import datetime

# Import third-party modules
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy

# Any changes to the path and your own modules
from plot_launch import constants


class LaunchStatistics:  # pylint: disable=too-few-public-methods
    """
    Class for the statistics of orbital launches.
    """

    def __init__(self,
                 launch_info_lists):
        """
        Get all the statistics needed for the plot.
        :param launch_info_lists: A LaunchInfoLists object.
        """
        self.countries = numpy.unique(launch_info_lists.launcher_man_country)
        countries_length = len(self.countries)
        self.launch_time_total = numpy.zeros(
            (len(launch_info_lists.time), countries_length), dtype=int)
        self.launch_success = numpy.zeros(countries_length, dtype=int)
        self.launch_failure = numpy.zeros(countries_length, dtype=int)
        self.launch_overall = numpy.zeros(countries_length, dtype=int)
        for i in numpy.arange(0, len(launch_info_lists.time)):
            idx = [j for j, x in enumerate(self.countries)
                   if x == launch_info_lists.launcher_man_country[i]]
            idx = idx[0]
            if launch_info_lists.launch_result[i]:
                self.launch_success[idx] += 1
            else:
                self.launch_failure[idx] += 1
            self.launch_time_total[i][idx] = 1
            self.launch_overall[idx] += 1
            if i > 0:
                self.launch_time_total[i] = self.launch_time_total[i - 1]
                self.launch_time_total[i][idx] = self.launch_time_total[i - 1][idx] + 1


def plot_launch_statistics(launch_statistics,
                           launch_info_lists,
                           figure_filename=constants.FIGURE_PATH):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param launch_info_lists: A LaunchInfoLists object.
    :param figure_filename: The filename to save the plotted figure.
    :return None:
    """
    matplotlib.rcParams.update({'font.size': constants.DEFAULT_FONTSIZE})
    fprop_title = fm.FontProperties(fname=constants.FONT_PATH)
    fprop = fm.FontProperties(fname=constants.FONT_PATH)

    x_min = datetime.datetime(year=launch_info_lists.time[0].year,
                              month=1,
                              day=1)
    x_value = [x_min] + launch_info_lists.time
    x_max = datetime.datetime.utcnow()
    x_value.append(x_max)

    fig, ax = plt.subplots(1,
                           figsize=constants.DEFAULT_FIGSIZE,
                           dpi=constants.DEFAULT_DPI)

    for j in numpy.arange(0, len(launch_statistics.countries)):
        y_value = launch_statistics.launch_time_total[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=constants.HEX_COLOR_DICT[launch_statistics.countries[j]],
                 label="{country}({number})".format(
                     country=launch_statistics.countries[j],
                     number=str(y_value[-1])),
                 linewidth=3)
    plt.legend(prop=fprop)
    ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    ax.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))

    text = """截至UTC时间：{cur_time}
绘制者：@旋火_SwingFire
绘制脚本：https://github.com/Bourshevik0/plot_launch
本作品采用 CC BY-NC-SA 4.0 进行许可
(https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)
""".format(cur_time=constants.CURRENT_TIME)

    ax.text(0.2, 0.95, text,
            fontproperties=fprop, color="grey",
            transform=ax.transAxes, va='top')
    plt.title(label='{year}年世界航天入轨发射统计'.format(
        year=launch_info_lists.time[0].year), y=1.01,
        fontproperties=fprop_title, fontsize=35)
    plt.xlabel('时间', fontproperties=fprop, fontsize=18)
    plt.ylabel('发射次数', fontproperties=fprop, rotation=0, fontsize=18)
    ax.xaxis.set_label_coords(0.5, -0.06)
    ax.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')

    y_max = ax.get_ylim()[1] - 3
    i = 5
    while i < y_max:
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)
        i = i + 5

    i = 1
    d = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_info_lists.time[0].year,
                                   month=i,
                                   day=d[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_info_lists.time[0].year,
                                       month=i,
                                       day=d[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2

    cc_img = mpimg.imread(constants.LICENSE_IMG_PATH)
    cc_img_ax = fig.add_axes([0.28, 0.60, 0.1, 0.1], anchor='NE')
    cc_img_ax.imshow(cc_img)
    cc_img_ax.axis('off')
    plt.imshow(cc_img)
    plt.savefig(figure_filename)
