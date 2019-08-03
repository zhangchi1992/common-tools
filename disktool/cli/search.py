#!/usr/bin/env python

from base import BaseAction
from utils.utils import explode_array
from utils.search_info import search_from_sn


class Search(BaseAction):
    action = 'Search'
    command = 'search'
    usage = '%(prog)s [options]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-s', '--serial_number', dest='sn',
                            action='store', type=str, default='',
                            help='search disk from sn')

    @classmethod
    def build_directive(cls, options):
        return {
            'sn': explode_array(options.sn),
        }

    @classmethod
    def do_action(cls, options):
        sn = options.sn
        search_from_sn(sn)


