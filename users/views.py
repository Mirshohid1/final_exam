from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import CustomUser
from .forms import UserCreationForm

class Dashboard(TemplateView):
    template_name = 'index.html'
