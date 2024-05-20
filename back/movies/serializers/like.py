from rest_framework import serializers
from ..models import Movie, People, Genre, Keyword
 


# 영화 리스트
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id','title','poster_path','popularity','release_date','origin_country','status',)