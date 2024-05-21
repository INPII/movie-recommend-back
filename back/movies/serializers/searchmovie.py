from rest_framework import serializers
from ..models import Movie,Genre,People,Keyword
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('name',)

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('name',)

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    people = PeopleSerializer(many=True)
    keywords = KeywordSerializer(many=True, source='keyword')
    
    class Meta:
        model = Movie
        fields = ('id','title', 'keywords', 'overview', 'people','genres','people','keywords','poster_path',)