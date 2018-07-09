from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
# Create your views here.

from .models import Art
from .serializers import ArtSerializer
from .forms import ArtForm
import os
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class ListArt(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


@method_decorator(login_required, name='dispatch')
class DetailArt(generics.RetrieveUpdateDestroyAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


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
            art = Art(title=form.cleaned_data['title'],
                      description=form.cleaned_data['description'],
                      file=form.cleaned_data['file'])
            art.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/arts/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArtForm()
        return render(request,  'add_art.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class ArtDelete(DeleteView):
    """ Delete image by id """
    success_url = reverse_lazy('get_list_art')
    template_name = "delete_art.html"
    model = Art
    form_class = ArtForm
    fields = ('title', 'description', 'file',)


def load_sandbox(request):
    return render(request, 'sandbox.html')
