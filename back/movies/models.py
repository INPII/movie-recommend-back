from django.db import models
from accounts.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

# from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name
    
class Keyword(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name
    
class People(models.Model):
    adult = models.BooleanField(null=True)
    biography = models.TextField(null=True)
    birthday = models.DateField(null=True)
    deathday = models.DateField(null=True)
    gender = models.CharField(max_length=20)
    imdb_id = models.CharField(max_length=100, null=True)
    known_for_department = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=False)
    place_of_birth = models.TextField(null=True)
    popularity = models.FloatField(null=True)
    profile_path=models.TextField(null=True)

    def __str__(self):
        return self.name
    

class Movie(models.Model):
    adult = models.BooleanField(null=True)
    backdrop_path = models.TextField(null=True)
    budget = models.BigIntegerField(null=True)
    genres = models.ManyToManyField(Genre, related_name='movies')
    imdb_id = models.TextField(null=True)
    origin_country = models.CharField(max_length=100, null=True)
    original_language = models.CharField(max_length=100,null=True)
    original_title = models.CharField(max_length=300,null=True)
    overview = models.TextField(null=True,blank=True)
    popularity = models.FloatField(null=True)
    poster_path = models.TextField(null=True)
    release_date = models.DateField(null=True, default=datetime.date.today)
    revenue = models.BigIntegerField(null=True) 
    runtime = models.IntegerField(null=True)
    status = models.CharField(max_length=100, null=True)
    tagline = models.TextField(null=True)
    title = models.CharField(max_length=300)
    video = models.TextField(null=True)
    vote_average = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    detail_count = models.IntegerField(null=True)
    people = models.ManyToManyField(People, related_name="filmography")
    keyword = models.ManyToManyField(Keyword, related_name="movies",blank=True)


    def __str__(self):
        return self.title


# 영화 상세페이지 조회수
class Count(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)


# 영화 좋아요
class MovieLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

# 사람(배우/감독) 좋아요
class PeopleLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    people = models.ForeignKey(People, on_delete=models.CASCADE)


# 영화 리뷰
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

class ReviewLike():
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UserGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

