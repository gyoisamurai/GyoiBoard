from __future__ import absolute_import, unicode_literals
from celery import shared_task

import time
import subprocess
from subprocess import PIPE


@shared_task
def add(x1, x2):
    time.sleep(10)
    y = x1 + x2
    print('処理完了')
    return y


@shared_task
def executation(command):
    proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE, text=True)
    print('STDOUT: {}'.format(proc))
    return proc.stdout
