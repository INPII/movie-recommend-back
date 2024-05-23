from rest_framework import serializers
from ..models import People,Movie

class MovieSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'release_date', 'origin_country', 'is_liked')

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False


# 사람 리스트
class PeopleListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = People
        fields = ('id', 'name', 'profile_path', 'is_liked')

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False





# 사람 상세 리스트

class PeopleDetailSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    filmography = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = People
        fields = '__all__'

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return False
    
    