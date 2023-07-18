import unittest
from unittest.mock import MagicMock
from modules import cmd

class TestCmd(unittest.TestCase):
    def setUp(self):
        self.bot = MagicMock()
        self.cog = cmd.Cmd(self.bot)

    def test_ping(self):
        ctx = MagicMock()
        self.cog.ping(ctx)
        ctx.send.assert_called_once_with('pong')


if __name__ == '__main__':
    unittest.main()