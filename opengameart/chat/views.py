import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from django.contrib.auth.models import User
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from accounts.models import ArtUser


logger = logging.getLogger(__name__)


# Create your views here.
def get_list_of_users_ids(current_user_id):
    art_user = ArtUser.objects.get(user_id=current_user_id)
    friends = art_user.get_friends()
    friends_ids = []
    friends_avatars = {}
    for friend in friends:
        friends_ids.append(int(friend.user_id))
        if friend.user_avatar:
            friends_avatars.update({friend.user_id: friend.user_avatar.url})
        else:
            friends_avatars.update({friend.user_id: None})
    return friends_ids, friends_avatars


@login_required
def chat_view(request):
    if request.method == "GET":
        current_user_id = request.user.id
        friends_ids, friends_avatars = get_list_of_users_ids(current_user_id)
        users = User.objects.filter(id__in=friends_ids)
        users = [{'user': users[i], 'avatar': friends_avatars[str(users[i].id)]} for i in range(users.count())]
        # users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat.html',
                      {'users': users})


@login_required
def message_view(request, sender, receiver):
    if request.method == "GET":
        current_user_id = request.user.id
        friends_ids, friends_avatars = get_list_of_users_ids(current_user_id)
        users = User.objects.filter(id__in=friends_ids)
        users = [{'user': users[i], 'avatar': friends_avatars[str(users[i].id)]} for i in range(users.count())]
        sender_art_user = ArtUser.objects.get(user_id=(str(sender)))
        if sender_art_user.user_avatar:
            sender_avatar = sender_art_user.user_avatar.url
        else:
            sender_avatar = None
        return render(request, "messages.html",
                      {'users': users,
                       'receiver': User.objects.get(id=receiver),
                       'receiver_avatar': friends_avatars[str(receiver)],
                       'sender_avatar': sender_avatar,
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


@login_required
@csrf_exempt
def user_list(request, pk=None):
    """
    List all available users, or create a new message.
    """
    if request.method == 'GET':
        friends_avatars = {}
        if pk:
            users = User.objects.filter(id=pk)
        else:
            try:
                current_user_id = request.user.id
                friends_ids, friends_avatars = get_list_of_users_ids(current_user_id)
                users = User.objects.filter(id__in=friends_ids)
                # users = [{'user': users[i], 'avatar': friends_avatars[str(users[i].id)]} for i in range(
                # users.count())]
            except Exception as ex:
                logger.error(ex)
                users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse({'data': serializer.data, 'avatars': friends_avatars}, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@login_required
def get_unread_messages(request):
    """ Quantity of all messages, which are not read"""
    if request.method == "GET":
        pk = int(request.GET.get('pk'))
        user = User.objects.get(id=pk)
        messages = Message.objects.filter(receiver=user).filter(is_read=False).count()
        return JsonResponse({'count_messages': messages})
