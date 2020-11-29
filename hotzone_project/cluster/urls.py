from django.urls import path
from cluster import views

urlpatterns=[
    path('', views.Cluster.as_view(), name='cluster'),
]
