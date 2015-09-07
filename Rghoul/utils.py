import time
import datetime
import settings
from os.path import isfile, join
from os import listdir
import os
import subprocess

def getToday():
    ts = time.time();
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d");
    return today

def getNow():
    ts = time.time();
    now = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S");
    return now

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
            subprocess.call(['chmod', '-R', '777', prefix])
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
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip