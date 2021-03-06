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

def guest(request):
    user = User.objects.filter(email = 'guest')
    request.session['userid'] = user[0].id
    return(redirect('/dashboard'))

def register(request):
    errors = User.objects.validator(request.POST)
    if len (errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        logged_user = User.objects.create(
            first_name = request.POST['first_name'].lower(),
            last_name = request.POST['last_name'].lower(),
            email = request.POST['email'].lower(),
            # birthday = request.POST['birthday'],
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
    if len(request.POST['search_books'])<1:
        return redirect('/dashboard')
    else:
        search = request.POST['search_books']
        request.session['search'] = search
        results = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={search}&maxResults=40')
        request.session['results'] = results.json()
        return redirect('/search_books_results')

def search_books_results(request):
    context = {
            'results': request.session['results']['items'],
            'user': User.objects.get(id = int(request.session['userid']))
        }
    return render(request,'search_results.html',context)

def show_events_page(request):
    return redirect('/eventsApp/eventMap')

def go_back(request):
    return redirect('/dashboard')

def add_book(request):
    db_book = Book.objects.filter(google_id = request.POST['google_id'])
    user = User.objects.get(id = int(request.session['userid']))
    #check if book is already in database
    #if book exists within database, add to current user
    if db_book:
        user.fav_books.add(db_book[0])
    #Otherwise, create book object in DB and add to current user
    else:
        new_book = Book.objects.create(
            title = request.POST['title'],
            image_link = request.POST['image'],
            google_id = request.POST['google_id'],
            desc = request.POST['desc'],
            link = 'https://www.indiebound.org/'
        )
        user.fav_books.add(new_book)
        #Convert author data from 1 string to a list of strings
        authors = request.POST['author']
        authors = authors.replace("[","")
        authors = authors.replace("]","")
        authors = authors.replace("'","")
        authors_list = authors.split(",")
        #check each author in list to see if it's in the DB
        for author in authors_list:
            author_check = Author.objects.filter(name = author)
            #if author already exists, add book
            if author_check:
                author_check[0].books.add(new_book)
            #Otherwise, create author and add book to author
            else:
                new_author = Author.objects.create(
                    name = author,
                )
                new_book.authors.add(new_author)
            
    return redirect('/dashboard')

def remove_book(request,book_id):
    db_book = Book.objects.get(id = book_id)
    user = User.objects.get(id = int(request.session['userid']))
    user.fav_books.remove(db_book)
    return redirect('/dashboard')

def user_search(request):
    if len(request.POST['search_users'])<1:
        return redirect('/dashboard')
    else:
        request.session['search'] = request.POST['search_users']
        return redirect('/user_search_results')

def user_search_results(request):
    search_results = User.objects.search(request.session['search'])
    context = {
        'results': search_results
    }
    return render (request,'user_search.html',context)
    
def userpage(request,userid):
    context = {
        'page_user': User.objects.get(id = userid),
        'user':User.objects.get(id = int(request.session['userid'])),
    }
    return render(request,'userpage.html',context)

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

def book_info(request,book_id):
    context= {
        'book':Book.objects.get(id=book_id),
        'user': User.objects.get(id=int(request.session['userid']))
    }
    return render(request,'book_info.html',context)