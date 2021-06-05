from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('/main/', views.main, name="main"),
    path('/status/',views.status,name="status"),
     url(r'^alert/',views.alert,name="alert"),
    url(r'^postuser/',views.postuser,name="post_user")
]