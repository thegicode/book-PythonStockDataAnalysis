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

-   사용자 및 그룹에 대한 권한 설정

```
python3 manage.py createsuperuser
http://localhost:8000/admin

```

<br>
<hr>
<br>

## 7.3 장고 인덱스 페이지

-   html 코드 부분을 template 파일로 작성, 동적인 데이터 부분은 파이썬 코드로 개발하는 것이 효율적
-   장고에서는 보안성을 높이려는 의도로 파이썬 코드와 html 페이지들을 한 디렉터리에 두지 못한다.
    -   또한 장고에서 이미지 파일을 표시하려면 추가 절차가 필요하다.

### 7.3.1 index 애플리케이션 생성하기

-   index 애플리케이션 생성

    ```
    python3 manage.py startapp index
    ```

-   [settings.py](../../Investar/Investar/settings.py)
    -   INSTALLED_APPS에 'index' 앱 추가

### 7.3.2 URLConf 추가하기

-   [urls.py](../../Investar/Investar/urls.py)
    -   index 모듈 내의 views를 index_views로 임포트
    -   마지막 라인에 path() 함수 추가하여 URLConf를 수정
    -   URL이 'index/'이면 index 애플리케이션 뷰의 main_view()함수로 매핑s하라는 의미

### 7.3.3 뷰 수정하기

-   [views.py](../../Investar/index/views.py)
-   main_view() 함수는 단순히 django.shortcuts의 render() 함수에 템플릿으로 사용할 파일명(index.html)만 넘겨주는 역할

### 7.3.4 템플릿 작서

-   index/template 디렉터리 생성
-   [index.html](../../Investar/index/templates/index.html)
-   이미지도 template 폴더 안에

    ```
    tree -f
    http://localhost:8000/index/

    ```

### 7.3.5 템플릿 태그

-   static, static/index 디렉터리 생성
-   이미지를 static/index 아래로 이동

-   [index.html](../../Investar/index/templates/index.html)

    ```
    {% load static %}
    <link rel="stylesheet" href={% static "index/style.css" %} />
    <img src={% static "index/Django_Logo.jpg" %} /></a>
    ```

### 7.3.6 CSS

-   [style.css](../../Investar/index/static/index/style.css)
-   http://localhost:8000/index/

<br>
<hr>
<br>

## 7.4 웹으로 계좌 잔고 확인하기

### 7.4.1 balance 애플리케이션 생성하기

-   balance 애플리케이션 생성

    ```
    python3 manage.py startapp balance
    ```

-   [setting.py](../../Investar/Investar/settings.py) 수정
    -   INSTALLED_APPS에 'balance' 추가

### 7.4.2 URLConf 추가하기

-   [urls.py](../../Investar/Investar/urls.py)
    -   'path('balance/', balance_views.main_view)'

### 7.4.3 현재가 구하기

[네이버 종목별 시세](https://finance.naver.com/item/sise.nhn?code=035420)

### 7.4.4 뷰 수정하기

[views.py](../../Investar/balance/views.py)

### 7.4.5 뷰에서 템플릿으로 컨텍스트 전달하기

-   템플릿에서 표시해야 할 컨텍스트가 있다면 딕셔너리 형태로 render() 함수의 세 번째 인수를 통해 넘겨주면 된다.

    -   위의 코드에서는 values = {'rows': rows, 'total': totalAmlount}
    -   rows는 중첩된 리스트이기 때문에 템플릿에서도 {% for %} 태그를 중첩해서 사용해야 rows의 모든 원소를 출력할 수 있다.

    ```
    {% for row in rows %}
    <tr>
        {% for x in row %}
        <td>{{ x }}</td>
        {% endfor %}
    </tr>
    {% endfor %}
    ```

### 7.4.6 템플릿 작성

-   balance/templates 디렉터리 생성, balance.html 추가
-   [balance.html](../../Investar/balance/templates/balance.html)

### 7,4.7 캐스캐이딩 스타일 시트 적용

-   [b_style.css](../../Investar/balance/static/b_style.css)

### 7.4.8 웹으로 계좌 잔고 확인하기

-   장고 서버 재시작하고
-   http://localhost:8000/balance/?035420=30&005930=20
-   장고에서 웹 페이지로 표시하려면 URL 처리, 뷰 처리, 템플릿 태그 처리 등 기본적으로 거쳐야 하는 과정이 제법 있다.
-   더 익히고 싶다면 6장의 트레이딩 전략결과를 장고 웹 페이지로

<br>
<hr>
<br>

## 7.5 슬랙으로 알림 메시지 보내기

-   매매 체결 내역이라든가 서버 시스템 에러 상황을 사용자에게 알려줄 때 요긴하다.
    -   또한 주기적으로 계좌 잔고를 보내주거나 주가가 5% 이상 등락할 때 알림 메시지를 보내주는 등 활용 방안이 많기 때문에 시스템 자동화에 반드시 필요한 라이브러리다.

### 7.5.1 슬랙의 특징

### 7.5.2 워크스페이스와 앱 만들기

-   [슬랙](https://slack.com/)에 접속해 워크스페이스를 만든다.
    -   Create Workspace
-   [슬랙 API](https://api.slack.com/)
    -   Create Slack App
    -   mySlackBot, Investar

### 7.5.3 봇 기능 추가하기

-   앱이 생성된 다음에는 화면 좌측에 있는 OAuth & Permissions

### 7.5.4 토큰 발급하기

-   Bots의 토큰 영역을 설정하는 것
    -   Bot Token Scopes, chat:write, Add an OAuth Scope
    -   이후 'Install App to Workspace' -> 앱을 인증받을 때 사용할 수 있는 토큰이 발급된다.
-   토큰은 일종의 패스워드와 같은 개념으로, 토큰 종류에 따라 사용할 수 있는 슬랙 API 범위가 달라진다.
-   xoxb로 시작되는 봇 사용자용 토큰을 사용(Bot User OAuth Access Token)

### 7.5.5 슬랙으로 메시지 보내기

-   슬랙 API를 사용해서 메시지를 보내려면 파이썬 외부 라이브러리인 slacker가 필요하므로, 명령창에서 pip install slacker를 입력하여 설치
-   Slacker 객체를 생성하여 봇 사용자용 토큰을 넘겨주어야 한다.
    -   post_message() 함수의 첫 번째 인수로 워크스페이스가 아닌 채팅방이름 channel을 넘겨줘야 한다.
    -   채널명 앞 부분에 있는 #은 있으나 없으나 상관없다.
-   [슬랙 message](./slack_message.py)
-   [슬랙 markdown](./slack_markdown.py)
