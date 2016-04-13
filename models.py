import datetime
from django.db import models
from django.utils import timezone
from django import forms
from django.core import validators
from django.contrib.auth.models import User


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'

# class UserProfile(models.Model):
#     user = models.OneToOneField(User)
#     activation_key = models.CharField(maxlength=40)
#     key_expires = models.DateTimeField()

# class RegistrationForm(forms.Manipulator):
#
#     def __init__(self):
#         self.fields = (
#             forms.TextField(field_name='username',
#                             length=30, maxlength=30,
#                             is_required=True, validator_list=[validators.isAlphaNumeric,
#                                                               self.isValidUsername]),
#             forms.EmailField(field_name='email',
#                              length=30,
#                              maxlength=30,
#                              is_required=True),
#             forms.PasswordField(field_name='password1',
#                                 length=30,
#                                 maxlength=60,
#                                 is_required=True),
#             forms.PasswordField(field_name='password2',
#                                 length=30, maxlength=60,
#                                 is_required=True,
#                                 validator_list=[validators.AlwaysMatchesOtherField('password1',
#                                                                                    'Passwords must match.')]),
#             )
#
#     def isValidUsername(self, field_data, all_data):
#         try:
#             User.objects.get(username=field_data)
#         except User.DoesNotExist:
#             return
#         raise validators.ValidationError('The username "%s" is already taken.' % field_data)
#
#     def save(self, new_data):
#         u = User.objects.create_user(new_data['username'],
#                                      new_data['email'],
#                                      new_data['password1'])
#         u.is_active = False
#         u.save()
#         return u