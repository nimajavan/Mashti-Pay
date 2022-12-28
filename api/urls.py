from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('get_balance/', views.get_balance_pm, name="get_balance")
]
