from django.shortcuts import render
from datetime import date
from django import http
from django.http import JsonResponse
from django.views.generic.base import View
from .models import Text
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import redirect
from rest_framework import serializers
from .models import Record,User
import os
import threading
# Create your views here.
from django.contrib.auth.decorators import login_required

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

@login_required
def text(request,record_id) :
    try:    
        filename = Record.objects.get(record_id=record_id).audio_file
        texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
        filename = str(filename)[:-4]
    except :
        pass    
    return render(request, 'text.html', {'texts' : texts, 'filename':filename} )
@login_required
def editText(request,idx) :
    text = Text.objects.get( idx = idx)
    record_id = text.record_id
    speaker_id = text.speaker_id
    
    if request.method =="POST" :
        # content
        text.content = request.POST['content'] 
        text.save()

        # speaker_name        
        speaker_name = Text.objects.all().filter(speaker_id=speaker_id, record_id=record_id)
        speaker_name.update(speaker_name = request.POST['speaker_name'])

        # texts
        texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
        return render(request, 'text.html', {'texts' : texts} )
    else:
        return render(request, 'editText.html' ,{'text' : text} ) 

def sttThread(record_id):
    print(os.system('/opt/test.sh '+record_id))

@login_required
def recorde(request):
    if request.user.is_anonymous:
        return redirect("/login/")
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
        except :
            pass
        return redirect('recorde')
    else:
        #recorde = Record.objects.all().filter(user_id=request.user.username).first()
        recorde = Record.objects.all()
        return render(request,'recorde.html',{'recorde':recorde})

@login_required
def delete(request,record_id):
    recode = Record.objects.get(record_id=record_id)
    audio_file = '/home/ubuntu/saejulproject/saejulproject/media/'+str(recode.audio_file)[:-4]
    os.system('rm '+audio_file+'.wav '+audio_file+'.flac ')#+audio_file+'.txt')
    os.system('rm -rf '+audio_file)
    recode.delete()
    return redirect('recorde')

#######################
# model Class
class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        exclude = [
            'user_id',
            'audio_file',
            'deleted'
        ]

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        exclude = [
            'record_id',
        ]

#######################
# App
def record_app(request, user_id):
    record = Record.objects.all().filter(user_id=user_id)
    record_serializer = RecordSerializer(record, many=True)
    record_json = record_serializer.data[:]
    return JsonResponse(record_json, status=200, safe=False)

def text_app(request, record_id):
    text = Text.objects.all().filter(record_id=record_id)
    text_serializer = TextSerializer(text, many=True)
    text_json = text_serializer.data[:]
    return JsonResponse(text_json, status=200, safe=False)
