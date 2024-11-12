from django.db import models


NULLABLE = dict(blank=True, null=True)
# Create your models here.
class Author:
    """The class-model of Author"""
    full_name = models.CharField(max_length=255, help_text='Author full name', )
    birth_date = models.DateField(help_text='Birthdate date', **NULLABLE)
    death_date = models.DateField(help_text='Death date', **NULLABLE)
    biography = models.TextField(help_text='Author biography')
    image = models.ImageField(upload_to='photo/authors/', help_text='Photo', **NULLABLE)

    def __repr__(self):
        return self.full_name


    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ('pk', )

class Genre:
    """The class-model of the Genre"""
    name = models.CharField(max_length=100, help_text='Genre name', unique=True)

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ('name', )

class Book:
    """The class-model of the Book"""
    title = models.CharField(max_length=255, help_text='Book title')
    description = models.TextField(help_text='Book description')
    publication_book_year = models.PositiveIntegerField(help_text='Publication book year')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ManyToManyField(Genre, related_name='books')
    image = models.ImageField(upload_to='photo/books/', help_text='Photo', **NULLABLE)
    rating = models.FloatField(help_text='Book rating', default=0)
    num_pages = models.IntegerField(help_text='Number of pages', **NULLABLE)

