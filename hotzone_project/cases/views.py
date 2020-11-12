from django.shortcuts import render
from django.views.generic import TemplateView
from cases.models import Case, Location, Visit, Patient, Virus
from django.http import JsonResponse, HttpResponse
import urllib.parse
from django.core import serializers

class AddVisit(TemplateView):
    template_name='add-visit.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['locations']=Location.objects.all()
        return context

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
    newVisit=Visit()
    try:
        newVisit.case=Case.objects.get(case_id=request.POST.get('case_id'))
    except Case.DoesNotExist:
        return JsonResponse({'msg': 'Case not exists.'})
    try:
        newVisit.location=Location.objects.get(pk=request.POST.get('location_id'))
    except:
        return JsonResponse({'msg': 'Location not exists.'})
    newVisit.date_from=request.POST.get('date_from')
    newVisit.date_to=request.POST.get('date_to')
    newVisit.category=request.POST.get('category')
    newVisit.save()
    return JsonResponse({'msg': 'Visit added.'})