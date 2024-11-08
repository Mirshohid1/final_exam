from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Post


class HomePageView(TemplateView):
    template_name = 'index.html'

class AllPostsView(TemplateView):
    model = Post
    template_name = 'all-posts.html'
