from urllib import request

from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponse
from .models import *
import random
import string
from django.contrib.auth.decorators import login_required


def register(request):
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect("login")

  else:
    form = UserCreationForm()

  return render(request, 'register.html', {'form': form})


def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
      user = form.get_user()
      auth_login(request, user)
      return redirect("home")

  else:
    form = AuthenticationForm()

  return render(request, 'login.html', {'form': form})

def logout(request):
  logout(request)
  return redirect('login')

def randomCode():
  code = "".join(random.choices(string.ascii_letters, k=8))

  while True:
    if not shortURL.objects.filter(short_code=code).exists():
      return code


@login_required(login_url='login')
def home(request):
  if request.method == "POST":
    if request.POST.get("url"):
      user_input = request.POST.get("url")
      if user_input[:4] != "http":
        user_input = "https://" + user_input

      if shortURL.objects.filter(url=user_input).exists():  # if the link is already stored
        return render(request,
                      "home.html",
                      {"short_code": shortURL.objects.filter(url=user_input).first().short_code})

      short_code = randomCode()

      new_short_url = shortURL.objects.create(url=user_input, short_code=short_code, author= request.user.username)
      return render(request, "home.html", {"short_code": new_short_url.short_code,"profile_name": request.user.username})

  return render(request, "home.html", {"profile_name": request.user.username})

def redirectPage(request, short_code):
  url_object = get_object_or_404(shortURL, short_code=short_code)
  if url_object.url:
    shortURL.objects.filter(short_code=short_code).update(click_count=F('click_count') + 1)

  return render(request, 'redirect.html', {'original_url': url_object.url, "profile_name": request.user.username})

@login_required(login_url='login')
def profile(request):
  data = {}
  username = request.user.username

  user_urls = shortURL.objects.filter(author=username)

  # Store data in a dictionary
  data['urls'] = user_urls

  return render(request, "profile.html", data)