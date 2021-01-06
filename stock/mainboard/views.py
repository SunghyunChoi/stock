from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import ArticleForm, CommentForm
from .models import Article, Comment



def index(request):
    article_list = Article.objects.order_by('-create_date')
    context = {'article_list' : article_list}

    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    return render(request, 'article_list.html', context)

def detail(request, article_id):
    #article = Article.objects.get(id=article_id)
    article = get_object_or_404(Article, pk = article_id)
    context = {'article': article}
    return render(request, 'article_detail.html', context)



def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.create_date = timezone.now()
            article.save()
            return redirect('mainboard:index')
    else:
        form = ArticleForm()
    context = {'form': form}
    return render(request, 'article_form.html', context)





# def comment_create(request, article_id):
#     article = get_object_or_404(Article, pk=article_id)
#     article.comment_set.create(content=request.POST.get('content'), create_date=timezone.now())
#     return redirect('mainboard:detail', article_id=article.id)

def comment_create(request, article_id):
    
    article = get_object_or_404(Article, pk=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.create_date = timezone.now()
            comment.article = article
            comment.save()
            return redirect('mainboard:detail', article_id=article.id)
    else:
        form = CommentForm()
    context = {'article': article, 'form': form}
    return render(request, 'article_detail.html', context)