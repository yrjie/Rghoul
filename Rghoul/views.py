from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from os import listdir
from os.path import isfile, join
import os
import settings
import datetime
import time

# Create your views here.
def home(request):
    return HttpResponse("Hello World, Django")

def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = ("title = %s, category = %s, date_time = %s, content = %s"
        % (post.title, post.category, post.date_time, post.content))
    return HttpResponse(str)

def index(request):
    ts = time.time();
    today = datetime.datetime.fromtimestamp(ts).strftime("%Y%m%d");
    prefix = settings.BASE_DIR + "/static/" + today
    if not os.path.exists(prefix):
        os.makedirs(prefix + "/lunch9")
        os.makedirs(prefix + "/lunch22")
        os.makedirs(prefix + "/dinner9")
        os.makedirs(prefix + "/dinner22")
    lunch9dir = prefix + "/lunch9"
    lunch9 = [ f for f in listdir(lunch9dir) if isfile(join(lunch9dir,f)) ]
    lunch22dir = prefix + "/lunch22"
    lunch22 = [ f for f in listdir(lunch22dir) if isfile(join(lunch22dir,f)) ]
    
    dinner9dir = prefix + "/dinner9"
    dinner9 = [ f for f in listdir(dinner9dir) if isfile(join(dinner9dir,f)) ]
    dinner22dir = prefix + "/dinner22"
    dinner22 = [ f for f in listdir(dinner22dir) if isfile(join(dinner22dir,f)) ]
    
    return render_to_response("index.html", {"today":today, "lunch9":lunch9, "lunch22":lunch22, 
                                             "dinner9":dinner9, "dinner22":dinner22})