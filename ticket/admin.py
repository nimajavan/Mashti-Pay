from django.contrib import admin
from .models import Ticket, ReplyTicket


class ReplyTicketInline(admin.TabularInline):
    model = ReplyTicket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_filter = ('status', 'user')
    list_display = ('id', 'title', 'user', 'updated_at', 'status')
    inlines = [ReplyTicketInline]


class RepTicketAdmin(admin.ModelAdmin):
    list_display = ('rep_body',)


admin.site.register(ReplyTicket, RepTicketAdmin)
