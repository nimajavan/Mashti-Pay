# Generated by Django 4.0.6 on 2022-12-01 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_alter_profile_last_name_alter_profile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile/avatar.png', upload_to='profile/avatar/'),
        ),
    ]
