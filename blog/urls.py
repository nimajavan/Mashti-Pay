from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('show_comments/', views.ApiTest.as_view())
]
