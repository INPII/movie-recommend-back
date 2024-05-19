from django.urls import path
from . import views

urlpatterns = [
    path('genre/',views.genre),
    path('actor/',views.actor),
    path('director/',views.director),
    path('movie/',views.movie),
    path('movie/<int:movie_id>/',views.moviedetail),
    path('actor/<int:actor_id>/',views.actordetail),
    path('genre/<int:genre_id>/',views.genredetail),
    path('director/<int:director_id>/',views.directordetail),
]