
import re
import pymysql
from datetime import datetime, timedelta 
import pandas as pd
from sqlalchemy import create_engine

class MarketDB:
    def __init__(self):
        """생성자: MarketDB 연결 및 종목코드 딕셔너리 생성"""
        self.conn = pymysql.connect(host='localhost', user='root',
                                  password='code', db='Investar', charset='utf8')
        self.engine = create_engine('mysql+pymysql://root:code@localhost/Investar')
        self.codes = {}
        self.get_comp_info()
    
    def __del__(self): # del mk
        """소멸자 : MariaDB 연결 해제"""
        self.conn.close()
        self.engine.dispose()


    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes에 저장"""
        """company_info 테이블에서 읽어와서 companyData와 codes에 저장"""
        sql = "SELECT * FROM company_info"
        company_info = pd.read_sql(sql, self.engine)
        for idx in range(len(company_info)):
            self.codes[company_info['code'].values[idx]] = company_info['company'].values[idx]
    

    def get_daily_price(self, code, start_date=None, end_date=None, count=None):
        """KRX 종목의 일별 시세를 데이터프레임 형태로 반환
        - code       : KRX 종목코드('005930') 또는 상장기업명('삼성전자')
        - start_date : 조회 시작일('2020-01-01'), 미입력 시 1년 전 오늘
        - end_date   : 조회 종료일('2020-12-31'), 미입력 시 오늘 날짜
        - count      : 최근 N개의 데이터 가져오기
        """

        # 시작 날짜 초기화
        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
        else:
            start_date = self.format_date(start_date)

        # 종료 날짜 초기화
        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
        else:
            end_date = self.format_date(end_date)

        # 코드 확인
        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())

        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")
            return None

        # SQL 쿼리 작성
        sql = f"""
            SELECT * FROM daily_price 
            WHERE code = '{code}' 
            AND date >= '{start_date}' 
            AND date <= '{end_date}'
            ORDER BY date DESC
        """
        
        # count가 주어진 경우 LIMIT 추가
        if count:
            sql += f" LIMIT {count}"

        # 쿼리 실행 및 결과 반환
        df = pd.read_sql(sql, self.engine)
        df.index = pd.to_datetime(df['date'])
        return df.sort_index()  # 날짜 순서 정렬 (오름차순)



if __name__ == '__main__':
    mk = MarketDB()
    # print (mk.codes)
    # df = mk.get_daily_price('004840', start_date='2024-11-01', end_date='2024-11-20')
    df = mk.get_daily_price('305080')
    print(df)




