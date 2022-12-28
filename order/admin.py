from django.contrib import admin
from .models import *


class OrderBuyAdmin(admin.ModelAdmin):
    list_display = ['user', 'dollar_price', 'quantity', 'total_price', 'paid', 'condition', 'tracking_code']
    list_filter = ['paid', 'condition']
    search_fields = ['user__username']

    def total_price(self, obj):
        order_price = OrderBuy.objects.get(id=obj.id).total_price
        return order_price


admin.site.register(OrderBuy, OrderBuyAdmin)
admin.site.register(OrderSell)
