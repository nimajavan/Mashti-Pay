from django.contrib import admin
from .models import User, Profile, VoucherWallet, Notification


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'last_name', 'id_card_status', 'bank_card_pic_status', 'vip_user']
    list_filter = ['vip_user', 'id_card_status', 'bank_card_pic_status']


    # def is_vip(self, modeladmin, request, queryset):
    #     queryset.update(vip_user=True)
    #
    # admin.site.add_action(is_vip, 'is vip')


admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(VoucherWallet)
admin.site.register(Notification)
