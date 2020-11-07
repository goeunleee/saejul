from django.shortcuts import render
from datetime import date
from django import http
from django.views.generic.base import View
from .models import Text
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import Record,User
import os
import threading
# Create your views here.

class AudioFileCreateViewMixin(View):
    model = None
    create_field = None

    def create_object(self, audio_file):
        return self.model.objects.create(**{self.create_field: audio_file})

    def post(self, request):
        audio_file = request.FILES.get('audio_file', None)

        if audio_file is None:
            return http.HttpResponseBadRequest()

        result = self.create_object(audio_file)
        # print result.audio_file.url
        return http.JsonResponse({
            'id': result.pk,
            'url': result.audio_file.url,
        }, status=201)

def contents(request,record_id) :
    filename = Record.objects.get(record_id=record_id).audio_file
    texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
    filename = str(filename)[:-4]
    return render(request, 'content.html', {'texts' : texts, 'filename':filename} )

def detail(request,idx) :
    text = Text.objects.get( idx = idx)
    record_id = text.record_id
    if request.method =="POST" :
        text.content = request.POST['content'] 
        text.save()
        texts = Text.objects.all().filter(record_id=record_id)
        return render(request, 'content.html', {'texts' : texts} )
    else:
        return render(request, 'detail.html' ,{'text' : text} ) 

def sttThread(record_id):
    print(os.system('/opt/test.sh '+record_id))

def recorde(request):
    if request.method =='POST':
        title = request.POST['title']
        audio_file = request.FILES['audio_file']
        people = request.POST['people']
        location = request.POST['location']
        user_id = User.objects.filter(username = request.user.username).first()
        try:
            Record.objects.create(title=title, audio_file=audio_file,people=people,location=location,user_id=user_id )
            record_id = Record.objects.filter(user_id=user_id).last().record_id
#            print(os.system('/opt/test.sh '+str(record_id)))
            thread = threading.Thread(target = sttThread, args = (str(record_id),))
            thread.start()
        except: 
            pass
        return redirect('recorde')
    else:
        #recorde = Record.objects.all().filter(user_id=request.user.username).first()
        recorde = Record.objects.all()
        return render(request,'recorde.html',{'recorde':recorde})

def delete(request,record_id):
    recode = Record.objects.get(record_id=record_id)
    audio_file = '/home/ubuntu/saejulproject/saejulproject/media/'+str(recode.audio_file)[:-4]
    os.system('rm '+audio_file+'.wav '+audio_file+'.flac ')#+audio_file+'.txt')
    os.system('rm -rf '+audio_file)
    recode.delete()
    return redirect('recorde')
