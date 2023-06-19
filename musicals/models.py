from django.db import models
from django.contrib.auth.models import User

TYPE_CHOICES = (
    ('private','Private'),
    ('public','Public'),
    ('protected','Protected')
)
class Music(models.Model):
    title=models.CharField(max_length=500)
    type=models.CharField(max_length=10, choices=TYPE_CHOICES, default='public'
    )
    # Storing Integer Id to fasten the search
    owner=models.IntegerField()
    music=models.FileField(upload_to='musics/')
    class META:
        db_table="Music"

class Access(models.Model):
    # Storing emails to give access to emails which are not yet registered
    email=models.EmailField(max_length = 254)
    music=models.ForeignKey(Music, on_delete=models.CASCADE)
    class META:
        db_table="Access"
