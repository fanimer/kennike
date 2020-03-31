from django.shortcuts import render, redirect
from bukobook.models import Article, Userinfo, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import F

def index(request):
    latest_list = Article.objects.values\
    ("author__username", "author_id", "title", "body", "id", "create_time").order_by('-create_time')
    context = {'latest_list': latest_list}
    return render(request, 'blog/index.html', context)

@csrf_exempt
@login_required(login_url='/login')
def create_article(request):
    if request.method == 'POST':
        error = None
        title = request.POST['title']
        body = request.POST['body']
        author = request.user.id
        if title is None:
            error = 'Title is empty.'
        elif body is None:
            error = 'Body is empty.'
        if error is None:
            Article.objects.create(title=title, body=body, author_id=author).save()
            user = Userinfo.objects.get(id=author)
            user.publish = F('publish') + 1
            user.save()
            return redirect('bukobook:index')
        else:
            messages.add_message(request, messages.INFO, error)
    return render(request, 'blog/create.html')

def read_article(request, id):
    article = Article.objects.get(id=id)
    article.pv = F('pv') + 1
    article.save()
    comments = Comment.objects.filter(article_id=id, tag="C")
    for comment in comments:
        comment.reply = Comment.objects.filter(article_id=id, floor=comment.id, tag="R").order_by('-create_time')[:3]
    context = {'article': article, 'comments': comments}
    return render(request, 'blog/article.html', context)

@csrf_exempt
def update(request, id):
    article = Article.objects.get(id=id)
    if article.author_id is not request.user.id:
        raise Http404("No access to this page.")
    elif request.method == 'POST':
        error = None
        article.title =  request.POST['title']
        article.body =  request.POST['body']
        article.save()
        return redirect('bukobook:article', id=id)
    context = {'article': article}
    return render(request, 'blog/update.html', context)

def personal(request, id):
    user = Userinfo.objects.get(id=id)
    articles = Article.objects.filter(author_id=id)
    context = {'user': user, 'articles': articles}
    return render(request, 'blog/personal.html', context)

@csrf_exempt
def delete(request, id):
    if request.method == 'POST':
        Article.objects.get(id=id).delete()
        return redirect('bukobook:index')
    else:
        raise Http404("This page is not exist.")

@csrf_exempt
def submit_comment(request, id):
    if request.method == 'POST':
        comment = request.POST['comment']
        author = request.user.id
        if comment:
            Comment.objects.create(article_id=id, body=comment,
                                   author_id=author).save()
        else:
            error = 'Comment is emply.'
            messages.add_message(request, messages.INFO, error)
        return redirect('bukobook:article', id=id)
    else:
        raise Http404("This page is not exist.")

@csrf_exempt
def submit_reply(request, id):
    if request.method == 'POST':
        body = request.POST['reply']
        author= request.user.id
        floor = request.COOKIES.get('floor')
        reply_to = request.COOKIES.get('reply_to')
        tag = 'R'
        if body:
            Comment.objects.create(article_id=id, body=body,
                                   author_id=author, floor=floor,
                                   reply_to=reply_to, tag=tag).save()
        else:
            error = 'Comment is emply.'
            messages.add_message(request, messages.INFO, error)
        return redirect('bukobook:article', id=id)
    else:
        raise Http404("This page is not exist.")

