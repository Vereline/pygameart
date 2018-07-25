from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from django.contrib.auth.models import User
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib.auth.decorators import login_required
from accounts.models import ArtUser


# Create your views here.
def get_list_of_users_ids(current_user_id):
    art_user = ArtUser.objects.get(user_id=current_user_id)
    friends = art_user.get_friends()
    friends_ids = []
    for friend in friends:
        friends_ids.append(int(friend.user_id))
    return friends_ids


@login_required
def chat_view(request):
    if request.method == "GET":
        current_user_id = request.user.id
        friends_ids = get_list_of_users_ids(current_user_id)
        users = User.objects.filter(id__in=friends_ids)
        # users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat.html',
                      {'users': users})


@login_required
def message_view(request, sender, receiver):
    if request.method == "GET":
        current_user_id = request.user.id
        friends_ids = get_list_of_users_ids(current_user_id)
        users = User.objects.filter(id__in=friends_ids)
        return render(request, "messages.html",
                      {'users': users,
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


@login_required
@csrf_exempt
def user_list(request, pk=None):
    """
    List all available users, or create a new message.
    """
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            try:
                current_user_id = request.user.id
                friends_ids = get_list_of_users_ids(current_user_id)
                users = User.objects.filter(id__in=friends_ids)
            except Exception as ex:
                print(ex)
                users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

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
