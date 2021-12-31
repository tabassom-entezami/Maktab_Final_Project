from django.db import models
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from .models import *
from accounts.models import *
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.decorators import login_required


@login_required
def home_page(re):
    return render(re, "Home.html")
# Create your views here.


