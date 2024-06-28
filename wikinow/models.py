from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from tinymce import models as tinymce_models
from django.conf import settings


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)

    def __str__(self):
        return self.username

class Entry(models.Model):
    title = models.CharField(max_length=50, null=True)
    content = tinymce_models.HTMLField(null=True)
    thumbnail = models.URLField(null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.title