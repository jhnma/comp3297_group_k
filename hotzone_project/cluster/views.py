from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

# Create your views here.
class Cluster(TemplateView):
    template_name = "cluster.html"

    def get(self, request, **kwargs):
        if request.method == 'GET':
            c = request.GET.get('c', 0)
            d = request.GET.get('d', 0)
            t = request.GET.get('t', 0)
            if (c and d and t):
                context = {'d':d, 'c':c, 't':t}
                return render(request, self.template_name, context)
            else:
                return render(request, self.template_name, {})
        else:
            return HttpResponse("Bad Request")