from django.urls import path
from . import views


urlpatterns = [
    path('', views.articleAll),
    path('like/<int:article_id>/',views.article_like),
    path('<int:article_id>/', views.articleDetail),
    path('comment/<int:article_id>/', views.comment),
    path('search/', views.search_articles),
]
