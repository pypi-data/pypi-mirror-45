#!/usr/bin/env python3
# encoding:utf-8


import subprocess


class Apt:

    @classmethod
    def actualizar(cls):
        cls.update()
        subprocess.run(['aptitude', 'full-upgrade'], check=True)
        subprocess.run(['apt-get', 'autoremove'], check=True)
        subprocess.run(['aptitude', 'autoclean'], check=True)
        subprocess.run(['apt-get', 'autoclean'], check=True)

    @staticmethod
    def update():
        subprocess.run(['aptitude', 'update'], check=True)

    @staticmethod
    def purge(packages, force=False):
        eliminar = ['aptitude', 'purge']
        if force:
            eliminar.append('-y')
        if isinstance(packages, str):
            eliminar.append(packages)
        else:
            eliminar.extend(packages)
        subprocess.run(eliminar, check=True)

    @classmethod
    def install(cls, packages, force=False):
        instalar = ['aptitude', 'install']
        if force:
            instalar.append('-y')
        if isinstance(packages, str):
            instalar.append(packages)
        else:
            instalar.extend(packages)
        cls.update()
        subprocess.run(instalar, check=True)

    @staticmethod
    def import_key(id):
        add_key = ['apt-key', 'adv', '--keyserver', 'keyserver.ubuntu.com', '--recv-keys', id]
        subprocess.run(add_key, check=True)
