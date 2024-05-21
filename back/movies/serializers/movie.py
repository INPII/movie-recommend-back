from rest_framework import serializers
from ..models import Movie, People, Genre, Keyword,SurveyResponse
from accounts.models import User  
 


# 영화 리스트
class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id','title','poster_path','popularity','release_date','origin_country','status',)

    
# 영화 상세 페이지
class MovieDetailSerializer(serializers.ModelSerializer):
    
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'
    
    class PeopleSerializer(serializers.ModelSerializer):
        class Meta:
            model = People
            fields = ('id', 'name','profile_path',)
    
    class KeywordSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keyword
            fields = '__all__'
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'
            
    like_movie = UserSerializer(allow_null=True, many=True,read_only=True)
    genres = GenreSerializer(allow_null=True,many=True,read_only=True)
    people = PeopleSerializer(allow_null=True, many=True,read_only=True)
    keyword = KeywordSerializer(allow_null=True, many=True,read_only=True)
    overview = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_overview(self, obj):
        return obj.overview_kr if obj.overview_kr else obj.overview


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6']