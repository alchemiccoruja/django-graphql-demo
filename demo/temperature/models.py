from django.db import models
from django.utils import timezone
import datetime


class Temperature(models.Model):
    unit = models.CharField(max_length=50, default="Fahrenheit")
    create_date = models.DateTimeField('create date')

    def __str__(self):
        return "{}".format(self.unit)
    
    
    def latest_measurement(self):
        latest_measure = self.currentmeasurement_set.all().order_by('-timestamp')[0]
        return latest_measure
    
    def was_measured_recently(self):
        _latest_measure = self.latest_measurement()
        now = timezone.now()
        _yesterday = now - datetime.timedelta(days=1)
        return _yesterday <= _latest_measure.timestamp <= now

class CurrentMeasurement(models.Model):
    unit = models.ForeignKey(Temperature, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    value = models.FloatField(max_length=50)

    def __str__(self):
        return "{} {} at {}".format(self.value, self.unit, self.timestamp)