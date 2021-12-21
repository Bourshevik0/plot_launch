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
from plot_launch import constants


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
        # Common data of launches
        self.id = []
        self.launcher_man_country = []
        self.time = []
        self.location = []
        self.mission_name = []
        self.flight_num = []
        self.launch_provider = []
        self.payload_provider = []
        self.payload_operator = []
        self.payload_developer = []
        self.payload_info = []
        self.payload_mass = []
        self.launcher = []
        self.orbit = []
        self.orbital_energy = []
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
                      raw_data,
                      config_dict):
        """
        Initialize a LaunchInfoLists object from raw_data.
        :param raw_data: A raw format of data of launches which separated by '\n\n' which is a
        string.
        :param config_dict: A dictionary to filter out unwanted data files.
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

            time_str = data_dict.get('时间')
            time_str_part = time_str[:time_str.find('(')]
            time_obj = from_str_to_datetime(time_str_part)
            if '+' in data_dict.get('时间'):
                time_obj = time_obj - datetime.timedelta(hours=8)
            if time_obj < config_dict['time_filter'][0] or time_obj > config_dict['time_filter'][1]:
                continue
            launch_info_lists.time.append(time_obj)
            launch_info_lists.append_dict(data_dict)
        return launch_info_lists

    def append_dict(self,
                    data_dict):
        """
        Append a LaunchInfoLists object from a data_dict.
        :param data_dict: A dictionary of raw data from a single launch.
        :return None:
        """
        # common statistics of launches
        self.id.append(data_dict.get('编号'))
        self.launcher_man_country.append(data_dict.get('火箭制造方'))

        self.location.append(data_dict.get('位置'))
        self.mission_name.append(data_dict.get('任务名'))
        self.flight_num.append(data_dict.get('飞行编号'))

        result = data_dict.get('发射提供方')
        if not result:
            self.launch_provider.append(data_dict.get('发射与载荷'))
        else:
            self.launch_provider.append(result)

        result = data_dict.get('载荷运营方')
        if not result:
            self.payload_operator.append(data_dict.get('发射与载荷'))
        else:
            self.payload_operator.append(result)

        result = data_dict.get('载荷研制方')
        if not result:
            self.payload_developer.append(self.payload_operator[-1])
        else:
            self.payload_developer.append(result)

        result = data_dict.get('载荷信息')
        if not result:
            result = '{part1}；{part2}'.format(
                part1=data_dict.get('主载荷信息'),
                part2=data_dict.get('搭车载荷信息'))
        self.payload_info.append(result)

        result = data_dict.get('载荷质量')
        if not result:
            result = list(map(float, re.findall(r'(\d+\.?\d+|\d+)吨', self.payload_info[-1])))
            if not result:
                result = '0吨'
            else:
                result = '{value}吨'.format(value=result[0])
        self.payload_mass.append(result)

        self.launcher.append(data_dict.get('载具'))

        for key in constants.ORBIT_KEY_CANDIDATE:
            result = data_dict.get(key)
            if result:
                break
        self.orbit.append(result)

        result = data_dict.get('结果')
        if not result:
            result = data_dict.get('结果(发射与回收)')
        if result == '成功':
            self.launch_result.append(True)
            self.orbital_energy.append(get_orbital_energy(self.orbit[-1],
                                                          self.payload_mass[-1]))
            if self.orbital_energy[-1] == 0:
                print('发射时间：{time}'.format(time=self.time[-1]))
                print('载荷信息：{info}'.format(info=self.payload_info[-1]))
                print('轨道额外能量：{content}\n'.format(content=self.orbital_energy[-1]))
        else:
            self.launch_result.append(False)
            self.orbital_energy.append(0.0)

        self.remarks.append(data_dict.get('备注'))

        # special statistics of launches
        self.recovery_result.append(data_dict.get('结果(发射与回收)'))
        self.recovery_ship.append(data_dict.get('回收船'))


def get_orbital_energy(orbit_str,
                       mass_str):
    """
    Get potential extra orbital energy from payload orbit and payload mass of the index number.
    :param orbit_str: A string contains basic orbit data.
    :param mass_str: A string contains basic mass data.
    :return result: The potential extra orbital energy from payload(s).
    """
    orbit_str_list = orbit_str.split('；')
    mass_list = list(map(float, re.findall(r'(\d+\.?\d+|\d+)吨', mass_str)))

    i = 0
    result = 0.0
    for orbit_str in orbit_str_list:
        if 'C₃' in orbit_str:
            specific_orbital_energy = \
                list(map(float, re.findall(r'(\d+\.?\d+|\d+)km', orbit_str)))[0]
        elif '半长轴' in orbit_str:
            semi_major_axis = \
                list(map(float, re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *\+?\ *[0-9]+)?',
                                           orbit_str)))[0] * 1000.0
            specific_orbital_energy = 0.0 - constants.GEO_CONSTANT / (2.0 * semi_major_axis)
        else:
            orbit_str = orbit_str.replace('km', '')
            apsis_list = list(map(float, re.findall(r'\d+\.?\d+|\d+', orbit_str)))
            semi_major_axis = (apsis_list[0] + apsis_list[1]) / 2.0 + constants.NOMINAL_EARTH_RADIUS
            specific_orbital_energy = 0.0 - constants.GEO_CONSTANT / (2.0 * semi_major_axis)
        result = (specific_orbital_energy - constants.EARTH_SURFACE_POTENTIAL_ENERGY) * \
                 mass_list[i] / 1E4 + result
        # * 1000 / unit 10MJ
        i = i + 1
    return round(result)


def get_launch_info_from_files(data_dir,
                               config_dict=None):
    """
    Defines codes to get launchinfo from multiple raw data files.
    :param config_dict: A dictionary to filter out unwanted data files.
    :param data_dir: A directory path contains several raw data files to read.
    :return LaunchInfoLists: An initialized LaunchInfoLists object.
    """
    dir_data = []
    for filename in os.listdir(data_dir):
        if config_dict['filename_filter'] not in filename or not filename.endswith('txt'):
            continue
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
    return LaunchInfoLists.from_raw_data(raw_data=raw_data, config_dict=config_dict)


def from_str_to_datetime(datetime_str,
                         custom_format=None):
    """
    Get datetime object from a string depending on a custom format.
    :param datetime_str: A string of datetime.
    :param custom_format: A custom format of datetime.
    :return:
    """
    if not custom_format:
        if datetime_str.count(':') < 2:
            time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        elif '.' not in datetime_str:
            time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        else:
            time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    else:
        time_obj = datetime.datetime.strptime(datetime_str, custom_format)

    return time_obj


def prcs_config_dict(config_dict):
    """
    Process config dictionary.
    :param config_dict: A dictionary to filter out unwanted data files.
    :return config_dict: Same dictionary as the input but processed.
    """
    config_dict['time_filter'] = [from_str_to_datetime(config_dict['time_filter'][0],
                                                       config_dict['time_filter_format']),
                                  from_str_to_datetime(config_dict['time_filter'][1],
                                                       config_dict['time_filter_format'])]
    if config_dict['time_filter'][1] > constants.CURRENT_TIME:
        config_dict['time_filter'][1] = constants.CURRENT_TIME
    return config_dict


# if __name__ == '__main__':
#     here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#     os.chdir(here)
#     data_dir = os.path.join(here, 'launchinfo')
#     get_launch_info_from_files(data_dir)
