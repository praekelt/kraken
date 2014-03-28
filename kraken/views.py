from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from kraken.models import Profile, Request, Test, Server, generate_config_xml
from kraken import forms, tasks


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
    profile = Profile.objects.get(id=id)

    if request.method == "POST":
        form = forms.ProfileRequest(request.POST)
        if form.is_valid():
            prequest = form.save(commit=False)
            prequest.profile = profile

            rs = Request.objects.filter(profile=profile).order_by('-order')
            if rs:
                last_order = rs[0].order
            else:
                last_order = 0

            prequest.order = last_order + 1

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
def profile_down_request(request, id, rid):
    req = Request.objects.get(id=rid)
    profile = Profile.objects.get(id=id)
    rs = Request.objects.filter(profile=profile, order__gt=req.order)
    if rs:
        rs = rs.order_by('order')[0]
        this_order = req.order
        req.order = rs.order
        rs.order = this_order
        req.save()
        rs.save()

    return redirect('profile_view', id=id)


@login_required
def profile_up_request(request, id, rid):
    req = Request.objects.get(id=rid)
    profile = Profile.objects.get(id=id)
    rs = Request.objects.filter(profile=profile, order__lt=req.order)
    if rs:
        rs = rs.order_by('-order')[0]
        this_order = req.order
        req.order = rs.order
        rs.order = this_order
        req.save()
        rs.save()

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

    task = tasks.run_test.delay(test, generate_config_xml(profile))

    test.task_id = task.task_id
    test.save()

    return redirect('profile_view', id=id)
