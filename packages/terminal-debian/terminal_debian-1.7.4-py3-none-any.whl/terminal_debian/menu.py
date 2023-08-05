#!/usr/bin/env python3
# encoding:utf-8


import os
import shutil
import sys
from enum import Enum
from random import SystemRandom
from time import sleep
from typing import Union

from terminal_debian.utils import Utils


class Menu:
    __redirect_name = str.format('Menu.redirect {0}', SystemRandom().getrandbits(32))
    """
    La variable de inicialización "opciones" contiene todos los menús superiores, y debe ser un mapa con el siguiente formato:
    opciones = {
        0: {
            0: 'Cabecera del menú',
            1: ('Primera opción del menú', función_a_ejecutar, reset=True),
            2: ('Segunda opción del menú', función_a_ejecutar, reset=True),
        }
    }
    """

    def __init__(self, opciones: dict, ancho: int = None, alto: int = None):
        self.__opciones = dict(opciones)
        self.__dimensiones_originales_terminal = shutil.get_terminal_size()
        ancho = ancho if ancho is not None else self.__dimensiones_originales_terminal[0]
        alto = alto if alto is not None else self.__dimensiones_originales_terminal[1]
        Utils.redimensionar_terminal(ancho, alto, estricto=False)

    def get_dimensiones_originales_terminal(self):
        return self.__dimensiones_originales_terminal

    def get_opciones(self):
        return self.__opciones

    def menu_superior(self, menu):
        os.system('clear')
        inner_menu = dict(self.__opciones[menu])
        print(inner_menu[0])
        for opcion in range(1, len(inner_menu)):
            titulo = inner_menu[opcion][0]
            print(str.format('\t{0}. {1}\n', opcion, titulo))
        opcion_selec = input(' Seleccione una opción: ')
        self.exec(menu, opcion_selec)

    @staticmethod
    def menu_opciones(pregunta: str, opciones: Union[list, tuple]):
        print('\n' + pregunta + '\n')
        for i in range(len(opciones)):
            print(str.format('\t{0}. {1}\n', i + 1, opciones[i]))
        while True:
            try:
                opcion_selec = input(' Seleccione una opción: ')
                opcion_selec = int(opcion_selec) - 1
                opciones[opcion_selec]
                print()
                return opcion_selec
            except (IndexError, ValueError):
                print(' Error: La opción seleccionada no es válida\n')

    @staticmethod
    def menu_booleano(pregunta: str, ejecutar_si=lambda: None, ejecutar_no=lambda: None, defecto=None):
        if defecto is None:
            pregunta += ' [s/n] '
        elif defecto is Opciones.SI:
            pregunta += ' [S/n] '
        elif defecto is Opciones.NO:
            pregunta += ' [s/N] '
        while True:
            opcion = input(pregunta).lower()
            res = Opciones.REINICIAR
            if (opcion == 's') or ((opcion == '') and defecto is Opciones.SI):
                res = ejecutar_si()
            elif (opcion == 'n') or ((opcion == '') and defecto is Opciones.NO):
                res = ejecutar_no()
            else:
                print(' Error: La opción seleccionada no es válida')
            if res is Opciones.REINICIAR:
                print()
                continue
            return res

    @staticmethod
    def redirect(opcion):
        """
        Carga el menú superior que es pasado a través del parámetro 'opción'.
        """

        def redirect_fixed():
            return opcion

        redirect_fixed.__name__ = Menu.__redirect_name
        return redirect_fixed

    def exec(self, menu, opcion, reset=True):
        try:
            opcion = int(opcion)
            funcion = self.__opciones[menu][opcion][1]
        except (KeyError, ValueError):
            print(' Error: La opción seleccionada no es válida\n')
            opcion = input(' Seleccione una opción: ')
            self.exec(menu, opcion)
        else:
            if len(self.__opciones[menu][opcion]) == 3:
                reset = bool(self.__opciones[menu][opcion][2])
            if reset:
                os.system('clear')
            else:
                print()
            if funcion.__name__ == Menu.__redirect_name:
                self.menu_superior(funcion())
            else:
                funcion()

    def salir(self, mensaje='', reset=False, sleep_time=0, exit_code=0):
        print(mensaje)
        sleep(sleep_time)
        if reset:
            os.system('clear')
        Utils.redimensionar_terminal(*self.__dimensiones_originales_terminal, estricto=True)
        Utils.restore_echo_control_characters()
        sys.exit(exit_code)


class Opciones(Enum):
    SI = 1
    NO = 2
    REINICIAR = 3
