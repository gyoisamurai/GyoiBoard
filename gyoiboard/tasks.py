from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time


@shared_task
def add(x1, x2):
    time.sleep(10)
    y = x1 + x2
    print('処理完了')
    return y
