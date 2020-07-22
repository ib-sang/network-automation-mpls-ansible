#!/usr/bin/python3

import pprint
import subprocess
import sys


def sample(host):
    cmd = ['ansible-playbook', 'ping-playbook.yml', '--extra-vars', 'host='+host ]

    proc = subprocess.Popen(cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            )

    try:
        outs, errs = proc.communicate(timeout=15)
        pprint.pprint(outs.decode().split('\n'))
    except subprocess.SubprocessError as errs:
        proc.kill()
        sys.exit("Error: {}".format(errs))

def main():
    sample("P1")