'''
DB에 저장되는 스키마 정하기위해서
전처리이전 raw_data를 통해서
데이터 최대값이 어느정도인지 파악하기 위한 파일.

'''

from recent_music_commentary_json_format import *
from os import path


FILE_NAME = "raw_data/{}_commentary_json_{}.json"
categories = ["recent", "music"]
max_title_length = 0
max_url_length = 0
max_img_url_length = 0
max_comment_length = 0
total = {}
for category in categories:
    sum=0
    for id in range(101,101+50):
        name = FILE_NAME.format(category,"%03d"%id)
        if path.exists(name):
            a = tmp_read_json(name)
            t = a["metadata"]["scrap_count"]
            max_title_length = max(max_title_length,len(a["title"]))
            max_url_length = max(max_url_length,len(a["metadata"]["url"]))
            max_img_url_length = max(max_img_url_length,len(a["img_url"]))
            for i in a["comments_all"]:
                max_comment_length = max(max_comment_length,len(i))
            print(name,":",t)
            sum+=t
    total[category] = sum
to = 0
for c in categories:
    to+=total[c]
    print(c,":",total[c])
print("total :",to)
print("max_title_length:",max_title_length)
print("max_url_length:",max_url_length)
print("max_img_url_length:",max_img_url_length)
print("max_comment_length:",max_comment_length)

