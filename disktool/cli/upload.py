#!/usr/bin/env python

from base import BaseAction
from utils.utils import explode_array
from utils.upload_info import upload_to_url, upload_to_promether


class Upload(BaseAction):
    action = 'Upload'
    command = 'upload'
    usage = '%(prog)s [options]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-d', '--destination', dest='destination',
                            action='store', type=str, default='',
                            help='request url')

        parser.add_argument('-t', '--timeout', dest='timeout',
                            action='store', type=str, default='5',
                            help='request timeout')

    @classmethod
    def build_directive(cls, options):
        return {
            'destination': explode_array(options.destination),
        }

    @classmethod
    def do_action(cls, options):
        destination = options.destination
        timeout = options.timeout
        if 'prometheus' in destination:
            upload_to_promether()
        else:
            upload_to_url(destination, timeout)



