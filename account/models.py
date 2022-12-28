from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django import db
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('please enter username')
        if not email:
            raise ValueError('please enter email')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class UserDocumentStatus(models.TextChoices):
    To_Do = 'to do'
    In_progress = 'in_progress'
    Failed = 'failed'
    Ok = 'ok'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    id_card_code = models.IntegerField(null=True, blank=True)
    bank_card_num = models.IntegerField(null=True, blank=True)
    shaba_num = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(upload_to='profile/avatar/', default='profile/avatar.png')
    id_card = models.ImageField(upload_to='profile/id_card/', null=True, blank=True)
    bank_card_pic = models.ImageField(upload_to='profile/bank_card/', null=True, blank=True)
    vip_user = models.BooleanField(default=False)
    id_card_status = models.CharField(max_length=255, choices=UserDocumentStatus.choices,
                                      default=UserDocumentStatus.To_Do)
    bank_card_pic_status = models.CharField(max_length=255, choices=UserDocumentStatus.choices,
                                            default=UserDocumentStatus.To_Do)
    # personal information
    ticket_sum = models.IntegerField(default=0)
    buy_sum = models.IntegerField(default=0)
    sell_sum = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    def set_status(self):
        if self.id_card and self.id_card_status == UserDocumentStatus.To_Do:
            self.id_card_status = UserDocumentStatus.In_progress
            self.save()
        elif not self.id_card:
            self.id_card_status = UserDocumentStatus.To_Do
            self.save()

        if self.bank_card_pic and self.bank_card_pic_status == UserDocumentStatus.To_Do:
            self.bank_card_pic_status = UserDocumentStatus.In_progress
            self.save()
        elif not self.bank_card_pic:
            self.bank_card_pic_status = UserDocumentStatus.To_Do
            self.save()

    def vip_status(self):
        if self.id_card_status == UserDocumentStatus.Ok and self.bank_card_pic_status == UserDocumentStatus.Ok:
            self.vip_user = True
            self.save()
        else:
            self.vip_user = False
            self.save()


class VoucherWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    e_voucher = models.CharField(max_length=10)
    activation_code = models.CharField(max_length=17)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.CharField(max_length=244, null=True, blank=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        p_create = Profile(user=kwargs['instance'])
        p_create.save()


post_save.connect(create_profile, User)
