'''
팀원 김태준 님 소스코드 활용
카테고리 메인에서 영상 별 url수집하는 코드
- recent, music
수집 내용
- 영상url, 썸네일url
'''

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import warnings

def get_urls():
    warnings.filterwarnings('ignore')
    warnings.filterwarnings(action = 'ignore')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    url = "https://www.youtube.com/feed/trending"
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920*1080')
    options.add_argument('--disable-gpu')
    options.add_argument('lang=ko_KR, en_US')
    options.add_argument('user-agent=' + user_agent)


    def recent_check_url():
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.implicitly_wait(3)

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
        title_list = []
        for video in driver.find_elements(By.XPATH, "//a[@id='video-title']"):
            if video.get_attribute is not None and 'shorts' not in video.get_attribute('href'):
                video_links.append(video.get_attribute("href"))
                title_list.append(video.text.strip())

        video_links = video_links[:50]
        title_list = title_list[:50]

        # 썸네일 이미지 가져오기
        thumbnails = []
        for video_link in video_links:
            driver.get(video_link)
            thumbnail = driver.find_element(By.XPATH, "//meta[@property='og:image']")
            thumbnails.append(thumbnail.get_attribute('content'))

        thumbnails = thumbnails[:50]
        return video_links, title_list, thumbnails


    def music_check_url():
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.implicitly_wait(3)

        # 카테고리별 클릭 버튼 추가하기 해당 class name 찾고 (영화)
        # 영화 버튼 클릭하기
        music_button = driver.find_element(By.XPATH, '//*[@id="tabsContent"]/tp-yt-paper-tab[2]/div/div[1]')
        ActionChains(driver).click(music_button).perform()

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
        title_list = []
        for video in driver.find_elements(By.XPATH, "//a[@id='video-title']"):
            if video.get_attribute is not None and 'shorts' not in video.get_attribute('href'):
                video_links.append(video.get_attribute("href"))
                title_list.append(video.text.strip())

        # 썸네일 이미지 가져오기
        thumbnails = []
        for video_link in video_links:
            driver.get(video_link)
            thumbnail = driver.find_element(By.XPATH, "//meta[@property='og:image']")
            thumbnails.append(thumbnail.get_attribute('content'))

        return video_links, title_list, thumbnails

    recent_results = recent_check_url()
    recent_urls, recent_thumbnail_urls = recent_results[0], recent_results[2]

    music_results = music_check_url()
    music_urls, music_thumbnail_urls = music_results[0], music_results[2]

    return [recent_urls, recent_thumbnail_urls, music_urls, music_thumbnail_urls]
