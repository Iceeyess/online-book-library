from rest_framework import serializers

from books.models import Author, Genre, Book, Rent
from datetime import timedelta
from .services import TAX_20_VALUE


class AuthorSerializer(serializers.ModelSerializer):
    """Class-model for author serializers"""
    class Meta:
        model = Author
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    """Class-model for genre serializers"""
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    """Class-model for book serializers"""
    class Meta:
        model = Book
        fields = '__all__'

class RentSerializer(serializers.ModelSerializer):
    """Class-model for rent serializers"""
    deadline = serializers.SerializerMethodField()
    tax_amount = serializers.SerializerMethodField()

    class Meta:
        model = Rent
        fields = '__all__'

    def get_deadline(self, obj):
        """Calculates a deadline date for rent book"""
        return obj.transaction_date_created + timedelta(days=obj.term)

    def get_tax_amount(self, obj):
        """Calculates a tax amount for rent book"""
        return obj.retail_amount * TAX_20_VALUE


