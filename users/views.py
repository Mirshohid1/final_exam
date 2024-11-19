from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import CreateView, FormView
from django.views import View
from .forms import RegisterForm, LoginForm, EditProfileForm
from .models import CustomUser, FollowedUserNotification, CommentPostNotification


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('blog_site:home')

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
    success_url = reverse_lazy('users:login')

class Logout(LogoutView):
    next_page = reverse_lazy('blog_site:home')

class ProfileView(TemplateView):
    model = CustomUser
    template_name = 'user-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['customuser'] = get_object_or_404(CustomUser, username=username)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class EditProfileView(UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'edit-profile.html'
    success_url = reverse_lazy('blog_site:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class Subscribe(View):
    def post(self, request, username1, username2, *args, **kwargs):
        user1 = get_object_or_404(CustomUser, username=username1)
        user2 = get_object_or_404(CustomUser, username=username2)
        user1.subscriptions.add(user2)

        FollowedUserNotification.objects.create(
            user=user2,
            followed_user=username1,
            is_read=False,
        )

        return redirect(reverse('users:user-profile', kwargs={'username': username2}))

class Unsubscribe(View):
    def post(self, request, username1, username2, *args, **kwargs):
        user1 = get_object_or_404(CustomUser, username=username1)
        user2 = get_object_or_404(CustomUser, username=username2)
        user1.subscriptions.remove(user2)

        return redirect(reverse('users:user-profile', kwargs={'username': username2}))

class ReadNotificationFollow(View):
    def get(self, request, pk, username, *args, **kwargs):
        notification = get_object_or_404(FollowedUserNotification, pk=pk)
        notification.is_read = True
        notification.save()

        return redirect(reverse('users:user-profile', kwargs={'username': username}))

class ReadNotificationComment(View):
    def get(self, request, pk, pk2, *args, **kwargs):
        notification = get_object_or_404(CommentPostNotification, pk=pk)
        notification.is_read = True
        notification.save()

        return redirect(reverse('blog_site:post-detail', kwargs={'pk': pk2}))