from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from account.models import Profile
from api.models import DollarPriceModel
from .forms import *


class Buy(View):
    def post(self, request):
        profile_user = Profile.objects.get(user_id=request.user.id)
        inventory = profile_user.buy_sum
        if inventory <= 9000000 and profile_user.vip_user is False or inventory > 9000000 and profile_user.vip_user:
            form = BuyForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                order_obj = OrderBuy.objects.create(user_id=request.user.id,
                                                    dollar_price=DollarPriceModel.objects.get().price,
                                                    quantity=cd['quantity'])
                order_obj.save()
                messages.success(request, 'سفارش شما ثبت شد لطفا جهت نهایی شدن, اقدام به پرداخت کنید.')
                order = OrderBuy.objects.get(id=order_obj.id)
                order_id = order.id
                return render(request, 'order/order_buy.html', {'order': order, 'order_id': order_id})
            else:
                messages.error(request, 'متاسفانه خاطایی رخ داده است !است لطفا دوباره تلاش کنید.')
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'سقف مجاز شما به حد نصاب خود رسیده لطفا اقدام به احراز هویت کنید')
            return redirect(request.META.get('HTTP_REFERER'))


class Sell(View):
    def post(self, request):
        form = SellForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            order_obj = OrderSell.objects.create(user_id=request.user.id, voucher_code=cd['voucher_code'],
                                                 activate_code=cd['activate_code'])
            order_obj.save()
            messages.success(request, 'سفارش شما با موفقیت ثبت شد در کمترین زمان ممکن به حساب شما واریز خواهد شد')
            return redirect('order:order_sell_show')
        else:
            messages.error(request, 'متاسفانه خاطایی رخ داده است ! لطفا دوباره امتحان کنید.')
            return redirect(request.META.get('HTTP_REFERER'))


class BuyShow(View):
    def get(self, request, order_id):
        pass


class SellShow(View):
    def get(self, request):
        buy_obj = OrderSell.objects.filter(user_id=request.user.id)
        paginator = Paginator(buy_obj, 2)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'order/order_sell.html', {'order': page_obj, 'page_num': page})


class FormBuySell(View):
    def get(self, request):
        dollar_price = DollarPriceModel.objects.get().price
        form_buy = BuyForm()
        form_sell = SellForm()
        context = {'form_buy': form_buy, 'form_sell': form_sell, 'dollar_price': dollar_price}
        return render(request, 'order/form_exchange.html', context)
