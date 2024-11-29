
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
    

    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목의 일별 시세를 데이터프레임 형태로 반환
            - code       : KRX 종목코드('005930') 또는 상장기업명('삼성전자')
            - start_date : 조회 시작일('2020-01-01'), 미입력 시 1년 전 오늘
            - end_date   : 조회 종료일('2020-12-31'), 미입력 시 오늘 날짜
        """

        if start_date is None:
            one_year_ago = datetime.today() - timedelta(days=365)
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print(f"start_date is initialized to {start_date}")
        else:
            start_lst = re.split(r'\D+', start_date)
            if start_lst[0] == '':
                start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError: start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError: start_month({start_month:d}) is wrong.")
                return
            if start_day < 1 or start_day > 31:
                print(f"ValueError: start_day({start_day:d}) is wrong.")
                return
            start_date=f"{start_year:04d}-{start_month:02d}-{start_day:02d}"

        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            print(f"end_date is initialized to {end_date}")
        else:
            end_lst = re.split(r'\D+', end_date)
            if end_lst[0] == '':
                end_lst = end_lst[1:] 
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1800 or end_year > 2200:
                print(f"ValueError: end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError: end_month({end_month:d}) is wrong.")
                return
            if end_day < 1 or end_day > 31:
                print(f"ValueError: end_day({end_day:d}) is wrong.")
                return
            end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}"

        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())

        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")
        
        # Corrected SQL query
        sql = f"""
            SELECT * FROM daily_price 
            WHERE code = '{code}' 
            AND date >= '{start_date}' 
            AND date <= '{end_date}'
        """
        df = pd.read_sql(sql, self.engine)
        df.index = pd.to_datetime(df['date'])
        return df


if __name__ == '__main__':
    mk = MarketDB()
    # print (mk.codes)
    # df = mk.get_daily_price('004840', start_date='2024-11-01', end_date='2024-11-20')
    df = mk.get_daily_price('004840')
    print(df)




