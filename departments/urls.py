from django.conf.urls import patterns, url
from departments import views


urlpatterns = patterns('',  # NOQA
    url(r'^$', views.index, name='departments'),
     url(r'^(?P<department_id>\d+)/$', views.detail, name='department'),
)
