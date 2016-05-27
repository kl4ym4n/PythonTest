from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
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
        # raise forms.ValidationError('duplicate email')

    # modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False  # not active until he opens activation link
            user.save()

        return user


class LinkForm(ModelForm):
    link = forms.CharField(label='Link', widget=forms.widgets.TextInput(attrs={'placeholder': 'Link',
                                                                               'class': 'input-block-level'}))

    link_description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description',
                                                                    'class': 'input-block-level'}))
    private_flag = forms.BooleanField(required=False)

    class Meta:
        model = Link
        fields = ('link', 'link_description', 'private_flag')


class UserProfileForm(ModelForm):
    # login = forms.CharField(label='Login:', widget=forms.widgets.TextInput())
    # name = forms.CharField(label='Name:', widget=forms.widgets.TextInput())
    # surname = forms.CharField(label='Surname:', widget=forms.widgets.TextInput())
    # mail = forms.CharField(label='Email:', widget=forms.widgets.TextInput())
    # password = forms.CharField(label='Password:', widget=forms.widgets.TextInput())
    # status = forms.BooleanField(label='Active status:')
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        #fields = ('login', 'name', 'surname', 'mail', 'password', 'status')
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
        #fields = ('email',)
