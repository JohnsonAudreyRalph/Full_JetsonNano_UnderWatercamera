from django.db import models
from datetime import datetime
from django.utils import timezone


# Create your models here.
class Auto_cam(models.Model):
    Timers = models.IntegerField(default=0)
    Counters = models.IntegerField(default=0)
    start_Time = models.TimeField(default=timezone.now().strftime('%H:%M'))
    stat_Date = models.DateField(default=datetime.now)
    Check_cap = models.BooleanField(default=False)

    def __str__(self):
        template = '{0.Timers} {0.Counters} {0.start_Time} {0.stat_Date} {0.Check_cap}'
        return template.format(self)