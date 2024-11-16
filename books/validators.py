from rest_framework import serializers


class IsAmountNegative:

    def __call__(self, value):
        """Amount field verification. Amount must be positive."""
        if value <= 0:
            raise serializers.ValidationError('Amount must be strictly positive.')