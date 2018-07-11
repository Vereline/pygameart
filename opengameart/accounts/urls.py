from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    url(r'^posts/$', views.UserArtPostView.as_view(), name='art_posts_list'),
]
