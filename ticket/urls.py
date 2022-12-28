from django.urls import path
from . import views

app_name = 'ticket'

urlpatterns = [
    path('ticket/<int:ticket_id>/', views.SingleTicketView.as_view(), name='single_ticket'),
    path('ticket_show/', views.TicketShow.as_view(), name='ticket_show'),
    path('ticket_form/', views.TicketFormView.as_view(), name='ticket_formView'),
]
