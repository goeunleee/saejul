import registerapp
from django.contrib import admin
from django.urls import path

urlpatterns = [
    
  path('login/', registerapp.views.login, name='login'),
  path('signup/', registerapp.views.signup, name='signup'),
  path('logout/', registerapp.views.logout, name='logout'),
  path('app_login/', registerapp.views.app_login),


]