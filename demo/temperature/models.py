from django.db import models

class Temperature(models.Model):
    unit = models.CharField(max_length=50, default="Fahrenheit")
    create_date = models.DateTimeField('create date', auto_now=True)

    def __str__(self):
        return "{}".format(self.unit)

class CurrentMeasurement(models.Model):
    unit = models.ForeignKey(Temperature, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    value = models.FloatField(max_length=50)

    def __str__(self):
        return "{} {} at {}".format(self.value, self.unit, self.timestamp)