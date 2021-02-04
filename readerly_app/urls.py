from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('dashboard',views.dashboard),
    path('logout',views.logout),
    path('search_books',views.search_books),
    path('eventMap', views.show_events_page),
    path('go_back', views.go_back),
    path('search_books_results',views.search_books_results),
    path('add_book',views.add_book),
    path('remove_book/<int:book_id>',views.remove_book),
    path('user_search',views.user_search),
    path('user/<int:userid>',views.userpage),
    path('user_search_results',views.user_search_results),
    path('myaccount/<int:user_id>', views.show_update_account_page),
    path('update_account', views.update_account),
    path('update_password', views.update_password),
    path('book_info/<int:book_id>',views.book_info),
    path('guest',views.guest),
]