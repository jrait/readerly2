from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User,Author,Book,Event
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

def add_book(request):
    db_book = Book.objects.filter(google_id = request.POST['google_id'])
    user = User.objects.get(id = int(request.session['userid']))
    if db_book:
        user.fav_books.add(db_book[0])
    else:
        new_book = Book.objects.create(
            title = request.POST['title'],
            image_link = request.POST['image'],
            google_id = request.POST['google_id'],
            desc = request.POST['desc'],
            link = 'https://www.indiebound.org/'
        )
        user.fav_books.add(new_book)
        
    return redirect('/dashboard')

def remove_book(request,book_id):
    db_book = Book.objects.get(id = book_id)
    user = User.objects.get(id = int(request.session['userid']))
    user.fav_books.remove(db_book)
    return redirect('/dashboard')

def user_search(request):
    request.session['search'] = request.POST['search_users']
    return redirect('/user_search_results')

def user_search_results(request):
    search_results = request.session['search']
    list_results = search_results.split()
    all_items = []
    for item in list_results:
        email = User.objects.filter(email = item)
        first_name = User.objects.filter(first_name = item)
        last_name = User.objects.filter(last_name =item)
        if email:
            all_items.append(email)
        if first_name:
            all_items.append(first_name)
        if last_name:
            all_items.append(last_name)
    context = {
        'results': all_items
    }
    return render (request,'user_search.html',context)
    
def userpage(request,userid):

    return render(request,'userpage.html')

def show_update_account_page(request,user_id):
    context = {
        'user': User.objects.get(id=int(request.session['userid']))
    }
    return render(request, 'update_account.html',context)


def update_account(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['userid'])
        errors = User.objects.update_acct_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect(f'/myaccount/{ user.id }')
        
        user.first_name = request.POST['update_first_name']
        user.last_name = request.POST['update_last_name']
        user.email = request.POST['update_email']
        user.save()
        return redirect(f'/myaccount/{ user.id }')
    else:
        return redirect('/logout')


def update_password(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['userid'])
        errors = User.objects.update_pw_validator(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value,extra_tags=key)
            return redirect(f'/myaccount/{user.id}')
        pw = bcrypt.hashpw(request.POST['update_password'].encode(),bcrypt.gensalt()).decode()
        user.password = pw
        user.save()
        return redirect(f'/myaccount/{user.id}')
    else:
        return redirect('/logout')
