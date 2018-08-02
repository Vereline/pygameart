import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from .models import Post, Comment
# Create your views here.
from .forms import CommentForm
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import logging


logger = logging.getLogger(__name__)


def news_list(request):
    post_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    paginator = Paginator(post_list, 5)

    page = request.GET.get('page')
    try:
        posts = paginator.get_page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    # Get the index of the current page
    index = posts.number - 1  # edited to something easier without index
    # This value is maximum index of pages, so the last page - 1
    max_index = len(paginator.page_range)
    # calculate where to slice the list
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index
    # Get a new page range.
    page_range = list(paginator.page_range)[start_index:end_index]

    return render(request, 'news.html', {'posts': posts, 'page_range': page_range})


def news_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()
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


# TODO: rewrite all ajax backend methods (which return Json response) with usage of Rest framework serializers
def comment_approve(request):
    try:
        pk = request.GET.get('pk')
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
    except Exception as ex:
        logger.error(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})


def comment_remove(request):
    try:
        pk = request.GET.get('pk')
        # action = request.GET.get('action')
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
    except Exception as ex:
        logger.error(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})


# @login_required
# def comment_edit(request):
#     try:
#         pk = request.GET.get('pk')
#         # action = request.GET.get('action')
#         comment = get_object_or_404(Comment, pk=pk)
#         # comment.edit()
#     except Exception as ex:
#         print(ex)
#         return JsonResponse({'message': "fail"})
#     return JsonResponse({'message': "success"})

def save_comment_form(request, form, comment_pk,template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            data['new_text'] = form.cleaned_data['text']
            data['id'] = comment_pk
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    try:
        data['html_form'] = render_to_string(template_name, context, request=request)
        data['message'] = 'success'
    except Exception as ex:
        data['message'] = 'fail'
        logger.error(ex)
    return JsonResponse(data)


def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
    else:
        form = CommentForm(instance=comment)
    return save_comment_form(request, form, pk, 'partial_comment_edit.html')
