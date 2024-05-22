from rest_framework import serializers
from ..models import Review,Movie
from accounts.models import User
# from accounts.serializers import 


# 영화를 참조하기위해 들고온 시리얼라이저
class MovieSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    class Meta:
        model = Movie
        fields = ('id', 'title', 'poster_path')

    def get_title(self, obj):
        return obj.name_kr if obj.name_kr else obj.title

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'profile_path','nickname',)

# 리뷰 리스트
class ReviewListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)  
    user = UserSerializer(read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'content', 'create_at', 'updated_at', 'rating', 'user', 'movie', 'like_count', 'is_liked')

    def get_like_count(self, obj):
        return obj.like_user.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None or not hasattr(request, 'user'):
            return False
        user = request.user
        return obj.like_user.filter(id=user.id).exists() if user.is_authenticated else False

class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer(read_only=True)
    like_review = UserSerializer(allow_null=True, many=True, read_only=True)
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('id', 'content', 'create_at', 'updated_at', 'rating', 'user', 'movie', 'like_review', 'like_count', 'is_liked')

    def get_like_count(self, obj):
        return obj.like_user.count()

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request is None or not hasattr(request, 'user'):
            return False
        user = request.user
        return obj.like_user.filter(id=user.id).exists() if user.is_authenticated else False

    

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('content', 'rating')
        

# # 사람 상세 리스트
# class PeopleDetailSerializer(serializers.ModelSerializer):
#     class MovieSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Movie
#             fields = ('id','title', 'poster_path','release_date','origin_country',)

#     filmography = MovieSerializer(many=True, read_only=True)

#     class Meta:
#         model = People
#         fields = '__all__'