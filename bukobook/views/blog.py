from django.shortcuts import render, redirect
from bukobook.models import Article, Userinfo, Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import F

def index(request):
    latest_list = Article.objects.values\
    ("author__username", "author_id", "title", "body", "id", "create_time")[:5]
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
    article.pv = F('pv')+1
    article.save()
    comments = Comment.objects.filter(article_id=id)
    context = {'article': article, 'comments': comments}
    return render(request, 'blog/article.html', context)


@csrf_exempt
def update(request, id):
    article = Article.objects.filter(id=id)
    if article[0].author_id is not request.user.id:
        raise Http404("No access to this page.")
    elif request.method == 'POST':
        error = None
        info = {
            'title': request.POST['title'],
            'body': request.POST['title']
        }
        article.update(info)
        return redirect('bukobook:article', id=id)
    context = {'article': article[0]}
    return render(request, 'blog/update.html', context)

@login_required(login_url='/login')
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
        article = Article.objects.get(id=id)
        article.comments = F('comments') + 1
        article.save()
        Comment.objects.create(article_id=id, body=comment, author_id=author).save()
        return redirect('bukobook:article', id=id)
    else:
        raise Http404("This page is not exist.")

