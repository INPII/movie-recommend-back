from django.db import models
from accounts.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator

# from django.contrib.auth.models import User

class Keyword(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

# class Genre(models.Model):
#     name = models.CharField(max_length=100, null=False)

#     def __str__(self):
#         return self.name
    
    
# class People(models.Model):
#     adult = models.BooleanField(null=True)
#     biography = models.TextField(null=True)
#     birthday = models.DateField(null=True)
#     deathday = models.DateField(null=True)
#     gender = models.CharField(max_length=20)
#     imdb_id = models.CharField(max_length=100, null=True)
#     known_for_department = models.CharField(max_length=100, null=True)
#     name = models.CharField(max_length=100, null=False)
#     place_of_birth = models.TextField(null=True)
#     popularity = models.FloatField(null=True)
#     profile_path=models.TextField(null=True)
#     like_user = models.ManyToManyField(User, blank=True,related_name="like_people")

#     def __str__(self):
#         return self.name


# class Movie(models.Model):
#     adult = models.BooleanField(null=True)
#     backdrop_path = models.TextField(null=True)
#     budget = models.BigIntegerField(null=True)
#     genres = models.ManyToManyField(Genre, related_name='movies')
#     imdb_id = models.TextField(null=True)
#     origin_country = models.CharField(max_length=100, null=True)
#     original_language = models.CharField(max_length=100,null=True)
#     original_title = models.CharField(max_length=300,null=True)
#     overview = models.TextField(null=True,blank=True)
#     popularity = models.FloatField(null=True)
#     poster_path = models.TextField(null=True)
#     release_date = models.DateField(null=True, default=datetime.date.today)
#     revenue = models.BigIntegerField(null=True) 
#     runtime = models.IntegerField(null=True)
#     status = models.CharField(max_length=100, null=True)
#     tagline = models.TextField(null=True)
#     title = models.CharField(max_length=300)
#     video = models.TextField(null=True)
#     vote_average = models.FloatField(null=True)
#     vote_count = models.IntegerField(null=True)
#     detail_count = models.IntegerField(null=True)
#     people = models.ManyToManyField(People, related_name="filmography")
#     keyword = models.ManyToManyField(Keyword, related_name="movies",blank=True)
#     like_user = models.ManyToManyField(User, related_name="like_movie",blank=True)

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
    profile_path = models.TextField(null=True)
    like_user = models.ManyToManyField(User, blank=True, related_name="liked_people")

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, null=False)
    name_kr = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    adult = models.BooleanField(null=True)
    backdrop_path = models.TextField(null=True)
    budget = models.BigIntegerField(null=True)
    genres = models.ManyToManyField(Genre, related_name='genre_movies')
    imdb_id = models.TextField(null=True)
    origin_country = models.CharField(max_length=100, null=True)
    original_language = models.CharField(max_length=100, null=True)
    original_title = models.CharField(max_length=300, null=True)
    overview = models.TextField(null=True, blank=True)
    popularity = models.FloatField(null=True)
    poster_path = models.TextField(null=True, blank = True)
    release_date = models.DateField(null=True, default=datetime.date.today)
    revenue = models.BigIntegerField(null=True, blank = True)
    runtime = models.IntegerField(null=True, blank = True)
    status = models.CharField(max_length=100, null=True)
    tagline = models.TextField(null=True, blank = True)
    title = models.CharField(max_length=300)
    video = models.TextField(null=True, blank = True)
    vote_average = models.FloatField(null=True, blank = True)
    vote_count = models.IntegerField(null=True, blank = True)
    detail_count = models.IntegerField(null=True, blank = True)
    people = models.ManyToManyField(People, related_name="filmography")
    keywords = models.ManyToManyField('Keyword', related_name="keyword_movies", blank=True)
    like_user = models.ManyToManyField(User, related_name="liked_movies", blank=True)
    name_kr = models.CharField(max_length=300, null=True, blank=True)
    overview_kr = models.TextField(null=True, blank=True)

    # 평점을 계속 업데이트

    def update_vote_average(self, new_rating=None, delete_rating=None):
        if new_rating is not None:
            total_rating = self.vote_average * self.vote_count + new_rating
            self.vote_count += 1
            self.vote_average = round(total_rating / self.vote_count, 2)
        elif delete_rating is not None:
            if self.vote_count > 1:
                total_rating = self.vote_average * self.vote_count - delete_rating
                self.vote_count -= 1
                self.vote_average = round(total_rating / self.vote_count, 2)
            else:
                self.vote_count = 0
                self.vote_average = 0
        self.save()

    def __str__(self):
        return self.title

    


# 영화 상세페이지 조회수
class Count(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    count = models.IntegerField(null=True)


# 영화 리뷰
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="user_reviews")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    like_user = models.ManyToManyField(User, related_name="liked_reviews", blank=True)

    def __str__(self):
        return self.content
    
    # 리뷰 작성과 삭제 시 vote_average, vote_count에 영향을 줌
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_rating = None
        if not is_new:
            old_review = Review.objects.get(pk=self.pk)
            old_rating = old_review.rating
        super().save(*args, **kwargs)
        if is_new:
            self.movie.update_vote_average(new_rating=self.rating)
        else:
            self.movie.update_vote_average(delete_rating=old_rating)
            self.movie.update_vote_average(new_rating=self.rating)
    
    def delete(self, *args, **kwargs):
        movie = self.movie
        super().delete(*args, **kwargs)
        movie.update_vote_average(delete_rating=self.rating)
# 유저의 장르
class UserGenre(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)


class SurveyResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_1 = models.CharField(max_length=1, choices=[
        ('a', '동물'), ('b', '기계'), ('c', '하트'), ('d', '총'), 
        ('e', '용'), ('f', '우주'), ('g', '코미디'), ('h', '공포'), 
        ('i', '스포츠'), ('j', '음악'), ('k', '애니메이션'), ('l', '자연재해(화산)')
    ])
    question_2 = models.CharField(max_length=1, choices=[
        ('a', '재난'), ('b', '외계인'), ('c', '중세 권력 싸움'), 
        ('d', '탐정'), ('e', '가족 드라마'), ('f', '권력싸움'), 
        ('g', '귀여움'), ('h', '즐거움'), ('i', '상상력'), ('j', '스릴')
    ])
    question_3 = models.CharField(max_length=1, choices=[
        ('a', '지적 악당'), ('b', '용감한 주인공'), ('c', '냉소적 조력자'), 
        ('d', '평범한 사람'), ('e', '모험에 휘말리는 사람')
    ])
    question_4 = models.CharField(max_length=1, choices=[
        ('a', '60분'), ('b', '90분'), ('c', '120분'), ('d', '그 이상')
    ])
    question_5 = models.CharField(max_length=1, choices=[
        ('a', '긴장감'), ('b', '감동'), ('c', '웃음'), 
        ('d', '영감'), ('e', '편안함')
    ])
    question_6 = models.CharField(max_length=1, choices=[
        ('a', '1~2.9'), ('b', '3~4.9'), ('c', '5~6.9'), ('d', '8~10')
    ])