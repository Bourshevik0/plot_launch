#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines plot_launch's entry point.
"""
# Import built-in modules
# pylint: disable=no-member, protected-access
import sys

if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    # Reference: https://github.com/rg3/youtube-dl/blob/master/youtube_dl/__main__.py
    import os.path
    PATH = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(PATH)))

# Any changes to the path and your own modules

if __name__ == "__main__":
    # On Windows calling this function is necessary.
    # if sys.platform.startswith('win'):
    #     multiprocessing.freeze_support()
    import plot_launch
    plot_launch.main()
