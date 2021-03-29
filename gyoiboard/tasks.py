from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
import subprocess
from subprocess import PIPE


@shared_task
def executation(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    print('STDOUT: {}'.format(proc.stdout))
    return proc.stdout
