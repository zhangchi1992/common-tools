import urllib2
import json
from diskinfo import diskinfo


def upload_failed_disk(url, timeout):
    headers = {'Content-Type': 'application/json'}
    failed_disk = diskinfo.get_failed_disk()
    request = urllib2.Request(url=url, headers=headers, data=json.dumps(failed_disk))
    urllib2.urlopen(request, timeout=timeout)

