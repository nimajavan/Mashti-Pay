import requests
from .models import DollarPriceModel
from pm.celery import app
from perfectmoney import PerfectMoney


@app.task(name='dollar_price_task')
def dollar_price():
    url = requests.get('http://api.navasan.tech/latest/?api_key=freeZBx2134c93rJ2Cl2j39w7shAElLI')
    r = url.json()
    print(r['harat_naghdi_buy']['value'])
    DollarPriceModel.objects.filter(pk=1).update(price=r['harat_naghdi_buy']['value'])


@app.task(name='create_ev_task')
def create_ev_task(amount):
    p = PerfectMoney('37631678', 'Annymtavalod1377')
    ev = p.voucher_create('U1234567', amount)
    return ev


@app.on_after_finalize.connect()
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60.0, dollar_price.s(), name='dollar_price_schedule')
