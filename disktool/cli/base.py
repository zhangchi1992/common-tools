import sys
from argparse import ArgumentParser


class BaseAction(object):

    action = ''
    command = ''
    usage = ''
    description = ''

    @classmethod
    def get_argument_parser(cls):
        parser = ArgumentParser(
                prog='disktool %s' % cls.command,
                usage=cls.usage,
                description=cls.description
                )

        cls.add_ext_arguments(parser)
        return parser

    @classmethod
    def add_ext_arguments(cls, parser):
        pass

    @classmethod
    def build_directive(cls, options):
        return None

    @classmethod
    def do_action(cls, options):
        return None

    @classmethod
    def main(cls, args):
        parser = cls.get_argument_parser()
        options = parser.parse_args(args)

        directive = cls.build_directive(options)
        if directive is None:
            parser.print_help()
            sys.exit(-1)

        cls.do_action(options)


