from io import StringIO
import warnings
import pymysql
import pandas as pd
from datetime import datetime 
import requests
from sqlalchemy import create_engine

# HTTPS 경고 무시 설정 - 테스트 환경
warnings.filterwarnings("ignore", message="Unverified HTTPS request")


class DBUpdater:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root', 
                                    password='code', db='Investar', charset='utf8')
        
        # SQLAlchemy 엔진 생성
        self.engine = create_engine('mysql+pymysql://root:code@localhost/Investar')
        
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

        self.update_comp_info()


    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

    def read_krx_code(self):
        """KRX로부터 상장법인목록 파일을 읽어와서 데이터프레임으로 변환"""
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'
        response = requests.get(url, verify=False)  # 인증서 검증 비활성화
        response.raise_for_status()  # HTTP 오류 확인
        html = StringIO(response.text)  # StringIO로 감싸기
        krx = pd.read_html(html, header=0)[0]
        krx = krx[['종목코드', '회사명']]
        krx = krx.rename(columns={'종목코드':'code', '회사명':'company'})
        krx.code = krx.code.map('{:06d}'.format)
        return krx

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트한 후 딕셔너리에 저장"""
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
                    tmnow = datetime.now().strftime('%Y-%m-%d')
                    print(f"[{tmnow}] {idx:04d} REPLACE INTO compnay_info VALUES({code}, {company}, {today})")
                self.conn.commit()
                print('')

    
    def read_naver(self, code, company, pages_to_fetch):
        """네이버 금융에서 주식 시세를 읽어서 데이터프레임으로 반환"""

    def replace_into_db(self, df, num, code, company):
        """네이버 금융에서 읽어온 주식 시세를 DB에 REPLACE"""

    def update_daiyl_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시레를 네이버로부터 읽어서 DB에 업데이트"""
    
    def execute_daily(self):
        """실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""


if __name__ == '__main__':
    # DBUpdater 객체 생성 -> DBUpdater의 생성자 내부에서 마라아디비 연결
    dbu = DBUpdater()

    # # 데이터 초기화
    # with dbu.conn.cursor() as curs:
    #     print("초기화 중...")
    #     curs.execute("DELETE FROM compnay_info")
    #     curs.execute("DELETE FROM daily_price")
    #     dbu.conn.commit()
    #     print("데이터 초기화 완료.")
    
    # # 코드 재실행 테스트
    # dbu.update_comp_info()
    # print("종목코드 업데이트 완료!")

    # compnay_info 테이블에 오늘 업데이트된 내용이 있는지 확인하고 
    # 없으면 read_krx_code를 호출하여 compnay_info 테이블에 업데이트하고 codes 딕셔너리에도 저장
    dbu.execute_daily()

 