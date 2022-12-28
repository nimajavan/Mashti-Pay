from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Ticket


@receiver(post_save, sender=Ticket)
def ticket_status(sender, instance, **kwargs):
    t = Ticket.objects.get(id=instance.id)
    try:
        tr = t.rep.get().rep_body
        t.status = 'Done'
        t.save()
    except:
        pass
