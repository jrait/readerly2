from django.urls import path
from . import views

urlpatterns = [
    path('simpleMap', views.simpleMap),
    path("simpleMap2", views.simpleMap2),
    path('', views.simpleMap3)
]