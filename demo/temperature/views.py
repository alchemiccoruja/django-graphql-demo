
import random
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views import generic
from django.utils import timezone


from .models import Temperature, CurrentMeasurement

# def index(request):
#     cur_time = datetime.now().isoformat()
#     cur_temp = random.uniform(0, 100)
#     response_body = "Current Time: {} <br>Current Temperature: {}".format(cur_time, cur_temp)
#     latest_temperature_list = Temperature.objects.order_by('-create_date')[:5]
#     template = loader.get_template('temperature/index.html')
#     context = {
#         'latest_temperature_list': latest_temperature_list,
#     }
#     return HttpResponse(template.render(context, request))

# Django Generic Views implementation
class IndexView(generic.ListView):
    template_name = 'temperature/index.html'
    context_object_name = 'latest_temperature_list'

    def get_queryset(self):
        """Return the last five Temperatures."""
        return Temperature.objects.filter(
            create_date__lte=timezone.now()
        ).order_by('-create_date')[:5]

 
# def detail(request, temperature_id):
#     #return HttpResponse("You're looking at temperature %s." % temperature_id)
#     temperature = get_object_or_404(Temperature, pk=temperature_id)
#     currentmeasurement = random.uniform(0, 100)
#     return render(request, 'temperature/detail.html',
#                   {
#                     'temperature': temperature,
#                     'currentmeasurement': currentmeasurement
#                   }
#                   )

# Django Generic Views implementation
class DetailView(generic.DetailView):
    model = Temperature
    template_name = 'temperature/detail.html'


# def measurements(request, temperature_id):
#     temperature = get_object_or_404(Temperature, pk=temperature_id)
#     return render(request, 'temperature/measurements.html', {'temperature': temperature})

# Django Generic Views implementation
class ResultsView(generic.DetailView):
    model = Temperature
    template_name = 'temperature/measurements.html'


def measure(request, pk):
    temperature = get_object_or_404(Temperature, pk=pk)
    try:
        measurement_value = request.POST['currentmeasurement']
        now = timezone.now()
        currentmeasurement = CurrentMeasurement(timestamp = now)
        currentmeasurement.value = float(measurement_value)
        currentmeasurement.unit = temperature
        currentmeasurement.save()
    except Exception as exp:
        # Redisplay the question voting form.
        return render(request, 'temperature/detail.html', {
            'temperature': temperature,
            'error_message': str(exp),
        })
    else:
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('temperature:measurements', args=(temperature.id,)))