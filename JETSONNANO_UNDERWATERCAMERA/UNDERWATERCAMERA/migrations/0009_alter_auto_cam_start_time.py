# Generated by Django 4.2 on 2023-04-16 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UNDERWATERCAMERA', '0008_alter_auto_cam_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto_cam',
            name='start_Time',
            field=models.TimeField(default='08:33'),
        ),
    ]
