from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Movie, Rank

User = get_user_model()

# 박스오피스 순위
class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'
    
