import hashlib
import json
import time
# selenium으로부터 webdriver 모듈을 불러옵니다.
from selenium import webdriver
from selenium.webdriver.common.by import By
# Explicit Wait을 위해 추가
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
json_format = '{}.json'


def category_id_gen(input_str):
    m = hashlib.md5()
    m.update(input_str.encode())
    return str(int(m.hexdigest(), 16))[1:13]


def get_video_id(url):
    video_id = ""
    if url is not None:
        idx = url.find("?v=")
        return url[idx+3:]
    return video_id

def get_categories(url, file_format=None, postfix='category', wait_time=10):
    if file_format is not None:
        file_path = file_format.format(postfix)
    links = []
    categories = []
    with webdriver.Chrome(options=options) as driver:
        #크롬 드라이버에 url 주소 넣고 실행
        driver.get(url)
        element = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab')))

        tabs = driver.find_elements(By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab')
        for tab in tabs:
            category_name = tab.find_element(By.CLASS_NAME, 'tab-title').text
            # category table 데이터 수집
            category_id = category_id_gen(category_name)
            categories.append([category_id, category_name])
            # 해당 tab으로 이동
            tab.click()
            time.sleep(5)
            links.append([category_id, driver.current_url])
    if file_path is not None:
        with open(file_path, 'w') as f:
            json.dump(categories, f)
    return links


def get_trending(category_id, category_url, file_format=None, postfix='trending', wait_time=10):
    if file_format is not None:
        file_path = file_format.format(category_id+'_'+postfix)
    with webdriver.Chrome(options=options) as driver:
        driver.get(category_url)
        driver.implicitly_wait(wait_time)

        # 페이지 스크롤 다운 (모든 동영상 로딩)
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(5)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            time.sleep(1.5)
            # 팝업 제거
            try:
                driver.find_element_by_css_selector('#dismiss-button > a').click()
            except:
                pass

        # 모든 동영상 (쇼츠 제외) 링크, 제목 수집
        video_links = []
        for video in driver.find_elements(By.XPATH, "//a[@id='video-title']"):
            if video.get_attribute is not None and 'shorts' not in video.get_attribute('href'):
                print(video.get_attribute("href"))
                video_id = get_video_id(video.get_attribute("href"))
                print(video_id)
                video_links.append([category_id, video_id])
    if file_path is not None:
        with open(file_path, 'w') as f:
            json.dump(video_links, f)
    return video_links


if __name__ == "__main__":
    base_url = './youtube_comment_crawling/data/'
    youtube_url = 'https://www.youtube.com/feed/trending'
    # category 데이터 저장
    category_urls = get_categories(youtube_url, base_url + json_format)
    # trending 데이터 저장
    trending_path = base_url + json_format.format('trending')
    for category_id, category_url in category_urls:
        links = get_trending(category_id, category_url, base_url + json_format)