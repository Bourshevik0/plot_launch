#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's commandline entry point functionality.
"""
# Import built-in modules
import os
import sys
import json
import datetime

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
            config_dict = launch_info.prcs_config_dict(config_dict)
    else:
        config_dict = {
            'time_filter': [
                datetime.datetime(year=constants.CURRENT_TIME.year,
                                  month=1,
                                  day=1),
                constants.CURRENT_TIME],
            'filename_filter': str(constants.CURRENT_TIME.year),
            'launch_times_figure_title': '{year}年世界航天入轨发射次数统计'.format(
                year=constants.CURRENT_TIME.year),
            'launch_times_figure_filename':
                os.path.join(constants.HERE, '{year}_launch_time_by_countries_step.png'.format(
                    year=constants.CURRENT_TIME.year)),
            'energy_figure_title': '{year}年世界航天入轨发射轨道能量统计'.format(
                year=constants.CURRENT_TIME.year),
            'energy_figure_filename':
                os.path.join(constants.HERE, '{year}_launch_energy_by_countries_step.png'.format(
                    year=constants.CURRENT_TIME.year)),
            's_energy_figure_title': '{year}年世界航天入轨发射轨道比能量统计'.format(
                year=constants.CURRENT_TIME.year),
            's_energy_figure_filename':
                os.path.join(constants.HERE,
                             '{year}_launch_s_energy_by_countries_step.png'.format(
                                 year=constants.CURRENT_TIME.year)),
        }

    launch_info_lists = launch_info.get_launch_info_from_files(constants.DATA_PATH,
                                                               config_dict=config_dict)
    launch_statistics = launch_plotter.LaunchStatistics(launch_info_lists)

    if 'launch_times_figure_filename' in config_dict:
        launch_plotter.plot_launch_times_by_country(launch_statistics=launch_statistics,
                                                    launch_info_lists=launch_info_lists,
                                                    config_dict=config_dict)
    if 'energy_figure_filename' in config_dict:
        launch_plotter.plot_launch_energy_by_country(launch_statistics=launch_statistics,
                                                     launch_info_lists=launch_info_lists,
                                                     config_dict=config_dict)
    if 's_energy_figure_title' in config_dict:
        launch_plotter.plot_launch_s_energy_by_country(launch_statistics=launch_statistics,
                                                       launch_info_lists=launch_info_lists,
                                                       config_dict=config_dict)
