# Generated by Django 4.0.6 on 2022-12-24 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_delete_ticketproxy'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='reply',
            field=models.TextField(blank=True, null=True),
        ),
    ]
