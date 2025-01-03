from rest_framework import serializers
from ..models import Review,Movie,Genre,People,UserGenre
from accounts.models import User
from django.db.models import Count
# from accounts.serializers import 
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path', 'genres',)

    def get_title(self, obj):
        return obj.name_kr if obj.name_kr else obj.title

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ('id', 'name', 'profile_path',)

class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta: 
        model = Review
        fields = '__all__'

class UserGenreSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = UserGenre
        fields = ('id','genre',)

class ProfileSerializer(serializers.ModelSerializer):
    user_reviews = ReviewSerializer(read_only=True, many=True)
    liked_movies = MovieSerializer(read_only=True, many=True)
    favorite_genres = UserGenreSerializer(source='usergenre_set', read_only=True, many=True)
    liked_people = PeopleSerializer(read_only=True, many=True)
    is_following = serializers.SerializerMethodField()
    most_liked_genres = serializers.SerializerMethodField()
    profile_view_count = serializers.IntegerField(read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)
    following_count = serializers.IntegerField(source='following.count', read_only=True)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions', 'is_superuser', 'is_staff', 'is_active',)

    def get_is_following(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False

    def get_most_liked_genres(self, obj):
        liked_movies = obj.liked_movies.all()
        genre_counts = Genre.objects.filter(genre_movies__in=liked_movies).annotate(
            like_count=Count('genre_movies__like_user')
        ).order_by('-like_count')
        most_liked_genres = genre_counts[:3]  # 상위 3개의 장르
        return GenreSerializer(most_liked_genres, many=True).data

class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','nickname','profile_path',)


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'nickname', 'profile_path', 'first_name', 'last_name', 'age', 'mbti', 'gender', 'email',)
        read_only_fields = ('username', 'email')

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field not in self.Meta.read_only_fields:
                setattr(instance, field, value)
        instance.save()
        return instance


