# Generated by Django 4.0.6 on 2022-12-22 23:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_alter_ticket_options_alter_ticket_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketShowStatus',
            fields=[
            ],
            options={
                'verbose_name': 'Tickewt',
                'db_table': 'ticket',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ticket.ticket',),
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={},
        ),
        migrations.AlterModelTable(
            name='ticket',
            table=None,
        ),
    ]
