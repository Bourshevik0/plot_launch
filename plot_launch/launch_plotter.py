#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines codes needed to plot using matplotlib and numpy.
"""

# Import built-in modules
import datetime
import gc
import re

# Import third-party modules
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.ticker import FuncFormatter
import numpy

# Any changes to the path and your own modules
from plot_launch import constants


class LaunchStatistics:  # pylint: disable=too-few-public-methods
    """
    Class for the statistics of orbital launches.
    """

    def __init__(self,
                 launch_info_lists,
                 group_list,
                 group_text):
        """
        Get all the statistics needed for the plot.
        :param launch_info_lists: A LaunchInfoLists object.
        :param group_list: A group to segment launch data.
        :param group_text: A text string to describe the group.
        """
        self.groups = numpy.unique(group_list)
        self.group_text = group_text
        groups_dict = {value: key for key, value in enumerate(self.groups)}
        self.groups_length = len(self.groups)

        group_set = set(self.groups)
        constant_set = set(constants.HEX_COLOR_DICT.keys())
        group_complement = group_set - constant_set
        if not group_complement:
            self.color = []
            for group_name in self.groups:
                self.color.append(constants.HEX_COLOR_DICT.get(group_name))
        elif len(group_complement) < len(self.groups):
            self.color = []
            new_color_dict = constants.HEX_COLOR_DICT.copy()
            i = 7
            color_length = len(constants.HEX_COLOR_LIST)
            compiler = re.compile(r'\(.*?\)')
            last_item = ''
            for group_item in group_complement:
                origin_item = ''.join(compiler.split(group_item))
                if origin_item in constants.HEX_COLOR_DICT and origin_item != last_item:
                    new_color_dict[group_item] = constants.HEX_COLOR_DICT[origin_item]
                else:
                    new_color_dict[group_item] = constants.HEX_COLOR_LIST[i]
                    i = (i + 1) % color_length
                last_item = origin_item
            for group_name in self.groups:
                self.color.append(new_color_dict.get(group_name))
        else:
            color_length = len(constants.HEX_COLOR_LIST)
            if self.groups_length < color_length:
                self.color = constants.HEX_COLOR_LIST[:self.groups_length]
            else:
                self.color = constants.HEX_COLOR_LIST * int(self.groups_length / color_length) + \
                             constants.HEX_COLOR_LIST[:self.groups_length % color_length]
        launch_count = len(launch_info_lists.time)
        self.total_launch_steps = numpy.zeros(
            (len(launch_info_lists.time), self.groups_length), dtype=int)
        self.successful_launch_time = []
        self.scs_array = numpy.zeros(self.groups_length, dtype=int)
        self.scs_count = 0
        self.failure_array = numpy.zeros(self.groups_length, dtype=int)
        self.failure_count = 0
        self.launch_array = numpy.zeros(self.groups_length, dtype=int)
        for i in numpy.arange(0, launch_count):
            idx = groups_dict[group_list[i]]
            if launch_info_lists.launch_result[i]:
                self.successful_launch_time.append(launch_info_lists.time[i])
                self.scs_array[idx] += 1
                self.scs_count += 1
            else:
                self.failure_array[idx] += 1
                self.failure_count += 1
            self.launch_array[idx] += 1
            if i > 0:
                self.total_launch_steps[i] = self.total_launch_steps[i - 1]
                self.total_launch_steps[i][idx] = self.total_launch_steps[i - 1][idx] + 1
            else:
                self.total_launch_steps[i][idx] = 1

        self.indices = numpy.argsort(self.launch_array)
        self.r_indices = numpy.flip(self.indices)

        self.total_launch_energy_steps = numpy.zeros(
            (self.scs_count, self.groups_length), dtype=int)
        self.total_launch_r_energy_steps = numpy.zeros(
            (self.scs_count, self.groups_length), dtype=int)
        self.total_launch_delta_v_steps = numpy.zeros(
            (self.scs_count, self.groups_length), dtype=int)
        self.total_launch_mass_steps = numpy.zeros(
            (self.scs_count, self.groups_length), dtype=int)

        i = 0
        j = 0
        while i < launch_count:
            idx = groups_dict[group_list[i]]
            if launch_info_lists.launch_result[i]:
                k = i - j
                if k > 0:
                    self.total_launch_energy_steps[k] = \
                        self.total_launch_energy_steps[k - 1]
                    self.total_launch_energy_steps[k][idx] = \
                        self.total_launch_energy_steps[k - 1][idx] + \
                        launch_info_lists.orbital_energy[i]

                    self.total_launch_r_energy_steps[k] = \
                        self.total_launch_r_energy_steps[k - 1]
                    self.total_launch_r_energy_steps[k][idx] = \
                        self.total_launch_r_energy_steps[k - 1][idx] + \
                        launch_info_lists.r_orbital_energy[i]

                    self.total_launch_delta_v_steps[k] = \
                        self.total_launch_delta_v_steps[k - 1]
                    self.total_launch_delta_v_steps[k][idx] = \
                        self.total_launch_delta_v_steps[k - 1][idx] + \
                        launch_info_lists.delta_v[i]

                    if len(launch_info_lists.payload_mass[i]) > 1:
                        self.total_launch_mass_steps[k] = \
                            self.total_launch_mass_steps[k - 1]
                        self.total_launch_mass_steps[k][idx] = \
                            self.total_launch_mass_steps[k - 1][idx] + \
                            round(sum(launch_info_lists.payload_mass[i]) * 1000)
                    else:
                        self.total_launch_mass_steps[k] = self.total_launch_mass_steps[k - 1]
                        self.total_launch_mass_steps[k][idx] = \
                            self.total_launch_mass_steps[k - 1][idx] + \
                            round(launch_info_lists.payload_mass[i][0] * 1000)
                else:
                    self.total_launch_energy_steps[k][idx] = launch_info_lists.orbital_energy[i]
                    self.total_launch_r_energy_steps[k][idx] = \
                        launch_info_lists.r_orbital_energy[i]
                    self.total_launch_delta_v_steps[k][idx] = launch_info_lists.delta_v[i]
                    if len(launch_info_lists.payload_mass[i]) > 1:
                        self.total_launch_mass_steps[k][idx] = \
                            round(sum(launch_info_lists.payload_mass[i]) * 1000)
                    else:
                        self.total_launch_mass_steps[k][idx] = \
                            round(launch_info_lists.payload_mass[i][0] * 1000)
            else:
                j = j + 1
            i = i + 1


def draw_cc_license(
        fig,
        axes,
        text_x,
        text_y,
        img_x,
        img_y,
        config_dict):
    """
    Draw CC license related things on the plot.
    :param fig: A matplot figure object.
    :param axes: A matplot axes object.
    :param text_x: The text position x from data coordinates transformed by ax.transAxes.
    :param text_y: The text position y from data coordinates transformed by ax.transAxes.
    :param img_x: The img position x from data coordinates transformed by ax.transAxes.
    :param img_y: The img position y from data coordinates transformed by ax.transAxes.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """
    text = """截至UTC时间：{end_time}
绘制者：@旋火_SwingFire
绘制脚本：https://github.com/Bourshevik0/plot_launch
本作品采用 CC BY-NC-SA 4.0 进行许可
(https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh)
""".format(end_time=config_dict['time_filter'][1].strftime('%Y/%m/%d %H:%M:%S'))
    axes.text(text_x, text_y, text,
              fontproperties=config_dict['fprop'], color='grey',
              transform=axes.transAxes, va='top')
    cc_img = mpimg.imread(constants.LICENSE_IMG_PATH)
    cc_img_ax = fig.add_axes([img_x, img_y, 0.1, 0.1], anchor='NE', transform=axes.transAxes)
    cc_img_ax.imshow(cc_img)
    cc_img_ax.axis('off')
    plt.imshow(cc_img)


def plot_launch_times(launch_statistics,
                      launch_info_lists,
                      config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param launch_info_lists: A LaunchInfoLists object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """
    x_min = config_dict['time_filter'][0]
    x_value = [x_min] + launch_info_lists.time
    x_max = config_dict['time_filter'][1]
    x_value.append(x_max)

    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])

    for j in launch_statistics.r_indices:
        y_value = launch_statistics.total_launch_steps[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=launch_statistics.color[j],
                 label='{country}({number})'.format(
                     country=launch_statistics.groups[j],
                     number=str(y_value[-1])),
                 linewidth=3)
    plt.legend(prop=config_dict['fprop'], loc=2)
    axes.text(-0.008, 0.98, launch_statistics.group_text + '(次数)',
              fontproperties=config_dict['fprop'],
              transform=axes.transAxes, va='top', ha='right')
    axes.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(5))
    axes.yaxis.set_minor_locator(matplotlib.ticker.MultipleLocator(1))

    title_text = config_dict.get('step_title')
    if title_text:
        plt.title(label=title_text, y=1.01,
                  fontproperties=config_dict['fprop_title'], fontsize=35)
    plt.xlabel('时间', fontproperties=config_dict['fprop'], fontsize=18)
    plt.ylabel('发射次数\n总数：{count}'.format(
        count=launch_statistics.scs_count + launch_statistics.failure_count),
        fontproperties=config_dict['fprop'], rotation=0, fontsize=14)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position('right')
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])
    for label in axes.get_yticklabels():
        label.set_fontproperties(config_dict['fprop'])

    y_max = axes.get_ylim()[1] - 3
    i = 5
    while i < y_max:
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)
        i = i + 5

    i = 1
    day_tuple = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_info_lists.time[0].year,
                                   month=i,
                                   day=day_tuple[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_info_lists.time[0].year,
                                       month=i,
                                       day=day_tuple[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2

    draw_cc_license(axes=axes, fig=fig, text_x=0.2, text_y=0.95,
                    img_x=0.28, img_y=0.60, config_dict=config_dict)
    plt.savefig(config_dict['step_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


def count_update_scale_value(temp, position):
    """
    :param temp:
    :param position:
    :return:
    """
    return '{result}'.format(result=int(temp))


def energy_update_scale_value(temp, position):
    """
    :param temp:
    :param position:
    :return:
    """
    result = temp / 100000
    return '{result}'.format(result=result)


def dv_update_scale_value(temp, position):
    """
    :param temp:
    :param position:
    :return:
    """
    result = int(temp / 1000)
    return '{result}'.format(result=result)


def mass_update_scale_value(temp, position):
    """
    :param temp:
    :param position:
    :return:
    """
    result = int(temp / 1000)
    return '{result}'.format(result=result)


def plot_launch_energy(launch_statistics,
                       config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """

    x_min = config_dict['time_filter'][0]
    x_value = [x_min] + launch_statistics.successful_launch_time
    x_max = config_dict['time_filter'][1]
    x_value.append(x_max)

    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])

    last_values = launch_statistics.total_launch_energy_steps[-1:].flatten()
    r_indices = numpy.flip(numpy.argsort(last_values))

    for j in r_indices:
        y_value = launch_statistics.total_launch_energy_steps[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        label_value = '{value:.3g}'.format(value=round(y_value[-1] / 100000, 2))
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=launch_statistics.color[j],
                 label='{country}({number})'.format(
                     country=launch_statistics.groups[j],
                     number=label_value),
                 linewidth=3)
    plt.legend(prop=config_dict['fprop'], loc=2)
    axes.text(-0.008, 0.98, launch_statistics.group_text + '(能量)',
              fontproperties=config_dict['fprop'],
              transform=axes.transAxes, va='top', ha='right')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(energy_update_scale_value))
    axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    title_text = config_dict.get('energy_step_title')
    if title_text:
        plt.title(label=title_text,
                  y=1.01, fontproperties=config_dict['fprop_title'], fontsize=35)

    plt.xlabel('时间', fontproperties=config_dict['fprop'], fontsize=18)
    plt.ylabel('能量\n(太焦耳)\n(TJ)', fontproperties=config_dict['fprop'], rotation=0, fontsize=14)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position('right')
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])
    for label in axes.get_yticklabels():
        label.set_fontproperties(config_dict['fprop'])

    for i in axes.yaxis.get_major_locator().tick_values(0, axes.get_ylim()[1]):
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)

    i = 1
    day_tuple = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                   month=i,
                                   day=day_tuple[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                       month=i,
                                       day=day_tuple[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2

    draw_cc_license(axes=axes, fig=fig, text_x=0.2, text_y=0.95,
                    img_x=0.28, img_y=0.60, config_dict=config_dict)
    plt.savefig(config_dict['energy_step_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


def plot_launch_r_energy(launch_statistics,
                         config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """
    x_min = config_dict['time_filter'][0]

    x_value = [x_min] + launch_statistics.successful_launch_time
    x_max = config_dict['time_filter'][1]
    x_value.append(x_max)

    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])

    last_values = launch_statistics.total_launch_r_energy_steps[-1:].flatten()
    r_indices = numpy.flip(numpy.argsort(last_values))

    for j in r_indices:
        y_value = launch_statistics.total_launch_r_energy_steps[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        label_value = '{value:.3g}'.format(value=round(y_value[-1] / 100000, 2))
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=launch_statistics.color[j],
                 label='{country}({number})'.format(
                     country=launch_statistics.groups[j],
                     number=label_value),
                 linewidth=3)
    plt.legend(prop=config_dict['fprop'], loc=2)
    axes.text(-0.008, 0.98, launch_statistics.group_text + '(比能量)',
              fontproperties=config_dict['fprop'],
              transform=axes.transAxes, va='top', ha='right')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(energy_update_scale_value))
    axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    title_text = config_dict.get('r_energy_step_title')
    if title_text:
        plt.title(label=title_text,
                  y=1.01, fontproperties=config_dict['fprop_title'], fontsize=35)
    plt.xlabel('时间', fontproperties=config_dict['fprop'], fontsize=18)
    plt.ylabel('比能量\n(吉焦耳/千克)\n(GJ/kg)', fontproperties=config_dict['fprop'],
               rotation=0, fontsize=12)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position('right')
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])
    for label in axes.get_yticklabels():
        label.set_fontproperties(config_dict['fprop'])

    for i in axes.yaxis.get_major_locator().tick_values(0, axes.get_ylim()[1]):
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)

    i = 1
    day_tuple = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                   month=i,
                                   day=day_tuple[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                       month=i,
                                       day=day_tuple[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2

    draw_cc_license(axes=axes, fig=fig, text_x=0.2, text_y=0.95,
                    img_x=0.28, img_y=0.60, config_dict=config_dict)
    plt.savefig(config_dict['r_energy_step_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


def plot_launch_delta_v(launch_statistics,
                        config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """
    x_min = config_dict['time_filter'][0]

    x_value = [x_min] + launch_statistics.successful_launch_time
    x_max = config_dict['time_filter'][1]
    x_value.append(x_max)

    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])

    last_values = launch_statistics.total_launch_delta_v_steps[-1:].flatten()
    r_indices = numpy.flip(numpy.argsort(last_values))

    for j in r_indices:
        y_value = launch_statistics.total_launch_delta_v_steps[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        label_value = '{value:.3g}'.format(value=round(y_value[-1] / 1000, 2))
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=launch_statistics.color[j],
                 label='{country}({number})'.format(
                     country=launch_statistics.groups[j],
                     number=label_value),
                 linewidth=3)
    plt.legend(prop=config_dict['fprop'], loc=2)
    axes.text(-0.008, 0.98, launch_statistics.group_text + '(dv)',
              fontproperties=config_dict['fprop'],
              transform=axes.transAxes, va='top', ha='right')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(dv_update_scale_value))
    axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    title_text = config_dict.get('delta_v_step_title')
    if title_text:
        plt.title(label=title_text,
                  y=1.01, fontproperties=config_dict['fprop_title'], fontsize=35)
    plt.xlabel('时间', fontproperties=config_dict['fprop'], fontsize=18)
    plt.ylabel('dv\n(千米/秒)\n(km/s)', fontproperties=config_dict['fprop'],
               rotation=0, fontsize=12)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position('right')
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])
    for label in axes.get_yticklabels():
        label.set_fontproperties(config_dict['fprop'])

    for i in axes.yaxis.get_major_locator().tick_values(0, axes.get_ylim()[1]):
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)

    i = 1
    day_tuple = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                   month=i,
                                   day=day_tuple[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                       month=i,
                                       day=day_tuple[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2

    draw_cc_license(axes=axes, fig=fig, text_x=0.2, text_y=0.95,
                    img_x=0.28, img_y=0.60, config_dict=config_dict)
    plt.savefig(config_dict['delta_v_step_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


def plot_launch_mass(launch_statistics,
                     config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """

    x_min = config_dict['time_filter'][0]

    x_value = [x_min] + launch_statistics.successful_launch_time
    x_max = config_dict['time_filter'][1]
    x_value.append(x_max)

    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])

    last_values = launch_statistics.total_launch_mass_steps[-1:].flatten()
    r_indices = numpy.flip(numpy.argsort(last_values))

    for j in r_indices:
        y_value = launch_statistics.total_launch_mass_steps[:, j]
        y_value = numpy.append(0, y_value)
        y_value = numpy.append(y_value, y_value[-1])
        label_value = '{value:.3g}'.format(value=round(y_value[-1] / 1000, 2))
        plt.plot(x_value, y_value,
                 drawstyle='steps-post',
                 color=launch_statistics.color[j],
                 label='{country}({number})'.format(
                     country=launch_statistics.groups[j],
                     number=label_value),
                 linewidth=3)
    plt.legend(prop=config_dict['fprop'], loc=2)
    axes.text(-0.008, 0.98, launch_statistics.group_text + '(质量)',
              fontproperties=config_dict['fprop'],
              transform=axes.transAxes, va='top', ha='right')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(mass_update_scale_value))
    axes.yaxis.set_minor_locator(matplotlib.ticker.AutoMinorLocator())

    title_text = config_dict.get('mass_step_title')
    if title_text:
        plt.title(label=title_text,
                  y=1.01, fontproperties=config_dict['fprop_title'], fontsize=35)
    plt.xlabel('时间', fontproperties=config_dict['fprop'], fontsize=16)
    plt.ylabel('质量\n(吨，t)', fontproperties=config_dict['fprop'], rotation=0, fontsize=16)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(1.075, 0.5)
    plt.ylim(ymin=0)
    plt.xlim(x_min,
             xmax=x_max)
    axes.yaxis.tick_right()
    axes.yaxis.set_label_position('right')
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])
    for label in axes.get_yticklabels():
        label.set_fontproperties(config_dict['fprop'])

    for i in axes.yaxis.get_major_locator().tick_values(0, axes.get_ylim()[1]):
        plt.axhline(y=i, color=constants.DEFAULT_AXLINE_COLOR, linestyle='solid', linewidth=0.5)

    i = 1
    day_tuple = (1, 16)
    j = 1
    datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                   month=i,
                                   day=day_tuple[j])

    while datetime_i < x_max and i < 13:
        datetime_i = datetime.datetime(year=launch_statistics.successful_launch_time[0].year,
                                       month=i,
                                       day=day_tuple[j])
        plt.axvline(x=datetime_i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
        i = i + j % 2
        j = j + 1
        j = j % 2
    draw_cc_license(axes=axes, fig=fig, text_x=0.2, text_y=0.95,
                    img_x=0.28, img_y=0.60, config_dict=config_dict)
    plt.savefig(config_dict['mass_step_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()


def font_resize(axes,
                text_length,
                font_size,
                rect_wh):
    """
    Resize the font from font_size.
    Ref: https://stackoverflow.com/questions/59794014/convert-pixel-coordinates-to-data-coordinates-in-matplotlib
    https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html
    :param axes: A matplot axes object.
    :param text_length: The length of the text.
    :param font_size: The font_size(in pixel-coordinates) before being resized.
    :param rect_wh: The rectangle limitation(in data-coordinates) to check
    if it is necessary to resize.
    :return font_size: The font_size after being resized.
    """
    origin_xy = axes.transData.transform((0.0, 0.0))
    rect_xy = axes.transData.transform(rect_wh)
    rect_pix = (rect_xy[0] - origin_xy[0], rect_xy[1] - origin_xy[1])
    if text_length > 1:
        rect_font_w = int(rect_pix[0] / (text_length * 2 - 0.2))
        # rect_pix[0] = ((text_length - 1) * 0.2 + text_length * 1.8) * rect_font_w
        # rect_pix[0] = (text_length * 2 - 0.2) * rect_font_w
    else:
        rect_font_w = int(rect_pix[0])
    if font_size > rect_font_w:
        font_size = int(rect_font_w)
    if font_size > rect_pix[1]:
        font_size = int(rect_pix[1])
    return font_size


def draw_labels_on_bars(axes,
                        config_dict):
    """
    Draw the labels on the bars.
    :param axes: A matplot axes object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return axes: A matplot axes object.
    """
    y_x_dict = dict()
    default_font_size = 24

    for rect in axes.patches:
        x_value = rect.get_width()
        if x_value <= 0:
            continue
        text_length = len(str(x_value))
        font_size = font_resize(axes=axes,
                                text_length=text_length,
                                font_size=default_font_size,
                                rect_wh=(x_value, rect.get_height()))
        if text_length > 1:
            x_offset = font_size * (0.1 - text_length)
        elif font_size < default_font_size:
            x_offset = font_size * (-0.9)
        else:
            x_offset = - font_size
        y_value = rect.get_y() + rect.get_height() * 0.5
        label_value = x_value
        if y_value not in y_x_dict:
            y_x_dict[y_value] = x_value
        else:
            x_value = y_x_dict[y_value] + x_value
        label = '{:.0f}'.format(label_value)
        axes.annotate(
            label,
            (x_value, y_value),
            xytext=(x_offset, font_size * (-0.5)),
            textcoords='offset pixels',
            color='#FFFFFF',
            rotation=0,
            fontsize=font_size,
            fontproperties=config_dict['fprop'])


def plot_launch_bar(launch_statistics,
                    config_dict):
    """
    :param launch_statistics: A LaunchStatistics object.
    :param config_dict: A dictionary to control the plotting procedure.
    :return None:
    """
    indices = launch_statistics.indices
    y_axis_labels = []
    for country in launch_statistics.groups[indices]:
        y_axis_labels.append(country)
    fig, axes = plt.subplots(1,
                             figsize=config_dict['fig_size'],
                             dpi=config_dict['dpi'])
    axes.yaxis.set_ticks(numpy.arange(0, launch_statistics.groups_length), rotation=0)
    axes.yaxis.set_ticklabels(y_axis_labels, fontproperties=config_dict['fprop'],
                              rotation=0, fontsize=20)
    for label in axes.get_xticklabels():
        label.set_fontproperties(config_dict['fprop'])

    plt.barh(launch_statistics.groups, launch_statistics.scs_array[indices],
             color=constants.STATUS_COLOR_DICT['成功'], label='成功')
    plt.barh(launch_statistics.groups, launch_statistics.failure_array[indices],
             left=launch_statistics.scs_array[indices],
             color=constants.STATUS_COLOR_DICT['失败'], label='失败')

    major_ticks = axes.xaxis.get_major_locator().tick_values(0, axes.get_xlim()[1])

    x_max = axes.get_xlim()[1]
    if x_max == launch_statistics.scs_array[indices][-1] \
            + launch_statistics.failure_array[indices][-1]:
        if major_ticks[1] < 1:
            delta = 1.0
        else:
            delta = major_ticks[1]
        x_max = float(launch_statistics.scs_array[indices][-1]) \
            + float(launch_statistics.failure_array[indices][-1]) + delta
        axes.set_xlim(xmax=x_max)

    if major_ticks[1] < 1:
        axes.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(1))
        major_ticks = axes.xaxis.get_major_locator().tick_values(0, axes.get_xlim()[1])

    for i in major_ticks:
        plt.axvline(x=i,
                    color=constants.DEFAULT_AXLINE_COLOR,
                    linestyle='solid',
                    linewidth=1)
    draw_labels_on_bars(axes=axes, config_dict=config_dict)
    plt.gca().xaxis.set_major_formatter(FuncFormatter(count_update_scale_value))
    title_text = config_dict.get('bar_title')
    if title_text:
        plt.title(label=title_text,
                  y=1.01, fontproperties=config_dict['fprop_title'], fontsize=35)

    plt.xlabel('发射次数(总数：{total}，失败：{failure})'.format(
        total=launch_statistics.scs_count + launch_statistics.failure_count,
        failure=launch_statistics.failure_count),
        fontproperties=config_dict['fprop'], fontsize=18)
    plt.ylabel(launch_statistics.group_text,
               fontproperties=config_dict['fprop'], rotation=0, fontsize=16)
    axes.xaxis.set_label_coords(0.5, -0.06)
    axes.yaxis.set_label_coords(0, 1.0)
    plt.legend(prop=config_dict['fprop'], loc=1)

    draw_cc_license(axes=axes, fig=fig, text_x=0.5, text_y=0.3,
                    img_x=0.515, img_y=0.1, config_dict=config_dict)

    plt.savefig(config_dict['bar_filename'])
    plt.cla()
    plt.clf()
    plt.close('all')
    gc.collect()
