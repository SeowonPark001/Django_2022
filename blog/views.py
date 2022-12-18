from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Post, Category, Tag, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm
from django.shortcuts import get_object_or_404
from .serializers import postSerializer

# Creates your view here.


# DRF
# class postViewSet(viewsets.ModelViewSet):
#     queryset = Post.objects.all()
#     serializer_class = postSerializer


# 16장 Comment 수정하기
# class CommentUpdate(LoginRequiredMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm
#     # comment_form
#
#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated and request.user == self.get_object().author:
#             return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
#         else:
#             raise PermissionDenied  # Exception 발생


# 15장 : Form
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']  # 등록글 속성들 , 'tags' << 추가하고 다시 없애기!!!

    # post_form.html: CreateView가 (모델명)_form.html을 템플릿으로 인지

    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostCreate, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    # 폼이 올바른지 확인 (LoginRequiredMixin)
    def form_valid(self, form):
        # 요청하는 사용자 정보
        current_user = self.request.user

        # 인증된 사용자(+슈퍼유저/스탭 (UserPassesTestMixin))인 경우
        if current_user.is_authenticated and (current_user.is_superuser or current_user.is_staff):
            # 해당 사용자를 폼에 해당하는 작성자로 간주
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)
            # 태그 입력
            tags_str = self.request.POST.get('tags_str')
            if tags_str: # true: / false: 원래 애방
                tags_str = tags_str.strip()             # 문자열의 전체 앞뒤 여백 제거
                tags_str = tags_str.replace(',',';')    # [,]->[;]으로 변환 , is_created
                tag_list = tags_str.split(';')          # [;] 기준으로 문자열 분리 >> 배열
                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
            return response             # super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')   # 인증된 사용자가 아닌 경우 blog 페이지로 이동

    # (UserPassesTestMixin)
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff  # 둘 중 하나 해당 시 true 반환



# 15장 이미 존재하는 포스트 수정
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']  # 등록글 속성들, 똑같이 적기 , 'tags'
    template_name = 'blog/post_update_form.html'


    def get_context_data(self, object_list=None, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        # 태그 입력 - 기존 태그에 입력한 새 태그 추가
        if self.object.tags.exists:
            tag_str_list = list()
            for t in self.object.tags.all():
                tag_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tag_str_list)
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context

    # 요청 사용자가 권한ㅇ => 포스트 수정하기 페이지 보내기(dispatch)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # Exception 발생

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()    # 기존 태그들을 삭제 후 새 태그들 등록
        # 태그 입력
        tags_str = self.request.POST.get('tags_str')
        if tags_str:
            tags_str = tags_str.strip()             # 문자열의 전체 앞뒤 여백 제거
            tags_str = tags_str.replace(',', ';')   # [,]->[;]으로 변환 , is_created
            tag_list = tags_str.split(';')          # [;] 기준으로 문자열 분리 >> 배열
            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)
        return response



# CBV: ListView 사용 >> 포스트 목록 페이지 만들기
class PostList(ListView):
    model = Post
    # post_list.html: ListView이 (모델명)_list.html을 템플릿으로 인지
    # 매개변수 모델명_list: post_list

    ordering = '-pk'    # 최신등록순
    paginate_by = 5     # 한 페이지에 포스트 n개씩만 보여주기

    # Context 데이터 전달
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context


# 포스트 상세 페이지
class PostDetail(DetailView):
    model = Post
    # post_detail.html: ListView이 (모델명)_detail.html을 템플릿으로 인지
    # 매개변수 모델명: post

    # 13장 카테고리 context 데이터 전달
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        context['comment_form'] = CommentForm   # 추가
        return context

    # # 새 댓글 작성하기
    # def new_comment(request, pk):
    #     # 로그인한 유저인 경우
    #     if request.user.is_authenticated:
    #         post = get_object_or_404(Post, pk=pk)
    #
    #         # 요청 형식이 POST인 경우
    #         if request.method == 'POST':
    #             comment_form = CommentForm(request.POST)
    #
    #             if comment_form.is_valid():
    #                 comment = comment_form.save(commit=False)
    #                 comment.post = post
    #                 comment.author = request.user
    #                 comment.save() # 서버 model에 save
    #                 return redirect(comment.get_absolute_url()) # 해당 url로 이동
    #         # 요청 형식이 POST가 아닌 경우 : GET
    #         else:
    #             return redirect(post.get_absolute_url()) # post 상세 페이지로 이동
    #     # 로그인 X 사용자인 경우
    #     else:
    #         raise PermissionDenied


# 카테고리&태그: PostList에서도 사용ㅇ => PostDetail 안x 밖ㅇ

# 13장 다대일: Category 페이지
def category_page(request, slug):  # <- slug: 매개변수로 갖고옴
    # slug1[ERROR]: 221027강의 33:00~ 그 이후에 다시 고침...
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog/post_list.html', {
        'category': category,
        'post_list': post_list,  # 미분류 때문에 미리 변수에 할당 / Post.objects.filter(category=category)
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })


# 14장 다대다 : Tag 페이지
def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()

    return render(request, 'blog/post_list.html', {
        'tag': tag,
        'post_list': post_list,  # 미분류 때문에 미리 변수에 할당 / Post.objects.filter(category=category)
        # sidebar의 category
        'categories': Category.objects.all(),
        'no_category_post_count': Post.objects.filter(category=None).count
    })


# FBV
# def index(request):
#     # 모델명.objects.all() => 모든 post 가져오기
#     # pk 역순(-)으로 정렬(나열)
#     posts = Post.objects.all().order_by('-pk')
#
#     return render(
#         request,
#         'blog/index.html',  # 사용할 템플릿
#         {
#             'posts': posts  # 템플릿에 넘겨줄 값 => 딕셔너리 형태 { 'key': value }
#         }
#     )


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             'post': post,
#         }
#     )
