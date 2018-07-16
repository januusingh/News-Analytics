from django.db import models
from datetime import datetime
import uuid

# Create your models here.
class Post(models.Model):
    article = models.TextField(default=None, null=True)
    author = models.TextField(default=None, null=True)
    website = models.TextField(default=None, null=True)
    published = models.DateTimeField(null=True, blank=True)
    topics = models.TextField(default=None, null=True)

    def __str__(self):
        return self.author + " " + str(self.published) + " " + self.topics + " " + self.website

class Posts(models.Model):
    postID = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    article = models.TextField(default=None, null=True)
    author = models.TextField(default=None, null=True)
    website = models.TextField(default=None, null=True)
    published = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return str(self.postID)

class Topic(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    topic = models.TextField(default=None, null=True)
    published = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.topic + " " + str(self.post)

class Hot(models.Model):
    date = models.DateTimeField(null=True, blank=True)

class Newspaper(models.Model):
    website = models.TextField(default=None, null=True)
