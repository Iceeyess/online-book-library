from django.utils.timezone import now
from rest_framework import serializers

from books.models import Author, Genre, Book, Rent
from datetime import timedelta
from .services import TAX_20_VALUE
from .validators import IsAmountNegative


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
    genre = serializers.StringRelatedField(many=True)  # for string related fields in response of JSON serialization
    author = serializers.StringRelatedField(many=True)  # same
    class Meta:
        model = Book
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    """Class-model for rent serializers"""
    retail_amount = serializers.FloatField(required=True, validators=[IsAmountNegative()])
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    books_ = serializers.StringRelatedField(source='books', many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())  # hide user field API
    is_book_returned = serializers.HiddenField(default=False)
    deadline = serializers.DateTimeField(required=False)
    tax_amount = serializers.FloatField(required=False)

    def to_representation(self, instance):
        """In order to hide 'books' field from response of server"""
        if self.fields.get('books'):
            self.fields.pop('books')
        return super().to_representation(instance)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['deadline'] = now() + timedelta(days=validated_data['term'])
        validated_data['tax_amount'] = round(validated_data['retail_amount'] * TAX_20_VALUE, 2)  # add tax amount to validated data
        return super().create(validated_data)


    class Meta:
        model = Rent
        fields = '__all__'