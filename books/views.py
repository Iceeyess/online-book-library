from django.core.serializers import serialize
from django.shortcuts import render
from django.utils.timezone import now
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
import datetime
from django_filters import rest_framework as filters
from books.models import Author, Genre, Book, Rent
from books.serializers import (AuthorSerializer, GenreSerializer, BookSerializer, RentSerializer,
                               RentReturnBackSerializer)
from books.services import return_book_back
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

class BookListListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['title', 'publication_book_year', 'author', 'genre', ]
    ordering_fields = ('title', )


class RentViewSet(viewsets.ModelViewSet):
    """Class for rent CRUD"""
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = [AllowAny, ]

    def retrieve(self, request, *args, **kwargs):
        """Method to get status Rent object in response server"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = {
            'id': serializer.data.get('id'),
            'books_': serializer.data.get('books_'),
            'deadline': serializer.data.get('deadline'),
            'status': 'Срок просрочен' if datetime.datetime.strptime(serializer.data.get('deadline'),
                                                                     '%Y-%m-%dT%H:%M:%S.%f%z') < now() else (
                'Аренда закрыта' if instance.are_books_returned else 'В аренде'),
        }
        return Response(response)

class ReturnBackBookUpdateAPIView(generics.UpdateAPIView):
    queryset = Rent
    serializer_class = RentReturnBackSerializer

    def update(self, request, *args, **kwargs):
        """This API checks if Rent object attribute 'are_books_returned' is False, then it switches on True value"""
        instance = self.get_object()
        return_book_back(instance)
        return super().update(request, *args, **kwargs)
