#!/usr/bin/env python3
# encoding:utf-8


import re
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Union, Tuple

from terminal_debian.drives import drive
from terminal_debian.drives import volume_group as vg
from terminal_debian.drives.common import Properties, Side, BaseDevices
from terminal_debian.style import Backgrounds, TextColors


class LogicalVolume(drive.Drive):
    PROPERTIES = dict(drive.Drive.PROPERTIES)
    PROPERTIES.update({
        Properties.NAME: ('LOGICAL VOLUME', 'name', Side.LEFT),
        Properties.ORIGIN: ('SNAPSHOT', 'origin', Side.LEFT),
        Properties.PHYSICAL_VOLUMES: ('PHYSICAL VOLUMES', 'physical_volumes', Side.LEFT),
    })

    def __init__(self, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None):
        self.path = self.get_real_path(path, volume_group, logical_volume)
        self.name = Path(self.path).name
        super().__init__(path)
        self.volume_group = vg.VolumeGroup.get_volume_group(logical_volume=self.path)
        self.physical_volumes = super().get_physical_volumes(logical_volume=self.path)
        self.print_cols = [Properties.NAME, Properties.VOLUME_GROUP, Properties.PHYSICAL_VOLUMES, Properties.FSTYPE, Properties.MOUNTPOINT, Properties.SIZE, Properties.USED, Properties.FREE,
                           Properties.USAGE_PERCENT, Properties.USAGE_GRAPH]
        self.is_snapshot = self.snapshot_exists(self.path)
        self.origin = None
        if self.is_snapshot:
            self.origin, self.size, self.used, self.free, self.usage_percent, self.usage_graph = self.get_snapshots_usages(self.path)

    @classmethod
    def logical_volume_exists(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> bool:
        res = True
        if path is None:
            if volume_group is None or logical_volume is None:
                return False
            else:
                path = Path('/').joinpath('dev').joinpath(volume_group.strip()).joinpath(logical_volume.strip())
        try:
            path = super().get_real_path(path)
            command = ['lvs', path]
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        except (CalledProcessError, ValueError):
            res = False
        return res

    @classmethod
    def snapshot_exists(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> bool:
        res = True
        try:
            path = cls.get_real_path(path, volume_group, logical_volume)
            command = ['lvs', '--noheadings', '--options', 'ORIGIN', path]
            origin = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.strip()
            if not origin:
                res = False
        except (CalledProcessError, ValueError):
            res = False
        return res

    @classmethod
    def assert_exists(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None):
        if path is None:
            if volume_group is None or logical_volume is None:
                raise ValueError('You must provide either a path to the logical volume or the volume group it belongs to and its name.')
            path = Path('/').joinpath('dev').joinpath(volume_group.strip()).joinpath(logical_volume.strip())
        if not cls.logical_volume_exists(path):
            raise ValueError('Device "{0}" is not a logical volume'.format(path))

    @classmethod
    def get_real_path(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> str:
        cls.assert_exists(path, volume_group, logical_volume)
        if path is None:
            path = Path('/').joinpath('dev').joinpath(volume_group.strip()).joinpath(logical_volume.strip())
        path = super().get_real_path(path)
        return path

    @classmethod
    def get_logical_volumes(cls, physical_device: Union[str, Path] = None, volume_group: str = None) -> Tuple[str]:
        logical_volumes = ()
        if physical_device:
            physical_device = drive.Drive.get_real_path(physical_device)
            if drive.Drive.physical_volume_exists(physical_device):
                command = ['lsblk', '--list', '--paths', '-o', 'NAME', '--noheadings', physical_device]
                lsblk = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip().split('\n')[1:]
                logical_volumes = [drive.Drive.get_real_path(lv) for lv in lsblk]
                logical_volumes = [x for x in logical_volumes if x is not None]
                logical_volumes = tuple(dict.fromkeys(logical_volumes))
        else:
            command = ['lvs', '--noheadings', '--options', 'NAME,VG_NAME']
            if volume_group:
                vg.VolumeGroup.assert_exists(volume_group)
                command.append(volume_group)
            lvs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
            if lvs:
                lvs = lvs.split('\n')
                lvs = [lv.strip() for lv in lvs]
                regex = re.compile(r'^(\S+) +(\S+)$')
                logical_volumes = []
                for line in lvs:
                    match = re.search(regex, line)
                    log_vol = str(Path('/').joinpath('dev').joinpath(match.group(2)).joinpath(match.group(1)))
                    logical_volumes.append(log_vol)
                logical_volumes = tuple(logical_volumes)
        if len(logical_volumes) == 0:
            logical_volumes = None
        return logical_volumes

    @classmethod
    def get_snapshots(cls, physical_device: Union[str, Path] = None, volume_group: str = None) -> Tuple[str]:
        logical_volumes = cls.get_logical_volumes(physical_device=physical_device, volume_group=volume_group)
        if logical_volumes is None:
            return None
        logical_volumes = tuple([x for x in logical_volumes if LogicalVolume.snapshot_exists(path=x)])
        if len(logical_volumes) == 0:
            logical_volumes = None
        return logical_volumes

    @classmethod
    def get_snapshots_usages(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> Tuple[str, int, int, int, int, str]:
        path = cls.get_real_path(path, volume_group, logical_volume)
        if not cls.snapshot_exists(path):
            raise ValueError('Error: Device {0} is not a snapshot.'.format(path))
        command = ['lvs', '--noheadings', '--units', 'b', '--rows', '--options', 'ORIGIN,LV_SIZE,SNAP_PERCENT', path]
        res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip().split('\n')
        res = [x.strip() for x in res]
        origin = res[0]
        size = int(res[1][:-1])
        usage_percent = float(res[2].replace(',', '.'))
        used = round(size * usage_percent / 100.0)
        usage_percent = round(usage_percent)
        free = size - used
        usage_graph = cls.draw_usage_graph(usage_percent, Backgrounds.LIGHT_CYAN, brackets_color=TextColors.DARK_GRAY, hashtag_color=TextColors.LIGHT_RED, point_color=TextColors.BLUE)
        return origin, size, used, free, usage_percent, usage_graph

    @classmethod
    def get_origin(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> str:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[0]
        return None

    @classmethod
    def get_size(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> int:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[1]
        path = cls.get_real_path(path, volume_group, logical_volume)
        return super().get_size(path)

    @classmethod
    def get_used(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> int:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[2]
        path = cls.get_real_path(path, volume_group, logical_volume)
        return super().get_used(path)

    @classmethod
    def get_free(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> int:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[2]
        path = cls.get_real_path(path, volume_group, logical_volume)
        return super().get_free(path)

    @classmethod
    def get_usage_percent(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> int:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[4]
        path = cls.get_real_path(path, volume_group, logical_volume)
        return super().get_usage_percent(path)

    @classmethod
    def get_usage_graph(cls, path: Union[str, Path] = None, volume_group: str = None, logical_volume: str = None) -> str:
        if cls.snapshot_exists(path, volume_group, logical_volume):
            return cls.get_snapshots_usages(path, volume_group, logical_volume)[5]
        path = cls.get_real_path(path, volume_group, logical_volume)
        return super().get_usage_graph(path)


class LogicalVolumes(BaseDevices):

    def __init__(self, logical_volumes=None):
        if logical_volumes is None:
            logical_volumes = LogicalVolume.get_logical_volumes()
        if logical_volumes is None:
            logical_volumes = []
        logical_volumes = [LogicalVolume(path=x) for x in logical_volumes]
        self.devices = tuple(logical_volumes)
        self.device_class = LogicalVolume
        self.print_cols = [Properties.NAME, Properties.ORIGIN, Properties.VOLUME_GROUP, Properties.PHYSICAL_VOLUMES, Properties.FSTYPE, Properties.MOUNTPOINT, Properties.SIZE, Properties.USED,
                           Properties.FREE, Properties.USAGE_PERCENT, Properties.USAGE_GRAPH]


class Snapshots(LogicalVolumes):

    def __init__(self):
        logical_volumes = LogicalVolume.get_snapshots()
        if logical_volumes is None:
            logical_volumes = []
        super().__init__(logical_volumes)
