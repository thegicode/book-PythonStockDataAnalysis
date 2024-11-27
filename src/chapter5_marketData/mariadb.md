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
