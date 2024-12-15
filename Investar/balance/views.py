import ssl
import certifi
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

def get_data(symbol):
    # SSL 인증서 검증 비활성화
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    
    url = f'http://finance.naver.com/item/sise.nhn?code={symbol}'
    request = Request(url, headers=headers)

    # with urlopen(url) as doc:
    with urlopen(request, context=ssl_context) as response:
        html = BeautifulSoup(response, 'lxml')
        # soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = html.find('strong', id='_nowVal')  # ①
        cur_rate = html.find('strong', id='_rate')  # ②
        stock = html.find('title')  # ③
        stock_name = stock.text.split(':')[0].strip()  # ④
        return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):
    querydict = request.GET.copy()
    # ⑤ GET 방식으로 넘오온 QueryDict 형태의 URL을 리스트 형태로 변환
    mylist = querydict.lists() 
    rows = []
    total = 0

    for x in mylist:
        # ⑥  mylist의 종목코드로 get_data 함수를 호출하여 현재가, 등락률, 종목명을 구한다.
        cur_price, cur_rate, stock_name = get_data(x[0])      
        price = cur_price.replace(',', '')
        # ⑦ mylist의 종목수를 int형으로 변환한 뒤 천 자리마다 쉼표(',')를 포함하는 문자열로 변환
        stock_count = format(int(x[1][0]), ',')  
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',') 
        # ⑧ 종목명, 종목코드, 현재가, 주식수, 등락률, 평가금액을 릿트로 생성, row 리스트에 추가
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
            stock_sum]) 
        # ⑨ 평가금액을 주식수로 곱한 뒤 total 변수에 더한다.
        total = total + int(price) * int(x[1][0])  

    total_amount = format(total, ',')     
    # ⑩ balance.html 파일에 전달할 값들을 values 딕셔너리에 저장  
    values = {'rows' : rows, 'total' : total_amount}  
    # ⑪ balance.html 파일을 표시하도록 render() 힘수를 호출하면서 인숫값에 해당하는 values 딕셔너리를 넘겨준다.
    return render(request, 'balance.html', values)  