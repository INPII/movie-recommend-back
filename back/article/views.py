from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers.article import ArticleListSerializer, ArticleSerializer
from .serializers.comment import CommentListSerializer, CommentSerializer
from .models import Article,Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def comment(request,article_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=article_id)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        article = Article.objects.get(pk=article_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_articles(request):
    query = request.GET.get('q', '')

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(user__nickname__icontains=query))
    else:
        return Response({"message": "검색어를 입력해주세요."})

    if articles.exists():
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "검색결과가 없습니다."})
