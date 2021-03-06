from django.shortcuts import render
import logging
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import ArtUser, ArtPost, RELATIONSHIP_BLOCKED, RELATIONSHIP_FOLLOWING
from arts.models import Art
from blog.models import Comment
from chat.models import Message
from .serializers import ArtUserSerializer, ArtPostSerializer, ArtRelationshipSerializer
from .forms import ArtUserForm, UserUpdateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required


logger = logging.getLogger(__name__)


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
    if request.user.is_authenticated:
        pk = request.user.id
        art_user = get_object_or_404(ArtUser, user_id=pk)
        logger.info("User is authenticated")
        return render(request, 'home.html', {'art_user': art_user})
    else:
        logger.info("User is not authenticated")
        return render(request, 'home.html')


def look_profile(request, **kwargs):
    if request.user.is_authenticated:
        current_authenticated_user = ArtUser.objects.get(user_id=request.user.id)
        if kwargs:
            pk = kwargs["pk"]
        else:
            pk = request.user.id
        art_user = get_object_or_404(ArtUser, user_id=pk)
        follow_message = 'follow'
        block_message = 'block'
        if art_user in current_authenticated_user.get_blocking():
            block_message = 'unblock'
        if art_user in current_authenticated_user.get_following():
            follow_message = 'unfollow'
        try:
            user_profile = get_object_or_404(User, id=int(pk))
        except ValueError as err:
            logger.error(err)
            return render(request, 'user_page.html')
        return render(request, 'user_page.html', {'art_user': art_user,
                                                  'user_profile': user_profile,
                                                  'follow_message': follow_message,
                                                  'block_message': block_message})
    else:
        return render(request, 'user_page.html')


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
        # update_all_likes()
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
        # update_all_likes()
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
                current_user.save(update_picture=True)
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
        if art_user.user_avatar:
            user_image = art_user.user_avatar.url
        else:
            user_image = None
        return render(request, 'users.html', {'art_user_form': art_user_form, 'user_form': user_form,
                                              "user_image": user_image})


@login_required
def search_users(request):
    if request.method == "GET":
        search_query = request.GET.get('search_field')
        users = User.objects.filter(username__contains=search_query).filter(is_staff=False).filter(is_active=True)
        art_users = []
        # reformat this expression
        for user in users:
            art_users.append(ArtUser.objects.get(user_id=user.id))

        arts = Art.objects.filter(title__contains=search_query)
        return render(request, 'search.html', {'friends': art_users, 'arts': arts})
    return render(request, 'search.html')


@method_decorator(login_required, name='dispatch')
class CurrentUserFollowersView(generics.ListAPIView):
    """
    A view that returns a template HTML representation of a given user.
    """
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'followers.html'

    def get(self, request, *args, **kwargs):
        current_user = False
        pk = self.kwargs['pk']
        current_user_id = request.user.id
        if pk == current_user_id:
            current_user = True

        # make check if user is not art user (admin, for example)
        art_user = ArtUser.objects.get(user_id=pk)
        serializer = ArtRelationshipSerializer(art_user, many=False)
        serializer_data = serializer.data
        return Response({'data': serializer_data, 'current': current_user})


@login_required
def count_posts(request):
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        art_user = ArtUser.objects.get(user_id=pk)
        user_id = art_user.id
        posts = ArtPost.objects.filter(user_id=user_id).count()
        return JsonResponse({'count_posts': posts})


@login_required
def count_followers(request):
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        art_user = ArtUser.objects.get(user_id=pk)
        followers = art_user.get_followers().count()
        return JsonResponse({'count_followers': followers})


@login_required
def appreciate_post(request):
    """ This view is called, when like or dislike button is pressed
        And ajax query is done
    """
    actions = {
     "like": like_post,
     "dislike": dislike_post,
    }
    messages = {
     "like": 'already liked',
     "dislike": 'already disliked',
    }
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        art_user = ArtUser.objects.get(user_id=pk)
        art_pk = int(request.GET.get('art_pk'))
        art = Art.objects.get(id=art_pk)
        action = request.GET.get('action')
        if action not in actions:
            return JsonResponse({'message': 'error', 'likes': 0})
        message_status, likes = actions[action](art_user, art, art_pk)
        if message_status:
            message = messages[action]
        else:
            message = 'success'
        return JsonResponse({'message': message, 'likes': likes})


def like_post(art_user, art, art_pk):
    """ This view is called, when like button is pressed And ajax query is done """
    liked = False
    if art_user.liked_arts.filter(id=art_pk).count():
        liked = True
    else:
        art.likes += 1
        art.save()
        art_user.liked_arts.add(art)
        art_user.save()
    return liked, art.likes


def dislike_post(art_user, art, art_pk):
    """ This view is called, when dislike button is pressed And ajax query is done"""
    disliked = False
    if not art_user.liked_arts.filter(id=art_pk).count():
        disliked = True
    else:
        art.likes -= 1
        art.save()
        art_user.liked_arts.remove(art)
        art_user.save()
    return disliked, art.likes


# @login_required
# def show_likes_in_post(request):
#     """ This view is already made to show quantity of likes"""
#     # Deprecated and useless
#     if request.method == "GET":
#         user_id = request.user.id
#         current_art_user = ArtUser.objects.get(user_id=user_id)
#         art_pk = int(request.GET.get('art_pk'))
#         art = Art.objects.get(id=art_pk)
#         likes = art.artuser_set.count()
#         liked = False
#         if current_art_user.liked_arts.get(id=art_pk):
#             liked = True
#         return JsonResponse({'likes': likes, 'liked': liked})


def update_likes(art_id):
    """ Update likes in 1 art """
    quantity_of_likes = ArtUser.objects.filter(liked_arts__id=art_id).count()
    art = Art.objects.get(id=art_id)
    art.likes = quantity_of_likes
    art.save(update_picture=False)
    return quantity_of_likes


def update_all_likes():
    """ Syncs all liked items in ArtUser collection with Arts in database """
    arts = [art for art in Art.objects.all()]
    for art in arts:
        update_likes(art.id)


def follow_user(art_user, following_user):
    """ This view is called, when follow button is pressed """
    if following_user in art_user.get_blocking():
        art_user.remove_relationship(following_user, RELATIONSHIP_BLOCKED)
    already_followed = False
    if following_user in art_user.get_following():
        already_followed = True
    else:
        art_user.add_relationship(following_user, RELATIONSHIP_FOLLOWING)

    return already_followed


def unfollow_user(art_user, following_user):
    """ This view is called, when unfollow button is pressed """
    already_unfollowed = False
    if following_user not in art_user.get_following():
        already_unfollowed = True
    else:
        art_user.remove_relationship(following_user, RELATIONSHIP_FOLLOWING)

    return already_unfollowed


def block_user(art_user, blocking_user):
    """ This view is called, when block button is pressed """
    if blocking_user in art_user.get_following():
        art_user.remove_relationship(blocking_user, RELATIONSHIP_FOLLOWING)
    already_blocked = False
    if blocking_user in art_user.get_blocking():
        already_blocked = True
    else:
        art_user.add_relationship(blocking_user, RELATIONSHIP_BLOCKED)

    return already_blocked


def unblock_user(art_user, blocking_user):
    """ This view is called, when unblock button is pressed """
    already_unblocked = False
    if blocking_user not in art_user.get_blocking():
        already_unblocked = True
    else:
        art_user.remove_relationship(blocking_user, RELATIONSHIP_BLOCKED)

    return already_unblocked


@login_required
def set_relationship(request):
    """ This view is called, when every relation button is pressed
        And ajax query is done
    """
    actions = {
        'follow': follow_user,
        'unfollow': unfollow_user,
        'block': block_user,
        'unblock': unblock_user,
    }
    messages = {
        'follow': 'already followed',
        'unfollow': 'already unfollowed',
        'block': 'already blocked',
        'unblock': 'already unblocked',
    }
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        art_user = ArtUser.objects.get(user_id=pk)
        relate_pk = int(request.GET.get('relate_pk'))
        relate_user = ArtUser.objects.get(id=relate_pk)
        action = request.GET.get('action')
        if action not in actions:
            return JsonResponse({'message': 'error'})
        message_status = actions[action](art_user, relate_user)
        if message_status:
            message = messages[action]
        else:
            message = 'success'
        return JsonResponse({'message': message})


def delete_objects_for_user(user_id):
    try:
        art_user_id = ArtUser.objects.get(user_id=user_id).id
        # remove comments
        Comment.objects.filter(author_id=user_id).delete()
        # remove art posts and arts
        Art.objects.filter(owner_id=art_user_id).delete()
        # remove likes, news, chats and relationships
        ArtUser.objects.filter(user_id=user_id).delete()
        update_all_likes()
        Message.objects.filter(receiver__id=user_id).delete()
        Message.objects.filter(sender__id=user_id).delete()
        return True
    except Exception as ex:
        logger.error(ex)
        return False


@login_required
def remove_account(request):
    delete_objects_for_user(request.user.id)  # optional
    User.objects.filter(pk=request.user.pk).update(is_active=False, email='')
    return HttpResponseRedirect(reverse('logout'))
