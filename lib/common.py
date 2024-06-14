from cmath import log
from flask import request
from conf.config import Config
import time,requests,json,os,re,hashlib
from lib.mysqldb import MysqlDB
from lib.log import Log
from  importlib import import_module


def _getDatetimeStr():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())

def _getDateInt():
    return int(time.time())

def _getTimeStr():
    return time.strftime('%Y-%m-%d', time.localtime())


def _getRequestParams(param_list, type='form', filter=True, exclude=[]):
    page = request.args.get('page', 1)
    pagenum = request.args.get('perPage', 10)

    request_param = {}
    request_param['page'] = int(page)
    request_param['pagenum'] = int(pagenum)

    # .-@:
    bad_word = ["\"", "\\", "'", "=", "#", ";", "<", ">", "%", "$", "(", ")", "&", "!", "~", '^', '*', '/', '+']

    if type == 'form':
        if param_list:
            for i in param_list:
                if request.method == 'POST':
                    tmp = request.form.get(i, '').strip()

                    if tmp == '':
                        tmp = request.args.get(i, '').strip()

                if request.method == 'GET':
                    tmp = request.args.get(i, '').strip()

                for j in bad_word:

                    if exclude and i in exclude:
                        continue

                    tmp = tmp.replace(j, '')

                request_param[i] = tmp

    if type == 'json' and filter == True:
        tmp = json.loads(request.get_data(as_text=True))
        print(tmp)
        for k, v in tmp.items():
            if isinstance(v, dict):
                request_param[k] = v
            else:
                v = str(v).strip()
                if k not in exclude:
                    for j in bad_word:
                        v = v.replace(j, '')

                request_param[k] = v
    if type == 'json' and filter == False:
        tmp = json.loads(request.get_data(as_text=True))

        for k, v in tmp.items():
            if isinstance(v, str):
                request_param[k] = v.replace("'", '"')
            else:
                request_param[k] = v

    return request_param

def getTodayStamp():
    timestr = time.strftime('%Y-%m-%d', time.localtime())+' 00:00:00'
    timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp

def _dateStrToInt(timestr):
    timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")
    # 转换为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def add_plan(product,target,task_id):
    try:
        print('~~~~~~~~~~~~~')
       
        #如果是检测脚本
        #导入检测脚本
        PASSWORD_DIC =['123123','123456','root']
        for i in target.strip('\n\r').split("\n"):
            #i: 192.168.10.122:6379
            ip = i.split(':')[0]
            port = i.split(':')[1]
            # print(ip,port)

            checkDir = Config.LOG_DIR + '/check/' + product+'/'
            if not os.path.exists(checkDir):
                print('-目录不存在:'+ checkDir)
                os.makedirs(checkDir)

            #如果是检测脚本
            if os.path.exists(Config.VUL_DIR+'/'+product+'.py'):
                cmdstr = Config.python2+" "+Config.VUL_DIR+'/'+product+'.py '+ip+' '+str(port)
                result = os.popen(cmdstr).read()
                print(result)
                if result != None:
                    #发现异常
                    sql = "insert into task_result(task_id,result,create_time,create_date,info) values(%s,'%s',%s,'%s','%s')"%(task_id,result,_getDateInt(),_getDatetimeStr(),i)
                    MysqlDB().execute(sql)
                    
                
                resultstr = ''
                if result!=None:
                    
                    # print( requests.post(Config.fs_alert_url,data=json.dumps({'msg_type':"text","content":{'text':i+'|'+result}}),headers={'Content-Type':'application/json'},verify=False) )
                    resultstr = result
            
            #如果是检测json
            if os.path.exists(Config.VUL_DIR+'/'+product+'.json'):
                print(Config.VUL_DIR+'/'+product+'.json')
                with open (Config.VUL_DIR+'/'+product+'.json','r') as f:
                    data = json.loads(f.read())
                an_type = data['plugin']['analyzing']
                analyzingdata = data['plugin']['analyzingdata']
                url = data['plugin']['url']
                res_html = requests.get('http://'+i+url).text

                resultstr = None
                if an_type == 'keyword':
                    if analyzingdata in res_html:
                        resultstr = data['plugin']['tag']
                elif an_type == 'regex':
                    if re.search(analyzingdata, res_html, re.I):
                        resultstr = data['plugin']['tag']
                elif an_type == 'md5':
                    md5 = hashlib.md5()
                    md5.update(res_html)
                    if md5.hexdigest() == analyzingdata:
                        resultstr = data['plugin']['tag']
                
                if resultstr != None:
                    # print( requests.post(Config.fs_alert_url,data=json.dumps({"msg_type":"text","content":{'text':i+'|'+resultstr}}),headers={'content-type':'application/json'},verify=False).json()  )
                    #发现异常
                    sql = "insert into task_result(task_id,result,create_time,create_date,info) values(%s,'%s',%s,'%s','%s')"%(task_id,resultstr,_getDateInt(),_getDatetimeStr(),i)
                    MysqlDB().execute(sql)
              

            with open(checkDir+str(task_id)+'.log','a') as f:
                f.write('time:['+_getDatetimeStr()+'],target:['+i+'],result:['+resultstr.strip('\n\r')+"]\n")
        
    except Exception as e:
        print(e)


def str_to_week(num):
    if num == 1:
        return '-'
    if num == 2:
        return '二'
    if num == 3:
        return '三'
    if num == 4:
        return '四'
    if num == 5:
        return '五'
    if num == 6:
       return '六'
    if num == 7:
        return '日'

def str_to_day(num):
    if num == 'day':
        return '天'
    if num == 'week':
        return '周'
    if num == 'month':
        return '月'
    if num == 'hour':
        return '时'
    if num == 'minute':
        return '分'
    if num == 'second':
        return '秒'