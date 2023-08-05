#!/usr/bin/env python3
# encoding:utf-8


import copy
import os
import re
import shutil
import subprocess
import sys
import termios
from pathlib import Path
from random import SystemRandom
from zipfile import ZipFile


class Utils:
    disable_echo_control_characters = lambda x=None: None
    restore_echo_control_characters = lambda x=None: None

    @staticmethod
    def create_tmp_folder(path: str = '/tmp'):
        i = 0
        while True:
            carpeta_temporal = Path(path).joinpath('tmp_{random}{number}'.format(random=SystemRandom().getrandbits(32), number=i))
            if not carpeta_temporal.is_dir():
                Path.mkdir(carpeta_temporal, parents=True, exist_ok=True)
                return carpeta_temporal
            i += 1

    @classmethod
    def extract_from_zip(cls, zipfile: str, content: str, destination: str, include_folder: bool = True, recursive: bool = False):
        """
        Extrae los contenidos de una carpeta contenida en un zip en la carpeta destino.
        Hay que tener en cuenta que al extraerse los contenidos de una carpeta, ésta también es creada.
        :param zipfile: Ruta al fichero zip
        :param content: Carpeta o Archivo del zip a ser extraído. Las carpetas deben terminar en /. Si solo queremos extraer los archivos
        de la carpeta raíz, sin subcarpetas, dejaremos este parámetro como una cadena en blanco.
        :param destination: Dónde será extraido el contenido. No puede estar vacío ni ser el directorio raíz '/'.
        :param include_folder: (Sólo si en content hemos seleccionado una carpeta) Incluye la propia carpeta en la extracción, o bien extrae directamente todos los archivos
        :param recursive: Si vale True, se extraerán todas las subcarpetas de la carpeta que indiquemos
        :return: Lista de archivos que han sido extraídos
        """
        if not destination:
            raise ValueError("El parámetro 'destination' no puede ser vacío")
        if destination == '/':
            raise ValueError("El parámetro 'destination' no puede ser el directorio raíz '/'")
        regex = '^' + re.escape(content)
        if recursive:
            regex = regex + '.*'
        else:
            regex = regex + '[^/]*'
        regex = re.compile(regex)
        is_folder = False
        with ZipFile(zipfile, 'r') as myzip:
            files = [file for file in myzip.filelist]
            extract = [file.string for file in [regex.fullmatch(file.filename) for file in files] if file is not None]
            if not len(extract):  # Si no hay ningún archivo por extraer, se sale de la ejecución
                return None
            if content:
                is_folder = True if extract[0][-1] == '/' else False  # Determina si el contenido a extraer es una carpeta
            tmp = cls.create_tmp_folder(destination)
            for file in extract:
                is_dir = True if file[-1] == '/' else False
                destino = tmp.joinpath(file)
                if is_dir:
                    permisos = myzip.getinfo(file).external_attr >> 16
                    Path.mkdir(destino, parents=True, exist_ok=True)
                    Path.chmod(destino, permisos)
                else:
                    destino = destino.parent
                    cls.extract_single_file(zipfile, file, str(destino))  # Extraemos cada archivo y carpeta deseados en una carpeta temporal dentro del destino
        copy = ['cp', '-rfl']  # Copiamos de manera recursiva, forzosa y usando enlaces duros
        if (not content) or (is_folder and not include_folder):  # Si vamos a extraer el zip completo o bien sólo los contenidos de una carpeta sin incluirla
            copy.append('-T')  # No incluir la carpeta contenedora
        copy.extend([str(tmp.joinpath(content)), str(destination)])  # Origen y destino
        subprocess.run(copy, check=True)
        shutil.rmtree(str(tmp))
        return extract

    @classmethod
    def extract_single_file(cls, zip_file: str, inner_file_rel_path: str, destination: str):
        """
        Extrae un archivo concreto contenido en un zip en la carpeta especificada preservando los permisos.
        :param zip_file: Ruta al fichero zip
        :param inner_file_rel_path: Ruta interna dentro del zip del archivo a extraer
        :param destination: Carpeta destino del archivo a extraer
        """
        with ZipFile(zip_file) as myzip:
            permisos = myzip.getinfo(inner_file_rel_path).external_attr >> 16
            tmp = cls.create_tmp_folder(destination)
            myzip.extract(inner_file_rel_path, str(tmp))
        extraido = tmp.joinpath(inner_file_rel_path)
        os.chmod(str(extraido), permisos)
        shutil.move(str(extraido), str(destination))
        shutil.rmtree(str(tmp))

    @classmethod
    def configure_echo_control_characters(cls):
        '''
        Create methods for enabling and disabling the printing of some inputs as Control+C (^C)
        The optional argument x=None is required in case the method is called with self or cls as first argument
        '''
        try:
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = copy.deepcopy(old)
            new[3] = new[3] & ~termios.ECHOCTL
            cls.disable_echo_control_characters = lambda x=None: termios.tcsetattr(fd, termios.TCSADRAIN, new)
            cls.restore_echo_control_characters = lambda x=None: termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except termios.error:
            print('Error: Could not configure echo control characters', file=sys.stderr)

    @classmethod
    def redimensionar_terminal(cls, ancho: int = 0, alto: int = 0, estricto: bool = True):
        dim_ancho, dim_alto = shutil.get_terminal_size()
        ancho = dim_ancho if ancho is None else ancho
        alto = dim_alto if alto is None else alto
        ancho, alto = int(ancho), int(alto)  # Si los dos valen 0, se restablece el terminal a las dimensiones por defecto
        if os.environ.get('TERM', default=None) == 'linux':  # Para los terminales tty puros y no emuladores del terminal
            pass
        elif estricto:
            formato = "\033[8;{0};{1}t".format(alto, ancho)  # El byte \033 representa \e (también sirve el byte \x1b)
            print(formato, end='')
        else:
            ancho = dim_ancho if dim_ancho > ancho else ancho
            alto = dim_alto if dim_alto > alto else alto
            cls.redimensionar_terminal(ancho, alto, estricto=True)


Utils.configure_echo_control_characters()
