# 5월 19일
- ERD 100퍼센트 확정
- back 역할 : 감독 배우 장르 를 역참조로 해서 데이터를 front쪽으로 보내주기

- json 을 만드는 파이썬 파일을 만들때, 데이터 자체가 null일 경우를 대비하여서 movie.get('title','null') 이런식으로 받아왔어야했다.
- 그리고 json 파일에 pk가 null 일경우에는 직접 삭제를 했어야했다. "pk":"null" 을 찾아서 직접 삭제
- model을 만들때 null=True 를 해야하며 변경했으면 무조건 makemigrations 하기!

## 변경사항
actor, director을 people로 합침(관리하기가 더 편함)

