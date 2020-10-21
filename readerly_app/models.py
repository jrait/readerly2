from django.db import models
import re
from datetime import datetime,timedelta

# Create your models here.
class UserManager(models.Manager):
    def validator(self,postData):
        errors = {}
        today = datetime.now()
        if not postData['birthday']:
            errors['birthday'] = "Birthday is required!"
        else: 
            birthday = datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if birthday > today:
                errors['future_baby'] = "Birthday must be in the past!"
            elif (today - birthday).days < 4745:
                errors['age'] = "User must be at least 13 years old"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            errors['first_name'] = "First name must be 2 or more characters!"
        if len(postData['last_name'])<2:
            errors['last_name'] = "Last name must be 2 or more characters!"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password'])<8:
            errors['password'] = "Password must be 8 or more characters!"
        if postData['password'] != (postData['password2']):
            errors['password_match'] = "Passwords do not match!"
        if len(User.objects.filter(email = postData['email'])) > 0:
            errors['email_exists'] = "Email Already Exists!"
        
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length =255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    #fav_books - user's favorite books, related to Book
    #fav_authors - user's favorite authors, related to Author
    #events - user's attending events, related to Event


class Book(models.Model):
    title =  models.CharField(max_length = 255)
    image_link = models.CharField(max_length = 255)
    faved_by = models.ManyToManyField(User, related_name = "fav_books")
    link = models.CharField(max_length = 255)
    google_id = models.CharField(max_length = 255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #authors - book's author, related to Author
    #events_for_book - related to Event



class Author(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length =255)
    books = models.ManyToManyField(Book, related_name = "authors")
    faved_by = models.ManyToManyField(User, related_name = "fav_authors")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    #events_for_author - related to Event


class Event(models.Model):
    name = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    desc = models.TextField()
    time = models.DateTimeField()
    users_going_to_event = models.ManyToManyField(User, related_name = "events")
    books_event = models.ManyToManyField(Book, related_name = "events_for_book")
    authors_event = models.ManyToManyField(Author, related_name = "events_for_author")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)