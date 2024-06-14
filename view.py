import json,os,time,random
import requests
import urllib3
from flask import request, Blueprint, render_template,make_response,send_from_directory
from conf.config import Config
from lib.mysqldb import MysqlDB
from lib.common import _getDatetimeStr,_getDateInt,_getRequestParams
from scan import add_scan

urllib3.disable_warnings()


path = Blueprint('path', __name__)


@path.route('/index', methods=['GET', "POST"])
def index():
    return render_template("index.html")


@path.route('/scan', methods=['GET', "POST"])
def scan():
    path = request.form.get('path') 
    token = Config.token 
    filename =time.strftime('%Y%m%d%H%M%S',time.localtime())

    cmd_str = Config.SCAN_DIR+'/opensca-cli -path '+path +" -out "+ Config.LOG_DIR+'/'+filename+'.html '
    if token:
        cmd_str += "-token "+token
    if not os.path.exists(path):
        return json.dumps({"msg":"路径不存在","status":100})

    print(cmd_str)
    # os.system(cmd_str)
    try:
        taskid = add_scan.delay(cmd_str)
        print(taskid)
        sql = "insert into scan(path,filename,create_time,create_date,taskid) values('%s','%s','%s','%s','%s')"%(path,filename,_getDateInt(),_getDatetimeStr(),taskid)
        num = MysqlDB().execute(sql)
        if num>0:
            data = {
                'status': 0,
                "msg":"开启扫描成功"
            }
        else:
            data = {
                'status': 100,
                "msg":"开启扫描失败"
            }
        return json.dumps(data)
    except Exception as e:
        print(sql)
        return json.dumps({'msg':str(e),'status':100})



@path.route('/search', methods=['get',"POST"])
def search():
    param = ['app_name']
    req_param = _getRequestParams(param)
    page = req_param['page']
    pagenum = req_param['pagenum']

    where = []
    if req_param['app_name']:
        where.append("a.app_name like '%" + req_param['app_name'] + "%'")
   
    if where:
        where = 'where ' + ' and '.join(where)
    else:
        where = ''

    sql = " SELECT id,path,filename,create_time,status,taskid,status FROM scan %s limit %s,%s"%(where, str((int(page) - 1) * pagenum), str(pagenum))
    
    print(sql)
    res = MysqlDB().query(sql)
    sql = "select count(*) as num from scan a %s  " % (where)
    rows = MysqlDB().query(sql)
    data = {
        'status': 0,
        "data": {
            "rows": res,
            "count": rows[0]['num']
        },
    }
    return json.dumps(data)


@path.route('/download', methods=[ 'get'])
# @isLogin
def download():
    param = ['filename']
    req_param = _getRequestParams(param,'form',True,['filename'])
    if not os.path.exists(Config.LOG_DIR+'/'+req_param['filename']+'.html'):
        print(Config.LOG_DIR+'/'+req_param['filename']+'.html')
        return json.dumps({'msg':Config.LOG_DIR+'/'+req_param['filename']+'.html'+" 文件不存在",'status':100})
    else:
        response = make_response(send_from_directory(Config.LOG_DIR, req_param['filename']+'.html', as_attachment=True))
        return response

@path.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']
        token = Config.token
        base_path = os.path.abspath(os.getcwd())
        filename = generate_random_str() +'_'+f.filename
        upload_path = os.path.join(base_path,'static/uploads/',filename)
        f.save(upload_path)

        cmd_str = Config.SCAN_DIR+'/opensca-cli -path '+upload_path +" -out "+ Config.LOG_DIR+'/'+filename+'.html '
        if token:
            cmd_str += "-token "+token
        if not os.path.exists(upload_path):
            return json.dumps({"msg":"路径不存在","status":100})

        print(cmd_str)
        # os.system(cmd_str)
        try:
            taskid = add_scan.delay(cmd_str)
            print(taskid)
            sql = "insert into scan(path,filename,create_time,create_date,taskid) values('%s','%s','%s','%s','%s')"%(upload_path,filename,_getDateInt(),_getDatetimeStr(),taskid)
            num = MysqlDB().execute(sql)
            if num>0:
                data = {
                    'status': 0,
                    "msg":"ok",
                    "data":{
                        "filename":filename,
                        "url":"/static/uploads/"+filename
                    }
                }
            else:
                data = {
                    'status': 100,
                    "msg":"开启扫描失败"
                }
            return json.dumps(data)
        except Exception as e:
            print(sql)
            return json.dumps({'msg':str(e),'status':100})
            
                    
        
def generate_random_str(randomlength=16):
    """
    生成一个指定长度的随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str