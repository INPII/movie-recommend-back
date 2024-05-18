from django.urls import path
from . import views

urlpatterns = [
    path('rank/<int:movie_id>',views.rank),
    path('genre/',views.genre),
    path('actor/',views.actor),
    path('director/',views.director),
    path('movie/',views.movie),

]