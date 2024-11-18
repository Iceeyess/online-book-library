from curses.ascii import isalpha

from rest_framework import serializers


class IsAmountNegative:

    def __call__(self, value):
        """Amount field verification. Amount must be positive."""
        if value <= 0:
            raise serializers.ValidationError('Amount must be strictly positive.')

class CanNotEdit:

    def __call__(self, *args, **kwargs):
        """This validation function checks on the availability to turn-off a change to edit a field."""
        if args:
            raise serializers.ValidationError('Field is protected to create/update.')