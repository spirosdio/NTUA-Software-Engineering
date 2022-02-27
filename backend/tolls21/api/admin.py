from django.contrib import admin

from .models import driver, vehicle, station, pass_event, provider

admin.site.register(provider)
admin.site.register(driver)
admin.site.register(vehicle)
admin.site.register(station)
admin.site.register(pass_event)