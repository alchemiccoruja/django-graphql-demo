import datetime
import random
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse



from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium import webdriver


from .models import Temperature, CurrentMeasurement


def create_temperature(unit, days):
    """
    Create a temperature with the given `unit` and measured the
    given number of `days` offset to now (negative for measurements made
    in the past, positive for temperatures that have yet to be measured).
    """
    create_time = timezone.now() + datetime.timedelta(days=days)
    temperature = Temperature.objects.create(unit=unit, create_date=create_time)
    return temperature


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
        


class TemperatureIndexViewTests(TestCase):
    def test_no_temperatures(self):
        """
        If no temperatures exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('temperature:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Temperatures are available.")
        self.assertQuerysetEqual(response.context['latest_temperature_list'], [])

    def test_past_temperature(self):
        """
        Temperatures with a create_date in the past are displayed on the
        index page.
        """
        create_temperature(unit="Celcius", days=-30)
        response = self.client.get(reverse('temperature:index'))
        self.assertQuerysetEqual(
            response.context['latest_temperature_list'],
            ['<Temperature: Celcius>']
        )
    
    def test_future_temperature(self):
        """
        Temperatures with a create_date in the future aren't displayed on
        the index page.
        """
        create_temperature(unit="Future Celcius", days=30)
        response = self.client.get(reverse('temperature:index'))
        self.assertContains(response, "No Temperatures are available.")
        self.assertQuerysetEqual(response.context['latest_temperature_list'], [])
    
    def test_future_temperature_and_past_temperature(self):
        """
        Even if both past and future temperature exist, only past questions
        are displayed.
        """
        create_temperature(unit="Past Celcius", days=-30)
        create_temperature(unit="Future Celcius", days=30)
        response = self.client.get(reverse('temperature:index'))
        self.assertQuerysetEqual(
            response.context['latest_temperature_list'],
            ['<Temperature: Past Celcius>']
        )
    
    def test_two_past_temperature(self):
        """
        The temperatures index page may display multiple temperatures.
        """
        create_temperature(unit="Past Celcius 1", days=-30)
        create_temperature(unit="Past Celcius 2", days=-5)
        response = self.client.get(reverse('temperature:index'))
        self.assertQuerysetEqual(
            response.context['latest_temperature_list'],
            ['<Temperature: Past Celcius 2>', '<Temperature: Past Celcius 1>']
        )




       
class SeleniumBrowserTests(LiveServerTestCase):
    #fixtures = ['user-data.json']
    host = "0.0.0.0"
    port = 8000
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_capability("browserVersion", "81")
        #firefox_options.set_capability("platformName", "Windows XP")
        cls.selenium  = webdriver.Remote(
        command_executor='http://10.0.1.93:4444',
        options=firefox_options
        )
        #cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        #breakpoint()
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys('admin')
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys('admin')
        self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
