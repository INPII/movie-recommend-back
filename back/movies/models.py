from django.db import models
from accounts.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=100, null=False)
    gender = models.CharField(max_length=20)
    profile_img = models.TextField(null=True)
    biography = models.TextField(null=True)
    imdb_id = models.CharField(max_length=100, null=True)
    popularity = models.FloatField()

    def __str__(self):
        return self.name
    

class Director(models.Model):
    name = models.CharField(max_length=100, null=False)
    gender = models.CharField(max_length=20)
    profile_img = models.TextField()
    Filmography = models.TextField(null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_at = models.DateField()
    popularity = models.FloatField(null=True)
    overview = models.TextField()
    runtime = models.IntegerField(null=True)
    video_url = models.TextField(null=True)
    total_audience_count = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    original_language = models.CharField(max_length=20)
    production_corp = models.CharField(max_length=100, null=True)
    post_path = models.TextField()
    actors = models.ManyToManyField(Actor, related_name="filmography")



    def __str__(self):
        return self.title


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

# 영화 상세페이지 조회수
class Count(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)

# 박스오피스 랭킹
class Rank(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rank = models.IntegerField()

# 영화 검색을 위한 키워드
class Keyword(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    keyword = models.CharField(max_length = 50)

# 영화 좋아요
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

# 영화 평점
class avgRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    score = models.FloatField()

#영화를 본 사람
class Watch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)


# 영화 리뷰
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

