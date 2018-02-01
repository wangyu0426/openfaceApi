from django.conf.urls import url
from snippets import views

urlpatterns = [       
    url(r'^faces/train/(?P<identity>[0-9]+)/$', views.faceTrain.as_view()),     
    url(r'^faces/seek/$', views.faceSeek.as_view()),
    url(r'^faces/vector/$', views.faceProcess.as_view()),
    url(r'^faces/dump/$', views.svmDump.as_view()),
    url(r'^faces/load/$', views.svmLoad.as_view()),
]