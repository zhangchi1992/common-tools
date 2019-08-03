#!/usr/bin/env python

from base import BaseAction
from utils.utils import explode_array
from utils.upload_info import upload_failed_disk


class Upload(BaseAction):
    action = 'Upload'
    command = 'upload'
    usage = '%(prog)s [options]'

    @classmethod
    def add_ext_arguments(cls, parser):
        parser.add_argument('-', '--url', dest='url',
                            action='store', type=str, default='',
                            help='request url')

        parser.add_argument('-t', '--timeout', dest='timeout',
                            action='store', type=str, default='5',
                            help='request timeout')

    @classmethod
    def build_directive(cls, options):
        return {
            'list_element': explode_array(options.list_element),
        }

    @classmethod
    def do_action(cls, options):
        url = options.url
        timeout = options.timeout
        upload_failed_disk(url, timeout)



