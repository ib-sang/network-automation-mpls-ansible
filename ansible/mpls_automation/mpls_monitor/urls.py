from django.urls import include,path
from django.contrib.auth import views as loginview
#from ORGui.forms import LoginForm
from . import views




urlpatterns = [
    path('', views.index, name="home"),
]