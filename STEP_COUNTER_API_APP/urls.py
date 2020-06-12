"""STEP_METER_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from STEP_COUNTER_API_APP import views

urlpatterns = [
    re_path('get_available_languages', views.get_available_languages, name='get_available_languages'),
    re_path('translate', views.page_translate, name='page_translate'),

    re_path('profile', views.user_profile, name='user_profile'),
    re_path('statistics/add', views.add_stat, name='add_stat'),
    re_path('statistics', views.stat, name='stat'),

    re_path('treners', views.get_treners, name='treners'),

    re_path('auth/code/confirm', views.code_confirm, name='code_confirm'),
    re_path('auth/code', views.device_auth, name='device_auth'),
    re_path('main_page', views.get_main_page, name='get_main_page'),
    re_path('check_payment', views.check_payment_upay, name='check_payment_upay'),
    re_path('follow/add/', views.create_follow, name='create_follow'),
    re_path('normativ/add/', views.normativ_add, name='normativ_add'),
    re_path('rate_trener/', views.rate_trener, name='rate_trener'),
    re_path('follow/filter/', views.filter_follow, name='filter_follow'),
    re_path('follow/activate/', views.activate_follow, name='activate_follow'),
    re_path('chat/get_all_chats/', views.get_all_chats, name='get_all_chats'),
    re_path('messages/mark_as_read/', views.mark_message_as_read, name='mark_message_as_read'),
    re_path('push_notifications/', views.push_notifications_add_token, name='push_notifications_add_token'),

    path('', views.get_main_page, name='main_page'),

]
