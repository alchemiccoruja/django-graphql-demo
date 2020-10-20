from django.urls import path

from . import views


urlpatterns = [
    # ex: /temperature/
    path('', views.index, name='index'),
    # ex: /temperature/5/
    path('<int:temperature_id>/', views.detail, name='detail'),
    # ex: /temperature/5/measurements/
    path('<int:temperature_id>/measurements/', views.measurements, name='measurements'),
    # ex: /temperature/5/measure/
    path('<int:temperature_id>/measure/', views.measure, name='measure'),
]
