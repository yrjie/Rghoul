#!/usr/local/bin/python3

import sys, os
import requests
import getpass
from requests_ntlm import HttpNtlmAuth
import shutil
import json
import time
import datetime
import html.parser

if len(sys.argv)<2:
    print('Usage: infile')
    print('\ninfile format: floor picid')
    exit(1)

def downloadPic(s, floor, picId):
    picurl = urlPic % (floor, picId)
    print(picurl)
    pic = s.get(picurl, stream=True)
    src = 'static/images/%d_%s.jpg' % (floor, picId)
    with open(src, 'wb') as out_file:
        shutil.copyfileobj(pic.raw, out_file)
    del pic

pw=getpass.getpass()

url01 = 'https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
url02 = 'https://login.microsoftonline.com/login.srf'
url03 = 'https://portal.microsoftonline.com'
url04 = 'https://portal.office.com/landing.aspx?target=%2fdefault.aspx&wa=wsignin1.0'
url05 = 'https://officerakuten.sharepoint.com/_forms/default.aspx?apr=1&wa=wsignin1.0'
url06 = 'https://o365.sso.rakuten-it.com/adfs/ls/'

urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/_w/%d_jpg.jpg'
url9 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'

payload01 = {'username':'1@rakuten.com', 'wa':'wsignin1.0', 'wtrealm':'urn:federation:MicrosoftOnline', 'popupui':''}
payload02 = {'wa': 'wsignin1.0'}
payload03 = {'wa': 'wsignin1.0'}
payload04 = {}
payload05 = {}

infile = sys.argv[1]
lines = open(infile).readlines()

parser=html.parser.HTMLParser()

with requests.session() as s:
    s.auth = HttpNtlmAuth('INTRA\\ruijie.yang', pw, s)
    s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Content-Type':'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests':'1'
        })
    # ret01 = s.get(url02)
    # payload01['wctx'] = ret01.text.split('wctx=')[1].split('\\u0026')[0]
    ret01 = s.get(url01)
    payload01['wctx'] = 'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BBYVHnL4-T7Qcc-kppq1-SXbVjEqEzZC_wIj4wtGxltMgv5F6Z4p4cVuqSmpRYklmfl5j5h4Q4tTi_zzcipD8rNT8yYx8-Xkp2fmxRcXpcWn5eSXAwWAJhQkJpfEl2QmZ6eW7GJWSTYySDEwSkvSTTQ2T9M1MTU30LUwMjXXNUlLNrBINkhMTTZJu8AicICTEQA1'
    # payload02['wctx'] = payload01['wctx']
    ret01 = s.get(url06, params=payload01)
    payload02['wresult'] = parser.unescape(ret01.text.split('name="wresult" value="')[1].split('" />')[0])
    payload02['wctx'] = parser.unescape(ret01.text.split('name="wctx" value="')[1].split('" />')[0])
    ret02 = s.post(url02, data=payload02)
    # print(ret02.text)
    payload03['t'] = ret02.text.split('value="')[1].split('">')[0]
    ret03 = s.post(url03, data=payload03)
    payload04['t'] = ret03.text.split('value="')[1].split('">')[0]
    ret04 = s.post(url04, data=payload04)
    ret9 = s.get(url9)
    payload05['t'] = ret9.text.split('value="')[1].split('">')[0]
    
    ret9 = s.post(url05, data=payload05)
    for line in lines:
        line = line.strip()
        if len(line) < 1:
            continue
        [floor, picId] = [int(x) for x in line.split()]
        downloadPic(s, floor, picId)
