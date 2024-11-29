import calendar
from io import StringIO
import json
import os
import ssl
from threading import Timer
import threading
import warnings
from bs4 import BeautifulSoup
import pymysql
import pandas as pd
from datetime import datetime
import requests
from sqlalchemy import create_engine
from urllib.request import urlopen
import atexit

# HTTPS 경고 무시 설정 - 테스트 환경
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.timer = None  # Timer 객체를 저장
        self.shutting_down = False  # 종료 상태를 나타내는 플래그
        atexit.register(self.stop)  # 프로그램 종료 시 안전한 중지 처리 등록

        self.conn = pymysql.connect(host='localhost', user='root',
                                    password='code', db='Investar', charset='utf8')
        # SQLAlchemy 엔진 생성
        self.engine = create_engine('mysql+pymysql://root:code@localhost/Investar')
        # 테이블 생성
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS compnay_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
        self.conn.commit()
        self.codes = dict()
        print("self.codes initialized: ", self.codes)

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def stop(self):
        """종료 처리를 위해 Timer 중지"""
        self.shutting_down = True  # 종료 상태 설정
        if self.timer and self.timer.is_alive():
            self.timer.cancel()  # 실행 중인 Timer 중지
            print("Timer cancelled.")

    def read_krx_code(self):
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        response = requests.get(url, verify=False)  # 인증서 검증 비활성화
        response.raise_for_status()  # HTTP 오류 확인
        html = StringIO(response.text)  # StringIO로 감싸기
        krx = pd.read_html(html, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        krx.code = krx.code.map(lambda x: f"{x:06d}")
        return krx

    def update_comp_info(self):
        print("* update_comp_info")

        sql = "SELECT * FROM compnay_info"
        df = pd.read_sql(sql, self.engine)  # SQLAlchemy 엔진 사용
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM compnay_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] is None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code()
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"""
                    REPLACE INTO compnay_info (code, company, last_update)
                    VALUES ('{code}', '{company}', '{today}')
                    """
                    curs.execute(sql)
                    self.codes[code] = company
                self.conn.commit()
                print(f"Updated compnay_info with {len(krx)} records.")

    def read_naver(self, code, company, pages_to_fetch):
        print("\n * read_naver", code, company, pages_to_fetch)
        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            url = f'https://finance.naver.com/item/sise_day.naver?code={code}'
            context = ssl._create_unverified_context()

            with urlopen(url, context=context) as doc:
                html = BeautifulSoup(doc, 'lxml')
                pgrr = html.find("td", class_="pgRR")
                if pgrr is None:
                    return None
                lastpage = int(str(pgrr.a['href']).split('=')[-1])

            df = pd.DataFrame()
            pages = min(lastpage, pages_to_fetch)
            for page in range(1, pages + 1):
                pg_url = f'{url}&page={page}'
                df = pd.concat([df, pd.read_html(pg_url, header=0)[0]])
            df = df.rename(columns={
                '날짜': 'date', '종가': 'close', '전일비': 'diff',
                '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'
            })
            df['date'] = df['date'].str.replace('.', '-')
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
            return df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
        except Exception as e:
            print("Exception occurred:", str(e))
            return None

    def update_daily_price(self, pages_to_fetch):
        print("\n * update_daily_price", f"pages_to_fetch: {pages_to_fetch}")
        for idx, code in enumerate(self.codes):
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            if df is None:
                continue
            with self.conn.cursor() as curs:
                for row in df.itertuples():
                    sql = f"""
                    REPLACE INTO daily_price (code, date, open, high, low, close, diff, volume)
                    VALUES ('{code}', '{row.date}', {row.open}, {row.high}, {row.low}, {row.close}, {row.diff}, {row.volume})
                    """
                    curs.execute(sql)
                self.conn.commit()
            print(f"Updated daily_price for {self.codes[code]} ({code})")

    def execute_daily(self, test_mode=False):
        print("\n* execute_daily")

        # 종료 상태 확인
        if self.shutting_down:
            print("Shutting down. Timer execution halted.")
            return

        # 업데이트 작업 실행
        self.update_comp_info()
        self.update_daily_price(100)

        # 다음 실행 시간 계산
        # tmnow = datetime.now()
        # lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        # if test_mode:
        #     secs = 3
        #     print("Test mode enabled. Executing every 3 seconds.")
        # else:
        #     tmnext = tmnow.replace(day=tmnow.day + 1, hour=17, minute=0, second=0) if tmnow.day < lastday else tmnow.replace(
        #         month=tmnow.month + 1 if tmnow.month < 12 else 1,
        #         year=tmnow.year + 1 if tmnow.month == 12 else tmnow.year,
        #         day=1, hour=17, minute=0, second=0
        #     )
        #     secs = (tmnext - tmnow).total_seconds()

        # # 타이머 생성 전에 기존 타이머 상태 확인 및 종료 상태 확인
        # if self.timer and self.timer.is_alive():
        #     self.timer.cancel()

        # # 인터프리터 종료 상태를 추가로 확인
        # if not self.shutting_down and threading.main_thread().is_alive():
        #     self.timer = Timer(secs, self.execute_daily, [test_mode])
        #     self.timer.start()
        #     print(f"Waiting for next update ({'in 3 seconds' if test_mode else 'at 17:00'}) ...")
        # else:
        #     print("Main thread is shutting down, skipping timer creation.")


def reset_config(config_path='./config.json'):
    if os.path.exists(config_path):
        os.remove(config_path)
    with open(config_path, 'w') as f:
        json.dump({"pages_to_fetch": 100}, f)


if __name__ == '__main__':
    dbu = DBUpdater()
    try:
        dbu.execute_daily(test_mode=True)
    except KeyboardInterrupt:
        dbu.stop()
        print("Stopped by user.")
