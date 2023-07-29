'''
* request_json.py
크롤링하여 수집하고, 전처리하여 포맷에 맞춘 json파일을
http request를 통해서 레코드 하나씩 전송.

모든 파일을 같은 폴더에 넣어놓고
*video.json
*keyword.json
*video.json
순서대로 일치하는 파일 내용 전송.
'''

import requests
from os import path, listdir
import json
import re

# scrf값만 가져와서 넣기
headers = {
    "Content-Type":"application/json",
    "X-CSRFToken":"EafFMjAmySk7tMjcN3VhYsf6athHrfyY",
}

# 내가만든 쿠키~,. 세션값이랑 scrf값 가져와서 넣기
cookies = {
    "sessionid":"axiqatufne1ogrvrvxt747cai0ks6vlv",
    "csrftoken":"EafFMjAmySk7tMjcN3VhYsf6athHrfyY"
}

# 리퀘스트 보낼 장고서버 주소
request_url = "http://127.0.0.1:8000/youtube_comment/load/{}/"

# 수집한 json파일이 들어있는 디렉토리 위치.
dir = "./data/"

def request_post(FILE = "", TYPE="", REQUEST_URL = "", headers={}, cookies={}):
    '''

    :param FILE: FILE_NAME with DIR
    :param TYPE: [ video | comment | keyword ]
    :param REQUEST_URL:
    '''
    print(f"submit progress..")
    print(f" FILE:\t\'{FILE}\'")
    print(f" TYPE:\t{TYPE}")

    j = {}
    id_list = []
    # read file
    if path.exists(FILE):
        with open(FILE,"r") as f:
            j = json.load(f)
            for id in j.keys():
                id_list.append(id)

    print(f"record count : {len(id_list)}\n")

    if TYPE=="video":
        for id in id_list:
            print(f"{id}.. ",end="")
            thumbnail_url,title,url,count_of_view,count_of_comment = j[id]

            data = {
                'id':id,
                'thumbnail_url':thumbnail_url,
                'title':title,
                'url':url,
                'count_of_view':count_of_view,
                'count_of_comment':count_of_comment,
            }

            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)

            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)

    if TYPE == "comment":
        for id in id_list:
            print(f"{id}.. ", end="")
            err = 0
            cpt = 0
            for comment in j[id]:

                data = {
                    'video_id': id,
                    'comment': comment
                }

                res = requests.post(REQUEST_URL.format(TYPE),
                                    data=json.dumps(data),
                                    headers=headers,
                                    cookies=cookies)

                if res.status_code==400:
                    err+=1
                    #print("Error")
                else:
                    cpt+=1
                    #print(res.status_code)
            print(f"complete:{cpt}\terror:{err}")

    if TYPE=="keyword":
        for id in id_list:
            print(f"{id}.. ",end="\n")
            keyword = j[id]

            data = {
                'video_id':id,
                'keyword':keyword
            }

            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)

            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)

    if TYPE=="trending":
        pass




# 일단 보낼 파일 유형 3가지
for p in ["video","comment","keyword"]:
    for fn in listdir(dir):
        if re.match(".*"+p+".json",fn):
            # print(p,fn)
            # if p=="video":
            request_post(FILE=dir+fn, TYPE=p, REQUEST_URL=request_url, headers=headers, cookies=cookies)
