from rest_framework import serializers
from ..models import Genre



# 장르
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
    
