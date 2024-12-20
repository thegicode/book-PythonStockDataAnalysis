

from datetime import datetime
from dbgout import dbgout
from ohlc import get_ohlc


def get_movingaverage(code, window):
    """인자로 받은 종목에 대한 이동평균가격을 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        # 1. 인수로 받은 종목의 두 달치 OHLC 데이터를 조회
        ohlc = get_ohlc(code, 20)

        # 2. 첫 번째 OHLC 행의 인덱스 날짜가 오늘이면 두 번째 OHLC 행의 인덱스 날짜를 어제 날짜로 사용하고, 
        # 첫 번째 OHLC 행의 인덱스 날짜가 오늘이 아니라면 첫 번째 OHLC 행의 인덱스 날짜를 어제 날짜로 사용한다.
        if str_today == str(ohlc.iloc[0].name):
            lastday = ohlc.iloc[1].name
        else:
            lastday = ohlc.iloc[0].name
        closes = ohlc['close'].sort_index()   
        ma = closes.rolling(window=window).mean()
        return ma.loc[lastday]
    except Exception as ex:
        dbgout('get_movingavrg(' + str(window) + ') -> exception! ' + str(ex))
        return None    
    

if __name__ == "__main__":
    print(get_movingaverage('305080', 10))