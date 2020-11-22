from django.urls import path
from cases import views

urlpatterns=[
    path('<int:case_id>/add_visit', views.AddVisit.as_view(), name='add_visit'),
    path('get-locations', views.getLocations, name='get-locations'),
    path('add-location', views.addLocation, name='add-location'),
    path('add', views.add, name='add'),

    path('', views.Root.as_view(), name='root'),
    path('<int:case_id>/view_visits', views.ViewVisits.as_view(), name='view_visits'),
    path('<int:case_id>', views.CaseView.as_view(), name='case'),
    path('save', views.save, name='save'),
]
