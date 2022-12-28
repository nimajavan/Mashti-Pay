from django.shortcuts import render, redirect
from perfectmoney import PerfectMoney
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(http_method_names=['GET'])
def get_balance_pm(request):
    pass
