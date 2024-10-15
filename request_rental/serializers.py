from .models import RequestRental
from rest_framework import serializers


class RequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = RequestRental
        fields = ('id', 'user', 'book', 'status', 'created_at', 'updated_at')
