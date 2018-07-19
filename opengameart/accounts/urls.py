from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import (
    password_change,
    password_change_done,
)
from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^posts/$', views.UserArtPostView.as_view(), name='art_posts_list'),
    path('posts/<int:pk>', views.CurrentUserArtPostView.as_view(), name='art_posts_list_current'),
    path('users/<int:pk>/', views.configure_user, name='configure_user'),
    url('search/$', views.search_users, name='search_users'),
    path('followers/<int:pk>', views.CurrentUserFollowersView.as_view(), name='show_followers'),
    url(r'^password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),

    url(r'^ajax/count_posts/$', views.count_posts, name='count_posts'),
    url('^ajax/like/$', views.like_post, name='like_post'),
    url('^ajax/dislike/$', views.dislike_post, name='dislike_post'),
    url('^ajax/show_likes/$', views.show_likes_in_post, name='show_likes_in_post'),
]
# path for post, url for get are suitable
