"""keylogger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from logger import views
from logger.views import login_view, signup_view


urlpatterns = [
    path('', login_view, name='login'), # set login_view as the default URL
    path('signup/', signup_view, name='signup'), 
    path('start/', views.start, name='start'),
    path('stop/', views.stop, name='stop'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
]

