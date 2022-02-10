#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's commandline entry point functionality.
"""
# Import built-in modules
import sys
import json

# Import third-party modules

# Any changes to the path and your own modules
from plot_launch import constants
from plot_launch import launch_info
from plot_launch import launch_plotter


def main():
    """
    Run plot_launch as a command-line program.
    :return None:
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding='utf-8') as config_file:
            config_dict = json.load(config_file)
    else:
        config_dict = None

    config_dict = launch_info.prcs_config_dict(config_dict)

    launch_info_lists = launch_info.get_launch_info_from_files(constants.DATA_PATH,
                                                               config_dict=config_dict)
    launch_statistics = launch_plotter.LaunchStatistics(launch_info_lists)

    if 'step_filename' in config_dict:
        launch_plotter.plot_launch_times_by_country(launch_statistics=launch_statistics,
                                                    launch_info_lists=launch_info_lists,
                                                    config_dict=config_dict)
    if 'energy_step_filename' in config_dict:
        launch_plotter.plot_launch_energy_by_country(launch_statistics=launch_statistics,
                                                     config_dict=config_dict)
    if 's_energy_step_filename' in config_dict:
        launch_plotter.plot_launch_s_energy_by_country(launch_statistics=launch_statistics,
                                                       config_dict=config_dict)

    if 'mass_step_filename' in config_dict:
        launch_plotter.plot_launch_mass_by_country(launch_statistics=launch_statistics,
                                                   config_dict=config_dict)

    if 'bar_filename' in config_dict:
        launch_plotter.plot_launch_bar_by_country(launch_statistics=launch_statistics,
                                                  config_dict=config_dict)

    if 'latest_month_bar' in config_dict:
        new_lists = launch_info.LaunchInfoLists()
        i, j = launch_info_lists.get_slice_from_datetime(
            datetime_start=config_dict['latest_month_start'],
            datetime_end=config_dict['latest_month_end'])
        if j:
            launch_info_lists.slice_info(new_lists, i, j)
            new_statistics = launch_plotter.LaunchStatistics(new_lists)
            config_dict['bar_filename'] = config_dict['latest_month_bar']
            config_dict['bar_title'] = config_dict['month_title']
            launch_plotter.plot_launch_bar_by_country(launch_statistics=new_statistics,
                                                      config_dict=config_dict)
