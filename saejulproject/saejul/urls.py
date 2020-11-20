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
from django.conf.urls import url
import mainapp.views
from django.conf import settings
import meetingapp.views
import registerapp.views
from mainapp import views
from meetingapp import views
from registerapp import views


handler400=''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mainapp.views.main, name='main'),
    path('recorde/',meetingapp.views.recorde, name='recorde'),
    path('login/', registerapp.views.login, name='login'),
    path('signup/', registerapp.views.signup, name='signup'),
    path('logout/', registerapp.views.logout, name='logout'),
    path('text/<int:record_id>' , meetingapp.views.text, name = 'contents') ,
    path('editText/<int:idx>/', meetingapp.views.editText, name='editText'),
    path('recode/<int:record_id>/delete',meetingapp.views.delete, name='delete'),
    path('recordtest/',meetingapp.views.recordtest,name='recordtest'),
    path('editdoc/<int:record_id>', meetingapp.views.editdoc, name='editdoc'),
    path('note/<int:record_id>', meetingapp.views.note, name='note'),



    path('login_app/', registerapp.views.login_app, name='login_app'),
    path('register_app/', registerapp.views.register_app, name='register_app'),
    path('record_app/<str:user_id>', meetingapp.views.record_app, name="record_app"),
    path('text_app/<str:record_id>', meetingapp.views.text_app, name="text_app"),
    path('mic_app/', meetingapp.views.mic_app, name="mic_app"),

    path('edit_text_app/', meetingapp.views.edit_text_app, name='edit_text_app'), 
    path('edit_speaker_app/<int:record_id>', meetingapp.views.edit_speaker_app, name='edit_speaker_app'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

