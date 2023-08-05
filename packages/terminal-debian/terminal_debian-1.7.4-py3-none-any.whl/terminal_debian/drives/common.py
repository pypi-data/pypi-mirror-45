#!/usr/bin/env python3
# encoding:utf-8


from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from terminal_debian.style import Style, Backgrounds, TextColors


class Side(Enum):
    LEFT = 0
    RIGHT = 1


class StorageUnits(Enum):
    B = 1
    KB = 2
    MB = 3
    GB = 4
    TB = 5
    PB = 6
    EB = 7

    @classmethod
    def get_proper_unit(cls, size_bytes):
        units = {
            0: cls.B,
            1: cls.KB,
            2: cls.MB,
            3: cls.GB,
            4: cls.TB,
            5: cls.PB,
            6: cls.EB,
        }
        count = 0
        old_size = size_bytes
        while count < 6:
            new_size = old_size / 1024.0
            if new_size < 1:
                break
            old_size = new_size
            count += 1
        unit = units[count]
        res = str(round(old_size, 2)) + ' ' + unit.name
        return res


class Properties(Enum):
    FREE = 1
    FSTYPE = 2
    LABEL = 3
    LOGICAL_VOLUMES = 4
    MOUNTPOINT = 5
    NAME = 6
    ORIGIN = 7
    PATH = 8
    PHYSICAL_VOLUMES = 9
    SIZE = 10
    USAGE_GRAPH = 11
    USAGE_PERCENT = 12
    USED = 13
    UUID = 14
    VOLUME_GROUP = 15


class BaseDevice(ABC):
    GRAPH_SIZE = 30

    PROPERTIES = {
        Properties.FREE: ('FREE', 'free_str', Side.RIGHT),
        Properties.NAME: ('NAME', 'name', Side.LEFT),
        Properties.SIZE: ('SIZE', 'size_str', Side.RIGHT),
        Properties.USAGE_GRAPH: ('USAGE GRAPH', 'usage_graph', Side.LEFT),
        Properties.USAGE_PERCENT: ('USAGE%', 'usage_percent_str', Side.RIGHT),
        Properties.USED: ('USED', 'used_str', Side.RIGHT),
    }

    @abstractmethod
    def __init__(self):
        self.name = None
        self.size = None
        self.free = None
        self.used = None
        self.usage_percent = None
        self.usage_graph = None
        self.print_cols = None

    @property
    def size_str(self) -> str:
        if self.size is None:
            return None
        return StorageUnits.get_proper_unit(self.size)

    @property
    def used_str(self) -> str:
        if self.used is None:
            return None
        return StorageUnits.get_proper_unit(self.used)

    @property
    def free_str(self) -> str:
        if self.free is None:
            return None
        return StorageUnits.get_proper_unit(self.free)

    @property
    def usage_percent_str(self) -> str:
        if self.usage_percent is None:
            return None
        return str(self.usage_percent) + '%'

    @classmethod
    def draw_usage_graph(cls, usage_percent, background_color=Backgrounds.DEFAULT, brackets_color=TextColors.DEFAULT, hashtag_color=TextColors.DEFAULT, point_color=TextColors.DEFAULT) -> str:
        usage_graph = Style.apply('[', background_color, brackets_color)
        usage_rounded = round((0.01 * usage_percent * cls.GRAPH_SIZE))
        for i in range(cls.GRAPH_SIZE):
            if i < usage_rounded:
                usage_graph += Style.apply('#', background_color, hashtag_color)
            else:
                usage_graph += Style.apply('.', background_color, point_color)
        usage_graph += Style.apply(']', background_color, brackets_color)
        return usage_graph

    def _aligned_col_str(self, column):
        header = self.PROPERTIES[column][0]
        attribute = self.__getattribute__(self.PROPERTIES[column][1])
        attribute = attribute if attribute is not None else ''
        side = self.PROPERTIES[column][2]
        if column is Properties.LOGICAL_VOLUMES:
            attribute = [Path(attr).name for attr in attribute]
        if column is Properties.PHYSICAL_VOLUMES or column is Properties.LOGICAL_VOLUMES:
            attribute = list(attribute)
            attribute = str(attribute)[1:-1].replace("'", '')
        len_header = len(header)
        len_attribute = len(attribute)
        if column is Properties.USAGE_GRAPH:
            len_attribute = min(self.GRAPH_SIZE + 2, len(attribute))
        maximum = max(len_header, len_attribute)
        if side == Side.LEFT:
            header_str = header + ' ' * (maximum - len_header)
            attribute_str = attribute + ' ' * (maximum - len_attribute)
        elif side == Side.RIGHT:
            header_str = ' ' * (maximum - len_header) + header
            attribute_str = ' ' * (maximum - len_attribute) + attribute
        res = [header_str, attribute_str]
        res = '\n'.join(res)
        return res

    def __str__(self):
        header = ''
        attribute = ''
        for column in self.print_cols:
            aligned_col = self._aligned_col_str(column).split('\n')
            header += 2 * ' ' + aligned_col[0]
            attribute += 2 * ' ' + aligned_col[1]
        return header + '\n' + attribute


class BaseDevices(ABC):

    @abstractmethod
    def __init__(self):
        self.devices = None
        self.print_cols = None
        self.device_class = None

    def _aligned_col_str(self, column):
        header = self.device_class.PROPERTIES[column][0]
        attribute = self.device_class.PROPERTIES[column][1]
        side = self.device_class.PROPERTIES[column][2]
        attr_list = [x.__getattribute__(attribute) for x in self.devices]
        attr_list = [attr if attr is not None else '' for attr in attr_list]
        if column is Properties.LOGICAL_VOLUMES:
            attr_list = [[Path(x).name for x in attr] for attr in attr_list]
        if column is Properties.LOGICAL_VOLUMES or column is Properties.PHYSICAL_VOLUMES:
            attr_list = [list(x) for x in attr_list]
            attr_list = [str(x)[1:-1].replace("'", '') for x in attr_list]
        attr_list.insert(0, header)
        attr_lenghts = [len(x) for x in attr_list]
        if column is Properties.USAGE_GRAPH:
            attr_lenghts = [min(self.device_class.GRAPH_SIZE + 2, len(x)) for x in attr_list]
            attr_lenghts[0] = len(header)
        maximum = max(attr_lenghts)
        for i in range(len(attr_list)):
            if side == Side.LEFT:
                attr_list[i] += ' ' * (maximum - attr_lenghts[i])
            elif side == Side.RIGHT:
                attr_list[i] = ' ' * (maximum - attr_lenghts[i]) + attr_list[i]
        res = '\n'.join(attr_list)
        return res

    def __str__(self):
        res = ['' for i in range(len(self.devices) + 1)]
        for column in self.print_cols:
            string = self._aligned_col_str(column).split('\n')
            res = [res[i] + 2 * ' ' + string[i] for i in range(len(res))]
        return '\n'.join(res)
