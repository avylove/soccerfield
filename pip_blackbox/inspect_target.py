"""
Proof of concept
Call Python executable provided in argv[1] and retrieve JSON file
"""

import json
import os
import subprocess
import tempfile

import target_report

def get_report(python_exc):

    report = ''
    report_exc = os.path.abspath(target_report.__file__)
    if report_exc.endswith('.pyc'):
        report_exc = report_exc[:-1]

    try:
        report_out = tempfile.NamedTemporaryFile(delete=False)
        report_out.close()
        proc = subprocess.Popen((python_exc, '-E', report_exc, report_out.name))
        proc.communicate()
        if not proc.returncode:
            with open(report_out.name) as report_in:
                report = json.load(report_in)
    finally:
        os.unlink(report_out.name)

    return report

if __name__ == '__main__':

    from pprint import pprint
    import sys

    if len(sys.argv) < 2:
        sys.exit(2)

    pprint(get_report(sys.argv[1]))
