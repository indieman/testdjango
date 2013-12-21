import datetime

from django.db import models
from django.contrib.comments.models import Comment
from django.contrib.contenttypes import generic

class Hashtag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return u'%s' % self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(default=datetime.datetime.utcnow)
    text = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True, null=True)
    comments = generic.GenericRelation(Comment, object_id_field='object_pk')

    def __unicode__(self):
        return u'%s' % self.title