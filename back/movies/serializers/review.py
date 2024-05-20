from rest_framework import serializers
from ..models import Review
# from accounts.serializers import 

# 리뷰 리스트
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# 리뷰 상세 리스트
class ReviewDetailSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    movie = serializers.ReadOnlyField(source='movie.id')

    class Meta:
        model = Review
        fields = '__all__'
        

# # 사람 상세 리스트
# class PeopleDetailSerializer(serializers.ModelSerializer):
#     class MovieSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Movie
#             fields = ('id','title', 'poster_path','release_date','origin_country',)

#     filmography = MovieSerializer(many=True, read_only=True)

#     class Meta:
#         model = People
#         fields = '__all__'