from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import History


class _UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')


class ListHistorySerializer(serializers.ModelSerializer):
    user = _UserSerializer(read_only=True)
    class Meta:
        model = History
        fields = '__all__'


class CreateHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'