import sys
import os

from .commands.help import help
from .commands.newnet import newnet
from .commands.fork import fork
from .commands.merge import merge
from .commands.login import login
from .commands.logout import logout
from .commands.server_init import server_init
from .commands.pull import pull
from .commands.push import push
from .commands.add import add
from .commands.commit import commit
from .commands.init import init

from .commands.constants import config_path

class ManageUtil:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]

    def execute(self):

        if len(self.argv) > 1:

            subcommand = self.argv[1]

            if subcommand == 'login':
                login()

            if subcommand == 'logout':
                logout()

            if subcommand == 'newnet':
                newnet()

            if subcommand == 'fork':
                fork()

            if subcommand == 'merge':
                merge()

            if subcommand == 'upload':
                server_init()

            if subcommand == 'push':
                push()

            if subcommand == 'pull':
                pull()

            if subcommand == 'add':
                add()

            if subcommand == 'commit':
                commit()

            if subcommand == 'init':
                init()

            if subcommand == '-h' or subcommand == '--help':
                help()

        else:
            help()


def execute_from_command_line(argv=None):
    util = ManageUtil(argv)
    util.execute()
