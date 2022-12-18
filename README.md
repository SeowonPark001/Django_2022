# Django_2022

데이터베이스 생성
python manage.py migrate

관리자 계정 생성
python manage.py createsuperuser

장고앱 생성
python manage.py startapp 앱이름

생성한 장고앱 프로젝트에 등록
프로젝트폴더/settings.py
'앱이름' 추가

models.py 내용이 바뀔 때마다 데이터베이스에 모델 반영
makemigrations & migrate

모델 클래스 만들기
해당 앱 폴더/models.py
import models 필수

관리자 페이지에 모델 등록
해당 앱 폴더/admin.py

프로젝트에 해당앱 페이지 url로 접속
프로젝트/urls.py
path 추가

앱에서 url 처리
해당앱/urls.py
path 추가

___View로 페이지 만들기
해당앱/views.py