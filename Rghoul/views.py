from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import os
import settings
import utils
from models import Picture
import dateutil.parser

# Create your views here.
def home(request):
    return HttpResponse("Hello World, Django")

def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = ("title = %s, category = %s, date_time = %s, content = %s"
        % (post.title, post.category, post.date_time, post.content))
    return HttpResponse(str)

def onDate(request, date = None):
    if date == None:
        date = utils.getToday()
    lunch9, lunch22, dinner9, dinner22 = utils.getFileLists(date)
    lunch9cnt, lunch22cnt, dinner9cnt, dinner22cnt = {}, {}, {}, {}
    folders = utils.getDateList()
    for file in lunch9:
        rs = Picture.objects.filter(picName = file)
        cnt = [0, 0]
        for pic in rs:
            cnt[0] = pic.like
            cnt[1] = pic.dislike
        lunch9cnt[file] = cnt
    for file in lunch22:
        rs = Picture.objects.filter(picName = file)
        cnt = [0, 0]
        for pic in rs:
            cnt[0] = pic.like
            cnt[1] = pic.dislike
        lunch22cnt[file] = cnt
    for file in dinner9:
        rs = Picture.objects.filter(picName = file)
        cnt = [0, 0]
        for pic in rs:
            cnt[0] = pic.like
            cnt[1] = pic.dislike
        dinner9cnt[file] = cnt
    for file in dinner22:
        rs = Picture.objects.filter(picName = file)
        cnt = [0, 0]
        for pic in rs:
            cnt[0] = pic.like
            cnt[1] = pic.dislike
        dinner22cnt[file] = cnt
    return render_to_response("index.html", {"folders":folders, "date":date, 
                                             "lunch9cnt":lunch9cnt, "lunch22cnt":lunch22cnt, 
                                             "dinner9cnt":dinner9cnt, "dinner22cnt":dinner22cnt})

def getLike(request, name):
    rs = Picture.objects.filter(picName = name)
    ret = 0
    for pic in rs:
        ret = pic.like
    return HttpResponse(ret)

def getDislike(request, name):
    rs = Picture.objects.filter(picName = name)
    ret = 0
    for pic in rs:
        ret = pic.dislike
    return HttpResponse(ret)
    
def like(request, name):
    rs = Picture.objects.filter(picName = name)
    ret = 0
    for pic in rs:
        pic.like += 1
        ret = pic.like
        pic.save()
    return HttpResponse(ret)

def dislike(request, name):
    rs = Picture.objects.filter(picName = name)
    ret = 0
    for pic in rs:
        pic.dislike += 1
        ret = pic.dislike
        pic.save()
    return HttpResponse(ret)

def update(request):
    today = utils.getToday()
    prefix = settings.BASE_DIR + "/static/data/" + today
    if not os.path.exists(prefix):
        return HttpResponse("ERROR: today's pictures are not uploaded.")
    lunch9, lunch22, dinner9, dinner22 = utils.getFileLists()
    
    todayD = dateutil.parser.parse(today).date()
    pics = Picture.objects.filter(date__range=(todayD, todayD))
    cnt = 0
    for file in lunch9:
        if len(pics.filter(picName=file)) == 0:
            pic = Picture(picName=file, mealTime="L", floor=9, like=0, dislike=0)
            pic.save()
            cnt += 1
    for file in lunch22:
        if len(pics.filter(picName=file)) == 0:
            pic = Picture(picName=file, mealTime="L", floor=22, like=0, dislike=0)
            pic.save()
            cnt += 1
    for file in dinner9:
        if len(pics.filter(picName=file)) == 0:
            pic = Picture(picName=file, mealTime="D", floor=9, like=0, dislike=0)
            pic.save()
            cnt += 1
    for file in dinner22:
        if len(pics.filter(picName=file)) == 0:
            pic = Picture(picName=file, mealTime="D", floor=22, like=0, dislike=0)
            pic.save()
            cnt += 1
    return HttpResponse("INFO: updated %d pictures" % cnt)
