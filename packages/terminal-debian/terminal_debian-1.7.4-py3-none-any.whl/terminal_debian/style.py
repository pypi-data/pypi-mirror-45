#!/usr/bin/env python3
# encoding:utf-8


from enum import Enum


class TextColors(Enum):
    BLACK = '\033[30m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    DARK_GRAY = '\033[90m'
    DEFAULT = '\033[39m'
    GREEN = '\033[32m'
    LIGHT_BLUE = '\033[94m'
    LIGHT_CYAN = '\033[96m'
    LIGHT_GRAY = '\033[37m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_MAGENTA = '\033[95m'
    LIGHT_RED = '\033[91m'
    LIGHT_YELLOW = '\033[93m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    WHITE = '\033[97m'
    YELLOW = '\033[33m'


class Backgrounds(Enum):
    BLACK = '\033[40m'
    BLUE = '\033[44m'
    CYAN = '\033[46m'
    DARK_GRAY = '\033[100m'
    DEFAULT = '\033[49m'
    GREEN = '\033[42m'
    LIGHT_BLUE = '\033[104m'
    LIGHT_CYAN = '\033[106m'
    LIGHT_GRAY = '\033[47m'
    LIGHT_GREEN = '\033[102m'
    LIGHT_MAGENTA = '\033[105m'
    LIGHT_RED = '\033[101m'
    LIGHT_YELLOW = '\033[103m'
    MAGENTA = '\033[45m'
    RED = '\033[41m'
    WHITE = '\033[107m'
    YELLOW = '\033[43m'


class Formats(Enum):
    BLINK = '\033[5m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    HIDDEN = '\033[8m'
    RESET = '\033[0m'
    REVERSE = '\033[7m'
    UNDERLINED = '\033[4m'


class Style:

    @staticmethod
    def apply(string, *formats):
        res = string
        for formato in formats:
            res = formato.value + res
        res += Formats.RESET.value
        return res
