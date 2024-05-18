from rest_framework import serializers
from ..models import Actor


# 영화 리스트
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'
    