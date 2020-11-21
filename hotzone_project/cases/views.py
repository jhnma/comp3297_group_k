from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from cases.models import Case, Location, Visit, Patient, Virus
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.db.models import DateField
from django.db.models.functions import Trunc
import urllib.parse
from django.core import serializers
from cases import models
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
    template_name = "case-visits.html"

    def __init__(self):
        self.VISIT_TYPE = {'r': 'residence', 'w': 'workplace', 'v': 'visit'}
       
    def get_context_data(self, **kwargs):
        # self.search_request = self.request.GET.get("visit")

        context = super().get_context_data(**kwargs)
        self.visits = models.Visit.objects.filter(case_id=kwargs['case_id'])
        name = models.Case.objects.filter(case_id=kwargs['case_id'])[0].patient
        # .order_by(Trunc('date_to', 'date', output_field=DateField()).desc())

        self.search_result = []
        for visit in self.visits:
            self.search_result.append({"location":visit.location,
                                "datefrom":visit.date_from.strftime("%Y-%m-%d"),
                                "dateto":visit.date_to.strftime("%Y-%m-%d"),
                                "category":self.VISIT_TYPE[visit.category]})

        # "datefrom":visit.date_from.strftime("%Y-%m-%d"),
        # "dateto":visit.date_to.strftime("%Y-%m-%d")

        context["visits"] = self.search_result
        context['case_id'] = kwargs['case_id']
        context['pname'] = name

        return context

class CaseView(TemplateView):
    model=Visit
    template_name='case.html'

    def get(self, request, **kwargs):
        currentUrl=self.request.get_full_path()
        pos=currentUrl.find('cases/')+6
        cid=currentUrl[pos:]
        filtercase=Visit.objects.filter(case__case_id__exact=cid)
        context={'filtercase': filtercase}
        return render(request, self.template_name, context)

def save(request):
    if request.method == "GET":
        caseid=request.GET['caseid']

        model=Visit
        counter=0
        retrange=request.GET['locations'].count(',')
        retrange+=1
        removelist=[]
        for i in Visit.objects.filter(case__case_id__exact=request.GET['oldcaseid']):
            for j in range(retrange):
                counter=0
                if str(i.location.name)==request.GET['locations'].split(',')[j]:
                    if str(i.location.address)==request.GET['addresses'].split(',')[j]:
                        if str(i.location.x)==request.GET['xs'].split(',')[j]:
                            if str(i.location.y)==request.GET['ys'].split(',')[j]:
                                if str(i.date_from)==request.GET['dfroms'].split(',')[j].split("T")[0]:
                                    if str(i.date_to)==request.GET['dtos'].split(',')[j].split("T")[0]:
                                        if str(i.get_category_display())==request.GET['categories'].split(',')[j].lower():
                                            counter=1
                                            break

            if counter==0:
                removelist.append(i)
        for i in removelist:
            i.delete()

        model=Case
        Case.objects.filter(case_id__exact=request.GET['oldcaseid']).update(case_id=request.GET['caseid'], date=request.GET['confirmeddate'], category=request.GET['localimported'][0].lower())
        model=Patient
        Patient.objects.filter(case__case_id__exact=request.GET['oldcaseid']).update(lastname=request.GET['patientname'].split(' ')[0], firstname=request.GET['patientname'].split(' ')[1]+" "+request.GET['patientname'].split(' ')[2], idn=request.GET['IDN'], dob=request.GET['DoB'])
        model=Virus
        Virus.objects.filter(case__case_id__exact=request.GET['oldcaseid']).update(name=request.GET['virusname'], common_name=request.GET['commonname'], period=request.GET['MIP'])

    return redirect('/cases/'+caseid)
