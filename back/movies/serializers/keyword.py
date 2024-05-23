from rest_framework import serializers
from ..models import Keyword, Movie


# 장르
class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = '__all__'
# 장르 상세정보
class KeywordDetailSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id','title','poster_path',)
    keyword_movies = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = Keyword
        fields = '__all__'