from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('buy_order/', views.Buy.as_view(), name='buy_order'),
    path('sell_order/', views.Sell.as_view(), name='sell_order'),
    path('order_buy_show/<int:order_id>/', views.BuyShow.as_view(), name='order-buy-show'),
    path('order_sell_show/', views.SellShow.as_view(), name='order_sell_show'),
    path('form_buy_sell/', views.FormBuySell.as_view(), name='form_buy_sell'),

]
