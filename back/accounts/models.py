from django.db import models
from django.contrib.auth.models import AbstractUser
from allauth.account.adapter import DefaultAccountAdapter
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=100,blank=True)
    gender = models.CharField(max_length=100, blank=True,null=True)
    age = models.IntegerField(blank=True, null=True)
    mbti = models.CharField(max_length=4, blank=True, null=True)
    profile_path=models.TextField(null=True)

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        from allauth.account.utils import user_email, user_field, user_username

        data=form.cleaned_data
        first_name=data.get("first_name")
        last_name= data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        nickname = data.get("nickname")
        gender = data.get("gender")
        age = data.get("age")
        mbti = data.get("mbti")

        user_email(user,email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name",last_name)
        if nickname:
            user_field(user, "nickname", nickname)
        if gender:
            user_field(user, "gender", gender)
        if age:
            user_field(user, "age", age)
        if mbti:
            user_field(user, "mbti", mbti)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            user.save()
        return user
        