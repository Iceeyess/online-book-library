from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
import datetime

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
    # permission_classes = [IsSuperuser | IsAdminUser]


class BookViewSet(viewsets.ModelViewSet):
    """Class for book CRUD"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # permission_classes = [IsSuperuser | IsAdminUser]


class RentViewSet(viewsets.ModelViewSet):
    """Class for rent CRUD"""
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, *args, **kwargs):
        """Method to get status Rent object in response server"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        for_response = {
            'id': serializer.data.get('id'),
            'books_': serializer.data.get('books_'),
            'deadline': serializer.data.get('deadline'),
            'status': 'Срок просрочен' if datetime.datetime.strptime(serializer.data.get('deadline'),
                                                                '%Y-%m-%dT%H:%M:%S.%f%z') < now() else 'В аренде',
        }
        return Response(for_response)
