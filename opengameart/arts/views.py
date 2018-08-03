import json
import os
import logging
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from rest_framework import generics
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from accounts.models import ArtPost, ArtUser
from accounts.serializers import ArtPostSerializer
from .models import Art, ArtComment
from .serializers import ArtSerializer
from .forms import ArtForm, ArtCommentForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


logger = logging.getLogger(__name__)


@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class ListArt(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


@method_decorator(staff_member_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class DetailArt(generics.RetrieveUpdateDestroyAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


@staff_member_required
@login_required
def image_view(request, pk):
    art = get_object_or_404(Art, pk)
    img = '<img src={src} width="500px"/>'.format(src=os.getcwd()+art.file.url)
    return HttpResponse(img)


@login_required
def get_art(request):
    """ Add image to db """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ArtForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            current_art_user = ArtUser.objects.get(user_id=request.user.id)
            art = Art(title=form.cleaned_data['title'],
                      description=form.cleaned_data['description'],
                      file=form.cleaned_data['file'],
                      owner_id=current_art_user.id)
            art.save(update_picture=True)
            art_post = ArtPost(art_id=art.id, user_id=current_art_user.id)
            art_post.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArtForm()
        return render(request,  'add_art.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ArtDelete(DeleteView):
    """ Delete image by id """
    success_url = reverse_lazy('art_posts_list')
    template_name = "delete_art.html"
    model = Art
    form_class = ArtForm
    fields = ('title', 'description', 'file',)

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        art_post = ArtPost.objects.get(art_id=self.object.id)
        art_post.delete()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@login_required
def load_sandbox(request):
    return render(request, 'sandbox.html')


@method_decorator(login_required, name='dispatch')
class LoadGallery(generics.ListAPIView):
    """
    A view that returns a template HTML representation of a given user.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'gallery.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        current_user_id = request.user.id
        current_user = True if pk == current_user_id else False
        art_posts = ArtPost.objects.filter(user__user_id=pk)
        serializer = ArtPostSerializer(art_posts, many=True)
        return Response({'posts': serializer.data, 'current_user': current_user, 'first': serializer.data[0]})


def about_page(request):
    return render(request, 'about.html')


@login_required
def art_detailed(request, pk):
    art_post = ArtPost.objects.get(art__id=pk)
    serializer = ArtPostSerializer(art_post)
    form = ArtCommentForm()
    return render(request, 'art_detail.html', {'form': form, 'post': serializer.data})


@login_required
def add_art_comment_to_post(request):
    pk = int(request.POST.get('pk'))
    art = get_object_or_404(Art, pk=pk)
    if request.method == "POST":
        form = ArtCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.art = art
            comment.author_id = request.user.id
            art_user = ArtUser.objects.get(user_id=request.user.id)
            if art_user.user_avatar:
                comment.author_avatar = art_user.user_avatar.url
            else:
                comment.author_avatar = ''
            comment.save()

            response_data = {
                'author': comment.author,
                'text': comment.text,
                'comment_pk': comment.id,
                'created_date': str(comment.created_date.strftime('%b %d, %Y %H:%m')),
                'user_image': comment.author_avatar
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


@login_required
def art_comment_approve(request):
    try:
        pk = request.GET.get('pk')
        comment = get_object_or_404(ArtComment, pk=pk)
        comment.approve()
    except Exception as ex:
        logger.error(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})


@login_required
def art_comment_remove(request):
    try:
        pk = request.GET.get('pk')
        # action = request.GET.get('action')
        comment = get_object_or_404(ArtComment, pk=pk)
        comment.delete()
    except Exception as ex:
        logger.error(ex)
        return JsonResponse({'message': "fail"})
    return JsonResponse({'message': "success"})


@login_required
def save_comment_form(request, form, comment_pk, template_name):
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


@login_required
def art_comment_edit(request, pk):
    comment = get_object_or_404(ArtComment, pk=pk)
    if request.method == 'POST':
        form = ArtCommentForm(request.POST, instance=comment)
    else:
        form = ArtCommentForm(instance=comment)
    return save_comment_form(request, form, pk, 'partial_comment_edit.html')
