from django.shortcuts import render, redirect
from django.views import View
from .forms import TicketForm
from .models import Ticket
from django.core.paginator import Paginator
from django.contrib import messages


class SingleTicketView(View):
    single_ticket_template = 'ticket/single_show.html'

    def get(self, request, ticket_id):
        ticket_obj = Ticket.objects.get(id=ticket_id)
        context = {'ticket': ticket_obj}
        return render(request, self.single_ticket_template, context)


class TicketShow(View):
    def get(self, request):
        buy_obj = Ticket.objects.filter(user_id=request.user.id)
        paginator = Paginator(buy_obj, 2)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'ticket/ticket.html', {'ticket': page_obj, 'page_num': page})


class TicketFormView(View):
    ticket_form = TicketForm

    def get(self, request):
        form = self.ticket_form()
        context = {'form': form}
        return render(request, 'ticket/ticket_form.html', context)

    def post(self, request):
        form = self.ticket_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(user_id=request.user.id, title=cd['title'], body=cd['body'])
            ticket_obj.save()
            messages.success(request, 'تیکت شما با موفقیت ارسال شد , منتظر پاسخگویی تیم پشتیبانی باشید')
            return redirect('ticket:ticket_show')
        else:
            messages.error(request, 'ارسال تیکت با مشکل مواجه شد, لطفا دوباره امتحان کنید')
            return redirect('ticket:ticket_formView')
