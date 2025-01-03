1.  Homebrew 설치 확인
    brew --version
    brew update

2.  MariaDB 설치
    brew install mariadb

3.  MariaDB 서비스 시작
    brew services start mariadb

    종료
    brew services stop mariadb

4.  MariaDB 초기화
    mariadb-secure-installation

5.  MariaDB 접속
    mysql -u root -p

    FLUSH PRIVILEGES;
    ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_new_password';

6.  데이터베이스 생성하기
    CREATE DATABASE Investar;
    SHOW DATABASES;
    USE Investar;
    SHOW TABLES;
    SELECT VERSION();
    DROP DATABASE Investar;

7.  삭제
    DELETE FROM company_info
    WHERE company IN ('메리츠금융지주');

8.  추가
    INSERT INTO company_info (code, company, last_update)
    VALUES ('390390', 'KODEX 미국반도체MV', '2025-01-03');

    VALUES ('161510', 'PLUS 고배당주', '2025-01-03');
    VALUES ('138040', '메리츠금융지주', '2024-12-27');
    VALUES ('305080', 'TIGER 미국채10년선물', '2024-12-18');

9.  참조 문법

```
mysql -u root -p
code
SHOW DATABASES;
USE Investar;
SHOW TABLES;
SELECT * FROM company_info;
SELECT * FROM daily_price;
```
