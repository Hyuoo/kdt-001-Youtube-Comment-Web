from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from recent_music_Youtube_URL_Crawling import get_urls
from recent_music_replyscrapper import *
from recent_music_commentary_json_format import *
from os import path

# ===============유튭 URL들 덤핑===================
if not path.exists("./urls.json"):
    recent_urls, recent_imgs, music_urls, music_imgs = get_urls()

    di = {"recent_urls":recent_urls,"recent_imgs":recent_imgs,
          "music_urls":music_urls,"music_imgs":music_imgs}

    save_to_json(data=di,name="./urls.json")


# ===============브라우저 세팅===================
JSON_FILE_NAME = "raw_data/{}_commentary_json_{}"+".json"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR, en_US')
options.add_argument('user-agent=' + user_agent)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
window_size_to_thin(driver)


# ====================url별 스크래핑======================
urls = read_to_json("./urls.json")
data = {}

for category in ["recent", "music"]:
    id_start={"recent":101,"music":201}
    '''
    카테고리별로 url 가져오고 이름부여하여 json포맷 맞게 저장함.
    '''
    print("===={}====".format(category))
    url_count = len(urls[category+"_urls"])

    for id, url, img_src in zip(range(id_start[category],id_start[category]+url_count), urls[category+"_urls"], urls[category+"_imgs"]):
        '''
        한 url(영상하나)에 대해 댓글+기타정보 수집하여
        JSON_FIME_NAME.json에 저장함.
        수집요소: ((이름이 통일이 안됨..))
        category, id, title, img_url, comments,
        frequency, comments_all, url,
        count_of_view, count_of_comment, scrap_count
        '''
        print("progress.. (%d/%d)"%(id-100, url_count))
        print("url :",url)
        if path.exists(JSON_FILE_NAME.format(category,"%03d"%id)):
            print("file is already exist. : ",JSON_FILE_NAME.format(category,"%03d"%id))
            continue

        try:
            commentary = Commentary(driver, url=url, scroll=70, scroll_time=4)
        except:
            print("raised error.. skip file:",JSON_FILE_NAME.format(category,"%03d"%id))
            continue

        commentary_dict = for_dictionary(
            category=category,
            id=id,
            title=commentary.title,
            img_url=img_src,
            comments=commentary.small_contents,
            comments_all=commentary.comments,
            frequency=commentary.get_frequency_for_comments(),
            url=url,
            count_of_view=commentary.count_of_view,
            count_of_comment=commentary.count_of_comment,
            scrap_count=commentary.count_of_crawled,
        )
        print("crawled data ({}/{})\n".format(commentary.count_of_small_content, commentary.count_of_crawled))
        save_to_json(data=commentary_dict,name=JSON_FILE_NAME.format(category,"%03d"%id))




