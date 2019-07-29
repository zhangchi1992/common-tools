#!/usr/bin/env python

import sys
sys.path.append("..")

from base.tools import tools
from prettytable import PrettyTable

adp_info = tools.adp_info()['adps']
adapters_table = PrettyTable()
adapters_table.field_names = ['ID', 'virtual_drives', 'physical_devices']
for adp_id, info in adp_info.iteritems():
    adapters_table.add_row(['a{adp_id}'.format(adp_id=adp_id), info.get('virtual_drives'), info.get('physical_devices')])
print '-- Adapter Information --'
print adapters_table


lds_info = tools.ld_info()['lds']
lds_table = PrettyTable()
lds_table.field_names = ['ID', 'raid_level', 'path']
for ld_id, info in lds_info.iteritems():
    lds_table.add_row(['a{adapter_id}l{ld_id}'.format(adapter_id=info.get('adapter_id'), ld_id=ld_id),
                       info.get('raid_level'), info.get('path')])
print '-- Logical Drive Information --'
print lds_table


pds_info = tools.pd_info()['pds']
pds_table = PrettyTable()
u_pds_table = PrettyTable()
pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
u_pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
for pd_id, info in pds_info.iteritems():
    if info.get('ld_id') not in ['Unconfigured']:
        id_info = 'a{adapter_id}l{ld_id}p{pd_id}'.format(adapter_id=info.get('adapter_id'),
                                                         ld_id=info.get('ld_id'), pd_id=pd_id)
        pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                           info.get('path'), info.get('serial'), info.get('slot_number')])
    else:
        id_info = 'a{adapter_id}p{pd_id}'.format(adapter_id=info.get('adapter_id'), pd_id=pd_id)
        u_pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                             info.get('path'), info.get('serial'), info.get('slot_number')])

print '-- Physical Disk Information --'
print pds_table
print '-- Unconfigured Physical Disk Information --'
print u_pds_table







