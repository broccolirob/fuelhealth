from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from apps.news.models import Article, Comment
from apps.news.forms import ArticleForm, ArticleSearchForm, RegistrationForm, CommentForm
from apps.news.utils import top_articles


def data(request):
    return render(request, 'datascreen.html')


# The same pagination code is used in many views. You could make this DRYer by creating a function
# which takes in the paginator and returns the queryset
def index(request):
    article_list = top_articles()
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            # This form saving code for your ArticleForm is also repeated in multiple views
            # You could move this into the save() of the form and also pass in request.user
            # so it can handle liking the article.
            article = form.save(commit=False)
            article.moderator = request.user
            article.save()
            user = request.user
            user.liked_articles.add(article)
            user.save()
            return redirect('new')
        else:
            messages.error(request, "Something went wrong with your submission, please try again.")
    else:
        form = ArticleForm()
    data = {'article_list': articles, 'form': form}
    return render(request, 'news.html', data)


def new(request):
    article_list = Article.objects.order_by('-created_at')
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    if request.method == 'POST':
            form = ArticleForm(request.POST)
            if form.is_valid():
                article = form.save(commit=False)
                article.moderator = request.user
                article.save()
                user = request.user
                user.liked_articles.add(article)
                user.save()
                return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'news.html', {'article_list': articles,'form': form})


def article_search(request):
    form = ArticleSearchForm(request.GET)
    articles = form.search()
    return render(request, 'article_search.html', {'articles': articles})


@login_required()
def vote(request):
    article = get_object_or_404(Article, pk=request.POST.get('article'))
    article.points += 1
    article.save()
    # You may want to just make a method on your Profile model called like_article(article) for you to reuse.
    user = request.user
    user.liked_articles.add(article)
    user.save()
    return HttpResponse()


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    data = {'form': form}
    return render(request, 'registration/register.html', data)


def user_articles(request):
    user = request.user
    article_list = user.moderated_articles.all()
    paginator = Paginator(article_list, 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    data = {'user_articles': articles}
    return render(request, 'user_articles.html', data)


def user_comments(request):
    user = request.user
    user_comments = user.comments_made.all()
    paginator = Paginator(user_comments, 10)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    data = {'user_comments': comments}
    return render(request, 'user_comments.html', data)

@login_required
def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    # can't you just get comments from the article? article.comments.order_by("-created_at")
    new_comments = Comment.objects.filter(article_id=article_id).order_by("-created_at")
    top_comments = Comment.objects.filter(article_id=article_id).order_by("points")
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(article=article,
                                             body=form.cleaned_data['body'],
                                             author=request.user,
                                             points=1)
            comment.save()
            return redirect('article_detail', article_id)
    else:
        form = CommentForm()
    data = {'article': article, 'new_comments': new_comments, 'top_comments': top_comments, 'form': form}
    return render(request, 'article_detail.html', data)


# Will need try/excepts on these incase a bad ID is sent up
def delete_article(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.delete()
    return redirect('user_articles')


def delete_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    comment.delete()
    return redirect('user_comments')
