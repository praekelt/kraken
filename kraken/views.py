from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from kraken.models import Profile, UserAgents, UserAgent, Request, Test
from kraken import forms

from lxml import etree
import urlparse

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
def agent_create(request, id):
    if request.method == "POST":
        form = forms.UserAgentsForm(request.POST)
        if form.is_valid():
            agent_map = form.save(commit=False)
            agent_map.save()

            return redirect('profile_add_agent', id=id)

    else:
        form = forms.UserAgentsForm()

    return render(request, "agent_create.html", {
        'form': form
    })

@login_required
def profile_index(request):
    profiles = Profile.objects.all()

    return render(request, "profile/index.html", {
        'profiles': profiles
    })

@login_required
def profile_view(request, id):
    profile = Profile.objects.get(id=id)

    return render(request, "profile/view.html", {
        'profile': profile
    })

@login_required
def profile_add_request(request, id):
    profile = Profile.objects.get(id=id)

    if request.method == "POST":
        form = forms.ProfileRequest(profile, request.POST)
        if form.is_valid():
            pr_form = form.cleaned_data

            print pr_form

            profile_request = Request.objects.create(
                profile=profile,
                http_auth=pr_form['http_auth'],
                path=pr_form['path'],
                think_time=pr_form['think_time'],
                username=pr_form['username'],
                password=pr_form['password'],
                method=pr_form['method'],
                content=pr_form['content'],
                content_type=pr_form['content_type'],
                dyn_variable=pr_form['dyn_variable']
            )

            profile_request.save()

            return redirect('profile_view', id=id)
    else:
        form = forms.ProfileRequest(profile)

    return render(request, "profile/add_request.html", {
        'profile': profile, 
        'form': form
    })

@login_required
def profile_delete_request(request, id, rid):
    Request.objects.get(id=rid).delete()

    return redirect('profile_view', id=id)

@login_required
def profile_add_agent(request, id):
    profile = Profile.objects.get(id=id)
    if request.method == "POST":
        form = forms.ProfileUserAgentForm(profile, request.POST)
        if form.is_valid():
            agent_map = form.save(commit=False)
            agent_map.profile = profile
            agent_map.save()

            return redirect('profile_view', id=id)

    else:
        form = forms.ProfileUserAgentForm(profile)

    return render(request, "profile/add_agent.html", {
        'profile': profile,
        'form': form
    })

@login_required
def profile_edit(request):
    return render(request, "profile/create_edit.html")

@login_required
def profile_create(request):
    if request.method == "POST":
        form = forms.ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()

            return redirect('profile_index')

    else:
        form = forms.ProfileForm()

    return render(request, 'profile/create_edit.html', {
        'form': form
    })

@login_required
def profile_run(request, id):
    profile = Profile.objects.get(id=id)

    # Build test doc structure
    root = etree.Element("tsung", loglevel="notice", version="1.0")
    clients = etree.SubElement(root, 'clients')
    servers = etree.SubElement(root, 'servers')
    load = etree.SubElement(root, 'load')
    options = etree.SubElement(root, 'options')
    sessions = etree.SubElement(root, 'sessions')

    # Setup clients - this really needs to be configurable for clusters etc.
    clients.append(etree.Element('client', host="localhost", cpu="4"))

    # Setup load phase (just one for now)
    arivalphase = etree.SubElement(load, 'arrivalphase', phase="1",
        duration=str(profile.phase_duration), unit="minute")

    arivalphase.append(etree.Element('users', 
        interarrival="%0.2f" % (profile.phase_rate/1000.0), unit="second"))
    
    # Setup user agents
    option = etree.SubElement(options, 'option', type="ts_http", name="user_agent")
    for agent in profile.useragent_set.all():
        agent_tag = etree.Element(
            'user_agent',
            probability=str(agent.probability)
        )
        agent_tag.text = agent.agent.agent # Wow that was a shit idea...
        option.append(agent_tag)

    # Setup requests
    session = etree.SubElement(sessions, 'session')
    first_request = True
    for prequest in profile.request_set.all():
        think_tag = etree.Element('think_time', random='true', value=str(prequest.think_time))
        request_tag = etree.Element('request')

        if first_request:
            # Add the whole path
            url = urlparse.urljoin(profile.url, prequest.path)
            first_request = False
        else:
            url = prequest.path

        if prequest.dyn_variable:
            request_tag.append(
                etree.Element('dyn_variable', name=prequest.dyn_variable)
            )

        if prequest.method == 'POST':
            request_tag.append(
                etree.Element('http', url=url, version='1.1', method='POST', 
                    content_type=prequest.content_type, 
                    content=prequest.content
                )
            )
        else:
            request_tag.append(
                etree.Element('http', url=url, version='1.1', method=prequest.method)
            )

        session.append(think_tag)
        session.append(request_tag)
    
    return HttpResponse(
        etree.tostring(root, pretty_print=True),
        content_type="text/plain"
    )
