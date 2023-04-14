from django.db import models
from datetime import datetime


# Create your models here.
class Auto_cam(models.Model):
    Timers = models.IntegerField(default=0)
    Counters = models.IntegerField(default=0)
    start_Time = models.TimeField()
    stat_Date = models.DateField(default=datetime.now)

    def set_default_start_Time(self):
        return datetime.now().time().replace(second=0)

    def __str__(self):
        template = '{0.Timers} {0.Counters} {0.start_Time} {0.stat_Date}'
        return template.format(self)

    class Meta:
        verbose_name_plural = 'Auto Cameras'


Auto_cam.start_Time.default = Auto_cam().set_default_start_Time