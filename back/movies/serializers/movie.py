from rest_framework import serializers
from ..models import Movie, Actor
from .actor import ActorSerializer


# 영화 리스트
class MovieSerializer(serializers.ModelSerializer):
    class MovieactorSerializer(serializers.ModelSerializer):
        class Meta:
            model = Actor
            fields = ('id','name',)
    
    
    actors = MovieactorSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'
    
