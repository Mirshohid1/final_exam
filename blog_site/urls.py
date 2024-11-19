from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'blog_site'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('post-create/', views.CreatePostView.as_view(), name='post-create'),
    path('post-edit/<int:pk>/', views.EditPostView.as_view(), name='post-edit'),
    path('post-delete/<int:pk>/', views.DeletePostView.as_view(), name='post-delete'),
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('comment-delete/<int:pk>/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('all-posts/', views.AllPostsView.as_view(), name='all-posts'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)