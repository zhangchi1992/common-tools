import urllib2
import json
import collections
import pkg_resources
import time
import shutil
import os

from utils import metric_print_smart_meta, metric_print
from diskinfo import diskinfo


def upload_to_url(url, timeout):
    headers = {'Content-Type': 'application/json'}
    failed_disk = diskinfo.get_failed_disk()
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(failed_disk))
    try:
        urllib2.urlopen(request, timeout=timeout)
    except ValueError as e:
        print e.message


Metric = collections.namedtuple('Metric', 'name labels value')


def collect_failed_disk_metrics():
    failed_disk = diskinfo.get_failed_disk().get('failed_disks')
    for sn, failed_info in failed_disk.iteritems():
        _, info = diskinfo.search_disk(sn)
        info = {
            'assessment': failed_info.get('assessment'),
            'sn': sn,
            'path': info.get('path'),
            'slot_number': info.get('slot_number')
        }
        yield Metric('failed_disk', info, True)


def upload_to_promether():
    with open('disktool.prob', 'w') as f:
        version_metric = Metric('disktool_run', {
            'version': pkg_resources.require("disktool")[0].version,
        }, int(time.time()))
        f.write(metric_print_smart_meta(version_metric, 'disktool_'))
        f.write(metric_print(version_metric, 'disktool_'))

        metrics = list(collect_failed_disk_metrics())
        metrics.sort(key=lambda i: i.name)

        previous_name = None
        for m in metrics:
            if m.name != previous_name:
                f.write(metric_print_smart_meta(m, 'disktool_'))
                previous_name = m.name
            f.write(metric_print(m, 'disktool_'))

    if os.path.isfile('disktool.prob'):
        srcfile = 'disktool.prob'
        dstfile = '/opt/Prometheus/node_exporter/textfiles/disktool.prob'
        shutil.move(srcfile, dstfile)



