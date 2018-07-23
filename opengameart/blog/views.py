import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Comment
# Create your views here.
from .forms import CommentForm


def news_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'news.html', {'posts': posts})


def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm
    return render(request, 'news_detail.html', {'post': post, 'form': form})


def add_comment_to_post(request):
    pk = int(request.POST.get('pk'))
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author_id = request.user.id
            comment.save()

            response_data = {
                'author': comment.author,
                'text': comment.text,
                'comment_pk': comment.id,
                'created_date': str(comment.created_date.strftime('%b %d, %Y %H:%m')),
            }
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def comment_approve(request):
    try:
        pk = request.GET.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
    except Exception as ex:
        print(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})


def comment_remove(request):
    try:
        pk = request.GET.get('pk')
        action = request.GET.get('action')
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
    except Exception as ex:
        print(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})
