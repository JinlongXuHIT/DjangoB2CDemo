from celery import Celery

import os
# 与manager.py 的environ 关联
if   not  os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'

# create celery application
app = Celery('meiduo') # 名称随意

# 导入celery config
app.config_from_object('celery_tasks.config')
# register celery []内为任务列表
app.autodiscover_tasks(['celery_tasks.sms'])