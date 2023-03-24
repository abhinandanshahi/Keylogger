from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
     path('', include('keylogger.urls')),  # include the urls from the project
]
