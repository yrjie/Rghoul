from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import views
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Rghoul.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', views.onDate),
    url(r'^index/$', views.onDate),
    url(r'^get_like/(?P<name>.+)/$', views.getLike),
    url(r'^get_dislike/(?P<name>.+)/$', views.getDislike),
    url(r'^like/(?P<name>.+)/$', views.like),
    url(r'^dislike/(?P<name>.+)/$', views.dislike),
    url(r'^update/$', views.update),
    url(r'^date/(?P<date>[0-9]+)/$', views.onDate),
    url(r'^comment/$', views.comment),
    url(r'^date/(?P<date>[0-9]+)/comment/$', views.comment),

    url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()
