from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from cases.models import Case, Location, Visit
from cluster.clustering import doClustering
import datetime
import numpy as np

# Create your views here.
class Cluster(View):
    template_name = "cluster.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request):
        c = request.POST.get('c', 0)
        d = request.POST.get('d', 0)
        t = request.POST.get('t', 0)

        if (c and d and t):
            try:
                visits = list(Visit.objects.values('case', 'location_id', 'date_from'))
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Case doesn't exist.")
            
            vector = []

            caseLocation=[]
            counter=0

            for visit in visits:
                case_id=int(Case.objects.filter(id=visit['case']).values('case_id')[0]['case_id'])
                caseLocation.append([case_id, list(Location.objects.values('name').filter(id=visit['location_id']))[0]['name']])
                vector.append([
                    list(Location.objects.values('x').filter(id=visit['location_id']))[0]['x'],
                    list(Location.objects.values('y').filter(id=visit['location_id']))[0]['y'],
                    (visit['date_from'] - datetime.date(2020, 1, 1)).days,
                    counter
                ])
                counter=counter+1
            
            vector = np.array(vector)
            cluster_result = doClustering(vector, int(d), int(t), int(c), caseLocation)
            context = {'d':d, 'c':c, 't':t, 'cluster_result': cluster_result}
            return render(request, self.template_name, context)

        else:
            return render(request, self.template_name, {})