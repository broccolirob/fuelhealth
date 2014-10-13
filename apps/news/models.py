from urlparse import urlparse

from django.db import models
from django.contrib.auth.models import User
from apps.accounts.models import Profile


class Article(models.Model):
    title = models.CharField(max_length=120)
    url = models.URLField()
    points = models.IntegerField(default=1)
    flags = models.IntegerField(default=0)
    moderator = models.ForeignKey(Profile, related_name='moderated_articles')
    voters = models.ManyToManyField(Profile, related_name='liked_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def domain(self):
        return urlparse(self.url).netloc

    def __unicode__(self):
        return u"{}".format(self.title)


class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(Profile, related_name='comments_made')
    points = models.IntegerField(default=1)
    flags = models.IntegerField(default=0)
    voters = models.ManyToManyField(Profile, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"In {}, by {}".format(self.article, self.author)
