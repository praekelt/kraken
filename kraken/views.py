from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from kraken.models import Profile, UserAgents, UserAgent, Request, Test


@login_required
def index(request):
    profiles = Profile.objects.all()

    return render(request, "index.html", {
        'profiles': profiles
    })
