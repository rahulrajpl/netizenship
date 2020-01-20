# credits: https://stackoverflow.com/users/2650249/hoefling

import json
import urllib.request
import sys

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

from distutils.version import LooseVersion


def latest_version():
    name = sys.argv[1]
    installed_version = LooseVersion(version(name))

    # fetch package metadata from PyPI
    pypi_url = f'https://pypi.org/pypi/{name}/json'
    response = urllib.request.urlopen(pypi_url).read().decode()
    latest_version = max(LooseVersion(s) for s in json.loads(response)['releases'].keys())

    # print('package:', name, 'installed:', installed_version, 'latest:', latest_version)\
    return installed_version==latest_version

if not latest_version():
    print('Do you want to update to latest version?')