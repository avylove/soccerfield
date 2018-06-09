"""
Proof of concept
Call Python executable provided in argv[1] and retrieve JSON file
"""

import json
import os
import subprocess
import tempfile

import target_report

try:
    unicode
except NameError:
    HAS_UNICODE_TYPE = False
else:
    HAS_UNICODE_TYPE = True


def get_report(python_exc):

    report = ''
    report_exc = os.path.abspath(target_report.__file__)
    if report_exc.endswith('.pyc'):
        report_exc = report_exc[:-1]

    try:
        report_out = tempfile.NamedTemporaryFile(delete=False)
        report_out.close()

        # Sanitize environment
        env = os.environ.copy()
        for envvar in ('PYTHONPATH', 'PYTHONHOME'):
            if envvar in env:
                del env[envvar]

        # Escape arguments
        args = [python_exc, report_exc, report_out.name]

        if HAS_UNICODE_TYPE:
            sys_encoding = sys.getfilesystemencoding()
            for idx, arg in enumerate(args):
                if isinstance(arg, unicode):
                    args[idx] = args.encode(sys_encoding)

        proc = subprocess.Popen(args, env=env)
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
