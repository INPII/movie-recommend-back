from .models import Movie,Review,SurveyResponse,Genre,Keyword
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


import numpy as np

def get_genre_vector(genres, all_genres):
    genre_vector = np.zeros(len(all_genres))
    genre_indices = {genre.id: idx for idx, genre in enumerate(all_genres)}
    for genre in genres:
        genre_vector[genre_indices[genre.id]] = 1
    return genre_vector

def get_keyword_vector(keywords, all_keywords):
    keyword_vector = np.zeros(len(all_keywords))
    keyword_indices = {keyword.id: idx for idx, keyword in enumerate(all_keywords)}
    for keyword in keywords:
        keyword_vector[keyword_indices[keyword.id]] = 1
    return keyword_vector

def get_similar_movies(user):
    # 사용자가 좋아요를 누른 영화와 리뷰에서 높은 평점을 준 영화 가져오기
    liked_movies = user.liked_movies.all().prefetch_related('genres', 'keywords', 'people')
    reviewed_movies = Review.objects.filter(user=user).select_related('movie').prefetch_related('movie__genres', 'movie__keywords')
    liked_people = user.liked_people.all()

    # 비교 대상 영화 목록
    all_movies = Movie.objects.all().prefetch_related('genres', 'keywords', 'people')
    all_genres = list(Genre.objects.all())
    all_keywords = list(Keyword.objects.all())

    # 인덱스 매핑
    genre_indices = {genre.id: idx for idx, genre in enumerate(all_genres)}
    keyword_indices = {keyword.id: idx for idx, keyword in enumerate(all_keywords)}

    # 사용자가 좋아요를 누른 영화의 overview, 장르, 키워드 및 배우/감독을 추출
    target_overviews = [movie.overview for movie in liked_movies if movie.overview]
    target_genres = [genre for movie in liked_movies for genre in movie.genres.all()]
    target_keywords = [keyword for movie in liked_movies for keyword in movie.keywords.all()]
    target_people = liked_people

    # 사용자가 리뷰를 쓴 영화의 장르 추출
    for review in reviewed_movies:
        if review.movie.overview:
            target_overviews.append(review.movie.overview)
        target_genres.extend(review.movie.genres.all())
        target_keywords.extend(review.movie.keywords.all())

    # 비교 대상 영화의 overview, 장르, 키워드 및 배우/감독 추출
    movie_overviews = [movie.overview for movie in all_movies if movie.overview]
    genre_vectors = np.array([get_genre_vector(movie.genres.all(), all_genres) for movie in all_movies])
    keyword_vectors = np.array([get_keyword_vector(movie.keywords.all(), all_keywords) for movie in all_movies])
    people_vectors = np.array([1 if any(people in movie.people.all() for people in target_people) else 0 for movie in all_movies])

    # TF-IDF 벡터화
#     # 텍스트 데이터를 수치 데이터로 변환하기 위해 쓴다
#     # TF : 특정 문서에서 특정 단어가 등장하는 빈도
#     # IDF : 득정 단어가 전체 문서 집합에서 얼마나 흔한지를 나타낸다(흔한 단어일수록 값이 낮고, 드문단어일수록 값이 높음 즉 흔한단어일수록 적용이 되어도 영향이 크지않다는 뜻)
#     # stop_words 는 영어 불용어를 제거하도록 지정하는것(불용어란 is,the,in 등 분석에 크게 의미없는 단어들을 뜻함)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')


    # fit_transform은 TF,와 IDF를 계산하고 텍스트 데이터를 수치화된 벡터로 변환하여 결과를 반환한다.
    # 벡터로 변환하는 이유 
    # 1. 컴퓨터가 텍스트를 이해 하지 못하기 때문
    # 2. 텍스트간의 코사인 유사도를 계산하기 위해선 벡터가 필요하기 때문
    tfidf_matrix = tfidf_vectorizer.fit_transform(movie_overviews)

    # 유사도 점수를 기반으로 추천 영화 선정
    # 행렬 연산에서의 축은 즉 axis = 0 은 행을 따라서 연산을 수행한다(각 열별로 연산), axis=1은 열을 따라 연산을 수행(각 행 별로 연산을 수행)
    # 즉 여기서는 영화의 행을 따라서 유사도의 평균값을 계산하여 배열을 저장한다는 뜻이다.
    # 예를 들면 similar_movies[A]는 영화 A와 사용자가 좋아요를 누르거나 리뷰(높은 평점)를 쓴 영화 간의 평균 유사도를 나타낸다.
    
    if target_overviews:
        target_tfidf_matrix = tfidf_vectorizer.transform(target_overviews)
        cosine_sim = cosine_similarity(target_tfidf_matrix, tfidf_matrix)
        overview_sim = cosine_sim.mean(axis=0)
    else:
        overview_sim = np.zeros(len(all_movies))

    # 장르 및 키워드 유사도 계산
    if target_genres:
        target_genre_vector = get_genre_vector(target_genres, all_genres)
        genre_sim = cosine_similarity([target_genre_vector], genre_vectors).flatten()
    else:
        genre_sim = np.zeros(len(all_movies))

    if target_keywords:
        target_keyword_vector = get_keyword_vector(target_keywords, all_keywords)
        keyword_sim = cosine_similarity([target_keyword_vector], keyword_vectors).flatten()
    else:
        keyword_sim = np.zeros(len(all_movies))

    # 종합 유사도 계산 (가중 평균)
    overview_weight = 0.4
    genre_weight = 0.3
    keyword_weight = 0.2
    people_weight = 0.1

    # 모든 유사도 배열의 크기 확인
    num_movies = len(all_movies)
    overview_sim = np.resize(overview_sim, num_movies)
    genre_sim = np.resize(genre_sim, num_movies)
    keyword_sim = np.resize(keyword_sim, num_movies)
    people_vectors = np.resize(people_vectors, num_movies)

    combined_sim = (overview_weight * overview_sim +
                    keyword_weight * keyword_sim +
                    genre_weight * genre_sim +
                    people_weight * people_vectors)

    # 유사도 점수를 기반으로 추천 영화 선정
    # similar_movies 배열 값을 내림차순으로 정렬한 인덱스를 반환한다. argsort가 오름차순인데 -1로 정렬
    # 즉, 가장 유사도가 높은 영화부터 낮은 영화까지 인덱스를 포함한 배열을 생성한다.
    similar_movies_indices = combined_sim.argsort()[::-1]

    # 배열을 순회하면서 idx를 가지고 이미 리뷰를 작성하거나 좋아요를 누른 영화와 중복되는지 검사를 해보고 영화를 10개 추천해준다.
    recommended_movies = []
    for idx in similar_movies_indices:
        recommended_movie = all_movies[int(idx)]
        if recommended_movie not in liked_movies and not reviewed_movies.filter(movie=recommended_movie).exists():
            recommended_movies.append(recommended_movie)
            if len(recommended_movies) >= 10:  # 최대 10개 추천
                break

    return recommended_movies


import numpy as np


def get_genre_vector(genres, all_genres):
    genre_vector = np.zeros(len(all_genres))
    genre_indices = {genre.id: idx for idx, genre in enumerate(all_genres)}
    for genre in genres:
        genre_vector[genre_indices[genre.id]] = 1
    return genre_vector

def get_similar_movies_survey(user):
    survey_response = SurveyResponse.objects.filter(user=user).latest('id')

    if not survey_response:
        return Movie.objects.none()

    # 선택한 답변 출력
    print(f"Question 1 answer: {survey_response.question_1}")
    print(f"Question 2 answer: {survey_response.question_2}")
    print(f"Question 3 answer: {survey_response.question_3}")
    print(f"Question 4 answer: {survey_response.question_4}")
    print(f"Question 5 answer: {survey_response.question_5}")
    print(f"Question 6 answer: {survey_response.question_6}")

    question_1_keywords = {
        'a': ['animals', 'wildlife', 'pets', 'nature', 'zoo', 'safari', 'creatures', 'jungle', 'habitat'], # 동물
        'b': ['machines', 'technology', 'robots', 'gadgets', 'mechanics', 'innovation', 'automation', 'artificial intelligence', 'cybernetics'], # 기계
        'c': ['heart', 'love', 'romance', 'passion', 'emotion', 'family', 'relationships', 'affection', 'sentiment'], # 하트
        'd': ['guns', 'weapons', 'action', 'violence', 'combat', 'war', 'battle', 'conflict', 'military', 'firearms'], # 총
        'e': ['dragons', 'fantasy', 'myth', 'legend', 'adventure', 'magic', 'sorcery', 'epic', 'creatures', 'heroic'], # 용
        'f': ['space', 'universe', 'astronomy', 'science fiction', 'exploration', 'cosmos', 'aliens', 'galaxy', 'extraterrestrial', 'spaceship'], # 우주
        'g': ['comedy', 'humor', 'funny', 'laughter', 'sitcom', 'parody', 'satire', 'slapstick', 'jokes', 'hilarious'], # 코미디
        'h': ['horror', 'fear', 'scary', 'terror', 'creepy', 'haunting', 'nightmare', 'crisis'], # 공포
        'i': ['sports', 'competition', 'athletics', 'games', 'fitness', 'exercise', 'championship', 'tournament', 'training', 'team'], # 스포츠
        'j': ['music', 'concert', 'band', 'singing', 'melody', 'orchestra', 'instrument', 'performance', 'harmony', 'lyrics'], # 음악
        'k': ['animation', 'cartoon', 'anime', 'drawings', 'fantasy', 'animated', 'CGI', '2D', '3D', 'stop-motion'], # 애니메이션
        'l': ['disaster', 'volcano', 'earthquake', 'calamity', 'tsunami', 'hurricane', 'flood', 'catastrophe', 'emergency'] # 자연재해
    }
    question_2_genres = {
        'a': ['disaster', 'small town', 'survival', 'emergency', 'chaos', 'adventure'],  # 재난
        'b': ['aliens', 'first contact', 'extraterrestrial', 'invasion', 'science fiction'], # 외계인
        'c': ['medieval', 'kingdom', 'war', 'dynasty', 'history'], # 중세 
        'd': ['detective', 'investigation', 'mystery', 'crime', 'thriller', 'crime'], # 탐정
        'e': ['family', 'drama', 'relationships', 'love', 'emotions'], # 드라마
        'f': ['power struggle', 'action', 'crime'], # 권력싸움
        'g': ['cute', 'animation'], # 귀여움
        'h': ['smile', 'comedy'], # 즐거움
        'i': ['fantasy'], # 상상력
        'j': ['horror', 'thriller'] # 스릴
    }
    question_3_keywords = {
        'a': ['intelligent villain', 'complex plans', 'mastermind', 'antagonist', 'schemer', 'cunning', 'strategist', 'genius', 'manipulative', 'deceptive'], # 지적 악당
        'b': ['brave hero', 'courage', 'protagonist', 'adventure', 'fearless', 'valiant', 'bold', 'daring', 'selfless', 'noble'], # 용감한 주인공
        'c': ['cynical sidekick', 'insightful', 'wise', 'mentor', 'support', 'sarcastic', 'witty', 'guide', 'advisor', 'loyal'], # 냉소적 조력자
        'd': ['ordinary person', 'conflict resolution', 'realistic', 'relatable', 'everyman', 'common', 'average', 'mundane', 'authentic', 'practical'], # 평범한 사람
        'e': ['adventurous', 'accidental hero', 'unexpected', 'journey', 'growth', 'unintended', 'novel', 'exciting', 'serendipitous', 'transformative'] # 모험에 휘말리는 사람
    }
    question_5_keywords = {
        'a': ['tension', 'thrill', 'excitement', 'suspense', 'adrenaline', 'edge-of-seat', 'gripping', 'intense', 'nervousness', 'pressure'], # 긴장감
        'b': ['emotion', 'tear-jerker', 'heartfelt', 'moving', 'sentimental', 'touching', 'poignant', 'affecting', 'emotional', 'melancholic'], # 감동
        'c': ['laughter', 'humor', 'comedy', 'fun', 'joy', 'amusement', 'entertainment', 'hilarity', 'light-hearted', 'cheerful'], # 웃음
        'd': ['inspiration', 'thought-provoking', 'motivational', 'uplifting', 'enlightening', 'insightful', 'encouraging', 'stimulating', 'inspirational', 'hopeful'], # 영감
        'e': ['relaxation', 'comfort', 'calm', 'peaceful', 'soothing', 'tranquil', 'serene', 'reassuring', 'restful', 'relaxing'] # 편안함
    }

    preferred_keywords = []
    preferred_keywords.extend(question_1_keywords[survey_response.question_1.lower()])
    preferred_keywords.extend(question_3_keywords[survey_response.question_3.lower()])
    preferred_keywords.extend(question_5_keywords[survey_response.question_5.lower()])
    preferred_keywords = " ".join(preferred_keywords)

    preferred_runtime = survey_response.question_4
    preferred_rating = survey_response.question_6

    # 쿼리 최적화: 필요한 필드만 선택하고, overview가 없는 영화 제외
    filtered_movies = Movie.objects.exclude(overview__isnull=True).exclude(overview__exact='').only('overview', 'runtime', 'vote_average').prefetch_related('genres')

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

    overviews = [movie.overview.lower() for movie in filtered_movies]
    if not overviews:
        return Movie.objects.none()

    # TF-IDF 벡터화
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(overviews)

    target_matrix = vectorizer.transform([preferred_keywords.lower()])
    cosine_sim = cosine_similarity(target_matrix, matrix)
    overview_sim = cosine_sim.flatten()

    # 장르 유사도 계산
    all_genres = list(Genre.objects.all())
    preferred_genres = question_2_genres[survey_response.question_2.lower()]
    preferred_genres_set = set(preferred_genres)

    genre_similarities = []
    for movie in filtered_movies:
        movie_genres = set([genre.name.lower() for genre in movie.genres.all()])
        common_genres = len(preferred_genres_set & movie_genres)
        total_genres = len(preferred_genres_set | movie_genres)
        genre_similarity = common_genres / total_genres if total_genres != 0 else 0
        genre_similarities.append(genre_similarity)

    genre_similarities = np.array(genre_similarities)

    # 가중치 설정
    overview_weight = 0.3
    genre_weight = 0.3
    q3_weight = 0.2
    q5_weight = 0.2

    # 최종 유사도 계산 (가중치 적용)
    total_similarity = (overview_weight * overview_sim) + (genre_weight * genre_similarities) + (q3_weight * np.array([1]*len(overview_sim))) + (q5_weight * np.array([1]*len(overview_sim)))

    sorted_indices = total_similarity.argsort()[::-1]
    sorted_movies = [filtered_movies[int(idx)] for idx in sorted_indices[:10]]

    return sorted_movies





