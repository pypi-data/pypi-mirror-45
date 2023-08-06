# vim: set fenc=utf8 ts=4 sw=4 et :
from pdml2flow.plugin import Plugin2
from pdml2flow.conf import Conf
from pdml2flow.logging import *
from argparse import ArgumentParser

from dict2xml import dict2xml

argparser = ArgumentParser('XML output')
argparser.add_argument(
    '-0',
    dest='PRINT_0',
    action='store_true',
    help='Terminates lines with null character'
)

class XMLOutput(Plugin2):

    @staticmethod
    def help():
        """Return a help string."""
        return argparser.format_help()

    def __init__(self, *args):
        self.conf = vars(
            argparser.parse_args(args)
        )
        debug(
            '{}: {}'.format(
                self.__class__.__name__,
                self.conf
            )
        )

    def flow_end(self, flow):
        print(
            dict2xml({
                'flow': flow.frames
            }),
            end=('\n' if not self.conf['PRINT_0'] else '\n\0'),
            file=Conf.OUT
        )

if __name__ == '__main__':
    print(XMLOutput.help())
