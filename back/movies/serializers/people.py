from rest_framework import serializers
from ..models import People,Movie


# # 사람 리스트
# class PeopleListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = People
#         fields = ('id','name','profile_path',)

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
        return None

# 사람 상세 리스트
class PeopleDetailSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()

    class MovieSerializer(serializers.ModelSerializer):
        title = serializers.SerializerMethodField()
        class Meta:
            model = Movie
            fields = ('id', 'title', 'poster_path', 'release_date', 'origin_country')
        
        def get_title(self, obj):
            return obj.name_kr if obj.name_kr else obj.title
        
    
    filmography = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = People
        fields = '__all__'

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.like_user.filter(id=request.user.id).exists()
        return None
    
    