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
    keywords = KeywordSerializer(many=True)  
    overview = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_overview(self, obj):
        return obj.overview_kr if obj.overview_kr else obj.overview

    def get_title(self, obj):
        return obj.name_kr if obj.name_kr else obj.title
