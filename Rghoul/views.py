from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from os import listdir
from os.path import isfile, join
import settings

# Create your views here.
def home(request):
    return HttpResponse("Hello World, Django")

def detail(request, my_args):
    post = Article.objects.all()[int(my_args)]
    str = ("title = %s, category = %s, date_time = %s, content = %s"
        % (post.title, post.category, post.date_time, post.content))
    return HttpResponse(str)

def index(request):
    path9 = settings.BASE_DIR + '/static/images9'
    files9 = [ f for f in listdir(path9) if isfile(join(path9,f)) ]
    path22 = settings.BASE_DIR + '/static/images22'
    files22 = [ f for f in listdir(path22) if isfile(join(path22,f)) ]
    return render_to_response('index.html', {'files9':files9, 'files22':files22})