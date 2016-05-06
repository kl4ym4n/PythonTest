from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    # clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        # try:
        #     User._default_manager.get(email=email)
        # except User.DoesNotExist:
        return email
        #raise forms.ValidationError('duplicate email')

    # modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()

        return user

class LinkForm(forms.Form):
    link = forms.CharField(label='Link', widget=forms.widgets.TextInput(attrs={'placeholder': 'Link',
                                                                  'class': 'input-block-level'}))


    link_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description',
                                                           'rows': 8,
                                                           'class': 'input-block-level'}))
    private_flag = forms.BooleanField()
    class Meta:
        model = Link
        fields = ('user_id', 'link', 'link_description', 'creation_date', 'private_flag')