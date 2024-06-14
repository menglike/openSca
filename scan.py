from celery  import Celery
from celery  import platforms
from conf.config import Config
import os

app = Celery('scan',broker=Config.broker,backend=Config.backend)
#允许root执行
platforms.C_FORCE_ROOT = True

@app.task
def add_scan(cmd_str):
    try:
        os.system(cmd_str)
        print("scan end----")
    except Exception as e:
        return e
