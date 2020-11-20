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
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

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
            thread = threading.Thread(target = sttThread, args = (str(record_id),))
            thread.start()
        except :
            pass
        return redirect('recorde')
    else:
       # recorde = Record.objects.all().filter(user_id=request.user.username)
     
        recorde = Record.objects.all().filter(user_id =request.user.username)
        return render(request,'recorde.html',{'recorde':recorde})

@login_required
def text(request,record_id) :
    try:    
        filename = Record.objects.get(record_id=record_id).audio_file
        texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
        filename = str(filename)[:-4]
    except :
        pass    
    return render(request, 'text.html', {'texts' : texts, 'filename':filename, 'record_id':record_id})

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
        filename = Record.objects.get(record_id=record_id.record_id).audio_file
        texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
        filename = str(filename)[:-4]
        return render(request, 'text.html', {'texts' : texts, 'filename':filename} )
    else:
        return render(request, 'editText.html' ,{'text' : text} ) 


@login_required
def delete(request,record_id):
    recode = Record.objects.get(record_id=record_id)
    audio_file = '/home/ubuntu/saejulproject/saejulproject/media/'+str(recode.audio_file)[:-4]
    os.system('rm '+audio_file+'.wav '+audio_file+'.flac ')#+audio_file+'.txt')
    os.system('rm -rf '+audio_file)
    recode.delete()
    return redirect('recorde')

@login_required
def editdoc(request, record_id):
    record_id = record_id
    return render(request,'editdoc.html',{'record_id':record_id})

@login_required
def note(request, record_id):
    texts = Text.objects.all().filter(record_id=record_id).order_by('start_t')
    title = Record.objects.get(record_id=record_id).title
    location= Record.objects.get(record_id=record_id).location
    uploaded_date=Record.objects.get(record_id=record_id).uploaded_date
    return render(request,'note.html',{'texts' : texts, 'title':title, 'location':location, 'uploaded_date':uploaded_date})

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

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = [
            'record_id',
            'speaker_id',
            'speaker_name',
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

def removeSpec(s):
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
            return s[1:-1]
    return s

def mic_app(request):
    title = removeSpec(request.POST['title'])
    people = request.POST['people']
    location = removeSpec(request.POST['location'])
    user_id = removeSpec(request.POST['user_id'])

    audio_file = request.FILES['file']
    path = default_storage.save(str(audio_file), ContentFile(audio_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    print(title, people, location, user_id)    
    try:
        Record.objects.create(title=title, audio_file=audio_file,people=people,location=location,user_id=user_id)
        record_id = Record.objects.filter(user_id=user_id).last().record_id
        thread = threading.Thread(target = sttThread, args = (str(record_id),))
        thread.start()
    except :
        pass
    return JsonResponse({'result':'Success', 'status':1}, status=200) 

def edit_text_app(request):
    if request.method =="POST" :
        text = Text.objects.get(idx = request.POST['idx'])
        text.content = request.POST['content']
        text.save()

        print(request.POST['idx'])
        print(request.POST['content'])
    return JsonResponse({'result':'Success', 'status':1}, status=200) 

def edit_speaker_app(request, record_id):
    if request.method =="POST":
        # speaker_name        
        speaker_name = Text.objects.all().filter(speaker_id = request.POST['speaker_id'], record_id = record_id)
        speaker_name.update(speaker_name = request.POST['speaker_name'])
        return JsonResponse({'result':'Success', 'status':1}, status=200) 
    else :
        speaker = Text.objects.values('record_id', 'speaker_name', 'speaker_id').filter(record_id=record_id)
        

        speaker_serializer = SpeakerSerializer(speaker, many=True)
        speaker_json = speaker_serializer.data[:]
        return JsonResponse(speaker_json, status=200, safe=False)

def delete_app(request,record_id):
    recode = Record.objects.get(record_id=record_id)
    audio_file = '/home/ubuntu/saejulproject/saejulproject/media/'+str(recode.audio_file)[:-4]
    os.system('rm '+audio_file+'.wav '+audio_file+'.flac ')#+audio_file+'.txt')
    os.system('rm -rf '+audio_file)
    recode.delete()
    return JsonResponse({'result':'Success', 'status':1}, status=200)

def recordtest(request):
    return  render(request,'RecordTest.html')
