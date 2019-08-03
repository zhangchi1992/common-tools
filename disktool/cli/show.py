#!/usr/bin/env python

from base import BaseAction
from utils.utils import explode_array
from utils.show_info import show_adps, show_lds, show_pds, show_configured_disk, show_unconfigured_disk, show_failed_disk


class Show(BaseAction):

    show_list = {
        'adp': show_adps,
        'ld': show_lds,
        'pd': show_pds,
        'cd': show_configured_disk,
        'ud': show_unconfigured_disk,
        'fd': show_failed_disk,
    }

    action = 'Show'
    command = 'show'
    usage = '%(prog)s [options] \n\n' + 'Here are valid actions:\n\n' +  "\n".join(show_list.keys())

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-l', '--list', dest='list_element',
                            action='store', type=str, default='raid',
                            help='list disk info what you want')

    @classmethod
    def build_directive(cls, options):
        return {
            'list_element': explode_array(options.list_element),
        }

    @classmethod
    def do_action(cls, options):
        list_element = options.list_element
        if 'raid' in list_element:
            cls.show_list['adp']()
            cls.show_list['ld']()
            cls.show_list['pd']()
        elif list_element in cls.show_list.keys():
            cls.show_list.get(list_element)()


