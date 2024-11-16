from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, AllowAny
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

    # def create(self, request, *args, **kwargs):
    #     """Creates a new rent record"""
    #     # Add user to rent record
    #     request['user'] = self.context['request'].user  # get user from request context
    #     # ['deadline'] = self.data['transaction_date_created'] + timedelta(days=self.data['term'])
    #     # validated_data['tax_amount'] = self.data['retail_amount'] * TAX_20_VALUE
    #     return super().create(request, *args, **kwargs)
    # def perform_create(self, serializer):
    #     pass