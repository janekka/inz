# Generated by Django 2.0.7 on 2020-01-12 21:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0008_auto_20200112_2240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='ride_id',
        ),
    ]
