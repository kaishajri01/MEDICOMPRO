from rest_framework import serializers
from .models import UserMed

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model =UserMed
        fields='__all__'