"""This file contains classes for a simpler an easier print/log handeling"""

from warnings import warn
from enum import IntEnum

# Different display formats
text_format = {'normal': '\033[0;0;0m', 'error': '\033[0;31;0m', 'warning': '\033[0;31;0m',
               'info': '\033[0;34;0m', 'debug': '\033[0;32;0m', 'frivolous': '\033[0;0;0m'}

# Different headers
text_header = {'error': 'ERROR: ', 'warning': 'WARNING: ', 'info': 'INFO: ', 'debug': 'DEBUG: ',
               'frivolous': 'FRIVOLITY: '}


class AutoNumber(IntEnum):
    """ Super class for auto numbering the Enumeration"""
    def __new__(cls):
        value = len(cls.__members__) + 1
        obj = int.__new__(cls)
        obj._value_ = value
        return obj


class VerboseLevel(AutoNumber):
    """ Used to check on the different verbose levels. Auto-numbered for easy changes"""
    SILENT = ()
    ERROR = ()
    WARNING = ()
    INFO = ()
    DEBUG = ()
    FRIVOLOUS = ()


class PapageiError(Exception):
    """ Error class to return python errors in error()"""
    def __init__(self, args):
        # Formats the arguments into a string for display (takes a tuple as input)
        self.msg = _format_string_from_tuple(args)

    def __str__(self):
        return self.msg


VERBOSE = VerboseLevel.FRIVOLOUS  # Change this variable to change the verbose level


def log_error(*args):
    """
        Raises an python error.
        Works is VERBOSE is ERROR or higher.
            :param args: All formatted into a single string to be used as an error message
            :return: Raises an error
    """
    if VERBOSE.value >= VerboseLevel.ERROR.value:
        raise PapageiError(args)


def mock_error(*args):
    """
        Prints a message in an error-like format without stopping the program.
        Works if VERBOSE is ERROR or higher.
            :param args: All formatted into a single string to be used as an error message.
    """
    if VERBOSE.value >= VerboseLevel.ERROR.value:
        msg = _format_string_from_tuple(args)
        msg = text_format['error']+text_header['error']+msg+text_format['normal']
        print(msg)


def log_warning(*args, **kwarg):
    """
        Generates and print a python warning and returns the warning.
        Works if VERBOSE is WARNING or higher
            :param args:    All formatted into a single string to be used as a warning message.
            :param kwarg:   'type': warning type
                                    Is a python error type the will be used as the error type.
                                    Default: UserWarning

            :return: papagei_warning:  Warning of class 'type' containing the error message
    """
    warning_class = kwarg.pop('type', UserWarning)
    msg = _format_string_from_tuple(args)
    papagei_warning = warning_class(msg)
    if VERBOSE.value >= VerboseLevel.WARNING.value:
        warn(papagei_warning)
    return papagei_warning


def mock_warning(*args):
    """
        Prints a message in an warning-like format without stopping the program.
        Works if VERBOSE is WARNING or higher.
            :param args: All formatted into a single string to be used as a warning message.
    """
    if VERBOSE.value >= VerboseLevel.WARNING.value:
        msg = _format_string_from_tuple(args)
        msg = text_format['warning'] + text_header['warning'] + msg + text_format['normal']
        print(msg)


def log_info(*args):
    """
        Prints a message for generic information with a specific info-format.
        Works if VERBOSE is INFO or higher.
            :param args: All formatted into a single string to be used as an info message.
    """
    if VERBOSE.value >= VerboseLevel.INFO.value:
        msg = _format_string_from_tuple(args)
        msg = text_format['info'] + text_header['info'] + msg + text_format['normal']
        print(msg)


def log_debug(*args):
    """
        Prints a message for debug information with a specific debug-format.
        Works if VERBOSE is DEBUG or higher.
            :param args: All formatted into a single string to be used as a debug message.
    """
    if VERBOSE.value >= VerboseLevel.DEBUG.value:
        msg = _format_string_from_tuple(args)
        msg = text_format['debug'] + text_header['debug'] + msg + text_format['normal']
        print(msg)


def log_frivolity(*args):
    """
        Prints a message for very detailed info about the program with a specific frivolity-format.
        Works if VERBOSE is FRIVOLOUS or higher.
            :param args: All formatted into a single string to be used as frivolity message.
    """
    msg = _format_string_from_tuple(args)
    msg = text_format['frivolous'] + text_header['frivolous'] + msg + text_format['normal']
    print(msg)


def _format_string_from_tuple(string_tuple):
    """
        Gets a tuple and formats it as a string
            :param string_tuple: tuple to be formatted into a string.
            :return: msg: string generated from the tuple.
    """
    msg = ''
    for arg in string_tuple:
        msg += str(arg) + ' '
    msg = msg[:-1]  # Get rid of the last space
    return msg
