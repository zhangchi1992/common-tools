import sys
import argparse
import pkg_resources

from difflib import get_close_matches
from show import Show
from search import Search
from upload import Upload

ACTIONS = {
    'show': Show,
    'search': Search,
    'upload': Upload,
}

INDENT = ' ' * 2
NEWLINE = '\n' + INDENT


def exit_due_to_invalid_action(suggest_actions=None):
    usage = NEWLINE + '%(prog)s <action> [parameters]\n\n' \
                + 'Here are valid actions:\n\n' \
                + INDENT + NEWLINE.join(ACTIONS.keys())

    if suggest_actions:
        usage += '\n\nInvalid action, maybe you meant:\n  ' \
                + NEWLINE.join(suggest_actions)

    parser = argparse.ArgumentParser(
        prog='disktool',
        usage=usage,
    )
    parser.print_help()
    sys.exit(-1)


def get_action(action):
    return ACTIONS.get(action)


def check_argument(args):
    if len(args) < 2:
        exit_due_to_invalid_action()

    if args[1].lower() in ('--version', '-v'):
        version = pkg_resources.require("disktool")[0].version
        print('disktool version %s' % version)
        sys.exit(0)

    action = args[1]
    if action not in ACTIONS.keys():
        suggest_services = get_close_matches(action, ACTIONS.keys())
        exit_due_to_invalid_action(suggest_services)


def main():
    args = sys.argv
    check_argument(args)
    action = get_action(args[1])
    action.main(args[2:])
