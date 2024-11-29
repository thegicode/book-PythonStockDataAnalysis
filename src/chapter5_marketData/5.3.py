"""
5.3 주식 시세를 매일 DB로 업데이트하기

5.3.1 DBUpdate 클래스 구조
5.3.4 파이마이에스큐엘로 테이블 생성하기
5.3.5 종목코드 구하기
5.3.6 종목코드 DB에 업데이트하기
    REPLACE INTO 구문
    company_info 테이블 확인하기
5.3.7 주식 시세 데이터 읽어오기
    try except 에외 처리
    read_naver()
5.3.8 일별 시세 데이터를 DB에 저장하기
    reaplce_into_db()
    update_daily_price()
5.3.9 json을 이용한 업데이트 페이지 수 설정
    config.json
    execute_daily()
5.3.10 마리아디비 자동 연결 해제 방지
    마리아디비 설정 파일에서 wait_timeout 값 변경
    MariaDB의 기본 설정 파일은 일반적으로 /etc/my.cnf 또는 /usr/local/etc/my.cnf 경로에 있습니다.
    설정파일 경로 확인 : mysql --help | grep "Default options" -A 1

    설정파일 열기 
        sudo nano 경로
    
    wait_timeout = 288000

5.3.12 Run 레지스트리 등록해 자동 실행하기
    맥북환경 - GPT > 추천 방식
    - 초보자: Login Items 방식을 추천. 설정이 간단하고 GUI를 통해 관리가 쉬움.
    - 개발자: Launch Agents 방식을 추천. 더 세부적인 설정과 로그 확인이 가능.

"""

# DBUpdater.py