from django.urls import path
from cases import views

urlpatterns=[
    path('<int:case_id>/add_visit', views.AddVisit.as_view(), name='add_visit'),
    path('get-locations', views.getLocations, name='get-locations'),
    path('add-location', views.addLocation, name='add-location'),
    path('add', views.add, name='add')
]