from django.urls import path
from cases import views

urlpatterns=[
    path('add-visit', views.AddVisit.as_view(), name='add-visit'),
    path('get-locations', views.getLocations, name='get-locations'),
    path('add-location', views.addLocation, name='add-location'),
    path('add', views.add, name='add')
]