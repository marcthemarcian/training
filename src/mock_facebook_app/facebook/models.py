from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField()
    datetime = models.DateTimeField('date posted')


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name="likes")


class Comment(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name="comments")
    text = models.TextField()
    datetime = models.DateTimeField('date posted')
