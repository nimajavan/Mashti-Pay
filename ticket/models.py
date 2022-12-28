from django.db import models
from account.models import User


class TicketStatus(models.TextChoices):
    TO_DO = 'To Do'
    DONE = 'Done'


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    status = models.CharField(max_length=255, choices=TicketStatus.choices, default=TicketStatus.TO_DO)
    body = models.TextField()
    created_at = models.DateTimeField('created at', auto_now_add=True)
    updated_at = models.DateTimeField('updated at', auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.created_at = self.updated_at
        super(Ticket, self).save(*args, **kwargs)


class ReplyTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='rep')
    rep_body = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.ticket.title)
