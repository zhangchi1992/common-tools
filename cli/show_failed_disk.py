#!/usr/bin/env python

from base.tools import tools
from prettytable import PrettyTable

failed_disk = tools.get_failed_disk()['failed_disks']
for sn, info in failed_disk.iteritems():
    print '-- Disk sn: {sn}, Assessment: {assessment} --'.format(sn=sn, assessment=info.get('assessment'))
    disk_table = PrettyTable()
    disk_table.field_names = ['id', 'name', 'type', 'when_failed']
    disk_table.add_row([info.get('id'), info.get('name'), info.get('type'), info.get('when_failed')])
    print disk_table


