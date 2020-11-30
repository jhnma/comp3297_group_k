from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from cases.models import Case, Location, Visit, Patient, Virus
from sklearn.cluster import DBSCAN
import datetime
import numpy as np
import math

# Create your views here.
class Cluster(View):
    template_name = "cluster.html"

    def get(self, request, *args, **kwargs):
        try:
            visits = list(Visit.objects.values('id', 'location_id', 'date_from'))
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Case doesn't exist.")
        
        vector = []

        for visit in visits:
            vector.append([
                list(Location.objects.values('x').filter(id=visit['location_id']))[0]['x'],
                list(Location.objects.values('y').filter(id=visit['location_id']))[0]['y'],
                (visit['date_from'] - datetime.date(2020, 1, 1)).days,
                visit['id']
            ])
        
        vector = np.array(vector)
        return render(request, self.template_name, {'vector': vector})

    def post(self, request):
        c = request.POST.get('c', 0)
        d = request.POST.get('d', 0)
        t = request.POST.get('t', 0)
        #print(c, d, t)

        # TODO: Clustering
        if (c and d and t):
            cluster_result = {}
            context = {'d':d, 'c':c, 't':t, 'cluster_result': cluster_result}
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})