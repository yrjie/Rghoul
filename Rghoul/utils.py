import datetime
import settings
from os.path import isfile, join
from os import listdir
import os
import subprocess
from dateutil import tz

def getToday():
    today = datetime.date.today().strftime("%Y%m%d");
    return today

def getDateObj(dStr=None):
    if dStr==None:
        dStr = getToday()
    return datetime.datetime.strptime(dStr, "%Y%m%d").date()

def getFileLists(date=None):
    if date==None:
        today = getToday()
    else:
        today = date
    prefix = settings.BASE_DIR + "/static/data/" + today
    if not os.path.exists(prefix):  # make sure index will show properly
        if today == getToday():
            os.makedirs(prefix + "/lunch9")
            os.makedirs(prefix + "/lunch22")
            os.makedirs(prefix + "/dinner9")
            os.makedirs(prefix + "/dinner22")
            subprocess.call(["chmod", "-R", "777", prefix])
        return [], [], [], []
    
    lunch9dir = prefix + "/lunch9"
    lunch9 = [ f for f in listdir(lunch9dir) if isfile(join(lunch9dir,f)) ]
    lunch22dir = prefix + "/lunch22"
    lunch22 = [ f for f in listdir(lunch22dir) if isfile(join(lunch22dir,f)) ]
    
    dinner9dir = prefix + "/dinner9"
    dinner9 = [ f for f in listdir(dinner9dir) if isfile(join(dinner9dir,f)) ]
    dinner22dir = prefix + "/dinner22"
    dinner22 = [ f for f in listdir(dinner22dir) if isfile(join(dinner22dir,f)) ]
    return lunch9, lunch22, dinner9, dinner22

def getDateList():
    dataDir = settings.BASE_DIR + "/static/data/"
    return sorted([d for d in listdir(dataDir)], reverse=True)[0:10]

def getClientIp(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def getPdate(date):
    pdatetml = "\r\n<dd class=\"posttime\">posted at %s</dd>"
    tky = tz.gettz("Asia/Tokyo")
    now = date.astimezone(tky).strftime("%Y-%m-%d %H:%M:%S")
    return pdatetml % now

def getNowH():
    date = datetime.datetime.now().replace(tzinfo=tz.tzlocal())
    tky = tz.gettz("Asia/Tokyo")
    nowH = int(date.astimezone(tky).strftime("%H"))
    return nowH

def parseIngd(ingd):
    allIngd = ["ALCOHOL", "BEEF", "CHIKEN", "FISH", "HEALTHY", "MUTTON", "PORK"]
    ret = []
    for i, x in enumerate(allIngd):
        if ingd & (1<<i):
            ret.append(x)

def file2id(file):
    return int(file.split(".")[0])

notFound = "<h1>Not Found</h1><p>The requested URL %s was not found on this server.</p>"
dinnerH = 16
dateSp = getDateObj("20151002") # sharepoint
