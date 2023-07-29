'''
포맷이 다르게 수집된 데이터들을
db로 보낼 포맷에 맞춰서 json파일로 재처리.

문자별 빈도수가 잘못 저장해서 그런지 Counter오브젝트가 아닌 Dict가 되어서
전체댓글 데이터가 있어서 이를 이용해 다시 Counter뽑아서 워드클라우드까지 생성.
 ..> 추후에 댓글 스크래핑 할 때, 애초에 포맷을 맞춰서 하는 방향으로 개선 가능.

# 기존 영상별 1차 수집 데이터
'category'  -> str > 사용X
'id'        -> int > 사용X
'title'     -> str > ㅇㅇ
'img_url'   -> str > ㅇㅇ
'comments'  -> list(str) > 대체로 40개쯤? 더 적은것도
'comments_all' 올..
'frequency' -> 안써 comments_all 다시 처리하는걸로
'metadata'
    'url'   -> str > video_id로 쓰임_id
    'count_of_view' -> int > ㅇㅇ
    'count_of_comment'  -> int > ㅇㅇ
    'scrap_count'   -> 안씀

# 목적 파일
db의 각 테이블(comment, keyword, video)의
row단위 맞는 데이터 양식으로 변환
   comment : 	{ video_id : [comments], }
   keyword : 	{ video_id : "keyword", }
     video : 	{ video_id : [ thumbnail_url, title, url, count_of_view, count_of_comment ], }
'''

from os import path
import json
from konlpy.tag import Hannanum
from collections import Counter

FILE_NAME = "raw_data/{}_commentary_json_{}.json"
categories = ["recent", "music"]

comment_dict = {}
keyword_dict = {}
video_dict = {}

hannanum = Hannanum()

for category in categories:
    for id in range(101,101+50):
        FILE = FILE_NAME.format(category,"%03d"%id)
        if path.exists(FILE):
            with open(FILE,"r") as f:
                j = json.loads(json.load(f))
                j_meta = j["metadata"]

                video_url = j_meta["url"]
                count_of_view = j_meta["count_of_view"]
                count_of_comment = j_meta["count_of_comment"]
                video_id = video_url[video_url.find("?v=")+3:]
                title = j["title"]
                thumbnail_url = j["img_url"]
                comments = j["comments"]

                nouns_all = []
                for comment in j["comments_all"]:
                    nouns = hannanum.nouns(comment)
                    nouns_all.extend(\
                        [noun for noun in nouns if (
                                len(noun) > 1 and
                                "ㅋㅋ" not in noun and
                                "ㅎㅎ" not in noun and
                                "ㅜㅜ" not in noun and
                                "ㅠㅠ" not in noun
                        )])
                try:
                    counter = Counter(nouns_all).most_common(30)
                except:
                    counter = {}
                keyword = []
                for k,_ in counter:
                    keyword.append(k)
                keyword = " ".join(keyword)
                if len(comments)>30:
                    comments = comments[:30]
                if len(video_id) != 11:
                    print("id 길이가 다름.", video_id,"->", FILE)
            comment_dict[video_id] = comments
            keyword_dict[video_id] = keyword
            video_dict[video_id] = [thumbnail_url, title, video_url,
                                    count_of_view, count_of_comment]

with open("data/recent_music_comment.json", "w") as f:
    json.dump(comment_dict, f)
with open("data/recent_music_keyword.json", "w") as f:
    json.dump(keyword_dict, f)
with open("data/recent_music_video.json", "w") as f:
    json.dump(video_dict, f)