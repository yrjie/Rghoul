# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseNotFound
import os
import settings
import utils
from models import Picture, Comment, Dish, Poll
import dateutil.parser
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
import json
import string
import random

# Create your views here.
def home(request):
    return HttpResponse("Hello World, Django")

def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = ("title = %s, category = %s, date_time = %s, content = %s"
        % (post.title, post.category, post.date_time, post.content))
    return HttpResponse(str)

def onDate(request, date=None, page=None):
    if date == None:
        date = utils.getToday()
    if page and page!="lunch" and page!="dinner":
        return HttpResponseNotFound(utils.notFound % request.path_info)
    lunch9, lunch22, dinner9, dinner22 = utils.getFileLists(date)
    lunch9cnt, lunch22cnt, dinner9cnt, dinner22cnt = {}, {}, {}, {}
    folders = utils.getDateList()
    dateObj = utils.getDateObj(date)
    useSp = dateObj > utils.dateSp  # sharepoint
    if not useSp:
        for file in lunch9:
            lunch9cnt[file] = getPicCnt(file)
        for file in lunch22:
            lunch22cnt[file] = getPicCnt(file)
        for file in dinner9:
            dinner9cnt[file] = getPicCnt(file)
        for file in dinner22:
            dinner22cnt[file] = getPicCnt(file)
    showDinner = (dinner9cnt or dinner22cnt) and utils.getNowH() >= utils.dinnerH
    if page=="lunch":
        showDinner = False
    elif page=="dinner":
        showDinner = True
    cmts = []
    allcmts = Comment.objects.order_by("-id")[0:50]
    groupSize = 10
    group = []
    for i, x in enumerate(allcmts):
        if i%groupSize == 0:
            if i>0:
                cmts.append(group)
            group = []
        group.append(x.context + utils.getPdate(x.date))
    if group:
        cmts.append(group)
    if not useSp:
        return render_to_response("index.html", {"folders":folders, "date":date, 
                                             "lunch9cnt":lunch9cnt, "lunch22cnt":lunch22cnt, 
                                             "dinner9cnt":dinner9cnt, "dinner22cnt":dinner22cnt,
                                             "cmts":cmts, "showDinner":showDinner})
    isToday = date==utils.getToday()
    lunch9info, lunch22info, dinner9info, dinner22info = {}, {}, {}, {}
    for file in lunch9:
        lunch9info[file] = getDishInfo(file, date)
    for file in lunch22:
        lunch22info[file] = getDishInfo(file, date)
    for file in dinner9:
        dinner9info[file] = getDishInfo(file, date)
    for file in dinner22:
        dinner22info[file] = getDishInfo(file, date)
    meal = ""
    if isToday and (lunch9info or lunch22info or dinner9info or dinner22info):
        if utils.getNowH() >= utils.dinnerH:
            meal = "dinner"
        else:
            meal = "lunch"
    showDinner = (dinner9info or dinner22info) and utils.getNowH() >= utils.dinnerH
    if page=="lunch":
        showDinner = False
    elif page=="dinner":
        showDinner = True
    polls = getOpenPolls()
    dateTtl = dateObj.strftime("%m.%d")
    return render_to_response("indexSp.html", {"folders":folders, "date":date, "meal":meal,
                                             "lunch9info":lunch9info, "lunch22info":lunch22info, 
                                             "dinner9info":dinner9info, "dinner22info":dinner22info, 
                                             "cmts":cmts, "showDinner":showDinner,
                                             "polls":polls, "dateTtl":dateTtl})

# not used
def getLike(request, name):
    rs = Picture.objects.filter(picName=name)
    ret = 0
    for pic in rs:
        ret = pic.like
    return HttpResponse(ret)

# not used
def getDislike(request, name):
    rs = Picture.objects.filter(picName=name)
    ret = 0
    for pic in rs:
        ret = pic.dislike
    return HttpResponse(ret)
    
def like(request, name):
    rs = Picture.objects.filter(picName=name)
    ret = 0
    for pic in rs:
        pic.like += 1
        ret = pic.like
        pic.save()
    return HttpResponse(ret)

def dislike(request, name):
    rs = Picture.objects.filter(picName=name)
    ret = 0
    for pic in rs:
        pic.dislike += 1
        ret = pic.dislike
        pic.save()
    return HttpResponse(ret)

def likeSp(request, id):
    rs = Dish.objects.filter(id=int(id))
    ret = 0
    for x in rs:
        x.like += 1
        ret = x.like
        x.save()
    return HttpResponse(ret)

def dislikeSp(request, id):
    rs = Dish.objects.filter(id=int(id))
    ret = 0
    for x in rs:
        x.dislike += 1
        ret = x.dislike
        x.save()
    return HttpResponse(ret)

@csrf_exempt
def comment(request, date=None):
    res = ""
    if request.POST.has_key("context") and len(request.POST["context"])>0:
        maxLen = Comment._meta.get_field("context").max_length
        author = utils.escapeHtml(request.POST["author"])
        if len(author) == 0:
            author = utils.getMaskedIp(request)
        if author == "admin@mars":
            res = "<dt><font color=\"orange\">%s</font></dt>" % "admin"
        else:
            res = "<dt>%s</dt>" % author
        context = utils.escapeHtml(request.POST["context"].replace("\r\n", "\n"))
        for line in context.split("\n"):
            res += "\r\n<dd>%s</dd>" % line
        res = res[0:maxLen-55]
        context = res
        parent = utils.getToday()
        cmt = Comment(author=author, context=context, parent=parent)
        cmt.save()
        res += utils.getPdate(cmt.date)
    return HttpResponse(res)

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

# sharepoint
@csrf_exempt
def updateSp(request):
    today = utils.getToday()
    todayD = dateutil.parser.parse(today).date()
    allDishes = json.loads(request.body)
    cnt = 0
    for x in allDishes:
        rs = Dish.objects.filter(pid=x["id"], date__range=(todayD, todayD))
        if rs:
            continue
        d0 = Dish()
        if rs:
            d0.date = rs[0].date
        d0.pid = x["id"]
        d0.name = x["name"]
        d0.booth = x["booth"]
        d0.ingredient = x["ingredient"]
        if "<Simple Wamen>" in x["name"]:
            d0.energy = 320
        else:
            d0.energy = x["energy"]
        d0.price = x["price"]
        d0.mealTime = x["mealTime"]
        d0.floor = x["floor"]
        d0.like = 0
        d0.dislike = 0
        d0.save()
        cnt += 1
    return HttpResponse("INFO(SP): updated %d pictures" % cnt)

def favicon(request):
    filepath = settings.BASE_DIR + "/static/favicon.ico"
    return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

def bookmark(request):
    folders = utils.getDateList()
    return render_to_response("bookmark.html", {"folders":folders})

@csrf_exempt
def createPoll(request):
    if not request.POST:
        folders = utils.getDateList()
        if utils.getNowH() >= utils.dinnerH:
            meal = "dinner"
        else:
            meal = "lunch"
        return render_to_response("createpoll.html", {"folders":folders, "meal":meal})
    codeLen = 8
    codeChars = string.ascii_uppercase+string.ascii_lowercase+string.digits
    code = ""
    while True:
        code = "".join(random.choice(codeChars) for _ in range(codeLen))
        if not Poll.objects.filter(code=code):
            break
    owner = utils.escapeHtml(request.POST["owner"])
    if not owner:
        owner = utils.getMaskedIp(request)
    title = utils.escapeHtml(request.POST["title"])
    if not title:
        title = "%s's poll" % owner
    open = "open" in request.POST
    p = Poll(owner=owner, title=title, open=open, parent=utils.getToday(), code=code, count=0)
    result = {}
    result["0_-1"] = []  # any
    result["9_-1"] = []  # 9 any
    result["22_-1"] = []  # 22 any
    lunch9, lunch22, dinner9, dinner22 = utils.getFileLists()
    if utils.getNowH() >= utils.dinnerH:
        dish9 = [int(x.split(".")[0]) for x in dinner9]
        dish22 = [int(x.split(".")[0]) for x in dinner22]
    else:
        dish9 = [int(x.split(".")[0]) for x in lunch9]
        dish22 = [int(x.split(".")[0]) for x in lunch22]
    for d in dish9:
        result["9_"+str(d)] = []
    for d in dish22:
        result["22_"+str(d)] = []
    p.result = json.dumps(result)
    p.save()
    return redirect("/poll/%s/" % code)

def showPoll(request, code):
    rs = Poll.objects.filter(code=code)
    if not rs:
        return HttpResponseNotFound(utils.notFound % request.path_info)
    folders = utils.getDateList()
    poll = rs[0]
    owner = poll.owner
    title = poll.title
    count = poll.count
    dish0res, dish0cnt, dish9res, dish9cnt, dish22res, dish22cnt = getDishResult(poll)
    return render_to_response("poll.html", {"folders":folders, "count":count,
                                        "owner":owner, "title":title, "code":code,
                                        "dish0res":dish0res, "dish0cnt":dish0cnt,
                                        "dish9res":dish9res, "dish9cnt":dish9cnt,
                                        "dish22res":dish22res, "dish22cnt":dish22cnt})

@csrf_exempt
def vote(request):
    if not request.POST:
        return HttpResponseNotFound(utils.notFound % request.path_info)
    code = utils.escapeHtml(request.POST["code"])
    rs = Poll.objects.filter(code=code)
    if not rs:
        return HttpResponseNotFound(utils.notFound % request.path_info)  # to be tested
    voter = utils.escapeHtml(request.POST["voter"])
    if not voter:
        voter = utils.getMaskedIp(request)
    dish = utils.escapeHtml(request.POST["voteDish"])
    poll = rs[0]
    res = json.loads(poll.result)
    if res[dish]:
        added = ", " + voter
    else:
        added = ": " + voter
    res[dish].append(voter)
    poll.result = json.dumps(res)
    poll.count += 1
    poll.save()
    return HttpResponse(added)

# common functions performing directly on models
def getPicCnt(file):
    rs = Picture.objects.filter(picName = file)
    cnt = [0, 0]
    for pic in rs:
        cnt[0] = pic.like
        cnt[1] = pic.dislike
    return cnt

def getDishInfo(file, date):
    dateD = dateutil.parser.parse(date).date()
    pid = utils.file2id(file)
    rs = Dish.objects.filter(pid = pid, date__range = (dateD, dateD))
    ret = []
    for dish in rs:
        booth = dish.booth.split("_")[1]
        name = "<font color=\"#0174DF\">[" + booth  + "]</font> " + dish.name
        energy = dish.energy
        id = dish.id
        if dish.price:
            name += unicode("<font color=\"red\">(￥%d)</font>" % dish.price, "utf-8")
        ret.append(name)
        ret.append(utils.parseIngd(dish.ingredient))
        ret.append(energy)
        ret.append([dish.like, dish.dislike])
        ret.append(id)
    return ret

def getDishResult(p):
    res = json.loads(p.result)
    dishRes = {}
    dishRes[0] = {}
    dishRes[9] = {}
    dishRes[22] = {}
    dishCnt = {}
    dishCnt[0] = 0
    dishCnt[9] = 0
    dishCnt[22] = 0
    for x in res:
        floor, id = utils.getFloorDish(x)
        if floor == 0:
            name = "Any dish is fine for me"
            energy = "-"
        else:
            if floor == 9:
                name = "9th floor - "
            else:
                name = "22nd floor - "
            rs = Dish.objects.filter(pid=id, floor=floor).order_by("-id")
            if rs:
                d = rs[0]
                name += "[%s] %s" % (d.booth.split("_")[1], d.name)
                energy = "%d kcal" % d.energy
            else:
                name += "Any dish is fine for me"
                energy = "-"
        num = len(res[x])
        if num:
            val = "%d: %s" % (num, ", ".join(res[x]))
        else:
            val = "0"
        dishRes[floor][x] = []
        dishRes[floor][x].append(name)
        dishRes[floor][x].append(energy)
        dishRes[floor][x].append(val)
        dishCnt[floor] += num
    return dishRes[0], dishCnt[0], dishRes[9], dishCnt[9], dishRes[22], dishCnt[22]

def getOpenPolls():
    polls = {}
    today = utils.getToday()
    rs = Poll.objects.filter(open=True, parent=today)
    for p in rs:
        info = []
        info.append(p.title)
        info.append(p.owner)
        info.append(p.count)
        polls[p.code] = info
    return polls

def about(request):
    folders = utils.getDateList()
    return render_to_response("about.html", {"folders":folders})

def close(request):
    cmts = []
    allcmts = Comment.objects.order_by("-id")[0:50]
    groupSize = 10
    group = []
    for i, x in enumerate(allcmts):
        if i%groupSize == 0:
            if i>0:
                cmts.append(group)
            group = []
        group.append(x.context + utils.getPdate(x.date))
    if group:
        cmts.append(group)
    return render_to_response("close.html", {"cmts":cmts})
