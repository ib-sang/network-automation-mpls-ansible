#!/usr/bin/python3

import pprint
import subprocess
import sys


def sample(host, user):
    cmd = ["ansible-playbook",
           "-i {},".format(host),
           "-e ansible_user={}".format(user),
           "-e ANSIBLE_HOST_KEY_CHECKING=False",
           "ping-playbook.yaml",
           "-v"]

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
    sample("P1", "admin")