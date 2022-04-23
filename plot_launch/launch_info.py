#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Defines launch_info classes and methods used by plot_launch.
"""

# Import built-in modules
import datetime
import re
import os
from calendar import monthrange
import math

# Import third-party modules
import matplotlib
import matplotlib.font_manager as fm
import pysubs2

# Any changes to the path and your own modules
from plot_launch import constants


# class PayloadInfoLists:  # pylint: disable=too-few-public-methods
#     """
#     Class for the data of orbital payloads of an orbital launch.
#     """
#
#     def __init__(self):
#         self.payload_info = []
#         self.payload_man = []
#         self.payload_operator = []
#         self.payload_mass = []
#         self.payload_type = []
#
#     def append_dict(self,
#                     data_dict):
#         """
#         :param data_dict:  A dictionary of raw data from a single launch.
#         :return None:
#         """
#         self.payload_operator.append(data_dict.get('载荷运营方'))
#         self.payload_man.append(data_dict.get('载荷研制方'))
#         self.payload_info.append(data_dict.get('载荷信息'))
#
#         mass_list = list(map(float, re.findall(r'\d+\.?\d+|\d+吨', self.payload_info[-1])))
#         if mass_list:
#             self.payload_mass.append(mass_list[0])
#         else:
#             self.payload_mass.append(None)


class LaunchInfoLists:  # pylint: disable=too-few-public-methods
    """
    Class for the data of orbital launches.
    """

    def __init__(self):
        # Common data of launches
        self.identifier = []
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
        self.s_orbital_energy = []
        # specific orbital energy
        self.r_orbital_energy = []
        # relative specific orbital energy
        self.orbital_energy = []
        # total orbital energy
        self.delta_v = []
        # ideal delta velocity to certain orbital
        self.launch_result = []
        self.remarks = []

        # special data of launches
        self.recovery_result = []
        self.recovery_ship = []

        # data sources
        self.data_dicts = []
        # self.citation_seq_tuple_list = []
        # self.sources = []

    def get_slice_from_datetime(self,
                                datetime_start,
                                datetime_end):
        """
        Return a slice based on a datetime range.
        :param datetime_start: A datetime start.
        :param datetime_end: A datetime end.
        :return i, j: 'i' is the start of the slice. 'j' is the end of the slice.
        """
        i = 0
        j = len(self.time)
        k = 0
        length = j
        if self.time[-1] > datetime_start and self.time[0] < datetime_end:
            while k < length:
                if i == 0 and datetime_start < self.time[k]:
                    i = k
                if j == length and datetime_end < self.time[k]:
                    j = k
                    break
                k = k + 1
        else:
            j = 0
        return i, j

    def slice_info(self,
                   new_info_lists,
                   i,
                   j):
        """
        Slice self into a new_info_lists.
        :param new_info_lists: An empty LaunchInfoLists class variable to get the result.
        :param i: A start sequence i.
        :param j: An end sequence j.
        :return None:
        """
        new_info_lists.identifier = self.identifier[i:j]
        new_info_lists.launcher_man_country = self.launcher_man_country[i:j]
        new_info_lists.time = self.time[i:j]
        new_info_lists.location = self.location[i:j]
        new_info_lists.mission_name = self.mission_name[i:j]
        new_info_lists.flight_num = self.flight_num[i:j]
        new_info_lists.launch_provider = self.launch_provider[i:j]
        new_info_lists.payload_provider = self.payload_provider[i:j]
        new_info_lists.payload_operator = self.payload_operator[i:j]
        new_info_lists.payload_developer = self.payload_developer[i:j]
        new_info_lists.payload_info = self.payload_info[i:j]
        new_info_lists.payload_mass = self.payload_mass[i:j]
        new_info_lists.launcher = self.launcher[i:j]
        new_info_lists.orbit = self.orbit[i:j]
        new_info_lists.s_orbital_energy = self.s_orbital_energy[i:j]
        new_info_lists.r_orbital_energy = self.r_orbital_energy[i:j]
        new_info_lists.orbital_energy = self.orbital_energy[i:j]
        new_info_lists.delta_v = self.delta_v[i:j]
        new_info_lists.launch_result = self.launch_result[i:j]
        new_info_lists.remarks = self.remarks[i:j]
        new_info_lists.recovery_result = self.recovery_result[i:j]
        new_info_lists.recovery_ship = self.recovery_ship[i:j]
        new_info_lists.data_dicts = self.data_dicts[i:j]

    @classmethod
    def from_raw_data(cls,
                      raw_data,
                      config_dict):
        """
        Initialize a LaunchInfoLists object from raw_data.
        :param raw_data: A raw format of data of launches which separated by '\n\n' which is a
        string.
        :param config_dict: A dictionary to control the plotting procedure.
        :return launch_info_lists: An initialized LaunchInfoLists object.
        """
        launch_info_lists = cls()
        raw_list = raw_data.split('\n\n')
        compiler = re.compile(r'\[.*?]')
        for item in raw_list:
            i = item.find('\n')
            j = item[:i].find('：')
            data_dict = {item[:j]: item[j + 1:i]}
            key_list = [item[:j]]
            value_list = [item[j + 1:i]]
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
                    key_list.append(the_rest[:j])
                    value_list.append(text)
                else:
                    data_dict[last_key] = data_dict[last_key] + text
                    value_list[-1] = data_dict[last_key]
            time_str = data_dict.get('时间')
            time_str_part = time_str[:time_str.find('(')]
            time_obj = from_str_to_datetime(time_str_part)
            if '+' in data_dict.get('时间'):
                time_obj = time_obj - datetime.timedelta(hours=8)
            if time_obj < config_dict['time_filter'][0] or time_obj > config_dict['time_filter'][1]:
                continue
            launch_info_lists.time.append(time_obj)
            launch_info_lists.append_dict(data_dict)

            result = config_dict.get('to_subs')
            if result:
                launch_info_to_subs(key_list=key_list, value_list=value_list,
                                    output_path=result)
        return launch_info_lists

    def append_dict(self,
                    data_dict):
        """
        Append a LaunchInfoLists object from a data_dict.
        :param data_dict: A dictionary of raw data from a single launch.
        :return None:
        """
        self.data_dicts.append(data_dict)
        # common statistics of launches
        self.identifier.append(data_dict.get('编号'))
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
                result = [0.0]
            else:
                result = [result[0]]
        else:
            result = list(map(float, re.findall(r'(\d+\.?\d+|\d+)吨', result)))
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
            s_orbital_energy_list = get_specific_orbital_energy(self.orbit[-1])
            r_orbital_energy_list = [s_orbital_energy_list[0]
                                     - constants.EARTH_SURFACE_POTENTIAL_ENERGY]
            self.s_orbital_energy.append(s_orbital_energy_list[0])
            self.r_orbital_energy.append(
                round((r_orbital_energy_list[-1]) / 10000))
            for s_orbital_e in s_orbital_energy_list[1:]:
                r_orbital_energy_list.append(
                    s_orbital_e - constants.EARTH_SURFACE_POTENTIAL_ENERGY)
                if self.s_orbital_energy[-1] < s_orbital_e:
                    self.s_orbital_energy[-1] = s_orbital_e
                    self.r_orbital_energy[-1] = round(r_orbital_energy_list[-1] / 10000)
            # unit 10J/kg
            self.orbital_energy.append(get_orbital_energy(r_orbital_energy_list,
                                                          self.payload_mass[-1]))
            self.delta_v.append(round(max(get_delta_v(s_orbital_energy_list))))
            if self.orbital_energy[-1] == 0 or not self.launch_provider[-1]:
                print('发射时间：{time}'.format(time=self.time[-1]))
                print('火箭：{rocket}'.format(rocket=self.launcher[-1]))
                print('发射提供方：{lp}'.format(lp=self.launch_provider[-1]))
                print('载荷信息：{info}'.format(info=self.payload_info[-1]))
                print('轨道能量：{content:.3g}GJ'.format(
                    content=self.orbital_energy[-1] / 100))
                print('轨道比能量：{content:.3g}MJ/kg'.format(
                    content=self.s_orbital_energy[-1] / 100))
                print('轨道相对比能量：{content:.3g}MJ/kg'.format(
                    content=self.r_orbital_energy[-1] / 100))
                print('轨道理想dv：{content:.3g}km/s\n'.format(
                    content=self.delta_v[-1] / 1000))
        else:
            self.launch_result.append(False)
            self.orbital_energy.append(0)
            self.s_orbital_energy.append(0.0)
            self.r_orbital_energy.append(0)
            self.delta_v.append(0)

        self.remarks.append(data_dict.get('备注'))

        # special statistics of launches
        self.recovery_result.append(data_dict.get('结果(发射与回收)'))
        self.recovery_ship.append(data_dict.get('回收船'))


def launch_info_to_subs(key_list,
                        value_list,
                        output_path):
    """
    Write launch_info strings to subtitles files.
    :param key_list: An ordered key list of the data_dict.
    :param value_list: An ordered value list of the data_dict.
    :param output_path: A path for subtitles files to output.
    :return:
    """
    line_list = []
    for i in range(0, len(key_list)):
        line_list.append(rf'{key_list[i]}\h\h\h{{\fn更纱黑体 SC Semibold\fs45}}{value_list[i]}')
    sub_text = r'\N{\fs25}\N{\r}'.join(line_list)
    ssafile = pysubs2.SSAFile.load(path=constants.DEFAULT_STYLES_PATH)
    ssafile.events = [pysubs2.SSAEvent(
        start=0,
        end=5000,
        text=sub_text,
        style=list(ssafile.styles.keys())[0]
    )]
    sub_filename = os.path.join(output_path, value_list[0] + '.ass')
    ssafile.save(path=sub_filename)


def get_specific_orbital_energy(orbit_str):
    """
    Get the specific orbital energy from the orbit_str.
    Reference: https://en.wikipedia.org/wiki/Specific_orbital_energy
    :param orbit_str: A string contains basic orbit data.
    :return result_list: The specific potential extra orbital energy list from payload(s).
    """
    orbit_str_list = orbit_str.split('；')

    i = 0
    result_list = []
    for orbit in orbit_str_list:
        if 'C₃' in orbit:
            specific_orbital_energy = \
                list(map(float, re.findall(r'(\d+\.?\d+|\d+)km', orbit)))[0] / 2 * 1E6
            # Reference: https://en.wikipedia.org/wiki/Characteristic_energy
        elif '半长轴' in orbit:
            semi_major_axis = \
                list(map(float, re.findall(r'-?\ *[0-9]+\.?[0-9]*(?:[Ee]\ *\+?\ *[0-9]+)?',
                                           orbit)))[0] * 1000.0
            specific_orbital_energy = 0.0 - constants.GEO_CONSTANT / (2.0 * semi_major_axis)
        else:
            orbit = orbit.replace('km', '')
            apsis_list = list(map(float, re.findall(r'\d+\.?\d+|\d+', orbit)))
            semi_major_axis = (apsis_list[0] + apsis_list[1]) / 2.0 * 1E3 \
                + constants.NOMINAL_EARTH_RADIUS
            specific_orbital_energy = 0.0 - constants.GEO_CONSTANT / (2.0 * semi_major_axis)
        result_list.append(specific_orbital_energy)
        i = i + 1
    return result_list


def get_delta_v(s_orbital_energy_list):
    """
    Get the ideal delta velocity from the specific orbital energy.
    Reference: https://en.wikipedia.org/wiki/Vis-viva_equation
    https://en.wikipedia.org/wiki/Characteristic_energy
    :param s_orbital_energy_list: A list contains s_orbital_energy.
    :return result_list: The specific potential extra orbital energy list from payload(s).
    """
    result_list = []
    for s_orbital_energy in s_orbital_energy_list:
        c3_energy = s_orbital_energy * 2
        delta_v = math.sqrt(c3_energy - constants.EARTH_SURFACE_POTENTIAL_ENERGY * 2)
        result_list.append(delta_v)
    return result_list


def get_orbital_energy(specific_energy_list,
                       mass_list):
    """
    Get total orbital energy of the payloads of a launch.
    :param specific_energy_list: The specific potential extra orbital energy list from payload(s).
    :param mass_list: A list contains basic mass data.
    :return result: The potential extra orbital energy list from payload(s).
    """
    i = 0
    result = 0.0
    for mass in mass_list:
        result = specific_energy_list[i] * mass / 1E4 + result
        # 1E3(ton to kg) / 1E7(unit 10MJ) = 1E4
    return round(result)


def get_launch_info_from_files(data_dir,
                               config_dict=None):
    """
    Get launchinfo from multiple raw data files.
    :param config_dict: A dictionary to control the plotting procedure.
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
        colon_count = datetime_str.count(':')
        if colon_count == 0:
            if ' ' not in datetime_str.rstrip():
                time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d')
            else:
                time_obj = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H')
        elif colon_count == 1:
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
    :param config_dict: A dictionary to control the plotting procedure.
    :return config_dict: Same dictionary as the input but processed.
    """
    matplotlib.rcParams.update({'font.size': constants.DEFAULT_FONTSIZE})

    if config_dict and 'group_by' in config_dict:
        config_dict['time_filter'] = [from_str_to_datetime(config_dict['time_filter'][0],
                                                           config_dict['time_filter_format']),
                                      from_str_to_datetime(config_dict['time_filter'][1],
                                                           config_dict['time_filter_format'])]
    else:
        config_dict = {
            'time_filter': [
                datetime.datetime(year=constants.CURRENT_TIME.year,
                                  month=1,
                                  day=1),
                constants.CURRENT_TIME],
            'group_by': '火箭制造方',
            'filename_filter': str(constants.CURRENT_TIME.year),
            'step_title': '{year}年世界航天发射次数统计(阶跃图)'.format(
                year=constants.CURRENT_TIME.year),
            'step_filename':
                os.path.join(constants.HERE, '{year}_launch_time_step.png'.format(
                    year=constants.CURRENT_TIME.year)),
            'energy_step_title': '{year}年世界航天发射轨道能量统计(阶跃图)'.format(
                year=constants.CURRENT_TIME.year),
            'energy_step_filename':
                os.path.join(constants.HERE, '{year}_launch_energy_step.png'.format(
                    year=constants.CURRENT_TIME.year)),
            'r_energy_step_title': '{year}年世界航天发射轨道相对比能量统计(阶跃图)'.format(
                year=constants.CURRENT_TIME.year),
            'r_energy_step_filename':
                os.path.join(constants.HERE,
                             '{year}_launch_r_energy_step.png'.format(
                                 year=constants.CURRENT_TIME.year)),
            'delta_v_step_title': '{year}年世界航天发射轨道理想dv统计(阶跃图)'.format(
                year=constants.CURRENT_TIME.year),
            'delta_v_step_filename':
                os.path.join(constants.HERE,
                             '{year}_delta_v_step.png'.format(
                                 year=constants.CURRENT_TIME.year)),
            'mass_step_title': '{year}年世界航天发射质量统计(阶跃图)'.format(
                year=constants.CURRENT_TIME.year),
            'mass_step_filename':
                os.path.join(constants.HERE,
                             '{year}_mass_step.png'.format(
                                 year=constants.CURRENT_TIME.year)),
            'bar_title': '{year}年世界航天发射次数统计(柱状图)'.format(
                year=constants.CURRENT_TIME.year),
            'bar_filename':
                os.path.join(constants.HERE, '{year}_launch_time_bar.png'.format(
                    year=constants.CURRENT_TIME.year)),
            'latest_month_bar':
                os.path.join(constants.HERE,
                             '{year}{month:02d}_launch_time_bar_month.png'.format(
                                 year=constants.CURRENT_TIME.year,
                                 month=constants.CURRENT_TIME.month)),
            'month_title': '{year}年{month}月世界航天发射次数统计(柱状图)'.format(
                year=constants.CURRENT_TIME.year,
                month=constants.CURRENT_TIME.month)
        }
    if config_dict['time_filter'][1] > constants.CURRENT_TIME:
        config_dict['time_filter'][1] = constants.CURRENT_TIME

    if 'latest_month_bar' in config_dict:
        start = datetime.datetime(
            year=config_dict['time_filter'][1].year,
            month=config_dict['time_filter'][1].month,
            day=1)
        config_dict['latest_month_end'] = config_dict['time_filter'][1]
        if start == config_dict['latest_month_end']:
            if config_dict['latest_month_end'].month > 1:
                config_dict['latest_month_start'] = \
                    config_dict['latest_month_end'] - datetime.timedelta(
                        days=monthrange(config_dict['latest_month_end'].year,
                                        config_dict['latest_month_end'].month - 1)[1])
            else:
                config_dict['latest_month_start'] = \
                    config_dict['latest_month_end'] - datetime.timedelta(days=31)
        else:
            config_dict['latest_month_start'] = start

    config_dict['fprop_title'] = fm.FontProperties(fname=constants.FONT_PATH)
    config_dict['fprop'] = fm.FontProperties(fname=constants.FONT_PATH)

    if 'fig_size' in config_dict:
        config_dict['fig_size'] = tuple(config_dict['fig_size'])
    else:
        config_dict['fig_size'] = constants.DEFAULT_FIGSIZE
    if 'dpi' not in config_dict:
        config_dict['dpi'] = constants.DEFAULT_DPI

    return config_dict

# if __name__ == '__main__':
#     here = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
#     os.chdir(here)
#     data_dir = os.path.join(here, 'launchinfo')
#     get_launch_info_from_files(data_dir)
