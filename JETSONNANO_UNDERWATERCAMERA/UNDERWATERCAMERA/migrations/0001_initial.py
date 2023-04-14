# Generated by Django 4.2 on 2023-04-14 06:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Camera_Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Timers', models.IntegerField(default=0)),
                ('Counters', models.IntegerField(default=0)),
                ('start_Time', models.TimeField()),
                ('stat_Date', models.DateField(default=datetime.datetime.now)),
            ],
            options={
                'verbose_name_plural': 'Auto Cameras',
            },
        ),
    ]