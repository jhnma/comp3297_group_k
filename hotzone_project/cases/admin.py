from django.contrib import admin
from .models import Virus, Patient, Case, Location, Visit
#, Staff

admin.site.register(Virus)
admin.site.register(Patient)
admin.site.register(Case)
admin.site.register(Location)
admin.site.register(Visit)
#admin.site.register(Staff)
