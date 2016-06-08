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
