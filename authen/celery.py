from __future__ import absolute_import   #解决命名问题

import os
import django

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','bbs.settings')   #blo是我的项目名
django.setup()

app = Celery('bbs')

app.config_from_object('django.conf:settings')    #制定celery配置文件
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)  #任务