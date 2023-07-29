'''
카테고리 별 모든 영상 json파일 풀어서
다시 집계해서 워드클라우드 생성...

처음 스크래핑 하는 클래스에서 한번에 했으면 좋았으나
1. Counter 객체를 통째로 저장하는 방법에 문제.
2. 다시 수집하려면 당장의 시간 문제때문에
    이미 수집한 코멘트를 재사용,
'''

from os import path
import json
from konlpy.tag import Hannanum
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

FILE_NAME = "./raw_data/{}_commentary_json_{}.json"

categories = ["recent", "music"]
hannanum = Hannanum()
freq = {}
for category in categories:
    '''
    카테고리별로 단어빈도를 체크
    일단 단어전체 카테고리별로 딕셔너리에 넣고 일괄 처리
    '''
    freq[category] = []
    print(f"{category}_진행중")
    for id in range(101,101+50):
        '''
        모든 영상의 코멘트에서 단어 추출
        '''
        print(id,"..")
        FILE = FILE_NAME.format(category,"%03d"%id)

        if path.exists(FILE):
            with open(FILE,"r") as f:
                j = json.loads(json.load(f))
                nouns_all = []
                for comment in j["comments_all"]:
                    nouns = hannanum.nouns(comment)
                    nouns_all.extend( \
                        [noun for noun in nouns if (
                                len(noun) > 1 and
                                "ㅋㅋ" not in noun and
                                "ㅎㅎ" not in noun and
                                "ㅜㅜ" not in noun and
                                "ㅠㅠ" not in noun
                        )])
                freq[category].extend(nouns_all)

    print(f"{category}_집계완료")
    word = Counter(freq[category])

    wordcloud = WordCloud(font_path = 'malgun',
                          background_color = 'white',
                          height = 2000,
                          width = 2000,
                          contour_width = 100,
                          contour_color = 'black'
                          )
    # 빈도 기반 워드클라우드 이미지 생성
    img = wordcloud.generate_from_frequencies(word)
    plt.figure(figsize = (6, 6))
    plt.tight_layout(pad=0)
    plt.xticks(ticks=[], labels=[])
    plt.yticks(ticks=[], labels=[])
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.imshow(img, interpolation="bilinear")
    plt.savefig('./wordcloud/{}.png'.format(category))
    print(f"{category}_이미지생성완료")
