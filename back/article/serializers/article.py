from rest_framework import serializers
from ..models import Article,Comment
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'username', 'profile_path',)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created_at',)

class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    like_article = UserSerializer(allow_null=True, many=True, read_only=True, source='like_users')
    like_count = serializers.ReadOnlyField()   
    
    #동적필드를 추가할때 유용한 도구 SerializerMethodField, 이걸 쓰지않으면 직접 메서드를 오버라이드하여서 추가해야한다.
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'user', 'created_at', 'like_article', 'like_count', 'is_liked',)

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and not request.user.is_anonymous:
            return obj.like_users.filter(id=request.user.id).exists()
        return False
    
    # 직접 오버라이드 해서 추가하는 방법
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     request = self.context.get('request', None)
    #     if request and not request.user.is_anonymous:
    #         representation['is_liked'] = instance.like_users.filter(id=request.user.id).exists()
    #     else:
    #         representation['is_liked'] = False
    #     return representation

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'

    def get_is_liked(self, obj):
        request = self.context.get('request', None)
        if request and not request.user.is_anonymous:
            return obj.like_users.filter(id=request.user.id).exists()
        return False

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','content',)
        
