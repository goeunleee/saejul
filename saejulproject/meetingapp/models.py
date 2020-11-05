from saejul.settings import MEDIA_ROOT, MEDIA_URL
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Record(models.Model):
     record_id = models.AutoField(primary_key=True) 
     user_id = models.CharField(max_length=100)
     audio_file = models.FileField()
     title = models.CharField(max_length=100)
     uploaded_date = models.DateTimeField(auto_now_add = True, blank=True)
     people = models.IntegerField()
     location = models.CharField(max_length=100)
     deleted = models.BooleanField(default=False)

class Text(models.Model): 
    idx = models.AutoField(primary_key =True)
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE)
    content = models.TextField(null=True)
    start_t = models.CharField(null=True, max_length=200)
    end_t = models.CharField(null=True,max_length=200)
    speaker_id = models.IntegerField(null=True) 
    speaker_name = models.CharField(null=True, max_length=100)
