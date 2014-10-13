import json
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, render_to_response
from apps.accounts.models import Profile
from apps.news.forms import ProfileForm


def settings(request, user_id):
    user = Profile.objects.get(id=user_id)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = ProfileForm(instance=user)
    data = {'user': user, 'form': form}
    return render(request, 'settings.html', data)


def rankings(request):
    user_list = Profile.objects.all().order_by('-points')
    data = {'user_list': user_list}
    return render(request, 'rankings.html', data)


def signin(request):
    user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))

    if user and user.is_active:
        login(request, user)
        message = True
    else:
        message = False

    return HttpResponse(json.dumps(message))