import requests
from os import path, listdir
import json
import re

def request_post(FILE = "", TYPE="", REQUEST_URL = "", headers={}, cookies={}):
    '''
    :param FILE: FILE_NAME
    :param TYPE: video, comment, keyword
    :param REQUEST_URL:
    :return:
    '''
    print(f"submit progress..")
    print(f" FILE:\t\'{FILE}\'")
    print(f" TYPE:\t{TYPE}")

    j = {}
    id_list = []
    if path.exists(FILE):
        with open(FILE,"r") as f:
            j = json.load(f)

    if isinstance(j, dict):
        id_list = j.keys()
    elif isinstance(j, list):
        id_list = j

    print(f"record count : {len(id_list)}\n")

    if TYPE=="video":
        for id in id_list:
            print(f"{id}.. ",end="")

            thumbnail_url, title, url, count_of_view, count_of_comment = j[id]
            data = {
                'id': id,
                'thumbnail_url': thumbnail_url,
                'title': title,
                'url': url,
                'count_of_view': count_of_view,
                'count_of_comment': count_of_comment,
            }
            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)
            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)

    elif TYPE == "comment":
        for id in id_list:
            print(f"{id}.. ", end="")
            err = 0
            cpt = 0
            for comment in j[id]:
                #print(comment)
                data = {
                    'video_id': id,
                    'comment': comment
                }
                res = requests.post(REQUEST_URL.format(TYPE),
                                    data=json.dumps(data),
                                    headers=headers,
                                    cookies=cookies)
                if res.status_code > 400:
                    print(res.reason)
                    err+=1
                else:
                    cpt+=1
            print(f"complete:{cpt}\terror:{err}")

    elif TYPE=="keyword":
        for id in id_list:
            print(f"{id}.. ",end="\n")
            keyword = j[id]
            #print(type(keyword))
            #print(keyword)
            data = {
                'video_id': id,
                'keyword': keyword
            }
            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)
            print(data)
            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)

    elif TYPE=="category":
        for id, category in id_list:
            print(f"{id}.. ",end="\n")

            data = {
                'id': id,
                'category': category
            }
            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)
            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)

    elif TYPE=="trending":
        for category_id, video_id in id_list:
            print(f"{category_id} {video_id}.. ",end="\n")

            data = {
                'category_id': category_id,
                'video_id': video_id
            }
            res = requests.post(REQUEST_URL.format(TYPE),
                                data=json.dumps(data),
                                headers=headers,
                                cookies=cookies)
            if res.status_code == 400:
                print("Error")
            else:
                print(res.status_code)
    else:
        print("TYPE {} is not supported.".format(TYPE))


headers = {
    "Content-Type":"application/json",
    "X-CSRFToken":"EafFMjAmySk7tMjcN3VhYsf6athHrfyY",
}
cookies = {
    "sessionid":"axiqatufne1ogrvrvxt747cai0ks6vlv",
    "csrftoken":"EafFMjAmySk7tMjcN3VhYsf6athHrfyY"
}

dir = "./youtube_comment_crawling/data/"
fl = listdir(dir)
request_url = "http://127.0.0.1:8000/youtube_comment/load/{}/"
postfix = ["category", "video", "comment", "keyword", "trending"]
#print(fl)
for p in postfix:
    for fn in fl:
        if re.match(".*"+p+".json",fn):
            #print(p,fn)
            request_post(FILE=dir+fn, TYPE=p, REQUEST_URL=request_url, headers=headers, cookies=cookies)