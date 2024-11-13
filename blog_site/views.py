from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView, FormView
from .models import Post, CustomUser
from .forms import CreatePostForm, RegisterForm, LoginForm
from django.contrib.auth import authenticate, login


class HomePageView(TemplateView):
    template_name = 'index.html'

class PostDetailView(DetailView):
    model = Post
    template_name = 'show-post.html'

class AllPostsView(ListView):
    model = Post
    template_name = 'all-posts.html'
    context_object_name = 'posts'

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('all-posts')
    login_url = 'login'

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit-post.html'
    success_url = reverse_lazy('all-posts')
    login_url = 'login'

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid email or password')
            return self.form_invalid(form)

class RegisterView(CreateView):
    model = CustomUser
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')