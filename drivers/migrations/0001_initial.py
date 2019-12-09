# Generated by Django 2.0.7 on 2019-12-09 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(default='noname')),
                ('start', models.TextField()),
                ('end', models.TextField()),
                ('stops', models.TextField()),
                ('stops_arr', models.TextField(default='')),
                ('date', models.DateField()),
                ('time_dep', models.FloatField()),
                ('time_arr', models.FloatField()),
                ('car_model', models.TextField()),
                ('car_cap', models.IntegerField()),
                ('cigs', models.BooleanField()),
                ('pets', models.BooleanField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.TextField(default='noname')),
                ('start', models.TextField()),
                ('end', models.TextField()),
                ('distance', models.FloatField()),
                ('date', models.DateField()),
                ('time_dep', models.FloatField()),
                ('time_arr', models.FloatField()),
                ('cigs', models.BooleanField()),
                ('pets', models.BooleanField()),
                ('max_cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('bio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('ride_id', models.AutoField(primary_key=True, serialize=False)),
                ('driver_username', models.TextField(default='noname')),
                ('passenger_username', models.TextField(default='noname')),
                ('date', models.DateField()),
                ('pick_up', models.TextField()),
                ('drop_off', models.TextField()),
                ('driver_ride_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivers.Driver')),
                ('passenger_ride_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drivers.Passenger')),
            ],
        ),
    ]
