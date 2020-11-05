from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', mainapp.views.main, name='main'),
   # path('login',mainapp.views.login, name='login'),
]