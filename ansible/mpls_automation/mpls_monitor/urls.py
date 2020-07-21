from django.urls import path
from mpls_monitor import views


urlpatterns = [
	path('', views.index, name='index'),
	path('ping/', views.ping_test, name='ping_test'),
]