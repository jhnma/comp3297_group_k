from django.shortcuts import render, redirect

# Create your views here.
def redirectViewCases(request):
    return redirect("/cases", permanent=True)