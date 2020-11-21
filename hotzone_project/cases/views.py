from django.shortcuts import render, redirect
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
