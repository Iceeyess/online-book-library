from datetime import datetime, timedelta
from django.db import models

from users.models import User

NULLABLE = dict(blank=True, null=True)
# Create your models here.
class Author(models.Model):
    """The class-model of Author"""
    full_name = models.CharField(max_length=255, help_text='Author full name', )
    birth_date = models.DateField(help_text='Birthdate date', **NULLABLE)
    death_date = models.DateField(help_text='Death date', **NULLABLE)
    biography = models.TextField(help_text='Author biography', **NULLABLE)
    image = models.ImageField(upload_to='photo/authors/', help_text='Photo', **NULLABLE)

    def __repr__(self):
        return self.full_name

    def __str__(self):
        return self.full_name


    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ('pk', )

class Genre(models.Model):
    """The class-model of the Genre"""
    name = models.CharField(max_length=100, help_text='Genre name', unique=True)

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ('name', )

class Book(models.Model):
    """The class-model of the Book"""
    title = models.CharField(max_length=255, help_text='Book title')
    description = models.TextField(help_text='Book description')
    publication_book_year = models.PositiveIntegerField(help_text='Publication book year')
    author = models.ManyToManyField(Author, help_text='Author', related_name='authors_list')
    genre = models.ManyToManyField(Genre, help_text='Genre', related_name='genres_list')
    image = models.ImageField(upload_to='photo/books/', help_text='Photo', **NULLABLE)
    num_pages = models.IntegerField(help_text='Number of pages', **NULLABLE)


    def __repr__(self):
        return f'Book - {self.title}, author - {self.author}'

    def __str__(self):
        return f'Book - {self.title}, author - {self.author}'

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ('title', )


class Rent(models.Model):
    """The class-model of the balance which consists from the status rent books"""
    book = models.ManyToManyField(Book, help_text='rent book', related_name='books_list')
    transaction_date_created = models.DateTimeField(auto_now_add=True, help_text='Date of transaction')
    transaction_date_update = models.DateTimeField(auto_now=True, help_text='Date of last update transaction')
    is_book_returned = models.BooleanField(default=False, help_text='Shows if book was returned to library')
    term = models.PositiveIntegerField(help_text='Field depends on how long book was took rent in days')
    retail_amount = models.FloatField(help_text='Total amount, excluded tax')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, help_text='debtor user', **NULLABLE)
    deadline = models.DateTimeField(help_text='The deadline date of rent book, red flag!', **NULLABLE)
    tax_amount = models.FloatField(help_text='Total tax amount for revenue', **NULLABLE)

    def __repr__(self):
        return f'Rent user - {self.user}, Term - {self.term} days'

    def __str__(self):
        return f'Rent user - {self.user}, Term - {self.term} days'

    class Meta:
        verbose_name = 'Rent'
        verbose_name_plural = 'Rents'
        ordering = ('id', )