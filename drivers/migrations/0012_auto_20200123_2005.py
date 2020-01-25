# Generated by Django 2.0.7 on 2020-01-23 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drivers', '0011_auto_20200123_1952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='username',
        ),
        migrations.RemoveField(
            model_name='passenger',
            name='username',
        ),
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='passenger',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]