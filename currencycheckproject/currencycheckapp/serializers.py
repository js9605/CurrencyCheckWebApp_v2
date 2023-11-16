from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Currency, UserProfile


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = [
                # 'currency_name',
                'currency_shortcut',
                'country',
                'ref_number',
                'purchase_rate',
                'selling_rate',
                'average_exchange_rate',
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    currencies = serializers.PrimaryKeyRelatedField(many=True, queryset=Currency.objects.all())

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'currencies']


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']
