from rest_framework import serializers
from ..models import Movie, People, Genre, Keyword,SurveyResponse
from accounts.models import User  
from .review import ReviewListSerializer
 
class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = ('id', 'name', 'profile_path', 'is_liked')

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False
    
    
#영화 리스트
class MovieListSerializer(serializers.ModelSerializer):
    
    title = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'popularity', 'release_date', 'origin_country', 'status','is_liked')

    def get_title(self, obj):
        return obj.name_kr if obj.name_kr else obj.title
    
    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False


# 영화 상세 페이지
class MovieDetailSerializer(serializers.ModelSerializer):
    class GenreSerializer(serializers.ModelSerializer):
        class Meta:
            model = Genre
            fields = '__all__'

    class KeywordSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keyword
            fields = '__all__'

    genres = GenreSerializer(allow_null=True, many=True, read_only=True)
    people = PeopleSerializer(allow_null=True, many=True, read_only=True)
    keywords = KeywordSerializer(allow_null=True, many=True, read_only=True)
    overview = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    reviews = ReviewListSerializer(source='review_set', many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = '__all__'

    def get_overview(self, obj):
        return obj.overview_kr if obj.overview_kr else obj.overview

    def get_title(self, obj):
        return obj.name_kr if obj.name_kr else obj.title

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False


class SurveyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyResponse
        fields = ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'question_6']