# Generated by Django 2.2.4 on 2020-10-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('readerly_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('image_link', models.CharField(max_length=255)),
                ('link', models.CharField(max_length=255)),
                ('google_id', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('faved_by', models.ManyToManyField(related_name='fav_books', to='readerly_app.User')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('desc', models.TextField()),
                ('time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('authors_event', models.ManyToManyField(related_name='events_for_author', to='readerly_app.Author')),
                ('books_event', models.ManyToManyField(related_name='events_for_book', to='readerly_app.Book')),
                ('users_going_to_event', models.ManyToManyField(related_name='events', to='readerly_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(related_name='authors', to='readerly_app.Book'),
        ),
        migrations.AddField(
            model_name='author',
            name='faved_by',
            field=models.ManyToManyField(related_name='fav_authors', to='readerly_app.User'),
        ),
    ]
