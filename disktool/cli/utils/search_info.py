from diskinfo import diskinfo
from prettytable import PrettyTable


def search_from_sn(sn):
    device_id, info = diskinfo.search_disk(sn)
    pds_table = PrettyTable()
    pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
    id_info = 'a{adapter_id}l{ld_id}p{device_id}'.format(adapter_id=info.get('adapter_id'), ld_id=info.get('ld_id'),
                                                         device_id=device_id)
    pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                       info.get('path'), info.get('serial'), info.get('slot_number')])

    print '-- Disk {sn} Information --'.format(sn=sn)
    print pds_table
