from django.shortcuts import render, redirect
from blog.models import Company, City, Meeting

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


def add(request):
	return render(request, 'meetings/add.html')