
카테고리 별 작업한 코드 내역입니다.

< 게임, 영화 - Game_Movie_Crawling.ipynb > 

크롤링 -> DataFrame -> json


< 최신, 인기 > 

크롤링 -> dictionary -> json


< Category, Trending >
- Category: 인기 급상승에서 분류를 의미합니다. (예시: 최신, 음악, 게임, 영화)
- Trending: 카테고리와 영상을 매핑하기 위한 테이블입니다. (n:n 관계)
- 다음과 같은 형태로 데이터가 수집됩니다.
  Category: [[ id, category ]]
  Trending: [[ category_id, video_id]]

< Django 데이터 적재>
- Django에 Post 요청을 통해 수집한 데이터를 적재합니다.
