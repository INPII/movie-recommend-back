from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Rank,Genre,Actor,Director,Movie
from .serializers.rank import RankSerializer
from .serializers.genre import GenreSerializer
from .serializers.actor import ActorSerializer
from .serializers.director import DirectorSerializer
from .serializers.movie import MovieSerializer

def rank(request, movie_id):
    if Movie.objects.filter(pk=movie_id).exists():
        movie = Movie.objects.get(pk=movie_id)
        movie_serializer = MovieSerializer(movie)
        
        if Rank.objects.filter(movie=movie).exists():
            rank = Rank.objects.get(movie=movie)
            response_data = {
                'movie': movie_serializer.data,
                'rank': rank.rank
            }
        else:
            response_data = {
                'movie': movie_serializer.data,
                'rank': None
            }
        
        return JsonResponse(response_data, safe=False)
    else:
        return JsonResponse({'error': 'Movie not found'}, status=404)

def genre(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def actor(request):
    if request.method == 'GET':
        actors = Actor.objects.all()
        serializer = ActorSerializer(actors, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def director(request):
    if request.method == 'GET':
        directors = Director.objects.all()
        serializer = DirectorSerializer(directors, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def movie(request):
    if request.method == 'GET':
        movies = Movie.objects.all().order_by('-popularity')[:10]
        serializer = MovieSerializer(movies, many=True)
        return JsonResponse(serializer.data, safe=False)







