#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

"""A module for updating the sqlite data of menu"""

import sys
import os
import getpass
import shutil
import json
import time
import datetime
import html.parser
import requests
from requests_ntlm import HttpNtlmAuth

INGD_LST = ['ALCOHOL', 'BEEF', 'CHIKEN', 'FISH', 'HEALTHY', 'MUTTON', 'PORK']
URL01 = 'https://adfs.mail.rakuten.com/adfs/ls/auth/integrated/'
URL02 = 'https://login.microsoftonline.com/login.srf'
URL03 = 'https://portal.microsoftonline.com'
URL04 = 'https://portal.office.com/landing.aspx?target=%2fdefault.aspx&wa=wsignin1.0'
URL05 = 'https://officerakuten.sharepoint.com/_forms/default.aspx?apr=1&wa=wsignin1.0'
URL06 = 'https://o365.sso.rakuten-it.com/adfs/ls/'

URL9 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_9F/TodaysMenu.aspx'
URL22 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/Lists/Menu_22F/TodaysMenu.aspx'

URL_DISH = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/Forms/DispForm.aspx?ID=%d'
# URL_PIC = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/%d.jpg'
URL_PIC = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_%dF/_w/%d_jpg.jpg'

URL2 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/Forms/DispForm.aspx'
URL3 = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/MenuImage_9F/Forms/DispForm.aspx?ID=186'
URL_INGD = 'https://officerakuten.sharepoint.com/sites/Committees/cafeteria/IngredientIcons_9F/%s.jpg'
URL_UPDATE = 'http://gcsd-id-mars-japan.cloudapp.net/thisisupdateSp/'

class Dish(object):
    """A class for storing dish information"""
    def __init__(self, id, name, booth, ingredient, energy, price, meal_time, floor):
        self.id = id
        self.name = name
        self.booth = booth
        self.ingredient = ingredient
        self.energy = energy
        self.price = price
        self.meal_time = meal_time
        self.floor = floor

def parse_dish(sess, floor, lines, dishes, id2pic):
    """parse dish information from website"""
    id = 0
    name = ''
    booth = ''
    ingredient = 0
    price = 0
    meal_time = ''
    lookup_id = 0

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
                lookup_id = int(line.split('lookup_id":')[1].split(',')[0])
                name = line.split('lookupValue":"')[1].split('",')[0].replace('\\', '').replace('u3000', ' ').replace('uff53', 'ｓ')
            if 'Ingredients' in line:
                ingds = set()
                temp = line.split('title=\\"')
                for x in temp[1:]:
                    ingds.add(x.split('\\"')[0])
                ingredient = 0
                for i, x in enumerate(INGD_LST):
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
                meal_time = line.split('Timezone": "')[1].split('",')[0][0]
            if 'MenuTypeTitle' in line:
                booth = line.split('MenuTypeTitle": "')[1].split('",')[0]
                pic_id = get_pic(sess, floor, lookup_id)
                if pic_id:
                    id2pic[id] = pic_id
                    dishes.append(Dish(id, name, booth, ingredient,
                                       energy, price, meal_time, floor))
                state = 1
            continue

def get_pic(sess, floor, lookup_id):
    """get the id of a picture"""
    ret_dish = sess.get(URL_DISH % (floor, lookup_id))
    pic_lines = ret_dish.text.replace('\r\n', '\n').split('\n')
    ret = 0
    for line in pic_lines:
        if 'Menu Image' in line:
            ret = int(line.split('-')[-1])
            break
    return ret

def download_pics(sess, dishes, id2pic):
    """download the pictures"""
    now_dir = os.getcwd()
    today = get_today()
    for x in dishes:
        pic_id = id2pic[x.id]
        pic = sess.get(URL_PIC % (x.floor, pic_id), stream=True)
        meal = 'lunch'
        if x.meal_time == 'D':
            meal = 'dinner'
        os.chdir('%s/static/data/%s/%s%d/' % (now_dir, today, meal, x.floor))
        src = '../../../images/%s.jpg' % pic_id
        dst = '%d.jpg' % x.id
        with open(src, 'wb') as out_file:
            shutil.copyfileobj(pic.raw, out_file)
        del pic
        try:
            os.symlink(src, dst)
        except:
            os.unlink(dst)
            os.symlink(src, dst)

def get_today():
    """get today's date"""
    ts = time.time()
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d")
    return today

def main():
    """main function"""
    if len(sys.argv) < 2:
        print('Usage: auto script')
        exit(1)

    payload01 = {'username':'1@rakuten.com', 'wa':'wsignin1.0',
                 'wtrealm':'urn:federation:MicrosoftOnline', 'popupui':''}
    payload02 = {'wa': 'wsignin1.0'}
    payload03 = {'wa': 'wsignin1.0'}
    payload04 = {}
    payload05 = {}
    pw = getpass.getpass()

    dishes = []
    id2pic = {}

    parser = html.parser.HTMLParser()

    with requests.session() as sess:
        sess.auth = HttpNtlmAuth('INTRA\\ruijie.yang', pw, sess)
        sess.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
                             'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                             'Accept-Encoding':'gzip, deflate',
                             'Accept-Language':'en-US,en;q=0.8,ja;q=0.6,zh-CN;q=0.4,zh;q=0.2',
                             'Cache-Control':'max-age=0',
                             'Connection':'keep-alive',
                             'Content-Type':'application/x-www-form-urlencoded',
                             'Upgrade-Insecure-Requests':'1'})
        # ret01 = sess.get(URL02)
        # payload01['wctx'] = ret01.text.split('wctx=')[1].split('\\u0026')[0]
        ret01 = sess.get(URL01)
        print(ret01.text)
        payload01['wctx'] = 'estsredirect=2&estsrequest=rQIIAbPSySgpKSi20tcvyC8qSczRy81MLsovzk8ryc_LycxL1UvOz9XLL0rPTAGxioS4BBYVHnL4-T7Qcc-kppq1-SXbVjEqEzZC_wIj4wtGxltMgv5F6Z4p4cVuqSmpRYklmfl5j5h4Q4tTi_zzcipD8rNT8yYx8-Xkp2fmxRcXpcWn5eSXAwWAJhQkJpfEl2QmZ6eW7GJWSTYySDEwSkvSTTQ2T9M1MTU30LUwMjXXNUlLNrBINkhMTTZJu8AicICTEQA1'
        # payload02['wctx'] = payload01['wctx']
        ret01 = sess.get(URL06, params=payload01)
        payload02['wresult'] = parser.unescape(ret01.text.split('name="wresult" value="')[1].split('" />')[0])
        payload02['wctx'] = parser.unescape(ret01.text.split('name="wctx" value="')[1].split('" />')[0])
        ret02 = sess.post(URL02, data=payload02)
        # print(ret02.text)
        payload03['t'] = ret02.text.split('value="')[1].split('">')[0]
        ret03 = sess.post(URL03, data=payload03)
        payload04['t'] = ret03.text.split('value="')[1].split('">')[0]
        ret04 = sess.post(URL04, data=payload04)
        ret9 = sess.get(URL9)
        payload05['t'] = ret9.text.split('value="')[1].split('">')[0]

        ret9 = sess.post(URL05, data=payload05)
        lines = ret9.text.replace('\r\n', '\n').split('\n')
        parse_dish(sess, 9, lines, dishes, id2pic)

        ret22 = sess.get(URL22)
        lines = ret22.text.replace('\r\n', '\n').split('\n')
        parse_dish(sess, 22, lines, dishes, id2pic)
        download_pics(sess, dishes, id2pic)
        # for x in INGD_LST:
        #     ingdfile = sess.get(URL_INGD % x, stream=True)
        #     with open('static/images/%s.jpg' % x, 'wb') as out_file:
        #         shutil.copyfileobj(ingdfile.raw, out_file)
        #     del ingdfile

    dish_json = json.dumps([vars(x) for x in dishes])
    # print(dish_json)
    # print(id2pic)

    ret = requests.post(URL_UPDATE, data=dish_json)
    print(ret.text)

if __name__ == '__main__':
    main()
