# Chapter 6 트레이딩 전략과 구현

-   현대 포트폴리오 이론과 효율적 투자선
-   볼린저 밴드를 이용한 추세추종, 반전 매매기법
-   세 가지 창으로 시장을 분석하는 삼중창 매매기법
-   상대 모멘텀과 절대 모멘텀을 합친 듀얼 모멘텀 전략

## 6.1 현대 포트폴리오 이론

### 6.1.1 수익률의 표준편차

### 6.1.2 효율적 투자선

-   [시총 상위 4 종목으로 효율적 투자선 구하기](./6.1_EfficientFrontier.py)
-   몬테카를로 시뮬레이션 : 많은 난수를 이용해 함수의 값을 확률적으로 계산하는 것

## 6.2 샤프 지수와 포트폴리오 최적화

### 6.2.1 샤프 지수

샤프 지수 = (포트폴리오 예상 수익률 - 무위험률) / 수익률의 표준편차
샤프 지수가 높을 수록 위험에 대한 보상이 크다.

### 6.2.2 포트폴리오 최적화

[전체소스코드](./6.2_PortfolioOptimization.py)

## 6.3 볼린저 밴드 지표

### 6.3.1 볼린저 밴드 구하기

[소스코드](./6.3_BollingerBand.py)

### 6.3.2 볼린저 밴드 지표 1 : %b

-   주가가 볼린저 밴드 어디에 위치하는지를 나타내는 지표
-   %b = (종가 - 하단 볼린저 밴드) / (상단 볼린저 밴드 - 중간 볼린저 밴드)

[소스코드](./6.4_BollingerBand_PercentB.py)

### 6.3.3 볼린저 밴드 지표 2 : 밴드폭

-   밴드폭 = (상단 볼린저 밴드 - 하단 볼린저 밴드) / 중간 볼린저 밴드
-   강력한 추세의 시작과 마지막을 포착
-   강력한 추세는 스퀴즈로부터 시작되는데 변동성이 커지면서 밴드폭 수치가 급격히 높아진다.
    이 때 밴드폭이 넓어지면서 추세의 반대쪽에 있는 밴드는 추세 반대 방향으로 향한다.
    [소스코드](./6.5_BollingerBand_BandWidth.py)

## 6.4 볼린저 밴드 매매기법

### 6.4.1 볼린저 밴드를 이용한 추세 추종 매매기법

-   매수 : 주가가 상단 밴드에 접근하며, 지표가 강세를 확증할 때만 매수
    (%b가 0.8보다 크고, MFI가 80보다 클 때)
-   매도 : 주가가 하단 밴드에 접근하며, 지표가 약세를 확증할 때만 매도
    (%b가 0.2보다 작고, MFI가 20보다 작을 때)

#### MFI (현금흐름지표, Money Flow Index)

-   MFI = 100 - (100 / (1 + (긍정적 현금 흐름 / 부정적 현금 흐름)))
    -   긍정적 현금 흐름 : 중심 가격이 전일보다 상승한 날들의 현금 흐름의 합
    -   부정적 현금 흐름 : 중심 가격이 전일보다 하락한 날들의 현금 흐름의 합

#### 추세 추종 매매 구현

[소스코드](./6.6_BollingerBand_TrendFollowing.py)

### 6.4.2 볼린저 밴드를 이용한 반전(Reversals) 매매기법

-   주가가 반전하는 지점을 찾아내 매수 또는 매도하는 기법
-   주가가 하단 밴드를 여러 차례 태그하는 과정에서 강세 지표가 발생하면 매수하고,
-   주가가 상단 밴드를 여러 차례 태그하는 과정에서 약세 지표가 발생하면 매도한다.

-   매수 : 주가가 하단 밴드 부근에서 W형 패턴을 나타내고, 강세 지표가 확중할 때 매수 (%b가 0.05보다 작고 II%가 0보다 크면 매수)
-   매도 : 상단 밴드 부근에서 일련의 주가 태그가 일어나며, 약세 지표가 확증할 때 매도 (%b가 0.95보다 크고 II가 0보다 작으면 매도)

#### 일중 강도 intraday intensity , II

-   장이 끝나는 시점에서 트레이더들의 움직임을 나타내는데, 종가가 거래 범위 천정권에서 형성되면 1, 중간에서 형성되면 0, 바닥권에서 형성되면 -1이 된다.
-   21일 기간 동안의 II합을 21일 기간 동안의 거래량 합으로 나누어 표준화한 것이 일중 강도율이다.

-   일중 강도 = ((2 × 종가 - 고가 - 저가) / (고가 - 저가)) × 거래량
-   일중 강도율 = (일중강도의 21일 합 / 거래량의 21일 합) × 100

-   [소스코드](./6.7_BollingerBand_IIP21.py)
    -   세 번째 차트에 표시된 일중 강도율은 기관 블록 거래자의 활동을 추적할 목적으로 만들어진 지표다.
    -   존 볼린저는 일중 강도율을 볼린저 밴드를 확증하는 도구로 사용하는데,
        -   주가가 하단 볼린저 밴드에 닿을 때 일중 강도율이 + 이면 매수하고,
        -   반대로 주가가 상단 볼린저 밴드에 닿을 때 강도율이 -이면 매도하라고 조언한다.

#### 반전 매매 구현

-   [소스코드](./6.8_BollingerBand_Reversals.py)

## 6.5 심리투자 법칙

-   Alexander Elder, "주식시장에서 살아남는 심리투자 법칙", 이레미디어

-   정신 (Mind) : 시장 노이즈에 휩쓸리지 않도록 해주는 법칙
-   기법 (Method) : 시장 지표를 활용해 주가를 분석하고 이를 매매에 활용하는 기법
-   자금 (Money) : 리스크를 거래의 일부로 포함시키는 자금 관리

### 6.5.1 시장 지표 Market Indicator

-   이동평균, MACD 같이 시장의 흐름을 나타내는 지표를 추세 trend 지표라고 하는데,
    시장이 움직일 때는 잘 맞지만 시장이 횡보할 때 잘못된 신호를 보낼 수 있다.

-   스토캐스틱이나 RSI처럼 과거 일정 기간의 가격 범위 안에서 현재 가격의 상대적인 위치를 나타내는 지표를 Osillator라고 하는데, 현재 가격 위치가 주기적으로 변화하는 모습이 오실레이터 발전기에서 생성하는 교류 주파수 므솝과 유사하다.
-   오실레이터는 횡보장에서 전환점을 포착하는 데 적합히지만 가격보다 앞서 변하는 경향이 있다.
-   기타 지표들은 강세장과 약세장에 따른 강도를 예측한다.

##### 표: 시장 지표의 분류

| **구분**       | **발생 시점**  | **지표**                                      |
| -------------- | -------------- | --------------------------------------------- |
| **추세**       | 동행 또는 후행 | 이동평균(Moving Averages)                     |
|                |                | 이동평균 수렴확산(MACD)                       |
|                |                | MACD 히스토그램                               |
|                |                | 방향성 시스템(The Directional System)         |
|                |                | 거래량 균형 지표(On-Balance Volume, OBV)      |
|                |                | 누적분산 지표(Accumulation/Distribution, AD)  |
| **오실레이터** | 선행 또는 동행 | 스토캐스틱(Stochastic)                        |
|                |                | 변화율(Rate of Change)                        |
|                |                | 평활화된 변화율(Smoothed RoC)                 |
|                |                | 모멘텀(Momentum)                              |
|                |                | 상대강도지수(Relative Strength Index, RSI)    |
|                |                | 엘더레이(Elder-ray)                           |
|                |                | 강도지수(The Force Index)                     |
|                |                | 윌리엄스(Williams %R)                         |
|                |                | 상대가격변동폭(The Commodity Channel Index)   |
| **기타 지표**  | 선행 또는 동행 | 신고점-신저점 지수(New High-New Low Index)    |
|                |                | 풋-콜 비율(The Put-Call Ratio)                |
|                |                | 상승하락 지수(The Advance/Decline Index, A/D) |
|                |                | 트레이더 지수(The Trader's Index, TRIN)       |

### 6.5.2 단순 이동평균 simple moving average, SMA

-   이동평균선 진행 방향을 보면 전반적인 가격 흐름을 예측할 수 있다.
-   단순 이동 평균은 오래된 가격의 변동과 최근 가격의 변동을 동일하게 반영하기 때문에 최근 가격의 변동이 왜곡될 가능성이 있다.

### 6.5.3 지수 이동평균 esponential moving average, EMA

-   최근의 데이터에 가중치를 부여해 단순 이동평균에 비해서 최근의 데이터 변동을 잘 반영하도록 설계되었다.

-   EMA = P (today) × K + EMA (yesterday) × (1 - K)

-   K : 2/(N + 1)
-   N: 지수 이동평균 일수
-   P (today): 오늘의 가격
-   EMA (yesterday): 어제의 지수 이동평균

-   단순 이동평균에 비해서 두 가지 장점
    1.  최근 거래일에 더 많은 가중치를 주므로 최근 가격의 변동을 더 잘 나타낸다.
    2.  오래된 지수 이동평균 데이터가 천천히 사라지므로 오래된 데이터가 빠져나갈 때 지수 이동평균이 급등락하지 않는다.
-   지수 이동평균이 오르면 추세가 상승하고 있음을 나타내므로 매수 측에서 매매해야 한다. 반대로 지수 이동평균이 내리고 있다면 매도 측에서 매매하는 것이 좋다.
    -   알렉산더 엘더에 따르면 이동평균의 기간은 시장 the dominant market 사이클의 절반 정도가 적당하다.
    -   즉 20일 주기를 발견했다면 10일 이동평균선을 사용하면 된다.
    -   <u>참고로 알렉산더 엘더는 매매할 때 주로 13일 지수이동평균을 사용한다.</u>

### 6.5.4 이동평균 수렴확산(MACD) Moving Average Convergence DIvergence

-   MACD 선 (실선), 신호선 (점선)
-   MACD 선은 종가의 12일 지수 이동평균에서 26일 지수 이동평균선을 뺀 것으로, 가격변화에 상대적으로 빨리 반응한다.
-   한편, 신호선은 MACD 선의 9일 지수 이동평균을 구한 선으로 MACD선을 평활화시킨 것이기 때문에 가격 변화에 상대적으로 늦게 반응한다.
-   빠른 MACD선이 늦은 신호선을 상향 돌파하는 것은 매수세가 시장을 주도한다는 뜻이므로 매수적 관점에서 대응하는 것이 좋다.
-   반대로 빠른 MACD선이 늦은 신호선을 하향 돌파할 때는 매도 관점에서 대응해야 한다.

### 6.5.5 MAC 히스토그램 MACD Histogram

-   원래의 MACD보다 매수와 매도 상태를 더 잘 표현한다.

    -   단순히 매수와 매도의 비중을 표시할 뿐만 아니라 강해지고 있는지 약해지고 있는지를 보여주므로, 기술적 분석가에게는 최고의 도구다.

-   MACD 히스토그램 = MACD선 - 신호선
-   MACD 히스토그램의 기울기를 확인하는 것은 히스토그램이 중심선 위에 있는지 아니면 아래에 있는지 확인하는 것보다 중요하다.
    -   현재 봉이 이전 봉보다 높다면 기울기는 올라가고 있으므로 매수를 해야 한다.
    -   최고의 매수 신호는 MADC 히스토그램이 중심선 아래에 있고, 기울기가 상향 반전하고 있을 때 발생한다.
-   <u>MACD 히스토그램과 가격과의 다이버전스는 일 년에 몇 번만 일어나며 기술적 분석에서 가장 강력한 신호다.
    -   가격이 신저점까지 낮아졌으나 MACD 히스토그램이 저점에서 상승하기 시작했다면, 강세 다이버전스 bullish divergence가 형성됨을 뜻한다.
    -   반면에 가격이 신저점을 갱신하면서 MACD 히스토그램도 낮아지고 있다면 단순히 하향추세 신호다. </u>
-   [GTP 질문 예제](./6.9_MACD_Histogran_GPT.py)

### 6.5.6 스토캐스틱 Stocastic

-   지난 n일 동안의 거래 범위에서 현재 가격 위치를 백분율로 나타낸다.
    -   14일 스토캐스틱이 70 : 지난 14일간 거래에서 최저점과 최고점 사이 70%에 위치해 있다.
    -   일반적으로 80 이상은 고매수 상태를 나타내고 20 이하는 과매도 상태를 나타낸다.
-   스토캐스틱은 두 선으로 이루어져 있으며 빠른 서는 %K, 느린 선은 %D

    -   <u>일반적으로 %K의 기간은 14일로 설정하지만 알렉산더 엘더는 짧은 반전을 잡아내기 용이한 5일로 설정,</u>
        (반면 기간이 길면 중요 변곡점을 잡아내는 데 유용하다.)

-   %K = ((C <sub>today</sub> + L <sub>n</sub>) / (H <sub>n</sub> + L <sub>n</sub>)) × 100
    -   C <sub>today</sub>: 오늘의 종
    -   H <sub>n</sub> : 선정된 기간의 고점
    -   L <sub>n</sub> : 선정된 기간의 저점
    -   n : 트레이더에 의해 선정된 기간
-   느린 선 %D는 빠른 선 %K를 평활화해 얻는다. 일반적으로 3일을 이용한다.

    -   %D = ((C <sub>today</sub> + L <sub>n</sub> 의 3일간 합계) / (H <sub>n</sub> + L <sub>n</sub>의 3일간 합계)) × 100

-   <u>스토캐스틱은 시장이 박스권에서 움직일 때는 잘 작동</u>, 추세에 들어갈 때는 그렇지 않다.
-   스토캐스틱은 장기 추세 추종형 지표와 결합해서 사용해야 한다.

## 6.6 삼중창 매매 시스템

-   추세 추종과 역추세 매매법을 함께 사용하며, 세 단계의 창 Sereen 을 거쳐 더 정확한 매매 시점을 찾도록 구성
-   주식 시장의 중요한 딜레마 중 하나는 시간의 관점에 따라 주가 차트가 오를 수도 있고 내릴 수도 있다.

### 6.6.1 첫 번째 창 - 시장 조류

-   트레이더에게는 매수, 매도, 관망 세 가지 선택지가 주어진다.
    -   삼중창의 첫 번째 창 First Screen을 이용하면 이 중 한 선택지를 제거할 수 있다.
    -   시장이 상승 추세인지 하락 추세인지 판단해 상승 추세에는 매수하거나 관망하고, 하락 추세에너는 매도하거나 관망하면 된다.
-   삼중창의 첫 번째 창은 시장 조류 Market Tide, 즉 장기 차트를 분석하는 것이다.
    -   트레이더는 자신이 매매하는 시간 단위보다 한 단계 긴 단위 차트를 이용해 분석하면 된다.
        -   일간 차트 매매 -> 주간 차트 추세 분석
        -   5분 차트 매매 -> 30분 봉으로 추세 분석
-   [삼중창 매매 시스템의 첫 번째 창 소스 코드](./6.9_FirstScreen.py)
    -   시장의 장기 추세를 분석하기 위해서 26주 지수 이동평균에 해당하는 EMA 130 그래프와 주간 MACD 히스토그램을 함꼐 표시
        -   26주는 130일 거래일에 해당, 1년 동안의 개장일의 절반
        -   26주 지수 이동평균 대신 일간 지수 이동평균을 130일로 설정해서 사용해도 된다.
-   알렉산더의 두 번째 서적인 "나의 트레이딩 룸으로 오라"에서 저자 자신도 처음에는 주간 추세추종 지표로 주간 MACD 히스토그램의 기울기를 사용했으나, 최근에는 26주 지수이동평균을 사용한다고 밝혔다.
-   필자 테스트, 주간 MACD 히스토그램을 사용했을 때는 불필요한 매수/매도 신호가 자주 발생해서, 필자도 지금은 26주 지수 이동평균(EMA 130)을 주간 추세추종 지표로 사용하고 있다.
    -   <u>삼중창 매매 시스템의 첫 번째 창에서는 EMA 130 그래프가 오르고 있을 때에만 시장에 참여하면 된다.</u>