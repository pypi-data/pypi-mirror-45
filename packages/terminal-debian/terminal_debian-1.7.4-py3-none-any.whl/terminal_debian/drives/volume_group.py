#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Tuple, Union

from terminal_debian.drives import drive
from terminal_debian.drives import logical_volume as lv
from terminal_debian.drives.common import Properties, Side, BaseDevice, BaseDevices
from terminal_debian.style import Backgrounds, TextColors


class VolumeGroup(BaseDevice):
    PROPERTIES = dict(BaseDevice.PROPERTIES)
    PROPERTIES.update({
        Properties.NAME: ('VOLUME GROUP', 'name', Side.LEFT),
        Properties.LOGICAL_VOLUMES: ('LOGICAL VOLUMES', 'logical_volumes', Side.LEFT),
        Properties.PHYSICAL_VOLUMES: ('PHYSICAL VOLUMES', 'physical_volumes', Side.LEFT),
    })

    def __init__(self, volume_group: str):
        self.name = volume_group
        self.size, self.used, self.free, self.usage_percent, self.usage_graph = self.get_usages(self.name)
        self.physical_volumes = drive.Drive.get_physical_volumes(volume_group=self.name)
        self.logical_volumes = lv.LogicalVolume.get_logical_volumes(volume_group=self.name)
        self.print_cols = [Properties.NAME, Properties.LOGICAL_VOLUMES, Properties.PHYSICAL_VOLUMES, Properties.SIZE, Properties.USED, Properties.FREE, Properties.USAGE_PERCENT,
                           Properties.USAGE_GRAPH]

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.name != other.name:
            return False
        return True

    @staticmethod
    def volume_group_exists(volume_group: str):
        res = True
        command = ['vgs', volume_group]
        try:
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except CalledProcessError:
            res = False
        return res

    @classmethod
    def assert_exists(cls, volume_group: str):
        if not cls.volume_group_exists(volume_group):
            raise ValueError('Volume group "{0}" not found'.format(volume_group))

    @classmethod
    def get_usages(cls, volume_group: str) -> Tuple[int, int, int, int, str]:
        cls.assert_exists(volume_group)
        command = ['vgs', '--noheadings', '--units', 'b', '--rows', '--options', 'SIZE,FREE', volume_group]
        vgs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip().split('\n')
        vgs = [int(data.strip()[:-1]) for data in vgs]
        size = vgs[0]
        free = vgs[1]
        used = size - free
        usage_percent = round((used * 100.0) / size)
        usage_graph = cls.draw_usage_graph(usage_percent, Backgrounds.LIGHT_CYAN, brackets_color=TextColors.DARK_GRAY, hashtag_color=TextColors.LIGHT_RED, point_color=TextColors.BLUE)
        return size, used, free, usage_percent, usage_graph

    @classmethod
    def get_size(cls, volume_group: str) -> int:
        return cls.get_usages(volume_group)[0]

    @classmethod
    def get_used(cls, volume_group: str) -> int:
        return cls.get_usages(volume_group)[1]

    @classmethod
    def get_free(cls, volume_group: str) -> int:
        return cls.get_usages(volume_group)[2]

    @classmethod
    def get_usage_percent(cls, volume_group: str) -> int:
        return cls.get_usages(volume_group)[3]

    @classmethod
    def get_usage_graph(cls, volume_group: str) -> str:
        return cls.get_usages(volume_group)[4]

    @classmethod
    def get_volume_group(cls, logical_volume: Union[str, Path] = None, physical_volume: Union[str, Path] = None) -> str:
        if logical_volume is not None:
            logical_volume = lv.LogicalVolume.get_real_path(path=logical_volume)
            return Path(logical_volume).parent.name
        elif physical_volume is not None:
            physical_volume = drive.Drive.get_real_path(physical_volume)
            drive.Drive.assert_physical_volume_exists(physical_volume)
            command = ['pvs', '--noheadings', '--options', 'VG_NAME', physical_volume]
            pvs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
            pvs = None if not pvs else pvs
            return pvs
        else:
            raise ValueError('You must provide either a physical volume or a logical volume')

    @staticmethod
    def get_volume_groups() -> Tuple[str]:
        command = ['vgs', '--noheadings', '--options', 'VG_NAME']
        volume_groups = ()
        vgs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        if vgs:
            vgs = vgs.split('\n')
            volume_groups = [line.strip() for line in vgs]
        volume_groups = None if len(volume_groups) == 0 else tuple(volume_groups)
        return volume_groups

    def __repr__(self):
        return self.name


class VolumeGroups(BaseDevices):

    def __init__(self, volume_groups=None):
        if volume_groups is None:
            volume_groups = VolumeGroup.get_volume_groups()
        if volume_groups is None:
            volume_groups = []
        volume_groups = [VolumeGroup(x) for x in volume_groups]
        self.devices = tuple(volume_groups)
        self.device_class = VolumeGroup
        self.print_cols = [Properties.NAME, Properties.LOGICAL_VOLUMES, Properties.PHYSICAL_VOLUMES, Properties.SIZE, Properties.USED, Properties.FREE, Properties.USAGE_PERCENT,
                           Properties.USAGE_GRAPH]
