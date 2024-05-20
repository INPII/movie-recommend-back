from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Genre, Movie, People, Keyword,Review
from .serializers.genre import GenreSerializer,GenreDetailSerializer
from .serializers.people import PeopleListSerializer, PeopleDetailSerializer
from .serializers.movie import MovieListSerializer, MovieDetailSerializer
from .serializers.keyword import KeywordSerializer, KeywordDetailSerializer
from .serializers.searchmovie import MovieSerializer
from .serializers.review import ReviewListSerializer,ReviewDetailSerializer
from accounts.serializers import CustomUserDetailsSerializer,ProfileSerializer
from accounts.models import User
# from django.contrib.auth import get_user_model

# User = get_user_model()
@api_view(['GET'])
def genre(request):
    genres = Genre.objects.all()
    serializer = GenreSerializer(genres, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def actor(request):
    actors = People.objects.filter(known_for_department='Acting')
    serializer = PeopleListSerializer(actors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def director(request):
    directors = People.objects.filter(known_for_department='Directing')
    serializer = PeopleListSerializer(directors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def actorDetail(request, actor_id):
    actor = get_object_or_404(People, known_for_department='Acting', pk=actor_id)
    serializer = PeopleDetailSerializer(actor)
    return Response(serializer.data)

@api_view(['GET'])
def directorDetail(request, director_id):
    director = get_object_or_404(People, known_for_department='Directing', pk=director_id)
    serializer = PeopleDetailSerializer(director)
    return Response(serializer.data)

@api_view(['GET'])
def keyword(request):
    keywords = Keyword.objects.all()
    serializer = KeywordSerializer(keywords, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def keywordDetail(request, keyword_id):
    keyword = get_object_or_404(Keyword,  pk=keyword_id)
    serializer = KeywordDetailSerializer(keyword)
    return Response(serializer.data)

@api_view(['GET'])
def movie(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def movieDetail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def genreDetail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    serializer = GenreDetailSerializer(genre)
    return Response(serializer.data)

from django.db.models import Q

def search_movies(query, genre_ids=None, keyword_ids=None, sort_by='popularity'):
    query_terms = query.split()
    filters = Q()
    
    for term in query_terms:
        term_filter = Q(title__icontains=term) | Q(original_title__icontains=term) | Q(overview__icontains=term)| Q(genres__name__icontains=term) | Q(people__name__icontains=term) | Q(keyword__name__icontains=term)
        filters &= term_filter
    
    if genre_ids:
        filters &= Q(genres__id__in=genre_ids)
    
    if keyword_ids:
        filters &= Q(keyword__id__in=keyword_ids)
    
    movies = Movie.objects.filter(filters).distinct()

    # Custom sorting: title, keyword, overview, people
    movies = sorted(movies, key=lambda m: (
        not any(query_term.lower() in m.title.lower() for query_term in query_terms),
        not any(query_term.lower() in [kw.name.lower() for kw in m.keyword.all()] for query_term in query_terms),
        not any(query_term.lower() in m.overview.lower() for query_term in query_terms),
        not any(query_term.lower() in [person.name.lower() for person in m.people.all()] for query_term in query_terms),
    ))

    return movies[:4]

@api_view(['GET'])
def search_movies_view(request):
    query = request.GET.get('query')
    genre_ids = request.GET.getlist('genres')
    keyword_ids = request.GET.getlist('keywords')
    sort_by = request.GET.get('sort_by', 'popularity')
    
    movies = search_movies(query, genre_ids, keyword_ids, sort_by)
    
    if not movies:
        return Response({"message": "검색결과가 없습니다."}, status=404)
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def review(request,movie_id):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        serializer = ReviewDetailSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileDetail(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def (request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
    
#     serializer = MovieDetailSerializer(movie)
#     return Response(serializer.data)