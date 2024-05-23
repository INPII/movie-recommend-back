from rest_framework import serializers
from ..models import Genre, Movie


# 장르
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
# 장르 상세정보
class GenreDetailSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        overview = serializers.SerializerMethodField()
        title = serializers.SerializerMethodField()

        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path', 'release_date', 'origin_country', 'overview')

        def get_overview(self, obj):
            return obj.overview_kr if obj.overview_kr else obj.overview

        def get_title(self, obj):
            return obj.name_kr if obj.name_kr else obj.title
    
    genre_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = '__all__'
    
