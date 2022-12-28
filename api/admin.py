from django.contrib import admin
from .models import DollarPriceModel, DollarPriceHistory


class DollarPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['price_history', 'created_at']


admin.site.register(DollarPriceModel)
admin.site.register(DollarPriceHistory, DollarPriceHistoryAdmin)
