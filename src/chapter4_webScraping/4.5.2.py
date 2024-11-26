"""
4.5 OHLC와 캔들 차트
OHLC : Open - High - Low - Close, 시가 - 고가 - 저가 - 종가

4.5.2 셀트리온 종가 차트
셀트리온 종가 차트 : 셀트리온의 최근 30개 종가 데이터를 이용하여 차트로 표시
보통 일주일에 5일 개장하므로 약 한 달 반 정도 데이터
x축은 날짜 칼럼, y축은 종가 칼럼 차트
종가 그래프로는 한 달 반 동안의 종가 흐름을 파악할 수 있으나, 일자별 변동폭을 파악하기 어렵다.

"""

import ssl
import certifi
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import requests
from io import StringIO


ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}


# 4.4.3 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.naver?code=068270&page=1'

request = Request(url, headers=headers)
# URL 요청
with urlopen(request, context=ssl_context) as response:
    html = BeautifulSoup(response, 'lxml')
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]  # 마지막 페이지 번호 가져오기




# 4.4.4 전체 페이지 읽어오기
sise_url = 'https://finance.naver.com/item/sise_day.naver?code=068270'
data_frames = []
for page in range(1, int(last_page) + 1):
    page_url = f'{sise_url}&page={page}'
    page_response = requests.get(page_url, headers=headers, verify=certifi.where())
    html_string_io = StringIO(page_response.text)
    tables = pd.read_html(html_string_io, header=0)  
    data_frames.append(tables[0])
df = pd.concat(data_frames, ignore_index=True)

# 차트 출력을 위해 데이터프레임 가공하기
df = df.dropna().reset_index(drop=True)
df = df.iloc[0:30]
df = df.sort_values(by='날짜')



# 날짜, 종가 칼럼으로 차트 그리기
plt.title('Celltrion (close)')

# x축 레이블의 날짜가 겹쳐서 보기에 어려우므로 90도로 회전하여 표시
plt.xticks(rotation=45) 

# x축 날짜 데이터, y축 종가 데이터, co 좌표를 청록색 원으로, - 좌표를 실선으로
plt.plot(df['날짜'], df['종가'], 'co-') 

plt.grid(color='gray', linestyle='--')
plt.show()