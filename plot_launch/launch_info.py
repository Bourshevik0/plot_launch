#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines launch_info classes and methods used by plot_launch.
"""

# Import built-in modules
import datetime
import re
import os

# Import third-party modules


# Any changes to the path and your own modules

class PayloadInfoLists:  # pylint: disable=too-few-public-methods
    """
    Class for the data of orbital payloads of an orbital launch.
    """
    def __init__(self):
        self.payload_info = []
        self.payload_man = []
        self.payload_operator = []
        self.payload_mass = []
        self.payload_type = []

    def append_dict(self,
                    data_dict):
        """
        :param data_dict:  A dictionary of raw data from a single launch.
        :return: None
        """
        self.payload_operator.append(data_dict.get('载荷运营方'))
        self.payload_man.append(data_dict.get('载荷研制方'))
        self.payload_info.append(data_dict.get('载荷信息'))

        mass_list = list(map(float, re.findall(r'\d+\.?\d+|\d+吨', self.payload_info[-1])))
        if mass_list:
            self.payload_mass.append(mass_list[0])
        else:
            self.payload_mass.append(None)


class LaunchInfoLists:  # pylint: disable=too-few-public-methods
    """
    Class for the data of orbital launches.
    """
    def __init__(self):
        # common data of launches
        self.id = []
        self.launcher_man_country = []
        self.time = []
        self.location = []
        self.mission_name = []
        self.flight_num = []
        self.launch_provider = []
        self.payload_info = []
        self.launcher = []
        self.orbit = []
        self.launch_result = []
        self.remarks = []

        # special data of launches
        self.recovery_result = []
        self.recovery_ship = []

        # data sources
        self.citation_seq_tuple_list = []
        self.sources = []

    @classmethod
    def from_raw_data(cls,
                      raw_data):
        """
        :param raw_data: A raw format of data of launches which separated by '\n\n' which is a
        string.
        :return launch_info_lists: An initialized LaunchInfoLists object.
        """
        launch_info_lists = cls()
        raw_list = raw_data.split('\n\n')
        compiler = re.compile(r'\[.*?]')
        for item in raw_list:
            i = item.find('\n')
            j = item[:i].find('：')
            data_dict = {item[:j]: item[j + 1:i]}
            last_key = item[:j]
            the_rest = item
            not_last = True
            while not_last:
                the_rest = the_rest[i + 1:]
                i = the_rest.find('\n')
                if i < 0:
                    i = len(the_rest)
                    not_last = False
                j = the_rest[:i].find('：')
                if '[' in the_rest[j + 1:i]:
                    text = "".join(compiler.split(the_rest[j + 1:i]))
                else:
                    text = the_rest[j + 1:i]
                if j > 0:
                    data_dict[the_rest[:j]] = text
                    last_key = the_rest[:j]
                else:
                    data_dict[last_key] = data_dict[last_key] + text
            launch_info_lists.append_dict(data_dict)
        return launch_info_lists

    def append_dict(self,
                    data_dict):
        """
        :param data_dict: A dictionary of raw data from a single launch.
        :return: None
        """
        # common statistics of launches
        self.id.append(data_dict.get('编号'))
        self.launcher_man_country.append(data_dict.get('火箭制造方'))

        time_str = data_dict.get('时间')
        time_str_part = time_str[:time_str.find('(')]
        if time_str_part.count(':') < 2:
            time_obj = datetime.datetime.strptime(time_str_part, '%Y-%m-%d %H:%M')
        elif '.' not in time_str_part:
            time_obj = datetime.datetime.strptime(time_str_part, '%Y-%m-%d %H:%M:%S')
        else:
            time_obj = datetime.datetime.strptime(time_str_part, '%Y-%m-%d %H:%M:%S.%f')

        if '+' not in time_str:
            self.time.append(time_obj)
        else:
            self.time.append(time_obj - datetime.timedelta(hours=8))

        self.location.append(data_dict.get('位置'))
        self.mission_name.append(data_dict.get('任务名'))
        self.flight_num.append(data_dict.get('飞行编号'))
        self.launch_provider.append(data_dict.get('发射提供方'))
        self.payload_info.append(data_dict.get('载荷信息'))
        self.launcher.append(data_dict.get('载具'))
        self.orbit.append(data_dict.get('轨道'))

        result = data_dict.get('结果')
        if not result:
            result = data_dict.get('结果(发射与回收)')
        if result == '成功':
            self.launch_result.append(True)
        else:
            self.launch_result.append(False)

        self.remarks.append(data_dict.get('备注'))

        # special statistics of launches
        self.recovery_result.append(data_dict.get('结果(发射与回收)'))
        self.recovery_ship.append(data_dict.get('回收船'))


def get_launch_info_from_files(data_dir):
    """
    Defines code to get launchinfo from multiple raw data files.
    :param data_dir: A directory path contains several raw data files to read.
    :return LaunchInfoLists: An initialized LaunchInfoLists object.
    """
    dir_data = []
    for filename in os.listdir(data_dir):
        abs_path = os.path.join(data_dir, filename)
        with open(abs_path, encoding='utf-8') as data_file:
            raw_data = data_file.read()
            index = 0
            raw_list = raw_data.split('\n\n')
            for item in raw_list:
                i = item.find('\n')
                j = item[:i].find('：')
                if j < 0:
                    break
                index = index + 1
            dir_data.extend(raw_list[:index])
    raw_data = '\n\n'.join(dir_data)
    return LaunchInfoLists.from_raw_data(raw_data=raw_data)


# if __name__ == "__main__":
#     here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#     os.chdir(here)
#     data_dir = os.path.join(here, 'launchinfo')
#     get_launch_info_from_files(data_dir)
