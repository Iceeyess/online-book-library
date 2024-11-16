from rest_framework import serializers

from books.models import Author, Genre, Book, Rent
from datetime import timedelta, datetime
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
    retail_amount = serializers.FloatField(required=True, validators=[IsAmountNegative()])
    """Class-model for rent serializers"""
    # book = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # deadline = serializers.SerializerMethodField()
    # tax_amount = serializers.SerializerMethodField()

    # def get_deadline(self, obj):
    #     """Calculates a deadline date for rent book"""
    #     return obj.transaction_date_created + timedelta(days=obj.term)
    #
    # def get_tax_amount(self, obj):
    #     """Calculates a tax amount for rent book"""
    #     return obj.retail_amount * TAX_20_VALUE

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['deadline'] = datetime.now() + timedelta(days=validated_data['term'])
        validated_data['tax_amount'] = round(validated_data['retail_amount'] * TAX_20_VALUE, 2)  # add tax amount to validated data
        return super().create(validated_data)


    class Meta:
        model = Rent
        fields = '__all__'

