from .models import Movie,Review,SurveyResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_movies(user):
    # 사용자가 좋아요를 누른 영화와 리뷰에서 높은 평점을 준 영화 가져오기
    liked_movies = user.like_movie.all()
    reviewed_movies = Review.objects.filter(user=user).order_by('-rating')

    # 비교 대상 영화 목록
    all_movies = Movie.objects.all()

    # 사용자의 좋아요와 리뷰에서 높은 평점을 받은 영화의 overview를 추출
    liked_overviews = [movie.overview for movie in liked_movies if movie.overview]
    liked_overviews += [review.movie.overview for review in reviewed_movies if review.movie.overview]

    # 비교 대상 영화의 overview 추출
    movie_overviews = [movie.overview for movie in all_movies if movie.overview]

    # TF-IDF 벡터화
    # 텍스트 데이터를 수치 데이터로 변환하기 위해 쓴다
    # TF : 특정 문서에서 특정 단어가 등장하는 빈도
    # IDF : 득정 단어가 전체 문서 집합에서 얼마나 흔한지를 나타낸다(흔한 단어일수록 값이 낮고, 드문단어일수록 값이 높음 즉 흔한단어일수록 적용이 되어도 영향이 크지않다는 뜻)
    # stop_words 는 영어 불용어를 제거하도록 지정하는것(불용어란 is,the,in 등 분석에 크게 의미없는 단어들을 뜻함)
    vectorizer = TfidfVectorizer(stop_words='english')

    # fit_transform은 TF,와 IDF를 계산하고 텍스트 데이터를 수치화된 벡터로 변환하여 결과를 반환한다.
    # 벡터로 변환하는 이유 
    # 1. 컴퓨터가 텍스트를 이해 하지 못하기 때문
    # 2. 텍스트간의 코사인 유사도를 계산하기 위해선 벡터가 필요하기 때문 
    movie_matrix = vectorizer.fit_transform(movie_overviews)

    # 유사도 계산
    # target_overviews 리스트는 사용자가 좋아요를 누른 영화와 리뷰에서 높은 평점을 준 영화의 overview 텍스트로 구성이되어있다.
    # target_overviews 리스트에 있는 텍스트 데이터를 tf-idf 벡터로 변환한다.
    liked_matrix = vectorizer.transform(liked_overviews)

    # cosine_similarity 는 두 인자간의 유사도를 계산하여 유사도 행렬을 생성한다.
    cosine_sim = cosine_similarity(liked_matrix, movie_matrix)

    # 유사도 점수를 기반으로 추천 영화 선정
    # 행렬 연산에서의 축은 즉 axis = 0 은 행을 따라서 연산을 수행한다(각 열별로 연산), axis=1은 열을 따라 연산을 수행(각 행 별로 연산을 수행)
    # 즉 여기서는 영화의 행을 따라서 유사도의 평균값을 계산하여 배열을 저장한다는 뜻이다.
    # 예를 들면 similar_movies[A]는 영화 A와 사용자가 좋아요를 누르거나 리뷰(높은 평점)를 쓴 영화 간의 평균 유사도를 나타낸다.
    similar_movies = cosine_sim.mean(axis=0)

    # similar_movies 배열 값을 내림차순으로 정렬한 인덱스를 반환한다. argsort가 오름차순인데 -1로 정렬
    # 즉, 가장 유사도가 높은 영화부터 낮은 영화까지 인덱스를 포함한 배열을 생성한다.
    similar_movies_index = similar_movies.argsort()[::-1]


    # 배열을 순회하면서 idx를 가지고 이미 리뷰를 작성하거나 좋아요를 누른 영화와 중복되는지 검사를 해보고 영화를 10개 추천해준다.
    recommended_movies = []
    for idx in similar_movies_index:
        recommended_movie = all_movies[int(idx)]
        if recommended_movie not in liked_movies and recommended_movie not in reviewed_movies:
            recommended_movies.append(recommended_movie)
            if len(recommended_movies) >= 10:  # 최대 10개 추천
                break

    return recommended_movies


# def get_genre_vector(genres, all_genres):
#     genre_vector = np.zeros(len(all_genres))
#     for genre in genres:
#         genre_vector[all_genres.index(genre)] = 1
#     return genre_vector

# def get_keyword_vector(keywords, all_keywords):
#     keyword_vector = np.zeros(len(all_keywords))
#     for keyword in keywords:
#         keyword_vector[all_keywords.index(keyword)] = 1
#     return keyword_vector

# def get_similar_movies(user):
#     # 사용자가 좋아요를 누른 영화와 리뷰에서 높은 평점을 준 영화 가져오기
#     liked_movies = user.like_movie.all()
#     reviewed_movies = Review.objects.filter(user=user).order_by('-rating')
#     liked_people = user.like_people.all()

#     # 비교 대상 영화 목록
#     all_movies = Movie.objects.all()
#     all_genres = list(Genre.objects.all())
#     all_keywords = list(Keyword.objects.all())

#     # 사용자가 좋아요를 누른 영화의 overview, 장르, 키워드 및 배우/감독을 추출
#     target_overviews = [movie.overview for movie in liked_movies if movie.overview]
#     target_genres = [genre for movie in liked_movies for genre in movie.genres.all()]
#     target_keywords = [keyword for movie in liked_movies for keyword in movie.keyword.all()]
#     target_people = liked_people

#     # 사용자가 리뷰를 쓴 영화의 장르 추출
#     for review in reviewed_movies:
#         target_overviews.append(review.movie.overview)
#         target_genres.extend(review.movie.genres.all())
#         target_keywords.extend(review.movie.keyword.all())

#     # 비교 대상 영화의 overview, 장르, 키워드 및 배우/감독 추출
#     movie_overviews = [movie.overview for movie in all_movies if movie.overview]
#     genre_vectors = np.array([get_genre_vector(movie.genres.all(), all_genres) for movie in all_movies])
#     keyword_vectors = np.array([get_keyword_vector(movie.keyword.all(), all_keywords) for movie in all_movies])
#     people_vectors = np.array([1 if any(people in movie.people.all() for people in target_people) else 0 for movie in all_movies])

#     # TF-IDF 벡터화
#     tfidf_vectorizer = TfidfVectorizer(stop_words='english')
#     tfidf_matrix = tfidf_vectorizer.fit_transform(movie_overviews)

#     # 유사도 계산
#     if target_overviews:
#         target_tfidf_matrix = tfidf_vectorizer.transform(target_overviews)
#         cosine_sim = cosine_similarity(target_tfidf_matrix, tfidf_matrix)
#         overview_sim = cosine_sim.mean(axis=0)
#     else:
#         overview_sim = np.zeros(len(all_movies))

#     # 장르 및 키워드 유사도 계산
#     if target_genres:
#         target_genre_vector = get_genre_vector(target_genres, all_genres)
#         genre_sim = cosine_similarity([target_genre_vector], genre_vectors).flatten()
#     else:
#         genre_sim = np.zeros(len(all_movies))

#     if target_keywords:
#         target_keyword_vector = get_keyword_vector(target_keywords, all_keywords)
#         keyword_sim = cosine_similarity([target_keyword_vector], keyword_vectors).flatten()
#     else:
#         keyword_sim = np.zeros(len(all_movies))

#     # 종합 유사도 계산 (가중 평균)
#     overview_weight = 0.5
#     keyword_weight = 0.2
#     genre_weight = 0.2
#     people_weight = 0.1

#     combined_sim = (overview_weight * overview_sim +
#                     keyword_weight * keyword_sim +
#                     genre_weight * genre_sim +
#                     people_weight * people_vectors)

#     # 유사도 점수를 기반으로 추천 영화 선정
#     similar_movies_indices = combined_sim.argsort()[::-1]

#     recommended_movies = []
#     for idx in similar_movies_indices:
#         recommended_movie = all_movies[idx]
#         if recommended_movie not in liked_movies and recommended_movie not in reviewed_movies:
#             recommended_movies.append(recommended_movie)
#             if len(recommended_movies) >= 10:  # 최대 10개 추천
#                 break

#     return recommended_movies

import numpy as np

def get_similar_movies_survey(user):
    survey_response = SurveyResponse.objects.filter(user=user).first()

    if not survey_response:
        return Movie.objects.none()

    question_1_keywords = {
        'a': ['animals', 'wildlife', 'pets', 'nature', 'zoo'],
        'b': ['machines', 'technology', 'robots', 'gadgets', 'mechanics'],
        'c': ['heart', 'love', 'romance', 'passion', 'emotion'],
        'd': ['guns', 'weapons', 'action', 'violence', 'combat'],
        'e': ['dragons', 'fantasy', 'myth', 'legend', 'adventure'],
        'f': ['space', 'universe', 'astronomy', 'sci-fi', 'exploration'],
        'g': ['comedy', 'humor', 'funny', 'laughter', 'sitcom'],
        'h': ['horror', 'fear', 'scary', 'thriller', 'terror'],
        'i': ['sports', 'competition', 'athletics', 'games', 'fitness'],
        'j': ['music', 'concert', 'band', 'singing', 'melody'],
        'k': ['animation', 'cartoon', 'anime', 'drawings', 'fantasy'],
        'l': ['disaster', 'volcano', 'earthquake', 'calamity', 'crisis']
    }
    question_2_keywords = {
        'a': ['disaster', 'small town', 'survival', 'emergency', 'chaos'],
        'b': ['aliens', 'first contact', 'extraterrestrial', 'invasion', 'sci-fi'],
        'c': ['medieval', 'power struggle', 'kingdom', 'war', 'dynasty'],
        'd': ['detective', 'investigation', 'mystery', 'crime', 'thriller'],
        'e': ['family', 'drama', 'relationships', 'love', 'emotions']
    }
    question_3_keywords = {
        'a': ['intelligent villain', 'complex plans', 'mastermind', 'antagonist', 'schemer'],
        'b': ['brave hero', 'courage', 'protagonist', 'adventure', 'fearless'],
        'c': ['cynical sidekick', 'insightful', 'wise', 'mentor', 'support'],
        'd': ['ordinary person', 'conflict resolution', 'realistic', 'relatable', 'everyman'],
        'e': ['adventurous', 'accidental hero', 'unexpected', 'journey', 'growth']
    }
    question_5_keywords = {
        'a': ['tension', 'thrill', 'excitement', 'suspense', 'adrenaline'],
        'b': ['emotion', 'tear-jerker', 'heartfelt', 'moving', 'sentimental'],
        'c': ['laughter', 'humor', 'comedy', 'fun', 'joy'],
        'd': ['inspiration', 'thought-provoking', 'motivational', 'uplifting', 'enlightening'],
        'e': ['relaxation', 'comfort', 'calm', 'peaceful', 'soothing']
    }

    preferred_keywords = []
    preferred_keywords.extend(question_1_keywords[survey_response.question_1])
    preferred_keywords.extend(question_2_keywords[survey_response.question_2])
    preferred_keywords.extend(question_3_keywords[survey_response.question_3])
    preferred_keywords.extend(question_5_keywords[survey_response.question_5])
    preferred_keywords = " ".join(preferred_keywords)

    preferred_runtime = survey_response.question_4
    preferred_rating = survey_response.question_6

    filtered_movies = Movie.objects.all()
    
    if preferred_runtime == 'a':
        filtered_movies = filtered_movies.filter(runtime__lte=60)
    elif preferred_runtime == 'b':
        filtered_movies = filtered_movies.filter(runtime__lte=90)
    elif preferred_runtime == 'c':
        filtered_movies = filtered_movies.filter(runtime__lte=120)
    elif preferred_runtime == 'd':
        filtered_movies = filtered_movies.filter(runtime__gt=120)

    if preferred_rating == 'a':
        filtered_movies = filtered_movies.filter(vote_average__gte=1, vote_average__lte=2.9)
    elif preferred_rating == 'b':
        filtered_movies = filtered_movies.filter(vote_average__gte=3, vote_average__lte=4.9)
    elif preferred_rating == 'c':
        filtered_movies = filtered_movies.filter(vote_average__gte=5, vote_average__lte=6.9)
    elif preferred_rating == 'd':
        filtered_movies = filtered_movies.filter(vote_average__gte=8, vote_average__lte=10)

    overviews = [movie.overview for movie in filtered_movies if movie.overview]
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(overviews)

    target_matrix = vectorizer.transform([preferred_keywords])
    cosine_sim = cosine_similarity(target_matrix, matrix)
    similar_movies = cosine_sim.flatten()
    similar_movies_indices = similar_movies.argsort()[::-1]

    survey_recommended_movies = []
    for idx in similar_movies_indices:
        recommended_movie = filtered_movies[idx]
        if len(survey_recommended_movies) >= 10:
            break
        survey_recommended_movies.append(recommended_movie)

    return survey_recommended_movies