#!/usr/bin/env python3
# encoding:utf-8


import re
import subprocess
from pathlib import Path
from subprocess import CalledProcessError
from typing import Union, Tuple

from terminal_debian.drives.common import Properties, Side, BaseDevice, BaseDevices
from terminal_debian.style import Backgrounds, TextColors


class Drive(BaseDevice):
    PROPERTIES = dict(BaseDevice.PROPERTIES)
    PROPERTIES.update({
        Properties.FSTYPE: ('FSTYPE', 'fstype', Side.LEFT),
        Properties.LABEL: ('LABEL', 'label', Side.LEFT),
        Properties.LOGICAL_VOLUMES: ('LOGICAL VOLUMES', 'logical_volumes', Side.LEFT),
        Properties.MOUNTPOINT: ('MOUNTPOINT', 'mountpoint', Side.LEFT),
        Properties.PATH: ('DEVICE', 'path', Side.LEFT),
        Properties.UUID: ('UUID', 'uuid', Side.LEFT),
        Properties.VOLUME_GROUP: ('VOLUME GROUP', 'volume_group', Side.LEFT),
    })

    def __init__(self, path):
        self.path = self.get_real_path(path)
        self.name = Path(self.path).name
        self.fstype, self.label, self.mountpoint, self.uuid = self.get_properties(self.path)
        self.is_physical_volume = self.physical_volume_exists(self.path)
        self.size, self.used, self.free, self.usage_percent, self.usage_graph = self.get_usages(self.path)
        self.is_logical_volume = None
        self.volume_group = None
        self.logical_volumes = None
        self._set_external_properties()
        self.print_cols = [Properties.PATH, Properties.FSTYPE, Properties.LABEL, Properties.MOUNTPOINT, Properties.VOLUME_GROUP, Properties.LOGICAL_VOLUMES, Properties.SIZE, Properties.USED,
                           Properties.FREE, Properties.USAGE_PERCENT, Properties.USAGE_GRAPH]

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.path != other.path:
            return False
        return True

    @classmethod
    def get_properties(cls, physical_device: Union[str, Path]) -> Tuple[str, str, str, str]:
        physical_device = cls.get_real_path(physical_device)
        command = ['lsblk', '--pairs', '--paths', '--nodeps', '--output', 'NAME,FSTYPE,LABEL,MOUNTPOINT,UUID', physical_device]
        lsblk = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        regex_properties = re.compile(r'NAME=\".*?\" FSTYPE=\"(.*?)\" LABEL=\"(.*?)\" MOUNTPOINT=\"(.*?)\" UUID=\"(.*?)\"')
        properties = re.match(regex_properties, lsblk)
        fstype = properties.group(1) if properties.group(1) else None
        label = properties.group(2) if properties.group(2) else None
        mountpoint = properties.group(3) if properties.group(3) else None
        uuid = properties.group(4) if properties.group(4) else None
        return fstype, label, mountpoint, uuid

    def _set_external_properties(self):
        from terminal_debian.drives import logical_volume as lv
        from terminal_debian.drives import volume_group as vg
        self.is_logical_volume = lv.LogicalVolume.logical_volume_exists(path=self.path)
        self.volume_group = vg.VolumeGroup.get_volume_group(physical_volume=self.path) if self.is_physical_volume else None
        self.logical_volumes = lv.LogicalVolume.get_logical_volumes(physical_device=self.path) if self.volume_group else None

    @classmethod
    def get_fstype(cls, physical_device: Union[str, Path]) -> str:
        return cls.get_properties(physical_device)[0]

    @classmethod
    def get_label(cls, physical_device: Union[str, Path]) -> str:
        return cls.get_properties(physical_device)[1]

    @classmethod
    def get_mountpoint(cls, physical_device: Union[str, Path]) -> str:
        return cls.get_properties(physical_device)[2]

    @classmethod
    def get_uuid(cls, physical_device: Union[str, Path]) -> str:
        return cls.get_properties(physical_device)[3]

    @classmethod
    def get_usages(cls, physical_device: Union[str, Path]) -> Tuple[int, int, int, int, str]:
        physical_device = cls.get_real_path(physical_device)
        if cls.physical_volume_exists(physical_device):
            command = ['pvs', '--noheadings', '--units', 'b', '--rows', '--options', 'SIZE,FREE', physical_device]
            command_res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip().split('\n')
            command_res = [int(line.strip()[:-1]) for line in command_res]
        else:
            command = ['df', '--block-size=1', physical_device]
            command_res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip().split('\n')[1]
            if command_res.startswith('udev'):
                size = cls.get_partition_size(physical_device)
                return size, None, None, None, None
            regex = re.compile(r'^\S+ +(\d+) +\d+ +(\d+)')
            command_res = re.match(regex, command_res)
            command_res = [int(command_res.group(1)), int(command_res.group(2))]
        command_res.append(command_res[0] - command_res[1])
        size, free, used = command_res[0], command_res[1], command_res[2]
        usage_percent = round((used * 100.0) / size)
        usage_graph = cls.draw_usage_graph(usage_percent, Backgrounds.LIGHT_CYAN, brackets_color=TextColors.DARK_GRAY, hashtag_color=TextColors.LIGHT_RED, point_color=TextColors.BLUE)
        return size, used, free, usage_percent, usage_graph

    @classmethod
    def get_partition_size(cls, physical_device: Union[str, Path]) -> int:
        physical_device = cls.get_real_path(physical_device)
        command = ['lsblk', '--noheadings', '--nodeps', '--output', 'SIZE', '--bytes', physical_device]
        command_res = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
        size = int(command_res)
        return size

    @classmethod
    def get_size(cls, physical_device: Union[str, Path]) -> int:
        return cls.get_usages(physical_device)[0]

    @classmethod
    def get_used(cls, physical_device: Union[str, Path]) -> int:
        return cls.get_usages(physical_device)[1]

    @classmethod
    def get_free(cls, physical_device: Union[str, Path]) -> int:
        return cls.get_usages(physical_device)[2]

    @classmethod
    def get_usage_percent(cls, physical_device: Union[str, Path]) -> int:
        return cls.get_usages(physical_device)[3]

    @classmethod
    def get_usage_graph(cls, physical_device: Union[str, Path]) -> str:
        return cls.get_usages(physical_device)[4]

    @staticmethod
    def physical_device_exists(path: Union[str, Path]) -> bool:
        res = True
        path = Path(str(path).strip())
        if not path.is_block_device():
            res = False
        return res

    @classmethod
    def assert_physical_device_exists(cls, path: Union[str, Path]):
        path = Path(str(path).strip())
        if not cls.physical_device_exists(path):
            raise ValueError('Path "{0}" does not point to a block device'.format(path))

    @classmethod
    def physical_volume_exists(cls, path: Union[str, Path]) -> bool:
        res = True
        path = str(Path(str(path).strip()))
        if not cls.physical_device_exists(path):
            res = False
        else:
            try:
                command = ['pvs', path]
                subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            except CalledProcessError:
                res = False
        return res

    @classmethod
    def assert_physical_volume_exists(cls, path: Union[str, Path]):
        if not cls.physical_volume_exists(path):
            raise ValueError('Physical volume "{0}" not found'.format(path))

    @classmethod
    def get_real_path(cls, name: Union[str, Path]) -> str:
        res = str(Path(str(name).strip()))
        cls.assert_physical_device_exists(res)
        regex = re.compile(r'^/dev/dm-\d+$')
        if re.search(regex, res) is not None:
            command = ['dmsetup', 'info', '--noheadings', '--columns', '-o', 'name', res]
            dmsetup = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('utf-8').strip()
            res = str(Path('/').joinpath('dev').joinpath('mapper').joinpath(dmsetup))
        if res.find('mapper') != -1:
            from terminal_debian.drives import volume_group as vg
            volume_groups = vg.VolumeGroup.get_volume_groups()
            for vol in volume_groups:
                mapper = Path(res)
                candidates = Path('/').joinpath('dev').joinpath(vol)
                candidates = [file for file in candidates.glob('*')]
                for lv in candidates:
                    if mapper.samefile(lv):
                        res = str(lv)
                        return res
        return res

    @staticmethod
    def get_drives() -> Tuple[str]:
        command = ['lsblk', '--paths', '--noheadings', '--list', '--output', 'NAME']
        lsblk = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip().split('\n')
        drives = []
        for line in lsblk:
            line = line.strip()
            index = line.find('/')
            if index != -1:
                drives.append(Drive.get_real_path(line[index:]))
        drives = tuple([x for x in drives if x is not None])
        drives = tuple(dict.fromkeys(drives))
        return drives

    @classmethod
    def get_physical_volumes(cls, volume_group: str = None, logical_volume: Union[str, Path] = None) -> Tuple[str]:
        physical_volumes = ()
        if volume_group is not None:
            from terminal_debian.drives import volume_group as vg
            vg.VolumeGroup.assert_exists(volume_group)
            command = ['pvs', '--noheadings', '--options', 'NAME,VG_NAME']
            pvs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip().split('\n')
            pvs = '\n'.join([pv.strip() for pv in pvs])
            regex = re.compile(r'^(\S+) +(\S+)$', re.MULTILINE)
            physical_volumes = re.findall(regex, pvs)
            physical_volumes = [group[0] for group in physical_volumes if group[1] == volume_group]
            physical_volumes = [cls.get_real_path(pv) for pv in physical_volumes]
        elif logical_volume is not None:
            from terminal_debian.drives import logical_volume as lv
            from terminal_debian.drives import volume_group as vg
            logical_volume = lv.LogicalVolume.get_real_path(logical_volume)
            volume_group = vg.VolumeGroup.get_volume_group(logical_volume=logical_volume)
            drives = cls.get_drives()
            physical_volumes = []
            for drive in drives:
                if cls.physical_volume_exists(drive) and vg.VolumeGroup.get_volume_group(physical_volume=drive) == volume_group:
                    lvs = lv.LogicalVolume.get_logical_volumes(physical_device=drive)
                    if lvs is not None and logical_volume in lvs:
                        physical_volumes.append(drive)
        else:
            command = ['pvs', '--noheadings', '--options', 'NAME']
            pvs = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()
            if pvs:
                pvs = pvs.split('\n')
                physical_volumes = [pv.strip() for pv in pvs]
        physical_volumes = None if len(physical_volumes) == 0 else tuple(physical_volumes)
        return physical_volumes

    def __repr__(self):
        return self.path


class Drives(BaseDevices):

    def __init__(self, drives=None):
        from terminal_debian.drives import logical_volume
        if drives is None:
            drives = Drive.get_drives()
        if drives is None:
            drives = []
        drives = [Drive(x) if not logical_volume.LogicalVolume.logical_volume_exists(x) else logical_volume.LogicalVolume(x) for x in drives]
        self.devices = tuple(drives)
        self.device_class = Drive
        self.print_cols = [Properties.NAME, Properties.FSTYPE, Properties.LABEL, Properties.MOUNTPOINT, Properties.VOLUME_GROUP, Properties.LOGICAL_VOLUMES, Properties.SIZE, Properties.USED,
                           Properties.FREE, Properties.USAGE_PERCENT, Properties.USAGE_GRAPH]


class PhysicalVolumes(Drives):

    def __init__(self, physical_volumes=None):
        if physical_volumes is None:
            physical_volumes = Drive.get_physical_volumes()
        if physical_volumes is None:
            physical_volumes = []
        [Drive.assert_physical_volume_exists(_) for _ in physical_volumes]
        super().__init__(physical_volumes)
        self.print_cols = [Properties.NAME, Properties.VOLUME_GROUP, Properties.LOGICAL_VOLUMES, Properties.SIZE, Properties.USED, Properties.FREE, Properties.USAGE_PERCENT, Properties.USAGE_GRAPH]
