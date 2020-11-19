from django.shortcuts import render
from django.views.generic import TemplateView
from cases.models import Case, Location, Visit, Patient, Virus
from django.http import JsonResponse, HttpResponse
import urllib.parse
from django.core import serializers
from cases import models

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
    name=request.POST.get('name')
    address=request.POST.get('address')
    x=float(request.POST.get('x'))
    y=float(request.POST.get('y'))
    obj=Location.objects.filter(name=name, x=x, y=y)
    if(obj.exists()):
        return JsonResponse({'status':0, 'pk': obj[0].pk})
    else:
        newLocation=Location()
        newLocation.name=name
        newLocation.address=address
        newLocation.x=x
        newLocation.y=y
        newLocation.save()
        return JsonResponse({'status':1, 'pk': newLocation.pk})

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

# class Root(TemplateView):
#     template_name = "add-visit.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         return context

class Root(TemplateView):
    template_name = "cases.html"

    def __init__(self):
        self.INFECTED_TYPE = {"l":"local","i":"imported"}

    def get_search_result(self):
        
        if self.search_request == "" or self.search_request==None :
            self.cases = models.Case.objects.filter().extra( select={'int': 'CAST(case_id AS INTEGER)'}).order_by('int')
        else:
            self.cases = models.Case.objects.filter(case_id__contains=self.search_request).extra( select={'int': 'CAST(case_id AS INTEGER)'}).order_by('int')
        #print(self.cases)
            


    def get_display_data(self):
        length_of_db = (len(self.cases))
        # required as we will have many data
        # we need to show all cases , that means we need to set limit for init display
        self.length = length_of_db if length_of_db<50 else 50
   
    

    def get_render_entry(self):
        # todo -- period and button
        self.search_result = []
        for i in self.cases[:self.length]:
            self.search_result.append({"id":i.case_id,
                                "name":i.patient,
                                "virus":i.virus,
                                "date":i.date.strftime("%Y-%m-%d"),
                                "category":self.INFECTED_TYPE[i.category]})
       
    def get_context_data(self, **kwargs):
        self.search_request = self.request.GET.get("case")

        context = super().get_context_data(**kwargs)

        self.get_search_result()
        self.get_display_data()
        self.get_render_entry()

        context["search_result"] = self.search_result
        
        return context

class ViewVisits(TemplateView):
    template_name = "cases.html"

    def __init__(self):
        self.INFECTED_TYPE = {"l":"local","i":"imported"}

    def get_search_result(self):
        
        if self.search_request == "" or self.search_request==None :
            self.cases = models.Case.objects.filter().extra( select={'int': 'CAST(case_id AS INTEGER)'}).order_by('int')
        else:
            self.cases = models.Case.objects.filter(case_id__contains=self.search_request).extra( select={'int': 'CAST(case_id AS INTEGER)'}).order_by('int')
        #print(self.cases)

    def get_display_data(self):
        length_of_db = (len(self.cases))
        # required as we will have many data
        # we need to show all cases , that means we need to set limit for init display
        self.length = length_of_db if length_of_db<50 else 50

    def get_render_entry(self):
        # todo -- period and button
        self.search_result = []
        for i in self.cases[:self.length]:
            self.search_result.append({"id":i.case_id,
                                "name":i.patient,
                                "virus":i.virus,
                                "date":i.date.strftime("%Y-%m-%d"),
                                "category":self.INFECTED_TYPE[i.category]})
       
    def get_context_data(self, **kwargs):
        self.search_request = self.request.GET.get("case")

        context = super().get_context_data(**kwargs)

        self.get_search_result()
        self.get_display_data()
        self.get_render_entry()

        context["search_result"] = self.search_result
        
        return context