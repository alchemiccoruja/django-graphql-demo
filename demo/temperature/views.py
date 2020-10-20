
import random
from datetime import datetime
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import Temperature

def index(request):
    cur_time = datetime.now().isoformat()
    cur_temp = random.uniform(0, 100)
    response_body = "Current Time: {} <br>Current Temperature: {}".format(cur_time, cur_temp)
    latest_temperature_list = Temperature.objects.order_by('-create_date')[:5]
    template = loader.get_template('temperature/index.html')
    context = {
        'latest_temperature_list': latest_temperature_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, temperature_id):
    #return HttpResponse("You're looking at temperature %s." % temperature_id)
    temperature = get_object_or_404(Temperature, pk=temperature_id)
    return render(request, 'temperature/detail.html', {'temperature': temperature})

def measurements(request, temperature_id):
    response = "You're looking at the measurements of temperature %s."
    return HttpResponse(response % temperature_id)

def measure(request, temperature_id):
    return HttpResponse("You're measuring with %s temperature unit." % temperature_id)