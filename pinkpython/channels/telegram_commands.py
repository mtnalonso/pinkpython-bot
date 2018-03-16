import logging
import sys
from io import StringIO
import contextlib
from imp import find_module


logger = logging.getLogger(__name__)


def get_documentation(module_name):
    logger.info(module_name)
    try:
        documentation = __get__doc_from_module_name(module_name)
        return documentation
    except ImportError:
        return str('HEY I DONNOT KNOW BOUT THAT BRO')
    except KeyError as error:
        return str('Sorry, I couldn\'t find info for {}'.format(module_name))


def __get__doc_from_module_name(module_name):
    find_module(module_name)
    exec('import {}'.format(module_name))
    return eval(module_name).__doc__


def attack_command():
    return "(YOU DON'T HAVE ENOUGH GYM BADGES TO PERFORM THIS ACTION)"


def run_command(command):
    logger.info(command)
    try:
        return __exec_command(command) or eval(command)
    except:
        return 'DONNOT FUOL ME'


def __exec_command(command):
    with stdoutIO() as s:
        exec(command)
    return s.getvalue()


@contextlib.contextmanager
def stdoutIO():
    sys.stdout = output = StringIO()
    yield output
    sys.stdout = sys.__stdout__
