from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('user-profile/<str:username>/', views.ProfileView.as_view(), name='user-profile'),
    path('edit-profile/<int:pk>/', views.EditProfileView.as_view(), name='edit-profile'),

    path('follow/<str:username1>/<str:username2>/', views.Subscribe.as_view(), name='follow-user'),
    path('unfollow/<str:username1>/<str:username2>/', views.Unsubscribe.as_view(), name='unfollow-user'),
    path('notification-follow/<int:pk>/<str:username>/', views.ReadNotificationFollow.as_view(), name='notification-follow'),
    path('notification-comment/<int:pk>/<int:pk2>/', views.ReadNotificationComment.as_view(), name='notification-comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)