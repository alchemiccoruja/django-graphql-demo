import datetime
import random
from django.test import TestCase
from django.utils import timezone

from .models import Temperature, CurrentMeasurement


class TemperatureModelTests(TestCase):

    def test_was_measured_recently_with_future_temperature(self):
        """
        was_measured_recently() returns False for questions whose timestamp
        is in the future.
        """
        future_time = timezone.now() + datetime.timedelta(days=30)
        future_temperature = Temperature(create_date = future_time)
        future_temperature.save()
        
        measurement_value = random.uniform(0, 100)
        futuremeasurement = CurrentMeasurement(timestamp = timezone.now() + datetime.timedelta(days=31))
        futuremeasurement.value = float(measurement_value)
        futuremeasurement.unit = future_temperature
        futuremeasurement.save()
        self.assertIs(future_temperature.was_measured_recently(), False)
        
        
    def test_was_measured_recently_with_old_temperature(self):
        """
        was_measured_recently() returns False for temperatures/measurement whose create_date
        is older than 1 day.
        """
        old_time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_temperature = Temperature(create_date = old_time)
        old_temperature.save()
        
        measurement_value = random.uniform(0, 100)
        old_measurement = CurrentMeasurement(timestamp = timezone.now() - datetime.timedelta(days=1))
        old_measurement.value = float(measurement_value)
        old_measurement.unit = old_temperature
        old_measurement.save()
        self.assertIs(old_temperature.was_measured_recently(), False)

    def test_was_measured_recently_with_recent_temperature(self):
        """
        was_measured_recently() returns True for temperatures/measurement whose create_date
        is within the last day.
        """
        recent_time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_temperature= Temperature(create_date = recent_time)
        recent_temperature.save()
        
        measurement_value = random.uniform(0, 100)
        recent_measurement = CurrentMeasurement(timestamp = timezone.now() - datetime.timedelta(days=1))
        recent_measurement.value = float(measurement_value)
        recent_measurement.unit = recent_temperature
        recent_measurement.save()
        
        self.assertIs(recent_temperature.was_measured_recently(), False)
