"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from users import views
from django.conf.urls import url, include


urlpatterns = [
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    url(r'^insertProduct$', views.insertProduct, name="insertProduct"),
    url(r'^getProducts$', views.getProducts, name="getProducts"),
    url(r'^getCategories$', views.getCategories, name="getCategories"),
    url(r'^insertCategory$', views.insertCategory, name="insertCategory"),
    url(r'^insertSession$', views.insertSession, name="insertSession"),
    url(r'^changeTimezone$', views.changeTimezone, name="changeTimezone"),
    url(r'^change_visibility$', views.change_visibility, name="change_visibility"),
    url(r'^change_volume$', views.change_volume, name="change_volume"),
    url(r'^profile/(?P<username>.+)/changeTimezone_profile$', views.changeTimezone_profile, name="changeTimezone_profile"),
    url(r'^profile/(?P<username>.+)/insertStartPageJournal$', views.insertStartPageJournal, name="insertStartPageJournal"),
    url(r'^getTodaysSessions$', views.getTodaysSessions, name="getTodaysSessions"),
    url(r'profile/(?P<username>.+)/$', views.profile, name="profile"),
    url(r'profile/(?P<username>.+)/get_statestic$', views.get_statestic, name="get_statestic"),
    url(r'profile/(?P<username>.+)/get_statestic_year$', views.get_statestic_year, name="get_statestic_year"),
    url(r'profile/(?P<username>.+)/get_statestic_month$', views.get_statestic_month, name="get_statestic_month"),
]
