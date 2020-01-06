# Generated by Django 2.0.7 on 2020-01-06 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drivers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver_hist',
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
                ('assigned', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Passenger_hist',
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
                ('assigned', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Ride_hist',
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