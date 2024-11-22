from rest_framework import serializers


class IsValidPhoneValidator:

    def __call__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError('Phone number must be 10 digits and must consists from numbers only')
