from kavenegar import KavenegarAPI
from pm.celery import app
from django.core.mail import EmailMessage


@app.task(name='email_active_task')
def send_activate_email(link, user_email):
    email = EmailMessage(
        'active pm account',
        link,
        'from pm',
        [user_email]
    )
    email.send(fail_silently=False)


@app.task(name='send_sms_task')
def send_sms_task(phone_num, random_code):
    api = KavenegarAPI(
        '77634E51555442727237775751353472616B6C61306F5037565169563431326B79697A50434C785A5473413D')
    params = {'sender': '10008663', 'receptor': phone_num, 'message': str(random_code)}
    api.sms_send(params)
