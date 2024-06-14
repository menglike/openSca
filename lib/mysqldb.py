import pymysql
from conf.config import Config

class MysqlDB():
    def __init__(self):
        host   =  Config.MYSQL_HOST
        user   = Config.MYSQL_USER
        passwd = Config.MYSQL_PASS
        dbname = Config.MYSQL_DB
        port   = Config.MYSQL_PORT
        try:
            self.db = pymysql.connect(host=host,user=user,password=passwd,database=dbname,port=port)
        except  Exception  as e:
            print('mysql error:'+str(e))
            exit()


    def query(self,sql):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        res = cursor.fetchall()
        self.db.close()
        return res

    def queryOne(self,sql):
        cursor = self.db.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        res = cursor.fetchone()
        self.db.close()
        return res

    def execute(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        num = cursor.rowcount
        self.db.commit()
        self.db.close()
        return num

    def get_last_id(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        last_id = cursor.lastrowid
        self.db.commit()
        self.db.close()
        return last_id