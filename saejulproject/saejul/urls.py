"""saejul URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls.static import static
import mainapp.views
from django.conf import settings
import meetingapp.views
import registerapp.views
from mainapp import views
from meetingapp import views
from registerapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.views.main, name='main'),
    path('recorde/',meetingapp.views.recorde, name='recorde'),
    path('login/', registerapp.views.login, name='login'),
    path('signup/', registerapp.views.signup, name='signup'),
    path('logout/', registerapp.views.logout, name='logout'),
    path('app_login/', registerapp.views.app_login),
    path('contents/<int:record_id>' , meetingapp.views.contents, name = 'contents') ,
    path('detail/<int:idx>/', meetingapp.views.detail, name='detail'),
    path('recode/<int:record_id>/delete',meetingapp.views.delete, name='delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

