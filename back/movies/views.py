from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Genre, Movie, People
from .serializers.genre import GenreSerializer,GenreDetailSerializer
from .serializers.people import PeopleListSerializer, PeopleDetailSerializer
from .serializers.movie import MovieListSerializer, MovieDetailSerializer

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
def actordetail(request, actor_id):
    actor = get_object_or_404(People, known_for_department='Acting', pk=actor_id)
    serializer = PeopleDetailSerializer(actor)
    return Response(serializer.data)

@api_view(['GET'])
def directordetail(request, director_id):
    director = get_object_or_404(People, known_for_department='Directing', pk=director_id)
    serializer = PeopleDetailSerializer(director)
    return Response(serializer.data)

@api_view(['GET'])
def movie(request):
    movies = Movie.objects.all().order_by('-popularity')[:10]
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def moviedetail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    
    serializer = MovieDetailSerializer(movie)
    return Response(serializer.data)

@api_view(['GET'])
def genredetail(request, genre_id):
    genre = get_object_or_404(Genre, pk=genre_id)
    serializer = GenreDetailSerializer(genre)
    return Response(serializer.data)