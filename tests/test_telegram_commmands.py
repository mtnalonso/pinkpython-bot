import unittest
import pytest

from channels.telegram_commands import run_command, __exec_command

class TestTelegramCommands(unittest.TestCase):

    def test_run_command(self):
        assert 10 == run_command('4+6')
        assert 'foo\n' == run_command('print("foo")')
