from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404,get_list_or_404
from .models import Genre, Movie, People, Keyword,Review
from .serializers.genre import GenreSerializer,GenreDetailSerializer
from .serializers.people import PeopleListSerializer, PeopleDetailSerializer
from .serializers.movie import MovieListSerializer, MovieDetailSerializer
from .serializers.keyword import KeywordSerializer, KeywordDetailSerializer
from .serializers.searchmovie import MovieSerializer
from .serializers.review import ReviewListSerializer,ReviewDetailSerializer
from accounts.serializers import ProfileSerializer,ProfileListSerializer
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

def search_movies(query):
    query_terms = query.split()
    filters = Q()

    for term in query_terms:
        term_filter = (
            Q(title__icontains=term) |
            Q(original_title__icontains=term) |
            Q(overview__icontains=term) |
            Q(genres__name__icontains=term) |
            Q(people__name__icontains=term) |
            Q(keyword__name__icontains=term)
        )
        filters &= term_filter

    movies = Movie.objects.filter(filters).distinct()

    def sort_key(movie):
        title_matches = any(term.lower() in movie.title.lower() for term in query_terms)
        keyword_matches = any(term.lower() in [kw.name.lower() for kw in movie.keyword.all()] for term in query_terms)
        overview_matches = any(term.lower() in movie.overview.lower() for term in query_terms)
        genre_matches = any(term.lower() in [genre.name.lower() for genre in movie.genres.all()] for term in query_terms)
        people_matches = any(term.lower() in [person.name.lower() for person in movie.people.all()] for term in query_terms)
        
        return (
            not title_matches,
            not keyword_matches,
            not overview_matches,
            not genre_matches,
            not people_matches,
        )

    sorted_movies = sorted(movies, key=sort_key)
    
    return sorted_movies[:4]

@api_view(['GET'])
def search_movies_view(request):
    query = request.GET.get('q')
    
    if not query:
        return Response({"message": "검색어를 입력해주세요."}, status=400)
    
    movies = search_movies(query)
    
    if not movies:
        return Response({"message": "검색결과가 없습니다."}, status=404)
    
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def review(request):
    reviews = get_list_or_404(Review)
    serializer = ReviewListSerializer(reviews, many=True)
    return Response(serializer.data)



@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def reviewDetail(request,movie_id):
    if request.method == 'GET':
        reviews = Review.objects.filter(movie_id=movie_id)
        serializer = ReviewDetailSerializer(reviews, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        movie = Movie.objects.get(pk=movie_id)
        serializer = ReviewDetailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user,movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileDetail(request,user_id):
    user = get_object_or_404(User, pk=user_id)
    serializer = ProfileSerializer(instance=user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profileList(request):
    users = User.objects.filter(is_superuser=False).filter(is_staff=False)
    serializer = ProfileListSerializer(instance=users, many=True)
    return Response(serializer.data)


# @api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
# def (request, movie_id):
#     movie = get_object_or_404(Movie, pk=movie_id)
    
#     serializer = MovieDetailSerializer(movie)
#     return Response(serializer.data)