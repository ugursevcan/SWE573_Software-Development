# Generated by Django 3.1.1 on 2023-05-15 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20230514_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='location',
        ),
    ]