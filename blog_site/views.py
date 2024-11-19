from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Post, Comment
from users.models import CommentPostNotification
from .forms import PostForm, CommentPostForm


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'show-post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentPostForm()
        context['comments'] = self.object.comment_set.all()

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

    def post(self, request, **kwargs):
        post = self.get_object()
        form = CommentPostForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            CommentPostNotification.objects.create(
                user = post.author,
                comment_post = post.pk,
                is_read = False
            )

            return redirect(reverse('blog_site:post-detail', kwargs={'pk': post.pk}))
        return self.get(request, **kwargs)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'confirm_delete-comment.html'
    success_url = reverse_lazy('blog_site:all-posts')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class AllPostsView(ListView):
    model = Post
    template_name = 'all-posts.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'create-post.html'
    success_url = reverse_lazy('blog_site:all-posts')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'edit-post.html'
    form_class = PostForm
    success_url = reverse_lazy('blog_site:all-posts')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'confirm_delete-post.html'
    success_url = reverse_lazy('blog_site:all-posts')
    login_url = 'users:login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context['followed_notifications'] = self.request.user.followed_user_notifications.filter(is_read=False)
            context['comment_notifications'] = self.request.user.comment_post_notifications.filter(is_read=False)
        else:
            context['followed_notifications'] = []
            context['comment_notifications'] = []

        return context