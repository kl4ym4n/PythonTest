import datetime
from django.db import models
from django.utils import timezone
from django import forms
from django.core import validators
from django.contrib.auth.models import User


class Link(models.Model):
    user_id = models.IntegerField()
    link_title = models.CharField(max_length=100, default='none')
    link = models.TextField()
    link_description = models.TextField()
    creation_date = models.DateTimeField('date created', auto_now_add=True)
    private_flag = models.BooleanField()

    def __str__(self):
        return self.link
