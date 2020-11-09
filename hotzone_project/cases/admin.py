from django.contrib import admin
from .models import Virus, Patient, Case, Location, Visit

admin.site.register(Virus)
admin.site.register(Patient)
admin.site.register(Case)
admin.site.register(Location)
admin.site.register(Visit)

