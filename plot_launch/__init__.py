#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's commandline entry point functionality.
"""
# Import built-in modules
import os
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
    launch_info_lists = launch_info.get_launch_info_from_files(constants.DATA_PATH)
    launch_statistics = launch_plotter.LaunchStatistics(launch_info_lists)
    launch_plotter.plot_launch_times_by_country(launch_statistics=launch_statistics,
                                                launch_info_lists=launch_info_lists)
    launch_energy_figure_name = \
        os.path.join(constants.HERE,
                     str(constants.CURRENT_TIME.year) + '_launch_energy_by_countries_step.png')
    launch_plotter.plot_launch_energy_by_country(launch_statistics=launch_statistics,
                                                 launch_info_lists=launch_info_lists,
                                                 figure_filename=launch_energy_figure_name)
