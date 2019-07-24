#!/usr/bin/env python

import json
import os
import re
from megacli import MegaCLI
from pySMART import DeviceList


class Tools(object):
    def __init__(self):
        self.cli = MegaCLI()
        self.dev_list = DeviceList()

    def adp_info(self):
        ret = {
            'num': '',
            'adps': {},
        }
        adps = self.cli.adapters()
        ret['num'] = len(adps)
        for adp in adps:
            pci_path = self.__get_adp_pci_info(adp['id'])
            ret['adps'][adp['id']] = {
                'virtual_drives': adp['virtual_drives'],
                'physical_devices': adp['physical_devices'],
                'pci_path': pci_path,
            }

        return ret

    def pd_info(self):
        ret = {
            'num': '',
            'pds': {},
        }
        drives = self.cli.physicaldrives()
        ret['num'] = len(drives)
        for drive in drives:
            ret['pds'][drive['device_id']] = {
                'firmware_state': drive['firmware_state'],
                'adapter_id': drive['adapter_id'],
                'slot_number': drive['slot_number'],
                'pd_type': drive['pd_type'],
                'media_type': drive['media_type'],
                'path': self.get_pd_path(drive),
                'ld_id': self.get_pd_raid_info(drive),
            }
        return ret

    def ld_info(self):
        ret = {
            'num': '',
            'lds': {},
        }
        drives = self.cli.logicaldrives()
        ret['num'] = len(drives)
        for drive in drives:
            ret['lds'][drive['id']] = {
                'adapter_id': drive['adapter_id'],
                'path': self.get_ld_path(drive['adapter_id'], drive['id'])
            }
            ret['lds'][drive['id']]['raid_level'] = self.__get_raid_type(drive['raid_level'], drive['span_depth'], drive.get('number_of_drives_per_span', None))
        return ret

    def get_pd_path(self, drive):
        pd_path = ''
        if drive.get('drive_position'):
            return "N/A"
        else:
            pci_path = self.adp_info()['adps'].get(drive['adapter_id']).get('pci_path')
            if pci_path:
                if drive.get('firmware_state') in ['jbod']:
                    disk_prefix = str('/dev/disk/by-path/pci-' + pci_path + '-scsi-0:0:')
                    diskpath = disk_prefix + str(drive['device_id']) + ':0'
                    if os.path.exists(diskpath):
                        pd_path = os.path.realpath(diskpath)
                    else:
                        pd_path = 'N/A'
        return pd_path

    @staticmethod
    def get_pd_raid_info(drive):
        if 'drive_position' in drive:
            ld_id = None
            position = drive.get('drive_position').split(',')
            for pos in position:
                if 'diskgroup' in pos:
                    ld_id = int(pos.split(':')[1])
                    break
            return ld_id
        else:
            return 'Unconfigured'

    def get_ld_path(self, adapter_id, drive_id):
        ld_path = ''
        pci_path = self.adp_info()['adps'].get(adapter_id).get('pci_path')
        if pci_path:
            disk_prefix = str('/dev/disk/by-path/pci-' + pci_path + '-scsi-0:')
            for j in range(1, 8):
                disk_path = disk_prefix + str(j) + ':' + str(drive_id) + ':0'
                if os.path.exists(disk_path):
                    ld_path = os.path.realpath(disk_path)
                    break
        else:
            ld_path = 'N/A'
        return ld_path

    @staticmethod
    def __get_raid_type(raid_level, span_depth, diskperspan):
        if raid_level == '':
            raid_type = str('N/A')
        else:
            if int(span_depth) >= 2:
                raid_type = str('RAID-' + str(raid_level) + '0')
            else:
                if raid_level == 1:
                    if diskperspan > 2:
                        raid_type = str('RAID-10')
                    else:
                        raid_type = str('RAID-' + str(raid_level))
                else:
                    raid_type = str('RAID-' + str(raid_level))
        return raid_type

    def __get_adp_pci_info(self, adp_id):
        bus_prefix = '0000'
        bus_num = ''
        dev_num = ''
        function_num = ''
        output_line = self.cli.execute('-AdpGetPciInfo -a{adp_id}'.format(adp_id=adp_id))
        for line in output_line:
            if re.match(r'^bus number.*:.*$', line.strip()):
                bus_num = str(line.strip().split(':')[1].strip()).zfill(2)
            if re.match(r'^device number.*:.*$', line.strip()):
                dev_num = str(line.strip().split(':')[1].strip()).zfill(2)
            if re.match(r'^function number.*:.*$', line.strip()):
                function_num = str(line.strip().split(':')[1].strip()).zfill(1)
        if bus_num:
            pci_path = str(bus_prefix + ':' + bus_num + ':' + dev_num + '.' + function_num)
            return str(pci_path)
        else:
            return None

    def device_info(self):
        ret = {
            'num': '',
            'devices': {},
        }
        for dev in self.dev_list.devices:
            if dev.interface.startswith('sat'):
                attributes = {}
                for attr in dev.attributes:
                    if attr is not None:
                        attributes[attr.num] = {
                            'name': attr.name,
                            'value': attr.value,
                            'worst': attr.worst,
                            'thresh': attr.thresh,
                            'type': attr.type,
                            'updated': attr.updated,
                            'when_failed': attr.when_failed,
                            'raw': attr.raw,
                        }
                ret['devices'][dev.serial] = {
                    'path': dev.path,
                    'serial': dev.serial,
                    'assessment': dev.assessment,
                    'attributes': attributes,
                }
        return ret

    def get_raid_info(self):
        ret = {
            'adapters': self.adp_info()['adps']
        }

        lds = self.ld_info()['lds']
        pds = self.pd_info()['pds']
        for pd_id, pd_info in pds.iteritems():
            if pd_info.get('ld_id') not in ['Unconfigured']:
                if 'pds' not in lds[pd_info.get('ld_id')]:
                    lds[pd_info.get('ld_id')]['pds'] = {}
                lds[pd_info.get('ld_id')]['pds'][pd_id] = pd_info
            else:
                if 'unconfigured_pds' not in ret['adapters'][pd_info['adapter_id']]:
                    ret['adapters'][pd_info['adapter_id']]['unconfigured_pds'] = {}
                ret['adapters'][pd_info['adapter_id']]['unconfigured_pds'][pd_id] = pd_info

        for ld_id, ld_info in lds.iteritems():
            if 'lds' not in ret['adapters'][ld_info['adapter_id']]:
                ret['adapters'][ld_info['adapter_id']]['lds'] = {}
            ret['adapters'][ld_info['adapter_id']]['lds'][ld_id] = ld_info

        return ret

    def all_info(self):



tools = Tools()
