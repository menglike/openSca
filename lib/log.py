import os,time
from conf.config import  Config

class Log:

    def __init__(self,type,cloud):
        #判断日志目录是否存在
        if not os.path.exists(Config.LOG_DIR+'/'+type):
            os.mkdir(Config.LOG_DIR+'/'+type)

        datedir = time.strftime("%Y-%m-%d",time.localtime())
        self.datedir = Config.LOG_DIR+'/'+type+'/'+datedir

        if not os.path.exists(self.datedir):
            os.makedirs(self.datedir)

        self.cloud = cloud+'.log'


    def save(self,content):
        print(content+"\n")
        with open( self.datedir+'/'+self.cloud ,'a+') as f:
            f.write(content+'\n')


