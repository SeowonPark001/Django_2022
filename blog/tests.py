from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.

class TestView(TestCase):

    def setUp(self):
        self.client = Client()

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
        navbar = soup.nav

        # 1-5. Blog, About Me 라는 문구 => 내비게이션 바 안에 배치
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 2-1. Post(게시물)가 정상적으로 보이는지
        # => 맨 처음에는 Post가 없음: 0개
        self.assertEqual(Post.objects.count(), 0)

        # 2-2. main area에 문구 배치 : '아직 게시물이 없습니다.'
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다.', main_area.text)

        # 3-1. Post 2개 생성 => 검사
        post_001 = Post.objects.create(
            title='첫번째 포스트',
            content='첫번째 포스트입니다.' #'장고 테스트',
        )
        post_002 = Post.objects.create(
            title='두번째 포스트',
            content='두번째 포스트입니다.',
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
