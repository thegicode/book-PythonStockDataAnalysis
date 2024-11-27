"""
5.2.4 파아마이에스큐엘로 버전 정보 확인하기
pip install pymysql


"""

import pymysql


# connect() 함수를 사용해 connection 객체를 생성
connection = pymysql.connect(host='localhost', port=3306, db='Investar', 
                             user='root', password='code', autocommit=True)

# cursor() 함수를 사용해 cursor 객체를 생성
cursor = connection.cursor()

# 3. cursor 객체의 execute() 함수를 사용해 SELECT문을 실행
cursor.execute('SELECT VERSION();')

# cursor 객체의 fetchone() 함수를 사용해 3의 실행 결과를 튶ㄹ로 받는디.
result = cursor.fetchone()

# result 객체를 출력을 살펴보면 괄호로 둘러쌓여 있다. 
# 문자열 원소 옆에 쉼표가 표시되어 있으니 원소가 하나인 튜플
# 파이썬에서는 여러 값을 리턴할 때 일반적으로 튜플 사용
print(f"MariaDB version : {result}")

connection.close()