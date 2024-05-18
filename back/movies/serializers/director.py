from rest_framework import serializers
from ..models import Director


# 영화 리스트
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'
    