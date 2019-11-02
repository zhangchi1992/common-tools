from diskinfo import diskinfo
from prettytable import PrettyTable


def show_adps():
    adp_info = diskinfo.adp_info()['adps']
    adapters_table = PrettyTable()
    adapters_table.field_names = ['ID', 'virtual_drives', 'physical_devices']
    for adp_id, info in adp_info.iteritems():
        adapters_table.add_row(['a{adp_id}'.format(adp_id=adp_id), info.get('virtual_drives'), info.get('physical_devices')])
    print '-- Adapter Information --'
    print adapters_table


def show_lds():
    lds_info = diskinfo.ld_info()['lds']
    lds_table = PrettyTable()
    lds_table.field_names = ['ID', 'raid_level', 'path']
    for ld_id, info in lds_info.iteritems():
        lds_table.add_row(['a{adapter_id}l{ld_id}'.format(adapter_id=info.get('adapter_id'), ld_id=ld_id),
                           info.get('raid_level'), info.get('path')])
    print '-- Logical Drive Information --'
    print lds_table


def show_pds():
    pds_info = diskinfo.pd_info()['pds']
    pds_table = PrettyTable()
    u_pds_table = PrettyTable()
    pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
    u_pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
    for device_id, info in pds_info.iteritems():
        if info.get('ld_id') not in ['Unconfigured']:
            id_info = 'a{adapter_id}l{ld_id}d{device_id}'.format(adapter_id=info.get('adapter_id'),
                                                             ld_id=info.get('ld_id'), device_id=device_id)
            pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                               info.get('path'), info.get('serial'), info.get('slot_number')])
        else:
            id_info = 'a{adapter_id}d{device_id}'.format(adapter_id=info.get('adapter_id'), device_id=device_id)
            u_pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                                 info.get('path'), info.get('serial'), info.get('slot_number')])

    print '-- Configured Physical Disk Information --'
    print pds_table
    print '-- Unconfigured Physical Disk Information --'
    print u_pds_table


def show_configured_disk():
    pds_info = diskinfo.pd_info()['pds']
    pds_table = PrettyTable()
    pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
    for device_id, info in pds_info.iteritems():
        if info.get('ld_id') not in ['Unconfigured']:
            id_info = 'a{adapter_id}l{ld_id}d{device_id}'.format(adapter_id=info.get('adapter_id'),
                                                             ld_id=info.get('ld_id'), device_id=device_id)
            pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                               info.get('path'), info.get('serial'), info.get('slot_number')])

    print '-- Configured Physical Disk Information --'
    print pds_table


def show_unconfigured_disk():
    pds_info = diskinfo.pd_info()['pds']
    u_pds_table = PrettyTable()
    u_pds_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'path', 'serial', 'slot_number']
    for device_id, info in pds_info.iteritems():
        if info.get('ld_id') in ['Unconfigured']:
            id_info = 'a{adapter_id}d{device_id}'.format(adapter_id=info.get('adapter_id'), device_id=device_id)
            u_pds_table.add_row([id_info, info.get('pd_type'), info.get('media_type'), info.get('firmware_state'),
                                 info.get('path'), info.get('serial'), info.get('slot_number')])
    print '-- Unconfigured Physical Disk Information --'
    print u_pds_table


def show_failed_disk():
    failed_disk = diskinfo.get_failed_disk()['failed_disks']
    attr_err = failed_disk.get('attr')
    state_err = failed_disk.get('state')
    for sn, info in attr_err.iteritems():
        print '-- Disk sn: {sn}, Assessment: {assessment} --'.format(sn=sn, assessment=info.get('assessment'))
        disk_table = PrettyTable()
        disk_table.field_names = ['num', 'name', 'type', 'when_failed']
        for num, attr in info.get('failed_attr', {}).iteritems():
            disk_table.add_row([num, attr.get('name'), attr.get('type'), attr.get('when_failed')])
        print disk_table

    for device_id, info in state_err.iteritems():
        print '-- Adapter: {adapter_id}, Device: {device_id}, firmware_state: {firmware_state} --'.\
            format(adapter_id=info.get('adapter_id'), device_id=device_id, firmware_state=info.get('firmware_state'))
        disk_table = PrettyTable()
        disk_table.field_names = ['ID', 'pd_type', 'media_type', 'firmware_state', 'slot_number']
        id_info = 'a{adapter_id}d{device_id}'.format(adapter_id=info.get('adapter_id'), device_id=device_id)
        disk_table.add_row([id_info, info.get('pd_type'), info.get('media_type'),
                            info.get('firmware_state'), info.get('slot_number')])

