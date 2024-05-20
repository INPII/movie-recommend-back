from django.contrib import admin
from .models import MovieLike, Review


# Register your models here.
admin.site.register(MovieLike)
admin.site.register(Review)