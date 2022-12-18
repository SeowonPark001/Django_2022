from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post, Category
from django.contrib.auth.models import User

# Create your tests here.

class TestView(TestCase):

    def setUp(self):
        self.client = Client()

        # author test
        # user 생성
        self.user_kim = User.objects.create_user(username="kim", password="kim12345")
        self.user_lee = User.objects.create_user(username="lee", password="lee12345")

        # 카테고리 생성
        self.category_com = Category.objects.create(username="computer", slug="computer")
        self.category_edu = Category.objects.create(username="education", slug="education")

        # 포스트 생성
        self.post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='첫번째 포스트입니다.',
            author = self.user_kim,
            category=self.category_com,     # category 추가
        )
        self.post_002 = Post.objects.create(
            title='두번째 포스트',
            content='두번째 포스트입니다.',
            author=self.user_lee,
            category=self.category_edu,     # category 추가
        )
        self.post_003 = Post.objects.create(
            title='세번째 포스트',
            content='세번째 포스트입니다.',
            author=self.user_lee,
            # category 없음
        )


    # Navbar 테스트 함수 : 여러 곳에서 코드 중복 > 함수 따로 생성 (함수 이름: test로 시작하면 X)
    def nav_test(self, soup): # soup: 인자 전달 필수
        # soup의 navbar 태그 >> 텍스트에 Blog, About Me 가 있는지
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # Home 텍스트가 <a> 태그 내 포함되어 있는 것 >> navbar.html 일치해야!
        home_btn = navbar.find('a', text="Home")
        self.assertEqual(home_btn.attrs['href'], '/')

        # Blog 텍스트가 <a> 태그 내 포함되어 있는 것 >> 일치해야!
        blog_btn = navbar.find('a', text="Blog")
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        # About Me 텍스트가 <a> 태그 내 포함되어 있는 것 >> 일치해야!
        about_btn = navbar.find('a', text="About Me")
        self.assertEqual(about_btn.attrs['href'], '/about_me/')


    # Category 테스트 함수 - 여러 곳에서 코드 중복 > 함수 따로 생성 (함수 이름: test로 시작하면 X)
    # def category_test(self, soup): # soup: 인자 전달 필수
    #     category_card = soup.find('div', id='category_card')
    #     self.assertIn('Categories', category_card.text)
    #     self.assertIn( # string 형태 >> f'{}'             # post_set: 해당 카테고리 포스트 정보 받아오기
    #         f'{self.category_com.name} ({self.category_com.post_set})',
    #         category_card.text
    #     )



    # 블로그 목록 페이지 테스트
    def test_post_list(self):
        # 1-1. 포스트 목록 페이지 가져오기
        response = self.client.get('/blog/', follow=True) # 301?

        # 1-2. reponse 결과가 정상적으로 보이는지 => 정상적으로 페이지 로드됨
        self.assertEqual(response.status_code, 200)
        # 괄호 안 두 원소가 같으면 True / 다르면 False => AssertionError 발생

        # 1-3. 페이지 title이 정상적으로 보이는지 => title: Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog') # soup.title => <title>Blog</title> 태그포함

        # 1-4. 내비게이션 바(navbar)가 정상적으로 보이는지 => 배치
        # 공통된 내용 >> 함수로 호출
        self.nav_test(soup)

        # navbar = soup.nav
        # # 1-5. Blog, About Me 라는 문구 => Navbar 안에 배치
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)

        # 1-5. 카테고리 테스트
        # self.category_test(soup)

        # 2-1. Post(게시물)가 정상적으로 보이는지
        # => 맨 처음에는 Post가 없음: 0개
        self.assertEqual(Post.objects.count(), 0)

        # 2-2. main area에 문구 배치 : '아직 게시물이 없습니다.'
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3-1. Post 2개 생성 => 검사
        post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='첫번째 포스트입니다.', #'장고 테스트'
            author = self.user_kim,     # author 추가
        )
        post_002 = Post.objects.create(
            title='두번째 포스트',
            content='두번째 포스트입니다.',
            author=self.user_lee,       # author 추가
        )
        self.assertEqual(Post.objects.count(), 2)

        # 3-2. Post 목록 페이지를 새로고침 했을 때
        response = self.client.get('/blog/', follow=True)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 3-3. main area에 Post 2개의 제목 존재
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3-4. '아직 게시물이 없습니다' 문구는 더 이상 나타나지 X
        self.assertNotIn('아직 게시물이 없습니다.', main_area.text)

        # 13장: author 확인
        self.assertIn(post_001.author.username.upper(), main_area.text)
        self.assertIn(post_002.author.username.upper(), main_area.text)



    # 포스트 상세 페이지 테스트
    def test_post_detail(self):
        # 포스트 생성
        post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='첫번째 포스트입니다.',
            author=self.user_kim,   # author 추가
        )
        # 포스트 경로가 맞는지 확인
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 포스트 상세 페이지 가져오기
        # response = self.client.get('/blog/1/', follow=True)
        response = self.client.get(post_001.get_absolute_url(), follow=True)
        # 응답 코드 확인
        self.assertEqual(response.status_code, 200)
        # soup 변수에 html 파일 담기?
        soup = BeautifulSoup(response.content, 'html.parser')

        # soup의 navbar 태그 >> 텍스트에 Blog, About Me 가 있는지
        self.nav_test(soup)
        # navbar = soup.nav
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text) # post_detail.html 과 내용 맞추기 >> 안 그러면 ERROR

        # 웹문서의 타이틀이 올바른지 확인 : html 문서의 title 안에 포함되어 있는지
        self.assertIn(post_001.title, soup.title.text) # soup.title : <title> 태그 포함 >> ERROR

        # id로 연결한 div 태그 찾기 - Main, Post, Comment
        main_area = soup.find('div', id='main-area')
        post_area = soup.find('div', id='post-area')
        # comment_area = soup.find('div', id='comment-area')

        # 포스트 타이틀, 내용이 해당 텍스트 부분에 있는지 확인
        self.assertIn(post_001.title, post_area.text)
        self.assertIn(post_001.content, post_area.text)

        # 13장: author 확인
        self.assertIn(post_001.author.username.upper(), main_area.text)