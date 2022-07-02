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

HEX_COLOR_LIST = [
    # reference https://cran.r-project.org/web/packages/khroma/vignettes/tol.html#muted
    '#CC6677',  # rose
    '#332288',  # indigo
    '#DDCC77',  # sand
    '#117733',  # green
    '#88CCEE',  # cyan
    '#882255',  # wine
    '#44AA99',  # teal
    '#999933',  # olive
    '#AA4499',  # purple
    '#808080'   # grey
]

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
    '萨迪什·达万航天中心一号工位': '安得拉邦内洛尔县',
    '拜科努尔31/6号工位': '克孜勒奥尔达州拜科努尔市',
    '拜科努尔200/39号工位': '克孜勒奥尔达州拜科努尔市',
    '普列谢茨克35/1号工位': '阿尔汉格尔斯克州米尔内市',
    '普列谢茨克43/4号工位': '阿尔汉格尔斯克州米尔内市',
    '科迪亚克PSCA LP-3B': '阿拉斯加州科迪亚克岛',
    '中大西洋区太空空港(MARS)LP-0A': '弗吉尼亚州阿可麦克县',
    '范登堡太空军基地SLC-3E': '加利福尼亚州圣巴巴拉县',
    '范登堡太空军基地SLC-4E': '加利福尼亚州圣巴巴拉县',
    '卡角太空军基地SLC-40': '佛罗里达州布里瓦德县',
    '卡角太空军基地SLC-41': '佛罗里达州布里瓦德县',
    '卡角太空军基地SLC-46': '佛罗里达州布里瓦德县',
    '肯尼迪航天中心LC-39A': '佛罗里达州布里瓦德县',
    '酒泉卫星发射中心': '内蒙古阿拉善额济纳东风镇',
    '酒泉卫星发射中心9401工位': '内蒙古阿拉善额济纳东风镇',
    '酒泉卫星发射中心921工位': '内蒙古阿拉善额济纳东风镇',
    '西昌卫星发射中心2号工位': '四川凉山冕宁县泽远乡',
    '西昌卫星发射中心3号工位': '四川凉山冕宁县泽远乡',
    '文昌航天发射场2号工位(LC-201)': '海南省文昌市龙楼镇',
    '文昌航天发射场1号工位(LC-101)': '海南省文昌市龙楼镇',
    '太原卫星发射中心9号工位': '山西省忻州市岢岚县',
    '太原卫星发射中心16号工位': '山西省忻州市岢岚县',
    '太原卫星发射中心9A工位': '山西省忻州市岢岚县',  
    '火箭实验室LC-1A(新西兰玛希亚)': '霍克湾大区怀罗瓦地区',
    '火箭实验室LC-1B(新西兰玛希亚)': '霍克湾大区怀罗瓦地区',
    '沙赫鲁德导弹测试场': '塞姆南省沙赫鲁德县'
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

ORBIT_KEY_CANDIDATE = ('轨道', '轨道(末级)', '初始轨道', '实际轨道', '预期轨道', '运营轨道')
DATA_KEY = ['编号',
            '火箭制造方',
            '时间',
            '位置',
            '任务名',
            '冠名',
            '组名',
            '任务代号',
            '飞行编号',
            '发射提供方',
            '发射与运营',
            '发射与载荷',
            '载荷研制方',
            '载荷运营方',
            '服务提供方',
            '客户',
            '载荷信息',
            '主载荷信息',
            '搭车载荷信息',
            '载荷质量',
            '载具',
            '预期轨道',
            '初始轨道(预测)',
            '轨道',
            '轨道(末级)',
            '实际轨道',
            '运营轨道',
            '结果',
            '结果(发射与回收)',
            '回收船',
            '失败原因',
            '备注']

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
