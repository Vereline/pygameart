from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from accounts.models import ArtPost, ArtUser
from accounts.serializers import ArtPostSerializer
from .models import Art
from .serializers import ArtSerializer
from .forms import ArtForm
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


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
            art.save()
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
        current_user = False
        pk = self.kwargs['pk']
        current_user_id = request.user.id
        if pk == current_user_id:
            current_user = True
        art_posts = ArtPost.objects.filter(user__user_id=pk)
        serializer = ArtPostSerializer(art_posts, many=True)
        return Response({'posts': serializer.data, 'current_user': current_user, 'first': serializer.data[0]})


def about_page(request):
    return render(request, 'about.html')


def contacts_page(request):
    return render(request, 'contacts.html')


def news_page(request):
    return render(request, 'news.html')
