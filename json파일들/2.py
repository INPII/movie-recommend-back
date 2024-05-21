import requests
import json

TMDB_API_KEY = '7206c9eeca4b0f1e1266fd3dcd719152'
global_movies = []
global_people = []
global_keywords = set()

def get_movie_datas():
    print('movie')
    for i in range(1, 2):
        print(f'moviepage {i}')
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={i}"
        movies_response = requests.get(request_url).json()
        
        for movie in movies_response['results']:
            request_credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={TMDB_API_KEY}&language=en-US"
            credits_response = requests.get(request_credits_url).json()
            request_keywords_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/keywords?api_key={TMDB_API_KEY}"
            keywords_response = requests.get(request_keywords_url).json()
            
            for people in credits_response["cast"]:
                if people["known_for_department"] in ['Acting', 'Directing']:
                    global_people.append(people['id'])

            for keyword in keywords_response["keywords"]:
                global_keywords.add((keyword['id'], keyword['name']))
            
            global_movies.append(movie['id'])

def get_moviedetail(movieset):
    print('moviedetail')
    total_data = []
    for movie_id in movieset:
        print(f'moviedetail {movie_id}')
        
        # 영어 데이터 요청
        request_url_en = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        movie_en = requests.get(request_url_en).json()
        
        # 한국어 데이터 요청
        request_url_kr = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=ko-KR"
        movie_kr = requests.get(request_url_kr).json()

        request_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR"
        credits_response = requests.get(request_credits_url).json()
        
        # 배우는 popularity 높은 순으로 정렬하여 상위 10명만 추출
        actors = sorted([actor for actor in credits_response["cast"] if actor["known_for_department"] == 'Acting'], key=lambda x: x['popularity'], reverse=True)[:10]
        people_ids = [actor['id'] for actor in actors]
        
        # 감독은 한 명만 추출하여 추가
        directors = [director['id'] for director in credits_response["crew"] if director["known_for_department"] == 'Directing']
        if directors:
            people_ids.append(directors[0])  # 감독을 추가

        # 키워드 데이터 요청
        request_keywords_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}"
        keywords_response = requests.get(request_keywords_url).json()
        keyword_ids = [keyword['id'] for keyword in keywords_response.get('keywords', [])]
        
        for keyword in keywords_response.get('keywords', []):
            global_keywords.add((keyword['id'], keyword['name']))

        fields = {
            'adult': movie_en.get('adult', 'null'),
            'backdrop_path': movie_en['backdrop_path'],
            'budget': movie_en['budget'],
            'imdb_id': movie_en['imdb_id'],
            'origin_country': movie_en['origin_country'],
            'original_language': movie_en['original_language'],
            'original_title': movie_en['original_title'],
            'overview': movie_en['overview'],
            'popularity': movie_en['popularity'],
            'poster_path': movie_en['poster_path'],
            'release_date': movie_en['release_date'],
            'revenue': movie_en['revenue'],
            'runtime': movie_en['runtime'],
            'status': movie_en['status'],
            'tagline': movie_en['tagline'],
            'title': movie_en['title'],
            'video': movie_en['video'],
            'vote_average': movie_en['vote_average'],
            'vote_count': movie_en['vote_count'],
            'genres': [genre['id'] for genre in movie_en['genres']],
            'people': people_ids,
            'name_kr': movie_kr['title'],
            'overview_kr': movie_kr['overview'],
            'keyword': keyword_ids
        }

        data = {
            "pk": movie_en['id'],
            "model": "movies.movie",
            "fields": fields
        }

        total_data.append(data)

    with open("movie2.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)

def get_genre_data():
    print("genre")
    total_genre_data = []

    # 영어 장르 데이터 요청
    request_url_en = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    genres_en_response = requests.get(request_url_en).json()

    # 한국어 장르 데이터 요청
    request_url_kr = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-KR"
    genres_kr_response = requests.get(request_url_kr).json()

    genre_kr_dict = {genre['id']: genre['name'] for genre in genres_kr_response['genres']}

    for genre in genres_en_response['genres']:
        fields = {
            'name': genre['name'],
            'name_kr': genre_kr_dict.get(genre['id'], '')
        }

        data = {
            "pk": genre['id'],
            "model": "movies.genre",
            "fields": fields
        }
        total_genre_data.append(data)

    with open("genre2.json", "w", encoding="utf-8") as w:
        json.dump(total_genre_data, w, indent=4, ensure_ascii=False)

def get_people_data(peopleset):
    print("people")
    total_people_data = []
    for person_id in peopleset:
        request_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}&language=en-US"
        people_response = requests.get(request_url).json()

        fields = {
            'adult': people_response.get('adult', 'null'),
            'biography': people_response.get('biography', 'null'),
            'birthday': people_response.get('birthday', 'null'),
            'deathday': people_response.get('deathday', 'null'),
            'gender': people_response.get('gender', 'null'),
            'imdb_id': people_response.get('imdb_id', 'null'),
            'known_for_department': people_response.get('known_for_department', 'null'),
            'name': people_response.get('name', 'null'),
            'place_of_birth': people_response.get('place_of_birth', 'null'),
            'popularity': people_response.get('popularity', 'null'),
            'profile_path': people_response.get('profile_path', 'null')
        }

        data = {
            "pk": people_response.get('id', 'null'),
            "model": "movies.people",
            "fields": fields
        }

        total_people_data.append(data)

    with open("people2.json", "w", encoding="utf-8") as w:
        json.dump(total_people_data, w, indent=4, ensure_ascii=False)

def get_keyword_data():
    print("keywords")
    total_keyword_data = []

    for keyword_id, keyword_name in global_keywords:
        fields = {
            'name': keyword_name
        }

        data = {
            "pk": keyword_id,
            "model": "movies.keyword",
            "fields": fields
        }

        total_keyword_data.append(data)

    with open("keyword2.json", "w", encoding="utf-8") as w:
        json.dump(total_keyword_data, w, indent=4, ensure_ascii=False)

global_people = []
get_movie_datas()
set_movies = set(global_movies)
get_moviedetail(set_movies)
set_people = set(global_people)
get_people_data(set_people)
get_genre_data()
get_keyword_data()
