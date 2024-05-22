from django.contrib import admin
from .models import Review,People,Movie,SurveyResponse


# Register your models here.

admin.site.register(Review)
admin.site.register(People)
admin.site.register(Movie)
admin.site.register(SurveyResponse)
