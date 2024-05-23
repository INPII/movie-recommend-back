from django.urls import path
from . import views

urlpatterns = [
    #장르
    path('genre/all/',views.genreAll),
    path('genre/list/<int:start>/',views.genreList),
    path('genre/<int:genre_id>/',views.genreDetail),
    
    #배우
    path('actor/all/',views.actorAll),
    path('actor/list/<int:start>/',views.actorList),
    path('actor/<int:actor_id>/',views.actorDetail),
    
    #감독
    path('director/all/',views.directorAll),
    path('director/list/<int:start>/',views.directorList),
    path('director/<int:director_id>/',views.directorDetail),
    
    #좋아요한 감독/배우
    path('people/like/<int:people_id>/',views.like_people),

    #박스오피스
    path('boxoffice/',views.boxOffice),
    
    #영화
    path('all/',views.movieAll),
    path('list/<int:start>/',views.movieList),
    path('<int:movie_id>/',views.movieDetail),
    path('like/<int:movie_id>/',views.like_movie),
    path('postproduction/',views.PostProductionMovieList),

    #키워드
    path('keyword/all/',views.keywordAll),
    path('keyword/list/<int:start>/',views.keywordList),
    path('keyword/<int:keyword_id>/',views.keywordDetail),

    #검색
    path('search/',views.search_movies_view),


    #리뷰
    path('review/all/',views.reviewAll),
    path('review/list/<int:start>/',views.reviewList),
    path('review/<int:review_id>/',views.reviewDetail),
    path('review/like/<int:review_id>/',views.like_review),
    path('<int:movie_id>/review/',views.review),


    #프로필
    path('profile/', views.profile),
    path('profiles/', views.profileList),
    path('<int:user_id>/profile/', views.profileDetail),

    #팔로우
    path('follow/<int:user_id>/',views.follow),
    path('is_following/<int:user_id>/', views.is_following, name='is_following'),

    #알고리즘 추천
    path('recommend/',views.recommend_movies),
    path('survey/',views.survey_response),
    path('survey/recommend/',views.survey_recommended_movies),
]