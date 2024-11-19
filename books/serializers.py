from django.utils.timezone import now
from rest_framework import serializers

from books.models import Author, Genre, Book, Rent
from datetime import timedelta
from .services import TAX_20_VALUE
from .validators import IsAmountNegative, CanNotEdit


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
    # for string related fields in response of JSON serialization
    genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    genre_ = serializers.StringRelatedField(source='genre', many=True, read_only=True)
    author = serializers.PrimaryKeyRelatedField(many=True, queryset=Author.objects.all())
    author_ = serializers.StringRelatedField(source='author', many=True, read_only=True)

    def to_representation(self, instance):
        """In order to hide 'books' field from response of server"""
        if self.fields.get('genre'):
            self.fields.pop('genre')
        if self.fields.get('author'):
            self.fields.pop('author')
        return super().to_representation(instance)

    class Meta:
        model = Book
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    """Class-model for rent serializers"""
    retail_amount = serializers.FloatField(required=True, validators=[IsAmountNegative()])
    books = serializers.PrimaryKeyRelatedField(many=True, queryset=Book.objects.all())
    books_ = serializers.StringRelatedField(source='books', many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault(), )  # hide user field API
    deadline = serializers.DateTimeField(required=False, validators=[CanNotEdit()])
    tax_amount = serializers.FloatField(required=False, validators=[CanNotEdit()])
    published = serializers.DateTimeField(validators=[CanNotEdit()])
    record_updated = serializers.DateTimeField(read_only=True, validators=[CanNotEdit()])

    def to_representation(self, instance):
        """In order to hide 'books' field from response of server"""
        if self.fields.get('books'):
            self.fields.pop('books')
        return super().to_representation(instance)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['deadline'] = now() + timedelta(days=validated_data['term'])
        validated_data['tax_amount'] = round(validated_data['retail_amount'] * TAX_20_VALUE, 2)
        for book in validated_data.get('books'):
            book.is_available = False
            book.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Method updates values in validated data, as well as for related_fields which depend on the value of
        another fields and automatically formulas"""
        related_fields = {'term': 'deadline', 'retail_amount': 'tax_amount'}
        formula_for_related_fields = {'deadline': instance.published + timedelta(days=validated_data.get('term')),
                                      'tax_amount': round(validated_data.get('retail_amount') * TAX_20_VALUE, 2)}
        for data_ in validated_data:
            if data_ in related_fields:
                setattr(instance, related_fields.get(data_), formula_for_related_fields.get(related_fields[data_]))
            instance.data_ = validated_data.get(data_)
        instance.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Rent
        fields = '__all__'

class RentReturnBackSerializer(serializers.ModelSerializer):
    books = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Rent
        fields = ['id', 'books', 'are_books_returned']