from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic, View
from .models import ArtUser, ArtPost
from .serializers import ArtUserSerializer, ArtPostSerializer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_member_required, name='dispatch')
class ListUser(generics.ListCreateAPIView):
    queryset = ArtUser.objects.all()
    serializer_class = ArtUserSerializer


def home(request):
    numbers_list = range(1, 1000)

    page = request.GET.get('page', 1)

    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {'numbers': numbers})


@method_decorator(login_required, name='dispatch')
class UserArtPostView(APIView):
    """
    A class based view for creating and fetching ALL user arts
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'post.html'

    # renderer_classes = (JSONRenderer, )

    def get(self, format=None):
        """
        Get all the student records
        :param format: Format of the users posts to return to
        :return: Returns a list of users posts
        """
        posts = ArtPost.objects.all()
        serializer = ArtPostSerializer(posts, many=True)
        return Response({'posts': serializer.data})

    def post(self, request):
        """
        Create a student record
        :param request: Request object for creating art post
        :return: Returns a user record
        """
        serializer = ArtPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error_messages,
                        status=status.HTTP_400_BAD_REQUEST)


@method_decorator(login_required, name='dispatch')
class CurrentUserArtPostView(generics.ListAPIView):
    """
    A view that returns a template HTML representation of a given user.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        art_posts = ArtPost.objects.filter(user__user_id=pk)
        serializer = ArtPostSerializer(art_posts, many=True)
        return Response({'posts': serializer.data})


@login_required
def configure_user(request, **kwargs):
    return render(request, 'users.html')
