from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.decorators.http import require_POST
from six import text_type
from api.models import DollarPriceModel, DollarPriceHistory
from api.tasks import create_ev_task
from order.forms import BuyForm, SellForm
from order.models import OrderBuy, OrderSell
from ticket.forms import TicketForm
from ticket.models import Ticket
from .forms import *
from .models import User, VoucherWallet, Notification
from .serializer import *
from .tasks import send_sms_task
from rest_framework.decorators import api_view
from rest_framework.response import Response


class EmailRegisterToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.id) + text_type(timestamp)


email_generations = EmailRegisterToken()


class Register(View):
    register_form = RegisterForm
    register_template = 'account/register.html'

    def get(self, request):
        form = self.register_form()
        context = {'form': form}
        return render(request, self.register_template, context)

    def post(self, request):
        form = self.register_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(
                username=cd['username'], email=cd['email'], password=cd['password'])
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = email_generations.make_token(user)
            request.session['user_id'] = uidb64
            # domain = get_current_site(request).domain
            # uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            # url = reverse('account:email_active',
            #               kwargs={'uidb64': uidb64, 'token': email_generations.make_token(user)})
            # link = 'http://' + domain + url
            # user_email = cd['email']
            # send_activate_email.delay(link, user_email)
            return redirect('account:phone_register', uidb64, token)
        else:
            context = {'form': form}
            return render(request, self.register_template, context)


class PhoneRegister(View):
    def get(self, request, uidb64, token):
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if user and email_generations.check_token(user, token):
                form = PhoneForm()
                code_form = SmsCodeForm()
                return render(request, 'account/phone_register.html', {'form': form, 'code_form': code_form})
            else:
                messages.error(request, 'توکن شما منقضی شده است لطفا دوباره امتحان کند')
                return redirect('account:register')
        except:
            messages.error(request, 'توکن شما منقضی شده است لطفا دوباره امتحان کند')
            return redirect('account:register')


class ActivateUserEmail(View):
    def get(self, request, uidb64, token):
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        if user and email_generations.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('account:login')
        return messages.error(request, 'your token expired ! please try again')


def send_code(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        phone = request.POST.get('phone')
        random_code = 333
        phone_num = f"0{phone}"
        request.session['random_code'] = random_code
        request.session['phone_num'] = phone_num
        try:
            send_sms_task.delay(phone_num, random_code)
            data = {'success': 'کد تایید با موفقیت ارسال شد'}
            return JsonResponse(data)
        except:
            data = {'success': 'مشکلی به وجود آمده لطفا دوباره تلاش کنید'}
            return JsonResponse(data)


class VerifyCode(View):
    def post(self, request):
        form = SmsCodeForm(request.POST)
        user = User.objects.get(id=force_str(urlsafe_base64_decode(request.session.get('user_id'))))
        if form.is_valid():
            cd = form.cleaned_data['code']
            if user and cd == str(request.session.get('random_code')):
                user.phone = int(request.session.get('phone_num'))
                user.is_active = True
                user.save()
                messages.success(request, 'شماره همراه با موفقیت ثبت شد')
                return redirect('account:login')
            else:
                messages.error(request, 'کد وارد شده نادرست می باشد!')
                return redirect('account:register')
        else:
            messages.error(request, 'کد وارد شده نادرست می باشد!')
            return redirect('account:register')


class Login(View):
    login_form = LoginForm
    login_template = 'account/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account:profile')
        else:
            form = self.login_form
            context = {'form': form}
            return render(request, self.login_template, context)

    def post(self, request):
        form = self.login_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, email=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید')
                return redirect('account:profile')
            else:
                messages.error(request, 'یوزرنیم و پسورد صحیح نیست')
                form = self.login_form()
        return render(request, self.login_template, {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('account:login')


class UserProfile(View):
    profile_form = ProfileForm
    ticket_form = TicketForm
    profile_image_form = ProfileImageForm
    buy_form = BuyForm
    sell_form = SellForm
    profile_template = 'account/profile.html'

    def get(self, request):
        global sum_buy
        user_profile = Profile.objects.get(user_id=request.user.id)
        # status document
        user_profile.set_status()
        user_profile.vip_status()
        # end status document

        # buy-sell-form
        form_buy = BuyForm()
        form_sell = SellForm()
        # end buy-sell-form

        # api
        dollar_price = DollarPriceModel.objects.get().price
        # end api

        # order show
        order_buy = OrderBuy.objects.filter(user_id=request.user.id)
        order_sell = OrderSell.objects.filter(user_id=request.user.id)
        # end order show

        # ticket
        ticket_obj = Ticket.objects.filter(user_id=request.user.id)
        # end ticket

        # sum
        # ticket
        c = 0
        sum_buy = 0
        sum_sell = 0
        for t in ticket_obj:
            c += 1

        for o in order_buy:
            if o.paid:
                sum_buy += o.total_price

        for s in order_sell:
            sum_sell += 1

        Profile.objects.filter(user_id=request.user.id).update(
            buy_sum=sum_buy, ticket_sum=c, sell_sum=sum_sell)
        # end sum

        # voucher wallet
        voucher_wallet = VoucherWallet.objects.filter(user_id=request.user.id)
        # end voucher wallet

        # chart
        chart = DollarPriceHistory.objects.all()[:7]
        # end chart

        # notification
        notification = Notification.objects.filter(user_id=request.user.id, read=False)[:4]

        form_ticket = self.ticket_form()
        profile_image_form = self.profile_image_form()
        form = self.profile_form()
        context = {'form': form, 'profile': user_profile,
                   'ticket_form': form_ticket, 'profile_image_form': profile_image_form, 'form_buy': form_buy,
                   'form_sell': form_sell, 'dollar_price': dollar_price, 'order_buy': order_buy,
                   'order_sell': order_sell, 'ticket': ticket_obj, 'voucher_wallet': voucher_wallet,
                   'chart': chart, 'notification': notification}
        return render(request, self.profile_template, context)


def user_profile_update(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موففیت به روز شد')
            return redirect('account:profile')
        else:
            messages.error(request, 'متاسفانه مشکلی به وجود اومده دوباره تلاش کنید')
            return redirect('account:profile')


def ticket_send(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj = Ticket.objects.create(
                user_id=request.user.id, title=cd['title'], body=cd['body'])
            ticket_obj.save()
            messages.success(
                request, 'تیکت شما با موفقیت ارسال شد لطفا منتظر پاسخگویی باشید')
            return redirect('account:profile')
        else:
            messages.error(
                request, 'متاسفانه مشکلی به وجود اومده دوباره تلاش کنید')
            return redirect('account:profile')


@require_POST
def id_card_upload(request):
    form = IdCardForm(request.POST, request.FILES,
                      instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'با موفقیت آپلود شد! منتظر تایید باشید')
        return redirect('account:profile')
    else:
        messages.error(request, 'خطایی رخ داده است لطفا دوباره تلاش کنید')
        return redirect('account:profile')


@require_POST
def bank_card_upload(request):
    form = BankCardForm(request.POST, request.FILES,
                        instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'با موفقیت آپلود شد! منتظر تایید باشید')
        return redirect('account:profile')
    else:
        messages.error(request, 'خطایی رخ داده است لطفا دوباره تلاش کنید')
        return redirect('account:profile')


@require_POST
def profile_image_upload(request):
    form = ProfileImageForm(request.POST, request.FILES,
                            instance=request.user.profile)
    if form.is_valid():
        form.save()
        messages.success(request, 'تصویر شما با موفقیت تغییر کرد')
        return redirect('account:profile')
    else:
        messages.error(
            request, 'متاسفانه مشکلی پیش آمده لطفا دوباره تلاش کنید')
        return redirect('account:profile')


class ResetPassword(View):
    def get(self, request):
        form = EmailResetPassword()
        context = {'form': form}
        return render(request, 'account/password_reset_1.html', context)

    def post(self, request):
        form = EmailResetPassword(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(Q(email=cd['email']))
            if user.exists():
                for users in user:
                    domain = get_current_site(request).domain
                    uidb64 = urlsafe_base64_encode(force_bytes(users.id))
                    url = reverse('account:password_reset_2', kwargs={
                        'uidb64': uidb64, 'token': email_generations.make_token(users)
                    })
                    link = 'http://' + domain + url
                    user_email = cd['email']
                    email = EmailMessage(
                        'بازیابی کلمه عبور',
                        link,
                        'nimajavangt@gmail.com',
                        [str(user_email)]
                    )
                    email.send(fail_silently=False)
                    messages.success(request, 'ایمیل با موفقیت ارسال شد لطفا ایمیل خود را چک کنید')
                    return redirect(request.META.get('HTTP_REFERER'))


class ResetPasswordConfirm(View):
    def get(self, request, uidb64, token):
        url = request.META.get('HTTP_REFERER')
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=user_id)
        form = PasswordResetForm()
        context = {'form': form, 'user_id': user_id}
        if user and email_generations.check_token(user, token):
            return render(request, 'account/password_reset_2.html', context)
        else:
            messages.error(request, 'درخواست شما منقضی شده است لطفا مجدد درخواست ارسال کنید')
            return redirect('account:password_reset_1')

    def post(self, request, uidb64, token):
        url = request.META.get('HTTP_REFERER')
        user_id = force_str(urlsafe_base64_decode(uidb64))
        form = PasswordResetForm(request.POST)
        user = User.objects.get(id=user_id)
        if user and email_generations.check_token(user, token):
            if form.is_valid():
                cd = form.cleaned_data
                user.set_password(cd['password_2'])
                user.save()
                messages.success(request, 'پسورد شما با موفقیت تغییر کرد')
                return redirect('account:login')
            else:
                context = {'form': form}
                return render(request, 'account/password_reset_2.html', context)
        else:
            messages.error(request, 'درخواست شما منقضی شده است لطفا مجدد درخواست ارسال کنید')
            return redirect('account:password_reset_1')


def go_to_gateway_view(request, order_id):
    order = OrderBuy.objects.get(user_id=request.user.id, id=order_id)
    amount = order.total_price
    user_mobile_number = request.user.phone

    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.IDPAY)
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_client_callback_url(reverse('callback-gateway', args=[order_id]))
        bank.set_mobile_number(user_mobile_number)
        bank_record = bank.ready()

        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        raise e


def automatic_create_ev(order_id):
    order = OrderBuy.objects.get(id=order_id)
    amount = order.quantity
    voucher = create_ev_task.delay(amount)
    wallet = VoucherWallet(user_id=order.uesr.id)
    wallet.e_voucher = voucher['VOUCHER_NUM']
    wallet.activation_code = voucher['VOUCHER_CODE']


def callback_gateway_view(request, order_id):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        raise Http404

    if bank_record.is_success:
        order = OrderBuy.objects.get(user_id=request.user.id, id=order_id)
        order.paid = True
        order.tracking_code = tracking_code
        order.condition = 'pending'
        order.save()
        # automatic_create_ev(order_id)

        tc = request.GET.get('tc')
        return render(request, 'order/success_buy.html', {'tc': tc})

    tc = request.GET.get('tc')
    return render(request, 'order/failed_buy.html', {'tc': tc})


class ReadNotification(View):
    def get(self, request):
        notification = Notification.objects.filter(user_id=request.user.id, read=False)[:4]
        for n in notification:
            n.read = True
            n.save()
        return JsonResponse({'status': 200})


@api_view(['GET'])
def admin_page_information(request):
    ticket = Ticket.objects.filter(status='To Do').count()
    buy_order = OrderBuy.objects.filter(paid=True, condition='pending').count()
    context = {'ticket': ticket, 'buy_order': buy_order}
    return Response(context)
