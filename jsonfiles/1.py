import requests
import json

TMDB_API_KEY = '7206c9eeca4b0f1e1266fd3dcd719152'
global_movies=[]
global_keywords=[]
def get_movie_datas():
    print('movie')
    for i in range(1, 2):
        print(f'moviepage {i}')
        request_url = f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=en-US&page={i}"
        movies = requests.get(request_url).json()
        
        for movie in movies['results']:
            # print(movie['id'])
            request2_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={TMDB_API_KEY}&language=en-US"
            credits = requests.get(request2_url).json()
            request3_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/keywords?api_key={TMDB_API_KEY}"
            keywords2 = requests.get(request3_url).json()
            
            # actors=[]
            # directors=[]
            peoples=[]
            
            for people in credits["cast"]:
                
                if people["known_for_department"] in['Acting','Directing']:
                    peoples.append(people['id'])
                    # print(people['id'])
                    global_people.append(people['id'])
                    # people.append(actor["id"])
                    # global_actors.append(actor["id"])
            # for director in credits["cast"]:
            #     if director["known_for_department"] == 'Directing':
            #         if len(directors) > 10:
            #             break
            #         directors.append(director["id"])
            #         global_directors.append(director["id"])
            # print(keywords2)
            for keyword in keywords2["keywords"]:
                # print(keyword)
                global_keywords.append(keyword["id"])
            
            
            
            global_movies.append(movie['id'])

def get_moviedetail(movieset):
    print('moviedetail')
    total_data = []
    for movie_id in movieset:
        # print(f'moviedetail {movie_id}')
        request_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
        movie = requests.get(request_url).json()

    
        request2_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR"
        credits = requests.get(request2_url).json()
        actors=[]
        for actor in credits["cast"]:
            if actor["known_for_department"] in['Acting','Directing']:
                actors.append(actor["id"])

        request3_url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={TMDB_API_KEY}"
        keywords = requests.get(request3_url).json()
        keywords1 = []
        for keyword in keywords["keywords"]:
                keywords1.append(keyword["id"])



        fields = {
            # 'movie_id': movie['id'],
            'adult': movie.get('adult','null'),
            'backdrop_path': movie['backdrop_path'],
            'budget': movie['budget'],
            'imdb_id' : movie['imdb_id'],
            'origin_country' : movie['origin_country'],
            'original_language' : movie['original_language'],
            'original_title' : movie['original_title'],
            'overview' : movie['overview'],
            'popularity' : movie['popularity'],
            'poster_path' : movie['poster_path'],
            'release_date' : movie['release_date'],
            'revenue' : movie['revenue'],
            'runtime' : movie['runtime'],
            'revenue' : movie['revenue'],
            'status' : movie['status'],
            'tagline' : movie['tagline'],
            'title' : movie['title'],
            'video' : movie['video'],
            'vote_average' : movie['vote_average'],
            'vote_count' : movie['vote_count'],
            'genres': [genre['id'] for genre in movie['genres']],
            'people': actors,
            'keyword':keywords1
        }

        data = {
            "pk": movie['id'],
            "model": "movies.movie",
            "fields": fields
        }

        total_data.append(data)

    with open("movie.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)
        pass

def get_genre_data():
    print("genre")
    total_data = []

    request_url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    genres = requests.get(request_url).json()

    for genre in genres['genres']:
        fields = {
            # 'genre_id': genre['id'],
            'name': genre['name'],
        }

        data = {
            "pk": genre['id'],
            "model": "movies.genre",
            "fields": fields
        }
        total_data.append(data)

    with open("genre.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)

# def get_actor_data(actorset):
#     print("actor")
#     total_data = []
#     for person_id in actorset:
#         request_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}&language=en-US"
#         actor = requests.get(request_url).json()

        
#         fields = {
#             # 'movie_id': movie['id'],
#             'name': actor['name'],
#             'gender': actor['gender'],
#             'profile_img': actor['profile_path'],
#             'biography' : actor['biography'],
#             'imdb_id' : actor['imdb_id'],
#             'popularity' : actor['popularity']
#         }

#         data = {
#             "pk": actor['id'],
#             "model": "movies.actor",
#             "fields": fields
#         }

#         total_data.append(data)

#     with open("actor.json", "w", encoding="utf-8") as w:
#         json.dump(total_data, w, indent=4, ensure_ascii=False)
#         pass

def get_people_data(peopleset):
    print("people")
    total_data = []
    for person_id in peopleset:
        request_url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={TMDB_API_KEY}&language=en-US"
        people = requests.get(request_url).json()

        
        fields = {
            # 'movie_id': movie['id'],
            'adult': people.get('adult','null'),
            'biography': people.get('biography','null'),
            'birthday': people.get('birthday','null'),
            'deathday' : people.get('deathday','null'),
            'gender' : people.get('gender','null'),
            'imdb_id' : people.get('imdb_id','null'),
            'known_for_department' : people.get('known_for_department','null'),
            'name' : people.get('name','null'),
            'place_of_birth' : people.get('place_of_birth','null'),
            'popularity' : people.get('popularity','null'),
            'profile_path' : people.get('profile_path','null')
        }

        data = {
            "pk": people.get('id','null'),
            "model": "movies.people",
            "fields": fields
        }

        total_data.append(data)

    with open("people.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)
        pass

def get_keyword_data(movieset):
    print("keyword")
    total_data = []

    for movie in movieset:
        print(movie)
        request_url=f"https://api.themoviedb.org/3/movie/{movie}/keywords?api_key={TMDB_API_KEY}"
        keywords = requests.get(request_url).json()
        
        for keyword in keywords['keywords']:
            data = {
                "pk": keyword['id'],
                "model": "movies.keyword",
                "fields": {
                    "name": keyword['name']
                }
            }
            total_data.append(data)

    with open("keyword.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent=4, ensure_ascii=False)



global_people=[]
get_movie_datas()
set_movies = set(global_movies)
get_keyword_data(set_movies)
get_moviedetail(set_movies)
set_people = set(global_people)
print(global_people)
print(set_people)
get_people_data(set_people)
get_genre_data()