# -*- coding:utf-8 -*-

import pymysql
import re
import time
import requests
import urllib
import json
from apitest.models import *

HOSTNAME = '127.0.0.1'


def readSQLcase():
    
    list = Apitest.objects.all()
    
    sql = "select id,`apiname`,apiurl,apimethod,apiparamvalue,apiresult,`apistatus` from apitest_apistep " \
          "where apitest_apistep.Apitest_id=2"
    conn = pymysql.connect(user='root', db='autotest', passwd='test@123', host='127.0.0.1', charset='utf8')
    cursor = conn.cursor()
    info = cursor.fetchmany(cursor.execute(sql))
    print(f'info={info}')
    # interfaceTest([i for i in info])
    conn.commit()
    cursor.close()
    conn.close()


readSQLcase()


def interfaceTest(case_list):
    res_flags, request_urls, responses = [], [], []
    stringinfo, stringinfo1, stringinfo2 = re.compile('{TaskId}'), re.compile('{AssetId}'), re.compile('{PointId}')
    asseinfo = re.compile('{assetno}')
    tasknoinfo = re.compile('{taskno}')
    schemainfo = re.compile('{schema}')
    for case in case_list:
        try:
            case_id, interface_name, method, url, param, res_check = case[0], case[1], case[3], case[2], case[4], case[
                5]
        except Exception as e:
            return '测试用例格式不正确:%s' % e
        
        if param == '':
            new_url = f'http://api.test.com.cn{url}'
        elif param == 'null':
            new_url = f'http://{url}'
        else:
            url = stringinfo.sub(TaskId, url)
            param = stringinfo.sub(TaskId, param)
            param = tasknoinfo.sub(taskno, param)
            new_url = f'http://127.0.0.1{url}'
            request_urls.append(new_url)
        
        if method.upper() == 'GET':
            headers = {'Authorization': '', 'Content-Type': 'application/json'}
            data = None
            if '=' in urlParam(param):
                request_url = f'{new_url.encode("utf-8")}?{urlParam(param).encode("utf-8")}'
                print(f'{str(case_id)} request is get {request_url}')
                results = requests.get(request_url)
                responses.append(results)
                res = readRes(results, '')
            else:
                print(f'Request is get {new_url} body is {urlParam(param)}')
                req = urllib.request.Request(url=new_url, data=data, headers=headers, method='GET')
                results = urllib.request.urlopen(req).read()
                print(results)
                res = readRes(results, res_check)
            
            if 'pass' == res:
                writeResult(case_id, 1)
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, 0)
        
        elif method.upper() == 'PUT':
            headers = {'Host': HOSTNAME, 'Connection': 'keep-alive', 'CredentialId': id,
                       'Content-Type': 'application/json'}
            body_data = param
            results = requests.put(url=url, data=body_data, headers=headers)
            responses.append(results)
            res = readRes(results, res_check)
            if 'pass' == res:
                writeResult(case_id, 'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, 'fail')
                writeBug(case_id, interface_name, new_url, results, res_check)
        
        elif method.upper() == 'Post':
            headers = {'Authorization': 'Credential ' + id, 'Content-Type': 'application/json'}
            if '=' in urlParam(param):
                results = requests.patch(new_url + '?' + urlParam(param), None, headers=headers).text
                print(f'Response is post {results.encode("utf-8")}')
                responses.append(results)
                res = readRes(res, '')
            else:
                print(f'{str(case_id)} request is {new_url.encode("utf-8")} body is {urlParam(param).encode("utf-8")}')
                results = requests.post(new_url, data=urlParam(param).encode('utf-8'), headers=headers).text
                responses.append(results)
                res = readRes(res, res_check)
            if 'pass' == res:
                writeResult(case_id, '1')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, '0')
                writeBug(case_id, interface_name, new_url, results, res_check)
            try:
                TaskId(results)
            except:
                print('ok1')
        
        elif method.upper() == "PATCH":
            headers = {'Authorization': 'Credential ' + id, 'Content-Type': 'application/json'}
            data = None
            results = requests.patch(new_url + '?' + urlParam(param), data, headers=headers).text
            responses.append(results)
            res = readRes(results, res_check)
            if 'pass' == res:
                writeResult(case_id, 'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id, 'fail')
                writeBug(case_id, interface_name, new_url, results, res_check)
            try:
                preOrderSN(results)
            except:
                print('ok')


def credentialId():
    global id
    url = 'http://' + 'api.test.com.cn' + '/api/Security/Authentication/Signin/web'
    body_data = json.dumps({"Identity": 'test', "Password": 'test'})
    headers = {'Connection': 'keep-alive', 'Content-Type': 'application/json'}
    response = requests.post(url=url, data=body_data, headers=headers).text
    id = re.search('.*"CredentialId":"(.*)","Scene"', response).group(1)


def writeResult(case_id, result, value):
    result = result.encode("utf-8")
    now_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if value == 'step':
        sql = f'UPDATE apitest_apistep set apitest_apistep.apistatus={result},' \
            f'apitest_apistep.create_time={now_time} where apitest_apistep.id={case_id};'
    if value == 'case':
        sql = f'UPDATE apitest_apitest set apitest_apitest.apitestresult={result},' \
            f'apitest_apitest.create_time={now_time} where apitest_apitest.id={case_id};'
    print(f'api autotest result is {result.decode()}')
    
    pass


def writeBug(case_id, interface_name, new_url, results, res_check):
    pass


def readRes(res, res_check):
    res = res.decode().replace('";"', '=').replace('";', '=')
    res_check = res_check.split(';')
    for i in res_check:
        if i in res:
            pass
        else:
            return f'错误，返回参数和预期结果不一致{i}'
    return 'Pass'


def taskId(results):
    global TaskId
    regx = '.*"TaskId":(.*),"PlanId"'
    pm = re.search(regx, results)
    if pm:
        TaskId = pm.group(1).encode('utf-8')
        return TaskId
    return False


def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx, results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False


def taskNo():
    global taskno
    taskno = f'task_{str(int(time.time()))}'
    return taskno


def urlParam(param):
    return param.replace('&quot;', '"')
