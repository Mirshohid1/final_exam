from django.urls import path
import views

app_name = 'users'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard')
]