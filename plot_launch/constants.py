#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines constants used by plot_launch.
"""

# Import built-in modules
import datetime
import os

# Import third-party modules


# Any changes to the path and your own modules

HEX_COLOR_DICT = {
    # reference https://cran.r-project.org/web/packages/khroma/vignettes/tol.html#muted
    '中国': '#CC6677',  # rose
    '美国': '#332288',  # indigo
    '印度': '#DDCC77',  # sand
    '伊朗': '#117733',  # green
    '俄罗斯': '#88CCEE',  # cyan
    '韩国': '#882255',  # wine
    '欧洲': '#44AA99',  # teal
    '日本': '#808080'  # grey
}

RAW_CODE_DICT = {
    # reference https://en.wikipedia.org/wiki/ISO_3166-1
    '中国': 'CN',
    '美国': 'US',
    '印度': 'IN',
    '伊朗': 'IR',
    '俄罗斯': 'RU',
    '韩国': 'KR',
    '欧洲': 'EU',
    '日本': 'JP'
}

CURRENT_TIME = datetime.datetime.utcnow()

HERE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
FONT_NAME = 'font/sarasa-gothic-sc-semibold.ttf'
FONT_PATH = os.path.join(HERE, FONT_NAME)
DEFAULT_DATA_DIR = 'launchinfo'
DEFAULT_DATA_FILTER = str(CURRENT_TIME.year)
DATA_PATH = os.path.join(HERE, DEFAULT_DATA_DIR)
LICENSE_IMG_NAME = 'img/CC BY-NC-SA 4.0.png'
LICENSE_IMG_PATH = os.path.join(HERE, LICENSE_IMG_NAME)

ORBIT_KEY_CANDIDATE = ('轨道', '轨道(末级)', '预期轨道')

DEFAULT_DPI = 120
DEFAULT_FIGSIZE = (16, 9)
DEFAULT_FONTSIZE = 14
DEFAULT_AXLINE_COLOR = '#80808080'

GEO_CONSTANT = 3.9860044E14
# reference https://en.wikipedia.org/wiki/Standard_gravitational_parameter#Geocentric_gravitational_constant

EARTH_SURFACE_POTENTIAL_ENERGY = 0.0 - 6.26E7
# reference https://en.wikipedia.org/wiki/Specific_orbital_energy#Examples

NOMINAL_EARTH_RADIUS = 6.378145E6
# reference https://en.wikipedia.org/wiki/Earth_radius#Nominal_radius
# https://www.zarya.info/Diaries/Launches/Launches.php?year=2021