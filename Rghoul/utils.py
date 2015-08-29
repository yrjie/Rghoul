import time
import datetime
import settings
from os.path import isfile, join
from os import listdir
import os

def getToday():
    ts = time.time();
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d");
    return today

def getFileLists():
    today = getToday()
    prefix = settings.BASE_DIR + "/static/" + today
    if not os.path.exists(prefix):  # make sure index will show properly
        os.makedirs(prefix + "/lunch9")
        os.makedirs(prefix + "/lunch22")
        os.makedirs(prefix + "/dinner9")
        os.makedirs(prefix + "/dinner22")
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
