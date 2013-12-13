from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
import models


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = (
            'email', 'username', 'is_staff', 'is_active', 'is_superuser',
            'last_login', 'date_joined', 'groups', 'user_permissions'
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile

class UserAgentsForm(forms.ModelForm):
    class Meta:
        model = models.UserAgents

class ProfileUserAgentForm(forms.ModelForm):
    class Meta:
        model = models.UserAgent

class ProfileRequest(forms.Form):
    def __init__(self, profile, *args, **kwargs):
        super(ProfileRequest, self).__init__(*args, **kwargs)
        self.profile = profile

    path = forms.CharField(required=True, initial="/")
    think_time = forms.IntegerField(initial="1")

    method =

    http_auth = forms.BooleanField(required=False)
    csrf_auth = forms.BooleanField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)
