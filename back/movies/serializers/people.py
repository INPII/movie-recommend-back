from rest_framework import serializers
from ..models import People,Movie


# 사람 리스트
class PeopleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('id','name','profile_path',)

# 사람 상세 리스트
class PeopleDetailSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('id','title', 'poster_path',)

    filmography = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = People
        fields = '__all__'
    