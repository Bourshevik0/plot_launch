#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's commandline entry point functionality.
"""
# Import built-in modules

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
    launch_plotter.plot_launch_statistics(launch_statistics=launch_statistics,
                                          launch_info_lists=launch_info_lists)
