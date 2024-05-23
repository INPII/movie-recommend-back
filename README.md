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


# 5월 21
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
**이정재**
    - 팀장, FRONT-END, CSS  
**박재영**
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
    -사진

## 핵심 기능에 대한 설명
1. 사용자의 데이터(사용자가 좋아요 누른 영화, 리뷰를 작성한 영화(평점을 높은순으로 들고오기))를 통해서 장르, 키워드, 줄거리의 유사도를 판단하여 영화를 추천하는 알고리즘

2. 영화 리스트, 배우리스트, 감독 리스트, 또 영화 상세페이지 안에 있는 배우/감독 리스트, 리뷰 리스트, 게시글 리스트 모든 곳에서 좋아요(로그인 했을시)를 누를수 있고, 내가 좋아하는 것인지 확인 할 수 있는 기능

3. 영화 검색 창에서 검색을 하면 영화 제목, 장르, 키워드, 줄거리 등에서 검색을 하여서 검색결과를 가져다 주는 검색기능

4. 장르나 키워드를 눌렀을때 관련 영화들을 보여주는 기능

5. 프로필에 그사람이 좋아요 누른 영화, 배우, 감독을 볼수 있고 그것에 기반하여 그 사람이 좋아하는 장르 3가지를 표현하여서 프로필 상세 페이지에 나타내었다. 그외에도 그사람이 쓴 리뷰를 볼수있으며 다른사람이 프로필 상세페이지에 몇명이나 들어왔는지 조회수를 확인할 수 있다. 또한 최근 활동이 언제인지도 확인할 수 있다.

6. 커뮤니티 게시판에 글을 생성하고 그 글의 댓글을 생성할수 있다. 게시글의 조회수를 알 수 있다.

7. 

## 영화 추천 알고리즘에 대한 기술적 설명
## 기타(느낀점, 후기 등)
