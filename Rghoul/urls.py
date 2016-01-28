from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Rghoul.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.onDate),
    url(r'^index/(?P<page>.+)/$', views.onDate),
    url(r'^like/(?P<name>.+)/$', views.like),
    url(r'^dislike/(?P<name>.+)/$', views.dislike),
    url(r'^likeSp/(?P<id>.+)/$', views.likeSp),
    url(r'^dislikeSp/(?P<id>.+)/$', views.dislikeSp),
    url(r'^thisisupdate/$', views.update),
    url(r'^thisisupdateSp/$', views.updateSp),
    url(r'^date/(?P<date>[0-9]+)/$', views.onDate),
    url(r'^comment/$', views.comment),
    url(r'^date/(?P<date>[0-9]+)/comment/$', views.comment),
    url(r'^favicon.ico$', views.favicon),
    url(r'^bookmark/$', views.bookmark),
    url(r'^createpoll/$', views.createPoll),
    url(r'^poll/(?P<code>.+)/$', views.showPoll),
    url(r'^vote/$', views.vote),
    url(r'^about/$', views.about),

    url(r'^thisisadmin/', include(admin.site.urls)),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()
