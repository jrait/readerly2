from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User
import bcrypt
from datetime import datetime
import requests

# Create your views here.
def index(request):
    context = {
        'all_users': User.objects.all()
    }

    return render(request,'index.html',context)

def register(request):
    errors = User.objects.validator(request.POST)
    if len (errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        logged_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            birthday = request.POST['birthday'],
            password = pw_hash)
        request.session['userid'] = logged_user.id
        return redirect('/dashboard')

def login(request):
    user = User.objects.filter(email = request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(),logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/dashboard')

    messages.error(request,"User or password is incorrect")
    return redirect('/')

def dashboard(request):
    if 'userid' in request.session:
        context = {
            'user':User.objects.get(id = int(request.session['userid'])),
        }
        return render(request,'dashboard.html',context)
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def search_books(request):
    if request.POST == '':
        return redirect('/dashboard')
    else:
        search = request.POST['search_books']
        results = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=40')
        request.session['results'] = results.json()
    return redirect('/search_books_results')

def search_books_results(request):
    context = {
            'results': request.session['results']['items']
        }
    return render(request,'search_results.html',context)

def show_events_page(request):
    return render(request, 'events_page.html')

def go_back(request):
    return redirect('/dashboard')