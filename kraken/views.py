from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from kraken.models import Profile, UserAgents, UserAgent, Request, Test, Server
from kraken import forms, tasks

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
def server_index(request):
    servers = Server.objects.all()

    return render(request, "servers/index.html", {
        'servers': servers
    })

@login_required
def server_create(request):
    if request.method == "POST":
        form = forms.ServerForm(request.POST)
        if form.is_valid():
            server = form.save(commit=False)
            server.save()

            return redirect('server_index')
    else:
        form = forms.ServerForm()

    return render(request, "servers/create_edit.html", {
        'form': form
    })

@login_required
def server_edit(request, id):
    server = Server.objects.get(id=id)

    if request.method == "POST":
        form = forms.ServerForm(request.POST, instance=server)
        if form.is_valid():
            server = form.save(commit=False)
            server.save()

            return redirect('server_index')
    else:
        form = forms.ServerForm(instance=server)

    return render(request, "servers/create_edit.html", {
        'form': form,
        'server': server
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

    if request.method == "POST":
        profile = Profile.objects.get(id=id)
        form = forms.ProfileRequest(request.POST)
        if form.is_valid():
            prequest = form.save(commit=False)
            prequest.profile = profile
            prequest.save()

            return redirect('profile_view', id=id)
    else:
        form = forms.ProfileRequest()

    return render(request, "profile/add_edit_request.html", {
        'profile': profile, 
        'form': form
    })

@login_required
def profile_edit_request(request, id, rid):
    prequest = Request.objects.get(id=rid)

    if request.method == "POST":
        form = forms.ProfileRequest(request.POST, instance=prequest)
        if form.is_valid():
            prequest = form.save(commit=False)
            prequest.save()

            return redirect('profile_view', id=id)
    else:
        form = forms.ProfileRequest(instance=prequest)

    return render(request, "profile/add_edit_request.html", {
        'profile': prequest.profile,
        'prequest': prequest,
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
def test_report(request, id):
    test = Test.objects.get(id=id)

    return render(request, "test_report.html", {
        'test': test
    })

@login_required
def profile_edit(request, id):
    profile = Profile.objects.get(id=id)
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()

            return redirect('profile_index')

    else:
        form = forms.ProfileForm(instance=profile)

    return render(request, 'profile/create_edit.html', {
        'form': form
    })

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

    test = Test.objects.create(
        profile=profile,
        running=False
    )

    # Build test doc structure
    root = etree.Element("tsung", loglevel="notice", version="1.0")
    clients = etree.SubElement(root, 'clients')
    servers = etree.SubElement(root, 'servers')
    load = etree.SubElement(root, 'load')
    options = etree.SubElement(root, 'options')
    sessions = etree.SubElement(root, 'sessions')

    # Setup clients - this really needs to be configurable for clusters etc.
    server_list = Server.objects.all()
    for server in server_list:
        clients.append(etree.Element('client', host=server.hostname,
            cpu=str(server.cores)))

    # Setup target server
    profile_server = urlparse.urlparse(profile.url)
    port = profile_server.port
    # but urlparse is retarded...
    if not port:
        if profile_server.scheme == 'http':
            port = 80
        elif profile_server.scheme == 'https':
            port = 443
        else:
            raise Exception('This is for testing webservers...')

    server = etree.SubElement(servers, 'server', host=profile_server.hostname,
        port=str(port), type="tcp")

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
    session = etree.SubElement(sessions, 'session', name=profile.name.lower(), probability='100', type='ts_http')
    first_request = True
    for prequest in profile.request_set.all():
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
                    contents=prequest.content
                )
            )
        else:
            request_tag.append(
                etree.Element('http', url=url, version='1.1', method=prequest.method)
            )

        if prequest.think_time:
            think_tag = etree.Element('thinktime', random='true', 
                value=str(prequest.think_time))
            session.append(think_tag)

        session.append(request_tag)

    task = tasks.run_test.delay(test, etree.tostring(root, pretty_print=True, 
            doctype='<!DOCTYPE tsung SYSTEM "/usr/share/tsung/tsung-1.0.dtd">'))

    test.task_id = task.task_id
    test.save()
    
    return redirect('profile_index')
