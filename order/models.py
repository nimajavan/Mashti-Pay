from django.db import models
from account.models import User


class ConditionChoices(models.TextChoices):
    accept = 'accept'
    reject = 'reject'
    pending = 'pending'
    null = 'null'


class OrderBuy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dollar_price = models.IntegerField()
    quantity = models.IntegerField()
    paid = models.BooleanField(default=False)
    tracking_code = models.CharField(max_length=300, null=True, blank=True)
    condition = models.CharField(max_length=255, choices=ConditionChoices.choices, default=ConditionChoices.null)

    def __str__(self):
        return self.user.username

    @property
    def total_price(self):
        p = self.dollar_price * self.quantity
        return p


class OrderSell(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=60)
    activate_code = models.CharField(max_length=60)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
