from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('logout',views.logout),
    path('search_books',views.search_books),
    path('events', views.show_events_page),
    path('go_back', views.go_back),
    path('search_books_results',views.search_books_results)
]