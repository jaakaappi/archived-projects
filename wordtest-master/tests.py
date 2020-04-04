import wordtest
import unittest


class Tests(unittest.TestCase):
    def test_wrong_command_file_name(self):
        message, commands = wordtest.parse_commands('')
        assert message is "Could not parse command file : [Errno 2] No such file or directory: ''"
        assert commands is {}
