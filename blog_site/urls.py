from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('all-posts/', views.AllPostsView.as_view(), name='all-posts'),
]