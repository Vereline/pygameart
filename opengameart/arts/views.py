from django.shortcuts import render
from rest_framework import generics
from django.http import HttpResponse
# Create your views here.

from .models import Art
from .serializers import ArtSerializer
import os


class ListArt(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


class DetailArt(generics.RetrieveUpdateDestroyAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


def image_view(request, pk):
    art = Art.objects.get(id=pk)
    img = '<img src={src} width="500px"/>'.format(src=os.getcwd()+art.file.url)
    return HttpResponse(img)
