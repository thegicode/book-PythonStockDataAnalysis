"""
4.4 뷰티풀 수프로 일별 시세 읽어오기

접근 권한이 있는 저작권 자료를 스크레핑해서 분석 목적으로 사용하는 것은 괜찮지만, 
원저작자의 허가를 받지 않고 자신의 웹에 게시하거나 다른 사람이 다운로드하도록 공유하면 안 된다. 
또한 잦은 웹 스크레이핑으로 상대방 시스템 성능에 지장을 주는 경우도 문제가 될  수 있으니, 
합법적으로 허용되는 범위가 어디까지인지 반드시 확인한 후  웹 스크레이핑을 수행하기 바란다.

4.4.2 find_all() 함수와 find() 함수 비교
find_all(['검색할 태그'][, class_='클래스 속성값'][, id='아이디 속성값'][, limit=찾을 개수])
find(['검색할 태그'][, class_='클래스 속성값'][, id='아이디 속성값'])
"""

import ssl
import certifi
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

import ssl
import certifi
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import requests
from io import StringIO

# SSL 인증서 강제 설정
ssl_context = ssl.create_default_context(cafile=certifi.where())

# 기본 URL
sise_url = 'https://finance.naver.com/item/sise_day.naver?code=068270'

# User-Agent 추가
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
request = Request(sise_url, headers=headers)

# URL 요청
with urlopen(request, context=ssl_context) as response:
    html = BeautifulSoup(response, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]  # 마지막 페이지 번호 가져오기


# 데이터를 저장할 리스트
data_frames = []

for page in range(1, int(last_page) + 1):
    page_url = f'{sise_url}&page={page}'
    # requests로 데이터 가져오기
    page_response = requests.get(page_url, headers=headers, verify=certifi.where())
    # StringIO로 HTML을 래핑
    html_string_io = StringIO(page_response.text)
    tables = pd.read_html(html_string_io, header=0)  # HTML에서 테이블 읽기
    data_frames.append(tables[0])

# 모든 페이지 데이터를 하나의 DataFrame으로 병합
df = pd.concat(data_frames, ignore_index=True)

# 결측치 제거
df = df.dropna().reset_index(drop=True)

print(df)
