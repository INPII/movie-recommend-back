from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404
from .models import Rank,Genre
from .serializers.rank import RankSerializer
from .serializers.genre import GenreSerializer

def rank(request):
    if request.method == 'GET':
        rankings = Rank.objects.all().order_by('popularity')[:10]
        serializer = RankSerializer(rankings, many=True)
        print(serializer.data)
        return JsonResponse(serializer.data)

def genre(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return JsonResponse(serializer.data)







