from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from .models import User
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_account_settings
from allauth.utils import get_username_max_length
from allauth.socialaccount.models import SocialAccount, EmailAddress
from movies.models import Review,Movie,People,Genre,MovieLike,PeopleLike,UserGenre

UserModel = get_user_model()

    
class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FILED'):
            extra_fields.append(UserModel.USERNAME_FILED)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append(UserModel.first_name)
        if hasattr(UserModel, 'last_name'):
            extra_fields.append(UserModel.last_name)
        if hasattr(UserModel, 'nickname'):
            extra_fields.append(UserModel.nickname)
        if hasattr(UserModel, 'gender'):
            extra_fields.append(UserModel.gender)
        if hasattr(UserModel, 'age'):
            extra_fields.append(UserModel.age)
        if hasattr(UserModel, 'mbti'):
            extra_fields.append(UserModel.mbti)
        model = UserModel
        fields = ('pk',*extra_fields)
        read_only_fields = ('email',)


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        max_length=get_username_max_length(),
        min_length=allauth_account_settings.USERNAME_MIN_LENGTH,
        required=allauth_account_settings.USERNAME_REQUIRED,
    )
    email = serializers.EmailField(required=allauth_account_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    nickname = serializers.CharField(
        required = False,
        allow_blank=True,
        max_length=100
    )
    gender = serializers.CharField(
        required = False,
        allow_blank=True,
        max_length=100
    )
    age = serializers.CharField(
        required = False,
        allow_blank=True,
        max_length=100
    )
    mbti = serializers.CharField(
        required = False,
        allow_blank=True,
        max_length=4
    )


    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_account_settings.UNIQUE_EMAIL:
            if email and EmailAddress.objects.is_verified(email):
                raise serializers.ValidationError(
                    ('A user is already registered with this e-mail address.'),
                )
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'nickname': self.validated_data.get('nickname', ''),
            'gender': self.validated_data.get('gender', ''),
            'age': self.validated_data.get('age', ''),
            'mbti': self.validated_data.get('mbti', ''),
        }
    

# UserDetailsSerializer
# class ProfileSerializer(serializers.ModelSerializer):
     
#     class ReviewSerializer(serializers.ModelSerializer):
        
#         class MovieReviewSerializer(serializers.ModelSerializer):
#             class Meta:
#                 model = Movie
#                 fields =('title', 'overview', 'people', 'genres')
            
#             class GenreSerializer(serializers.ModelSerializer):
#                 class Meta:
#                     model = Genre
#                     fields = '__all__'
                    
            
            
#         movie = MovieReviewSerializer(read_only = True)

#         class Meta: 
#             model = Review
#             fields = '__all__'

#     review_set = ReviewSerializer(read_only = True, many=True)

#     class Meta:
#         model = User
#         exclude = ('password','groups','user_permissions',)
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(read_only=True, many=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'poster_path', 'overview', 'genres']

class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id', 'name', 'profile_path']

class ReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta: 
        model = Review
        fields = '__all__'

class LikeMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = MovieLike
        fields = ['movie']

class LikePeopleSerializer(serializers.ModelSerializer):
    people = PeopleSerializer(read_only=True)

    class Meta:
        model = PeopleLike
        fields = ['people']

class UserGenreSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)

    class Meta:
        model = UserGenre
        fields = ['genre']

class ProfileSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(read_only=True, many=True)
    movie_likes = LikeMovieSerializer(source='movielike_set', read_only=True, many=True)
    people_likes = LikePeopleSerializer(source='peoplelike_set', read_only=True, many=True)
    favorite_genres = UserGenreSerializer(source='usergenre_set', read_only=True, many=True)

    class Meta:
        model = User
        exclude = ('password', 'groups', 'user_permissions','is_superuser', 'is_staff','is_active',)



class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','nickname','profile_path',)