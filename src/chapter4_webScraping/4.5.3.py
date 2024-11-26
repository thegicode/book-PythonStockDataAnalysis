"""
4.5.3 셀트리온 캔들 차트

신버전으로 캔들 차트 그리기
엠피엘파이낸스의 가장 큰 장점은 
OHLC 데이터 칼럼과 인덱스(DatetimeIndex)를 포함한 데이터프레임만 있으면 
기존에 사용자들이 수동으로 처리했던 데이터 변환 작업을 모두 자동화해준다는 것이다.

pip install --upgrade mplfinance

imprt mplfinance as mpf
mpf.plot(OHLC 데이터프레임, [, title=차트제목] [, type=차트형태] [, mav=이동평균선] [, volumne=거래량 표시여부] [, ylabel=y축 레이블])

엠피엘파이낸스 개발자 깃허브
https://github.com/matplotlib/mplfinance
"""

import ssl
import certifi
import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
from io import StringIO
import mplfinance as mpf


ssl_context = ssl.create_default_context(cafile=certifi.where())
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}


# 4.4.3 맨 뒤 페이지 숫자 구하기
url = 'https://finance.naver.com/item/sise_day.naver?code=068270&page=1'

request = Request(url, headers=headers)
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
df = df.dropna()
df = df.iloc[0:30]

# 한글 컬럼명을 영문 컬럼명으로 변경
df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})

# 네이버 데이터는 날짜가 내림차순으로 정렬되어 있으므로, 이를 오름차순으로 변경
df = df.sort_values(by='Date')

# Date 칼럼을 DatetimeIndex형으로 변경한 후 인덱스로 설정
df.index = pd.to_datetime(df.Date)

# Open, Hight, Low, Close, Volume 칼럼만 갖도록 데이터프레임 구조 변경
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]


# 엠피엘파이낸스로 캔들 차트 그리기
# mpf.plot(df, title='Celltrion candle chart', type='candle')
# mpf.plot(df, title='Celltrion candle chart', type='ohlc')


# kwargs는 keywrod argynebts의 약자, mpf.plot() 함수를 호출할 때 쓰이는 여러 인수를 담은 딕셔너리
kwargs = dict(title='Celltrion cutomized chart', type='candle', mav=(2, 4, 6), volume=True, ylabel='ohlc candles')

# 마켓 색상은 스타일을 지정하는 필수 객체로서, 상승은 빨간색, 하락은 파란색으로 지정, 관련 색상은 이를 따로도록 한다.
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)

# 마켓 색상을 인수로 넘겨줘서 스타일 객체를 생성한다.
s = mpf.make_mpf_style(marketcolors=mc)

# 셀트리온 시세 OHLC 데이터와 kwargs로 설정한 인수들과 스타일 객체를 인수로 넘겨주면서 mpf.plot() 함수를 호출하여 차트를 출력한다. 
mpf.plot(df, **kwargs, style=s)