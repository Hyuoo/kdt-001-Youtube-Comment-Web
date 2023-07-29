'''
하나의 유튜브 url에서 (하나의영상)
제목, 조회수, 댓글수, 댓글을 수집하는 클래스

클래스 내에서 위 데이터들 멤버변수 형태로 접근하여 사용

빈도계산을 처음 여기서 하긴 했는데 이후 사용못하게되어 제거가 필요함,
일부댓글만 가져오는 부분도 수정이 필요
-> 일부 댓글만 가져오는게
    모든 댓글을 손실없이 가져오려고하면 이상이 있어서
    중복이 있더라도 다 가져온 뒤 set연산을 통해 중복제거를 하려 해서
    상위 댓글을 따로 수집하는것이 좋다고 판단했으나
    손실이 어느정도 있어도 그냥 수집하기로 하면서 필요없는 부분이 됨. 
'''

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from collections import Counter
from konlpy.tag import Hannanum


def window_size_to_thin(driver):
    '''
    유튜브 창 크기에 따라 레이아웃이 변해서
    좌우로 얇은 레이아웃이 크롤링에 유용하다고 판단
    '''
    driver.maximize_window()
    driver.set_window_size("700", driver.get_window_size()["height"])


class Commentary():
    '''
    title            : str   (제목)
        -> .title
    count_of_views   : int   (조회수)
        -> .count_of_view
    comments         : list  (샘플댓글리스트)
        -> .comments
    count_of_comment : int   (전체댓글수)
        -> .count_of_comment
    scrap_count      : int   (샘플댓글수)
        -> .count_of_crawled
    small_contents   : list  (순서있는댓글리스트)
        -> .small_contents
    scrap_count_small: int   (스몰콘텐츠 수)
        -> .count_of_small_content

    위 thin함수 실행 후 (좌우얇은브라우저)
    driver와 url 주고 Commentary호출하면 끝.
    '''
    def __init__(self, driver, url="", short=1, scroll=3, scroll_time=0.7):
        '''
        드라이버 받아서 각 요소 생성하고,
        드라이버 None으로 할당.
        :param shrot: 순서있는 댓글수집 범위(스크롤)
        :param scroll: 총 스크롤 횟수
        :param scroll_time: 스크롤 사이 시간간격
        '''
        # scroll_once 후 대기시간 (second)
        self.SCROLL_WAIT_TIME = scroll_time
        # scroll_once 실행 횟수
        self.MAX_SCROLL_TIME = scroll
        self.PRECRAWL = short

        self.driver = driver
        self.url = url
        self.title = ""
        self.count_of_view = 0
        self.small_contents = []
        self.count_of_small_content = 0
        self.comments = []
        self.count_of_comment = 0
        self.count_of_crawled = 0

        if url:
            self.driver.get(self.url)
            time.sleep(3)
            self.title = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1').text
            self.deo_bogi()
            self.count_of_view = self.get_count_of_views()
            self.scroll_once()
            time.sleep(2)
            # 댓글사용 중지 시 나타나는 element로 했는데 에러가 빈번해서 try except로 처리함.
            # if len(driver.find_elements(By.XPATH,'//*[@id="message"]'))==0:
            try:
                self.count_of_comment = self.get_count_of_comments()

                print("get_comments..", end=" ")
                print(self.count_of_comment)
                self.comments = self.preprocess_comment_elements(self.get_elements())
                self.small_contents = self.preprocess_comment_elements(self.small_contents)
                self.count_of_small_content = len(self.small_contents)
                self.count_of_crawled = len(self.comments)
            except:
                print("댓글이 사용 중지되었습니다.")
                self.comments = ["댓글이 사용 중지되었습니다."]
        self.driver = None

    def __str__(self):
        if self.url=="":
            return None
        title = self.title
        views = self.count_of_view
        count_of_comment = self.count_of_comment
        crawled = self.count_of_crawled
        comments = self.comments[:5]

        # 하드코딩으로 01 댓글표시 유무 설정..
        f = 0
        if f:
            return "{} 조회수 ({}), 댓글수 ({}), 샘플링수 ({}):\ncomments:\n{}"\
                    .format(title, views, count_of_comment, crawled, "\n".join(comments))
        else:
            return "{} 조회수 ({}), 댓글수 ({}), 샘플링수 ({})"\
                    .format(title, views, count_of_comment, crawled)

    # konlpy까지 할 경우
    def is_instance(self):
        return (self.title!="" and self.url!="" and len(self.comments)!=0)

    # konlpy까지 할 경우
    def get_frequency_for_comments(self):
        if not self.is_instance():
            return None
        hannanum = Hannanum()
        print("빈도계산중:",len(self.comments))
        nouns_all = []
        for comment in self.comments:
            nouns = hannanum.nouns(comment)
            nouns_all.extend([noun for noun in nouns if (len(noun)>1 and "ㅋㅋ"not in noun and "ㅎㅎ"not in noun)])
        return Counter(nouns_all)

    def deo_bogi(self):
        '''
        페이지 로드 후 더보기 버튼 누름
        -> 눌러야 조회수 잘보임.. 안누르면 약식표기
        '''
        button = self.driver.find_element(By.XPATH,'//*[@id="snippet"]')
        ActionChains(self.driver).click(button).perform()
        time.sleep(0.2)

    def get_count_of_views(self):
        '''
        조회수 따오기
        '''
        tmp = self.driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
        views = tmp.split()[1][:-1].replace(",","")
        return int(views)

    def get_count_of_comments(self):
        '''
        전체 댓글 수 가져오기
        페이지 한번 내리고나서 할 것
        '''
        tmp = self.driver.find_element(By.XPATH,'//*[@id="count"]/yt-formatted-string/span[2]').text
        tmp = tmp.replace(",", "")
        return int(tmp)

    def scroll_once(self):
        '''
        스크롤 한번 밑으로 내리기
        *내린 뒤 로딩시간 필요
        '''
        # 바닥까지 스크롤링 방법 두개
        # self.driver.find_element(By.TAG_NAME, "body").send_keys("\ue010")
        self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(self.SCROLL_WAIT_TIME)

    def preprocess_comment_elements(self,elements):
        '''
        element상태의 댓글내용 리스트 가져와서
        .text 전환 후
        전처리해서 다시 리턴
        '''
        comments = []
        for element in elements:
            comment = element.text
            comment = comment \
                .replace("𝐏𝐥𝐚𝐲𝐥𝐢𝐬𝐭", "playlist") \
                .replace("\n", " ") \
                .replace("\t", " ") \
                .replace("\r", " ") \
                .strip()
            comments.append(comment)
        return comments

    def get_elements(self):
        '''
        self.url 에서 댓글"만" 긁어오기
        comments:list
        '''
        if not self.driver:
            return

        scrolling = self.MAX_SCROLL_TIME
        last_height = 0
        precrawl = self.PRECRAWL

        while 1:
            scrolling -= 1
            precrawl -= 1
            self.scroll_once()
            now_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            # 필요없어진 부분
            if precrawl==0:
                self.small_contents = self.driver.find_elements(By.ID, "content-text")
            if now_height == last_height or scrolling==0:
                break
            last_height = now_height

        elements = self.driver.find_elements(By.ID, "content-text")
        return elements
