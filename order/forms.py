from django import forms
from .models import OrderBuy, OrderSell


class BuyForm(forms.ModelForm):
    class Meta:
        model = OrderBuy
        fields = ['quantity']


class SellForm(forms.ModelForm):
    class Meta:
        model = OrderSell
        fields = ['voucher_code', 'activate_code']
