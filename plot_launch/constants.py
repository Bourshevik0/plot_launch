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

STATUS_COLOR_DICT = {
    # reference https://cran.r-project.org/web/packages/khroma/vignettes/tol.html#vibrant
    '成功': '#0077BB',
    '失败': '#CC3311'
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

LOCATION_DICT = {
    '普列谢茨克35/1号工位': '阿尔汉格尔斯克州米尔内市',
    '普列谢茨克43/4号工位': '阿尔汉格尔斯克州米尔内市',
    '范登堡太空军基地SLC-3E': '加利福尼亚州圣巴巴拉县',
    '范登堡太空军基地SLC-4E': '加利福尼亚州圣巴巴拉县',
    '卡角太空军基地SLC-40': '佛罗里达州布里瓦德县',
    '卡角太空军基地SLC-41': '佛罗里达州布里瓦德县',
    '卡角太空军基地SLC-46': '佛罗里达州布里瓦德县',
    '肯尼迪航天中心LC-39A': '佛罗里达州布里瓦德县',
    '酒泉卫星发射中心': '内蒙古阿拉善额济纳东风镇',
    '酒泉卫星发射中心9401工位': '内蒙古阿拉善额济纳东风镇',
    '酒泉卫星发射中心921工位': '内蒙古阿拉善额济纳东风镇'
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
DEFAULT_STYLES_NAME = 'font/default_styles.ass'
DEFAULT_STYLES_PATH = os.path.join(HERE, DEFAULT_STYLES_NAME)

ORBIT_KEY_CANDIDATE = ('轨道', '轨道(末级)', '实际轨道', '预期轨道')

DEFAULT_DPI = 120
DEFAULT_FIGSIZE = (16, 9)
DEFAULT_FONTSIZE = 14
DEFAULT_AXLINE_COLOR = '#80808080'

GEO_CONSTANT = 3.9860044E14
# reference https://en.wikipedia.org/wiki/Standard_gravitational_parameter
# #Geocentric_gravitational_constant

EARTH_SURFACE_POTENTIAL_ENERGY = - 6.25E7
# reference https://en.wikipedia.org/wiki/Specific_orbital_energy
# GEO_CONSTANT / NOMINAL_EARTH_RADIUS

NOMINAL_EARTH_RADIUS = 6.378145E6
# reference https://en.wikipedia.org/wiki/Earth_radius#Nominal_radius
# https://www.zarya.info/Diaries/Launches/Launches.php?year=2021
