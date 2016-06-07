import datetime
from django.db import models
from django.utils import timezone
from django import forms
from django.core import validators
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    # status_active = models.BooleanField()
    # list_display = ('status_active')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = u'User profiles'


class Link(models.Model):
    user_id = models.IntegerField()
    # link_title = models.TextField()
    link = models.TextField()
    link_description = models.TextField()
    creation_date = models.DateTimeField('date created', auto_now_add=True)
    private_flag = models.BooleanField()

    def __str__(self):
        return self.link

