from rest_framework import serializers
from .models import Profile


class IdCardPicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id_card']
