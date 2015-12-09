#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
import getpass
import shutil
import json
import time
import datetime
import requests
from requests_ntlm import HttpNtlmAuth
import html.parser

if len(sys.argv) < 2:
    print('Usage: auto script')
    exit(1)

class dish:
    def __init__(self, id, name, booth, ingredient, energy, price, mealTime, floor):
        self.id = id
        self.name = name
        self.booth = booth
        self.ingredient = ingredient
        self.energy = energy
        self.price = price
        self.mealTime = mealTime
        self.floor = floor

def parseDish(s, floor, lines, dishes, id2pic):
    id = 0
    pic = 0
    name = ''
    booth = ''
    ingredient = 0
    price = 0
    mealTime = ''
    lookupId = 0

    state = 0  # 0: before dishes, 1: in dishes, 2: in one dish
    for line in lines:
        if state == 0:
            if 'var WPQ2ListData' in line:
                state = 1
            continue
        if state == 1:
            if '"ID"' in line:
                state = 2
                id = int(line.split('": "')[1].split('",')[0])
            if 'FolderPermissions' in line:
                break
            continue
        if state == 2:
            if 'lookupValue' in line:
                lookupId = int(line.split('lookupId":')[1].split(',')[0])
                name = line.split('lookupValue":"')[1].split('",')[0].replace('\\', '').replace('u3000', ' ').replace('uff53', 'ｓ')
            if 'Ingredients' in line:
                ingds = set()
                temp = line.split('title=\\"')
                for x in temp[1:]:
                    ingds.add(x.split('\\"')[0])
                ingredient = 0
                for i, x in enumerate(ingdLst):
                    if x in ingds:
                        ingredient += (1<<i)
            if 'Menu_x003a_Calory' in line:
                temp = line.split('Menu_x003a_Calory": "')[1].split('",')[0]
                if temp:
                    energy = int(temp)
                else:
                    energy = 0
            if 'Menu_x003a_Value' in line:
                temp = line.split('Menu_x003a_Value": "')[1].split('",')[0]
                if temp:
                    price = int(temp)
                else:
                    price = 0
            if 'Timezone' in line:
                mealTime = line.split('Timezone": "')[1].split('",')[0][0]
            if 'MenuTypeTitle' in line:
                booth = line.split('MenuTypeTitle": "')[1].split('",')[0]
                picid = getPic(s, floor, lookupId)
                if picid:
                    id2pic[id] = picid
                    dishes.append(dish(id, name, booth, ingredient, energy, price, mealTime, floor))
                state = 1
            continue

def getPic(s, floor, lookupId):
    retDish = s.get(urlDish % (floor, lookupId))
    picLines = retDish.text.replace('\r\n', '\n').split('\n')
    ret = 0
    for line in picLines:
        if 'Menu Image' in line:
            ret = int(line.split('-')[-1])
            break
    return ret

def downloadPics(s, dishes, id2pic):
    nowDir = os.getcwd()
    today = getToday()
    for x in dishes:
        picId = id2pic[x.id]
        pic = s.get(urlPic % (x.floor, picId), stream=True)
        meal = 'lunch'
        if x.mealTime == 'D':
            meal = 'dinner'
        os.chdir('%s/static/data/%s/%s%d/' % (nowDir, today, meal, x.floor))
        src = '../../../images/%s.jpg' % picId
        dst = '%d.jpg' % x.id
        with open(src, 'wb') as out_file:
            shutil.copyfileobj(pic.raw, out_file)
        del pic
        try:
            os.symlink(src, dst)
        except:
            os.unlink(dst)
            os.symlink(src, dst)

def getToday():
    ts = time.time()
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d")
    return today

def main():
    pw = getpass.getpass()

    url01 = 'https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
    url02 = 'https://login.microsoftonline.com/login.srf'
    url03 = 'https://portal.microsoftonline.com'
    url04 = 'https://portal.office.com/landing.aspx?target=%2fdefault.aspx&wa=wsignin1.0'
    url05 = 'https://officerakuten.sharepoint.com/_forms/default.aspx?apr=1&wa=wsignin1.0'
    url06 = 'https://o365.sso.rakuten-it.com/adfs/ls/'

    url9 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'
    url22 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_22F/TodaysMenu.aspx'

    urlDish = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/Forms/DispForm.aspx?ID=%d'
    # urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/%d.jpg'
    urlPic = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/_w/%d_jpg.jpg'

    url2 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/Forms/DispForm.aspx'
    url3 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_9F/Forms/DispForm.aspx?ID=186'
    urlIngd = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/%s.jpg'
    urlUpdate = 'http://gcsd-id-mars-japan.cloudapp.net/thisisupdateSp/'

    payload01 = {'username':'1@rakuten.com', 'wa':'wsignin1.0', 'wtrealm':'urn:federation:MicrosoftOnline', 'popupui':''}
    payload02 = {'wa': 'wsignin1.0'}
    payload03 = {'wa': 'wsignin1.0'}
    payload04 = {}
    payload05 = {}

    ingdLst = ['ALCOHOL', 'BEEF', 'CHIKEN', 'FISH', 'HEALTHY', 'MUTTON', 'PORK']
    dishes = []
    id2pic = {}

    parser = html.parser.HTMLParser()

    with requests.session() as s:
        s.auth = HttpNtlmAuth('INTRA\\ruijie.yang', pw, s)
        s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
                          'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                          'Accept-Encoding':'gzip, deflate',
                          'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2',
                          'Cache-Control':'max-age=0',
                          'Connection':'keep-alive',
                          'Content-Type':'application/x-www-form-urlencoded',
                          'Upgrade-Insecure-Requests':'1'})
        # ret01 = s.get(url02)
        # payload01['wctx'] = ret01.text.split('wctx=')[1].split('\\u0026')[0]
        ret01 = s.get(url01)
        print(ret01.text)
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
        lines = ret9.text.replace('\r\n', '\n').split('\n')
        parseDish(s, 9, lines, dishes, id2pic)

        ret22 = s.get(url22)
        lines = ret22.text.replace('\r\n', '\n').split('\n')
        parseDish(s, 22, lines, dishes, id2pic)
        downloadPics(s, dishes, id2pic)
        # for x in ingdLst:
        #     ingdfile = s.get(urlIngd % x, stream=True)
        #     with open('static/images/%s.jpg' % x, 'wb') as out_file:
        #         shutil.copyfileobj(ingdfile.raw, out_file)
        #     del ingdfile
        
    dishJson = json.dumps([vars(x) for x in dishes])
    # print(dishJson)
    # print(id2pic)

    ret = requests.post(urlUpdate, data=dishJson)
    print(ret.text)

if __name__ == '__main__':
    main()
