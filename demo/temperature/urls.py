from django.urls import path

from . import views

app_name = 'temperature'
urlpatterns = [
    # ex: /temperature/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /temperature/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /temperature/5/measurements/
    path('<int:pk>/measurements/', views.ResultsView.as_view(), name='measurements'),
    # ex: /temperature/5/measure/
    path('<int:pk>/measure/', views.measure, name='measure'),
]

