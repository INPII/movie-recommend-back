# 5월 19일
- ERD 100퍼센트 확정
- back 역할 : 감독 배우 장르 를 역참조로 해서 데이터를 front쪽으로 보내주기

- json 을 만드는 파이썬 파일을 만들때, 데이터 자체가 null일 경우를 대비하여서 movie.get('title','null') 이런식으로 받아왔어야했다.
- 그리고 json 파일에 pk가 null 일경우에는 직접 삭제를 했어야했다. "pk":"null" 을 찾아서 직접 삭제
- model을 만들때 null=True 를 해야하며 변경했으면 무조건 makemigrations 하기!

## 변경사항
actor, director을 people로 합침(관리하기가 더 편함)

# 5월 20일
- 오늘 한것들
    1. 영화 검색, 게시글 검색 알고리즘
    2. 게시판, 게시글, 댓글
    3. 영화 리뷰 작성하기
    4. 프로필 상세 페이지 만들기

- 내일 할것들
연결 
게시글,리뷰 delete, update,
동일 영화에 request.user의 리뷰가있다면 또 생성 못하고 수정 만 할수 있게 설정(평점 주작가능하니까.)
평점넣으면 영화 전체 평점에도 반영할수있게
좋아요,

팔로우 기능, 
프로필 페이지 조회수, 
알고리즘, 

추가기능(여유): 검색기능을 제목, 키워드, 배우/감독, 줄거리 로 나눌수있게 selection form으로, 쿼리 나누기 가능


# 5월 21일
- 오늘 한 것
    - 메인페이지 박스오피스, 리뷰, 영화리스트 페이지 백에서 프론트로 연결시키기
    - 좋아요를 리스트 페이지에도 구현을 할때 
    - #동적필드를 추가할때 유용한 도구 SerializerMethodField, 이걸 쓰지않으면 직접 메서드를 오버라이드하여서 추가해야한다.
    - 위의 도구를 사용한다
    - 영화 좋아요, 감독/배우 좋아요, 게시글 좋아요, 리뷰 좋아요 기능 추가
    - 팔로우 기능 추가



# 5월 22일
- 영화 추천 알고리즘 구현(사용자 데이터기반), 설문기반
- url이랑 related_name, 모델 필드 가다듬기,재정의, serializer 재정의




```python
# 코사인 유사도 추천 방식 코드 및 설명주석
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
        recommended_movie = all_movies[idx]
        if recommended_movie not in liked_movies and recommended_movie not in reviewed_movies:
            recommended_movies.append(recommended_movie)
            if len(recommended_movies) >= 10:  # 최대 10개 추천
                break

    return recommended_movies
```

# 5월 23일
좋아요를 누르면 is_liked가 true로 바뀌지만 그것을 사람 리스트나 영화리스트에도 볼수있게하려면 context{'request': request} 라고 view에서 설정을 해줘야 리스트에서도 is_liked 상태를 유지하면서 보내줄수 있다.



# 프로젝트 "MM(MyMovie)"

### 진행기간 : 2024.05.16 ~ 2024.05.24 
### 목표
    - django와 Vue를 이용해서 영화추천서비스를 제공하는 웹서비스 개발
    - 유연성과 효율성을 높여서 사용자가 사용하기 편리한 서비스 개발
    - 유지 보수 하기 쉽도록 서비스 개발
## 팀원 정보 및 업무 분담 내역
 - **이정재**
    - FRONT-END, CSS, 팀장
 - **박재영**
    - BACK-END, 영화 추천 알고리즘
## 데이터 베이스 모델링(ERD)
    - 사진
## 목표 서비스 구현 및 실제 구현 정도
**목표 서비스 구현**
- 회원가입, 로그인
- 영화, 감독, 배우, 장르/키워드, 리뷰 리스트와 상세 페이지
- 프로필 페이지
- 커뮤니티 게시판, 게시글 작성, 댓글 작성
- 리뷰 작성, 별점
- 영화, 감독, 배우, 리뷰, 게시글 좋아요 기능
- 프로필 팔로우 기능
- OPEN AI API를 통한 연동
- 영화 추천 알고리즘을 통해 영화를 추천해주기

**실제 구현 화면**
    - 메인 페이지
    - 영화 리스트 페이지
    - 감독 리스트 페이지
    - 배우 리스트 페이지
    - 장르 / 키워드 리스트 페이지
    - 프로필 페이지
    - 게시판 페이지
    - AI 질문



- ![alt text](/image/image-1.png)
- ![alt text](/image/image-1.png)
- ![alt text](/image/image-2.png)
- ![alt text](/image/image-3.png)
- ![alt text](/image/image-4.png)
- ![alt text](/image/image-5.png)
- ![alt text](/image/image-6.png)
- ![alt text](/image/image-7.png)
- ![alt text](/image/image-8.png)
- ![alt text](/image/image-9.png)
- ![alt text](/image/image-10.png)
- ![alt text](/image/image-11.png)
- ![alt text](/image/image-12.png)
- ![alt text](/image/image-13.png)
- ![alt text](/image/image-14.png)
- ![alt text](/image/image-15.png)

## 핵심 기능에 대한 설명
1. 사용자의 데이터(사용자가 좋아요 누른 영화, 리뷰를 작성한 영화(평점을 높은순으로 들고오기))를 통해서 장르, 키워드, 줄거리의 유사도를 판단하여 영화를 추천하는 알고리즘

2. 영화 리스트, 배우리스트, 감독 리스트, 또 영화 상세페이지 안에 있는 배우/감독 리스트, 리뷰 리스트, 게시글 리스트 모든 곳에서 좋아요(로그인 했을시)를 누를수 있고, 내가 좋아하는 것인지 확인 할 수 있는 기능

3. 영화 검색 창에서 검색을 하면 영화 제목, 장르, 키워드, 줄거리 등에서 검색을 하여서 검색결과를 가져다 주는 검색기능

4. 장르나 키워드를 눌렀을때 관련 영화들을 보여주는 기능

5. 프로필에 그사람이 좋아요 누른 영화, 배우, 감독을 볼수 있고 그것에 기반하여 그 사람이 좋아하는 장르 3가지를 표현하여서 프로필 상세 페이지에 나타내었다. 그외에도 그사람이 쓴 리뷰를 볼수있으며 다른사람이 프로필 상세페이지에 몇명이나 들어왔는지 조회수를 확인할 수 있다. 또한 최근 활동이 언제인지도 확인할 수 있다. 팔로우 수와 팔로잉 수를 알 수 있다.

6. 커뮤니티 게시판에 글을 생성하고 그 글의 댓글을 생성할수 있다. 게시글의 조회수를 알 수 있다.

7. 영화, 배우, 감독 페이지에서 스크롤을 끝까지 내리면 자동으로 리스트가 추가되는 기능

8. 크롤이랑 
7. 게시판의 글 수정은 페이지 이동없이 제목과 본문을 수정 가능

8. 영화 리뷰 또한 페이지 이동없이 별점과 본문을 수정 및 삭제 가능

9. chatGPT 챗봇 기능을 활용할 수 있는 기능

## 영화 추천 알고리즘에 대한 기술적 설명
영화를 추천하기 위해서 코사인 유사도를 이용했다.
코사인 유사도란 두 벡터간의 방향 유사성을 측정하여, -1에서 1 사이의 값을 반환하는 수치이다, -1이면 반대, 0이면 관계없음, 1에 가까우면 매우 유사하다 라는 뜻. 하지만 컴퓨터는 텍스트를 가지고 계산을 못하기 때문에 TF-IDF로 텍스트를 벡터화 시킨다. TF-IDF는 단어의 중요도를 계산하여 벡터로 만들고 자주 등장하는 단어일 수록 가중치가 낮아진다. 그리고 불용어를 제거하여서 추천의 정확도를 더 높였다.

사용자가 좋아요 한 영화의 정보(줄거리), 리뷰를 쓴 영화(평점 높은순)의 줄거리, 키워드, 장르, 감독/배우를 TF-IDF를 통해 변환하고 영화리스트와 비교하여서 
종합 유사도 계산 (가중 평균)에 비중을 줄거리,장르, 키워드, 감독/배우 순으로 가중평균을 준다음 계산하여서 유사도가 가장 1에 가까운 영화부터 10개를 뽑아오는 형식이다.

다음은 코드와 그에 대한 자세한 설명이다.
```python
# 밑에 두 함수 장르 벡터와 키워드 벡터는 장르 및 키워드를 이진 벡터로 변환을 한다. 그리고 모든 장르 및 키워드의 인덱스를 매핑하여 해당 영화에 속하는 장르 또는 키워드의 인덱스를 1로 설정한다.
#np.zero는 배열을 초기화 하는 용도인데 이 이유는 데이터 구조를 미리 정해진 크기와 형태로 준비하여서 계산의 안정성과 일관성을 보장하고 오류를 방지할 수있다.
# 파이썬 내장함수 enumerate로 반복가능한 객체의 인덱스와 요소를 동시에 얻을 수 있게 해준다.
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
    #np.array로 효율적인 메모리를 사용
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
    # np.resize 함수를 사용하는 이유는 다양한 영화 데이터의 유사도 배열 크기를 동일하게 맞추기 위해서이다. 유사도 배열을 동일한 길이로 만들어야지 계산을 할 수 있기 때문.
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
```

## 기타(느낀점, 후기 등)
박재영 - 우선 BACK-END 쪽을 담당하면서 힘들었던 점은 FRONT-END와의 데이터 형식이 일치하지 않아서 생기는 오류와, 데이터를 받아올 때 내가 원하는 필드를 받아오기 위해서 JSON 형식으로 데이터를 받아올 때 생기는 오류가 제일 힘들었다. 우선 만든 ERD 특성상 ManyToMany fields가 많았는데 related_name 관련해서 정말 많은 오류가 생겼었다. 한쪽에 모델명 때문에 오류가 생겨서 수정하고 해결을 했을 때 문제가 됐던 모델명이 관련된 모든 곳에서 오류가 생겼다. 그로 인해 정재형이 몇시간동안 오타를 찾은적도 있어서 너무 미안했던 기억이 있다. 그리고 JSON도 TMDB에서 받아왔는데 우리가 원하는 모델을 만드려면 movie_id를 들고와서 그것으로 keyword나 다른 것들을 가져와야 했는데 들고올때 빈값이 올때도 있어서 loaddata를 할때마다 양식에 맞지않다고 퇴짜를 계속 맞았었다. 그때마다 데이터를 하나씩 지워가며 어떤것이 오류가 있었는지 확인을 해야했고 거기에 시간을 많이 낭비했었던 기억이 있다. 이제는 python 파일로 어떤것이 오류가 있는지 일치하지 않는 JSON데이터를 바로 비교할 수 있는 코드를 짜서 빠르게 해결을 할 수도 있는 경험이 생겼다. 또 좋아요를 눌렀을 때는 바로 적용이 되었는데 새로고침을 하면 다시 is_liked가 false가 되는 오류가 있었다 그떄 context{'request': request} 라고 view에서 설정을 해줘야 리스트에서도 is_liked 상태를 유지하면서 보내줄 수 있었다. 이런 오류를 해결 한 끝에 결국 내가 생각한대로 데이터가 보내져서 front쪽에서 잘 작동되는 것을 보며 너무 좋았고 전체적인 흐름을 파악할 수 있어서 좋았다. 뭔가 처음이라서 정리를 못하고 중간중간에 헤맸었는데 처음부터 정리를 잘하고 차근차근 순서대로 진행을 해야할 필요가 있다고 느꼈고, 수정된 것이 있다면 바로바로 소통을 해서 둘다 재확인 작업을 거쳐야 한다고 느꼈다. 아무래도 처음 협업하는 거라 시간을 낭비를 한 부분이 있지만 이제는 잘 할 수 있다는 자신감이 생겼다. 
- 이정재

  전반적으로 Front-end에 사용되는 언어와 프레임워크에 대해 지식이 없었으나 프로젝트를 통한 여러 단계 성장함을 느낄 수 있었습니다.
  Vue 기반의 프로젝트를 생성하고 Route, Pinia를 통해 SPA에 대한 이해와 흥미를 느낄 수 있었습니다.
  잠을 줄여가며 개발에 집중함으로써 프로젝트에 깊이 빠져들어 시간 가는 줄 모르고 진행했습니다.
  추후에는 AI 관련 API를 활용하여 특화된 프로젝트를 진행할 계획입니다.
