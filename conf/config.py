import os

class Config():
    #配置opensca扫描器的路径
    SCAN_DIR  = os.path.dirname ( os.path.dirname( os.path.abspath(__file__) ) ) +'/tools/opensca-cli_v1.0.12_Darwin_x86_64'
    LOG_DIR   = os.path.dirname ( os.path.dirname( os.path.abspath(__file__) ) ) +'/static/scanlog/'

    #配置opensca的官网token
    token = ''

    #mysql配置
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASS = 'root'
    MYSQL_DB   = 'hawkeye2'

    #celery的配置
    broker  = "redis://127.0.0.1:6379/1"
    backend = "redis://127.0.0.1:6379/2"   

    

    
