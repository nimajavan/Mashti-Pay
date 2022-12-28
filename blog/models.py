from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User


class Blog(models.Model):
    title = models.CharField(max_length=200)
    intro = models.TextField(null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog', null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=50)
    body = models.TextField()

    def __str__(self):
        return self.name
