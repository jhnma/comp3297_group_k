from django.shortcuts import render
from django.views.generic import View
from cases.models import Case, Location, Visit, Patient, Virus
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
import urllib.parse
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
import json

class AddVisit(View):
    def get(self, *args, **kwargs):
        try:
            case = Case.objects.get(case_id=kwargs['case_id'])
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Case doesn't exist.")
        patient = case.patient
        context = {
            'case': case,
            'patient': patient,
        }
        return render(self.request, 'add-visit.html', context)

def getLocations(request):
    name=urllib.parse.unquote(request.GET.get('name'))
    obj=Location.objects.filter(name__icontains=name)
    data=serializers.serialize('json', obj)
    return HttpResponse(data, content_type='application/json')

def addLocation(request):
    obj, created = Location.objects.get_or_create(
        name=request.POST.get('name'),
        address=request.POST.get('address'),
        x=float(request.POST.get('x')),
        y=float(request.POST.get('y')),
    )
    if (created):
        return JsonResponse({'status':1, 'pk': obj.pk})
    else:
        return JsonResponse({'status':0, 'pk': obj.pk})

def add(request):
    locations=request.POST.getlist('locations[]')
    case=Case.objects.get(case_id=request.POST.get('case_id'))
    for i in range(0,len(locations)):
        data=json.loads(locations[i])
        newVisit=Visit()
        newVisit.case=case
        newVisit.location=Location.objects.get(pk=data['location_id'])
        newVisit.date_from=data['date_from']
        newVisit.date_to=data['date_to']
        newVisit.category=data['category']
        newVisit.save()
    return JsonResponse({'msg': 'Visits added.'})