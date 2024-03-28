from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm, CommentForm, UserForm
from .models import Post, Category, User, Comment
from .constants import NUMBER_OF_PUBLICATIONS


def get_paginator(request, queryset, number_of_pages=NUMBER_OF_PUBLICATIONS):
    """Функция для получения объектов пагинатора"""
    paginator = Paginator(queryset, number_of_pages)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """Отображение ленты публикаций"""
    posts = Post.objects.get_published()
    page_obj = get_paginator(request, posts)
    return render(request, 'blog/index.html', {'page_obj': page_obj})


def category_posts(request, category_slug):
    """Отображение категорий"""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = category.posts.get_published()
    page_obj = get_paginator(request, posts)
    return render(request, 'blog/category.html',
                  {'category': category, 'page_obj': page_obj})


def post_detail(request, post_id):
    """Отображение карточки публикации"""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        post = get_object_or_404(Post.objects.get_published(
        ).filter(id=post_id))
    form = CommentForm(request.POST or None)
    comments = Comment.objects.select_related(
        'author').filter(post=post)
    return render(request, 'blog/detail.html',
                  {'post': post, 'form': form, 'comments': comments})


@login_required
def create_post(request):
    """Создание публикаций"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    """Редактирование публикаций"""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/create.html', {'form': form})


@login_required
def delete_post(request, post_id):
    """Удаление публикаций"""
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('blog:post_detail', post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')
    return render(request, 'blog/create.html', {'form': form})


@login_required
def create_comment(request, post_id):
    """Добавление комментария к публикациям"""
    post = get_object_or_404(Post, id=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('blog:post_detail', post_id)


@login_required
def edit_comment(request, post_id, comment_id):
    """Редактирование комментария к публикациям"""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)
    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html',
                  {'comment': comment, 'form': form})


@login_required
def delete_comment(request, post_id, comment_id):
    """Удаление комментария к публикациям"""
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author:
        return redirect('blog:post_detail', post_id)
    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id)
    return render(request, 'blog/comment.html', {'comment': comment})


def profile(request, username):
    """Отображение профиля пользователя"""
    profile = get_object_or_404(User, username=username)
    posts = Post.objects.get_posts().filter(author=profile)
    if request.user != profile:
        posts = Post.objects.get_published().filter(author=profile)
    page_obj = get_paginator(request, posts)
    return render(request, 'blog/profile.html',
                  {'profile': profile, 'page_obj': page_obj})


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    profile = get_object_or_404(User, username=request.user)
    form = UserForm(request.POST or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', request.user)
    return render(request, 'blog/user.html', {'form': form})
