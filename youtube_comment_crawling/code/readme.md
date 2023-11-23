
카테고리 별 작업한 코드 내역입니다.

### 담당 :
|담당자|담당 범위|절차|코드|
|-|:-|:-|:-|
|김태준|게임, 영화 카테고리 크롤링|크롤링 -> DataFrame -> json|Game_Movie_Crawling.ipynb|
|임형우|최신, 음악 카테고리 크롤링|크롤링 -> json|recent_music_*.py<br>request_json.py|
|김상희|영상-카테고리 매핑 데이터 크롤링|크롤링 -> json|category_trending.py|



> Category: 인기 급상승에서 분류를 의미합니다. (예시: 최신, 음악, 게임, 영화)

> Trending: 카테고리와 영상을 매핑하기 위한 테이블입니다. (n:n 관계)

> 다음과 같은 형태로 데이터가 수집됩니다.
> ```
> comment : { video_id: [comments], ..}
> keyword : { video_id: "keyword", ..}
> video   : { video_id: [ thumbnail_url, title, url, count_of_view, count_of_comment ], ..}
> - - -
> Category: [[ id, category ], ..]
> Trending: [[ category_id, video_id ], ..]
> ```
> 자세한 내용은 ../data 디렉토리 참고

< Django 데이터 적재 >   
- request_json.py를 이용하여 Django에 API Post 요청을 통해 수집한 데이터를 적재합니다.
