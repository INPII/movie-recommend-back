from django.urls import path
from . import views

urlpatterns = [
    path('genre/',views.genre),
    path('actor/',views.actor),
    path('director/',views.director),
    path('movie/',views.movie),
    path('keyword/',views.keyword),
    path('movie/<int:movie_id>/',views.movieDetail),
    path('actor/<int:actor_id>/',views.actorDetail),
    path('genre/<int:genre_id>/',views.genreDetail),
    path('keyword/<int:keyword_id>/',views.keywordDetail),
    path('director/<int:director_id>/',views.directorDetail),
    path('search_movies/',views.search_movies_view),
]