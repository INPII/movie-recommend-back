from rest_framework import serializers
from ..models import Article,Comment
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','nickname','username','profile_path',)

class CommentSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id','content','user','created_at',)


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    like_article = UserSerializer(allow_null=True, many=True,read_only=True)
    like_count = serializers.ReadOnlyField()
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'user','created_at','like_article','like_count',)


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    comments = CommentSerializer(read_only = True, many=True)
    
    class Meta:
        model = Article
        fields = '__all__'

class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','content',)
        
