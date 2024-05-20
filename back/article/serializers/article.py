from rest_framework import serializers
from ..models import Article,Comment
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','nickname','username','profile_path',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','comment','user',)


class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'user','created_at',)


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only = True)
    comments = CommentSerializer(read_only = True, many=True)
    class Meta:
        model = Article
        fields = '__all__'
        
