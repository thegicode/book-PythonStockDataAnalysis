# 7 장고 웹 서버 구축 및 자동화

## 7.1 장고 웹 프레임워크

-   [장고 홈페이지](https://www.djangoproject.com/)

    -   "Django makes it easier to build better web apps more quickly and with less code."

-   장고를 이용하여 실시간 계좌잔고를 확인하는 웹 시스템 개발

### 7.1.1 장고의 개발 환경

### 7.1.2 장고 vs. 플라스크

-   웹 개발 경험이 없거나 초보자라면 플라스크보다는 장고를 선택하는 것이 낫다.

### 7.1.3 장고 웹 프레임워크 설치

```
# 설치
pip install django

# 버전확인
django-admin --version
```

### 7.1.4 장고 프로젝트 생성하기

```
django-admin startproject Investar
```

### 7.1.5 장고 서버 실행하기

```
python3 Investar/manage.py runserver 0.0.0.0:8000
http://localhost:8000/
```

서버 외부에서 접속하려면 실제 서버 IP를 추가: "ALLOWED_HOSTS"
[setting.py](../../Investar/Investar/settings.py)

<br>
<hr>
<br>

## 7.2 Hello Django 애플리케이션

-   "Hello, Django!"를 출력하는 애플리케이션 작성

### 7.2.1 MTV model-template-view 패턴

-   장고 개발 목적은 기사를 마감 기한 내에 빠르게 웹 사이트에 올리는 것이었다.
    -   장고 프레임워크만이 갖는 고유의 사상과 개발 방식이 있다.
-   MTV
    -   Model : 데이터베이스에 데이터를 읽고 쓰는 역할
    -   Template : 사용자에게 보여주는 부분 렌더링 처리
    -   View : URL 요청에 맞게 함수를 호출하고 처리된 데이터를 템플릿에 전달하는 역할을 담당

### 7.2.2 ORM object relative mapping

-   파이썬 객체와 관계형 데이터베이스를 연결해준다.
    -   models.py 파일에 모델 클래스를 정의하면 이에 대한 매핑 테이블이 데이터베이스에 자동으로 생성된다.
    -   모델 클래스의 속성은 해당 테이블의 칼럼으로 매핑되기 때문에, 애플리케이션 입장에서는 SQL이 없어도 객체를 통해 데이터베이스에 접근할 수 있어 편리하다.

### 7.2.3 장고 애플리케이션 생성하기

-   장고에서는 웹 사이트를 프로젝트 단위로 구분하고, 프로젝트를 구성하는 모듈화된 프로그램들을 애플리케이션이라고 부른다.
    -   즉, 애플리케이션들이 모여서 프로젝트가 된다.
-   hello 애플리케이션 생성

```
> Investar /
python3 manage.py startapp hello

python3 manage.py migrate

brew install tree
tree -f
```

-   tree -f 명령을 입력했을 때 디렉터리와 파일들이 보인다.

    -   hello 디럭터리는 애플리케이션 디렉터리이고, Investar는 프로젝트 디렉터리다.

-   [Investar/setting.py](../../Investar/Investar/settings.py) 파일에서는 프로젝트와 관련된 설정을 할 수 있다.
    -   INSTALLED_APPS 리스트의 마지막에 'hello'를 추가

### 7.2.4 URLConf 설정하기

-   settings.py 파일은 프로젝트와 관련된 설정 사항을 기록하는 파일
    -   ROOT_URLCONF : '프로젝트명.urls'
    -   즉, 최상위 URLConf가 Investar.urls
    ```
    ROOT_URLCONF = 'Investar.urls'
    ```

### 7.2.5 정규표현식으로 URL-View 매핑하기

-   [urls.py](../../Investar/Investar/urls.py)
-   영문 주석을 보면 URL 설정
    ```
    from hello import views
    re_path(r'^(?P<name>[A-Z][a-z]*)$', views.sayHello)
    ```
-   urlpatterns 리스트는 URL에 따라 실제로 보여줄 뷰를 매핑하는 역할을 한다.

### 7.2.6 views 수정하기

-   [views.py](../../Investar/hello/views.py)
-   웹 브라우저의 주소창에 URL을 입력해 호스트와 포트 번호 다음에 나오는 리소스 경로를 받아와서 'Hello." 문자열에 이어서 출력해볼 것이다.
-   보통 request 인수 하나만 있으면 되지만, URL 리소스 경로를 파라미터로 받도록 name 인수를 추가한다.

    ```
    python3 manage.py runserver 0.0.0.0:8000
    http://localhost:8000/Django
    http://localhost:8000/Python
    ```

### 7.2.7 장고 관리자 페이지
