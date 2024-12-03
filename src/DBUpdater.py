import calendar
from io import StringIO
import json
import os
import ssl
from threading import Timer
import warnings
from bs4 import BeautifulSoup
import certifi
import pymysql
import pandas as pd
from datetime import datetime 
import requests
from sqlalchemy import create_engine
from urllib.request import urlopen, Request
from threading import Timer

# HTTPS 경고 무시 설정 - 테스트 환경
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.timer = None  # Timer 객체를 저장
        self.shutting_down = False  # 종료 상태를 나타내는 플래그
        
        self.conn = pymysql.connect(host='localhost', user='root', 
                                    password='code', db='Investar', charset='utf8')
        
        # SQLAlchemy 엔진 생성
        self.engine = create_engine('mysql+pymysql://root:code@localhost/Investar')
        
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
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
        print("self.codes: ")
        print(self.codes)
        # self.update_comp_info()


    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()
        self.engine.dispose()


    def read_krx_code(self, test_mode=False, stocks=None):
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        response = requests.get(url, verify=False)  # 인증서 검증 비활성화
        response.raise_for_status()  # HTTP 오류 확인
        html = StringIO(response.text)  # StringIO로 감싸기
        krx = pd.read_html(html, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드':'code', '회사명':'company'})
        krx.code = krx.code.map(lambda x: f"{x:06d}")

        # stocks 리스트가 주어진 경우 필터링
        if stocks:
            krx = krx[krx['company'].isin(stocks)]

        if test_mode == True:
            krx = krx.head(5) # 테스트 

        return krx
    

    def update_comp_info(self, test_mode=False, stocks=None):
        print("* update_comp_info")

        """종목코드를 company_info 테이블에 업데이트한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.engine)  # SQLAlchemy 엔진 사용
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()
            today = datetime.today().strftime('%Y-%m-%d')

            if rs[0] is None or rs[0].strftime('%Y-%m-%d') < today:
                krx = self.read_krx_code(test_mode=test_mode, stocks=stocks)
                
                print("krx\n", krx)

                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"""
                    REPLACE INTO company_info (code, company, last_update)
                    VALUES ('{code}', '{company}', '{today}')
                    """
                    curs.execute(sql)
                    self.codes[code] = company
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO company_info VALUES({code}, {company}, {today})")
                self.conn.commit()
                print('')

    
    def read_naver(self, code, company, pages_to_fetch, test_mode=False):
        print("\n * read_naver", code, company, pages_to_fetch)

        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""
        try:
            # SSL 인증서 검증 비활성화
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
            
            url = f'https://finance.naver.com/item/sise_day.naver?code={code}'
            request = Request(url, headers=headers)
            
            with urlopen(request, context=ssl_context) as response:
                html = BeautifulSoup(response, 'lxml')
                pgrr = html.find('td', class_='pgRR')
                if pgrr is None:
                    print("pgrr is None")
                    return None
                s = str(pgrr.a['href']).split('=')
                lastpage = s[-1]  # 마지막 페이지 번호 가져오기

            data_frames = []
            pages = min(int(lastpage), pages_to_fetch)

            if test_mode == True:
                pages = 10 

            for page in range(1, pages + 1):
                page_url = f'{url}&page={page}'
                page_response = requests.get(page_url, headers=headers, verify=certifi.where())
                html_string_io = StringIO(page_response.text)
                tables = pd.read_html(html_string_io, header=0)  
                data_frames.append(tables[0])
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print(f'[{tmnow}] {company} ({code}) : {page:04d}/{pages:04d} pages are downloading... \r')
            
            df = pd.concat(data_frames, ignore_index=True)
            df = df.rename(columns={
                '날짜': 'date', '종가': 'close', '전일비': 'diff',
                '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'
            })
            df['date'] = df['date'].replace('.', '-')
            df = df.dropna()

            # 'diff' 열 클리닝
            df['diff'] = df['diff'].astype(str).str.replace(r'[^\d-]', '', regex=True).replace('', '0').astype(int)

            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]

        except Exception as e:
            print("Exception occurred in read_naver:", str(e))
            return None
        
        return df


    def replace_into_db(self, df, num, code, company):
        print("\n * replace_into_db")

        """네이버 금융에서 읽어온 주식 시세를 DB에 REPLACE"""
        with self.conn.cursor() as curs:
            # 1. 인수로 넘겨받은 데이터프레임을 튜플로 순회처리한다. 
            for r in df.itertuples():
                sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})"
                # 2. REPLACE INTO 구문으로 daily_price 테이블을 업데이트한다.
                curs.execute(sql)
            # 3. commit() 함수를 호출해 마리아디비에 반영한다.
            self.conn.commit()
            print('[{}] #{:04d} {} {} : {} rows > REPLCACE INTO daily_'\
                  'price [OK]'.format(datetime.now().strftime('%Y-%m-%d'\
                                                              ' %H:%M'), num+1, company, code, len(df)))


    def update_daily_price(self, pages_to_fetch, test_mode=False):
        print("\n * update_daily_price", "pages_to_fetch:", pages_to_fetch)

        """KRX 상장법인의 주식 시레를 네이버로부터 읽어서 DB에 업데이트"""
        # 1 self.codes 딕셔너리에 저장된 모든 종목코드에 대해 순회처리한다.

        for idx, code in enumerate(self.codes):
            # 2. read_naver() 메서드를 이용하여 종목코드에 대한 일별 시세 데이터 프레임을 구한다.
            df = self.read_naver(code, self.codes[code], pages_to_fetch, test_mode=test_mode)
            if df is None:
                continue

            # 3. 일별 시세 데이터프레임이 구해지면 reaplreplace_into_db() 메서드로 DB에 저장한다.
            self.replace_into_db(df, idx, code, self.codes[code])


    def execute_daily(self, test_mode=False, stocks=None):
        print("\n* execute_daily")
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""

        # 종료 상태 확인
        if self.shutting_down:
            print("Shutting down. Timer execution halted.")
            return

        # 1. update_comp_info() 메서드를 호출하여 상장 법인 목록을 DB에 업데이트한다.
        self.update_comp_info(test_mode=test_mode, stocks=stocks)

        config_path = './src/config.json'
        try:
            # 2. DBUpdater.py가 있는 디렉터리에서 config.json 파일을 읽기 모드로 연다.
            with open(config_path, 'r') as in_file:
                config = json.load(in_file)
                # 3.  파일이 있다면 pages_to_fetch값을 읽어서 프로그램에서 사용
                pages_to_fetch = config['pages_to_fetch']
        # 4. 1에서 열려고 시도했던 config.json 파일이 존재하지 않는 경우
        except FileNotFoundError:
            # 5. 최초 실행 시 프로그램에서 사용할 pages_to_fetch값을 100으로 설정한다. 
            # (config.json 파일에 pages_to_fetch값을 1로 저장해서 이후부터는 1페이지씩 읽음).
            pages_to_fetch = 100
            config = {'pages_to_fetch': 1}
            with open(config_path, 'w') as out_file:
                json.dump(config, out_file)

        # 6. pages_to_fetch 값으로 update_daily_price() 메서드를 호출
        self.update_daily_price(pages_to_fetch, test_mode=test_mode)

        # 다음 실행 시간 계산
        tmnow = datetime.now()
        # 7. 이번 달의 마지막 날(lastday)을 구해 다음 날 오후 5시를 계산하는 데 사용
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year + 1, month=1, day=1, hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month + 1, day=1, hour=17, minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day + 1, hour=17, minute=0, second=0)

        tmdiff = tmnext - tmnow
        secs = tmdiff.total_seconds()

        if test_mode:
                secs = 3

        # 8. 다음 날 오후 5시에 execute_daily() 메서드를 실행하는 타이머(Timer) 객체를 생성한다.
        # 종료 상태 확인 후 Timer 생성
        if not self.shutting_down:
            self.timer = Timer(secs, self.execute_daily, [test_mode])  # test_mode 전달
            print(f"Waiting for next update ({tmnext.strftime('%Y-%m-%d %H:%M') if not test_mode else 'in 3 seconds'}) ...")
            self.timer.start()


    def stop(self):
        """종료 처리를 위해 Timer 중지"""
        self.shutting_down = True  # 종료 상태 설정
        if self.timer and self.timer.is_alive():
            self.timer.cancel()  # 실행 중인 Timer 중지
            print("Timer cancelled.")


def reset_config(config_path='./src/chapter5_marketData/config.json'):
    """
    config.json 파일 초기화 함수.
    파일이 존재하면 기본값으로 덮어쓰고, 없으면 새로 생성.
    """
    default_config = {
        "pages_to_fetch": 100  # 기본값 설정
    }
    
    try:
        # 파일이 존재하면 삭제
        if os.path.exists(config_path):
            os.remove(config_path)
            print(f"기존 {config_path} 파일 삭제 완료.")
        
        # 기본값으로 새 파일 생성
        with open(config_path, 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
            print(f"{config_path} 파일 초기화 완료. 기본값으로 설정됨: {default_config}")
    except Exception as e:
        print("config.json 초기화 중 오류 발생:", str(e))


def reset_test_environment(dbu, config_path='./src/chapter5_marketData/config.json'):
    """
    테스트를 위한 초기화 함수.
    - 데이터베이스 테이블 초기화
    - config.json 초기화
    """
    # 데이터 초기화
    with dbu.conn.cursor() as curs:
        print("테이블 초기화 중...")
        curs.execute("DELETE FROM company_info")
        curs.execute("DELETE FROM daily_price")
        dbu.conn.commit()
        print("테이블 초기화 완료.")
    
    # config.json 초기화
    print("config.json 초기화 중...")
    reset_config(config_path)
    print("config.json 초기화 완료.")



if __name__ == '__main__':
    # DBUpdater 객체 생성 -> DBUpdater의 생성자 내부에서 마라아디비 연결
    dbu = DBUpdater()

    test_mode = False

    stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER', '엔씨소프트']

    # 테스트 위한 초기화
    # reset_test_environment(dbu)

    # company_info 테이블에 오늘 업데이트된 내용이 있는지 확인하고 
    # 없으면 read_krx_code를 호출하여 company_info 테이블에 업데이트하고 codes 딕셔너리에도 저장
    try:
        dbu.execute_daily(test_mode=test_mode, stocks=stocks)
    except KeyboardInterrupt:
        print("\nShutdown signal received. Cleaning up...")
        dbu.stop()
        print("Exiting program.")


 