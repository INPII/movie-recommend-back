from rest_framework import serializers
from ..models import Rank
from .movie import MovieSerializer


# 박스오피스 순위


class RankSerializer(serializers.ModelSerializer):
  

    

    class Meta:
        model = Rank
        fields = ['rank','movie']
    
    
