from rest_framework import serializers


class IsAmountNegative:
    """This class is to be check if a number is a negative or equal to zero."""
    def __call__(self, value):
        """Amount field verification. Amount must be positive."""
        if value <= 0:
            raise serializers.ValidationError('Amount must be strictly positive.')


class CanNotEdit:
    """This class is to check if fields are not editable by user, just to demonstrate as a workaround
    for serializer that not only attribute 'read_only' is good for that purpose."""
    def __call__(self, *args, **kwargs):
        """This validation function checks on the availability to turn-off a change to edit a field."""
        if args:
            raise serializers.ValidationError('Field is protected to any create or update.')
