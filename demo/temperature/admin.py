from django.contrib import admin

from .models import Temperature, CurrentMeasurement      

class CurrentMeasurementInline(admin.TabularInline):
    model = CurrentMeasurement
    extra = 3


class TemperatureAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['unit']}),
        ('Date information', {'fields': ['create_date'], 'classes': ['collapse']}),
    ]
    inlines = [CurrentMeasurementInline]
    list_display = ('unit', 'create_date', 'was_measured_recently')
    list_filter = ['create_date']
    search_fields = ['unit']

admin.site.register(Temperature, TemperatureAdmin)