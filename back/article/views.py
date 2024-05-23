from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers.article import ArticleListSerializer, ArticleSerializer,ArticleCreateSerializer
from .serializers.comment import CommentListSerializer, CommentSerializer
from .models import Article,Comment

#context, request는 serializer에서 좋아요 is_liked를 동적으로 구현하기 위한것
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def articleAll(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})

    elif request.method == 'POST':
        serializer = ArticleCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def articleList(request, start):
    if request.method == 'GET':
        articles = get_list_or_404(Article)[start:start+10]
        serializer = ArticleListSerializer(articles, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def articleDetail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        if request.user != article.user:
            article.view_count += 1  # 자신이 작성한 게시글이 아닌 경우에만 조회수 증가
            article.save()
        serializer = ArticleSerializer(article, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT':
        if request.user != article.user:
            return Response({"detail": "게시글 작성자만 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ArticleCreateSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        if request.user != article.user:
            return Response({"detail": "게시글 작성자만 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_like(request, article_id):
    user = request.user
    article = get_object_or_404(Article, pk=article_id)
    if article.like_users.filter(pk=user.pk).exists():
        article.like_users.remove(user)
        return Response({'is_liked': False, 'like_count': article.like_count}, status=status.HTTP_201_CREATED)
    else:
        article.like_users.add(user)
        return Response({'is_liked': True, 'like_count': article.like_count}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def comment(request, article_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(article_id=article_id)
        serializer = CommentListSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'POST':
        article = get_object_or_404(Article, pk=article_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
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
