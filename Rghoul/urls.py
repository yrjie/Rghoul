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
    url(r'^$', views.index),
    url(r'^index/', views.index),
    url(r'^like/(?P<picName>.+)/$', views.like),
    url(r'^dislike/(?P<picName>.+)/$', views.dislike),
    url(r'^update/$', views.update),

    url(r'^admin/', include(admin.site.urls)),
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns += staticfiles_urlpatterns()
