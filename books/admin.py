from django.contrib import admin
from books.models import Author, Genre, Book, Rent


# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'birth_date', )
    list_filter = ('id', 'full_name', 'birth_date', )
    search_fields = ('full_name', 'full_name', 'birth_date', 'death_date', )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )
    list_filter = ('id', 'name', )
    search_fields = ('id', 'name', )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_book_year',)
    list_filter = ('id', 'title', 'author', 'publication_book_year',)
    search_fields = ('id', 'title', 'author', 'publication_book_year', 'genre', )


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'book__title', 'user__username', )
    list_filter = ('id', 'is_book_returned', 'transaction_date_created', 'term', 'deadline', )
    search_fields = ('id', 'title', 'author', 'publication_book_year', 'genre', 'term', 'deadline', )
