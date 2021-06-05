from django.urls import path
from . import views

urlpatterns = [
    path('', views.signIn, name="signIn"),
    path('postsignIn/',views.postsignIn,name="postsign"),
    path('logout/',views.logout,name="logout")
    
]