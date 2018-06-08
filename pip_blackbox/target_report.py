"""
Proof of concept
Inspect current python environment and write to file argv[1]
Output is JSON
"""

import json
import os
import platform
import site
import sys

try:
    import sysconfig
except ImportError:
    from distutils import sysconfig

def get_report():

    report = {}

    # Get Python implementation
    report['python_implementation'] = platform.python_implementation()
    report['python_version'] = platform.python_version()

    # Get prefixes from sys
    report['sys'] = {'prefix': getattr(sys, 'prefix', None),
                     'real_prefix': getattr(sys, 'real_prefix', None),
                     'base_prefix': getattr(sys, 'base_prefix', None)}

    # Get paths from sysconfig
    if hasattr(sysconfig, 'get_paths'):
        report['sysconfig'] = sysconfig.get_paths()
    else:
        paths = {'stdlib': sysconfig.get_python_lib(standard_lib=True),
                 'platstdlib': sysconfig.get_python_lib(standard_lib=True,
                                                        plat_specific=True),
                 'purelib': sysconfig.get_python_lib(),
                 'platlib': sysconfig.get_python_lib(plat_specific=True),
                 'include': sysconfig.get_python_inc(),
                 'platinclude': sysconfig.get_python_inc(plat_specific=True)}

        report['sysconfig'] = paths

    # Get site module directory
    report['site_mod_dir'] = os.path.dirname(os.path.abspath(site.__file__))

    # Get user site-packages directory
    try:
        # Use getusersitepackages if this is present
        # as it ensures that the value is initialized properly.
        report['user_site'] = site.getusersitepackages()
    except AttributeError:
        report['user_site'] = site.USER_SITE

    return report

if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.exit(2)

    with open(sys.argv[1], 'w+') as outfile:
        json.dump(get_report(), outfile)

