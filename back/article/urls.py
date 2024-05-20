from django.urls import path
from . import views


urlpatterns = [
    path('articles/', views.article_list),
    path('articles/<int:article_id>/', views.article_detail),
    path('articles/<int:article_id>/comment/', views.comment),
    path('search/article/', views.search_articles),
]
