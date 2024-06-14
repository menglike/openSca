
import time,json,os
from scan import app
from celery.result import  AsyncResult
from conf.config import Config
from lib.mysqldb import MysqlDB

def isScanOver():
    sql = "select id,taskid,filename from scan where status=-1 "
    res = MysqlDB().query(sql)
    if res:
        for i in res:
            if i['filename']:
                    if os.path.exists(Config.LOG_DIR+'/'+i['filename']+'.html'):
                        print('已扫描出报告')
                        sql = "update scan set status=1 where id=%s "%(i['id'])
                        MysqlDB().execute(sql)
    else:
        print('没有找到扫描任务')
      

if __name__ == '__main__':
    try:
        isScanOver()
        # scheduler = BlockingScheduler()
        # #每分钟巡检一次
        # scheduler.add_job(isScanOver, 'interval',minutes=1)  
        # scheduler.start()
    except Exception as e:
        print(e)
