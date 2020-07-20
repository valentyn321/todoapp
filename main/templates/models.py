from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")    

    def __str__(self):
        return self.title


class Todo(models.Model):
    added_date = models.DateTimeField(blank=True, null=True)
    text = models.CharField(max_length=256)
    status = models.BooleanField(default=False)
    user_id = models.IntegerField(default=0)
    deadline = models.DateTimeField(blank=True, null=True, default=timezone.now().strftime("%Y-%m-%d"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)