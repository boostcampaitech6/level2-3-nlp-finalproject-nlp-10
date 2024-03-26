from bs4 import BeautifulSoup as bs
import requests

import pandas as pd

news = pd.read_csv("/content/drive/MyDrive/level2-boostcamp-team10/level3/뉴스데이터/병합/news_total_ver1.csv")
news.head()

def get_news_first_image_source_link(news_url):

    # requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
    response = requests.get(news_url)

    # 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
    html_text = response.text

    # html을 잘 정리된 형태로 변환
    html = bs(html_text, 'html.parser')

    try : # 'img' 태그 찾기
        img_tag = html.select_one('span.end_photo_org > div > div > img')
          # 'data-src' 속성 값 추출
        img_url = img_tag['data-src'] if img_tag else 'Image URL not found'
    except :
        img_url = 'Image URL not found'

    return img_url


## 실제로 돌려보고 싶으면 아래를 실행해보면 됨
test_news = news[:10]
test_news['image_url'] = 'None'

for i, news_url in enumerate(test_news['url'].tolist()):
    img_url = get_news_first_image_source_link(news_url)
    test_news.loc[i, 'image_url'] = img_url

print(test_news.head(10))

from IPython.display import Image, display

# 이미지 웹 주소
image_url = '여기에 이미지 웹 주소를 입력하세요'

# 이미지 보여주기
display(Image(url=test_news.loc[1, 'image_url']))

# 이미지 보여주기
display(Image(url=test_news.loc[9, 'image_url']))

