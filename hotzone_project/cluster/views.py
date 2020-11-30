from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse

# Create your views here.
class Cluster(View):
    template_name = "cluster.html"

    def get(self, request):
        return render(request, self.template_name, {})

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