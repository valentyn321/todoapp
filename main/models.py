from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    added_date = models.DateTimeField()
    text = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    user_id = models.IntegerField(default=0)
