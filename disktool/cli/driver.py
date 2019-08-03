import sys
import argparse
from difflib import get_close_matches

from show_raid import show

ACTIONS = {
    'show': show,
    'search': search,
    'upload': upload,
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

    action = args[1]
    if action not in ACTIONS.keys():
        suggest_services = get_close_matches(action, ACTIONS.keys())
        exit_due_to_invalid_action(suggest_services)


def main():
    args = sys.argv
    check_argument(args)
    action = get_action(args[1])
    action(args[2:])
