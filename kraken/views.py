from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from kraken.models import Profile, UserAgents, UserAgent, Request, Test
from kraken import forms


@login_required
def index(request):
    profiles = Profile.objects.all()

    return render(request, "index.html", {
        'profiles': profiles
    })

@login_required
def accounts_profile(request):
    if request.method == "POST":
        form = forms.UserForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = forms.UserForm(instance=request.user)

    return render(request, "accounts_profile.html", {
        'form': form
    })

@login_required
def profile_index(request):
    profiles = Profile.objects.all()

    return render(request, "profile/index.html", {
        'profiles': profiles
    })
