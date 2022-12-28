from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderBuy
from account.views import automatic_create_ev


@receiver(post_save, sender=OrderBuy)
def automate_buy_signal(sender, instance, **kwargs):
    if instance.paid and instance.condition == 'accept':
        automatic_create_ev(instance.id)



