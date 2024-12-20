from datetime import datetime
from dbgout import dbgout
from ohlc import get_ohlc


def get_target_price(code):
    """매수 목표가를 반환한다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        # 1. 인수로 받은 종목의 10일 OHLC 데이터를 조회
        ohlc = get_ohlc(code, 10)
        # 2. 첫 번째 OHLC 행의 인덱스 날짜가 오늘이면 두 번째 OHLC 행을 어제의 OHLC 데이터로 사용
        # 첫 번째 OHLC 행의 인덱스 날짜가 오늘이 아니라면 첫 번째 OHLC 행을 어제의 OHLC 데이터로 사용
        if str_today == str(ohlc.iloc[0].name):
            # 3. 오늘의 시가는 첫 번째 OHLC 행의 '시가' 열을 사용
            today_open = ohlc.iloc[0].open 
            lastday = ohlc.iloc[1]
        else:
            lastday = ohlc.iloc[0]     
            # 4. 오늘의 시가가 존재하지 않을 경우 어제의 종가를 대신 사용                                 
            today_open = lastday.iloc[3]  
        lastday_high = lastday.iloc[1]    
        lastday_low = lastday.iloc[2]  
        # 5. 목표 매수가는 오늘 시가 + (어제 최고가 - 어제 최고가)  * K
        target_price = today_open + (lastday_high - lastday_low) * 0.5
        return target_price
    except Exception as ex:
        dbgout("`get_target_price() -> exception! " + str(ex) + "`")
        return None
    

if __name__ == "__main__":
    print(get_target_price('305080'))
