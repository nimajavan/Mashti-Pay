from django.db import models
from django.db.models.signals import post_save


class DollarPriceHistory(models.Model):
    price_history = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.price_history)


class DollarPriceModel(models.Model):
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.price)


def post_save_dollar_history(sender, instance, created, *args, **kwargs):
    data = instance
    DollarPriceHistory.objects.create(price_history=data.price)


post_save.connect(post_save_dollar_history, sender=DollarPriceModel)
