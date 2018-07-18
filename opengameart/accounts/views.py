from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import generic
from .models import ArtUser, ArtPost
from arts.models import Art
from .serializers import ArtUserSerializer, ArtPostSerializer
from .forms import ArtUserForm, UserUpdateForm
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

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        art_user = ArtUser(user_id=self.object.id)
        art_user.save(update_picture=False)
        return super().form_valid(form)


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
        update_all_likes()
        posts = ArtPost.objects.all()
        serializer = ArtPostSerializer(posts, many=True)
        return Response({'posts': serializer.data})

    def post(self, request):
        """
        Create a student record
        :param request: Request object for creating art post
        :return: Returns a user record
        """
        update_all_likes()
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
        update_all_likes()
        current_user = False
        pk = self.kwargs['pk']
        current_user_id = request.user.id
        if pk == current_user_id:
            current_user = True
        art_posts = ArtPost.objects.filter(user__user_id=pk)
        serializer = ArtPostSerializer(art_posts, many=True)
        return Response({'posts': serializer.data, 'current_user': current_user})


@login_required
def configure_user(request, pk):
    """ Change user configuration"""
    if request.method == 'POST':
        art_user_form = ArtUserForm(request.POST, request.FILES)
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if art_user_form.is_valid() and user_form.is_valid():
            current_user = ArtUser.objects.get(user_id=pk)
            current_user.description = art_user_form.cleaned_data['description']
            current_user.location = art_user_form.cleaned_data['location']
            current_user.birth_date = art_user_form.cleaned_data['birth_date']
            current_user.art_direction = art_user_form.cleaned_data['art_direction']
            if art_user_form.cleaned_data['user_avatar']:
                current_user.user_avatar = art_user_form.cleaned_data['user_avatar']
                current_user.save()
            else:
                current_user.save(update_picture=False)

            user = User.objects.get(id=pk)
            user.first_name = user_form.cleaned_data['first_name']
            user.last_name = user_form.cleaned_data['last_name']
            user.username = user_form.cleaned_data['username']
            user.email = user_form.cleaned_data['email']
            user.save()

            return HttpResponseRedirect('/')
    else:
        art_user = get_object_or_404(ArtUser, user_id=pk)
        art_user_form = ArtUserForm(instance=art_user)
        user = get_object_or_404(User, id=pk)
        user_form = UserUpdateForm(instance=user)
        return render(request, 'users.html', {'art_user_form': art_user_form, 'user_form': user_form})


@login_required
def search_users(request):
    if request.method == "GET":
        search_query = request.GET.get('search_field')
        users = User.objects.filter(username__contains=search_query).filter(is_staff=False)
        arts = Art.objects.filter(title__contains=search_query)
        return render(request, 'search.html', {'friends': users, 'arts': arts})
    return render(request, 'search.html')


@login_required
def show_friends(request, **kwargs):
    return render(request, 'friends.html')


@login_required
def count_posts(request):
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        art_user = ArtUser.objects.get(user_id=pk)
        user_id = art_user.id
        posts = ArtPost.objects.filter(user_id=user_id)
        number = [post for post in posts].__len__()
        return JsonResponse({'count_posts': number})


@login_required
def like_post(request):
    """ This view is called, when like button is pressed
        And ajax query is done
    """
    post_is_liked = False
    likes = 0
    liked = True
    if post_is_liked:
        return JsonResponse({'likes': likes, 'liked': liked})

    return JsonResponse({'likes': likes, 'liked': liked})


@login_required
def show_likes_in_post(request):
    """ This view is already made to show quantity of likes"""
    # Deprecated and useless
    if request.method == "GET":
        user_id = request.user.id
        current_art_user = ArtUser.objects.get(user_id=user_id)
        art_pk = int(request.GET.get('art_pk'))
        art = Art.objects.get(id=art_pk)
        likes = art.artuser_set.count()
        liked = False
        if current_art_user.liked_arts.get(id=art_pk):
            liked = True
        return JsonResponse({'likes': likes, 'liked': liked})


def update_likes(art_id):
    quantity_of_likes = ArtUser.objects.filter(liked_arts__id=art_id).count()
    art = Art.objects.get(id=art_id)
    art.likes = quantity_of_likes
    art.save(update_picture=False)
    return quantity_of_likes


def update_all_likes():
    arts = [art for art in Art.objects.all()]
    for art in arts:
        update_likes(art.id)
