# Generated by Django 4.0.6 on 2022-08-08 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='intro',
            field=models.TextField(blank=True, null=True),
        ),
    ]