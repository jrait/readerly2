from django.urls import path
from . import views

urlpatterns = [
    path('simpleMap', views.simpleMap),
    path("simpleMap2", views.simpleMap2),
    path('simpleMap3', views.simpleMap3),
    path('simpleMap4', views.simpleMap4),
    path('newScrape', views.newScrape),
    path('', views.eventsMap)
]