from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=120)
    url = models.URLField()
    points = models.IntegerField(default=1)
    moderator = models.ForeignKey(User, related_name='moderated_articles')
    voters = models.ManyToManyField(User, related_name='liked_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def domain(self):
        return urlparse(self.url).netloc

    def __unicode__(self):
        return "{}".format(self.title)


# class Comment(models.Model):
#     article = models.ForeignKey(Article, related_name='comments')
#     body = models.TextField()