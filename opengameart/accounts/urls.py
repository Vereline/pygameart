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
    path('users_profile/<int:pk>/', views.look_profile, name='user_profile'),
    url('search/$', views.search_users, name='search_users'),
    url('remove/$', views.remove_account, name='remove_account'),
    path('followers/<int:pk>', views.CurrentUserFollowersView.as_view(), name='show_followers'),
    url(r'^password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),

    url(r'^ajax/count_posts/$', views.count_posts, name='count_posts'),
    url(r'^ajax/count_followers/$', views.count_followers, name='count_followers'),
    url('^ajax/appreciate/$', views.appreciate_post, name='appreciate_post'),
    # url('^ajax/show_likes/$', views.show_likes_in_post, name='show_likes_in_post'),
    url('^ajax/set_relationship/$', views.set_relationship, name='set_relationship'),
]
# path for post, url for get are suitable
