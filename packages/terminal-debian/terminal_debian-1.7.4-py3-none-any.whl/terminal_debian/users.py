#!/usr/bin/env python3
# encoding:utf-8


import grp
import os
import pwd
import shutil
import subprocess
from pathlib import Path
from subprocess import CalledProcessError

from terminal_debian.utils import Utils


class Users:

    @classmethod
    def adduser(cls, user: str, uid: int = None, home: str = None, system: bool = False, group: bool = False):
        command = ['adduser']
        if system:
            command.extend(('--system', '--shell', '/bin/bash'))
            if group:
                command.append('--group')
        elif uid is not None:
            command.extend(('--uid', str(uid)))
        if home is False:
            command.append('--no-create-home')
            command.extend(('--home', '/nonexistent'))
        elif home is not None:
            command.extend(('--home', home))
        try:
            command.append(user)
            already_exists = cls.user_exists(user)
            subprocess.run(command, check=True)
            if system and home is not False and not already_exists:
                cls.copy_skel(user)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def addgroup(group: str, gid: int = None, system: bool = False):
        command = ['addgroup']
        if system:
            command.append('--system')
        elif gid is not None:
            command.extend(('--gid', str(gid)))
        try:
            command.append(group)
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def delpass(user: str):
        '''
        Se elimina la contraseña del usuario, lo que hará el acceso como sudo inaccesible por consola al pedirnos una contraseña
        '''
        try:
            command = ['passwd', '-d', user]
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def set_blank_pass(user: str):
        '''
        La contraseña del usuario se pone en blanco, de modo que para loguearse basta con pulsar la tecla enter
        '''
        try:
            command = ['usermod', '-p', 'U6aMy0wojraho', user]
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def lock_account(user: str):
        '''
        Se bloquea la cuenta del usuario poniendo su shell a /usr/sbin/nologin
        '''
        try:
            command = ['usermod', '-s', '/usr/sbin/nologin', user]
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def unlock_account(user: str):
        '''
        Se desbloquea la cuenta del usuario poniendo su shell a /bin/bash
        '''
        try:
            command = ['usermod', '-s', '/bin/bash', user]
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def deluser(user: str, delete_home: bool = False, delete_all: bool = False):
        try:
            command = ['deluser']
            if delete_all:
                command.append('--remove-all-files')
            elif delete_home:
                command.append('--remove-home')
            command.append(user)
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def delgroup(group: str):
        try:
            command = ['delgroup', group]
            subprocess.run(command, check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def add_to_group(user: str, group: str):
        try:
            subprocess.run(['gpasswd', '-a', user, group], check=True)
            return True
        except CalledProcessError:
            return False

    @staticmethod
    def remove_from_group(user: str, group: str):
        try:
            subprocess.run(['gpasswd', '-d', user, group], check=True)
            return True
        except CalledProcessError:
            return False

    @classmethod
    def grant_admin(cls, user: str):
        groups = ['adm', 'audio', 'cdrom', 'dip', 'docker', 'floppy', 'lpadmin', 'netdev', 'plugdev', 'scanner', 'sudo', 'vboxsf', 'vboxusers', 'video', 'x2godesktopsharing']
        [cls.add_to_group(user, group) for group in groups if cls.group_exists(group)]

    @classmethod
    def revoke_admin(cls, user: str):
        groups = ['adm', 'docker', 'sudo']
        [cls.remove_from_group(user, group) for group in groups if cls.group_exists(group)]

    @staticmethod
    def is_sudo():
        return os.geteuid() == 0

    @staticmethod
    def user_exists(user: str):
        try:
            pwd.getpwnam(user)
            return True
        except KeyError:
            return False

    @staticmethod
    def group_exists(group: str):
        try:
            grp.getgrnam(group)
            return True
        except KeyError:
            return False

    @classmethod
    def copy_skel(cls, user: str):
        if not cls.user_exists(user):
            print('\n\tError: El usuario {usuario} no existe'.format(usuario=user))
            return False
        user_info = pwd.getpwnam(user)
        group = grp.getgrgid(user_info.pw_gid).gr_name
        home = Path(user_info.pw_dir)
        if not home.is_dir():
            print('\n\tError: La carpeta home del usuario {usuario} es {ruta}, pero no existe'.format(usuario=user, ruta=home))
            return False
        tmp = Utils.create_tmp_folder(home)
        subprocess.run(['cp', '-rfT', '/etc/skel', str(tmp)], check=True)
        subprocess.run(['chown', '-R', '{user}:{group}'.format(user=user, group=group), str(tmp)], check=True)
        subprocess.run(['su', '-', user, '-c', 'cp -rfTl {tmp} {home}'.format(tmp=str(tmp), home=str(home))], check=True)
        shutil.rmtree(str(tmp))
        return True
