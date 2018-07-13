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
    path('friends/', views.show_friends, name='show_friends'),
    url(r'^password/change/$', password_change, {
        'template_name': 'registration/password_change_form.html'},
        name='password_change'),
    url(r'^password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        name='password_change_done'),
]
# path for post, url for get are suitable
