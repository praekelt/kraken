from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import models


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    class Meta:
        model = User
        exclude = (
            'email', 'username', 'is_staff', 'is_active', 'is_superuser',
            'last_login', 'date_joined', 'groups', 'user_permissions'
        )

class ServerForm(forms.ModelForm):
    cores = forms.IntegerField(initial=2, help_text = "Number of CPU cores")
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.Server

class ProfileForm(forms.ModelForm):
    url = forms.CharField(required=True, initial="http://")
    phase_duration = forms.IntegerField(initial=5, help_text = "Minutes")
    phase_rate = forms.IntegerField(initial=2000, help_text = "Milliseconds")

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.Profile

class UserAgentsForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = models.UserAgents

class ProfileUserAgentForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('submit', 'Submit'))

    probability = forms.IntegerField(initial=100, help_text = "Percentage chance of this agent being chosen in a request")

    def __init__(self, profile, *args, **kwargs):
        super(ProfileUserAgentForm, self).__init__(*args, **kwargs)
        self.profile = profile

        self.fields['agent'] = forms.ModelChoiceField(
            queryset=models.UserAgents.objects.all(),
            help_text='<a href="/agent/create/%s" class="btn btn-success btn-small">Create new agent</a>' % profile.id
        )


    class Meta:
        model = models.UserAgent
        exclude = ('profile')

class ProfileRequest(forms.ModelForm):
    class Meta:
        model = models.Request
        exclude = ('profile', 'order')

    path = forms.CharField(required=True, initial="/")
    think_time = forms.IntegerField(initial="1")

    method = forms.ChoiceField(required=True, initial="GET",
        choices=(
            ('GET', 'GET'),
            ('POST', 'POST')
        )
    )
    content = forms.CharField(required=False)
    content_type = forms.CharField(required=False)

    dyn_variable = forms.CharField(required=False)

    http_auth = forms.BooleanField(required=False)

    username = forms.CharField(required=False)
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.add_input(Submit('submit', 'Submit'))
