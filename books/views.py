from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from books.models import Author, Genre, Book, Rent
from books.serializers import AuthorSerializer, GenreSerializer, BookSerializer, RentSerializer
from users.permissions import IsSuperuser


# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    """Class for author CRUD"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsSuperuser | IsAdminUser]

class GenreViewSet(viewsets.ModelViewSet):
    """Class for manage genre CRUD"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsSuperuser | IsAdminUser]

class BookViewSet(viewsets.ModelViewSet):
    """Class for book CRUD"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsSuperuser | IsAdminUser]

class RentViewSet(viewsets.ModelViewSet):
    """Class for rent CRUD"""
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    # permission_classes = [TBD]
