# Generated by Django 4.0.6 on 2022-09-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('To Do', 'To Do'), ('Done', 'Done')], default='To Do', max_length=255),
        ),
    ]
