"""autotest URL Configuration

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
from django.urls import path
from apitest import apiviews
from apptest import appviews
from product import proviews
from bug import bugviews
from set import setviews
from webtest import webviews

# import xadmin


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('xadmin/', xadmin.site.urls),
    # path('test/',views.test),
    path('login/', apiviews.login, name='login'),
    path('home/', apiviews.home, name='home'),
    path('logout/', apiviews.logout, name='logout'),
    path('product_manage/', proviews.product_manage, name='product_manage'),
    path('apitest_manage/', apiviews.apitest_manage, name='apitest_manage'),
    path('apistep_manage/', apiviews.apistep_manage, name='apistep_manage'),
    path('apis_manage/', apiviews.apis_manage, name='apis_manage'),
    path('bug_manage/', bugviews.bug_manage, name='bug_manage'),
    path('set_manage/', setviews.set_manage, name='set_manage'),
    path('set_user/', setviews.set_user, name='set_user'),
    path('appcase_manage/', appviews.appcase_manage, name='appcase_manage'),
    path('appcasestep_manage/', appviews.appcasestep_manage, name='appcasestep_manage'),
    path('webcase_manage/', webviews.webcase_manage, name='webcase_manage'),
    path('webcasestep_manage/', webviews.webcasestep_manage, name='webcasestep_manage'),
    # path ('test_report/', appviews.test_report),

]
