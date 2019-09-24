# -*-coding=utf-8-*-

# @Time : 2019/5/20 14:46
# @File : base_access.py
import base64
import re

import requests
import datetime
import time
from requests.cookies import RequestsCookieJar, create_cookie


class CookiesUtil(object):

    def __init__(self, ck=None):
        self.cookies = ck

    def to_list(self):

        return [(c.name, c.value, c.path) for c in self.cookies]

    def to_file(self, filename='cookies.txt'):
        cookies_list = self.to_list()

        with open(filename, 'w') as f:
            for c in cookies_list:
                f.write(str(c[0] + '=' + c[1] + '=' + c[2]) + '\n')

    def read_cookies(self, filename='cookies.txt'):

        cookiesjar = RequestsCookieJar()

        with open(filename, 'r') as f:
            for c in f:
                _c = c.strip().split('=')
                cookiesjar.set_cookie(create_cookie(_c[0], _c[1], path=_c[2]))

        return cookiesjar


def visit_web_origin():
    session = requests.Session()

    code_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/paramRewriter-paramEncode.shtml'
    code_headers = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    # d = int(time.time() * 1000)
    #
    # param_data = {
    #     'params': 'd={}'.format(d)
    # }
    #
    # param_sess = session.post(url=code_url, headers=code_headers, data=param_data)
    #
    # param_json = param_sess.json()
    #
    # # print(param_json)
    #
    # params_str = param_json.get('params')

    img_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/login-showPic.shtml'

    img_headers = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "image/webp,*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Connection": "keep-alive",
    }

    img = session.get(url=img_url, headers=img_headers)


    login_headers = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "keep-alive",
        # "Cookie": "JSESSIONID=xJHUPdqTGnWIfdthHkfpVE67305lUvQA26gG5eZOvmG85ObBdFCd!282725381!1490154843; avoid_declare=declare_pass",
        "Upgrade-Insecure-Requests": "1",
    }

    # code = input('输入验证码')
    Crack_code_URL = 'http://127.0.0.1:6667/cnipa'
    img_b64 = base64.b64encode(img.content)

    img_dict = {'img': img_b64}
    res = requests.post(Crack_code_URL, data=img_dict, verify=False, timeout=4)

    code = res.json().get('code')


    check_login_header = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
    }

    check_login_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/checkLoginTimes-check.shtml'

    # 看看这个数据是不是会变的
    check_login_data1 = {
        'username': 'TVcyYXJKZHFGVHFwRU9qNyt1RitCSDhuMXZ0QmVvMEZzUmhzOUlYKytZazFZbXFCZHRRMUM5OG0xQmxWTXhGWEZENWMvNWpaaUFXNFM3UGxuTENFcUNnSXB6NDJmQUYrMVdSYjFpZDI5NWs5TGxZNTZ6dW5wY3p1VkxrTktPbVpGNW8yc05yU3hma01UQVM5a0toQkphYW5TMytrbERtVkVDbnhzZVZhY3hnPQ'
    }

    try:
        s2 = session.post(url=check_login_url, headers=check_login_header, data=check_login_data1)
    except Exception as e:
        print(e)

    # print(dict(s2.cookies))

    check_user_status = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-checkUserState.shtml'
    check_user_data = {
        'userName': 'TVcyYXJKZHFGVHFwRU9qNyt1RitCSDhuMXZ0QmVvMEZzUmhzOUlYKytZazFZbXFCZHRRMUM5OG0xQmxWTXhGWEZENWMvNWpaaUFXNFM3UGxuTENFcUNnSXB6NDJmQUYrMVdSYjFpZDI5NWs5TGxZNTZ6dW5wY3p1VkxrTktPbVpGNW8yc05yU3hma01UQVM5a0toQkphYW5TMytrbERtVkVDbnhzZVZhY3hnPQ'
    }

    check_status_headers = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",

    }

    try:
        s3 = session.post(url=check_user_status, headers=check_status_headers, data=check_user_data)
    except Exception as e:
        print(e)
    else:
        print(s3.text)

    # print(dict(s3.cookies))
    update_cookie_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/sessionDeBugAC.do'

    cookies = dict(s3.cookies).get('WEE_SID')

    udpate_cookie_data = {
        'sessionDebugMod.opttype': 'login',
        'sessionDebugMod.position': 'keepalive',
        'sessionDebugMod.broswer': 'Netscape5.0 (Windows)',
        'sessionDebugMod.userName': 'xlzx_2019',
        'sessionDebugMod.cur_wee_sid': cookies,
        'sessionDebugMod.wee_sid': cookies,
    }

    cookie_headers = {
        "Host": "pss-system.cnipa.gov.cn",
        "User-Agent": "Mozilla/5.0 (Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
        "Content-type": "application/x-www-form-urlencoded",
    }
    # 这个也不是必须的
    try:
        ss = session.post(url=update_cookie_url, headers=cookie_headers, data=udpate_cookie_data)
    except Exception as e:
        print(e)

    login_data = {
        'j_loginsuccess_url': '',
        'j_validation_code': str(code),
        'j_username': 'TVcyYXJKZHFGVHFwRU9qNyt1RitCSDhuMXZ0QmVvMEZzUmhzOUlYKytZazFZbXFCZHRRMUM5OG0xQmxWTXhGWEZENWMvNWpaaUFXNFM3UGxuTENFcUNnSXB6NDJmQUYrMVdSYjFpZDI5NWs5TGxZNTZ6dW5wY3p1VkxrTktPbVpGNW8yc05yU3hma01UQVM5a0toQkphYW5TMytrbERtVkVDbnhzZVZhY3hnPQ==',
        'j_password': 'T2VZcUh2c1BXMWZLc1hYcVhnK2dLYjdycG9hMU1VOHk1SkU1NGliNjdlSnNvRGVuVzI2N0tZbXZyQVllL3c3aFpmRFovS1FodU83Q3J2UlRIRUlOdkc4TGViblZCWFE2VzRDU2ZEV2Q2UlhIeE9nbnA3bEl3Qk9ydUJieFd4WGhPU0txalUvLzI3cy9zTWRQc0FFc1p1VzR3N25VMXJIYlEvR1loRXhTNGZVPQ==',
    }
    login_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/wee/platform/wee_security_check?v=20190520'

    try:
        code_sess = session.post(url=login_url, headers=login_headers, data=login_data)
    except Exception as e:
        print(e)
        exit()

    else:
        if 'xlzx_2019，欢迎访问' in code_sess.text:
            print('登陆成功')
            print('打印cookies')
            # cj = requests.utils.dict_from_cookiejar(session.cookies)
            cookies = session.cookies
            ck_tool = CookiesUtil(cookies)
            ck_tool.to_file()

        else:
            print('登陆失败')
            exit()

    test_headers = {
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Host": "pss-system.cnipa.gov.cn",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
    }
    test_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uiIndex.shtml'
    r1 = session.get(url=test_url, headers=test_headers)
    print('r1', r1.status_code)

    # 先注释
    apply_id = 'CN201910259741'

    search_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
        # "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "WEE_SID=xJHUPdqTGnWIfdthHkfpVE67305lUvQA26gG5eZOvmG85ObBdFCd!282725381!1490154843!1558338984595;",
        "Host": "pss-system.cnipa.gov.cn",
        "Origin": "http://pss-system.cnipa.gov.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "User-Agent": "Mozilla/5.0 (Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0529-executeCommandSearch.shtml'

    post_data = {
        'searchCondition.searchExp': '申请号=({}+)'.format(apply_id),
        'searchCondition.dbId': 'VDB',
        'searchCondition.searchType': 'Sino_foreign',
        "searchCondition.extendInfo['MODE']": 'MODE_TABLE',
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        'searchCondition.originalLanguage': '',
        'searchCondition.targetLanguage': '',
        'wee.bizlog.modulelevel': '0200201',
        'resultPagination.limit': '12',
    }

    try:
        r = session.post(
            url=url,
            headers=search_headers,
            data=post_data,
        )

    except Exception as e:
        print(e)

    else:
        print('status code\t', r.status_code)

        js_data = r.json()
        #
        result_list = js_data.get('searchResultDTO', {}).get('searchResultRecord', [])
        name_list = []
        for item in result_list:
            fieldMap = item.get('fieldMap', {})
            name = fieldMap.get('PAVIEW')

            if name:
                name = re.sub(';', '', name)

            else:
                name = ''

            name_list.append(name)

        print(name_list)

def visit_web_modify():
    session = requests.Session()

    cookiesjar = CookiesUtil().read_cookies()

    test_headers = {
        "User-Agent": "Mozilla/5.0 (; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Connection": "keep-alive",
        "Host": "pss-system.cnipa.gov.cn",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uilogin-forwardLogin.shtml",
    }

    test_url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/portal/uiIndex.shtml'
    # r1 = session.get(url=test_url, headers=test_headers,cookies=cookiesjar)

    # print('r1', r1.status_code)
    # print(r1.text)
    # print(r1.cookies)

    # 先注释
    apply_id = 'CN201910259741'

    search_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh,en;q=0.9,en-US;q=0.8,zh-CN;q=0.7",
        # "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Cookie": "WEE_SID=xJHUPdqTGnWIfdthHkfpVE67305lUvQA26gG5eZOvmG85ObBdFCd!282725381!1490154843!1558338984595;",
        "Host": "pss-system.cnipa.gov.cn",
        "Origin": "http://pss-system.cnipa.gov.cn",
        "Pragma": "no-cache",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://pss-system.cnipa.gov.cn/sipopublicsearch/patentsearch/tableSearch-showTableSearchIndex.shtml",
        "User-Agent": "Mozilla/5.0 (Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/patentsearch/executeTableSearch0529-executeCommandSearch.shtml'

    post_data = {
        'searchCondition.searchExp': '申请号=({}+)'.format(apply_id),
        'searchCondition.dbId': 'VDB',
        'searchCondition.searchType': 'Sino_foreign',
        "searchCondition.extendInfo['MODE']": 'MODE_TABLE',
        "searchCondition.extendInfo['STRATEGY']": "STRATEGY_CALCULATE",
        'searchCondition.originalLanguage': '',
        'searchCondition.targetLanguage': '',
        'wee.bizlog.modulelevel': '0200201',
        'resultPagination.limit': '12',
    }

    try:
        r = session.post(
            url=url,
            headers=search_headers,
            data=post_data,
            cookies=cookiesjar
        )

    except Exception as e:
        print(e)

    else:
        print('status code\t', r.status_code)

        js_data = r.json()
        #
        result_list = js_data.get('searchResultDTO', {}).get('searchResultRecord', [])
        name_list = []
        for item in result_list:
            fieldMap = item.get('fieldMap', {})
            name = fieldMap.get('PAVIEW')

            if name:
                name = re.sub(';', '', name)

            else:
                name = ''

            name_list.append(name)

        print(name_list)


visit_web_modify()
# visit_web_origin()