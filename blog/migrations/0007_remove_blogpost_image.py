# Generated by Django 5.0.6 on 2025-04-03 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogpost_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='image',
        ),
    ]
