from django.shortcuts import render
from rest_framework import generics
# Create your views here.

from .models import Art
from .serializers import ArtSerializer


class ListTodo(generics.ListCreateAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset = Art.objects.all()
    serializer_class = ArtSerializer
