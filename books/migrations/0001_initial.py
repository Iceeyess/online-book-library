# Generated by Django 5.1.3 on 2024-11-13 21:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(help_text='Author full name', max_length=255)),
                ('birth_date', models.DateField(blank=True, help_text='Birthdate date', null=True)),
                ('death_date', models.DateField(blank=True, help_text='Death date', null=True)),
                ('biography', models.TextField(blank=True, help_text='Author biography', null=True)),
                ('image', models.ImageField(blank=True, help_text='Photo', null=True, upload_to='photo/authors/')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
                'ordering': ('pk',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Genre name', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Book title', max_length=255)),
                ('description', models.TextField(help_text='Book description')),
                ('publication_book_year', models.PositiveIntegerField(help_text='Publication book year')),
                ('image', models.ImageField(blank=True, help_text='Photo', null=True, upload_to='photo/books/')),
                ('num_pages', models.IntegerField(blank=True, help_text='Number of pages', null=True)),
                ('author', models.ForeignKey(help_text='Author', on_delete=django.db.models.deletion.CASCADE, to='books.author')),
                ('genre', models.ManyToManyField(help_text='Genre', to='books.genre')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
                'ordering': ('title',),
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date_created', models.DateField(auto_now_add=True, help_text='Date of transaction')),
                ('transaction_date_update', models.DateField(auto_now=True, help_text='Date of last update transaction')),
                ('are_books_returned', models.BooleanField(default=False, help_text='Shows if book was returned to library')),
                ('term', models.PositiveIntegerField(help_text='Field depends on how long book was took rent in days')),
                ('deadline', models.DateField(help_text='The deadline date of rent book, red flag!')),
                ('retail_amount', models.FloatField(help_text='Total amount, excluded tax')),
                ('tax_amount', models.FloatField(help_text='Total tax amount for revenue')),
                ('book', models.ForeignKey(help_text='rent book', on_delete=django.db.models.deletion.DO_NOTHING, to='books.book')),
                ('user', models.ForeignKey(help_text='debtor user', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Rent',
                'verbose_name_plural': 'Rents',
                'ordering': ('id',),
            },
        ),
    ]
