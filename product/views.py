from re import I
from django.shortcuts import render
from order.forms import BuyForm, SellForm
from blog.models import Blog, Comment
from account.models import Profile
from django.http import HttpResponse
from perfectmoney import PerfectMoney
import json


def home(request):
    form_buy = BuyForm()
    form_sell = SellForm()
    blog = Blog.objects.all()[:3]
    comment = Comment.objects.all()
    context = {'form_buy': form_buy, 'form_sell': form_sell,
               'blog': blog, 'comments': comment}
    return render(request, 'product/product.html', context)


def get_balance(request):
    p = PerfectMoney('37631678', 'Tavalod1377')
    balance = p.balance()
    if not balance:
        return HttpResponse(p.error)
    else:
        return HttpResponse(json.dumps(balance))


def test(request):
    return render(request, 'product/test.html')
