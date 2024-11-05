from django.urls import path
import views

app_name = 'users'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('register/', views.RegisterView.as_view(), 'register'),
]