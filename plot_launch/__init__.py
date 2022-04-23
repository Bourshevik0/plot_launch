#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's commandline entry point functionality.
"""
# Import built-in modules
import sys
import json
import os
import gc

# Import third-party modules
import matplotlib

# Any changes to the path and your own modules
from plot_launch import constants
from plot_launch import launch_info
from plot_launch import launch_plotter


def main():
    """
    Run plot_launch as a command-line program.
    :return None:
    """
    matplotlib.use('Agg')
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as config_file:
            config_dict = json.load(config_file)
    else:
        config_dict = None

    config_dict = launch_info.prcs_config_dict(config_dict)

    launch_info_lists = launch_info.get_launch_info_from_files(constants.DATA_PATH,
                                                               config_dict=config_dict)
    # info_set = set()
    # for data_dict in launch_info_lists.data_dicts:
    #     info_set = info_set | set(data_dict.keys())

    if 'image_seq' not in config_dict:
        launch_statistics = launch_plotter.LaunchStatistics(
            launch_info_lists=launch_info_lists,
            group_list=launch_info_lists.launcher_man_country)

        if 'step_filename' in config_dict:
            launch_plotter.plot_launch_times(launch_statistics=launch_statistics,
                                             launch_info_lists=launch_info_lists,
                                             config_dict=config_dict)
        if 'energy_step_filename' in config_dict:
            launch_plotter.plot_launch_energy(launch_statistics=launch_statistics,
                                              config_dict=config_dict)
        if 'r_energy_step_filename' in config_dict:
            launch_plotter.plot_launch_r_energy(launch_statistics=launch_statistics,
                                                config_dict=config_dict)
        if 'delta_v_step_filename' in config_dict:
            launch_plotter.plot_launch_delta_v(launch_statistics=launch_statistics,
                                               config_dict=config_dict)

        if 'mass_step_filename' in config_dict:
            launch_plotter.plot_launch_mass(launch_statistics=launch_statistics,
                                            config_dict=config_dict)

        if 'bar_filename' in config_dict:
            launch_plotter.plot_launch_bar(launch_statistics=launch_statistics,
                                           config_dict=config_dict)

        if 'latest_month_bar' in config_dict:
            new_lists = launch_info.LaunchInfoLists()
            i, j = launch_info_lists.get_slice_from_datetime(
                datetime_start=config_dict['latest_month_start'],
                datetime_end=config_dict['latest_month_end'])
            if j:
                launch_info_lists.slice_info(new_lists, i, j)
                new_statistics = launch_plotter.LaunchStatistics(
                    launch_info_lists=new_lists,
                    group_list=new_lists.launcher_man_country)
                config_dict['bar_filename'] = config_dict['latest_month_bar']
                config_dict['bar_title'] = config_dict['month_title']
                launch_plotter.plot_launch_bar(launch_statistics=new_statistics,
                                               config_dict=config_dict)
    else:
        launch_count = len(launch_info_lists.time) + 1
        i = 0
        new_lists = launch_info.LaunchInfoLists()
        time_end = config_dict['time_filter'][1]
        dv_filename_list = os.path.splitext(config_dict['delta_v_step_filename'])
        m_filename_list = os.path.splitext(config_dict['mass_step_filename'])
        e_filename_list = os.path.splitext(config_dict['energy_step_filename'])
        for j in range(1, launch_count):
            launch_info_lists.slice_info(new_lists, i, j)
            launch_statistics = launch_plotter.LaunchStatistics(
                launch_info_lists=new_lists,
                group_list=new_lists.launcher_man_country)
            if j < launch_count - 1:
                config_dict['time_filter'][1] = launch_info_lists.time[j]
            else:
                config_dict['time_filter'][1] = time_end
            if 'delta_v_step_filename' in config_dict:
                config_dict['delta_v_step_filename'] = \
                    f'{dv_filename_list[0]}{j:03d}{dv_filename_list[1]}'
                launch_plotter.plot_launch_delta_v(launch_statistics=launch_statistics,
                                                   config_dict=config_dict)
            if 'mass_step_filename' in config_dict:
                config_dict['mass_step_filename'] = \
                    f'{m_filename_list[0]}{j:03d}{m_filename_list[1]}'
                launch_plotter.plot_launch_mass(launch_statistics=launch_statistics,
                                                config_dict=config_dict)
            if 'energy_step_filename' in config_dict:
                config_dict['energy_step_filename'] = \
                    f'{e_filename_list[0]}{j:03d}{e_filename_list[1]}'
                launch_plotter.plot_launch_energy(launch_statistics=launch_statistics,
                                                  config_dict=config_dict)
            del launch_statistics
            del new_lists
            new_lists = launch_info.LaunchInfoLists()
            gc.collect()

